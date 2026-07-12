#!/usr/bin/env python3
"""Check THM-M-0043 statement metadata against the elaborated artifacts."""

from pathlib import Path
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0043"
ITEM_ID = "S56-M-0043-STATEMENT"
BASE_REVISION = "4ecdda4863162748b3ee70bc4ec842789418145d"
EXPRESSION_SHA256 = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"


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
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1083
    assert item["phase"] == "statement" and item["layer"] == 1
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0043-INTAKE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    local_dag = load(HERE / "task-dag.json")
    statement_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM_ID)
    assert statement_task["state"] == "open"
    assert statement_task["worker_evidence"] == "statement target and transports self-tested pending master acceptance"

    assert statement["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM_ID
    assert statement["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == BASE_REVISION
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is False

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == instance["canonical_formal_target"]["declaration_or_expression"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert formal["statement_file_sha256"] == receipt["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert statement["direct_imports"] == receipt["direct_imports"] == [
        "Mathlib.Data.Complex.Basic",
        "Mathlib.LinearAlgebra.UnitaryGroup",
    ]

    expected_mutations = {
        "mutationRemovedNormalityHypothesis",
        "mutationChangedScalarDomain",
        "mutationChangedBinderScope",
        "mutationIncludedEmptyBoundary",
    }
    assert {row["declaration"] for row in statement["mutation_tests"]["killed"]} == expected_mutations
    assert {row["declaration"] for row in receipt["mutation_tests"]} == expected_mutations
    assert len(statement["checked_alternate_encodings"]) == len(receipt["checked_transports"]) == 2

    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is receipt["theorem_complete"] is False
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert statement["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]

    expected_owned = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == expected_owned
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n"), f"missing final newline: {path.name}"
            assert b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("statement artifact check: ok (THM-M-0043 exact target; H1/M3/R4; proof open)")


if __name__ == "__main__":
    main()
