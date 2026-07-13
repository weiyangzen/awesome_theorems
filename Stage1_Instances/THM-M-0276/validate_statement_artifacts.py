#!/usr/bin/env python3
"""Check THM-M-0276 statement records against the scoped worker handoff."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0276"
ITEM_ID = "S56-M-0276-STATEMENT"
BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
EXPRESSION_SHA256 = "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
NAMED_ROOT_SHA256 = "ec2954c0a55ee364e73f3b49407d1ef62ba1ff03807b1e53771181ef27f04d80"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0276/README.md",
    "Stage1_Instances/THM-M-0276/Statement.lean",
    "Stage1_Instances/THM-M-0276/check_statement.py",
    "Stage1_Instances/THM-M-0276/instance.json",
    "Stage1_Instances/THM-M-0276/scope-map.md",
    "Stage1_Instances/THM-M-0276/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0276/statement-receipt.json",
    "Stage1_Instances/THM-M-0276/statement-validation.md",
    "Stage1_Instances/THM-M-0276/statement.json",
    "Stage1_Instances/THM-M-0276/task-dag.json",
    "Stage1_Instances/THM-M-0276/validate_statement_artifacts.py",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1282
    assert item["phase"] == "statement" and item["layer"] == 1
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0276-INTAKE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert statement["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM_ID
    assert statement["theorem_id"] == receipt["theorem_id"] == instance["theorem_id"] == THEOREM_ID
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == BASE_REVISION
    assert subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip() == BASE_TREE
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False

    formal = statement["canonical_formal_target"]
    instance_formal = instance["canonical_formal_target"]
    assert formal["declaration_or_expression"] == instance_formal["declaration_or_expression"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["named_root_expression_sha256"] == receipt["named_root_expression_sha256"] == NAMED_ROOT_SHA256
    assert instance_formal["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert formal["statement_file_sha256"] == receipt["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert statement["direct_imports"] == receipt["direct_imports"] == ["Mathlib.Analysis.Complex.Basic"]

    expected_mutations = {
        "mutationRemovedSurjectivityHypothesis",
        "mutationChangedScalarDomain",
        "mutationChangedBinderScope",
        "mutationDroppedDomainCompleteness",
        "mutationExcludedNoninjectiveBoundary",
    }
    assert {row["declaration"] for row in statement["mutation_tests"]["killed"]} == expected_mutations
    assert {row["declaration"] for row in receipt["mutation_tests"]} == expected_mutations
    assert len(statement["checked_alternate_encodings"]) == len(receipt["checked_transports"]) == 1

    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is statement["audit_complete"] is statement["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert statement["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    expected_owned = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == expected_owned
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in expected_owned
    }
    for path in [*HERE.iterdir(), ROOT / ".stage1-worker-selftest.json"]:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("statement artifact check: ok (THM-M-0276 exact Real/Complex target; H2/M3/R4; proof open)")


if __name__ == "__main__":
    main()
