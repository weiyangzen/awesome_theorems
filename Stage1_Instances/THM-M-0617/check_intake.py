#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0617 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0617"
ITEM_ID = "S56-M-0617-INTAKE"
RANK = 1311
BASE_REVISION = "d257e1e5e5fa003d6e1f26344c0331bf99374fa9"
BASE_TREE = "fa06b50b528e038d182d5479a18296f63fa5eae5"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "92ecc7af143bf0c75b11cf94d1f88ce6edbcc5217b0defebd68ec097d748afff"
STAGE0_EXCERPT_SHA256 = "3afd0f86c25d7dbebdfcb2806d7d3e675520cb6a41eaa1a3574cad978fb2ec3b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "1ba2ff9c58728fdf189ec19105f478c2d8a96c20a12e514bb23e86c561484d75"
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
    "IsCompact.of_isClosed_subset",
    "IsCompact.image_of_continuousOn",
    "IsCompact.image",
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
    "mathlib_filter_defs_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Defs/Filter.lean"
    ),
    "mathlib_compact_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Compactness/Compact.lean"
    ),
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


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode("utf-8")).hexdigest()


def check_text_hygiene(path: Path) -> None:
    content = path.read_bytes()
    assert content.endswith(b"\n"), f"missing final newline: {path}"
    assert not content.endswith(b"\n\n"), f"extra blank line at EOF: {path}"
    assert b"\r" not in content, f"carriage return: {path}"
    assert b"\0" not in content, f"NUL byte: {path}"
    for number, line in enumerate(content.splitlines(), start=1):
        assert line.rstrip() == line, f"trailing whitespace: {path}:{number}"


def run_recipe(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    check_text_hygiene(path.resolve())
    packet = load(path.resolve())
    required = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert required <= set(packet), "worker packet omits a scheduler-required field"
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["verdict"] == "no_state_change"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["covered_node_ids"] == [ITEM_ID]
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["first_failed_gate"] == receipt["first_failed_gate"]
    assert packet["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


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
    assert target["name"] == instance["name_zh"] == "紧致性定理"
    assert target["category"] == instance["category"] == "拓扑学 / 点集拓扑"
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
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "紧集的闭子集紧，连续像紧"
    assert instance["canonical_statement"] == (
        "Closed subsets of compact sets are compact, and continuous images of compact sets are compact."
    )
    assert "both independent preservation clauses" in instance["canonical_claim"]
    formal = instance["canonical_formal_target"]
    assert formal["module"] is formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is formal["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert "No binder-complete canonical formal proposition" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    git("cat-file", "-e", f"{BASE_REVISION}^{{commit}}")
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 4580, 4585) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 16882, 16907) == STAGE0_EXCERPT_SHA256
    assert revisions["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0617-{suffix}"
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
    assert "**紧致性定理**\n- 提出者: 众多数学家\n- 时间: 19世纪\n- 陈述: 紧集的闭子集紧，连续像紧" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0617 紧致性定理" in stage0
    assert "- 定理内容: 紧集的闭子集紧，连续像紧" in stage0
    compact_source = (ROOT / SOURCE_HASH_FIELDS["mathlib_compact_source_sha256"]).read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"theorem {declaration}" in compact_source

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for name in OWNED_FILES:
        check_text_hygiene(HERE / name)
    expected_changes = {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    assert set(receipt["changed_paths"]) == expected_changes
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["proof_body_locations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    probe_recipe = next(
        recipe for recipe in receipt["structured_validation_recipes"]
        if recipe["recipe_id"].endswith("LEAN-PROBE")
    )
    probe_output = run_recipe(probe_recipe)
    assert hashlib.sha256(probe_output).hexdigest() == PROBE_OUTPUT_SHA256
    decoded = probe_output.decode("utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert declaration in decoded
    assert decoded.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 2

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0617 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
