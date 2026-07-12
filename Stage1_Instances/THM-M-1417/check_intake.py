#!/usr/bin/env python3
"""Validate the fail-closed THM-M-1417 planned intake."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1417"
ITEM_ID = "S56-M-1417-INTAKE"
BASE_REVISION = "61ce73b9038706a45488f5644ad0e0f3d98937a1"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
instance = load(HERE / "instance.json")
dag = load(HERE / "task-dag.json")
receipt = load(HERE / "intake-receipt.json")
selftest = load(ROOT / ".stage1-worker-selftest.json")

assert target["execution_rank"] == instance["execution_rank"] == 916
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

assert instance["schema_version"] == "stage1-instance-intake/1.0"
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
assert instance["item_id"] == receipt["item_id"] == selftest["item_id"] == ITEM_ID
assert instance["lifecycle"] == dag["lifecycle"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
assert instance["literal_source_claim_zh"] == "耗散系统的物理测度"

formal = instance["canonical_formal_target"]
for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
    assert formal[key] is None
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
assert instance["audit_complete"] is receipt["audit_complete"] is False
assert instance["theorem_complete"] is receipt["theorem_complete"] is False

expected_tasks = [
    ("S56-M-1417-STATEMENT", [ITEM_ID]),
    ("S56-M-1417-ANCHOR_AUDIT", ["S56-M-1417-STATEMENT"]),
    ("S56-M-1417-OBLIGATION_TREE", ["S56-M-1417-ANCHOR_AUDIT"]),
    ("S56-M-1417-PROOF", ["S56-M-1417-OBLIGATION_TREE"]),
    ("S56-M-1417-VALIDATION", ["S56-M-1417-PROOF"]),
    ("S56-M-1417-RELEASE", ["S56-M-1417-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
assert set(instance["owned_artifacts"]) == actual_artifacts
expected_changed = {".stage1-worker-selftest.json"} | {
    f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_artifacts
}
assert set(receipt["changed_paths"]) == set(selftest["changed_paths"]) == expected_changed
assert receipt["base_revision"] == selftest["base_revision"] == BASE_REVISION
assert receipt["proposed_state"] == selftest["state"] == "[_]"
assert receipt["accepted"] is False
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []

for relative in instance["public_merge_targets"]:
    assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
    assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

for path in [ROOT / ".stage1-worker-selftest.json", *HERE.iterdir()]:
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
    text = (HERE / name).read_text(encoding="utf-8")
    assert "/home/" not in text and ".cron/" not in text
    assert "theorem_complete=true" not in text

print("intake invariant check: ok (THM-M-1417 planned; H5/M4/R4; six open tasks)")
