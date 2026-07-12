#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0098."""

import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-0098"
ITEM_ID = "S56-M-0098-INTAKE"


def find_target(value):
    if isinstance(value, dict):
        if value.get("theorem_id") == THEOREM_ID:
            return value
        for child in value.values():
            found = find_target(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_target(child)
            if found is not None:
                return found
    return None


instance = json.loads((ROOT / "instance.json").read_text(encoding="utf-8"))
dag = json.loads((ROOT / "task-dag.json").read_text(encoding="utf-8"))
selftest = json.loads((REPO / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
manifest = json.loads((REPO / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = find_target(manifest)

assert target is not None and target["execution_rank"] == 899
assert instance["theorem_id"] == target["theorem_id"] == THEOREM_ID
assert instance["item_id"] == selftest["item_id"] == ITEM_ID
assert instance["execution_rank"] == 899
assert instance["lifecycle"] == "planned" and instance["intent"] == "intake"
assert instance["baseline"] == "L0" and instance["rework_required"] is True
assert instance["canonical_claim"] is None

formal = instance["canonical_formal_target"]
assert formal["module"] is None and formal["declaration_or_expression"] is None
assert formal["elaborated_expression_hash"] is None
assert formal["environment_fingerprint"] is None
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is False and instance["theorem_complete"] is False

assert dag["theorem_id"] == THEOREM_ID and dag["lifecycle"] == "planned"
assert dag["accepted_states"] == []
expected_tasks = [
    ("S56-M-0098-STATEMENT", [ITEM_ID]),
    ("S56-M-0098-ANCHOR_AUDIT", ["S56-M-0098-STATEMENT"]),
    ("S56-M-0098-OBLIGATION_TREE", ["S56-M-0098-ANCHOR_AUDIT"]),
    ("S56-M-0098-PROOF", ["S56-M-0098-OBLIGATION_TREE"]),
    ("S56-M-0098-VALIDATION", ["S56-M-0098-PROOF"]),
    ("S56-M-0098-RELEASE", ["S56-M-0098-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

source = (REPO / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
assert "**朗兰兹纲领基本引理**" in source
assert "- 陈述: 自守表示与伽罗瓦表示的对应" in source

actual_artifacts = sorted(path.name for path in ROOT.iterdir() if path.is_file())
assert actual_artifacts == sorted(instance["owned_artifacts"])
declared_target_paths = sorted(
    path for path in selftest["changed_paths"] if path.startswith(f"Stage1_Instances/{THEOREM_ID}/")
)
assert declared_target_paths == sorted(
    f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_artifacts
)
assert selftest["state"] == "[_]"
assert selftest["base_revision"] == instance["source_revisions"]["repository_base"]

print("THM-M-0098 intake invariant check: ok")
