#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0881"
BASE = "d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9"
BASE_TREE = "829a47c47ae831cada4f8acc6c2c00ba5883215e"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
TARGET_EXCERPT_SHA256 = "7cf6c15a559d748ff69d47a6308a2610f45facb6e94c661dfaf0c7dc48364e80"
WORKER_SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_Applicable_Theorems.md": "779e4bd66e6a1c7615ca2884d899f02a871096125a30b8e229536fa5937cc85c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "bcbce90f45f8df2b674e642470a641bea5a6df5c750be2ac69aa7e686f1c1d72",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0f01e5060d405907103ce214fe2b550b50fc081fbb0dd39f6ca3713cc23bfcd0",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": LEAN_TOOLCHAIN_SHA256,
    "Formalizations/Lean/lake-manifest.json": LAKE_MANIFEST_SHA256,
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Basic.lean": "ae6fd7c95ad151f84eb316d32c518485e9877bdda0d9eb6b4aac9e041676ad1e",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Finite.lean": "968b2c58d0e77e91c69815bf1ed5e3fafa7302eaebc08139d9fdbb323ad910e8",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/AdjMatrix.lean": "03a9e47e105ca413481cbca85c5e575bb1aac0077d7671c2bb7fa044b6572292",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/LapMatrix.lean": "8a8ca58ac3a8c808973531ce8bff0610b4552a07dbfca0f74d2e5e92efa88612",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--worker-packet", type=Path)
args = parser.parse_args()

target_manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
target = next(item for item in target_manifest["targets"] if item["theorem_id"] == "THM-M-0881")
execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
authority_item = next(item for item in execution_dag["items"] if item["id"] == "S56-M-0881-INTAKE")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

assert target["execution_rank"] == instance["execution_rank"] == 1035
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["intake_score"] == instance["intake_score"] == 96
assert target["target_lane"] == instance["target_lane"]
assert target["name"] == instance["name_zh"] == "扩展图"
assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is instance["theorem_complete"] is False

assert authority_item["theorem_id"] == "THM-M-0881"
assert authority_item["phase"] == "intake"
assert authority_item["depends_on"] == []
assert authority_item["owned_paths"] == ["Stage1_Instances/THM-M-0881"]
assert authority_item["state"] in {"[ ]", "[_]"}
if args.worker_packet is not None:
    assert authority_item["state"] == "[ ]"

assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-0881"
assert instance["item_id"] == receipt["item_id"] == "S56-M-0881-INTAKE"
assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
formal_target = instance["canonical_formal_target"]
assert formal_target["module"] is None
assert formal_target["declaration_or_expression"] is None
assert formal_target["elaborated_expression_hash"] is None
assert formal_target["environment_fingerprint"] is None
assert instance["ordered_binders"] == instance["quantifiers"] == instance["hypotheses"] == []
assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert dag["audit_complete"] is dag["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-0881-STATEMENT", ["S56-M-0881-INTAKE"]),
    ("S56-M-0881-ANCHOR_AUDIT", ["S56-M-0881-STATEMENT"]),
    ("S56-M-0881-OBLIGATION_TREE", ["S56-M-0881-ANCHOR_AUDIT"]),
    ("S56-M-0881-PROOF", ["S56-M-0881-OBLIGATION_TREE"]),
    ("S56-M-0881-VALIDATION", ["S56-M-0881-PROOF"]),
    ("S56-M-0881-RELEASE", ["S56-M-0881-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

expected_files = sorted(instance["owned_artifacts"])
owned_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
assert owned_files == expected_files
hashed_files = [name for name in owned_files if name != "intake-receipt.json"]
assert sorted(receipt["untracked_owned_artifact_sha256"]) == sorted(hashed_files)
for name in hashed_files:
    assert receipt["untracked_owned_artifact_sha256"][name] == digest(OWNED / name), (
        f"owned artifact hash mismatch: {name}"
    )
for path in OWNED.iterdir():
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

source_revisions = instance["source_revisions"]
assert source_revisions["repository_base"] == receipt["base_revision"] == BASE
assert source_revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
assert source_revisions["mathlib"] == MATHLIB
assert source_revisions["lean_toolchain_file_sha256"] == LEAN_TOOLCHAIN_SHA256
assert source_revisions["lake_manifest_sha256"] == LAKE_MANIFEST_SHA256
assert digest(ROOT / "Formalizations/Lean/lean-toolchain") == LEAN_TOOLCHAIN_SHA256
assert digest(ROOT / "Formalizations/Lean/lake-manifest.json") == LAKE_MANIFEST_SHA256
source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(
    keepends=True
)
source_excerpt = "".join(source_lines[6452:6458]).encode("utf-8")
assert hashlib.sha256(source_excerpt).hexdigest() == TARGET_EXCERPT_SHA256
assert source_revisions["repository_record_excerpt_sha256"] == TARGET_EXCERPT_SHA256

assert receipt["receipt_class"] == "provisional_worker_selftest"
assert receipt["verdict"] == "no_state_change"
assert receipt["verdict_boundary"]
assert receipt["proposed_state"] == "[_]"
assert receipt["accepted"] is receipt["content_addressed"] is False
assert receipt["root_vector_before"] == {
    "H": "unclassified",
    "M": "unclassified",
    "R": "unclassified",
}
assert receipt["root_vector_after"] == instance["root_vector"]
assert receipt["audit_complete"] is receipt["theorem_complete"] is False
assert receipt["accepted_receipt_ids"] == receipt["statement_fingerprints"] == []
assert receipt["canonical_obligation_ids"] == receipt["typed_graph_changes"] == []
assert receipt["composition_certificates"] == receipt["content_addressed_recipe_ids"] == []
assert receipt["content_addressed_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["change_impact_set"] == ["S56-M-0881-INTAKE"]
assert receipt["remaining_root_cut_set"] == [task_id for task_id, _ in expected_tasks]
assert receipt["selftest_result"] == "pass"
assert receipt["covered_node_ids"] == ["S56-M-0881-INTAKE"]
assert receipt["covered_declarations"] == receipt["covered_expression_fingerprints"] == []
assert receipt["validation_started_at"] and receipt["validation_ended_at"]
assert receipt["debt_vector_basis"] and receipt["ownership_and_change_impact"]
assert receipt["first_failed_gate"] == "master_acceptance_of_node_specific_intake_receipt"
assert receipt["first_failed_theorem_gate"].startswith("S56-M-0881-STATEMENT:")
assert receipt["reviewer_policy"] and receipt["support_window"]
assert receipt["archive_and_recovery_boundary"] and receipt["execution_time_boundary"]
assert receipt["dirty_input_evidence"]["tracked_binary_diff_sha256"] == hashlib.sha256(b"").hexdigest()
assert receipt["dirty_input_evidence"]["initial_git_status_stdout_sha256"] == (
    "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
)
assert receipt["dirty_input_evidence"]["final_changed_path_manifest_sha256"] == (
    "e654a2d1bf6d98322695dab0f46d2e7e605df4a8ced1e45cba05cac074a420f4"
)
assert len(receipt["structured_validation_recipes"]) == 2
expected_recipe_hashes = {
    "S56-M-0881-INTAKE-RECIPE-STRUCTURE": (
        "441b330f17352c917507fee1b288da38384d3c41d0a3d42fd4d04f1472631656"
    ),
    "S56-M-0881-INTAKE-RECIPE-LEAN-PROBE": (
        "289b8e2bd11a3f2240ce5f7115f847e6ecd6cbd3a1b310df11b347950377eb5b"
    ),
}
for recipe in receipt["structured_validation_recipes"]:
    assert recipe["recipe_id"] in expected_recipe_hashes
    assert recipe["exit_code"] == recipe["expected_exit"] == 0
    assert recipe["stdout_sha256"] == expected_recipe_hashes[recipe["recipe_id"]]
    assert recipe["stderr_sha256"] == hashlib.sha256(b"").hexdigest()
    assert recipe["execution_started_at"] and recipe["execution_ended_at"]
    assert recipe["covered_ids"] == ["S56-M-0881-INTAKE"]
    assert recipe["covered_obligation_ids"] == recipe["covered_declarations"] == []

if args.worker_packet is not None:
    packet_path = args.worker_packet if args.worker_packet.is_absolute() else ROOT / args.worker_packet
    packet = load(packet_path)
    assert packet["item_id"] == "S56-M-0881-INTAKE"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE
    assert packet["commands"] and packet["known_failures"] and packet["output_summary"]
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/THM-M-0881/{name}" for name in owned_files
    }
    assert set(packet["changed_paths"]) == expected_changed
    assert set(receipt["changed_paths"]) == expected_changed
    for relative, expected_digest in WORKER_SOURCE_HASHES.items():
        assert digest(ROOT / relative) == expected_digest, f"worker source drift: {relative}"
    assert receipt["source_inputs"] == {
        relative: f"sha256:{expected_digest}"
        for relative, expected_digest in WORKER_SOURCE_HASHES.items()
        if relative
        in {
            "Docs/Stage1_Targets_rev-5.6.json",
            "Docs/Stage1_Blueprint_Applicable_Theorems.md",
            "Docs/Stage1_Blueprint_rev-5.6.md",
            "Docs/Stage1_Execution_DAG_rev-5.6.json",
            "skills/execute-stage1-rev56/SKILL.md",
            "Docs/Blueprint_Guidelines.md",
            "Docs/researches/math_theorems.md",
            "Docs/Stage0_Blueprint.md",
            "Formalizations/Lean/lean-toolchain",
            "Formalizations/Lean/lake-manifest.json",
        }
    }

print("intake invariant check: ok (THM-M-0881 planned; H5/M4/R4; six open tasks)")
