#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0289."""

import argparse
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-0289"
ITEM_ID = "S56-M-0289-INTAKE"
BASE = "f294137feee7840fd105a4d3f6073d5cf45508ea"
BASE_TREE = "234b8f273d252c2c42ce6860315ed973049c871a"
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
assert target["execution_rank"] == instance["execution_rank"] == 1295
assert target["name"] == instance["name_zh"]
assert target["category"] == instance["category_zh"]
assert target["intake_score"] == instance["intake_score"] == 86
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["theorem_complete"] is False

assert authority_item["id"] == ITEM_ID
assert authority_item["phase"] == "intake"
assert authority_item["state"] == "[ ]"
assert authority_item["depends_on"] == []
assert authority_item["owned_paths"] == ["Stage1_Instances/THM-M-0289"]
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
    ("S56-M-0289-STATEMENT", [ITEM_ID]),
    ("S56-M-0289-ANCHOR_AUDIT", ["S56-M-0289-STATEMENT"]),
    ("S56-M-0289-OBLIGATION_TREE", ["S56-M-0289-ANCHOR_AUDIT"]),
    ("S56-M-0289-PROOF", ["S56-M-0289-OBLIGATION_TREE"]),
    ("S56-M-0289-VALIDATION", ["S56-M-0289-PROOF"]),
    ("S56-M-0289-RELEASE", ["S56-M-0289-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

revisions = instance["source_revisions"]
assert revisions["repository_base"] == receipt["base_revision"] == BASE
assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
assert revisions["mathlib"] == MATHLIB
for key, relative in {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}.items():
    assert revisions[key] == sha256(REPO / relative), key

assert excerpt_sha256(REPO / "Docs/researches/math_theorems.md", 2076, 2081) == (
    "27cf20aa057762329cb3aa19b346e99ddd2541e0c6c6d1ad3f3a6886e12d6465"
)
assert excerpt_sha256(REPO / "Docs/researches/math_theorems.md", 2675, 2680) == (
    "5d70728ca415609cc2ff264c0b498c57848c985d60310019daabc5189601b604"
)
assert excerpt_sha256(REPO / "Docs/Stage0_Blueprint.md", 7981, 8006) == (
    "4b9fbd1259b2225b0ca1ddeff51c571ab17dcc49e5568e1029c20a26443f5323"
)
assert excerpt_sha256(REPO / "Docs/Stage0_Blueprint.md", 10124, 10149) == (
    "cab16ddd14212c974b28433d3abef0be480d70742b1750d9c268e22a4ab58682"
)
crosswalk = (OWNED / "source-statement-crosswalk.md").read_text(encoding="utf-8")
scope = (OWNED / "scope-map.md").read_text(encoding="utf-8")
assert "10.1007/BF02547518" in crosswalk
assert "07fe6dcba8fe450170eafbbdb4a1ca4a8d62b0dcc214ce3d9e6d9db79a1ff8dc" in crosswalk
assert "source text was not inspected" in crosswalk
assert "THM-M-0368" in crosswalk and "THM-M-0368" in scope
assert "later immutable anchor audit" in crosswalk
assert "hasWeakType_maximalFunction_one" in crosswalk
assert "fdcce451b494680b1fd5534236a71d9b258860b2" in crosswalk

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
    assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

for relative in instance["public_merge_targets"]:
    assert relative.startswith("Stage1_Instances/THM-M-0289/")
    assert (REPO / relative).is_file(), relative
for name in [
    "README.md",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "validation.md",
]:
    text = (OWNED / name).read_text(encoding="utf-8")
    assert "/home/" not in text and ".cron/" not in text
    assert "theorem_complete=true" not in text
probe = (OWNED / "IntakeProbe.lean").read_text(encoding="utf-8")
prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
assert all(token not in probe for token in prohibited)

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

print("THM-M-0289 intake invariant check: ok (planned H1/M4/R4; six downstream tasks open)")
