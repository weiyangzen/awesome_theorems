#!/usr/bin/env python3
"""Independently replay and validate the frozen AimPL v5.5 candidate audit.

The checker is deliberately read-only and does not import any AimPL producer.
All local inputs are resolved below one authoritative repository root.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html as html_module
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
from typing import Any, Iterable


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR_REL = PurePosixPath("Docs/catalog/v5/sources/aimpl")
CURATION_DIR_REL = PurePosixPath("Docs/catalog/v5/curation/aimpl_v5_5")
TOOLS_DIR_REL = PurePosixPath("Docs/catalog/v5/tools")
PARENT_DIR_REL = PurePosixPath("Docs/catalog/v5/releases/5.4")

SOURCE_ASSET_REL = SOURCE_DIR_REL / "aimpl-source-snapshot.tar.gz"
SOURCE_MANIFEST_REL = SOURCE_DIR_REL / "source-manifest.json"
CANDIDATES_REL = SOURCE_DIR_REL / "candidates.jsonl"
ASSET_RECEIPT_REL = SOURCE_DIR_REL / "asset-receipt.json"
REVIEW_A_REL = CURATION_DIR_REL / "review-a.jsonl"
REVIEW_B_REL = CURATION_DIR_REL / "review-b.jsonl"
LEDGER_REL = CURATION_DIR_REL / "review-ledger.jsonl"
SUMMARY_REL = CURATION_DIR_REL / "review-summary.json"
RETRIEVAL_REL = CURATION_DIR_REL / "cross-dedupe-retrieval.jsonl"
RETRIEVAL_SUMMARY_REL = CURATION_DIR_REL / "cross-dedupe-retrieval-summary.json"
CB_REL = CURATION_DIR_REL / "crosscheck-conjecturebench-302.jsonl"
OEIS_REL = CURATION_DIR_REL / "crosscheck-oeis-602.jsonl"
AUDIT_RECEIPT_REL = CURATION_DIR_REL / "audit-receipt.json"
PARENT_CATALOG_REL = PARENT_DIR_REL / "Claim_Catalog.json"
PARENT_MANIFEST_REL = PARENT_DIR_REL / "Release_Manifest.json"

TOOL_RELS = (
    TOOLS_DIR_REL / "extract_aimpl_conjectures_v5_5.py",
    TOOLS_DIR_REL / "build_aimpl_review_b_v5_5.py",
    TOOLS_DIR_REL / "build_aimpl_cross_dedupe_v5_5.py",
    TOOLS_DIR_REL / "finalize_aimpl_audit_v5_5.py",
    TOOLS_DIR_REL / "check_aimpl_audit_v5_5.py",
)

SOURCE_SCHEMA = "awesome-theorems/aimpl-explicit-conjecture-source-audit/1"
REVIEW_SCHEMA = "awesome-theorems/aimpl-strict-conjecture-review/1"
RETRIEVAL_SCHEMA = "awesome-theorems/aimpl-cross-dedupe-retrieval/1"
LICENSE_SPDX = "CC-BY-SA-3.0"
LICENSE_URL = "http://creativecommons.org/licenses/by-sa/3.0/"
LICENSE_SCOPE = "All information is released under the Creative Commons Attribution-ShareAlike license."
SOURCE_TRANSPORT_NOTE = (
    "The active AimPL application was served over HTTP; the HTTPS virtual host "
    "served the unrelated aimath.org WordPress site during this audit."
)
REQUIRED_REVIEWS = [
    "source_statement_is_complete_atomic_truth_apt_proposition",
    "current_snapshot_does_not_mark_solved_or_resolved",
    "high_or_medium_importance",
    "rights_and_attribution_preserved",
    "semantic_deduplication_against_parent_5_4_oeis_conjecturebench_and_batch",
]
RELATION_TYPES = {
    "component_overlap",
    "excluded_source_component_equivalent",
    "excluded_source_component_overlap",
    "generalization_not_equivalent",
    "named_family_not_equivalent",
    "overlap_at_parameter_value_not_equivalent",
    "parity_variant_not_equivalent",
    "related_extremal_model_not_equivalent",
    "related_not_equivalent",
    "same_family_not_equivalent",
    "shared_attribution_name_not_equivalent",
    "special_case_not_equivalent",
}
ALL_DATA_RE = re.compile(r"^\s*var allData = (\{.*\});\s*$", re.MULTILINE)

# These fixed hashes anchor the frozen upstream snapshot and the three external
# semantic-deduplication corpora.  Derived AimPL files are instead replayed
# semantically so a resealed mutation cannot hide behind a new outer hash.
FIXED_SOURCE_ASSET_SHA256 = "03758e0add02f4d26eb883502d6000e0befd3e190deca48aea95b1dbf74c2f57"
FIXED_SOURCE_MANIFEST_SHA256 = "1c812a8e19424790ae29c957363c66fa1cb3b2f14fe4d784676bc847e5a10908"
FIXED_PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
FIXED_PARENT_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
FIXED_CB_SHA256 = "0efbd15dec93a9499644db5324c63ee02631732a295ce583ab7229e4e2e6291a"
FIXED_OEIS_SHA256 = "eb0836ca96c2a6a722f60d202fd31de758a834a60e0ce0a230b00c3e36b42ea7"

EXPECTED_SOURCE_COUNTS = {
    "root_pages": 80,
    "problem_lists": 80,
    "section_pages": 415,
    "all_problem_objects": 1742,
    "explicit_conjecture_tag_objects": 59,
    "mechanical_candidates": 59,
}
EXPECTED_REVIEW_COUNTS = {
    "accepted_high": 13,
    "accepted_medium": 30,
    "accepted_total": 43,
    "reject": 14,
    "pending": 2,
    "reviewed_exactly_once": 59,
    "mechanical_explicit_tag_candidates": 59,
    "cross_source_component_overlaps": 2,
    "strict_credits_granted": 0,
}
FORBIDDEN_ALLOCATION_KEYS = {
    "stage_claim_id",
    "variant_id",
    "family_id",
    "allocation",
    "grants_catalog_entry",
    "grants_strict_credit",
    "grants_strict_conjecture_credit",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_true(value: Any, message: str) -> None:
    require(type(value) is bool and value is True, message)


def require_false(value: Any, message: str) -> None:
    require(type(value) is bool and value is False, message)


def require_zero(value: Any, message: str) -> None:
    require(type(value) is int and value == 0, message)


def canonical_line(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_repo_file(repo_root: Path, relative: PurePosixPath | str, label: str) -> Path:
    raw = relative.as_posix() if isinstance(relative, PurePosixPath) else relative
    require(isinstance(raw, str) and raw, f"{label}: path is not a nonempty string")
    require("\\" not in raw, f"{label}: non-POSIX repository path")
    rel = PurePosixPath(raw)
    require(not rel.is_absolute() and ".." not in rel.parts,
            f"{label}: absolute or escaping repository path")
    require(rel.as_posix() == raw and raw not in {".", ""},
            f"{label}: non-canonical repository path")
    unresolved = repo_root.joinpath(*rel.parts)
    try:
        resolved = unresolved.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label}: missing repository file {raw}") from exc
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"{label}: repository path escapes root") from exc
    require(resolved.is_file(), f"{label}: repository path is not a regular file")
    return resolved


def load_json(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{label}: JSON value is not an object")
    return value


def load_jsonl(path: Path, label: str, *, canonical: bool = True) -> list[dict[str, Any]]:
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"{label}: missing final newline")
    lines = raw.splitlines()
    require(all(line.strip() for line in lines), f"{label}: blank JSONL row")
    output: list[dict[str, Any]] = []
    for number, line in enumerate(lines, 1):
        value = json.loads(line)
        require(isinstance(value, dict), f"{label}:{number}: row is not an object")
        if canonical:
            require(line + b"\n" == canonical_line(value),
                    f"{label}:{number}: row is not canonical JSON")
        output.append(value)
    return output


def expected_binding(path: Path, repo_root: Path, *, rows: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": path.relative_to(repo_root).as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        result["rows"] = rows
    return result


def validate_binding(
    value: Any,
    expected_path: Path,
    repo_root: Path,
    label: str,
    *,
    rows: int | None = None,
) -> None:
    require(isinstance(value, dict), f"{label}: binding is not an object")
    expected = expected_binding(expected_path, repo_root, rows=rows)
    require(value == expected, f"{label}: path/hash/size/rows binding mismatch")
    safe_repo_file(repo_root, value["path"], label)


def safe_tar_name(name: str) -> bool:
    if not isinstance(name, str) or not name or "\\" in name:
        return False
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts and path.as_posix() == name


def parse_all_data(data: bytes, label: str) -> tuple[str, dict[str, dict[str, Any]]]:
    text = data.decode("utf-8")
    matches = ALL_DATA_RE.findall(text)
    require(len(matches) == 1, f"{label}: expected exactly one allData object")
    value = json.loads(matches[0])
    require(isinstance(value, dict) and all(isinstance(row, dict) for row in value.values()),
            f"{label}: invalid allData object")
    return text, value


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_text(value: str | None) -> str:
    parser = _TextExtractor()
    parser.feed(value or "")
    parser.close()
    return re.sub(r"\s+", " ", html_module.unescape(" ".join(parser.parts))).strip()


def validate_page_evidence(data: bytes, row: dict[str, Any], label: str) -> str:
    require(len(data) == row.get("source_size_bytes"), f"{label}: source size mismatch")
    require(sha256_bytes(data) == row.get("source_sha256"), f"{label}: source SHA-256 mismatch")
    text = data.decode("utf-8")
    lines = text.splitlines()
    for field, needle in (
        ("license_evidence_line_one_based", LICENSE_URL),
        ("citation_evidence_line_one_based", "Cite this as:"),
    ):
        number = row.get(field)
        require(type(number) is int and 1 <= number <= len(lines),
                f"{label}: invalid {field}")
        require(needle in lines[number - 1], f"{label}: {field} evidence mismatch")
    require("All information is released under the " in text
            and "Creative Commons Attribution-ShareAlike license" in text,
            f"{label}: license scope sentence missing")
    return text


def object_sort_key(value: dict[str, Any]) -> tuple[int, int, str]:
    list_pos = value.get("list_pos", 0)
    order = value.get("order", 0)
    require(type(list_pos) is int and type(order) is int,
            "frozen allData object has a non-integer ordering field")
    return list_pos, order, str(value.get("_id", ""))


def linked_remarks(data: dict[str, dict[str, Any]], problem_id: str) -> list[dict[str, Any]]:
    remarks = [
        row for row in data.values()
        if row.get("type") == "remark" and problem_id in (row.get("path") or [])
    ]
    remarks.sort(key=object_sort_key)
    return [{
        "remark_object_id": row.get("_id"),
        "remark_object_rev": row.get("_rev"),
        "remark_html": row.get("remark", ""),
        "remark_plain_text": plain_text(row.get("remark", "")),
        "by": row.get("by") or row.get("by_id"),
    } for row in remarks]


def reject_allocations(value: Any, label: str) -> None:
    if isinstance(value, dict):
        found = FORBIDDEN_ALLOCATION_KEYS.intersection(value)
        require(not found, f"{label}: release allocation field present: {sorted(found)}")
        for child in value.values():
            reject_allocations(child, label)
    elif isinstance(value, list):
        for child in value:
            reject_allocations(child, label)


def verify_tar_and_replay_sources(
    asset_path: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    require(sha256_file(asset_path) == FIXED_SOURCE_ASSET_SHA256,
            "frozen source asset SHA-256 changed")
    require(sha256_file(manifest_path) == FIXED_SOURCE_MANIFEST_SHA256,
            "frozen source manifest SHA-256 changed")
    require(manifest.get("schema_version") == SOURCE_SCHEMA, "source manifest schema changed")
    require(manifest.get("artifact") == SOURCE_MANIFEST_REL.as_posix(),
            "source manifest artifact path is not repository-relative canonical path")
    require(manifest.get("counts") == EXPECTED_SOURCE_COUNTS, "source manifest counts changed")
    source = manifest.get("source", {})
    require(source.get("license_spdx") == LICENSE_SPDX, "source license SPDX changed")
    require(source.get("license_url") == LICENSE_URL, "source license URL changed")
    require_true(source.get("snapshot_is_content_addressed_not_upstream_versioned"),
                 "source snapshot version boundary changed")
    require_true(source.get("upstream_last_modified_not_exposed"),
                 "source date uncertainty was erased")
    require(manifest.get("repository_paths") == {
        "source_asset": SOURCE_ASSET_REL.as_posix(),
        "source_manifest": SOURCE_MANIFEST_REL.as_posix(),
        "candidates": CANDIDATES_REL.as_posix(),
        "asset_receipt": ASSET_RECEIPT_REL.as_posix(),
    }, "source manifest repository paths changed")

    root_rows = manifest.get("root_pages")
    section_rows = manifest.get("section_pages")
    require(isinstance(root_rows, list) and len(root_rows) == 80,
            "source root-page inventory is not 80")
    require(isinstance(section_rows, list) and len(section_rows) == 415,
            "source section-page inventory is not 415")
    page_rows = [*root_rows, *section_rows]
    member_names = [row.get("snapshot_member_path") for row in page_rows]
    require(all(isinstance(name, str) and safe_tar_name(name) for name in member_names),
            "source manifest contains an unsafe snapshot member path")
    require(len(set(member_names)) == 495, "source manifest member paths are not unique")
    expected_members = set(member_names) | {"source-manifest.json"}

    archived: dict[str, bytes] = {}
    with tarfile.open(asset_path, "r:gz") as archive:
        members = archive.getmembers()
        require(len(members) == 496, "source archive member count is not 496")
        for member in members:
            require(safe_tar_name(member.name), f"unsafe source archive member {member.name!r}")
            require(member.isfile(), f"non-regular source archive member {member.name!r}")
            require(member.name not in archived, f"duplicate source archive member {member.name!r}")
            handle = archive.extractfile(member)
            require(handle is not None, f"unreadable source archive member {member.name!r}")
            archived[member.name] = handle.read()
    require(set(archived) == expected_members, "source archive member set mismatch")
    require(archived["source-manifest.json"] == manifest_path.read_bytes(),
            "embedded and repository source manifests differ")

    roots_by_name: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    expected_sections: dict[tuple[str, int], dict[str, Any]] = {}
    for row in root_rows:
        member = row["snapshot_member_path"]
        data = archived[member]
        text = validate_page_evidence(data, row, f"root page {member}")
        _, all_data = parse_all_data(data, f"root page {member}")
        listings = [value for value in all_data.values() if value.get("type") == "list"]
        require(len(listings) == 1, f"root page {member}: list-object count changed")
        listing = listings[0]
        require(row.get("list_name") == listing.get("name"), f"root page {member}: list name mismatch")
        require(row.get("list_id") == listing.get("_id"), f"root page {member}: list ID mismatch")
        require(row.get("list_rev") == listing.get("_rev"), f"root page {member}: list revision mismatch")
        require(row.get("title") == listing.get("title", ""), f"root page {member}: title mismatch")
        require(row.get("category") == listing.get("category", ""), f"root page {member}: category mismatch")
        require(row.get("author") == listing.get("author"), f"root page {member}: author mismatch")
        list_name = row["list_name"]
        require(list_name not in roots_by_name, f"duplicate root list {list_name}")
        roots_by_name[list_name] = (row, listing)

        sections = [value for value in all_data.values() if value.get("type") == "section"]
        rendered = re.findall(
            r'<li\s+data-id="([^"]+)"\s+class="section">.*?'
            r'a\s+href="(\d+)/">',
            text,
            re.DOTALL,
        )
        require(len(rendered) == len(sections), f"root page {member}: rendered route count mismatch")
        route_by_id = {section_id: int(route) for section_id, route in rendered}
        require(len(route_by_id) == len(sections), f"root page {member}: duplicate rendered route ID")
        for section in sections:
            section_id = section.get("_id")
            require(section_id in route_by_id, f"root page {member}: section route missing")
            key = (list_name, route_by_id[section_id])
            require(key not in expected_sections, f"duplicate rendered section route {key}")
            expected_sections[key] = section
    require(len(expected_sections) == 415, "root pages do not independently enumerate 415 sections")

    derived_candidates: list[dict[str, Any]] = []
    all_problem_objects = 0
    observed_section_keys: set[tuple[str, int]] = set()
    for row in section_rows:
        member = row["snapshot_member_path"]
        list_name = row.get("list_name")
        list_pos = row.get("list_pos")
        require(type(list_pos) is int and list_pos > 0 and isinstance(list_name, str),
                f"section page {member}: invalid list route")
        require(member == f"pages/{list_name}/{list_pos}.html",
                f"section page {member}: noncanonical member route")
        key = (list_name, list_pos)
        require(key in expected_sections and key not in observed_section_keys,
                f"section page {member}: route is missing or duplicated")
        observed_section_keys.add(key)
        root_row, _ = roots_by_name[list_name]
        root_section = expected_sections[key]
        require(row.get("section_id") == root_section.get("_id"),
                f"section page {member}: section ID differs from root")
        require(row.get("section_rev") == root_section.get("_rev"),
                f"section page {member}: section revision differs from root")
        source_list_pos = root_section.get("list_pos")
        try:
            source_list_pos = int(source_list_pos)
        except (TypeError, ValueError):
            source_list_pos = None
        require(row.get("source_object_list_pos") == source_list_pos,
                f"section page {member}: source list position mismatch")
        require(row.get("source_url") == f"http://aimpl.org/{list_name}/{list_pos}/",
                f"section page {member}: source URL mismatch")

        data = archived[member]
        text = validate_page_evidence(data, row, f"section page {member}")
        _, all_data = parse_all_data(data, f"section page {member}")
        all_data_lines = [number for number, line in enumerate(text.splitlines(), 1)
                          if "var allData = " in line]
        require(all_data_lines == [row.get("all_data_line_one_based")],
                f"section page {member}: allData line binding mismatch")
        matching_sections = [value for value in all_data.values()
                             if value.get("type") == "section"
                             and value.get("_id") == row.get("section_id")]
        require(len(matching_sections) == 1, f"section page {member}: bound section object missing")
        section = matching_sections[0]
        require(section.get("_rev") == row.get("section_rev"),
                f"section page {member}: bound section revision mismatch")
        require(section.get("list_id") in (None, "", list_name),
                f"section page {member}: bound list name mismatch")

        problems = [value for value in all_data.values() if value.get("type") == "problem"]
        problems.sort(key=object_sort_key)
        all_problem_objects += len(problems)
        for problem in problems:
            if str(problem.get("tag", "")).strip().lower() != "conjecture":
                continue
            require(problem.get("tag") == "conjecture",
                    f"section page {member}: conjecture tag is not literal lowercase value")
            derived_candidates.append({
                "problem": problem,
                "all_data": all_data,
                "section": section,
                "section_row": row,
                "root_row": root_row,
            })
    require(observed_section_keys == set(expected_sections), "section-page coverage differs from roots")
    require(all_problem_objects == 1742, "independent all-problem-object count changed")
    require(len(derived_candidates) == 59, "independent explicit-conjecture count changed")
    return derived_candidates, archived


def verify_candidates(
    candidates: list[dict[str, Any]],
    derived: list[dict[str, Any]],
) -> None:
    require([row.get("candidate_index") for row in candidates] == list(range(1, 60)),
            "candidate coverage/order changed")
    require(len({row.get("candidate_key") for row in candidates}) == 59,
            "candidate keys are not unique")
    expected_top_keys = {
        "schema_version", "candidate_index", "candidate_key", "source_record_key",
        "source_explicitly_labels_conjecture", "exact_source", "context",
        "source_snapshot", "rights", "admission_boundary",
    }
    for index, (candidate, frozen) in enumerate(zip(candidates, derived), 1):
        require(set(candidate) == expected_top_keys,
                f"candidate {index}: top-level field set changed")
        reject_allocations(candidate, f"candidate {index}")
        problem = frozen["problem"]
        section = frozen["section"]
        page = frozen["section_row"]
        root = frozen["root_row"]
        problem_id = problem.get("_id")
        problem_rev = problem.get("_rev")
        expected_key = sha256_bytes(
            f"{page['list_name']}\0{section.get('_id')}\0{problem_id}\0{problem_rev}".encode("utf-8")
        )[:16]
        expected_record_key = (
            f"aimpl/{page['list_name']}/{section.get('_id')}/{problem_id}@{problem_rev}"
        )
        require(candidate.get("schema_version") == SOURCE_SCHEMA,
                f"candidate {index}: schema changed")
        require(candidate.get("candidate_key") == expected_key,
                f"candidate {index}: key does not match frozen object")
        require(candidate.get("source_record_key") == expected_record_key,
                f"candidate {index}: source record key does not match frozen object")
        require_true(candidate.get("source_explicitly_labels_conjecture"),
                     f"candidate {index}: explicit source-tag flag is not true")

        exact = candidate.get("exact_source", {})
        require(exact.get("problem_object_id") == problem_id,
                f"candidate {index}: problem ID does not match frozen object")
        require(exact.get("problem_object_rev") == problem_rev,
                f"candidate {index}: problem revision does not match frozen object")
        require(exact.get("problem_tag") == problem.get("tag") == "conjecture",
                f"candidate {index}: problem tag does not match frozen object")
        body = problem.get("body") or ""
        intro = problem.get("intro") or ""
        status = problem.get("status") or ""
        expected_exact = {
            "body_html": body,
            "body_plain_text": plain_text(body),
            "body_sha256": sha256_bytes(body.encode("utf-8")),
            "intro_html": intro,
            "intro_plain_text": plain_text(intro),
            "status_html": status,
            "status_plain_text": plain_text(status),
            "problem_object_id": problem_id,
            "problem_object_rev": problem_rev,
            "problem_tag": problem.get("tag"),
            "problem_number": problem.get("number", ""),
            "problem_name": problem.get("name", ""),
            "posed_by": problem.get("by") or problem.get("by_id"),
            "json_object_binding": f"allData/{problem_id}",
        }
        require(exact == expected_exact,
                f"candidate {index}: exact source fields differ from frozen allData object")

        context = candidate.get("context", {})
        expected_context = {
            "list_name": page["list_name"],
            "list_title": root.get("title", ""),
            "list_category": root.get("category", ""),
            "list_id": root.get("list_id", ""),
            "list_rev": root.get("list_rev", ""),
            "list_author": root.get("author"),
            "section_title": section.get("title", ""),
            "section_intro_html": section.get("intro", ""),
            "section_intro_plain_text": plain_text(section.get("intro", "")),
            "section_id": section.get("_id", ""),
            "section_rev": section.get("_rev", ""),
            "section_list_pos": page["list_pos"],
            "section_source_object_list_pos": page.get("source_object_list_pos"),
            "section_number": section.get("number", ""),
            "linked_remarks": linked_remarks(frozen["all_data"], str(problem_id)),
        }
        require(context == expected_context,
                f"candidate {index}: context differs from frozen allData objects")

        snapshot = candidate.get("source_snapshot", {})
        require(set(snapshot) == {
            "collection", "source_url", "source_transport_note", "snapshot_member_path",
            "repository_source_asset_path", "repository_source_manifest_path",
            "repository_candidates_path", "source_size_bytes", "source_sha256",
            "all_data_line_one_based", "retrieved_at_utc", "http_date",
            "license_evidence_line_one_based", "citation_evidence_line_one_based",
        }, f"candidate {index}: source snapshot field set changed")
        require(snapshot.get("collection") == "AIM Problem Lists (AimPL)",
                f"candidate {index}: collection changed")
        require(snapshot.get("source_transport_note") == SOURCE_TRANSPORT_NOTE,
                f"candidate {index}: source transport note changed")
        require(snapshot.get("snapshot_member_path") == page["snapshot_member_path"],
                f"candidate {index}: snapshot member binding mismatch")
        require(snapshot.get("repository_source_asset_path") == SOURCE_ASSET_REL.as_posix(),
                f"candidate {index}: source asset path is not repository-relative")
        require(snapshot.get("repository_source_manifest_path") == SOURCE_MANIFEST_REL.as_posix(),
                f"candidate {index}: source manifest path is not repository-relative")
        require(snapshot.get("repository_candidates_path") == CANDIDATES_REL.as_posix(),
                f"candidate {index}: candidates path is not repository-relative")
        for candidate_field, page_field in (
            ("source_url", "source_url"),
            ("source_size_bytes", "source_size_bytes"),
            ("source_sha256", "source_sha256"),
            ("all_data_line_one_based", "all_data_line_one_based"),
            ("license_evidence_line_one_based", "license_evidence_line_one_based"),
            ("citation_evidence_line_one_based", "citation_evidence_line_one_based"),
            ("retrieved_at_utc", "retrieved_at_utc"),
            ("http_date", "http_date"),
        ):
            require(snapshot.get(candidate_field) == page.get(page_field),
                    f"candidate {index}: snapshot {candidate_field} mismatch")

        rights = candidate.get("rights", {})
        require(rights == {
            "license_spdx": LICENSE_SPDX,
            "license_url": LICENSE_URL,
            "license_scope_source_text": LICENSE_SCOPE,
            "attribution": (
                f"AimPL: {root.get('title', '')}, available at "
                f"http://aimpl.org/{page['list_name']}"
            ),
            "evidence_repository_source_asset_path": SOURCE_ASSET_REL.as_posix(),
            "evidence_snapshot_member_path": page["snapshot_member_path"],
            "license_evidence_line_one_based": page["license_evidence_line_one_based"],
            "citation_evidence_line_one_based": page["citation_evidence_line_one_based"],
            "share_alike_required_for_adapted_source_text": True,
        }, f"candidate {index}: rights/citation evidence mismatch")

        boundary = candidate.get("admission_boundary", {})
        require(boundary == {
            "automatically_accepted": False,
            "candidate_only": True,
            "strict_credit_granted": False,
            "required_reviews": REQUIRED_REVIEWS,
            "question_sentences_must_not_be_rewritten_as_affirmative_conjectures": True,
        }, f"candidate {index}: admission boundary changed")


def review_map(
    review_a: list[dict[str, Any]],
    review_b: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    require([row.get("candidate_index") for row in review_a] == list(range(1, 31)),
            "review-a coverage/order changed")
    require([row.get("candidate_index") for row in review_b] == list(range(31, 60)),
            "review-b coverage/order changed")
    output = {row["candidate_index"]: row for row in [*review_a, *review_b]}
    expected_fields = {
        "candidate_index", "candidate_key", "decision", "reason_code", "exact_claim_html",
        "truth_apt", "context_complete", "source_asserted_open", "tier", "basis",
        "semantic_summary", "duplicate_hints",
    }
    for index in range(1, 60):
        row = output[index]
        require(set(row) == expected_fields, f"review {index}: field set changed")
        require(row.get("candidate_key") == candidates[index - 1]["candidate_key"],
                f"review {index}: candidate key mismatch")
        require(row.get("decision") in {"accept", "reject", "pending"},
                f"review {index}: invalid decision")
        require(isinstance(row.get("reason_code"), str) and row["reason_code"],
                f"review {index}: missing reason code")
        require(isinstance(row.get("basis"), str) and row["basis"],
                f"review {index}: missing basis")
        require(isinstance(row.get("semantic_summary"), str) and row["semantic_summary"],
                f"review {index}: missing semantic summary")
        require(isinstance(row.get("duplicate_hints"), list),
                f"review {index}: duplicate hints are not a list")
        if row["decision"] == "accept":
            require(row.get("tier") in {"high", "medium"},
                    f"review {index}: accepted tier invalid")
            claim = row.get("exact_claim_html")
            require(isinstance(claim, str) and claim
                    and claim in candidates[index - 1]["exact_source"]["body_html"],
                    f"review {index}: accepted exact claim is not a literal body substring")
            for field in ("truth_apt", "context_complete", "source_asserted_open"):
                require_true(row.get(field), f"review {index}: accepted gate {field} is not true")
        else:
            require(row.get("tier") == "none" and row.get("exact_claim_html") is None,
                    f"review {index}: nonaccepted row carries claim/tier credit fields")
        reject_allocations(row, f"review {index}")
    return output


def verify_ledger(
    ledger: list[dict[str, Any]],
    reviews: dict[int, dict[str, Any]],
    candidates: list[dict[str, Any]],
    retrieval_by_index: dict[int, dict[str, Any]],
    valid_relation_ids: dict[str, set[str]],
) -> tuple[Counter[str], Counter[str], Counter[str]]:
    require([row.get("candidate_index") for row in ledger] == list(range(1, 60)),
            "review ledger coverage/order changed")
    expected_fields = {
        "schema_version", "candidate_index", "candidate_key", "source_record_key",
        "source_url", "source_sha256", "initial_review", "cross_dedupe",
        "final_decision", "final_tier", "candidate_only", "strict_credit_granted",
    }
    for index, row in enumerate(ledger, 1):
        candidate = candidates[index - 1]
        review = reviews[index]
        require(set(row) == expected_fields, f"ledger {index}: field set changed")
        require(row.get("schema_version") == REVIEW_SCHEMA, f"ledger {index}: schema changed")
        require(row.get("candidate_key") == candidate["candidate_key"],
                f"ledger {index}: candidate key mismatch")
        require(row.get("source_record_key") == candidate["source_record_key"],
                f"ledger {index}: source record key mismatch")
        require(row.get("source_url") == candidate["source_snapshot"]["source_url"],
                f"ledger {index}: source URL mismatch")
        require(row.get("source_sha256") == candidate["source_snapshot"]["source_sha256"],
                f"ledger {index}: source SHA mismatch")
        require(row.get("initial_review") == review,
                f"ledger {index}: initial review differs from reviewer artifact")
        require(row.get("final_decision") == review["decision"],
                f"ledger {index}: unexplained decision rewrite")
        require(row.get("final_tier") == review["tier"],
                f"ledger {index}: final tier differs from initial review")
        require_true(row.get("candidate_only"), f"ledger {index}: candidate-only boundary missing")
        require_false(row.get("strict_credit_granted"), f"ledger {index}: strict credit granted")
        reject_allocations(row, f"ledger {index}")

        cross = row.get("cross_dedupe", {})
        require(set(cross) == {
            "manual_verdict", "parent_5_4", "conjecturebench", "oeis", "aimpl_batch",
            "top_lexical_retrieval_reviewed", "retrieval_scores_are_not_verdicts",
        }, f"ledger {index}: cross-dedupe field set changed")
        require_true(cross.get("retrieval_scores_are_not_verdicts"),
                     f"ledger {index}: retrieval promoted to verdict")
        require(cross.get("manual_verdict") in {
            "semantic_unique_with_any_listed_relations_non_equivalent",
            "component_overlap_present_no_duplicate_credit",
        }, f"ledger {index}: invalid manual cross-dedupe verdict")
        for corpus in ("parent_5_4", "conjecturebench", "oeis", "aimpl_batch"):
            relations = cross.get(corpus)
            require(isinstance(relations, list),
                    f"ledger {index}: {corpus} relations are not a list")
            for relation in relations:
                require(isinstance(relation, dict) and set(relation) == {"id", "relation", "basis"},
                        f"ledger {index}: malformed {corpus} relation")
                require(relation.get("id") in valid_relation_ids[corpus],
                        f"ledger {index}: unknown {corpus} relation ID")
                require(relation.get("relation") in RELATION_TYPES,
                        f"ledger {index}: invalid {corpus} relation type")
                require(isinstance(relation.get("basis"), str) and relation["basis"],
                        f"ledger {index}: empty {corpus} relation basis")
                if corpus == "aimpl_batch":
                    require(relation["id"] != f"aimpl/{index}",
                            f"ledger {index}: self relation is not allowed")
        retrieval = retrieval_by_index[index]["top_matches"]
        expected_top = {
            corpus: [{"id": item["id"], "score": item["score"], "label": item.get("label")}
                     for item in retrieval[corpus][:5]]
            for corpus in ("parent_5_4", "conjecturebench", "oeis", "aimpl_batch")
        }
        require(cross.get("top_lexical_retrieval_reviewed") == expected_top,
                f"ledger {index}: reviewed lexical retrieval does not match retrieval artifact")
    decisions = Counter(row["final_decision"] for row in ledger)
    tiers = Counter(row["final_tier"] for row in ledger if row["final_decision"] == "accept")
    reasons = Counter(row["initial_review"]["reason_code"] for row in ledger)
    require((tiers["high"], tiers["medium"], decisions["reject"], decisions["pending"])
            == (13, 30, 14, 2), "review decision/tier counts changed")
    return decisions, tiers, reasons


def verify_retrieval(
    retrieval: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    reviews: dict[int, dict[str, Any]],
    parent_ids: set[str],
    cb_ids: set[str],
    oeis_ids: set[str],
) -> dict[int, dict[str, Any]]:
    require([row.get("candidate_index") for row in retrieval] == list(range(1, 60)),
            "cross-dedupe retrieval coverage/order changed")
    result: dict[int, dict[str, Any]] = {}
    valid_ids = {
        "parent_5_4": parent_ids,
        "conjecturebench": cb_ids,
        "oeis": oeis_ids,
        "aimpl_batch": {f"aimpl/{index}" for index in range(1, 60)},
    }
    for index, row in enumerate(retrieval, 1):
        candidate = candidates[index - 1]
        require(row.get("candidate_key") == candidate["candidate_key"],
                f"retrieval {index}: candidate key mismatch")
        require_true(row.get("retrieval_only_not_a_verdict"),
                     f"retrieval {index}: retrieval promoted to verdict")
        expected_query = "\n".join(filter(None, [
            candidate["exact_source"].get("problem_name"),
            candidate["exact_source"].get("body_plain_text"),
            candidate["exact_source"].get("intro_plain_text"),
            candidate["context"].get("section_title"),
            candidate["context"].get("list_title"),
            reviews[index].get("semantic_summary"),
        ]))
        require(row.get("query_text") == expected_query,
                f"retrieval {index}: query text is not reproducibly bound")
        matches = row.get("top_matches")
        require(isinstance(matches, dict)
                and set(matches) == {"parent_5_4", "conjecturebench", "oeis", "aimpl_batch"},
                f"retrieval {index}: cross-dedupe corpus set is not closed")
        for corpus, allowed_ids in valid_ids.items():
            items = matches[corpus]
            require(isinstance(items, list) and len(items) == 8,
                    f"retrieval {index}: {corpus} top-match count changed")
            ids = [item.get("id") for item in items]
            require(len(ids) == len(set(ids)) and all(item_id in allowed_ids for item_id in ids),
                    f"retrieval {index}: {corpus} contains unknown/duplicate IDs")
            if corpus == "aimpl_batch":
                require(f"aimpl/{index}" not in ids,
                        f"retrieval {index}: AimPL self-match was not excluded")
            scores = [item.get("score") for item in items]
            require(all(type(score) in {int, float} and score >= 0 for score in scores),
                    f"retrieval {index}: {corpus} has an invalid score")
            require(scores == sorted(scores, reverse=True),
                    f"retrieval {index}: {corpus} scores are not descending")
        result[index] = row
    return result


def verify_summary(
    summary: dict[str, Any],
    manifest: dict[str, Any],
    paths: dict[str, Path],
    repo_root: Path,
    reasons: Counter[str],
) -> None:
    require(summary.get("schema_version") == REVIEW_SCHEMA, "review summary schema changed")
    require(summary.get("artifact") == SUMMARY_REL.as_posix(),
            "review summary artifact path is not repository-relative")
    require(summary.get("audit_cutoff_utc") == manifest.get("created_at_utc"),
            "review summary cutoff differs from source manifest")
    require(summary.get("counts") == EXPECTED_REVIEW_COUNTS, "review summary counts changed")
    require(summary.get("reason_counts") == dict(sorted(reasons.items())),
            "review summary reason counts differ from ledger")
    require(summary.get("source_scope") == manifest.get("counts"),
            "review summary source scope differs from manifest")
    require(summary.get("source_date") == {
        "snapshot_cutoff_utc": manifest.get("created_at_utc"),
        "upstream_last_modified_exposed": False,
        "policy": manifest["source"]["source_date_policy"],
    }, "review summary source-date boundary changed")
    require(summary.get("rights_and_citation") == {
        "license_spdx": LICENSE_SPDX,
        "license_url": LICENSE_URL,
        "verified_root_pages": 80,
        "verified_section_pages": 415,
        "citation_pattern": manifest["source"]["citation_pattern"],
        "share_alike_required_for_adapted_source_text": True,
    }, "review summary rights/citation boundary changed")
    require(summary.get("cross_dedupe_scope") == {
        "parent_5_4_records": 4100,
        "oeis_candidates": 602,
        "conjecturebench_records": 302,
        "aimpl_batch_candidates": 59,
        "policy": "lexical retrieval plus per-record manual semantic comparison; related non-equivalent variants do not collapse",
    }, "review summary cross-dedupe scope changed")
    boundary = summary.get("admission_boundary", {})
    require_true(boundary.get("candidate_only"), "review summary candidate-only boundary missing")
    require_false(boundary.get("formal_release_modified"), "review summary claims release modification")
    require_true(boundary.get("accepted_rows_are_not_formal_additions"),
                 "review summary formal-addition boundary changed")
    require_zero(boundary.get("strict_credit_granted"), "review summary grants strict credit")
    require_zero(summary["counts"].get("strict_credits_granted"),
                 "review summary strict-credit count is not integer zero")

    inputs = summary.get("inputs", {})
    expected = {
        "candidates": ("candidates", 59),
        "source_manifest": ("source_manifest", None),
        "source_asset_receipt": ("asset_receipt", None),
        "review_a": ("review_a", 30),
        "review_b": ("review_b", 29),
        "cross_dedupe_retrieval": ("retrieval", 59),
        "cross_dedupe_retrieval_summary": ("retrieval_summary", None),
    }
    require(set(inputs) == set(expected), "review summary input binding set changed")
    for name, (path_name, row_count) in expected.items():
        validate_binding(inputs[name], paths[path_name], repo_root,
                         f"review summary input {name}", rows=row_count)
    require(summary.get("review_ledger_sha256") == sha256_file(paths["ledger"]),
            "review summary ledger SHA mismatch")


def verify_audit_receipt(
    receipt: dict[str, Any],
    manifest: dict[str, Any],
    paths: dict[str, Path],
    repo_root: Path,
) -> None:
    require(receipt.get("schema_version") == REVIEW_SCHEMA, "audit receipt schema changed")
    require(receipt.get("artifact") == AUDIT_RECEIPT_REL.as_posix(),
            "audit receipt artifact path is not repository-relative")
    require(receipt.get("audit_cutoff_utc") == manifest.get("created_at_utc"),
            "audit receipt cutoff differs from source manifest")
    require_false(receipt.get("formal_release_modified"), "audit receipt claims release modification")
    require_zero(receipt.get("strict_credits_granted"), "audit receipt grants strict credit")

    expected_artifacts = {
        "source_asset": ("source_asset", None),
        "source_manifest": ("source_manifest", None),
        "source_asset_receipt": ("asset_receipt", None),
        "candidates": ("candidates", 59),
        "review_a": ("review_a", 30),
        "review_b": ("review_b", 29),
        "crosscheck_conjecturebench": ("cb", 302),
        "crosscheck_oeis": ("oeis", 602),
        "cross_dedupe_retrieval": ("retrieval", 59),
        "cross_dedupe_retrieval_summary": ("retrieval_summary", None),
        "review_ledger": ("ledger", 59),
        "review_summary": ("summary", None),
    }
    artifacts = receipt.get("artifacts", {})
    require(set(artifacts) == set(expected_artifacts), "audit receipt artifact binding set changed")
    for name, (path_name, row_count) in expected_artifacts.items():
        validate_binding(artifacts[name], paths[path_name], repo_root,
                         f"audit receipt artifact {name}", rows=row_count)

    parent_inputs = receipt.get("parent_release_inputs", {})
    require(set(parent_inputs) == {"claim_catalog", "release_manifest"},
            "audit receipt parent input set changed")
    validate_binding(parent_inputs["claim_catalog"], paths["parent_catalog"], repo_root,
                     "audit receipt parent catalog", rows=4100)
    validate_binding(parent_inputs["release_manifest"], paths["parent_manifest"], repo_root,
                     "audit receipt parent manifest")

    scripts = receipt.get("scripts", {})
    require(set(scripts) == {relative.as_posix() for relative in TOOL_RELS},
            "audit receipt script set changed")
    for relative in TOOL_RELS:
        script = safe_repo_file(repo_root, relative, f"audit script {relative.name}")
        require(scripts[relative.as_posix()] == sha256_file(script),
                f"audit script receipt mismatch: {relative.name}")


def verify_no_ephemeral_paths(paths: Iterable[Path]) -> None:
    banned = ("/" + "tmp/", "/" + "home/")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        require(not any(prefix in text for prefix in banned),
                f"{path.name}: ephemeral absolute path leaked into audit artifact")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT,
                        help="authoritative repository root (defaults to the checker's repository)")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve(strict=True)
    require(repo_root.is_dir(), "repository root is not a directory")

    relatives = {
        "source_asset": SOURCE_ASSET_REL,
        "source_manifest": SOURCE_MANIFEST_REL,
        "candidates": CANDIDATES_REL,
        "asset_receipt": ASSET_RECEIPT_REL,
        "review_a": REVIEW_A_REL,
        "review_b": REVIEW_B_REL,
        "ledger": LEDGER_REL,
        "summary": SUMMARY_REL,
        "retrieval": RETRIEVAL_REL,
        "retrieval_summary": RETRIEVAL_SUMMARY_REL,
        "cb": CB_REL,
        "oeis": OEIS_REL,
        "audit_receipt": AUDIT_RECEIPT_REL,
        "parent_catalog": PARENT_CATALOG_REL,
        "parent_manifest": PARENT_MANIFEST_REL,
    }
    paths = {name: safe_repo_file(repo_root, relative, name)
             for name, relative in relatives.items()}

    manifest = load_json(paths["source_manifest"], "source manifest")
    derived, _ = verify_tar_and_replay_sources(
        paths["source_asset"], paths["source_manifest"], manifest,
    )
    candidates = load_jsonl(paths["candidates"], "AimPL candidates")
    verify_candidates(candidates, derived)

    review_a = load_jsonl(paths["review_a"], "AimPL review-a", canonical=False)
    review_b = load_jsonl(paths["review_b"], "AimPL review-b", canonical=False)
    reviews = review_map(review_a, review_b, candidates)

    parent_catalog = load_json(paths["parent_catalog"], "parent 5.4 catalog")
    require(sha256_file(paths["parent_catalog"]) == FIXED_PARENT_CATALOG_SHA256,
            "parent 5.4 Claim Catalog SHA-256 changed")
    require(sha256_file(paths["parent_manifest"]) == FIXED_PARENT_MANIFEST_SHA256,
            "parent 5.4 Release Manifest SHA-256 changed")
    parent_records = parent_catalog.get("records")
    require(isinstance(parent_records, list) and len(parent_records) == 4100,
            "parent 5.4 catalog count changed")
    parent_ids = {row.get("variant_id") for row in parent_records}
    require(len(parent_ids) == 4100 and all(isinstance(value, str) for value in parent_ids),
            "parent 5.4 variant IDs are not unique strings")

    cb_rows = load_jsonl(paths["cb"], "ConjectureBench crosscheck")
    oeis_rows = load_jsonl(paths["oeis"], "OEIS crosscheck")
    require(sha256_file(paths["cb"]) == FIXED_CB_SHA256,
            "ConjectureBench crosscheck SHA-256 changed")
    require(sha256_file(paths["oeis"]) == FIXED_OEIS_SHA256,
            "OEIS crosscheck SHA-256 changed")
    cb_ids = {row.get("cb_id") for row in cb_rows}
    oeis_ids = {row.get("candidate_key") for row in oeis_rows}
    require(len(cb_rows) == len(cb_ids) == 302 and all(isinstance(value, str) for value in cb_ids),
            "ConjectureBench crosscheck identity/count changed")
    require(len(oeis_rows) == len(oeis_ids) == 602 and all(isinstance(value, str) for value in oeis_ids),
            "OEIS crosscheck identity/count changed")

    retrieval = load_jsonl(paths["retrieval"], "cross-dedupe retrieval")
    retrieval_by_index = verify_retrieval(
        retrieval, candidates, reviews, parent_ids, cb_ids, oeis_ids,
    )
    ledger = load_jsonl(paths["ledger"], "AimPL review ledger")
    _, _, reasons = verify_ledger(
        ledger,
        reviews,
        candidates,
        retrieval_by_index,
        {
            "parent_5_4": parent_ids,
            "conjecturebench": cb_ids,
            "oeis": oeis_ids,
            "aimpl_batch": {f"aimpl/{index}" for index in range(1, 60)},
        },
    )

    retrieval_summary = load_json(paths["retrieval_summary"], "retrieval summary")
    require(retrieval_summary.get("schema_version") == RETRIEVAL_SCHEMA,
            "retrieval summary schema changed")
    require(retrieval_summary.get("artifact") == RETRIEVAL_SUMMARY_REL.as_posix(),
            "retrieval summary artifact path is not repository-relative")
    require(retrieval_summary.get("counts") == {
        "aimpl_queries": 59,
        "parent_5_4": 4100,
        "conjecturebench": 302,
        "oeis": 602,
        "aimpl_batch": 59,
    }, "retrieval summary corpus counts changed")
    retrieval_inputs = retrieval_summary.get("inputs", {})
    require(set(retrieval_inputs) == {
        "aimpl_candidates", "parent_5_4", "conjecturebench", "oeis_candidates",
    }, "retrieval summary input set changed")
    validate_binding(retrieval_inputs["aimpl_candidates"], paths["candidates"], repo_root,
                     "retrieval AimPL input", rows=59)
    validate_binding(retrieval_inputs["parent_5_4"], paths["parent_catalog"], repo_root,
                     "retrieval parent input", rows=4100)
    validate_binding(retrieval_inputs["conjecturebench"], paths["cb"], repo_root,
                     "retrieval ConjectureBench input", rows=302)
    validate_binding(retrieval_inputs["oeis_candidates"], paths["oeis"], repo_root,
                     "retrieval OEIS input", rows=602)
    validate_binding(retrieval_summary.get("output"), paths["retrieval"], repo_root,
                     "retrieval output", rows=59)
    require(retrieval_summary.get("output_sha256") == sha256_file(paths["retrieval"]),
            "retrieval output SHA receipt mismatch")
    require(retrieval_summary.get("review_boundary")
            == "Scores retrieve candidates only; semantic equivalence requires manual review.",
            "retrieval/verdict boundary changed")

    asset_receipt = load_json(paths["asset_receipt"], "source asset receipt")
    require(asset_receipt.get("schema_version") == SOURCE_SCHEMA, "asset receipt schema changed")
    require(asset_receipt.get("artifact") == ASSET_RECEIPT_REL.as_posix(),
            "asset receipt path is not repository-relative")
    require(asset_receipt.get("created_at_utc") == manifest.get("created_at_utc"),
            "asset receipt cutoff differs from source manifest")
    validate_binding(asset_receipt.get("source_asset"), paths["source_asset"], repo_root,
                     "source asset receipt")
    validate_binding(asset_receipt.get("source_manifest"), paths["source_manifest"], repo_root,
                     "source manifest receipt")
    validate_binding(asset_receipt.get("candidates"), paths["candidates"], repo_root,
                     "candidate receipt", rows=59)
    require_zero(asset_receipt.get("strict_credit_granted"),
                 "source asset receipt grants strict credit")

    summary = load_json(paths["summary"], "review summary")
    verify_summary(summary, manifest, paths, repo_root, reasons)
    audit_receipt = load_json(paths["audit_receipt"], "audit receipt")
    verify_audit_receipt(audit_receipt, manifest, paths, repo_root)

    verify_no_ephemeral_paths([
        paths["source_manifest"], paths["candidates"], paths["asset_receipt"],
        paths["review_a"], paths["review_b"], paths["ledger"], paths["summary"],
        paths["retrieval_summary"], paths["audit_receipt"],
    ])
    print(
        "PASS independent AimPL audit check: "
        "pages=495 candidates=59 high=13 medium=30 reject=14 pending=2 strict_credit=0"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL independent AimPL audit check: {exc}", file=sys.stderr)
        raise SystemExit(1)
