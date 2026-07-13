#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0626"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--worker-packet", type=Path)
args = parser.parse_args()

target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
targets = target_data if isinstance(target_data, list) else target_data["targets"]
target = next(item for item in targets if item["theorem_id"] == "THM-M-0626")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")
execution_data = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
assigned = next(
    item for item in execution_data["items"] if item["id"] == "S56-M-0626-INTAKE"
)

assert target["execution_rank"] == instance["execution_rank"] == 1320
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["target_lane"] == instance["target_lane"]
assert target["intake_score"] == instance["intake_score"] == 86
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-0626"
assert instance["item_id"] == receipt["item_id"] == "S56-M-0626-INTAKE"
assert assigned == {
    "id": "S56-M-0626-INTAKE",
    "theorem_id": "THM-M-0626",
    "execution_rank": 1320,
    "phase": "intake",
    "layer": 0,
    "state": "[ ]",
    "depends_on": [],
    "owned_paths": ["Stage1_Instances/THM-M-0626"],
    "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
assert receipt["phase"] == receipt["intent"] == assigned["phase"]
assert receipt["assigned_layer"] == assigned["layer"]
assert receipt["authoritative_state_before"] == assigned["state"]
assert receipt["proposed_state"] == "[_]"
assert receipt["completion_gate"] == assigned["completion_gate"]

assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
assert instance["intent"] == "intake"
assert instance["canonical_statement"].startswith("Candidate intake scope:")
assert instance["canonical_claim"] == (
    "A continuous map sends every nonempty connected subset to a nonempty connected image."
)
formal = instance["canonical_formal_target"]
assert formal["module"] is None
assert formal["declaration_or_expression"] is None
assert formal["elaborated_expression_hash"] is None
assert formal["environment_fingerprint"] is None
assert formal["declaration_candidates"] == ["IsConnected.image"]
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert dag["audit_complete"] is False and dag["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-0626-STATEMENT", "statement", 1, ["S56-M-0626-INTAKE"]),
    ("S56-M-0626-ANCHOR_AUDIT", "anchor_audit", 2, ["S56-M-0626-STATEMENT"]),
    ("S56-M-0626-OBLIGATION_TREE", "obligation_tree", 3,
     ["S56-M-0626-ANCHOR_AUDIT"]),
    ("S56-M-0626-PROOF", "proof", 4, ["S56-M-0626-OBLIGATION_TREE"]),
    ("S56-M-0626-VALIDATION", "validation", 5, ["S56-M-0626-PROOF"]),
    ("S56-M-0626-RELEASE", "release", 6, ["S56-M-0626-VALIDATION"]),
]
assert [
    (task["id"], task["phase"], task["layer"], task["depends_on"])
    for task in dag["tasks"]
] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])
assert all(task["owned_paths"] == ["Stage1_Instances/THM-M-0626"] for task in dag["tasks"])
assert all(
    task["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    and task["evidence_ids"] == []
    and task["deliverable"]
    for task in dag["tasks"]
)

owned_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
assert sorted(instance["owned_artifacts"]) == owned_files
hashed_files = [name for name in owned_files if name != "intake-receipt.json"]
assert sorted(receipt["untracked_owned_artifact_sha256"]) == sorted(hashed_files)
for name in hashed_files:
    assert receipt["untracked_owned_artifact_sha256"][name] == sha256(OWNED / name), (
        f"owned artifact hash mismatch: {name}"
    )

for path in OWNED.iterdir():
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert b"\x00" not in data, f"NUL byte: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

base = "d1b510bacab792f84a99231485cf4429fdb78978"
tree = "f77c4e4db196fc0ecc271815514a411d06ea6053"
assert receipt["base_revision"] == instance["source_revisions"]["repository_base"] == base
assert receipt["base_tree"] == instance["source_revisions"]["repository_base_tree"] == tree
assert instance["source_revisions"]["mathlib"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert instance["source_revisions"]["mathlib_tree"] == (
    "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
)

input_hashes = {
    "target_manifest_sha256": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "authoritative_blueprint_sha256": "f79eb00e787d3356209879a046caae86de60d355daf11ae8923d6e90c511c625",
    "execution_dag_sha256": "ba0a151d3cb8c7fc6fbc0db54fe0653663c09d40c83790cd0ba185794d0931f8",
    "execution_skill_sha256": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "blueprint_guidelines_sha256": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "repository_math_source_sha256": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "stage0_blueprint_sha256": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "lean_toolchain_file_sha256": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake_manifest_sha256": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "mathlib_connected_basic_source_sha256": "929f0e1c789b8c0ed10c3164aa174e369b9b250317c525a8ad2f2dcca2a65e9c",
}
input_paths = {
    "target_manifest_sha256": ROOT / "Docs" / "Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": ROOT / "skills" / "execute-stage1-rev56" / "SKILL.md",
    "blueprint_guidelines_sha256": ROOT / "Docs" / "Blueprint_Guidelines.md",
    "repository_math_source_sha256": ROOT / "Docs" / "researches" / "math_theorems.md",
    "stage0_blueprint_sha256": ROOT / "Docs" / "Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": ROOT / "Formalizations" / "Lean" / "lean-toolchain",
    "lake_manifest_sha256": ROOT / "Formalizations" / "Lean" / "lake-manifest.json",
    "mathlib_connected_basic_source_sha256": ROOT / "Formalizations" / "Lean" / ".lake" /
        "packages" / "mathlib" / "Mathlib" / "Topology" / "Connected" / "Basic.lean",
}
for key, expected in input_hashes.items():
    assert sha256(input_paths[key]) == expected, f"actual input hash mismatch: {key}"
    assert instance["source_revisions"][key] == expected
    assert receipt["worker_input_hashes"][key] == expected

assert subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip() == base
assert subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
).strip() == tree
mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == instance["source_revisions"]["mathlib"]

assert receipt["receipt_class"] == "provisional_worker_selftest"
assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["receipt_id"] == receipt["selftest_id"] == (
    "S56-M-0626-INTAKE-worker-selftest"
)
assert receipt["accepted"] is False and receipt["content_addressed"] is False
assert receipt["selftest_result"] == "pass"
assert receipt["covered_node_ids"] == ["S56-M-0626-INTAKE"]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []

if args.worker_packet:
    packet = load(args.worker_packet)
    assert packet["item_id"] == "S56-M-0626-INTAKE"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == base
    assert packet["receipt_id"] == receipt["selftest_id"]
    assert packet["changed_paths"] == receipt["changed_path_scope"]
    assert receipt["worker_input_hashes"]["worker_packet_sha256"] == sha256(args.worker_packet)
    assert packet["known_failures"]
    data = args.worker_packet.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

print("intake invariant check: ok (THM-M-0626 planned; H1/M3/R4; six open tasks)")
