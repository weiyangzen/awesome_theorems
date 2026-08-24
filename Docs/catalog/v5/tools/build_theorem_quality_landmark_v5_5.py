#!/usr/bin/env python3
"""Build the repository-owned 1000+ landmark theorem quality ledger."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5")
CURATION = ROOT / CURATION_REL
OUTPUT_REL = CURATION_REL / "landmark-ledger-0-1199.json"
OUTPUT = ROOT / OUTPUT_REL
SOURCE_REL = Path("Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json")
REFERENCE_REL = Path("Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json")
NATURAL_JOIN_REL = Path("Docs/catalog/v5/sources/naturalproofs-proofwiki-1000-plus-title-join-v2.0.0.json.gz")
SOURCE_SHA256 = "fe61d56e4ba4cc3a9846e2b153edee32dae6b1266b668e1a63dd3639d867bdad"
REFERENCE_SHA256 = "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435"
NATURAL_JOIN_SHA256 = "3cb44f9f7ed62b402a892e0b485c38d3881b9a4e40c5f34135a57fbf1d8936b5"
PRE_MIGRATION_LEDGER_SHA256 = "a8cffb16f0040c4acb82a6f49ca8d6cab67068f512aefd0dd9e40ee0d3d668bc"

SLICES = (
    (0, 199, "review-000-199.jsonl", "9bbaf8db012b5f7283bac1f2362717a27e50ef8178e379992e24a2693dd59052", "3eb4af305d3c74be3affdf7569b8c6df80ef5f9ff8db4ccafcfe3f604e54303c"),
    (200, 399, "review-200-399.jsonl", "a7d4f4346ef291d672df63a0dfcfc6622ea27a6ed89ac8c3fc40496de06114d5", "a7d4f4346ef291d672df63a0dfcfc6622ea27a6ed89ac8c3fc40496de06114d5"),
    (400, 599, "review-400-599.jsonl", "14272a9aa336cb9bb446c79082647abe28cacd3dd770e905a0ac86fbeb96aaf0", "14272a9aa336cb9bb446c79082647abe28cacd3dd770e905a0ac86fbeb96aaf0"),
    (600, 799, "review-600-799.jsonl", "663e5aff63341d986e3c1a2cf3131524b9e57bee3636f1c4d475de54ea510bd0", "663e5aff63341d986e3c1a2cf3131524b9e57bee3636f1c4d475de54ea510bd0"),
    (800, 999, "review-800-999.jsonl", "9f81257c216c61b47cdad266ca8d44e4bdfabc984c0c3b8bd2fe032022d1290c", "9f81257c216c61b47cdad266ca8d44e4bdfabc984c0c3b8bd2fe032022d1290c"),
    (1000, 1199, "review-1000-1199.jsonl", "d0d3a51b176789d43610cd26a02f8ff1e0b4f51f77ecdc48847a8590b39c3e19", "d0d3a51b176789d43610cd26a02f8ff1e0b4f51f77ecdc48847a8590b39c3e19"),
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return sha256(canonical({key: item for key, item in value.items() if key != field}))


def review_index(row: Mapping[str, Any]) -> int:
    value = row.get("source_index", row.get("index"))
    if not isinstance(value, int):
        raise AssertionError("review row has no integer index")
    return value


def review_disposition(row: Mapping[str, Any]) -> str:
    value = row.get("review_disposition", row.get("decision"))
    if value in {"eligible", "eligible_existing_quality_credit"}:
        return "eligible_existing_quality_credit"
    if value in {"pending", "reject"}:
        return str(value)
    raise AssertionError(f"unknown review disposition: {value!r}")


def grants_quality(row: Mapping[str, Any]) -> bool:
    if "grants_quality_credit" in row:
        return row["grants_quality_credit"] is True
    return row["dedupe"]["existing_quality_credit"] is True


def grants_new(row: Mapping[str, Any]) -> bool:
    if "grants_new_catalog_entry" in row:
        return row["grants_new_catalog_entry"] is True
    return row["dedupe"]["new_theorem_addition_credit"] is True


def review_identity(row: Mapping[str, Any]) -> tuple[str, str]:
    if "external_id" in row:
        return str(row["external_id"]), str(row["title"])
    identity = row["identity"]
    return str(identity["synthetic_source_id"]), str(identity["title"])


def verify_self_hash(row: Mapping[str, Any], field: str = "row_sha256") -> None:
    if row.get(field) != hash_without(row, field):
        raise AssertionError(f"{field} mismatch")


def load_inputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    source_path = ROOT / SOURCE_REL
    reference_path = ROOT / REFERENCE_REL
    natural_path = ROOT / NATURAL_JOIN_REL
    if file_sha256(source_path) != SOURCE_SHA256:
        raise AssertionError("1000+ source asset hash mismatch")
    if file_sha256(reference_path) != REFERENCE_SHA256:
        raise AssertionError("reference candidate asset hash mismatch")
    if file_sha256(natural_path) != NATURAL_JOIN_SHA256:
        raise AssertionError("NaturalProofs join asset hash mismatch")
    source = json.loads(source_path.read_text(encoding="utf-8"))["records"]
    references = json.loads(reference_path.read_text(encoding="utf-8"))["records"]
    if len(source) != 1200 or len(references) != 1200:
        raise AssertionError("source/reference cardinality mismatch")

    review_rows: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    for first, last, name, expected, pre_migration in SLICES:
        relative = CURATION_REL / "reviews" / name
        path = ROOT / relative
        payload = path.read_bytes()
        if sha256(payload) != expected or not payload.endswith(b"\n"):
            raise AssertionError(f"review slice hash/newline mismatch: {name}")
        rows = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
        if len(rows) != 200 or [review_index(row) for row in rows] != list(range(first, last + 1)):
            raise AssertionError(f"review slice range mismatch: {name}")
        review_rows.extend(rows)
        decisions = Counter(review_disposition(row) for row in rows)
        receipts.append(
            {
                "path": relative.as_posix(),
                "sha256": expected,
                "pre_repository_migration_sha256": pre_migration,
                "index_range": [first, last],
                "row_count": len(rows),
                "decision_counts": dict(sorted(decisions.items())),
                "existing_quality_credits": sum(grants_quality(row) for row in rows),
                "new_theorem_addition_credits": sum(grants_new(row) for row in rows),
            }
        )
    return source, references, review_rows, receipts


def build() -> dict[str, Any]:
    source, references, review_rows, receipts = load_inputs()
    if [review_index(row) for row in review_rows] != list(range(1200)):
        raise AssertionError("review index coverage mismatch")

    records: list[dict[str, Any]] = []
    for index, (src, ref, review) in enumerate(zip(source, references, review_rows, strict=True)):
        verify_self_hash(src)
        verify_self_hash(ref)
        external_id, title = review_identity(review)
        if external_id != src["external_id"] or external_id != ref["external_id"]:
            raise AssertionError(f"external identity mismatch at {index}")
        if title != src["title"] or title != ref["title"]:
            raise AssertionError(f"title mismatch at {index}")
        if src["source_record_id"] != ref["source_record_id"]:
            raise AssertionError(f"source record mismatch at {index}")
        if src["row_sha256"] != ref["source_row_sha256"]:
            raise AssertionError(f"source row binding mismatch at {index}")
        if index >= 200:
            if review["source_record_id"] != src["source_record_id"] or review["source_row_sha256"] != src["row_sha256"]:
                raise AssertionError(f"review source binding mismatch at {index}")

        disposition = review_disposition(review)
        quality_credit = grants_quality(review)
        new_credit = grants_new(review)
        if quality_credit != (disposition == "eligible_existing_quality_credit"):
            raise AssertionError(f"quality decision/credit mismatch at {index}")
        if new_credit:
            raise AssertionError(f"unsupported new theorem credit at {index}")

        claimed_review_hash = review.get("review_record_sha256")
        if claimed_review_hash is not None and claimed_review_hash != hash_without(review, "review_record_sha256"):
            raise AssertionError(f"review record hash mismatch at {index}")

        for candidate in ref["reference_candidates"]:
            verify_self_hash(candidate)
            if candidate["automatic_credit"] is not False:
                raise AssertionError(f"automatic reference credit at {index}")
            if candidate["review_state"] != "candidate_reference_not_yet_matched_to_theorem_statement":
                raise AssertionError(f"reference review state mismatch at {index}")
        if ref["review_boundary"]["importance_or_proof_credit_granted"] is not False:
            raise AssertionError(f"reference asset grants credit at {index}")

        slice_hash = next(spec[3] for spec in SLICES if spec[0] <= index <= spec[1])
        records.append(
            {
                "source_index": index,
                "source_record_id": src["source_record_id"],
                "source_row_sha256": src["row_sha256"],
                "external_id": src["external_id"],
                "title": src["title"],
                "msc2020": src["msc2020"],
                "review_disposition": disposition,
                "grants_existing_quality_credit": quality_credit,
                "grants_new_release_theorem_credit": False,
                "review_slice_sha256": slice_hash,
                "source_review_record_sha256": claimed_review_hash,
                "source_review_record_canonical_sha256": sha256(canonical(review)),
                "source_review_record": review,
                "reference_candidate_entry": {
                    "asset_row_sha256": ref["row_sha256"],
                    "candidate_count": len(ref["reference_candidates"]),
                    "candidates": ref["reference_candidates"],
                    "exact_theorem_support_verified": False,
                    "grants_existing_quality_credit": False,
                    "boundary": "manual citation-to-exact-theorem verification required before any credit",
                },
            }
        )

    decisions = Counter(row["review_disposition"] for row in records)
    document: dict[str, Any] = {
        "schema_version": "awesome-theorems/thousand-plus-landmark-ledger/5.5",
        "artifact_path": OUTPUT_REL.as_posix(),
        "review_as_of": "2026-08-10",
        "scope": {
            "kind": "1200_identity_candidate_pool_existing-catalog-quality-review",
            "not_a_release_append": True,
            "not_a_universal_importance_or_frontier_ranking": True,
            "release_theorem_credit_granted": 0,
            "release_conjecture_credit_granted": 0,
        },
        "provenance_policy": {
            "all_filesystem_paths_repository_relative": True,
            "ephemeral_path_authority_retained": False,
            "pre_repository_migration_ledger_sha256": PRE_MIGRATION_LEDGER_SHA256,
            "normalization": [
                {
                    "index_range": [0, 199],
                    "change": "replace two NaturalProofs scratch paths with the pinned repository join asset",
                    "upstream_content_sha256_preserved": True,
                }
            ],
        },
        "inputs": {
            "source_path": SOURCE_REL.as_posix(),
            "source_sha256": SOURCE_SHA256,
            "reference_candidate_path": REFERENCE_REL.as_posix(),
            "reference_candidate_sha256": REFERENCE_SHA256,
            "naturalproofs_join_path": NATURAL_JOIN_REL.as_posix(),
            "naturalproofs_join_sha256": NATURAL_JOIN_SHA256,
            "review_slices": receipts,
        },
        "counts": {
            "candidate_identities": len(records),
            "decision_counts": dict(sorted(decisions.items())),
            "existing_quality_credits": sum(row["grants_existing_quality_credit"] for row in records),
            "new_release_theorem_credits": 0,
            "strict_conjecture_credits": 0,
            "reference_candidates": sum(row["reference_candidate_entry"]["candidate_count"] for row in records),
            "reference_candidates_granting_credit": 0,
        },
        "records": records,
    }
    document["records_canonical_sha256"] = sha256(canonical(records))
    document["authority_sha256"] = sha256(canonical(document))
    encoded = canonical(document)
    if b"/tmp/" in encoded or b"/home/sansha/" in encoded:
        raise AssertionError("ephemeral or workstation-local path in generated ledger")
    return document


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true", help="write the canonical ledger")
    action.add_argument("--check", action="store_true", help="check byte-for-byte reproducibility")
    args = parser.parse_args()
    document = build()
    encoded = canonical(document) + b"\n"
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(encoded)
        mode = "WROTE"
    else:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != encoded:
            raise SystemExit("landmark ledger is absent or not reproducible; run with --write")
        mode = "PASS"
    counts = document["counts"]
    print(
        f"{mode} theorem quality landmark ledger rows={counts['candidate_identities']} "
        f"eligible={counts['existing_quality_credits']} "
        f"pending={counts['decision_counts']['pending']} reject={counts['decision_counts']['reject']} "
        f"new=0 authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
