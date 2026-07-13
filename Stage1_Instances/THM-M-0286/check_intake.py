#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0286 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0286"
ITEM_ID = "S56-M-0286-INTAKE"
RANK = 1292
BASE_REVISION = "2eea98305d46266f078a50cf0e85853bf6a5e702"
BASE_TREE = "02279a8caa5f31ed8e37e35c8584a336eed9b974"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "763f5671f415d22937207dda25b4c9bd2277a4917c228bef3dc6fbbd1da3573c"
STAGE0_EXCERPT_SHA256 = "5dcff61d3a343560bd8684937cdc9a6a56c77a6f2f2766d38361dde6fac4e72b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_BLOB = "f61bda8ec5123da5a50542257f2313105229edc8"
MATHLIB_SOURCE_SHA256 = "b50aa1f20a157911db8a9dec01bc58ff0f1f2832b146a98b9bf80ca1d977a226"
PROBE_OUTPUT_SHA256 = "464b3a706f14c55c7158b6e30b175ba6586a88618cdda1bf128c20bedcaf871f"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
PROBE_DECLARATIONS = (
    "MeasureTheory.Egorov.notConvergentSeq",
    "MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist",
    "MeasureTheory.tendstoUniformlyOn_of_ae_tendsto",
    "MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist'",
    "MeasureTheory.tendstoUniformlyOn_of_ae_tendsto'",
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


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


def run_recipe(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {"LC_ALL": "C", "TZ": "UTC"}
    assert recipe["network_policy"] == "denied"
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "TZ": "UTC"})
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"] == recipe["exit_code"], result.stdout.decode(
        errors="replace"
    )
    return result.stdout


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
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "叶戈罗夫定理",
        "category": "分析学 / 实分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
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
    assert instance["name_zh"] == target["name"] and instance["category"] == target["category"]

    intake_item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake_item["theorem_id"] == THEOREM_ID and intake_item["execution_rank"] == RANK
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] == "[ ]" and intake_item["depends_on"] == []
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake_item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )
    assert intake_item["attempts"] == 0 and intake_item["children"] == []

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
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
    assert formal["declaration_candidates"] == list(PROBE_DECLARATIONS[1:])
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 2055, 2060) == (
        revisions["repository_record_excerpt_sha256"]
    ) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7900, 7925) == (
        revisions["stage0_projection_excerpt_sha256"]
    ) == STAGE0_EXCERPT_SHA256
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{revisions[field]}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    source = mathlib / "Mathlib/MeasureTheory/Function/Egorov.lean"
    assert git("hash-object", source.relative_to(mathlib).as_posix(), cwd=mathlib) == (
        revisions["mathlib_egorov_source_blob"]
    ) == MATHLIB_SOURCE_BLOB
    assert sha256(source) == revisions["mathlib_egorov_source_sha256"] == MATHLIB_SOURCE_SHA256
    assert sha256(mathlib / "docs/1000.yaml") == revisions["mathlib_1000_yaml_sha256"]

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0286-{suffix}"
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency], layer))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**叶戈罗夫定理**" in catalog
    assert "- 提出者: Dmitri Egorov" in catalog
    assert "- 时间: 1911" in catalog
    assert "- 陈述: 几乎处处收敛与一致收敛的关系" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0286 叶戈罗夫定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    assert worker_inputs["mathlib_egorov_source_sha256"] == MATHLIB_SOURCE_SHA256
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == (
        "sha256:" + hashlib.sha256(lake_target).hexdigest()
    ) == f"sha256:{LAKE_SYMLINK_TARGET_SHA256}"
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale artifact hash: {relative}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    lean_recipe = next(
        recipe
        for recipe in receipt["structured_validation_recipes"]
        if recipe["recipe_id"] == "S56-M-0286-INTAKE-RECIPE-LEAN-PROBE"
    )
    lean_output = run_recipe(lean_recipe)
    assert hashlib.sha256(lean_output).hexdigest() == PROBE_OUTPUT_SHA256
    for declaration in PROBE_DECLARATIONS:
        assert declaration.encode() in lean_output

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0286 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
