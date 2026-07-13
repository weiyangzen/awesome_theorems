#!/usr/bin/env python3
"""Validate the fail-closed THM-M-1490 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1490"
ITEM_ID = "S56-M-1490-INTAKE"
RANK = 1167
BASE_REVISION = "04d551db74b7e1d7d9d261bba4727b3daf8a70d5"
BASE_TREE = "ee8a3d7a6c48598ca61028d71e21e0802ed968e1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "mathlib_extrema_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Convex/Extrema.lean"
    ),
    "mathlib_compact_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Order/Compact.lean"
    ),
    "mathlib_convex_function_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Convex/Function.lean"
    ),
}
EXPECTED_NEIGHBORS = {
    "THM-M-1491": "凸优化",
    "THM-M-1492": "线性规划",
    "THM-M-1493": "单纯形法",
    "THM-M-1494": "内点法",
    "THM-M-1495": "椭球法",
    "THM-M-1496": "半定规划",
    "THM-M-1497": "锥规划",
    "THM-M-1498": "梯度下降法",
    "THM-M-1499": "随机梯度下降",
    "THM-M-1500": "牛顿法(优化)",
    "THM-M-1501": "拟牛顿法",
    "THM-M-1502": "BFGS算法",
    "THM-M-1503": "共轭梯度法(优化)",
    "THM-M-1504": "信赖域方法",
    "THM-M-1505": "Levenberg-Marquardt算法",
    "THM-M-1506": "KKT条件",
    "THM-M-1507": "拉格朗日对偶",
    "THM-M-1508": "鞍点定理",
    "THM-M-1509": "von Neumann极小极大定理",
}
EXPECTED_RECEIPT_KEYS = {
    "schema_version",
    "receipt_id",
    "item_id",
    "theorem_id",
    "phase",
    "intent",
    "verdict",
    "proposed_state",
    "accepted",
    "acceptance_authority",
    "receipt_class",
    "content_addressed",
    "content_addressing_boundary",
    "base_revision",
    "base_tree",
    "worker_branch_or_worktree",
    "worktree_state",
    "preexisting_untracked_paths",
    "attestor",
    "platform",
    "source_inputs",
    "source_evidence",
    "worker_input_hashes",
    "validated_scope",
    "changed_paths",
    "diff_summary",
    "exact_statement_change",
    "source_revision_and_proof_body_summary",
    "structured_validation_recipes",
    "commands_and_exit_codes",
    "worker_packet_commands",
    "output_summary",
    "root_vector_before",
    "root_vector_after",
    "debt_vector_delta",
    "debt_delta_basis",
    "axiom_and_placeholder_result",
    "actual_source_ownership",
    "declaration_ownership",
    "readable_ownership",
    "change_impact_set",
    "covered_node_ids",
    "accepted_receipt_ids",
    "proof_body_locations",
    "canonical_obligation_ids",
    "statement_fingerprints",
    "typed_graph_changes",
    "composition_certificates",
    "content_addressed_recipe_ids",
    "content_addressed_receipt_ids",
    "non_self_referential_owned_artifact_sha256",
    "owner",
    "reviewer_policy",
    "validation_time_boundary",
    "review_due",
    "support_state",
    "invalidation_inputs",
    "incident_path",
    "audit_complete",
    "theorem_complete",
    "first_failed_gate",
    "retry_condition",
    "remaining_root_cut_set",
    "known_failures",
    "selftest_result",
    "status_boundary",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_json_line_sha256(value: object) -> str:
    data = (
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def line_slice_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


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
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    worker_packet_path = (
        args.worker_packet.resolve()
        if args.worker_packet is not None
        else ROOT / ".stage1-worker-selftest.json"
    )

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    assert set(receipt) == EXPECTED_RECEIPT_KEYS

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "优化理论"
    assert target["category"] == instance["category"] == "其他重要领域 / 数值分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
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
    required_instance_fields = {
        "schema_version",
        "lifecycle_mode",
        "theorem_id",
        "canonical_name",
        "canonical_statement",
        "canonical_formal_target",
        "domain_and_universes",
        "quantifiers",
        "hypotheses",
        "conclusion",
        "alternate_encodings",
        "excluded_degenerate_cases",
        "foundation_profile",
        "tcb_profile",
        "computation_profile",
        "formal_system",
        "source_revisions",
        "obligation_registry_hash",
        "discovery_protocol_hash",
        "authoritative_blueprint",
        "public_merge_targets",
        "owners_and_reviewers",
        "freshness_and_revocation_policy",
    }
    assert required_instance_fields <= set(instance)
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "数学优化的理论"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    assert "does_not_select_one_exact_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["authoritative_blueprint"] == "Docs/Stage1_Blueprint_rev-5.6.md"
    assert instance["owners_and_reviewers"]["owner"] == "Stage1 integration lane"
    assert instance["owners_and_reviewers"]["required_reviewers"]
    assert instance["freshness_and_revocation_policy"]["invalidation_inputs"]
    assert instance["freshness_and_revocation_policy"]["incident_path"]
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    source_commit = revisions["repository_source_record_commit"]
    assert git("rev-parse", f"{source_commit}:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob"]
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib worktree is dirty"
    assert revisions["canonical_manifest_entry_sha256"] == compact_json_line_sha256(target)
    assert revisions["repository_record_excerpt_sha256"] == line_slice_sha256(
        ROOT / "Docs/researches/math_theorems.md", 10889, 10894
    )
    assert revisions["stage0_projection_excerpt_sha256"] == line_slice_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 40513, 40538
    )
    assert revisions["neighbor_catalog_excerpt_sha256"] == line_slice_sha256(
        ROOT / "Docs/researches/math_theorems.md", 10889, 10943
    )
    assert revisions["intake_dag_entry_sha256"] == line_slice_sha256(
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json", 144596, 144611
    )

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-1490-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**优化理论**") == 1
    assert "- 提出者: 众多数学家" in catalog and "- 时间: 20世纪" in catalog
    assert catalog.count("- 陈述: 数学优化的理论") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1490 优化理论" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in EXPECTED_NEIGHBORS
    }
    assert manifest_names == EXPECTED_NEIGHBORS
    instance_neighbors = {
        row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]
    }
    assert instance_neighbors == EXPECTED_NEIGHBORS

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-1490-INTAKE-WORKER-20260713"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "rev-5.6 integration lane"
    assert receipt["worker_branch_or_worktree"].endswith("worker slot7")
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["source_evidence"]["repository_source_record_commit"] == revisions[
        "repository_source_record_commit"
    ]
    assert receipt["source_evidence"]["repository_source_record_blob"] == revisions[
        "repository_source_record_blob"
    ]
    assert receipt["source_evidence"]["repository_record_excerpt_sha256"] == revisions[
        "repository_record_excerpt_sha256"
    ]
    assert receipt["source_evidence"]["stage0_projection_excerpt_sha256"] == revisions[
        "stage0_projection_excerpt_sha256"
    ]
    assert receipt["source_evidence"]["proof_body_locations"] == []
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    for field in (
        "mathlib_extrema_source_sha256",
        "mathlib_compact_source_sha256",
        "mathlib_convex_function_source_sha256",
    ):
        assert worker_inputs[field] == revisions[field]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}"
    recipes = receipt["structured_validation_recipes"]
    assert [recipe["recipe_id"] for recipe in recipes] == [
        "S56-M-1490-INTAKE-RECIPE-STRUCTURE",
        "S56-M-1490-INTAKE-RECIPE-LEAN-PROBE",
    ]
    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
        "covered_node_ids",
    }
    for recipe in recipes:
        assert set(recipe) == required_recipe_keys
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_node_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == recipe["covered_declarations"] == []
    structure_recipe, lean_recipe = recipes
    assert structure_recipe["cwd"] == "."
    assert structure_recipe["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    expected_structure_line = (
        f"intake invariant check: ok ({THEOREM_ID} planned; "
        "H5/M4/R4; six open tasks)"
    )
    assert structure_recipe["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": f"exact UTF-8 line: {expected_structure_line}",
    }]
    if args.worker_packet is not None:
        public_replay = subprocess.run(
            [
                argument
                for argument in structure_recipe["argv"]
                if argument not in ("--worker-packet", ".stage1-worker-selftest.json")
            ],
            cwd=ROOT / structure_recipe["cwd"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=structure_recipe["timeout_seconds"],
            check=False,
        )
        assert public_replay.returncode == structure_recipe["expected_exit"]
        assert public_replay.stdout == (expected_structure_line + "\n").encode()
    assert lean_recipe["cwd"] == "Formalizations/Lean"
    lean_result = subprocess.run(
        lean_recipe["argv"],
        cwd=ROOT / lean_recipe["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=lean_recipe["timeout_seconds"],
        check=False,
    )
    assert lean_result.returncode == lean_recipe["expected_exit"]
    lean_output = lean_result.stdout
    expected_lean_hash = lean_recipe["expected_outputs"][0]["semantic_hash_policy"]
    assert expected_lean_hash == f"sha256:{hashlib.sha256(lean_output).hexdigest()}"
    for declaration in (
        "IsCompact.exists_isMinOn",
        "IsMinOn.of_isLocalMinOn_of_convexOn",
        "StrictConvexOn.eq_of_isMinOn",
    ):
        assert (
            f"'{declaration}' depends on axioms: "
            "[propext, Classical.choice, Quot.sound]"
        ).encode() in lean_output

    command_ledger = receipt["commands_and_exit_codes"]
    assert all(
        set(row) in ({"command", "exit_code"}, {"command", "exit_code", "expected_no_match"})
        for row in command_ledger
    )
    ledger_commands = {row["command"] for row in command_ledger}
    assert set(receipt["worker_packet_commands"]) <= ledger_commands
    assert all(
        row["exit_code"] == 0 or row.get("expected_no_match") is True
        for row in command_ledger
    )
    assert receipt["change_impact_set"] == receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert set(receipt["readable_ownership"]) == {
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
    }
    assert "No exact mathematical or Lean statement was added" in receipt[
        "exact_statement_change"
    ]
    assert "no Lean proof body is credited" in receipt[
        "source_revision_and_proof_body_summary"
    ]
    assert "canonical source-statement identity" in receipt["first_failed_gate"]
    assert receipt["retry_condition"] and receipt["known_failures"]
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["review_due"] == "before master acceptance or any dependent statement work"
    assert "provisional intake only" in receipt["support_state"]
    assert receipt["invalidation_inputs"] and receipt["incident_path"]

    artifact_hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed_paths = {
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in OWNED_FILES - {"intake-receipt.json"}
    }
    assert set(artifact_hashes) == expected_hashed_paths
    for relative, digest in artifact_hashes.items():
        assert digest == sha256(ROOT / relative), f"stale owned artifact hash: {relative}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    tracked_changes = set(git("diff", "--name-only", "HEAD").splitlines())
    untracked_changes = set(
        git("ls-files", "--others", "--exclude-standard").splitlines()
    )
    preexisting = set(receipt["preexisting_untracked_paths"])
    actual_scoped_changes = (tracked_changes | untracked_changes) - preexisting
    assert actual_scoped_changes == expected_changed
    assert all(
        path == ".stage1-worker-selftest.json"
        or path.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        for path in actual_scoped_changes
    )

    check_worker_packet(worker_packet_path, receipt)

    print("intake invariant check: ok (THM-M-1490 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
