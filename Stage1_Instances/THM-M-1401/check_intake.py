#!/usr/bin/env python3
"""Check the fail-closed THM-M-1401 planned-intake invariants."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


instance = load(ROOT / "instance.json")
dag = load(ROOT / "task-dag.json")
receipt = load(ROOT / "intake-receipt.json")
selftest = load(WORKSPACE / ".stage1-worker-selftest.json")

artifacts = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "IntakeProbe.lean",
    "check_intake.py",
    "validation.md",
    "intake-receipt.json",
}
task_ids = [
    "S56-M-1401-STATEMENT",
    "S56-M-1401-ANCHOR_AUDIT",
    "S56-M-1401-OBLIGATION_TREE",
    "S56-M-1401-PROOF",
    "S56-M-1401-VALIDATION",
    "S56-M-1401-RELEASE",
]

assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-1401"
assert instance["item_id"] == receipt["item_id"] == selftest["item_id"] == "S56-M-1401-INTAKE"
assert instance["lifecycle"] == dag["lifecycle"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert instance["execution_rank"] == 900
assert instance["baseline"] == "L0" and instance["rework_required"] is True
assert instance["canonical_claim"] is None
formal = instance["canonical_formal_target"]
assert all(
    formal[key] is None
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint")
)
assert instance["accepted_proof_state"] == dag["accepted_states"] == []
assert not any(
    (
        instance["audit_complete"],
        instance["theorem_complete"],
        receipt["accepted"],
        receipt["audit_complete"],
        receipt["theorem_complete"],
    )
)
assert receipt["proposed_state"] == selftest["state"] == "[_]"
assert set(instance["owned_artifacts"]) == artifacts
assert {path.name for path in ROOT.iterdir() if path.is_file()} == artifacts
assert [task["id"] for task in dag["tasks"]] == task_ids
assert all(task["state"] == "open" for task in dag["tasks"])
assert dag["tasks"][0]["depends_on"] == ["S56-M-1401-INTAKE"]
assert all(after["depends_on"] == [before["id"]] for before, after in zip(dag["tasks"], dag["tasks"][1:]))

changed_paths = {".stage1-worker-selftest.json"} | {
    f"Stage1_Instances/THM-M-1401/{artifact}" for artifact in artifacts
}
assert set(receipt["changed_paths"]) == set(selftest["changed_paths"]) == changed_paths
assert all((WORKSPACE / path).is_file() for path in instance["public_merge_targets"])

print("intake invariant check: ok")
