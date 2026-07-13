#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0839."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0839"
ITEM_ID = "S56-M-0839-INTAKE"
RANK = 1396
BASE_REVISION = "be8701e88e791545c16a262edd1909486d5cef4b"
BASE_TREE = "78b0a751473bf6d71f453a6aad18b130268a3428"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
SOURCE_HASHES = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_HASHES = {
    "mathlib_coloring_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Coloring.lean",
    "mathlib_clique_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Clique.lean",
    "mathlib_basic_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Basic.lean",
    "mathlib_maps_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Maps.lean",
}
PROBED_DECLARATIONS = [
    "SimpleGraph.compl_adj",
    "SimpleGraph.induce",
    "SimpleGraph.chromaticNumber",
    "SimpleGraph.cliqueNum",
    "SimpleGraph.cliqueNum_le_chromaticNumber",
    "SimpleGraph.cliqueNum_compl",
]
TEMPORARY_SOURCE_HASHES = {
    "observed_crossref_normal_hypergraphs_sha256": "bbb49535c70e95adfa3dda60d3abf9b36bbe2d7edb023c91a30df8405ecab0eb",
    "observed_crossref_characterization_sha256": "6d6fdc00b3e4e32d52b814d34c306114dc5020a1b5039543e396bb5ed568b5cb",
    "observed_openaire_normal_hypergraphs_sha256": "1fb06a89a686b46bff7617cfce6faf5d02ddb7248a9776f90c7843e498af7221",
    "observed_openaire_characterization_sha256": "cf756d5aa8bfaea252f56abaab8174bf1787cd47874f6dddb8f95e2cb5cb4bb1",
    "observed_lovasz_publication_list_sha256": "399677d8d67733e01ac69f69d8ced789f157ad8a2a623d228645777c3c8ef082",
    "observed_coq_formalization_pdf_sha256": "a65c6f372dfe85309585752c76c8b267d7cacaf29dfaa97eff15f39176a68fbb",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    data = path.read_bytes()
    assert data.endswith(b"\n"), "worker packet is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data
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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
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
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "完美图定理"
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

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
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
    assert instance["authoritative_blueprint"] == "Docs/Stage1_Blueprint_rev-5.6.md"
    assert instance["open_task_dag"] == f"Stage1_Instances/{THEOREM_ID}/task-dag.json"
    assert "primary_sources_identified" in instance["canonical_claim_status"]

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["canonical_name"].endswith("not yet frozen)")
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert revisions["repository_source_record_commit"] == receipt["source_evidence"]["repository_source_record_commit"]
    assert revisions["repository_source_record_blob"] == receipt["source_evidence"]["repository_source_record_blob"]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{revisions[field]}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0839-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**完美图定理**") == 1
    assert "- 提出者: László Lovász" in catalog
    assert "- 时间: 1972" in catalog
    assert catalog.count("- 陈述: 图的完美性与其补图的完美性等价") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0839 完美图定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    projection = (ROOT / "Docs/Stage1_Blueprint_Applicable_Theorems.md").read_text(encoding="utf-8")
    assert "| 1396 | - | `THM-M-0839` | 完美图定理 |" in projection

    assert instance["neighbor_target_boundaries"] == [{
        "theorem_id": "THM-M-0840",
        "name": "强完美图定理",
        "relationship": "the 2006 forbidden-induced-subgraph characterization is the strong perfect graph theorem and is separately owned",
    }]
    neighbor = next(row for row in manifest["targets"] if row["theorem_id"] == "THM-M-0840")
    assert neighbor["name"] == "强完美图定理"

    sources = instance["primary_source_leads_not_credited"]
    assert [source["doi"] for source in sources] == [
        "10.1016/0012-365X(72)90006-4",
        "10.1016/0095-8956(72)90045-7",
    ]
    secondary = instance["secondary_source_and_external_formalization_leads_not_credited"]
    assert secondary[0]["observed_pdf_sha256"] == revisions["observed_coq_formalization_pdf_sha256"]
    assert secondary[1]["observed_pdf_sha256"] == revisions["observed_lovasz_publication_list_sha256"]
    for field, digest in TEMPORARY_SOURCE_HASHES.items():
        assert revisions[field] == digest

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    dirty = receipt["dirty_input_evidence"]
    assert set(dirty["owned_untracked_paths"]) == expected_changed
    expected_hashed_inputs = expected_changed - {
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    }
    assert set(dirty["untracked_input_hashes"]) == expected_hashed_inputs
    for relative, tagged_digest in dirty["untracked_input_hashes"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale untracked input hash: {relative}"
        )
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["lifecycle_before"] == "no_instance_at_L0_baseline"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    porcelain = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT
    )
    assert receipt["final_porcelain_status_sha256"] == f"sha256:{hashlib.sha256(porcelain).hexdigest()}"
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["support_state"] == "provisional_worker_only"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    for relative in expected_hashed_inputs:
        modified_at = datetime.fromtimestamp((ROOT / relative).stat().st_mtime, tz=validated_at.tzinfo)
        assert modified_at <= validated_at, f"validation timestamp predates input: {relative}"
    recipes = receipt["structured_validation_recipes"]
    actions = receipt["validation_actions"]
    assert [action["recipe_id"] for action in actions] == [
        "S56-M-0839-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0839-INTAKE-RECIPE-LEAN-PROBE",
    ]
    assert all(action["exit_code"] == 0 for action in actions)
    for recipe, action in zip(recipes, actions, strict=True):
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["covered_declarations"] == action["covered_declarations"]
        assert action["recipe_sha256"] == f"sha256:{canonical_sha256(recipe)}"
        assert action["stderr_sha256"] == f"sha256:{hashlib.sha256(b'').hexdigest()}"
        assert action["log_policy"] == "raw stdout bytes followed by raw stderr bytes"
        assert action["log_sha256"] == action["stdout_sha256"]
    assert recipes[0]["covered_declarations"] == []
    assert recipes[1]["covered_declarations"] == PROBED_DECLARATIONS
    assert actions[1]["stdout_sha256"] == (
        "sha256:305109dcab2f4d12882f073a3b7f72027f6ac511b3e86364066f763ec86f815d"
    )
    for action in actions:
        started_at = datetime.fromisoformat(action["started_at"])
        ended_at = datetime.fromisoformat(action["ended_at"])
        assert started_at <= ended_at <= validated_at
    structure_line = b"intake invariant check: ok (THM-M-0839 planned; H1/M4/R4; six open tasks)\n"
    assert actions[0]["stdout_sha256"] == f"sha256:{hashlib.sha256(structure_line).hexdigest()}"

    structure_inputs = {
        "base_revision": receipt["base_revision"],
        "base_tree": receipt["base_tree"],
        "source_inputs": receipt["source_inputs"],
        "untracked_input_hashes": dirty["untracked_input_hashes"],
    }
    assert actions[0]["input_set_sha256"] == f"sha256:{canonical_sha256(structure_inputs)}"

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    for field, relative in MATHLIB_HASHES.items():
        assert worker_inputs[field] == revisions[field] == sha256(ROOT / relative)
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    lean_inputs = {
        "probe": dirty["untracked_input_hashes"][f"Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
        "worker_input_hashes": worker_inputs,
    }
    assert actions[1]["input_set_sha256"] == f"sha256:{canonical_sha256(lean_inputs)}"

    assert receipt["readable_ownership"] == [
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
    ]
    assert receipt["first_failed_gate"].startswith(f"{ITEM_ID} master acceptance:")

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0839 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
