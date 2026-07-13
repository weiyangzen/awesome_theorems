#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0268 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0268"
ITEM_ID = "S56-M-0268-INTAKE"
RANK = 1275
BASE_REVISION = "c2e294becadae6ce784f27ee69f2e8dbf57e0b30"
BASE_TREE = "3f567e7f76b189432b73444354070c0ff75925b9"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "81fca7c7753f2df01239d9dd0cc06b239786902a8810a9f9799f24930315d1d4"
STAGE0_EXCERPT_SHA256 = "4aba16dc67a11e0aff65c0d56d13018a569eb3a0b994346fd3b9041dd3d7d839"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "834ccd18e768f3995086da58e3d02c89a3e51d12881731300802c066d4e73ebe"
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
    "MeasureTheory.tendsto_integral_of_dominated_convergence",
    "MeasureTheory.tendsto_integral_filter_of_dominated_convergence",
    "MeasureTheory.tendsto_lintegral_of_dominated_convergence",
    "MeasureTheory.tendsto_lintegral_of_dominated_convergence'",
    "MeasureTheory.tendsto_lintegral_filter_of_dominated_convergence",
    "MeasureTheory.hasFiniteIntegral_of_dominated_convergence",
    "MeasureTheory.tendsto_lintegral_norm_of_dominated_convergence",
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
STRUCTURE_INPUTS = (
    "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "Stage1_Instances/THM-M-0268/instance.json",
    "Stage1_Instances/THM-M-0268/task-dag.json",
    "Stage1_Instances/THM-M-0268/check_intake.py",
)
LEAN_INPUTS = (
    "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json",
    "Stage1_Instances/THM-M-0268/IntakeProbe.lean",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/DominatedConvergence.lean",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/HasFiniteIntegral.lean",
)


def load(path: Path) -> dict:
    def unique_object(pairs: list[tuple[str, object]]) -> dict:
        value = {}
        for key, item in pairs:
            assert key not in value, f"{path} contains duplicate JSON key: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
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


def canonical_json_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((raw + "\n").encode("utf-8")).hexdigest()


def path_content_hash(paths: tuple[str, ...] | list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update((ROOT / relative).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
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
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["first_failed_gate"] == receipt["first_failed_gate"]
    assert packet["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]


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
    assert target["name"] == instance["name_zh"] == "勒贝格控制收敛定理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
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
    assert item["state"] in ("[ ]", "[_]") and item["depends_on"] == []
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
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("hash-object", "Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 1929, 1934) == SOURCE_EXCERPT_SHA256
    assert revisions["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7414, 7439) == STAGE0_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    manifest_entry = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert revisions["manifest_entry_sha256"] == canonical_json_hash(manifest_entry)
    assert revisions["execution_dag_intake_entry_sha256"] == canonical_json_hash(item)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == "", "pinned mathlib package is dirty"
    assert revisions["mathlib_bochner_dominated_convergence_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/DominatedConvergence.lean"
    )
    assert revisions["mathlib_lintegral_dominated_convergence_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/Lebesgue/DominatedConvergence.lean"
    )
    assert revisions["mathlib_has_finite_integral_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Function/L1Space/HasFiniteIntegral.lean"
    )

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0268-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        source = next(row for row in execution["items"] if row["id"] == task_id)
        task = dag["tasks"][layer - 1]
        assert task["phase"] == source["phase"] and task["layer"] == source["layer"]
        assert task["owned_paths"] == source["owned_paths"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**勒贝格控制收敛定理**" in catalog
    assert "- 提出者: Henri Lebesgue" in catalog
    assert "- 时间: 1902" in catalog
    assert "- 陈述: 积分与极限交换的条件" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0268 勒贝格控制收敛定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert set(formal["declaration_candidates"]) == set(PROBE_DECLARATIONS)
    assert {
        candidate["declaration"] for candidate in instance["formal_candidates_not_credited"]
    } == set(PROBE_DECLARATIONS)

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["owned_artifact_sha256"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == instance["normative_profile"]
    assert receipt["receipt_id"] == "S56-M-0268-INTAKE-PROVISIONAL-C2E294BE"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["execution_rank"] == RANK
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["lifecycle_before"] == "L0 / rework_required"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["acceptance_authority"] == "rev-5.6 integration lane"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["content_addressed"] is receipt["signed"] is False
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["authority_input_sha256"] == {
        "Docs/Stage1_Targets_rev-5.6.json": f"sha256:{revisions['target_manifest_sha256']}",
        "Docs/Stage1_Blueprint_rev-5.6.md": f"sha256:{revisions['authoritative_blueprint_sha256']}",
        "Docs/Stage1_Execution_DAG_rev-5.6.json": f"sha256:{revisions['execution_dag_sha256']}",
        "skills/execute-stage1-rev56/SKILL.md": f"sha256:{revisions['execution_skill_sha256']}",
        "Docs/Blueprint_Guidelines.md": f"sha256:{revisions['blueprint_guidelines_sha256']}",
    }
    assert receipt["source_input_sha256"] == {
        "Docs/researches/math_theorems.md": f"sha256:{revisions['repository_math_source_sha256']}",
        "Docs/Stage0_Blueprint.md": f"sha256:{revisions['stage0_blueprint_sha256']}",
        "catalog_record_excerpt": f"sha256:{SOURCE_EXCERPT_SHA256}",
        "stage0_record_excerpt": f"sha256:{STAGE0_EXCERPT_SHA256}",
    }
    evidence = receipt["source_evidence"]
    assert evidence["repository_source_record_commit"] == SOURCE_COMMIT
    assert evidence["repository_source_record_blob"] == SOURCE_BLOB
    assert "Lebesgue" in evidence["catalog_record"] and "1902" in evidence["catalog_record"]
    assert "10.1007/BF02420592" in evidence["primary_source_lead"]
    assert evidence["proof_body_locations"] == []
    assert set(evidence["formal_source_leads"]) == set(formal["module_candidates"])
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    assert worker_inputs["intake_probe_sha256"] == sha256(HERE / "IntakeProbe.lean")
    assert worker_inputs["lean_probe_output_sha256"] == PROBE_OUTPUT_SHA256
    assert receipt["validated_scope"] == (
        "planned theorem dossier, scope map, source-statement crosswalk, bibliographic source lead, "
        "direct pinned Lean candidate-interface probe, structured invariants, and six-node open "
        "downstream task DAG only"
    )
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    recipes = {row["recipe_id"]: row for row in receipt["structured_validation_recipes"]}
    actions = {row["recipe_id"]: row for row in receipt["validation_actions"]}
    expected_recipe_ids = {
        "S56-M-0268-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0268-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert set(recipes) == set(actions) == expected_recipe_ids
    recipe_identity_fields = (
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
    )
    for recipe_id, recipe in recipes.items():
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] in {"fetch_only", "denied", "explicitly_required"}
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
        identity = {field: recipe[field] for field in recipe_identity_fields}
        action = actions[recipe_id]
        raw = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        assert action["recipe_sha256"] == hashlib.sha256(raw.encode("utf-8")).hexdigest()
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        for field in ("stdout_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
    structure_recipe = recipes["S56-M-0268-INTAKE-RECIPE-STRUCTURE"]
    lean_recipe = recipes["S56-M-0268-INTAKE-RECIPE-LEAN-PROBE"]
    assert structure_recipe["covered_declarations"] == []
    assert set(lean_recipe["covered_declarations"]) == set(PROBE_DECLARATIONS)
    assert structure_recipe["expected_outputs"] == [
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": "must contain the exact planned H1/M3/R4 and six-open-task success line",
        }
    ]
    assert lean_recipe["expected_outputs"] == [
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": f"complete UTF-8 combined output SHA-256 {PROBE_OUTPUT_SHA256}",
        }
    ]
    structure_digest = hashlib.sha256(
        b"intake invariant check: ok (THM-M-0268 planned; H1/M3/R4; six open tasks)\n"
    ).hexdigest()
    assert actions["S56-M-0268-INTAKE-RECIPE-STRUCTURE"]["stdout_sha256"] == structure_digest
    assert actions["S56-M-0268-INTAKE-RECIPE-STRUCTURE"]["log_sha256"] == structure_digest
    assert actions["S56-M-0268-INTAKE-RECIPE-LEAN-PROBE"]["stdout_sha256"] == PROBE_OUTPUT_SHA256
    assert actions["S56-M-0268-INTAKE-RECIPE-LEAN-PROBE"]["log_sha256"] == PROBE_OUTPUT_SHA256
    assert actions["S56-M-0268-INTAKE-RECIPE-STRUCTURE"]["input_manifest_sha256"] == path_content_hash(
        STRUCTURE_INPUTS
    )
    assert actions["S56-M-0268-INTAKE-RECIPE-LEAN-PROBE"]["input_manifest_sha256"] == path_content_hash(
        LEAN_INPUTS
    )
    dirty = receipt["dirty_input_evidence"]
    unhashed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    dirty_paths = sorted(expected_changed - unhashed)
    assert dirty["owned_untracked_paths"] == dirty_paths
    assert dirty["owned_untracked_patch_sha256"] == path_content_hash(dirty_paths)
    manifest = {relative: sha256(ROOT / relative) for relative in dirty_paths}
    assert dirty["owned_untracked_manifest_sha256"] == canonical_json_hash(manifest)

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
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0268/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    for declaration in PROBE_DECLARATIONS:
        assert declaration in lean_run.stdout

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0268 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
