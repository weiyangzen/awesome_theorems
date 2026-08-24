#!/usr/bin/env python3
"""Independently verify the repository-owned 1000+ landmark review ledger."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
LEDGER_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5/landmark-ledger-0-1199.json")
SOURCE_REL = Path("Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json")
REFERENCE_REL = Path("Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json")
NATURAL_JOIN_REL = Path("Docs/catalog/v5/sources/naturalproofs-proofwiki-1000-plus-title-join-v2.0.0.json.gz")
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
OPEN_REL = Path("Docs/catalog/v5/releases/5.4/Open_Claim_List.json")

LEDGER_SHA256 = "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471"
SOURCE_SHA256 = "fe61d56e4ba4cc3a9846e2b153edee32dae6b1266b668e1a63dd3639d867bdad"
REFERENCE_SHA256 = "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435"
NATURAL_JOIN_SHA256 = "3cb44f9f7ed62b402a892e0b485c38d3881b9a4e40c5f34135a57fbf1d8936b5"
MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
OPEN_SHA256 = "aa8acc2cfe859b7ce108863e51b69da6cbe9f5ab63a0b908ba7b811d82a165b4"
PRE_MIGRATION_LEDGER_SHA256 = "a8cffb16f0040c4acb82a6f49ca8d6cab67068f512aefd0dd9e40ee0d3d668bc"
EXPECTED_AUTHORITY_SHA256 = "2cc91efdcbd604f46fd7a4f59ca9f19b25a74fdabd5e829fc7a6c50e5c7bf844"
EXPECTED_RECORDS_SHA256 = "f33dbcdff40bc105e56375e58cc42cb16e4aac28b748b33834b7d959c385422e"

SLICE_SPECS = (
    (0, 199, "review-000-199.jsonl", "9bbaf8db012b5f7283bac1f2362717a27e50ef8178e379992e24a2693dd59052", "3eb4af305d3c74be3affdf7569b8c6df80ef5f9ff8db4ccafcfe3f604e54303c"),
    (200, 399, "review-200-399.jsonl", "a7d4f4346ef291d672df63a0dfcfc6622ea27a6ed89ac8c3fc40496de06114d5", "a7d4f4346ef291d672df63a0dfcfc6622ea27a6ed89ac8c3fc40496de06114d5"),
    (400, 599, "review-400-599.jsonl", "14272a9aa336cb9bb446c79082647abe28cacd3dd770e905a0ac86fbeb96aaf0", "14272a9aa336cb9bb446c79082647abe28cacd3dd770e905a0ac86fbeb96aaf0"),
    (600, 799, "review-600-799.jsonl", "663e5aff63341d986e3c1a2cf3131524b9e57bee3636f1c4d475de54ea510bd0", "663e5aff63341d986e3c1a2cf3131524b9e57bee3636f1c4d475de54ea510bd0"),
    (800, 999, "review-800-999.jsonl", "9f81257c216c61b47cdad266ca8d44e4bdfabc984c0c3b8bd2fe032022d1290c", "9f81257c216c61b47cdad266ca8d44e4bdfabc984c0c3b8bd2fe032022d1290c"),
    (1000, 1199, "review-1000-1199.jsonl", "d0d3a51b176789d43610cd26a02f8ff1e0b4f51f77ecdc48847a8590b39c3e19", "d0d3a51b176789d43610cd26a02f8ff1e0b4f51f77ecdc48847a8590b39c3e19"),
)


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


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


def values_for_key(value: Any, key: str) -> Iterable[Any]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key == key:
                yield child
            yield from values_for_key(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from values_for_key(child, key)


def review_index(row: Mapping[str, Any]) -> int:
    value = row.get("source_index", row.get("index"))
    require(isinstance(value, int), "review row has no integer index")
    return value


def review_disposition(row: Mapping[str, Any]) -> str:
    value = row.get("review_disposition", row.get("decision"))
    if value in {"eligible", "eligible_existing_quality_credit"}:
        return "eligible_existing_quality_credit"
    require(value in {"pending", "reject"}, f"unknown review disposition: {value!r}")
    return str(value)


def review_quality(row: Mapping[str, Any]) -> bool:
    if "grants_quality_credit" in row:
        return row["grants_quality_credit"] is True
    return row["dedupe"]["existing_quality_credit"] is True


def review_new_credit(row: Mapping[str, Any]) -> bool:
    if "grants_new_catalog_entry" in row:
        return row["grants_new_catalog_entry"] is True
    return row["dedupe"]["new_theorem_addition_credit"] is True


def review_identity(row: Mapping[str, Any]) -> tuple[str, str]:
    if "external_id" in row:
        return str(row["external_id"]), str(row["title"])
    identity = row["identity"]
    return str(identity["synthetic_source_id"]), str(identity["title"])


def verify_self_hash(row: Mapping[str, Any], label: str) -> None:
    require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"{label} row hash mismatch")


def verify_release_boundary(root: Path) -> None:
    manifest_path = root / MANIFEST_REL
    open_path = root / OPEN_REL
    require(file_sha256(manifest_path) == MANIFEST_SHA256, "release 5.4 manifest hash mismatch")
    require(file_sha256(open_path) == OPEN_SHA256, "release 5.4 open list hash mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    counts = manifest.get("counts", {})
    require(counts.get("cumulative_theorems") == 2500, "release theorem count changed")
    require(counts.get("effective_strict_conjecture_credits") == 1000, "release strict conjecture count changed")
    require(counts.get("origin_theorems") == 500 and counts.get("origin_open_claims") == 0, "release 5.4 origin counts changed")
    open_rows = json.loads(open_path.read_text(encoding="utf-8"))["records"]
    kinds = Counter(row["current_claim_kind"] for row in open_rows)
    require(kinds == Counter(conjecture=1001, open_problem=599), "release open-kind partition changed")


def check(root: Path = ROOT, ledger_path: Path | None = None) -> dict[str, Any]:
    ledger_path = ledger_path or root / LEDGER_REL
    source_path = root / SOURCE_REL
    reference_path = root / REFERENCE_REL
    natural_path = root / NATURAL_JOIN_REL
    require(file_sha256(ledger_path) == LEDGER_SHA256, "landmark ledger file hash mismatch")
    require(file_sha256(source_path) == SOURCE_SHA256, "1000+ source asset hash mismatch")
    require(file_sha256(reference_path) == REFERENCE_SHA256, "reference candidate asset hash mismatch")
    require(file_sha256(natural_path) == NATURAL_JOIN_SHA256, "NaturalProofs join asset hash mismatch")
    verify_release_boundary(root)

    encoded = ledger_path.read_bytes()
    require(encoded.endswith(b"\n"), "ledger lacks final newline")
    require(b"/tmp/" not in encoded and b"/home/sansha/" not in encoded, "ephemeral or workstation-local path in ledger")
    try:
        document = json.loads(encoded.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"cannot decode landmark ledger: {error}") from error
    require(document.get("schema_version") == "awesome-theorems/thousand-plus-landmark-ledger/5.5", "schema mismatch")
    require(document.get("artifact_path") == LEDGER_REL.as_posix(), "artifact path mismatch")
    require(document.get("authority_sha256") == EXPECTED_AUTHORITY_SHA256, "authority pin mismatch")
    require(document.get("authority_sha256") == hash_without(document, "authority_sha256"), "authority recomputation mismatch")
    require(document.get("scope") == {
        "kind": "1200_identity_candidate_pool_existing-catalog-quality-review",
        "not_a_release_append": True,
        "not_a_universal_importance_or_frontier_ranking": True,
        "release_theorem_credit_granted": 0,
        "release_conjecture_credit_granted": 0,
    }, "scope/credit boundary mismatch")
    provenance = document.get("provenance_policy", {})
    require(provenance.get("all_filesystem_paths_repository_relative") is True, "repository-relative path policy missing")
    require(provenance.get("ephemeral_path_authority_retained") is False, "ephemeral path retained as authority")
    require(provenance.get("pre_repository_migration_ledger_sha256") == PRE_MIGRATION_LEDGER_SHA256, "migration provenance mismatch")

    inputs = document.get("inputs", {})
    require(inputs.get("source_path") == SOURCE_REL.as_posix() and inputs.get("source_sha256") == SOURCE_SHA256, "source input binding mismatch")
    require(inputs.get("reference_candidate_path") == REFERENCE_REL.as_posix() and inputs.get("reference_candidate_sha256") == REFERENCE_SHA256, "reference input binding mismatch")
    require(inputs.get("naturalproofs_join_path") == NATURAL_JOIN_REL.as_posix() and inputs.get("naturalproofs_join_sha256") == NATURAL_JOIN_SHA256, "NaturalProofs input binding mismatch")

    source = json.loads(source_path.read_text(encoding="utf-8"))["records"]
    references = json.loads(reference_path.read_text(encoding="utf-8"))["records"]
    records = document.get("records")
    require(isinstance(records, list) and len(records) == len(source) == len(references) == 1200, "record cardinality mismatch")
    require([row.get("source_index") for row in records] == list(range(1200)), "ledger index coverage mismatch")
    require(len({row["source_record_id"] for row in records}) == 1200, "source record identity collision")
    require(len({(row["external_id"], row["title"], row["msc2020"]) for row in records}) == 1200, "semantic identity collision")
    require(document.get("records_canonical_sha256") == EXPECTED_RECORDS_SHA256, "record-set pin mismatch")
    require(document.get("records_canonical_sha256") == sha256(canonical(records)), "record-set recomputation mismatch")

    receipts = inputs.get("review_slices")
    require(isinstance(receipts, list) and len(receipts) == 6, "review slice receipt count mismatch")
    review_rows: list[dict[str, Any]] = []
    for receipt, spec in zip(receipts, SLICE_SPECS, strict=True):
        first, last, name, expected, pre_migration = spec
        relative = Path("Docs/catalog/v5/curation/theorem_quality_v5_5/reviews") / name
        require(receipt.get("path") == relative.as_posix(), f"review path mismatch: {name}")
        require(receipt.get("sha256") == expected, f"review receipt hash mismatch: {name}")
        require(receipt.get("pre_repository_migration_sha256") == pre_migration, f"review migration hash mismatch: {name}")
        require(receipt.get("index_range") == [first, last] and receipt.get("row_count") == 200, f"review receipt range mismatch: {name}")
        path = root / relative
        payload = path.read_bytes()
        require(sha256(payload) == expected and payload.endswith(b"\n"), f"review file hash/newline mismatch: {name}")
        require(b"/tmp/" not in payload and b"/home/sansha/" not in payload, f"ephemeral path in review: {name}")
        rows = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
        require(payload == b"".join(canonical(row) + b"\n" for row in rows), f"noncanonical review JSONL: {name}")
        require(len(rows) == 200 and [review_index(row) for row in rows] == list(range(first, last + 1)), f"review range mismatch: {name}")
        decisions = Counter(review_disposition(row) for row in rows)
        require(receipt.get("decision_counts") == dict(sorted(decisions.items())), f"review decision receipt mismatch: {name}")
        require(receipt.get("existing_quality_credits") == sum(review_quality(row) for row in rows), f"review quality count mismatch: {name}")
        require(receipt.get("new_theorem_addition_credits") == 0, f"review new-credit receipt mismatch: {name}")
        review_rows.extend(rows)

    normalized_natural_paths = 0
    for index, (record, src, ref, review) in enumerate(zip(records, source, references, review_rows, strict=True)):
        verify_self_hash(src, f"source {index}")
        verify_self_hash(ref, f"reference {index}")
        external_id, title = review_identity(review)
        require(record["source_index"] == index, f"index mismatch at {index}")
        require(record["source_record_id"] == src["source_record_id"] == ref["source_record_id"], f"source ID mismatch at {index}")
        require(record["source_row_sha256"] == src["row_sha256"] == ref["source_row_sha256"], f"source row binding mismatch at {index}")
        require(record["external_id"] == external_id == src["external_id"] == ref["external_id"], f"external ID mismatch at {index}")
        require(record["title"] == title == src["title"] == ref["title"], f"title mismatch at {index}")
        require(record["msc2020"] == src["msc2020"] == ref["msc2020"], f"MSC mismatch at {index}")
        require(record["source_review_record"] == review, f"embedded review mismatch at {index}")
        require(record["source_review_record_canonical_sha256"] == sha256(canonical(review)), f"embedded review hash mismatch at {index}")
        claimed = review.get("review_record_sha256")
        require(record["source_review_record_sha256"] == claimed, f"claimed review hash binding mismatch at {index}")
        if claimed is not None:
            require(claimed == hash_without(review, "review_record_sha256"), f"claimed review hash mismatch at {index}")
        if index >= 200:
            require(review["source_record_id"] == src["source_record_id"] and review["source_row_sha256"] == src["row_sha256"], f"review/source mismatch at {index}")

        disposition = review_disposition(review)
        quality = review_quality(review)
        require(record["review_disposition"] == disposition, f"normalized disposition mismatch at {index}")
        require(record["grants_existing_quality_credit"] == quality == (disposition == "eligible_existing_quality_credit"), f"quality boundary mismatch at {index}")
        require(review_new_credit(review) is False and record["grants_new_release_theorem_credit"] is False, f"new theorem credit at {index}")
        for field in ("grants_new_catalog_entry", "new_theorem_addition_credit", "grants_new_release_theorem_credit"):
            require(all(value in {False, 0} for value in values_for_key(record, field)), f"nested new theorem credit at {index}: {field}")
        require(all(value is False for value in values_for_key(review, "independent_universal_importance_ranking_claimed")), f"universal ranking claim at {index}")

        for join in review.get("exact_statement_joins", []):
            statement = join.get("statement_text")
            require(isinstance(statement, str) and join.get("statement_sha256") == sha256(statement.encode("utf-8")), f"statement join hash mismatch at {index}")
            if join.get("grants_existing_quality_credit"):
                require(join.get("complete_truth_apt_statement") is True and quality, f"unsupported statement credit at {index}")

        entry = record["reference_candidate_entry"]
        require(entry["asset_row_sha256"] == ref["row_sha256"], f"reference row mismatch at {index}")
        require(entry["candidates"] == ref["reference_candidates"], f"reference candidates mismatch at {index}")
        require(entry["candidate_count"] == len(ref["reference_candidates"]), f"reference count mismatch at {index}")
        require(entry["exact_theorem_support_verified"] is False and entry["grants_existing_quality_credit"] is False, f"unverified reference credit at {index}")
        for candidate in entry["candidates"]:
            verify_self_hash(candidate, f"reference candidate {index}")
            require(candidate["automatic_credit"] is False, f"automatic reference credit at {index}")
            require(candidate["review_state"] == "candidate_reference_not_yet_matched_to_theorem_statement", f"reference review state mismatch at {index}")
            require(candidate["context_sha256"] == sha256(candidate["context_text"].encode("utf-8")), f"reference context hash mismatch at {index}")

        for source_asset in values_for_key(review, "source_asset"):
            if source_asset == NATURAL_JOIN_REL.as_posix():
                normalized_natural_paths += 1
        expected_slice = next(spec[3] for spec in SLICE_SPECS if spec[0] <= index <= spec[1])
        require(record["review_slice_sha256"] == expected_slice, f"slice binding mismatch at {index}")

    require(normalized_natural_paths == 2, "NaturalProofs path normalization count mismatch")
    counts = Counter(row["review_disposition"] for row in records)
    require(counts == Counter(eligible_existing_quality_credit=439, pending=714, reject=47), "decision totals mismatch")
    summary = document.get("counts", {})
    require(summary.get("candidate_identities") == 1200, "candidate identity count mismatch")
    require(summary.get("decision_counts") == dict(sorted(counts.items())), "decision summary mismatch")
    require(summary.get("existing_quality_credits") == 439, "existing quality count mismatch")
    require(summary.get("new_release_theorem_credits") == 0 and summary.get("strict_conjecture_credits") == 0, "release credit leakage")
    require(summary.get("reference_candidates") == 5182 and summary.get("reference_candidates_granting_credit") == 0, "reference summary mismatch")
    return {
        "rows": 1200,
        "eligible_existing_quality": 439,
        "pending": 714,
        "reject": 47,
        "new_release_theorems": 0,
        "authority_sha256": document["authority_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", "--workspace", dest="workspace", type=Path, default=ROOT)
    parser.add_argument("--ledger", type=Path)
    args = parser.parse_args()
    try:
        result = check(args.workspace.resolve(), args.ledger.resolve() if args.ledger else None)
    except (CheckError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"FAIL theorem quality landmark ledger: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"overall_pass": True, **result}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
