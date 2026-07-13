#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0880."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0880"
ITEM_ID = "S56-M-0880-INTAKE"
RANK = 1433
BASE_REVISION = "0c019b7194c9c43fa5f683fa82d637a0b275410d"
BASE_TREE = "43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
MATH_SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
CS_SOURCE_BLOB = "0a87065663fa7966305127495f50a61c22e57066"
MATH_EXCERPT_SHA256 = "939df09c1fb30cae7d6a1b9cd250121a34904cbeed7bb56a3f81e92127c58cc5"
STAGE0_EXCERPT_SHA256 = "34bac9c24e00ecc30312b01e5e51affea64e3a7791d9afa75fa6e0bc555efb42"
CS_EXCERPT_SHA256 = "f23cdc0da380947cd7a76e70df72f28abf15ca4518da44eb23ca2092fc0e931d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_PROBE_OUTPUT_SHA256 = "8dd72c17e1d4db682d5bb25c66cacfd7c14a572537281f18f463196727109f5f"
OWNED_FILES = {
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASHES = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "applicable_targets_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "repository_cs_source_sha256": "Docs/researches/cs_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_HASHES = {
    "simplegraph_basic_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Basic.lean",
        "ae6fd7c95ad151f84eb316d32c518485e9877bdda0d9eb6b4aac9e041676ad1e",
    ),
    "simplegraph_density_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Density.lean",
        "28663cc7ac347f5f419f0bf41086c595f3f2fa30c861eb5741bcf71bdff2ad90",
    ),
    "simplegraph_finite_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Finite.lean",
        "968b2c58d0e77e91c69815bf1ed5e3fafa7302eaebc08139d9fdbb323ad910e8",
    ),
    "simplegraph_edge_connectivity_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Connectivity/EdgeConnectivity.lean",
        "7b4d638ae2e98b8131a3d4eccc53f3e52afab999d39895c5d21bd23b49db06b2",
    ),
    "simplegraph_partition_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Partition.lean",
        "3c454db614087593dc9dd2809af3ce47aa01687dfcce4fc0ea4058e786b29c68",
    ),
}


def load(path: Path) -> dict:
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode("utf-8")).hexdigest()


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    data = path.resolve().read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "稀疏割"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "do_not_determine_one_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["root_vector_status"] == "proposed_pending_master_acceptance"
    assert instance["foundation_profile"].startswith("provisional-foundation-profile/1.0:")
    assert instance["tcb_profile"].startswith("provisional-tcb-profile/1.0:")
    assert instance["computation_profile"].startswith("provisional-computation-profile/1.0:")
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == MATH_SOURCE_BLOB
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/cs_theorems.md") == CS_SOURCE_BLOB
    assert revisions["repository_math_source_record_blob"] == MATH_SOURCE_BLOB
    assert revisions["repository_cs_source_record_blob"] == CS_SOURCE_BLOB
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/researches/cs_theorems.md") == revisions["current_repository_cs_source_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{revisions[field]}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6446, 6451) == MATH_EXCERPT_SHA256
    assert revisions["repository_record_excerpt_sha256"] == MATH_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 24008, 24033) == STAGE0_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/researches/cs_theorems.md", 138, 138) == CS_EXCERPT_SHA256
    assert revisions["cross_catalog_record_excerpt_sha256"] == CS_EXCERPT_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, (relative, digest) in MATHLIB_SOURCE_HASHES.items():
        assert sha256(mathlib / relative) == revisions[field] == digest
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    assert worker_inputs["lean_toolchain"] == f'sha256:{revisions["lean_toolchain_file_sha256"]}'
    assert worker_inputs["lake_manifest"] == f'sha256:{revisions["lake_manifest_sha256"]}'
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix()
    assert worker_inputs["lake_symlink_target_string"] == (
        "sha256:" + hashlib.sha256(lake_target.encode()).hexdigest()
    )

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0880-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency], layer))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**稀疏割**") == 1
    assert "- 陈述: 图划分的稀疏性" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0880 稀疏割" in stage0
    cs_catalog = (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert cs_catalog.count("**Arora-Rao-Vazirani定理**") == 1
    assert "稀疏割的O(√log n)近似" in cs_catalog

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {
        "THM-M-0814",
        "THM-M-0831",
        "THM-M-0832",
        "THM-M-0877",
        "THM-M-0878",
        "THM-M-0879",
        "THM-M-0881",
        "THM-M-0887",
        "THM-M-0888",
    }
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0814": "最大流最小割定理",
        "THM-M-0831": "Karger算法",
        "THM-M-0832": "Stoer-Wagner算法",
        "THM-M-0877": "网络流",
        "THM-M-0878": "最小费用流",
        "THM-M-0879": "多商品流",
        "THM-M-0881": "扩展图",
        "THM-M-0887": "谱图理论",
        "THM-M-0888": "Cheeger不等式",
    }
    cross_catalog = instance["cross_catalog_boundaries"]
    assert len(cross_catalog) == 1 and cross_catalog[0]["theorem_id"] == "THM-C-0077"
    assert "THM-C-0077 Arora-Rao-Vazirani定理" in stage0
    assert "THM-C-0077" not in {row["theorem_id"] for row in manifest["targets"]}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["phase"] == "intake"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "Stage1 integration lane"
    assert receipt["first_failed_intake_gate"].startswith("independent integration-lane review")
    assert receipt["first_failed_theorem_gate"].startswith("S56-M-0880-STATEMENT:")
    assert receipt["known_failures"]
    assert receipt["source_evidence"]["proof_body_locations"] == []
    assert receipt["declaration_ownership"] == []
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    recipes = receipt["structured_validation_recipes"]
    assert [recipe["recipe_id"] for recipe in recipes] == [
        "S56-M-0880-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0880-INTAKE-RECIPE-LEAN-PROBE",
    ]
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    lean_output = run_recorded_action(recipes[1])
    assert hashlib.sha256(lean_output).hexdigest() == receipt["lean_probe_output_sha256"] == LEAN_PROBE_OUTPUT_SHA256

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0880 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
