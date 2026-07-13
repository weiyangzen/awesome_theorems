#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0202 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0202"
ITEM_ID = "S56-M-0202-INTAKE"
RANK = 1534
BASE_REVISION = "27400857bccc93638c97e9c65859ddf5d5b5f4da"
BASE_TREE = "3762537e0e5ae46cd70b086da49a69e2fd7b275c"
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
    "check_json.py",
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
    "mathlib_sphere_basic_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/"
        "Sphere/Basic.lean"
    ),
    "mathlib_angle_sphere_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/"
        "Angle/Sphere.lean"
    ),
    "mathlib_triangle_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/"
        "Triangle.lean"
    ),
    "mathlib_real_sqrt_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Real/Sqrt.lean"
    ),
}


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        assert key not in value, f"duplicate JSON key: {key}"
        value[key] = item
    return value


def load(path: Path) -> dict[str, Any]:
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


def canonical_sha256(value: Any) -> str:
    data = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(data).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode()).hexdigest()


def check_worker_packet(path: Path, receipt: dict[str, Any]) -> None:
    path = path.resolve()
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
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["worker_packet_output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_receipt_inputs(receipt: dict[str, Any]) -> None:
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest.startswith("sha256:")
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale receipt input hash: {relative}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_receipt_inputs(receipt)

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert len(targets) == 1
    target = targets[0]
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "婆罗摩笈多公式"
    assert target["category"] == instance["category"] == "几何学 / 欧几里得几何"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 78
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(items) == 1
    item = items[0]
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
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["declaration_candidates"] == []
    assert "EuclideanGeometry.Concyclic" in formal["adjacent_declarations_not_target_candidates"]
    assert "EuclideanGeometry.Cospherical.two_zsmul_oangle_eq" in formal["adjacent_declarations_not_target_candidates"]
    assert instance["formal_candidates_not_credited"] == []
    source_candidates = instance["source_candidates_not_credited"]
    mathworld = next(row for row in source_candidates if "MathWorld" in row["citation"])
    mactutor = next(row for row in source_candidates if "MacTutor" in row["citation"])
    assert "fdc7bed68dab186140b589bdc5ed73766cb182b988d8ebf9987efaf1ebc3a270" in mathworld["candidate_locator"]
    assert "a0dd298afce7f195d672625306635f21d66844ed96806ae6a535606ee856d17e" in mactutor["candidate_locator"]
    assert "disagree" in mactutor["candidate_summary"]
    secondary_hashes = instance["inspected_secondary_source_hashes"]
    assert secondary_hashes["mathworld_brahmagupta_formula_html_sha256"] == (
        "fdc7bed68dab186140b589bdc5ed73766cb182b988d8ebf9987efaf1ebc3a270"
    )
    assert secondary_hashes["mactutor_brahmagupta_html_sha256"] == (
        "a0dd298afce7f195d672625306635f21d66844ed96806ae6a535606ee856d17e"
    )
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector_status"] == "provisional_intake_classification_pending_master_acceptance"
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert "no immutable pinpoint passage" in receipt["source_evidence"]["historical_source_lead"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blob"]
    assert (
        git(
            "rev-parse",
            f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
        )
        == revisions["repository_source_record_blob"]
    )
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 1457, 1462
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 5617, 5642
    )
    assert revisions["manifest_entry_sha256"] == canonical_sha256(target)
    assert revisions["execution_dag_intake_entry_sha256"] == canonical_sha256(item)
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("rev-parse", "HEAD:Mathlib/Geometry/Euclidean/Sphere/Basic.lean", cwd=mathlib) == revisions["mathlib_sphere_basic_source_blob"]
    assert git("rev-parse", "HEAD:Mathlib/Geometry/Euclidean/Angle/Sphere.lean", cwd=mathlib) == revisions["mathlib_angle_sphere_source_blob"]
    assert git("rev-parse", "HEAD:Mathlib/Geometry/Euclidean/Triangle.lean", cwd=mathlib) == revisions["mathlib_triangle_source_blob"]
    assert git("rev-parse", "HEAD:Mathlib/Data/Real/Sqrt.lean", cwd=mathlib) == revisions["mathlib_real_sqrt_source_blob"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert revisions["lake_symlink_target_sha256"] == hashlib.sha256(lake_target).hexdigest()

    expected_tasks: list[tuple[str, list[str]]] = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0202-{suffix}"
        authoritative_rows = [row for row in execution["items"] if row["id"] == task_id]
        task_rows = [row for row in dag["tasks"] if row["id"] == task_id]
        assert len(authoritative_rows) == len(task_rows) == 1
        authoritative = authoritative_rows[0]
        task = task_rows[0]
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
    assert catalog.count("**婆罗摩笈多公式**") == 1
    assert "- 提出者: Brahmagupta" in catalog
    assert "- 时间: 628" in catalog
    assert "- 陈述: 圆内接四边形面积公式" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0202 婆罗摩笈多公式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0201",
        "THM-M-0203",
        "THM-M-0209",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(actual_files)),
    ]
    assert receipt["changed_paths"] == expected_changed
    owned_changed = set(expected_changed) - {".stage1-worker-selftest.json"}
    assert set(receipt["owned_output_sha256"]) == owned_changed
    for relative, digest in receipt["owned_output_sha256"].items():
        if digest is not None:
            assert digest == sha256(ROOT / relative), f"stale owned output hash: {relative}"
    assert receipt["owned_output_sha256"][f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"] is None
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert validated_at.tzinfo is not None
    assert validated_at.date().isoformat() == "2026-07-13"
    assert validated_at <= datetime.now(validated_at.tzinfo)
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["receipt_conformance"] == "worker_handoff_only_not_a_rev_5_6_accepted_evidence_receipt"
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["known_failures"] and all(
        isinstance(failure, str) and failure for failure in receipt["known_failures"]
    )
    expected_commands = [
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-0202",
        "git status --short --untracked-files=all",
        "git rev-parse HEAD 'HEAD^{tree}'",
        "git blame -L 1457,1462 -- Docs/researches/math_theorems.md",
        "cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0202/IntakeProbe.lean",
        "python3 -m json.tool Stage1_Instances/THM-M-0202/instance.json",
        "python3 -m json.tool Stage1_Instances/THM-M-0202/task-dag.json",
        "python3 -m json.tool Stage1_Instances/THM-M-0202/intake-receipt.json",
        "python3 -m json.tool .stage1-worker-selftest.json",
        "PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0202-pycache python3 -m py_compile Stage1_Instances/THM-M-0202/check_intake.py",
        "python3 -B Stage1_Instances/THM-M-0202/check_intake.py --worker-packet .stage1-worker-selftest.json",
        "python3 -B Stage1_Instances/THM-M-0202/check_intake.py",
        "python3 -B Stage1_Instances/THM-M-0202/check_json.py --worker-packet",
        "git diff --check -- Stage1_Instances/THM-M-0202 .stage1-worker-selftest.json",
    ]
    assert receipt["worker_packet_commands"] == expected_commands

    for recipe in receipt["structured_validation_recipes"]:
        assert recipe["recipe_id"].startswith(f"S56-M-0202-INTAKE-")
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
        assert recipe["covered_obligation_ids"] == []

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

    lean = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    assert prohibited.search(lean) is None, "prohibited Lean construct in intake probe"
    assert "theorem " not in lean and "lemma " not in lean
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    else:
        # Public replay intentionally excludes the scheduler-only root packet.
        assert receipt["worker_packet_reference"]["state"] == "[_]"

    print("intake invariant check: ok (THM-M-0202 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
