#!/usr/bin/env python3
"""Extract pinned scholarly-reference candidates for 1,200 theorem identities.

References are review leads only.  DOI/ISBN/arXiv syntax or proximity to a
Wikipedia theorem passage never grants theorem, proof, importance, or status
credit without a reviewer confirming that the cited work supports the exact
theorem identity and statement.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[4]
THOUSAND = ROOT / "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json"
WIKIPEDIA = ROOT / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
OUTPUT = ROOT / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
THOUSAND_SHA = "fe61d56e4ba4cc3a9846e2b153edee32dae6b1266b668e1a63dd3639d867bdad"
WIKIPEDIA_SHA = "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33"
DOI_PATTERNS = (
    re.compile(r"\bdoi\s*=\s*([^|}\s]+)", re.I),
    re.compile(r"doi\.org/(10\.[0-9]{4,9}/[^\s|}<>[]\"']+)", re.I),
    re.compile(r"(?<![A-Za-z0-9])10\.[0-9]{4,9}/[^\s|}<>[]\"']+", re.I),
)
ISBN_RE = re.compile(r"\bisbn(?:13)?\s*=\s*([0-9Xx][0-9Xx -]{8,22})", re.I)
ARXIV_RE = re.compile(
    r"\barxiv\s*=\s*((?:[0-9]{4}\.[0-9]{4,5}|(?:math|alg-geom|astro-ph|cond-mat|gr-qc|hep-ex|hep-lat|hep-ph|hep-th|math-ph|nlin|nucl-ex|nucl-th|physics|quant-ph)/[0-9]{7})(?:v[0-9]+)?)",
    re.I,
)
MAX_PER_IDENTITY = 8


class ReferenceError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def normalize_doi(raw: str) -> str | None:
    value = unquote(raw).strip().lower()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi\s*:\s*)", "", value)
    value = value.rstrip(".,;:)]}'\"")
    if re.fullmatch(r"10\.[0-9]{4,9}/\S+", value):
        return value
    return None


def normalize_isbn(raw: str) -> str | None:
    value = re.sub(r"[^0-9Xx]", "", raw).upper()
    return value if len(value) in {10, 13} else None


def context_bounds(text: str, start: int, end: int) -> tuple[int, int]:
    before = text.rfind("<ref", 0, start)
    close_before = text.rfind("</ref>", 0, start)
    after = text.find("</ref>", end)
    if before >= 0 and before > close_before and after >= 0 and after - before <= 4_000:
        return before, after + len("</ref>")
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    if line_end - line_start <= 2_000:
        return line_start, line_end
    return max(0, start - 600), min(len(text), end + 600)


def candidates(page: Mapping[str, Any]) -> list[dict[str, Any]]:
    text = str(page["wikitext"])
    found: list[tuple[int, int, str, str, str]] = []
    for pattern in DOI_PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group(1) if match.lastindex else match.group(0)
            normalized = normalize_doi(raw)
            if normalized:
                found.append((match.start(), match.end(), "doi", raw, normalized))
    for match in ISBN_RE.finditer(text):
        normalized = normalize_isbn(match.group(1))
        if normalized:
            found.append((match.start(), match.end(), "isbn", match.group(1), normalized))
    for match in ARXIV_RE.finditer(text):
        found.append((match.start(), match.end(), "arxiv", match.group(1), match.group(1).lower()))
    priority = {"doi": 0, "arxiv": 1, "isbn": 2}
    found.sort(key=lambda value: (value[0], priority[value[2]], value[4]))
    seen: set[tuple[str, str]] = set()
    output: list[dict[str, Any]] = []
    for start, end, kind, raw, normalized in found:
        key = (kind, normalized)
        if key in seen:
            continue
        seen.add(key)
        context_start, context_end = context_bounds(text, start, end)
        passage = text[context_start:context_end]
        item: dict[str, Any] = {
            "kind": kind,
            "normalized_identifier": normalized,
            "raw_identifier": raw,
            "identifier_char_start": start,
            "identifier_char_end_exclusive": end,
            "context_char_start": context_start,
            "context_char_end_exclusive": context_end,
            "context_text": passage,
            "context_sha256": sha(passage.encode("utf-8")),
            "page_id": page["page_id"],
            "resolved_title": page["resolved_title"],
            "revision_id": page["revision_id"],
            "revision_timestamp": page["revision_timestamp"],
            "mediawiki_revision_sha1": page["mediawiki_revision_sha1"],
            "wikitext_sha256": sha(text.encode("utf-8")),
            "source_locator": page["attribution_url"],
            "review_state": "candidate_reference_not_yet_matched_to_theorem_statement",
            "automatic_credit": False,
        }
        item["row_sha256"] = hash_without(item, "row_sha256")
        output.append(item)
        if len(output) == MAX_PER_IDENTITY:
            break
    return output


def build() -> dict[str, Any]:
    if file_sha(THOUSAND) != THOUSAND_SHA or file_sha(WIKIPEDIA) != WIKIPEDIA_SHA:
        raise ReferenceError("pinned input digest drifted")
    thousand = json.loads(THOUSAND.read_text(encoding="utf-8"))
    with gzip.open(WIKIPEDIA, "rt", encoding="utf-8") as stream:
        wikipedia = json.load(stream)
    source_rows = thousand.get("records", [])
    identity_rows = wikipedia.get("identity_resolution", [])
    pages = {int(page["page_id"]): page for page in wikipedia.get("pages", [])}
    if len(source_rows) != 1_200 or len(identity_rows) != 1_200 or len(pages) != 1_181:
        raise ReferenceError("input cardinality drifted")
    source_by_id = {str(row["source_record_id"]): row for row in source_rows}
    if len(source_by_id) != 1_200:
        raise ReferenceError("source identity collision")

    records: list[dict[str, Any]] = []
    for identity in identity_rows:
        source_id = str(identity["source_record_id"])
        source = source_by_id.get(source_id)
        if source is None:
            raise ReferenceError(f"Wikipedia identity not in 1000+ source: {source_id}")
        references: list[dict[str, Any]] = []
        for page_id in identity.get("resolved_page_ids", []):
            page = pages.get(int(page_id))
            if page is not None:
                references.extend(candidates(page))
        references.sort(key=lambda row: ({"doi": 0, "arxiv": 1, "isbn": 2}[row["kind"]], row["identifier_char_start"], row["normalized_identifier"]))
        deduped: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for item in references:
            key = (item["kind"], item["normalized_identifier"])
            if key not in seen:
                seen.add(key)
                deduped.append(item)
            if len(deduped) == MAX_PER_IDENTITY:
                break
        record: dict[str, Any] = {
            "source_record_id": source_id,
            "external_id": source["external_id"],
            "title": source["title"],
            "msc2020": source["msc2020"],
            "source_row_sha256": source["row_sha256"],
            "resolved_page_ids": identity.get("resolved_page_ids", []),
            "reference_candidates": deduped,
            "review_boundary": {
                "candidate_count": len(deduped),
                "reference_supports_exact_theorem_not_yet_verified": True,
                "importance_or_proof_credit_granted": False,
            },
        }
        record["row_sha256"] = hash_without(record, "row_sha256")
        records.append(record)
    records.sort(key=lambda row: row["source_record_id"].encode("utf-8"))
    by_kind = Counter(
        item["kind"]
        for row in records
        for item in row["reference_candidates"]
    )
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/thousand-plus-reference-candidates/5.5",
        "review_as_of": "2026-08-10",
        "scope": "pinned bibliography candidates for independent human theorem-evidence review",
        "inputs": {
            "thousand_plus_path": THOUSAND.relative_to(ROOT).as_posix(),
            "thousand_plus_sha256": THOUSAND_SHA,
            "wikipedia_path": WIKIPEDIA.relative_to(ROOT).as_posix(),
            "wikipedia_sha256": WIKIPEDIA_SHA,
        },
        "policy": {
            "maximum_reference_candidates_per_identity": MAX_PER_IDENTITY,
            "page_or_identifier_presence_grants_credit": False,
            "human_must_match_reference_to_exact_theorem_statement": True,
            "human_must_verify_bibliographic_identity_and_rights": True,
        },
        "counts": {
            "identities": len(records),
            "identities_with_reference_candidate": sum(bool(row["reference_candidates"]) for row in records),
            "identities_without_reference_candidate": sum(not row["reference_candidates"] for row in records),
            "reference_candidates": sum(len(row["reference_candidates"]) for row in records),
            "by_kind": dict(sorted(by_kind.items())),
            "credits_granted": 0,
        },
        "set_digests": {
            "source_record_id_set_sha256": set_digest(row["source_record_id"] for row in records),
            "row_sha256_set_sha256": set_digest(row["row_sha256"] for row in records),
        },
        "records": records,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = build()
    payload = canonical(document) + b"\n"
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != payload:
            raise ReferenceError(f"missing or stale output: {args.output}")
        print(f"PASS theorem reference candidates identities={len(document['records'])} refs={document['counts']['reference_candidates']} authority={document['authority_sha256']}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(f"wrote {args.output} identities={len(document['records'])} refs={document['counts']['reference_candidates']} authority={document['authority_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
