#!/usr/bin/env python3
"""Freeze and mechanically extract explicitly tagged AimPL conjectures.

This is a source-audit utility.  It never grants strict-conjecture credit.
The live site is used only to fetch section pages not already present in the
fixed snapshot directory; existing bytes are never overwritten. Repository
checks replay extraction exclusively from the content-addressed snapshot.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import email.utils
import gzip
import hashlib
import html
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request


SCHEMA = "awesome-theorems/aimpl-explicit-conjecture-source-audit/1"
BASE_URL = "http://aimpl.org"
LICENSE_URL = "http://creativecommons.org/licenses/by-sa/3.0/"
LICENSE_SPDX = "CC-BY-SA-3.0"
ALL_DATA_RE = re.compile(r"^\s*var allData = (\{.*\});\s*$", re.MULTILINE)

REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR_REL = Path("Docs/catalog/v5/sources/aimpl")
SOURCE_ASSET_REL = SOURCE_DIR_REL / "aimpl-source-snapshot.tar.gz"
SOURCE_MANIFEST_REL = SOURCE_DIR_REL / "source-manifest.json"
CANDIDATES_REL = SOURCE_DIR_REL / "candidates.jsonl"
ASSET_RECEIPT_REL = SOURCE_DIR_REL / "asset-receipt.json"


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def iso_mtime(path: Path) -> str:
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat()


def parse_all_data(path: Path) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8")
    matches = ALL_DATA_RE.findall(text)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one allData object in {path}, got {len(matches)}")
    data = json.loads(matches[0])
    if not isinstance(data, dict) or not all(isinstance(v, dict) for v in data.values()):
        raise ValueError(f"invalid allData object in {path}")
    return data


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_text(value: str | None) -> str:
    parser = TextExtractor()
    parser.feed(value or "")
    parser.close()
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def line_containing(path: Path, needle: str) -> int:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return number
    raise ValueError(f"required source evidence {needle!r} not found in {path}")


def validate_rights_and_citation(path: Path) -> tuple[int, int]:
    license_line = line_containing(path, LICENSE_URL)
    citation_line = line_containing(path, "Cite this as:")
    text = path.read_text(encoding="utf-8")
    if "All information is released under" not in text:
        raise ValueError(f"license scope sentence missing in {path}")
    return license_line, citation_line


@dataclasses.dataclass(frozen=True)
class Section:
    list_name: str
    list_title: str
    list_category: str
    list_id: str
    list_rev: str
    list_author: str | None
    section_id: str
    section_rev: str
    section_title: str
    section_intro: str
    list_pos: int
    source_list_pos: int | None
    section_number: str
    root_path: Path

    @property
    def url(self) -> str:
        return f"{BASE_URL}/{self.list_name}/{self.list_pos}/"

    def page_path(self, audit_dir: Path) -> Path:
        return audit_dir / "pages" / self.list_name / f"{self.list_pos}.html"


def discover_roots(audit_dir: Path) -> tuple[list[dict], list[Section]]:
    roots: list[dict] = []
    sections: list[Section] = []
    seen_lists: set[str] = set()
    for path in sorted(audit_dir.glob("root_*.html")):
        data = parse_all_data(path)
        lists = [v for v in data.values() if v.get("type") == "list"]
        if not lists:
            continue  # a pre-fetched section page, e.g. root_gemscombin_7.html
        if len(lists) != 1:
            raise ValueError(f"expected one list object in {path}, got {len(lists)}")
        listing = lists[0]
        name = listing.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(f"list without stable name in {path}")
        if name in seen_lists:
            raise ValueError(f"duplicate root for list {name}")
        seen_lists.add(name)
        root_row = {
            "list_name": name,
            "list_id": listing.get("_id"),
            "list_rev": listing.get("_rev"),
            "title": listing.get("title", ""),
            "category": listing.get("category", ""),
            "author": listing.get("author"),
            "snapshot_member_path": path.name,
            "source_size_bytes": path.stat().st_size,
            "source_sha256": sha256_file(path),
            "fixed_input_mtime_utc": iso_mtime(path),
            "license_evidence_line_one_based": validate_rights_and_citation(path)[0],
            "citation_evidence_line_one_based": validate_rights_and_citation(path)[1],
        }
        roots.append(root_row)
        items = [v for v in data.values() if v.get("type") == "section"]
        # list_pos inside old Couch objects is sometimes stale or duplicated.
        # The rendered root page is authoritative for the actual section route.
        rendered_routes = re.findall(
            r'<li\s+data-id="([^"]+)"\s+class="section">.*?'
            r'<a\s+href="(\d+)/">',
            path.read_text(encoding="utf-8"),
            re.DOTALL,
        )
        route_by_id = {section_id: int(route) for section_id, route in rendered_routes}
        if len(rendered_routes) != len(items) or len(route_by_id) != len(items):
            raise ValueError(f"rendered section-route inventory mismatch in {path}")
        positions: set[int] = set()
        for item in items:
            try:
                pos = route_by_id[item.get("_id")]
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"non-integer rendered section route in {path}: {item}") from exc
            if pos <= 0 or pos in positions:
                raise ValueError(f"invalid/duplicate rendered section route {pos} in {path}")
            positions.add(pos)
            try:
                source_list_pos = int(item.get("list_pos"))
            except (TypeError, ValueError):
                source_list_pos = None
            sections.append(Section(
                list_name=name,
                list_title=listing.get("title", ""),
                list_category=listing.get("category", ""),
                list_id=listing.get("_id", ""),
                list_rev=listing.get("_rev", ""),
                list_author=listing.get("author"),
                section_id=item.get("_id", ""),
                section_rev=item.get("_rev", ""),
                section_title=item.get("title", ""),
                section_intro=item.get("intro", ""),
                list_pos=pos,
                source_list_pos=source_list_pos,
                section_number=item.get("number", ""),
                root_path=path,
            ))
    sections.sort(key=lambda s: (s.list_name, s.list_pos, s.section_id))
    roots.sort(key=lambda x: x["list_name"])
    if not roots or not sections:
        raise ValueError("no AimPL root inventory discovered")
    return roots, sections


def validate_section_page(section: Section, path: Path) -> dict[str, dict]:
    data = parse_all_data(path)
    matching = [v for v in data.values()
                if v.get("type") == "section" and v.get("_id") == section.section_id]
    if len(matching) != 1:
        raise ValueError(f"{path} does not contain expected section {section.section_id}")
    if matching[0].get("list_id") not in (None, "", section.list_name):
        raise ValueError(f"{path} list_id does not match {section.list_name}")
    validate_rights_and_citation(path)
    return data


def fetch_one(section: Section, audit_dir: Path, attempts: int = 4) -> dict:
    out = section.page_path(audit_dir)
    if out.exists():
        validate_section_page(section, out)
        return {
            "list_name": section.list_name,
            "list_pos": section.list_pos,
            "url": section.url,
            "source_path": str(out.relative_to(audit_dir)),
            "retrieval_state": "preexisting-fixed-bytes",
            "retrieved_at_utc": iso_mtime(out),
            "http_status": None,
            "http_date": None,
            "size_bytes": out.stat().st_size,
            "sha256": sha256_file(out),
        }

    # One section page was supplied with the roots under a legacy filename.
    legacy = audit_dir / f"root_{section.list_name}_{section.list_pos}.html"
    if legacy.exists():
        validate_section_page(section, legacy)
        atomic_write(out, legacy.read_bytes())
        return {
            "list_name": section.list_name,
            "list_pos": section.list_pos,
            "url": section.url,
            "source_path": str(out.relative_to(audit_dir)),
            "retrieval_state": "copied-from-provided-fixed-input",
            "provided_path": legacy.name,
            "retrieved_at_utc": iso_mtime(legacy),
            "http_status": None,
            "http_date": None,
            "size_bytes": out.stat().st_size,
            "sha256": sha256_file(out),
        }

    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(
                section.url,
                headers={"User-Agent": "awesome-theorems-source-audit/1.0 (+read-only snapshot)"},
            )
            retrieved = utc_now()
            with urllib.request.urlopen(request, timeout=45) as response:
                status = response.getcode()
                body = response.read()
                response_url = response.geturl()
                http_date = response.headers.get("Date")
                content_type = response.headers.get("Content-Type")
            if status != 200:
                raise ValueError(f"HTTP {status} for {section.url}")
            atomic_write(out, body)
            validate_section_page(section, out)
            return {
                "list_name": section.list_name,
                "list_pos": section.list_pos,
                "url": section.url,
                "response_url": response_url,
                "source_path": str(out.relative_to(audit_dir)),
                "retrieval_state": "fetched-once-and-fixed",
                "retrieved_at_utc": retrieved,
                "http_status": status,
                "http_date": http_date,
                "content_type": content_type,
                "size_bytes": len(body),
                "sha256": sha256_bytes(body),
            }
        except Exception as exc:  # retain exact failure after bounded retries
            last_error = exc
            if out.exists():
                out.unlink()
            if attempt < attempts:
                time.sleep(0.3 * (2 ** (attempt - 1)))
    raise RuntimeError(f"failed to freeze {section.url}: {last_error}")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    atomic_write(path, b"".join(canonical_bytes(row) for row in rows))


def command_fetch(audit_dir: Path, workers: int) -> None:
    roots, sections = discover_roots(audit_dir)
    existing_log = load_fetch_log(audit_dir)

    def preserved_or_fetch(section: Section) -> dict:
        prior = existing_log.get((section.list_name, section.list_pos))
        page = section.page_path(audit_dir)
        if prior is not None and page.exists():
            validate_section_page(section, page)
            if prior.get("sha256") != sha256_file(page) or prior.get("size_bytes") != page.stat().st_size:
                raise ValueError(f"fixed page bytes drifted after retrieval: {page}")
            return prior
        return fetch_one(section, audit_dir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(preserved_or_fetch, section) for section in sections]
        rows = [future.result() for future in futures]
    rows.sort(key=lambda x: (x["list_name"], x["list_pos"]))
    write_jsonl(audit_dir / "fetch-log.jsonl", rows)
    print(f"PASS fetch: roots={len(roots)} sections={len(sections)} "
          f"pages={len(rows)} fetched={sum(r['retrieval_state'] == 'fetched-once-and-fixed' for r in rows)}")


def linked_remarks(data: dict[str, dict], problem: dict) -> list[dict]:
    problem_id = problem.get("_id")
    remarks = []
    for item in data.values():
        if item.get("type") != "remark":
            continue
        path = item.get("path") or []
        if problem_id in path:
            remarks.append(item)
    remarks.sort(key=lambda x: (x.get("list_pos", 0), x.get("order", 0), x.get("_id", "")))
    return remarks


def source_line(path: Path) -> int:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "var allData = " in line:
            return number
    raise ValueError(f"allData source line not found in {path}")


def load_fetch_log(audit_dir: Path) -> dict[tuple[str, int], dict]:
    path = audit_dir / "fetch-log.jsonl"
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        result[(row["list_name"], int(row["list_pos"]))] = row
    return result


def extract(audit_dir: Path) -> tuple[list[dict], dict]:
    roots, sections = discover_roots(audit_dir)
    fetch_log = load_fetch_log(audit_dir)
    page_rows: list[dict] = []
    candidates: list[dict] = []
    problem_count = 0
    explicit_count = 0
    for section in sections:
        page = section.page_path(audit_dir)
        if not page.exists():
            raise ValueError(f"missing fixed section page: {page}; run fetch first")
        data = validate_section_page(section, page)
        page_digest = sha256_file(page)
        page_log = fetch_log.get((section.list_name, section.list_pos), {})
        page_rows.append({
            "list_name": section.list_name,
            "list_pos": section.list_pos,
            "section_id": section.section_id,
            "section_rev": section.section_rev,
            "source_object_list_pos": section.source_list_pos,
            "snapshot_member_path": str(page.relative_to(audit_dir)),
            "source_url": section.url,
            "source_size_bytes": page.stat().st_size,
            "source_sha256": page_digest,
            "all_data_line_one_based": source_line(page),
            "retrieved_at_utc": page_log.get("retrieved_at_utc", iso_mtime(page)),
            "http_date": page_log.get("http_date"),
            "license_evidence_line_one_based": validate_rights_and_citation(page)[0],
            "citation_evidence_line_one_based": validate_rights_and_citation(page)[1],
        })
        problems = [v for v in data.values() if v.get("type") == "problem"]
        problems.sort(key=lambda x: (x.get("list_pos", 0), x.get("order", 0), x.get("_id", "")))
        problem_count += len(problems)
        for problem in problems:
            if str(problem.get("tag", "")).strip().lower() != "conjecture":
                continue
            explicit_count += 1
            remarks = linked_remarks(data, problem)
            body = problem.get("body") or ""
            intro = problem.get("intro") or ""
            status = problem.get("status") or ""
            record = {
                "schema_version": SCHEMA,
                "candidate_index": explicit_count,
                "candidate_key": sha256_bytes((
                    f"{section.list_name}\0{section.section_id}\0{problem.get('_id')}\0{problem.get('_rev')}"
                ).encode("utf-8"))[:16],
                "source_record_key": (
                    f"aimpl/{section.list_name}/{section.section_id}/{problem.get('_id')}"
                    f"@{problem.get('_rev')}"
                ),
                "source_explicitly_labels_conjecture": True,
                "exact_source": {
                    "body_html": body,
                    "body_plain_text": plain_text(body),
                    "intro_html": intro,
                    "intro_plain_text": plain_text(intro),
                    "status_html": status,
                    "status_plain_text": plain_text(status),
                    "body_sha256": sha256_bytes(body.encode("utf-8")),
                    "problem_object_id": problem.get("_id"),
                    "problem_object_rev": problem.get("_rev"),
                    "problem_tag": problem.get("tag"),
                    "problem_number": problem.get("number", ""),
                    "problem_name": problem.get("name", ""),
                    "posed_by": problem.get("by") or problem.get("by_id"),
                    "json_object_binding": f"allData/{problem.get('_id')}",
                },
                "context": {
                    "list_name": section.list_name,
                    "list_title": section.list_title,
                    "list_category": section.list_category,
                    "list_id": section.list_id,
                    "list_rev": section.list_rev,
                    "list_author": section.list_author,
                    "section_title": section.section_title,
                    "section_intro_html": section.section_intro,
                    "section_intro_plain_text": plain_text(section.section_intro),
                    "section_id": section.section_id,
                    "section_rev": section.section_rev,
                    "section_list_pos": section.list_pos,
                    "section_source_object_list_pos": section.source_list_pos,
                    "section_number": section.section_number,
                    "linked_remarks": [{
                        "remark_object_id": r.get("_id"),
                        "remark_object_rev": r.get("_rev"),
                        "remark_html": r.get("remark", ""),
                        "remark_plain_text": plain_text(r.get("remark", "")),
                        "by": r.get("by") or r.get("by_id"),
                    } for r in remarks],
                },
                "source_snapshot": {
                    "collection": "AIM Problem Lists (AimPL)",
                    "source_url": section.url,
                    "source_transport_note": (
                        "The active AimPL application was served over HTTP; the HTTPS virtual host "
                        "served the unrelated aimath.org WordPress site during this audit."
                    ),
                    "snapshot_member_path": str(page.relative_to(audit_dir)),
                    "repository_source_asset_path": SOURCE_ASSET_REL.as_posix(),
                    "repository_source_manifest_path": SOURCE_MANIFEST_REL.as_posix(),
                    "repository_candidates_path": CANDIDATES_REL.as_posix(),
                    "source_sha256": page_digest,
                    "source_size_bytes": page.stat().st_size,
                    "all_data_line_one_based": source_line(page),
                    "license_evidence_line_one_based": validate_rights_and_citation(page)[0],
                    "citation_evidence_line_one_based": validate_rights_and_citation(page)[1],
                    "retrieved_at_utc": page_log.get("retrieved_at_utc", iso_mtime(page)),
                    "http_date": page_log.get("http_date"),
                },
                "rights": {
                    "license_spdx": LICENSE_SPDX,
                    "license_url": LICENSE_URL,
                    "license_scope_source_text": "All information is released under the Creative Commons Attribution-ShareAlike license.",
                    "attribution": f"AimPL: {section.list_title}, available at {BASE_URL}/{section.list_name}",
                    "share_alike_required_for_adapted_source_text": True,
                    "evidence_snapshot_member_path": str(page.relative_to(audit_dir)),
                    "evidence_repository_source_asset_path": SOURCE_ASSET_REL.as_posix(),
                    "license_evidence_line_one_based": validate_rights_and_citation(page)[0],
                    "citation_evidence_line_one_based": validate_rights_and_citation(page)[1],
                },
                "admission_boundary": {
                    "candidate_only": True,
                    "strict_credit_granted": False,
                    "automatically_accepted": False,
                    "required_reviews": [
                        "source_statement_is_complete_atomic_truth_apt_proposition",
                        "current_snapshot_does_not_mark_solved_or_resolved",
                        "high_or_medium_importance",
                        "rights_and_attribution_preserved",
                        "semantic_deduplication_against_parent_5_4_oeis_conjecturebench_and_batch",
                    ],
                    "question_sentences_must_not_be_rewritten_as_affirmative_conjectures": True,
                },
            }
            candidates.append(record)
    dated_http_responses = [
        email.utils.parsedate_to_datetime(row["http_date"]).astimezone(dt.timezone.utc).isoformat()
        for row in page_rows if row.get("http_date")
    ]
    snapshot_cutoff_utc = max(
        [row["fixed_input_mtime_utc"] for row in roots]
        + [row["retrieved_at_utc"] for row in page_rows]
        + dated_http_responses
    )
    manifest = {
        "schema_version": SCHEMA,
        "artifact": SOURCE_MANIFEST_REL.as_posix(),
        "created_at_utc": snapshot_cutoff_utc,
        "source": {
            "collection": "AIM Problem Lists (AimPL)",
            "base_url": BASE_URL,
            "root_inventory_basis": "80 fixed root/list HTML pages supplied in the audit directory",
            "license_spdx": LICENSE_SPDX,
            "license_url": LICENSE_URL,
            "citation_pattern": "AimPL: <problem-list title>, available at http://aimpl.org/<list-name>",
            "snapshot_is_content_addressed_not_upstream_versioned": True,
            "upstream_last_modified_not_exposed": True,
            "source_date_policy": (
                "The frozen HTTP response Date/retrieval timestamp establishes the audit cutoff; "
                "AimPL exposes Couch revision identifiers but no trustworthy per-object publication "
                "or last-modified date, so none is invented."
            ),
        },
        "counts": {
            "root_pages": len(roots),
            "problem_lists": len(roots),
            "section_pages": len(sections),
            "all_problem_objects": problem_count,
            "explicit_conjecture_tag_objects": explicit_count,
            "mechanical_candidates": len(candidates),
        },
        "root_pages": roots,
        "section_pages": page_rows,
        "repository_paths": {
            "source_asset": SOURCE_ASSET_REL.as_posix(),
            "source_manifest": SOURCE_MANIFEST_REL.as_posix(),
            "candidates": CANDIDATES_REL.as_posix(),
            "asset_receipt": ASSET_RECEIPT_REL.as_posix(),
        },
        "snapshot_member_path_semantics": (
            "All snapshot_member_path fields are relative to the source_asset tar archive; "
            "they are archive member identifiers, not filesystem paths."
        ),
        "scope_warning": (
            "Only problem objects whose current fixed source tag is literally 'conjecture' are candidates. "
            "Extraction does not establish completeness, atomicity, truth-aptness, current openness, "
            "importance, or semantic uniqueness, and grants zero strict credit."
        ),
    }
    return candidates, manifest


def deterministic_tar_gz(audit_dir: Path, manifest_path: Path, output: Path) -> None:
    roots, sections = discover_roots(audit_dir)
    paths = [Path(row["snapshot_member_path"])
             for row in json.loads(manifest_path.read_text())["root_pages"]]
    paths += [section.page_path(audit_dir).relative_to(audit_dir) for section in sections]
    paths = sorted(set(paths), key=lambda p: p.as_posix())
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for rel in paths:
            src = audit_dir / rel
            info = tf.gettarinfo(str(src), arcname=rel.as_posix())
            info.mtime = 0
            info.uid = info.gid = 0
            info.mode = 0o644
            info.uname = info.gname = ""
            info.pax_headers = {}
            with src.open("rb") as f:
                tf.addfile(info, f)
        manifest_bytes = manifest_path.read_bytes()
        info = tarfile.TarInfo("source-manifest.json")
        info.size = len(manifest_bytes)
        info.mtime = 0
        info.uid = info.gid = 0
        info.mode = 0o644
        info.uname = info.gname = ""
        tf.addfile(info, io.BytesIO(manifest_bytes))
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0, compresslevel=9) as gz:
        gz.write(tar_buffer.getvalue())
    atomic_write(output, compressed.getvalue())


def command_extract(audit_dir: Path, output_dir: Path) -> None:
    candidates, manifest = extract(audit_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates_path = output_dir / "candidates.jsonl"
    manifest_path = output_dir / "source-manifest.json"
    write_jsonl(candidates_path, candidates)
    atomic_write(manifest_path, canonical_bytes(manifest))
    asset_path = output_dir / "aimpl-source-snapshot.tar.gz"
    deterministic_tar_gz(audit_dir, manifest_path, asset_path)
    receipt = {
        "schema_version": SCHEMA,
        "artifact": ASSET_RECEIPT_REL.as_posix(),
        "created_at_utc": manifest["created_at_utc"],
        "source_manifest": {"path": SOURCE_MANIFEST_REL.as_posix(), "sha256": sha256_file(manifest_path),
                            "size_bytes": manifest_path.stat().st_size},
        "candidates": {"path": CANDIDATES_REL.as_posix(), "sha256": sha256_file(candidates_path),
                       "size_bytes": candidates_path.stat().st_size, "rows": len(candidates)},
        "source_asset": {"path": SOURCE_ASSET_REL.as_posix(), "sha256": sha256_file(asset_path),
                         "size_bytes": asset_path.stat().st_size},
        "strict_credit_granted": 0,
    }
    atomic_write(output_dir / "asset-receipt.json", canonical_bytes(receipt))
    print(f"PASS extract: candidates={len(candidates)} manifest={sha256_file(manifest_path)} "
          f"asset={sha256_file(asset_path)}")


def command_verify(audit_dir: Path, output_dir: Path) -> None:
    candidates, expected_manifest = extract(audit_dir)
    candidates_path = output_dir / "candidates.jsonl"
    manifest_path = output_dir / "source-manifest.json"
    receipt_path = output_dir / "asset-receipt.json"
    if not candidates_path.exists() or not manifest_path.exists() or not receipt_path.exists():
        raise ValueError("missing generated audit artifacts")
    actual_candidates = [json.loads(line) for line in candidates_path.read_text(encoding="utf-8").splitlines()]
    if actual_candidates != candidates:
        raise ValueError("candidates.jsonl is not reproducible from fixed source bytes")
    actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if actual_manifest != expected_manifest:
        raise ValueError("source-manifest.json differs from fixed-source reconstruction")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    checks = {
        "source_manifest": manifest_path,
        "candidates": candidates_path,
        "source_asset": output_dir / "aimpl-source-snapshot.tar.gz",
    }
    for key, path in checks.items():
        row = receipt[key]
        if row["sha256"] != sha256_file(path) or row["size_bytes"] != path.stat().st_size:
            raise ValueError(f"receipt mismatch for {key}")
    if receipt["candidates"]["rows"] != len(candidates) or receipt["strict_credit_granted"] != 0:
        raise ValueError("candidate count or admission boundary mismatch")
    print(f"PASS verify: roots={actual_manifest['counts']['root_pages']} "
          f"sections={actual_manifest['counts']['section_pages']} candidates={len(candidates)}")


def _safe_extract_snapshot(asset_path: Path, target: Path) -> None:
    with tarfile.open(asset_path, "r:gz") as stream:
        members = stream.getmembers()
        names = [member.name for member in members]
        if len(names) != len(set(names)):
            raise ValueError("source snapshot has duplicate members")
        for member in members:
            rel = Path(member.name)
            if (not member.isfile() or rel.is_absolute() or ".." in rel.parts
                    or member.issym() or member.islnk()):
                raise ValueError(f"unsafe source snapshot member: {member.name}")
            handle = stream.extractfile(member)
            if handle is None:
                raise ValueError(f"cannot read source snapshot member: {member.name}")
            atomic_write(target / rel, handle.read())


def command_check_repository(repo_root: Path) -> None:
    source_dir = repo_root / SOURCE_DIR_REL
    asset_path = source_dir / SOURCE_ASSET_REL.name
    manifest_path = source_dir / SOURCE_MANIFEST_REL.name
    candidates_path = source_dir / CANDIDATES_REL.name
    receipt_path = source_dir / ASSET_RECEIPT_REL.name
    for path in (asset_path, manifest_path, candidates_path, receipt_path):
        if not path.is_file():
            raise ValueError(f"missing repository AimPL source artifact: {path}")

    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw.decode("utf-8"))
    if manifest_raw != canonical_bytes(manifest):
        raise ValueError("repository AimPL source manifest is not canonical JSON")
    if manifest.get("artifact") != SOURCE_MANIFEST_REL.as_posix():
        raise ValueError("repository AimPL source manifest path is not repository-relative")
    if manifest.get("repository_paths") != {
        "source_asset": SOURCE_ASSET_REL.as_posix(),
        "source_manifest": SOURCE_MANIFEST_REL.as_posix(),
        "candidates": CANDIDATES_REL.as_posix(),
        "asset_receipt": ASSET_RECEIPT_REL.as_posix(),
    }:
        raise ValueError("repository AimPL source path inventory drifted")

    with tempfile.TemporaryDirectory(prefix="aimpl-source-replay-") as directory:
        replay_dir = Path(directory)
        _safe_extract_snapshot(asset_path, replay_dir)
        embedded_manifest = replay_dir / "source-manifest.json"
        if embedded_manifest.read_bytes() != manifest_raw:
            raise ValueError("snapshot-embedded manifest differs from repository manifest")

        for row in manifest["root_pages"]:
            path = replay_dir / row["snapshot_member_path"]
            timestamp = dt.datetime.fromisoformat(row["fixed_input_mtime_utc"]).timestamp()
            os.utime(path, (timestamp, timestamp))
        fetch_rows = []
        for row in manifest["section_pages"]:
            fetch_rows.append({
                "list_name": row["list_name"],
                "list_pos": row["list_pos"],
                "url": row["source_url"],
                "source_path": row["snapshot_member_path"],
                "retrieval_state": "fixed-snapshot-replay",
                "retrieved_at_utc": row["retrieved_at_utc"],
                "http_status": None,
                "http_date": row["http_date"],
                "size_bytes": row["source_size_bytes"],
                "sha256": row["source_sha256"],
            })
        write_jsonl(replay_dir / "fetch-log.jsonl", fetch_rows)

        replayed_candidates, replayed_manifest = extract(replay_dir)
        if canonical_bytes(replayed_manifest) != manifest_raw:
            raise ValueError("manifest is not reproducible from the fixed snapshot")
        expected_candidate_bytes = b"".join(canonical_bytes(row) for row in replayed_candidates)
        if candidates_path.read_bytes() != expected_candidate_bytes:
            raise ValueError("candidate records are not reproducible from the fixed snapshot")
        replayed_asset = replay_dir / "replayed-source.tar.gz"
        deterministic_tar_gz(replay_dir, embedded_manifest, replayed_asset)
        if replayed_asset.read_bytes() != asset_path.read_bytes():
            raise ValueError("source snapshot archive is not deterministically reproducible")

    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw.decode("utf-8"))
    if receipt_raw != canonical_bytes(receipt):
        raise ValueError("AimPL asset receipt is not canonical JSON")
    if receipt.get("artifact") != ASSET_RECEIPT_REL.as_posix():
        raise ValueError("AimPL asset receipt path is not repository-relative")
    bound = {
        "source_manifest": manifest_path,
        "candidates": candidates_path,
        "source_asset": asset_path,
    }
    for key, path in bound.items():
        row = receipt.get(key, {})
        expected_rel = {
            "source_manifest": SOURCE_MANIFEST_REL,
            "candidates": CANDIDATES_REL,
            "source_asset": SOURCE_ASSET_REL,
        }[key].as_posix()
        if row.get("path") != expected_rel:
            raise ValueError(f"non-repository-relative receipt path for {key}")
        if row.get("sha256") != sha256_file(path) or row.get("size_bytes") != path.stat().st_size:
            raise ValueError(f"AimPL asset receipt mismatch for {key}")
    if receipt.get("strict_credit_granted") != 0 or receipt["candidates"].get("rows") != 59:
        raise ValueError("AimPL source audit crossed the zero-credit boundary")
    print("PASS AimPL repository source replay: roots=80 sections=415 candidates=59 strict_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("fetch", "build", "verify", "check"))
    parser.add_argument("--audit-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    if args.command == "fetch":
        if args.audit_dir is None:
            parser.error("fetch requires --audit-dir")
        command_fetch(args.audit_dir.resolve(), args.workers)
    elif args.command in {"build", "verify"}:
        if args.audit_dir is None:
            parser.error(f"{args.command} requires --audit-dir")
        output_dir = (args.output_dir or (args.repo_root / SOURCE_DIR_REL)).resolve()
        if args.command == "build":
            command_extract(args.audit_dir.resolve(), output_dir)
        else:
            command_verify(args.audit_dir.resolve(), output_dir)
    else:
        command_check_repository(args.repo_root.resolve())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
