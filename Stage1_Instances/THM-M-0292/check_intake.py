#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0292 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0292"
ITEM_ID = "S56-M-0292-INTAKE"
RANK = 1542
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB_AT_ORIGIN = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_DINI_BLOB = "34c07a3509d4fb6e6b26e2b5f718ccdf57709ecf"
MATHLIB_DINI_SHA256 = "d671cee68ea4d518e5260ae2faa98faf05c6e84a32ab4e7a1c8b9b2882b7dfab"
MANIFEST_ENTRY_SHA256 = "269cfa72d7ed21950b9774eaeaa2d34767f8dfe32e1b635a0324c8547e19185e"
DAG_TARGET_ENTRIES_SHA256 = "90c059246feb11c7eebf3b19cc6e0387272c55b254f2a96169119f68c6b5c27c"
CATALOG_EXCERPT_SHA256 = "e2fd9aad0de299287ad70bd369073c14bc4038a5df0a59f2b470f22922f97594"
STAGE0_EXCERPT_SHA256 = "1afc61a6f54137fab91896c2ce28ed50199e43c33a9441c624c5ec00092cbd0d"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
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
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "mathlib_dini_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/UniformSpace/Dini.lean"
    ),
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
RECIPE_FIELDS = {
    "recipe_id",
    "cwd",
    "argv",
    "env_allowlist",
    "timeout_seconds",
    "network_policy",
    "expected_exit",
    "expected_outputs",
    "covered_workflow_item_ids",
    "covered_obligation_ids",
    "covered_declarations",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def canonical_hash(value: object) -> str:
    payload = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(payload).hexdigest()


def check_worker_packet(path: Path, receipt: dict, expected_changed: set[str]) -> None:
    packet = load(path)
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == expected_changed
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["worker_packet_output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_recorded_commands(receipt: dict) -> None:
    commands = receipt["commands_and_results"]
    assert isinstance(commands, list) and commands
    for command in commands:
        assert "command" not in command
        assert isinstance(command.get("argv"), list) and all(
            isinstance(part, str) and part for part in command["argv"]
        )
        assert isinstance(command.get("exit_code"), int)
        assert isinstance(command.get("result"), str) and command["result"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "迪尼定理",
            "category": "分析学 / 实分析",
            "source_status_untrusted": "已验证",
            "baseline": "L0",
            "rework_required": True,
            "legacy_artifacts_accepted": False,
            "target_lane": "hard_statement_first_partial_verification",
            "intake_score": 78,
            "lifecycle_mode": "planned",
            "theorem_complete": False,
        }
    ]
    target = matches[0]
    assert canonical_hash(target) == MANIFEST_ENTRY_SHA256
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "迪尼定理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 78
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    target_items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    if args.worker_packet:
        assert canonical_hash(target_items) == DAG_TARGET_ENTRIES_SHA256
    item = target_items[0]
    assert item["id"] == ITEM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]", "[x]"}
    if args.worker_packet:
        assert item["state"] == "[ ]" and item["attempts"] == 0
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert item["depends_on"] == [] and item["children"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["receipt_id"] == "S56-M-0292-INTAKE-WORKER-20260713"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert receipt["phase"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "exact_source_theorem" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["module_candidate"] == "Mathlib.Topology.UniformSpace.Dini"
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["source_revisions"]["dini_bsb_iiif_manifest_observed_sha256"] == (
        "59352baea3cda1039d6c97837268a2c88b36102a2d8f7238db884b6834389be5"
    )
    assert instance["source_revisions"]["eom_dini_api_response_observed_sha256"] == (
        "706d060dada3be39e47308589c7cc9b8b0b7e4f1eb07a7f3ef62d81f11f936f7"
    )
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob_at_base"]
    assert git("rev-parse", f"{BASE_REVISION}:Docs/Stage0_Blueprint.md") == revisions["stage0_projection_blob_at_base"]
    assert (
        git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md")
        == revisions["repository_source_record_blob_at_origin"]
        == SOURCE_RECORD_BLOB_AT_ORIGIN
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        if args.worker_packet or field not in {
            "authoritative_blueprint_sha256",
            "execution_dag_sha256",
        }:
            assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    if args.worker_packet:
        assert revisions["manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256
        assert revisions["execution_dag_target_entries_sha256"] == DAG_TARGET_ENTRIES_SHA256
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 2097, 2102
    ) == CATALOG_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 8062, 8087
    ) == STAGE0_EXCERPT_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    dini_path = mathlib / "Mathlib/Topology/UniformSpace/Dini.lean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert git("hash-object", "Mathlib/Topology/UniformSpace/Dini.lean", cwd=mathlib) == (
        revisions["mathlib_dini_blob"]
    ) == MATHLIB_DINI_BLOB
    assert sha256(dini_path) == revisions["mathlib_dini_source_sha256"] == MATHLIB_DINI_SHA256

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0292-{suffix}"
        authoritative = next(row for row in target_items if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        expected_tasks.append((task_id, [dependency], "open"))
        dependency = task_id
    assert [(row["id"], row["depends_on"], row["state"]) for row in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**迪尼定理**") == 1
    assert catalog.count("- 陈述: 单调函数列的一致收敛") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert stage0.count("THM-M-0292 迪尼定理") == 1
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0
    assert instance["duplicate_search_boundary"]["result"].startswith("one repository")
    assert instance["neighbor_target_boundaries"] == [
        {
            "theorem_id": "THM-M-0291",
            "name": "费耶尔定理",
            "relationship": "adjacent uniform-convergence result for Fourier-Cesaro means; not the Dini monotone-sequence theorem",
        }
    ]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    receipt_path = f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == expected_changed
    dirty = receipt["dirty_input_evidence"]
    assert dirty["preflight_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert set(dirty["owned_untracked_paths"]) == expected_changed
    expected_dirty_hashes = expected_changed - {receipt_path}
    assert set(dirty["untracked_input_hashes"]) == expected_dirty_hashes
    if args.worker_packet:
        for relative, tagged in dirty["untracked_input_hashes"].items():
            assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale dirty hash: {relative}"
        actual_untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
        assert actual_untracked == expected_changed | {"Formalizations/Lean/.lake"}

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["proof_body_locations"] == receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["covered_node_ids"] == [ITEM_ID]
    check_recorded_commands(receipt)
    assert receipt["remaining_root_cut_set"] == [row["id"] for row in dag["tasks"]]
    expected_hashed = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["owned_artifact_hashes"]) == expected_hashed
    assert "intake-receipt.json" in receipt["self_reference_boundary"]
    for name, tagged in receipt["owned_artifact_hashes"].items():
        assert tagged == f"sha256:{sha256(HERE / name)}", f"stale owned hash: {name}"
    assert receipt["acceptance_authority"] == "rev-5.6 integration lane"
    assert receipt["validation_started_at"] <= receipt["validation_ended_at"] == receipt["validated_at"]
    assert receipt["attestor"] == {
        "kind": "stage1_rev56_worker_selftest",
        "identity": "isolated worker for S56-M-0292-INTAKE",
        "signature": None,
        "signature_status": "unsigned_provisional_worker_evidence",
    }
    assert receipt["invalidation_inputs"] and receipt["known_failures"]
    mutable_authority_inputs = {
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    }
    for relative, tagged in receipt["source_inputs"].items():
        if args.worker_packet or relative not in mutable_authority_inputs:
            assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["repository_base_revision"] == BASE_REVISION
    assert worker_inputs["repository_base_tree"] == BASE_TREE
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    if args.worker_packet:
        lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
        assert worker_inputs["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

    recipes = receipt["structured_validation_recipes"]
    assert [row["recipe_id"] for row in recipes] == [
        "S56-M-0292-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0292-INTAKE-RECIPE-LEAN-PROBE",
    ]
    for recipe in recipes:
        assert set(recipe) == RECIPE_FIELDS
        assert recipe["argv"] and recipe["expected_outputs"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["covered_workflow_item_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert isinstance(recipe["covered_declarations"], list)
    assert recipes[0]["covered_declarations"] == []
    assert set(recipes[1]["covered_declarations"]) == {
        "Monotone.tendstoLocallyUniformly_of_forall_tendsto",
        "Monotone.tendstoUniformly_of_forall_tendsto",
        "Monotone.tendstoUniformlyOn_of_forall_tendsto",
        "Antitone.tendstoLocallyUniformly_of_forall_tendsto",
        "Antitone.tendstoUniformly_of_forall_tendsto",
        "Antitone.tendstoUniformlyOn_of_forall_tendsto",
        "ContinuousMap.tendsto_of_monotone_of_pointwise",
        "ContinuousMap.tendsto_of_antitone_of_pointwise",
    }

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert not any(token in probe for token in forbidden)

    if args.worker_packet:
        check_worker_packet(args.worker_packet.resolve(), receipt, expected_changed)

    print("THM-M-0292 intake invariant check: ok (planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
