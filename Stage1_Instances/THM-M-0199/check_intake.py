#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0199 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0199"
ITEM_ID = "S56-M-0199-INTAKE"
RANK = 1531
BASE_REVISION = "5fe11f4b5e32a06ffb4432460319fc8ae906fe7b"
BASE_TREE = "64c5aacf7cf3eb79008f5a1970151e3e53cb9966"
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
    "mathlib_simplex_basic_source_sha256": (
        "Mathlib/LinearAlgebra/AffineSpace/Simplex/Basic.lean"
    ),
    "mathlib_affine_finite_dimensional_source_sha256": (
        "Mathlib/LinearAlgebra/AffineSpace/FiniteDimensional.lean"
    ),
    "mathlib_affine_map_source_sha256": (
        "Mathlib/LinearAlgebra/AffineSpace/AffineMap.lean"
    ),
    "mathlib_ceva_source_sha256": "Mathlib/LinearAlgebra/AffineSpace/Ceva.lean",
}
PROBE_DECLARATIONS = [
    "Affine.Triangle",
    "Affine.Simplex.points",
    "Affine.Simplex.independent",
    "AffineMap.lineMap",
    "AffineMap.lineMap_apply",
    "AffineMap.lineMap_apply_one_sub",
    "mem_affineSpan_pair_iff_exists_lineMap_eq",
    "Collinear",
    "affineIndependent_iff_not_collinear_set",
    "Collinear.mem_affineSpan_of_mem_of_ne",
    "Affine.Triangle.prod_eq_prod_one_sub_of_mem_line_point_lineMap",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_file(path.resolve())
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
    expected = set(receipt["changed_paths"]) | {".stage1-worker-selftest.json"}
    assert set(packet["changed_paths"]) == expected
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_probe(receipt: dict) -> None:
    result = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0199/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout.decode(errors="replace")
    expected = receipt["worker_input_hashes"]["lean_probe_stdout_sha256"]
    assert hashlib.sha256(result.stdout).hexdigest() == expected, "Lean probe output hash changed"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--run-lean", action="store_true")
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "梅涅劳斯定理"
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

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if args.worker_packet is not None:
        assert item["state"] == "[ ]", "worker packet must be checked against its pre-integration base"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["declaration_candidates"] == []
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector_status"] == "provisional_intake_classification_pending_master_acceptance"
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_current_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["stage0_current_blob"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    catalog_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines()
    catalog_excerpt = "\n".join(catalog_lines[1435:1441]) + "\n"
    assert hashlib.sha256(catalog_excerpt.encode()).hexdigest() == revisions["catalog_excerpt_sha256"]
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines()
    stage0_excerpt = "\n".join(stage0_lines[5535:5561]) + "\n"
    assert hashlib.sha256(stage0_excerpt.encode()).hexdigest() == revisions["stage0_excerpt_sha256"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
        assert receipt["worker_input_hashes"][field] == revisions[field]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert revisions["lake_symlink_target_sha256"] == hashlib.sha256(lake_target).hexdigest()

    expected_chain = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0199-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_chain.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_chain

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for phrase in (
        "**梅涅劳斯定理**",
        "- 提出者: Menelaus of Alexandria",
        "- 时间: 约公元100年",
        "- 陈述: 共线点的比例关系",
    ):
        assert phrase in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0199 梅涅劳斯定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files}
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["owned_output_sha256"]) == expected_changed
    for relative, digest in receipt["owned_output_sha256"].items():
        if digest is not None:
            assert digest == sha256(ROOT / relative), f"stale output hash: {relative}"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}"
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )
    assert receipt["worker_input_hashes"]["mathlib_revision"] == revisions["mathlib"]
    assert receipt["worker_input_hashes"]["mathlib_tree"] == revisions["mathlib_tree"]

    for recipe in receipt["structured_validation_recipes"]:
        assert recipe["recipe_id"].startswith(f"{ITEM_ID}-")
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
        assert recipe["covered_obligation_ids"] == []
    recipes = {recipe["recipe_id"]: recipe for recipe in receipt["structured_validation_recipes"]}
    assert recipes[f"{ITEM_ID}-lean-api-probe"]["covered_declarations"] == PROBE_DECLARATIONS

    if args.run_lean:
        check_probe(receipt)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0199 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
