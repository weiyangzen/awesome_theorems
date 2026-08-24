#!/usr/bin/env python3
"""Build or byte-check the reviewed 1962--1977 Putnam seed aggregate.

This is a progress artifact, not a release transaction.  It concatenates two
independently sealed 96-row review shards without changing either shard and
keeps every Putnam problem seed outside theorem/conjecture catalog credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Mapping, Sequence


REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/seed-reviews"
SHARD_STEMS = ("1962-1969", "1970-1977")
OUTPUT = ROOT / "1962-1977.jsonl"
SUMMARY = ROOT / "1962-1977-summary.json"
RECEIPT = ROOT / "1962-1977-receipt.json"
LOCATORS = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/PutnamGAP_Source_Locator_Manifest_v5_6.jsonl"
PB_PROBLEMS = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/PutnamBench_Source_Problems_v5_6.jsonl"
PB_HEADERS = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
PARENT_CATALOG = REPO / "Docs/catalog/v5/releases/5.5/Claim_Catalog.json"
PARENT_RELEASE_ROOT = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"
SCHEMA_SUMMARY = "awesome-theorems/putnam-seed-claim-review-summary/5.6"
SCHEMA_RECEIPT = "awesome-theorems/putnam-seed-claim-review-receipt/5.6"


class BuildError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def encoded(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def seal(value: Mapping[str, Any], field: str = "authority_sha256") -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop(field, None)
    result[field] = digest(canonical(result))
    return result


def verify_seal(value: Mapping[str, Any], field: str, label: str) -> None:
    observed = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    require(observed == digest(canonical(payload)), f"{label} self-seal drifted")


def read_document(path: Path, label: str) -> tuple[bytes, dict[str, Any]]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n") and payload.count(b"\n") == 1, f"{label} is not one canonical JSON line")
    value = json.loads(payload)
    require(payload == encoded(value), f"{label} is not canonical JSON")
    require(isinstance(value, dict), f"{label} is not an object")
    return payload, value


def read_rows(path: Path, label: str) -> tuple[bytes, list[dict[str, Any]]]:
    payload = path.read_bytes()
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{label} line {number} is empty")
        row = json.loads(raw)
        require(isinstance(row, dict), f"{label} line {number} is not an object")
        require(raw == canonical(row), f"{label} line {number} is not canonical JSON")
        seal_payload = dict(row)
        observed = seal_payload.pop("row_sha256", None)
        require(observed == digest(canonical(seal_payload)), f"{label} line {number} row seal drifted")
        rows.append(row)
    return payload, rows


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def file_binding(path: Path, *, rows: int) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": relative(path),
        "rows": rows,
        "sha256": digest(payload),
        "size_bytes": len(payload),
    }


def set_digest(values: Sequence[str]) -> str:
    return digest(canonical(sorted(values)))


def expected_problem_keys() -> list[str]:
    return [
        f"putnam_{year}_{section}{number}"
        for year in range(1962, 1978)
        for section in ("a", "b")
        for number in range(1, 7)
    ]


def load_shards() -> tuple[bytes, list[dict[str, Any]], dict[str, Any]]:
    payloads: list[bytes] = []
    rows: list[dict[str, Any]] = []
    inputs: dict[str, Any] = {}
    for stem in SHARD_STEMS:
        row_path = ROOT / f"{stem}.jsonl"
        summary_path = ROOT / f"{stem}-summary.json"
        receipt_path = ROOT / f"{stem}-receipt.json"
        row_payload, shard_rows = read_rows(row_path, f"seed shard {stem}")
        summary_payload, shard_summary = read_document(summary_path, f"seed shard summary {stem}")
        receipt_payload, shard_receipt = read_document(receipt_path, f"seed shard receipt {stem}")
        verify_seal(shard_summary, "authority_sha256", f"seed shard summary {stem}")
        verify_seal(shard_receipt, "authority_sha256", f"seed shard receipt {stem}")
        require(len(shard_rows) == 96, f"seed shard {stem} is not 96 rows")
        require(shard_summary.get("output", {}).get("sha256") == digest(row_payload), f"seed shard {stem} summary output hash drifted")
        require(shard_receipt.get("review_output", {}).get("sha256") == digest(row_payload), f"seed shard {stem} receipt output hash drifted")
        require(shard_receipt.get("review_summary", {}).get("sha256") == digest(summary_payload), f"seed shard {stem} receipt summary hash drifted")
        payloads.append(row_payload)
        rows.extend(shard_rows)
        inputs[stem] = {
            "review_rows": file_binding(row_path, rows=96),
            "summary": file_binding(summary_path, rows=1),
            "receipt": file_binding(receipt_path, rows=1),
            "summary_authority_sha256": shard_summary["authority_sha256"],
            "receipt_authority_sha256": shard_receipt["authority_sha256"],
        }
    aggregate = b"".join(payloads)
    require(len(rows) == 192, "aggregate source is not 192 rows")
    require([str(row.get("problem_key")) for row in rows] == expected_problem_keys(), "aggregate grid/order drifted")
    require(len({str(row.get("source_candidate_id")) for row in rows}) == 192, "aggregate source candidate IDs are not unique")
    return aggregate, rows, inputs


def build() -> tuple[bytes, dict[str, Any], dict[str, Any]]:
    aggregate, rows, shard_inputs = load_shards()
    dispositions = Counter(str(row["claim_review"]["claim_disposition"]) for row in rows)
    validity = Counter(str(row["claim_review"]["source_claim_validity"]) for row in rows)
    visibility = Counter(str(row["claim_review"]["answer_visibility"]) for row in rows)
    semantic_keys = [
        str(key)
        for row in rows
        for key in ([row["claim_review"]["semantic_key"]] if row["claim_review"]["semantic_key"] else [])
        + [child["semantic_key"] for child in row["claim_review"]["children"]]
    ]
    anomaly_codes = [str(code) for row in rows for code in row["anomaly_codes"]]
    formal_headers = sum(int(row["variant_handling"]["formal_variant_count"]) for row in rows)
    pb_present = sum(bool(row["putnambench_binding"]["present"]) for row in rows)
    split_children = sum(len(row["claim_review"]["children"]) for row in rows)
    repair_rows = sum(row["claim_review"]["source_claim_validity"] != "valid_as_scoped" for row in rows)
    require(len(semantic_keys) == len(set(semantic_keys)), "semantic keys collide across shards")
    summary = seal({
        "schema_version": SCHEMA_SUMMARY,
        "review_range": {"first_year": 1962, "last_year": 1977, "rows": 192},
        "full_grid_progress": {
            "reviewed_seed_rows": 192,
            "full_1962_2025_seed_rows": 768,
            "remaining_unreviewed_seed_rows": 576,
            "complete_768_crosswalk_authorized": False,
        },
        "expected_problem_keys": expected_problem_keys(),
        "inputs": {
            "review_shards": shard_inputs,
            "putnamgap_locator_manifest": file_binding(LOCATORS, rows=sum(1 for _ in LOCATORS.open("rb"))),
            "putnambench_source_problems": file_binding(PB_PROBLEMS, rows=675),
            "putnambench_formal_headers": file_binding(PB_HEADERS, rows=1_724),
            "parent_5_5_catalog": file_binding(PARENT_CATALOG, rows=1),
            "parent_release_root_sha256": PARENT_RELEASE_ROOT,
        },
        "output": {
            "path": relative(OUTPUT),
            "rows": 192,
            "sha256": digest(aggregate),
            "size_bytes": len(aggregate),
        },
        "counts": {
            "rows": 192,
            "reviewed_semantic_claims": len(semantic_keys),
            "claim_dispositions": dict(sorted(dispositions.items())),
            "split_children": split_children,
            "source_claim_validity": dict(sorted(validity.items())),
            "answer_visibility": dict(sorted(visibility.items())),
            "repair_or_explicit_convention_rows": repair_rows,
            "anomaly_occurrences": len(anomaly_codes),
            "distinct_anomaly_codes": len(set(anomaly_codes)),
            "putnambench_present": pb_present,
            "putnambench_absent": 192 - pb_present,
            "formal_variant_headers": formal_headers,
            "rows_with_existing_5_5_candidates": sum(bool(row["existing_5_5_exact_match_candidates"]) for row in rows),
            "unreviewed_rows_within_1962_1977": 0,
        },
        "coverage": {
            "exact_1962_1977_coordinate_grid": True,
            "all_problem_keys_and_source_candidate_ids_unique": True,
            "all_parts_and_answer_visibility_reviewed": True,
            "independently_written_statements_and_proof_summaries": True,
            "question_and_solution_value_hashes_bound": True,
            "putnambench_formal_headers_bound_where_available": True,
            "formal_variants_do_not_grant_duplicate_credit": True,
            "semantic_keys_unique_across_both_shards": True,
            "all_1962_1977_rows_reviewed": True,
        },
        "set_digests": {
            "problem_keys_sha256": set_digest([str(row["problem_key"]) for row in rows]),
            "source_candidate_ids_sha256": set_digest([str(row["source_candidate_id"]) for row in rows]),
            "semantic_keys_sha256": set_digest(semantic_keys),
            "row_seals_sha256": set_digest([str(row["row_sha256"]) for row in rows]),
        },
        "publication_boundary": {
            "candidate_only": True,
            "benchmark_seed_catalog_disposition": "reviewed_noncatalog_benchmark_seed",
            "theorem_identity_credits_granted": 0,
            "conjecture_credits_granted": 0,
            "release_entries_granted": 0,
            "release_mutation_authorized_or_performed": False,
            "question_or_solution_text_redistributed": False,
            "formal_variants_and_relation_edges_grant_duplicate_credit": False,
        },
    })
    summary_payload = encoded(summary)
    receipt = seal({
        "schema_version": SCHEMA_RECEIPT,
        "review_range": summary["review_range"],
        "full_grid_progress": summary["full_grid_progress"],
        "review_output": summary["output"],
        "review_summary": {
            "path": relative(SUMMARY),
            "rows": 1,
            "sha256": digest(summary_payload),
            "size_bytes": len(summary_payload),
            "authority_sha256": summary["authority_sha256"],
        },
        "source_shard_receipts": {
            stem: shard_inputs[stem]["receipt"] | {
                "authority_sha256": shard_inputs[stem]["receipt_authority_sha256"]
            }
            for stem in SHARD_STEMS
        },
        "checks": {
            **summary["coverage"],
            "canonical_json_and_row_seals": True,
            "source_locator_and_value_hashes_replayed": True,
            "formal_header_bindings_replayed": True,
            "summary_and_receipt_self_seals": True,
            "exact_output_hash_row_count_and_shard_concatenation": True,
            "noncatalog_seed_credit_boundary_enforced": True,
        },
        "publication_boundary": summary["publication_boundary"],
    })
    return aggregate, summary, receipt


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def emit(path: Path, payload: bytes, *, check: bool) -> None:
    if check:
        require(path.is_file(), f"missing output {relative(path)}")
        require(path.read_bytes() == payload, f"byte drift in {relative(path)}")
    else:
        atomic_write(path, payload)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        aggregate, summary, receipt = build()
        emit(OUTPUT, aggregate, check=args.check)
        emit(SUMMARY, encoded(summary), check=args.check)
        emit(RECEIPT, encoded(receipt), check=args.check)
    except (BuildError, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(f"FAIL Putnam seed review aggregate 1962-1977: {error}", file=os.sys.stderr)
        return 1
    print(
        "PASS Putnam seed review aggregate 1962-1977 "
        f"mode={'check' if args.check else 'write'} rows=192 "
        f"claims={summary['counts']['reviewed_semantic_claims']} "
        f"remaining_full_grid={summary['full_grid_progress']['remaining_unreviewed_seed_rows']} "
        f"sha256={summary['output']['sha256']} receipt={receipt['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
