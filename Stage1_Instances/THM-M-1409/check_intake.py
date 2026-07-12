#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1409."""

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-1409"
ITEM_ID = "S56-M-1409-INTAKE"


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
manifest = json.loads((REPO / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = find_target(manifest)

assert target is not None and target["execution_rank"] == 908
assert target["name"] == "Kakutani塔"
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["theorem_id"] == target["theorem_id"] == THEOREM_ID
assert instance["item_id"] == ITEM_ID
assert instance["execution_rank"] == 908
assert instance["lifecycle"] == "planned" and instance["intent"] == "intake"
assert instance["baseline"] == "L0" and instance["rework_required"] is True
assert instance["canonical_claim"] is None

formal = instance["canonical_formal_target"]
assert formal["module"] is None and formal["declaration_or_expression"] is None
assert formal["elaborated_expression_hash"] is None
assert formal["environment_fingerprint"] is None
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
assert instance["accepted_proof_state"] == []
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["audit_complete"] is False and instance["theorem_complete"] is False

assert dag["theorem_id"] == THEOREM_ID and dag["lifecycle"] == "planned"
assert dag["accepted_states"] == []
expected_tasks = [
    ("S56-M-1409-STATEMENT", [ITEM_ID]),
    ("S56-M-1409-ANCHOR_AUDIT", ["S56-M-1409-STATEMENT"]),
    ("S56-M-1409-OBLIGATION_TREE", ["S56-M-1409-ANCHOR_AUDIT"]),
    ("S56-M-1409-PROOF", ["S56-M-1409-OBLIGATION_TREE"]),
    ("S56-M-1409-VALIDATION", ["S56-M-1409-PROOF"]),
    ("S56-M-1409-RELEASE", ["S56-M-1409-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

source = (REPO / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
assert "**Kakutani塔**" in source
assert "- 提出者: Shizuo Kakutani" in source
assert "- 时间: 1943" in source
assert "- 陈述: 诱导变换的构造" in source

actual_artifacts = sorted(path.name for path in ROOT.iterdir() if path.is_file())
assert actual_artifacts == sorted(instance["owned_artifacts"])

if len(sys.argv) == 3 and sys.argv[1] == "--worker-packet":
    packet_path = (REPO / sys.argv[2]).resolve()
    assert packet_path.is_relative_to(REPO)
    selftest = json.loads(packet_path.read_text(encoding="utf-8"))
    assert selftest["item_id"] == ITEM_ID and selftest["state"] == "[_]"
    assert selftest["base_revision"] == instance["source_revisions"]["repository_base"]
    assert isinstance(selftest["commands"], list) and selftest["commands"]
    assert isinstance(selftest["output_summary"], str) and selftest["output_summary"]
    assert isinstance(selftest["known_failures"], list) and selftest["known_failures"]
    declared_target_paths = sorted(
        path for path in selftest["changed_paths"]
        if path.startswith(f"Stage1_Instances/{THEOREM_ID}/")
    )
    assert declared_target_paths == sorted(
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_artifacts
    )
    assert ".stage1-worker-selftest.json" in selftest["changed_paths"]
elif len(sys.argv) != 1:
    raise SystemExit(f"usage: {Path(sys.argv[0]).name} [--worker-packet PATH]")

print("THM-M-1409 intake invariant check: ok")
