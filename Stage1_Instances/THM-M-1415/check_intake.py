#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1415."""

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-1415"
ITEM_ID = "S56-M-1415-INTAKE"
BASE_REVISION = "cbe531e6fdc68190477a9c7e8f635fe5a68a4bcd"
BASE_TREE = "0b4a5720f51c89484fdc5f6b6f07dc01ee1e95c8"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


manifest = load(REPO / "Docs/Stage1_Targets_rev-5.6.json")
targets = manifest["targets"] if isinstance(manifest, dict) else manifest
target = next(row for row in targets if row["theorem_id"] == THEOREM_ID)
instance = load(ROOT / "instance.json")
dag = load(ROOT / "task-dag.json")
receipt = load(ROOT / "intake-receipt.json")
if "--without-handoff" in sys.argv:
    selftest = None
else:
    selftest = load(REPO / ".stage1-worker-selftest.json")

assert target["execution_rank"] == 914
assert target["name"] == "Markov\u5206\u5272"
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["legacy_artifacts_accepted"] is False
assert target["target_lane"] == "hard_statement_first_partial_verification"
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
assert instance["item_id"] == receipt["item_id"] == ITEM_ID
if selftest is not None:
    assert selftest["item_id"] == ITEM_ID
assert instance["execution_rank"] == target["execution_rank"]
assert instance["lifecycle_mode"] == instance["lifecycle"] == dag["lifecycle_mode"]
assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
assert instance["intent"] == "intake"
assert instance["baseline"] == "L0" and instance["rework_required"] is True
assert instance["legacy_artifacts_accepted"] is False
assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

formal = instance["canonical_formal_target"]
for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
    assert formal[key] is None
assert instance["ordered_binders"] == instance["quantifiers"] == instance["hypotheses"] == []
assert instance["alternate_encodings"] == []
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert dag["theorem_complete"] is False and dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-1415-STATEMENT", [ITEM_ID]),
    ("S56-M-1415-ANCHOR_AUDIT", ["S56-M-1415-STATEMENT"]),
    ("S56-M-1415-OBLIGATION_TREE", ["S56-M-1415-ANCHOR_AUDIT"]),
    ("S56-M-1415-PROOF", ["S56-M-1415-OBLIGATION_TREE"]),
    ("S56-M-1415-VALIDATION", ["S56-M-1415-PROOF"]),
    ("S56-M-1415-RELEASE", ["S56-M-1415-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

catalog = (REPO / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
assert "**Markov\u5206\u5272**" in catalog
assert "- \u63d0\u51fa\u8005: Yakov Sinai/Rufus Bowen" in catalog
assert "- \u9648\u8ff0: \u53cc\u66f2\u7cfb\u7edf\u7684\u7b26\u53f7\u5316" in catalog
stage0 = (REPO / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
assert "THM-M-1415 Markov\u5206\u5272" in stage0
assert "- \u7cbe\u786e\u5b9a\u4e49\u4e0e\u524d\u63d0\u6761\u4ef6: \u5f85\u8865\u5145" in stage0

actual_artifacts = sorted(path.name for path in ROOT.iterdir() if path.is_file())
assert actual_artifacts == sorted(instance["owned_artifacts"])
expected_changed = sorted(
    [f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_artifacts]
    + [".stage1-worker-selftest.json"]
)
assert sorted(receipt["changed_paths"]) == expected_changed
if selftest is not None:
    assert sorted(selftest["changed_paths"]) == expected_changed
assert instance["public_merge_targets"] == [f"Stage1_Instances/{THEOREM_ID}"]

assert receipt["proposed_state"] == "[_]"
assert receipt["base_revision"] == BASE_REVISION
if selftest is not None:
    assert selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE_REVISION
assert receipt["base_tree"] == BASE_TREE
assert receipt["result"] == "pass" and receipt["master_acceptance"] is False
assert receipt["accepted_proof_state"] == receipt["accepted_receipt_ids"] == []
assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
assert instance["source_revisions"]["repository_base"] == BASE_REVISION
assert instance["source_revisions"]["repository_tree"] == BASE_TREE

for path in ROOT.iterdir():
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )
for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
    text = (ROOT / name).read_text(encoding="utf-8")
    assert "/home/" not in text and ".cron/" not in text
    assert "theorem_complete=true" not in text

print("THM-M-1415 intake invariant check: ok")
