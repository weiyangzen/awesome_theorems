#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0060 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0060"
ITEM_ID = "S56-M-0060-INTAKE"
RANK = 1092
BASE_REVISION = "bba12d6e1323b0998c5f255e488c95ef89ab9e4c"
BASE_TREE = "aa4a56c727a0a616388e4bbdd8ceac1243c3a07d"
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
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
}
MATHLIB_HASH_FIELDS = {
    "free_module_pid_source_sha256": "Mathlib/LinearAlgebra/FreeModule/PID.lean",
    "matrix_tolin_source_sha256": "Mathlib/LinearAlgebra/Matrix/ToLin.lean",
    "module_pid_source_sha256": "Mathlib/Algebra/Module/PID.lean",
}
PROBE_DECLARATIONS = [
    "Module.Basis.SmithNormalForm",
    "Module.Basis.SmithNormalForm.bM",
    "Module.Basis.SmithNormalForm.bN",
    "Module.Basis.SmithNormalForm.f",
    "Module.Basis.SmithNormalForm.a",
    "Module.Basis.SmithNormalForm.snf",
    "Submodule.exists_smith_normal_form_of_le",
    "Submodule.smithNormalFormOfLE",
    "Submodule.smithNormalForm",
    "Matrix.toLin'",
    "LinearMap.toMatrix",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_sha256(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(
            relative.encode()
            + b"\0"
            + hashlib.sha256((ROOT / relative).read_bytes()).digest()
        )
    return digest.hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert any("python3 -m json.tool" in command for command in packet["commands"])
    assert any("sorry|admit|sorryAx" in command for command in packet["commands"])
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["worker_branch_or_worktree"] == receipt["worker_branch_or_worktree"]
    assert packet["covered_node_ids"] == receipt["covered_node_ids"] == [ITEM_ID]
    assert packet["content_addressed_recipe_ids"] == []
    assert packet["content_addressed_receipt_ids"] == []


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
    assert target["name"] == instance["name_zh"] == "史密斯标准形定理"
    assert target["category"] == instance["category"] == "代数学 / 线性代数"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

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
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "candidate_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert "interfaces_elaborated_for_discovery_only" in formal["candidate_expression_status"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    catalog_excerpt = b"\n".join((ROOT / "Docs/researches/math_theorems.md").read_bytes().splitlines()[446:452]) + b"\n"
    stage0_excerpt = b"\n".join((ROOT / "Docs/Stage0_Blueprint.md").read_bytes().splitlines()[1752:1778]) + b"\n"
    assert revisions["repository_record_excerpt_sha256"] == hashlib.sha256(catalog_excerpt).hexdigest()
    assert revisions["stage0_excerpt_sha256"] == hashlib.sha256(stage0_excerpt).hexdigest()

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0060-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
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
    assert "**史密斯标准形定理**" in catalog
    assert "- 提出者: Henry John Stephen Smith" in catalog
    assert "- 时间: 1861" in catalog
    assert "- 陈述: 整数矩阵的等价标准形" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0060 史密斯标准形定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    pid_source = (mathlib / MATHLIB_HASH_FIELDS["free_module_pid_source_sha256"]).read_text(encoding="utf-8")
    assert "structure Module.Basis.SmithNormalForm" in pid_source
    assert "theorem Submodule.exists_smith_normal_form_of_le" in pid_source
    assert "noncomputable def Submodule.smithNormalForm" in pid_source
    assert "divisibility" not in pid_source[pid_source.index("structure Module.Basis.SmithNormalForm"):pid_source.index("namespace Module.Basis.SmithNormalForm")]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    status_lines = git("status", "--short", "--untracked-files=all").splitlines()
    changed_worktree_paths = {line[3:] for line in status_lines}
    assert changed_worktree_paths == expected_changed | {"Formalizations/Lean/.lake"}
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    validation_started = datetime.fromisoformat(receipt["validation_started_at"])
    validation_ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert validation_started <= validation_ended == validated_at
    assert receipt["worker_branch_or_worktree"].startswith("detached Stage1 rev-5.6 automation worker")
    assert receipt["covered_node_ids"] == receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"]
    assert receipt["declaration_ownership"] == []
    assert set(receipt["readable_ownership"]) == {
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
    }
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []

    expected_hashed = expected_changed - {f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"}
    dirty = receipt["dirty_input_evidence"]
    assert set(dirty["untracked_input_hashes"]) == expected_hashed
    for relative, tagged_digest in dirty["untracked_input_hashes"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale dirty input: {relative}"
    assert receipt["nonreceipt_dirty_input_manifest_sha256"] == path_manifest_sha256(sorted(expected_hashed))
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain_file_sha256"] == revisions["lean_toolchain_file_sha256"]
    assert worker_inputs["lake_manifest_sha256"] == revisions["lake_manifest_sha256"]
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    for field in MATHLIB_HASH_FIELDS:
        assert worker_inputs[field] == revisions[field]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

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
    }
    recipes = {row["recipe_id"]: row for row in receipt["structured_validation_recipes"]}
    actions = {row["recipe_id"]: row for row in receipt["validation_actions"]}
    assert set(recipes) == set(actions) == {
        "S56-M-0060-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0060-INTAKE-RECIPE-LEAN-PROBE",
    }
    for recipe in recipes.values():
        assert set(recipe) == required_recipe_keys
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
        assert all(set(output) == {"path_or_stream", "semantic_hash_policy"} for output in recipe["expected_outputs"])
        action = actions[recipe["recipe_id"]]
        assert action["recipe_sha256"] == canonical_json_sha256(recipe)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        assert action["covered_declarations"] == recipe["covered_declarations"]
        assert len(action["stdout_sha256"]) == len(action["log_sha256"]) == 64
        assert validation_started <= datetime.fromisoformat(action["started_at"])
        assert datetime.fromisoformat(action["started_at"]) <= datetime.fromisoformat(action["ended_at"])
        assert datetime.fromisoformat(action["ended_at"]) <= validation_ended
    structure_id = "S56-M-0060-INTAKE-RECIPE-STRUCTURE"
    lean_id = "S56-M-0060-INTAKE-RECIPE-LEAN-PROBE"
    assert recipes[structure_id]["covered_declarations"] == []
    assert recipes[lean_id]["covered_declarations"] == PROBE_DECLARATIONS
    assert actions[structure_id]["input_manifest_sha256"] == path_manifest_sha256([
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        f"Stage1_Instances/{THEOREM_ID}/instance.json",
        f"Stage1_Instances/{THEOREM_ID}/task-dag.json",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
    ])
    assert actions[lean_id]["input_manifest_sha256"] == path_manifest_sha256([
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/LinearAlgebra/FreeModule/PID.lean",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/LinearAlgebra/Matrix/ToLin.lean",
        f"Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean",
    ])
    expected_structure_output = b"intake invariant check: ok (THM-M-0060 planned; H1/M3/R4; six open tasks)\n"
    assert actions[structure_id]["stdout_sha256"] == hashlib.sha256(expected_structure_output).hexdigest()
    probe_result = subprocess.run(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        check=False,
        capture_output=True,
    )
    if probe_result.returncode != 0:
        sys.stderr.buffer.write(probe_result.stdout + probe_result.stderr)
    assert probe_result.returncode == 0
    probe_output = probe_result.stdout + probe_result.stderr
    assert actions[lean_id]["stdout_sha256"] == hashlib.sha256(probe_output).hexdigest()

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
    assert "#check @Submodule.exists_smith_normal_form_of_le" in probe
    assert "#print axioms Submodule.exists_smith_normal_form_of_le" in probe

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0060 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
