#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0301."""

import argparse
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-0301"
ITEM_ID = "S56-M-0301-INTAKE"
BASE = "d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9"
BASE_TREE = "829a47c47ae831cada4f8acc6c2c00ba5883215e"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int):
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def find_target(value, theorem_id):
    if isinstance(value, dict):
        if value.get("theorem_id") == theorem_id:
            return value
        for child in value.values():
            found = find_target(child, theorem_id)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_target(child, theorem_id)
            if found is not None:
                return found
    return None


parser = argparse.ArgumentParser()
parser.add_argument("--worker-packet", type=Path)
args = parser.parse_args()

instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")
manifest = load(REPO / "Docs/Stage1_Targets_rev-5.6.json")
authority = load(REPO / "Docs/Stage1_Execution_DAG_rev-5.6.json")
target = find_target(manifest, THEOREM_ID)
authority_item = find_target(authority, THEOREM_ID)

assert target is not None and authority_item is not None
assert target["execution_rank"] == instance["execution_rank"] == 1047
assert target["name"] == instance["name_zh"]
assert target["category"] == instance["category_zh"]
assert target["intake_score"] == instance["intake_score"] == 94
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["theorem_complete"] is False

assert authority_item["id"] == ITEM_ID
assert authority_item["phase"] == "intake"
assert authority_item["state"] == "[ ]"
assert authority_item["depends_on"] == []
assert authority_item["owned_paths"] == ["Stage1_Instances/THM-M-0301"]
assert authority_item["deliverable"] == (
    "Create the theorem dossier, scope map, and source-statement crosswalk."
)

assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
assert instance["item_id"] == receipt["item_id"] == ITEM_ID
assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert instance["canonical_statement"] is None
assert instance["canonical_claim"] is None
formal = instance["canonical_formal_target"]
assert formal["module"] is None
assert formal["declaration_or_expression"] is None
assert formal["elaborated_expression_hash"] is None
assert formal["environment_fingerprint"] is None
assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert dag["theorem_complete"] is False and dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-0301-STATEMENT", [ITEM_ID]),
    ("S56-M-0301-ANCHOR_AUDIT", ["S56-M-0301-STATEMENT"]),
    ("S56-M-0301-OBLIGATION_TREE", ["S56-M-0301-ANCHOR_AUDIT"]),
    ("S56-M-0301-PROOF", ["S56-M-0301-OBLIGATION_TREE"]),
    ("S56-M-0301-VALIDATION", ["S56-M-0301-PROOF"]),
    ("S56-M-0301-RELEASE", ["S56-M-0301-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

revisions = instance["source_revisions"]
assert revisions["repository_base"] == receipt["base_revision"] == BASE
assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
assert revisions["mathlib"] == MATHLIB
assert revisions["target_manifest_sha256"] == sha256(
    REPO / "Docs/Stage1_Targets_rev-5.6.json"
)
assert revisions["authoritative_blueprint_sha256"] == sha256(
    REPO / "Docs/Stage1_Blueprint_rev-5.6.md"
)
assert revisions["execution_dag_sha256"] == sha256(
    REPO / "Docs/Stage1_Execution_DAG_rev-5.6.json"
)
assert revisions["execution_skill_sha256"] == sha256(
    REPO / "skills/execute-stage1-rev56/SKILL.md"
)
assert revisions["blueprint_guidelines_sha256"] == sha256(
    REPO / "Docs/Blueprint_Guidelines.md"
)
assert revisions["repository_math_source_sha256"] == sha256(
    REPO / "Docs/researches/math_theorems.md"
)
assert revisions["stage0_blueprint_sha256"] == sha256(REPO / "Docs/Stage0_Blueprint.md")
assert revisions["lean_toolchain_file_sha256"] == sha256(
    REPO / "Formalizations/Lean/lean-toolchain"
)
assert revisions["lake_manifest_sha256"] == sha256(
    REPO / "Formalizations/Lean/lake-manifest.json"
)

crosswalk = (OWNED / "source-statement-crosswalk.md").read_text(encoding="utf-8")
scope = (OWNED / "scope-map.md").read_text(encoding="utf-8")
assert excerpt_sha256(REPO / "Docs/researches/math_theorems.md", 2160, 2165) == (
    "39c77b4df80254840c9366477dd27ec93949769c4692577b6d28966c0a2f50dd"
)
assert excerpt_sha256(REPO / "Docs/researches/math_theorems.md", 2640, 2645) == (
    "f17f11092debfa2249b23cb06656c9fb440badc4687c85e56ab28ed9ddb62f22"
)
assert excerpt_sha256(REPO / "Docs/Stage0_Blueprint.md", 8305, 8330) == (
    "32f0add50f603d8c6cf133c71451120aa5ff05b152158f18611bbd7f56913f16"
)
assert excerpt_sha256(REPO / "Docs/Stage0_Blueprint.md", 9989, 10014) == (
    "15fe0737b81ea98f4ec88a71e3920af1c09578b96a2ffcc6b4650bcc158fe484"
)
assert "7352edb3d25ffcfd7473ad738751b5e0d8e7dccd13540b45a57647289405524d" in crosswalk
assert "Theorem 1" in crosswalk and "587" in crosswalk
assert "THM-M-0363" in crosswalk and "THM-M-0363" in scope
assert "later immutable anchor audit" in crosswalk

actual_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
assert actual_files == sorted(instance["owned_artifacts"])
hashed_files = [name for name in actual_files if name != "intake-receipt.json"]
assert sorted(receipt["owned_artifact_sha256"]) == sorted(hashed_files)
for name in hashed_files:
    assert receipt["owned_artifact_sha256"][name] == sha256(OWNED / name), name
for path in OWNED.iterdir():
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

assert receipt["proposed_state"] == "[_]"
assert receipt["accepted"] is receipt["content_addressed"] is False
assert receipt["acceptance_authority"] == "integration lane"
assert receipt["covered_node_ids"] == [ITEM_ID]
for field in [
    "accepted_receipt_ids",
    "proof_body_locations",
    "canonical_obligation_ids",
    "statement_fingerprints",
    "typed_graph_changes",
    "composition_certificates",
]:
    assert receipt[field] == []
assert receipt["audit_complete"] is receipt["theorem_complete"] is False
assert receipt["selftest_result"] == "pass"

if args.worker_packet is not None:
    packet_path = args.worker_packet
    if not packet_path.is_absolute():
        packet_path = REPO / packet_path
    packet = load(packet_path)
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"]["selftest_result"] == "pass"
    assert packet["output_summary"]["audit_complete"] is False
    assert packet["output_summary"]["theorem_complete"] is False

print("THM-M-0301 intake invariant check: ok (planned H1/M4/R4; six downstream tasks open)")
