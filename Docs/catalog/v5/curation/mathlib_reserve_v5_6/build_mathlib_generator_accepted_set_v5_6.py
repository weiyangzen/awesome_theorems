#!/usr/bin/env python3
"""Build the 1,092-row candidate-only input for a future v5.6 generator."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Sequence

import build_mathlib_reserve_inventory_v5_6 as base


HERE = Path(__file__).resolve().parent
REPO = base.REPO
QUALIFIED = HERE / "Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl"
OUTPUT = HERE / "Mathlib_Generator_Accepted_Set_v5_6.jsonl"
QUALIFIED_SHA256 = "b03a2a3df17165b7f1e4bff7e2de80a8ecea6060a115b0fed66975827fb0f039"
SCHEMA = "awesome-theorems/mathlib-generator-accepted-candidate/5.6"


class AcceptedSetError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AcceptedSetError(message)


def load_qualified() -> tuple[list[dict[str, Any]], bytes]:
    payload = QUALIFIED.read_bytes()
    require(base.sha(payload) == QUALIFIED_SHA256, "qualified candidate ledger SHA-256 drifted")
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"qualified ledger line {line_number} is empty")
        try:
            row = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise AcceptedSetError(f"invalid qualified line {line_number}: {error}") from error
        require(isinstance(row, dict), f"qualified line {line_number} is not an object")
        require(raw == base.canonical(row), f"qualified line {line_number} is not canonical JSON")
        require(row.get("row_sha256") == base.hash_without(row, "row_sha256"), f"qualified line {line_number} seal is stale")
        rows.append(row)
    require(len(rows) == 1_561, "qualified ledger is not 1,561 rows")
    require([row.get("candidate_index") for row in rows] == list(range(1, 1_562)), "qualified indexes are not dense")
    return rows, payload


def build() -> list[dict[str, Any]]:
    qualified, _ = load_qualified()
    selected = [
        row
        for row in qualified
        if row.get("generator_lane") == "provisional_generator_admission"
        and row.get("generator_admission_qualified") is True
    ]
    require(len(selected) == 1_092, "provisional generator lane is not exactly 1,092 rows")
    require(
        sum(row.get("source_syntax_kind") == "theorem" for row in selected) == 707
        and sum(row.get("source_syntax_kind") == "lemma" for row in selected) == 385,
        "accepted source-syntax partition drifted",
    )
    output: list[dict[str, Any]] = []
    for acceptance_rank, source in enumerate(selected, 1):
        require(source.get("semantic_alias_evidence") == [], "provisional row unexpectedly has semantic alias evidence")
        require(source.get("theorem_record_kind") == "theorem", "provisional row is not a theorem record")
        require(source.get("candidate_only") is True, "qualified row crossed candidate-only boundary")
        row: dict[str, Any] = {
            "schema_version": SCHEMA,
            "acceptance_rank": acceptance_rank,
            "qualified_candidate_index": source["candidate_index"],
            "candidate_key": source["candidate_key"],
            "qualified_candidate_row_sha256": source["row_sha256"],
            "source_binding": source["source_binding"],
            "declaration": source["declaration"],
            "source_syntax_kind": source["source_syntax_kind"],
            "theorem_record_kind": "theorem",
            "formal_proof_state": source["formal_proof_state"],
            "formal_type_sha256": source["formal_type_sha256"],
            "normalized_formal_type_sha256": source["normalized_formal_type_sha256"],
            "normalized_declaration_name_sha256": source["normalized_declaration_name_sha256"],
            "module": source["module"],
            "module_root": source["module_root"],
            "runtime_truth_status": source["runtime_truth_status"],
            "documentation_status": source["documentation_status"],
            "credit_policy_status": source["credit_policy_status"],
            "formal_identity_status": source["formal_identity_status"],
            "semantic_canonical_status": source["semantic_canonical_status"],
            "semantic_alias_evidence_sha256": base.sha(base.canonical(source["semantic_alias_evidence"])),
            "qualification_status": "independently_checkable_for_future_release_transaction",
            "generator_disposition": "accepted_set_pending_release_transaction",
            "qualification_receipt_path": (
                "Docs/catalog/v5/curation/mathlib_reserve_v5_6/"
                "Mathlib_Generator_Acceptance_Receipt_v5_6.json"
            ),
            "target_variant_id": None,
            "target_stage_claim_id": None,
            "candidate_only": True,
            "release_credit_pending_transaction": True,
            "grants_catalog_entry": False,
            "grants_theorem_credit": False,
            "row_sha256": None,
        }
        row["row_sha256"] = base.hash_without(row, "row_sha256")
        output.append(row)
    return output


def payload(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(base.canonical(row) + b"\n" for row in rows)


def atomic_write(path: Path, data: bytes) -> None:
    with tempfile.NamedTemporaryFile(
        mode="wb", prefix=path.name + ".", suffix=".tmp", dir=path.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="atomically write accepted set")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        rows = build()
        expected = payload(rows)
        if args.write:
            atomic_write(OUTPUT, expected)
            action = "wrote"
        else:
            observed = OUTPUT.read_bytes()
            require(observed == expected, f"accepted set drifted: {base.sha(observed)} != {base.sha(expected)}")
            action = "checked"
        print(
            f"PASS {action} mathlib generator accepted set v5.6 "
            f"rows={len(rows)} sha256={base.sha(expected)}"
        )
        return 0
    except (AcceptedSetError, OSError) as error:
        print(f"FAIL mathlib generator accepted set v5.6: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
