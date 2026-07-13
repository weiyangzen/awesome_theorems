#!/usr/bin/env python3
"""Cross-check the THM-M-0487 statement record, receipt, and worker packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0487-STATEMENT"
THEOREM_ID = "THM-M-0487"
BASE_REVISION = "561d83df037004ceb2259292d7c63be930b40391"
EXPRESSION_SHA256 = "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"
SOURCE_SHA256 = "9d0200046173c0b0d9d0b52cbf696087f4beea6946c92bfa41f03402a4090b0d"
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0487/README.md",
    "Stage1_Instances/THM-M-0487/Statement.lean",
    "Stage1_Instances/THM-M-0487/check_intake.py",
    "Stage1_Instances/THM-M-0487/check_statement.py",
    "Stage1_Instances/THM-M-0487/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0487/instance.json",
    "Stage1_Instances/THM-M-0487/intake-receipt.json",
    "Stage1_Instances/THM-M-0487/scope-map.md",
    "Stage1_Instances/THM-M-0487/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0487/statement-receipt.json",
    "Stage1_Instances/THM-M-0487/statement-validation.md",
    "Stage1_Instances/THM-M-0487/statement.json",
    "Stage1_Instances/THM-M-0487/task-dag.json",
    "Stage1_Instances/THM-M-0487/validation.md",
]
PROHIBITED = (
    "sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ",
    "TODO", "FIXME", "placeholder",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict)
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1366
    assert item["phase"] == "statement" and item["layer"] == 1
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0487-INTAKE"]
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []

    assert statement["item_id"] == receipt["item_id"] == ITEM_ID
    assert statement["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert statement["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == SOURCE_SHA256 == sha256(HERE / "Statement.lean")
    assert formal["direct_imports"] == [
        "Mathlib.Algebra.Ring.Int.Parity",
        "Mathlib.Data.Nat.Prime.Defs",
    ]
    transports = {
        row["checked_witness"] for row in statement["checked_alternate_encodings"]
    }
    assert transports == {
        "Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget",
        "Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_integerWeakGoldbachTarget",
    }
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )

    assert receipt["phase"] == receipt["intent"] == "statement"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["base_revision"] == BASE_REVISION
    assert receipt["statement_fingerprints"] == [f"sha256:{EXPRESSION_SHA256}"]
    assert receipt["statement_file_sha256"] == SOURCE_SHA256
    assert receipt["worker_input_hashes"]["mathlib_int_parity_source_sha256"] == (
        "d3d4c39ee9a880a9da780c09807fa1e7f612cb2813454716edac0b69da2163f4"
    )
    assert receipt["worker_input_hashes"]["mathlib_nat_prime_defs_source_sha256"] == (
        "fb7b8f26c48fdb96c39d264574b70ba382d700a9a97a06ee41bb05377dfc68a4"
    )
    artifact_hashes = receipt["non_self_referential_changed_artifact_sha256"]
    for relative, expected in artifact_hashes.items():
        assert sha256(ROOT / relative) == expected
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    recipes = receipt["structured_validation_recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0487-STATEMENT-RECIPE-LEAN",
        "S56-M-0487-STATEMENT-RECIPE-CHECKER",
    }
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    assert {action["recipe_id"] for action in receipt["validation_actions"]} == {
        recipe["recipe_id"] for recipe in recipes
    }
    assert all(action["exit_code"] == 0 for action in receipt["validation_actions"])
    for field in (
        "owner", "attestor", "validated_at", "review_due", "support_state",
        "supersession_state", "revocation_state", "incident_path",
    ):
        assert receipt[field]
    assert receipt["invalidation_inputs"]

    assert instance["owned_artifacts"] == [
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "IntakeProbe.lean",
        "check_intake.py",
        "validation.md",
        "intake-receipt.json",
        "Statement.lean",
        "check_statement.py",
        "check_statement_artifacts.py",
        "statement.json",
        "statement-receipt.json",
        "statement-validation.md",
    ]

    actual_changed = {".stage1-worker-selftest.json"}
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE)],
        cwd=ROOT,
        text=True,
    )
    for line in status.splitlines():
        relative = line[3:]
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        actual_changed.add(relative)
    assert actual_changed == set(CHANGED_PATHS)

    lean = (HERE / "Statement.lean").read_text(encoding="utf-8")
    assert all(token not in lean for token in PROHIBITED)
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"]
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["commands"] == receipt["worker_packet_commands"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    print(
        "statement artifact check: ok "
        "(THM-M-0487 exact target; four mutations; pending master acceptance)"
    )


if __name__ == "__main__":
    main()
