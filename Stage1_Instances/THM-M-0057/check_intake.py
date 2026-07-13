#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0057 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0057"
ITEM_ID = "S56-M-0057-INTAKE"
RANK = 1524
BASE_REVISION = "c79ae75db8880483f10bba17c9bc9dd91a9febcf"
BASE_TREE = "375fa18a4f8afa63bb51d8b05fb4c804f3bb1240"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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
    "star_normal_source_sha256": "Mathlib/Algebra/Star/SelfAdjoint.lean",
    "matrix_normed_source_sha256": "Mathlib/Analysis/Matrix/Normed.lean",
    "matrix_spectrum_source_sha256": "Mathlib/Analysis/Matrix/Spectrum.lean",
    "eigenspace_matrix_source_sha256": "Mathlib/LinearAlgebra/Eigenspace/Matrix.lean",
}


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


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda value: value.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("check_intake.py requires Python assertions; optimized mode is rejected")

    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument(
        "--skip-replay",
        action="store_true",
        help="validate static receipt structure without rerunning the Lean probe",
    )
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    assert manifest["schema_version"] == "stage1-target-set/5.6.2"
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "霍夫曼-魏兰德特定理",
            "category": "代数学 / 线性代数",
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
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]

    intake = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": RANK,
        "phase": "intake",
        "layer": 0,
        "state": "[ ]",
        "depends_on": [],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
        "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "general_normal_eigenvalue_enumeration" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0057-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    authoritative = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(authoritative) == 7
    for task, source in zip(dag["tasks"], authoritative[1:], strict=True):
        for field in ("id", "phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == source[field]
        assert task["depends_on"] == source["depends_on"] and source["state"] == "[ ]"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**霍夫曼-魏兰德特定理**") == 1
    assert "- 提出者: A.J. Hoffman/H.W. Wielandt" in catalog
    assert "- 时间: 1953" in catalog
    assert catalog.count("- 陈述: 正规矩阵特征值的扰动") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0057 霍夫曼-魏兰德特定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for needle in (
        "10.1215/S0012-7094-53-02004-3",
        "1612.05759v2",
        revisions["inspected_xu_zhang_pdf_sha256"],
        "provisional `H1`, not `H0`",
    ):
        assert needle in crosswalk
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0055",
        "THM-M-0056",
        "THM-M-0058",
        "THM-M-0059",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(actual_files)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(receipt["owned_artifact_sha256"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["selftest_result"] == "pass"
    for field in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[field] == []
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert isinstance(receipt["known_failures"], list) and receipt["known_failures"]
    timestamp_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}"
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(timestamp_pattern, receipt[field])
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated <= datetime.now().astimezone()

    recipes = receipt["structured_validation_recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0057-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0057-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert all(recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_task_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    structure_recipe = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("STRUCTURE"))
    expected_structure_output = b"intake invariant check: ok (THM-M-0057 planned; H1/M4/R4; six open tasks)\n"
    assert structure_recipe["expected_outputs"][0]["sha256"] == hashlib.sha256(expected_structure_output).hexdigest()
    assert structure_recipe["expected_outputs"][0]["semantic_hash_policy"] == "exact_bytes_sha256"
    assert structure_recipe["argv"] == [
        "/usr/bin/python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
        "--skip-replay",
    ]
    lean_recipe = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("LEAN-PROBE"))
    assert lean_recipe["expected_outputs"][0]["sha256"] == receipt["lean_probe_output_sha256"]
    if not args.skip_replay:
        lake = shutil.which("lake")
        assert lake is not None, "lake is missing from the runner tool path"
        runner_home = os.environ.get("HOME")
        assert runner_home, "HOME is required for pinned elan toolchain discovery"
        runner = [
            "bwrap",
            "--unshare-net",
            "--ro-bind",
            "/",
            "/",
            "--dev-bind",
            "/dev",
            "/dev",
            "--proc",
            "/proc",
            "--chdir",
            str(ROOT / lean_recipe["cwd"]),
            "/usr/bin/env",
            "-i",
            f"HOME={runner_home}",
            f"PATH={Path(lake).parent}:/usr/bin:/bin",
        ]
        lean_output = subprocess.check_output(
            runner + [lake, *lean_recipe["argv"][1:]],
            cwd=ROOT,
            stderr=subprocess.STDOUT,
            timeout=lean_recipe["timeout_seconds"],
        )
        assert hashlib.sha256(lean_output).hexdigest() == receipt["lean_probe_output_sha256"]

    actions = {action["recipe_id"]: action for action in receipt["validation_actions"]}
    assert set(actions) == {recipe["recipe_id"] for recipe in recipes}
    common_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
    ]
    expected_input_manifests = {
        "S56-M-0057-INTAKE-RECIPE-STRUCTURE": path_manifest_hash(
            common_inputs
            + [
                ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
                ROOT / "skills/execute-stage1-rev56/SKILL.md",
                ROOT / "Docs/researches/math_theorems.md",
                ROOT / "Docs/Stage0_Blueprint.md",
                HERE / "check_intake.py",
                HERE / "README.md",
                HERE / "scope-map.md",
                HERE / "source-statement-crosswalk.md",
                HERE / "validation.md",
            ]
        ),
        "S56-M-0057-INTAKE-RECIPE-LEAN-PROBE": path_manifest_hash(
            [
                ROOT / "Formalizations/Lean/lean-toolchain",
                ROOT / "Formalizations/Lean/lake-manifest.json",
                HERE / "IntakeProbe.lean",
            ]
        ),
    }
    for recipe in recipes:
        action = actions[recipe["recipe_id"]]
        assert action["observed_exit"] == recipe["expected_exit"] == 0
        assert action["covered_task_ids"] == recipe["covered_task_ids"] == [ITEM_ID]
        assert action["covered_obligation_ids"] == recipe["covered_obligation_ids"] == []
        assert action["covered_declarations"] == recipe["covered_declarations"]
        action_started = datetime.fromisoformat(action["started_at"])
        action_ended = datetime.fromisoformat(action["ended_at"])
        assert started <= action_started <= action_ended <= ended
        assert action["input_manifest_sha256"] == expected_input_manifests[recipe["recipe_id"]]
        assert action["output_evidence"][0]["sha256"] == recipe["expected_outputs"][0]["sha256"]
        assert action["log_evidence"]["sha256"] == action["output_evidence"][0]["sha256"]

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
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0057 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
