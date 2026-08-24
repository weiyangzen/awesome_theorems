#!/usr/bin/env python3
"""Independently verify the pinned OpenAlex DOI metadata asset for v5.5.

This checker intentionally does not import the network fetcher.  OpenAlex rows
are bibliographic discovery evidence only: even a perfectly verified row never
grants theorem-statement support, importance, or release credit.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping


INPUT_REL = Path("Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json")
METADATA_REL = Path("Docs/catalog/v5/sources/openalex-thousand-plus-doi-metadata-20260810.json.gz")
INPUT_SHA256 = "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435"
METADATA_SHA256 = "e3d490619eac4e16bdf24478c74de2024d32d3ec0d603f3ac4a102ad4c206486"
AUTHORITY_SHA256 = "4a6abb7d9f22dbca688eed164116b429beacb15a643465bf424f41d0e0e3f565"
EXPECTED_DOIS = 2_655
OPENALEX_ID = re.compile(r"https://openalex[.]org/W[0-9]+\Z")

BASE_BOUNDARY = {
    "bibliographic_metadata_only": True,
    "quality_credit_granted": False,
    "supports_exact_theorem_statement_verified": False,
}
AMBIGUOUS_BOUNDARY = {**BASE_BOUNDARY, "human_disambiguation_required": True}


class AuditError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha256_bytes(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical(sorted(values)))


def reject_constant(token: str) -> None:
    raise AuditError(f"non-finite JSON token: {token}")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_strict_json(payload: bytes, label: str) -> Any:
    try:
        return json.loads(
            payload,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"invalid {label}: {error}") from error


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def require_exact_int(value: Any, expected: int, label: str) -> None:
    require(type(value) is int and value == expected, f"{label} must be integer {expected}")


def collect_input_dois(document: Mapping[str, Any]) -> list[str]:
    records = document.get("records")
    require(isinstance(records, list), "reference-candidate records missing")
    dois: set[str] = set()
    for record in records:
        require(isinstance(record, dict), "reference candidate must be an object")
        references = record.get("reference_candidates", [])
        require(isinstance(references, list), "reference_candidates must be a list")
        for reference in references:
            require(isinstance(reference, dict), "reference candidate item must be an object")
            if reference.get("kind") != "doi":
                continue
            doi = reference.get("normalized_identifier")
            require(isinstance(doi, str) and doi == doi.lower() and doi.strip() == doi, "invalid normalized DOI")
            dois.add(doi)
    require(len(dois) == EXPECTED_DOIS, f"DOI denominator drifted: {len(dois)}")
    return sorted(dois)


def check_compact_match(match: Any, doi: str, label: str) -> None:
    require(isinstance(match, dict), f"{label} must be an object")
    require(match.get("normalized_doi") == doi, f"{label} DOI mismatch")
    require(isinstance(match.get("openalex_id"), str) and OPENALEX_ID.fullmatch(match["openalex_id"]), f"{label} invalid OpenAlex id")
    require(match.get("evidence_boundary") == BASE_BOUNDARY, f"{label} evidence boundary drifted")
    require(match.get("row_sha256") == hash_without(match, "row_sha256"), f"{label} row digest mismatch")
    require(match.get("title") is None or isinstance(match.get("title"), str), f"{label} title type invalid")
    require(match.get("authors") is None or isinstance(match.get("authors"), list), f"{label} authors type invalid")


def verify(repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve(strict=True)
    input_path = (root / INPUT_REL).resolve(strict=True)
    metadata_path = (root / METADATA_REL).resolve(strict=True)
    require(input_path.is_relative_to(root) and metadata_path.is_relative_to(root), "asset path escapes repo root")
    require(sha256_file(input_path) == INPUT_SHA256, "reference-candidate input digest drifted")
    require(sha256_file(metadata_path) == METADATA_SHA256, "OpenAlex gzip digest drifted")

    input_document = load_strict_json(input_path.read_bytes(), "reference-candidate JSON")
    require(isinstance(input_document, dict), "reference-candidate root must be an object")
    dois = collect_input_dois(input_document)

    raw_gzip = metadata_path.read_bytes()
    require(raw_gzip[:2] == b"\x1f\x8b", "metadata is not gzip")
    require(raw_gzip[4:8] == b"\x00\x00\x00\x00", "gzip mtime must be zero")
    try:
        payload = gzip.decompress(raw_gzip)
    except (gzip.BadGzipFile, EOFError) as error:
        raise AuditError(f"invalid metadata gzip: {error}") from error
    document = load_strict_json(payload, "OpenAlex metadata JSON")
    require(isinstance(document, dict), "metadata root must be an object")
    require(payload == canonical(document) + b"\n", "metadata JSON is not canonical")
    require(document.get("authority_sha256") == AUTHORITY_SHA256, "authority constant drifted")
    require(document.get("authority_sha256") == hash_without(document, "authority_sha256"), "authority replay mismatch")
    require(document.get("schema_version") == "awesome-theorems/openalex-theorem-reference-metadata/5.5", "schema drifted")
    require(document.get("observed_on") == "2026-08-10", "observation date drifted")
    require(
        document.get("source")
        == {
            "api": "https://api.openalex.org/works",
            "dataset_license": "CC0-1.0",
            "terms_url": "https://docs.openalex.org/download-all-data/openalex-snapshot",
        },
        "source declaration drifted",
    )
    require(
        document.get("policy")
        == {
            "human_exact_reference_and_scope_review_required": True,
            "openalex_metadata_grants_theorem_support_credit": False,
        },
        "credit policy drifted",
    )
    require(
        document.get("input")
        == {"doi_candidates": EXPECTED_DOIS, "path": INPUT_REL.as_posix(), "sha256": INPUT_SHA256},
        "input binding drifted",
    )

    records = document.get("records")
    require(isinstance(records, list) and len(records) == EXPECTED_DOIS, "metadata record denominator drifted")
    record_dois = [record.get("normalized_doi") if isinstance(record, dict) else None for record in records]
    require(record_dois == dois, "metadata DOI order/set mismatch")

    resolved = ambiguous = missing = 0
    row_hashes: list[str] = []
    for index, (doi, record) in enumerate(zip(dois, records, strict=True)):
        label = f"record[{index}] {doi}"
        require(isinstance(record, dict), f"{label} must be an object")
        require(record.get("row_sha256") == hash_without(record, "row_sha256"), f"{label} row digest mismatch")
        row_hashes.append(record["row_sha256"])
        is_ambiguous = record.get("ambiguous") is True
        is_missing = record.get("missing") is True
        openalex_id = record.get("openalex_id")
        is_resolved = isinstance(openalex_id, str)
        require(sum((is_resolved, is_ambiguous, is_missing)) == 1, f"{label} resolution state is not exclusive")
        if is_resolved:
            resolved += 1
            check_compact_match(record, doi, label)
            require("matches" not in record and "match_count" not in record, f"{label} resolved row carries ambiguity fields")
        elif is_ambiguous:
            ambiguous += 1
            require(openalex_id is None, f"{label} ambiguous row selected a work")
            require(record.get("evidence_boundary") == AMBIGUOUS_BOUNDARY, f"{label} ambiguity boundary drifted")
            matches = record.get("matches")
            require(isinstance(matches, list) and len(matches) > 1, f"{label} ambiguous matches missing")
            require_exact_int(record.get("match_count"), len(matches), f"{label}.match_count")
            ids: list[str] = []
            for match_index, match in enumerate(matches):
                check_compact_match(match, doi, f"{label}.matches[{match_index}]")
                ids.append(match["openalex_id"])
            require(ids == sorted(set(ids)), f"{label} ambiguous matches are duplicate or unordered")
        else:
            missing += 1
            require(openalex_id is None, f"{label} missing row selected a work")
            require(record.get("evidence_boundary") == BASE_BOUNDARY, f"{label} missing boundary drifted")
            require("matches" not in record and "match_count" not in record, f"{label} missing row carries matches")

    counts = document.get("counts")
    require(isinstance(counts, dict), "counts missing")
    require_exact_int(counts.get("requested_dois"), EXPECTED_DOIS, "counts.requested_dois")
    require_exact_int(counts.get("resolved_dois"), resolved, "counts.resolved_dois")
    require_exact_int(counts.get("ambiguous_dois"), ambiguous, "counts.ambiguous_dois")
    require_exact_int(counts.get("missing_dois"), missing, "counts.missing_dois")
    require_exact_int(counts.get("quality_credits"), 0, "counts.quality_credits")
    require(
        document.get("set_digests")
        == {
            "doi_set_sha256": set_digest(dois),
            "row_sha256_set_sha256": set_digest(row_hashes),
        },
        "set digests drifted",
    )
    return {"resolved": resolved, "ambiguous": ambiguous, "missing": missing, "authority": AUTHORITY_SHA256}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    try:
        result = verify(args.repo_root)
    except (AuditError, OSError) as error:
        print(f"FAIL OpenAlex metadata audit: {error}")
        return 1
    print(
        "PASS OpenAlex metadata audit "
        f"resolved={result['resolved']} ambiguous={result['ambiguous']} missing={result['missing']} "
        "quality_credit=0 "
        f"authority={result['authority']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
