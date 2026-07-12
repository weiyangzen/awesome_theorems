#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0036 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0036"
THEOREM_ID = "THM-M-0036"
ITEM_ID = "S56-M-0036-INTAKE"
BASE = "dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8"
BASE_TREE = "25138aaafcff80ee47bf04805bccd804978e6754"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--worker-packet", type=Path)
args = parser.parse_args()

manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
assigned = next(row for row in execution["items"] if row["id"] == ITEM_ID)

assert target == {
    "execution_rank": 1079,
    "legacy_priority_slot": None,
    "theorem_id": THEOREM_ID,
    "name": "阿廷-韦德尔本定理",
    "category": "代数学 / 环论",
    "source_status_untrusted": "已验证",
    "baseline": "L0",
    "rework_required": True,
    "legacy_artifacts_accepted": False,
    "target_lane": "hard_statement_first_partial_verification",
    "intake_score": 86,
    "lifecycle_mode": "planned",
    "theorem_complete": False,
}
assert assigned == {
    "id": ITEM_ID,
    "theorem_id": THEOREM_ID,
    "execution_rank": 1079,
    "phase": "intake",
    "layer": 0,
    "state": "[ ]",
    "depends_on": [],
    "owned_paths": ["Stage1_Instances/THM-M-0036"],
    "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}

assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
assert instance["item_id"] == receipt["item_id"] == ITEM_ID
assert instance["execution_rank"] == target["execution_rank"]
assert instance["baseline"] == target["baseline"] == "L0"
assert instance["rework_required"] is target["rework_required"] is True
assert instance["legacy_artifacts_accepted"] is target["legacy_artifacts_accepted"] is False
assert instance["legacy_priority_slot"] is target["legacy_priority_slot"] is None
assert instance["target_lane"] == target["target_lane"]
assert instance["intake_score"] == target["intake_score"]
assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"

assert instance["canonical_statement"] is None
assert instance["canonical_claim"] is None
formal = instance["canonical_formal_target"]
assert formal["module"] is formal["declaration_or_expression"] is None
assert formal["elaborated_expression_hash"] is formal["environment_fingerprint"] is None
assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert dag["audit_complete"] is dag["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-0036-STATEMENT", "statement", 1, [ITEM_ID]),
    ("S56-M-0036-ANCHOR_AUDIT", "anchor_audit", 2, ["S56-M-0036-STATEMENT"]),
    ("S56-M-0036-OBLIGATION_TREE", "obligation_tree", 3, ["S56-M-0036-ANCHOR_AUDIT"]),
    ("S56-M-0036-PROOF", "proof", 4, ["S56-M-0036-OBLIGATION_TREE"]),
    ("S56-M-0036-VALIDATION", "validation", 5, ["S56-M-0036-PROOF"]),
    ("S56-M-0036-RELEASE", "release", 6, ["S56-M-0036-VALIDATION"]),
]
assert [
    (task["id"], task["phase"], task["layer"], task["depends_on"])
    for task in dag["tasks"]
] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])
assert all(task["owned_paths"] == ["Stage1_Instances/THM-M-0036"] for task in dag["tasks"])
assert all(
    task["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    and task["evidence_ids"] == []
    and task["deliverable"]
    for task in dag["tasks"]
)

actual_owned = {path.name for path in OWNED.iterdir() if path.is_file()}
assert actual_owned == OWNED_FILES
assert set(instance["owned_artifacts"]) == OWNED_FILES
hashed = OWNED_FILES - {"intake-receipt.json"}
assert set(receipt["untracked_owned_artifact_sha256"]) == hashed
for name in hashed:
    assert receipt["untracked_owned_artifact_sha256"][name] == sha256(OWNED / name)

for path in OWNED.iterdir():
    if path.is_file():
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

source_paths = {
    "target_manifest_sha256": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": ROOT / "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": ROOT / "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": ROOT / "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": ROOT / "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": ROOT / "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
    "mathlib_candidate_source_sha256": ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/SimpleModule/WedderburnArtin.lean",
    "mathlib_csa_defs_sha256": ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/BrauerGroup/Defs.lean",
    "foreign_legacy_wrapper_sha256": ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_078.lean",
}
for field, path in source_paths.items():
    actual = sha256(path)
    assert instance["source_revisions"][field] == actual, field
    assert receipt["worker_input_hashes"][field] == actual, field

assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == BASE
assert subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip() == BASE_TREE
assert instance["source_revisions"]["repository_base"] == receipt["base_revision"] == BASE
assert instance["source_revisions"]["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
assert instance["source_revisions"]["mathlib"] == MATHLIB
assert instance["source_revisions"]["mathlib_tree"] == MATHLIB_TREE
assert subprocess.check_output(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"), "rev-parse", "HEAD"],
    text=True,
).strip() == MATHLIB

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["receipt_id"] == receipt["selftest_id"] == f"{ITEM_ID}-worker-selftest"
assert receipt["receipt_class"] == "provisional_worker_selftest"
assert receipt["accepted"] is receipt["content_addressed"] is False
assert receipt["selftest_result"] == "pass"
assert receipt["assigned_layer"] == assigned["layer"]
assert receipt["authoritative_state_before"] == assigned["state"]
assert receipt["proposed_state"] == "[_]"
assert receipt["completion_gate"] == assigned["completion_gate"]
assert receipt["covered_node_ids"] == [ITEM_ID]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
assert receipt["audit_complete"] is receipt["theorem_complete"] is False
assert receipt["known_failures"]

if args.worker_packet:
    packet = load(args.worker_packet.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE and packet["base_tree"] == BASE_TREE
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False

print("intake invariant check: ok (THM-M-0036 planned; H1/M3/R4; six open tasks)")
