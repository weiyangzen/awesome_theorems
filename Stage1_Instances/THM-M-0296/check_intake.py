#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0296."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0296"
ITEM_ID = "S56-M-0296-INTAKE"
RANK = 1300
BASE_REVISION = "940588d30669014430d5a1beb187f2bca118e816"
BASE_TREE = "42d80725ccbabcdd826ed2bc8b3622ac31ac7695"
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
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recorded_action(recipe: dict) -> bytes:
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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert receipt["worker_input_hashes"]["worker_packet_sha256"] == sha256(path)


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
    assert target["name"] == instance["name_zh"] == "里斯-索林插值定理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
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
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_math_source_blob_at_base"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert revisions["mathlib_hadamard_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/Complex/Hadamard.lean"
    )
    assert revisions["mathlib_lp_space_source_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Function/LpSpace/Basic.lean"
    )

    authoritative_tasks = {
        row["id"]: row for row in execution_dag["items"] if row["theorem_id"] == THEOREM_ID
    }
    dependency = ITEM_ID
    for task, suffix in zip(dag["tasks"], TASK_SUFFIXES, strict=True):
        assert task["id"] == f"S56-M-0296-{suffix}"
        assert task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        authority = authoritative_tasks[task["id"]]
        assert task["phase"] == authority["phase"]
        assert task["layer"] == authority["layer"]
        assert task["depends_on"] == authority["depends_on"]
        assert task["owned_paths"] == authority["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authority["deliverable"]
        assert task["completion_gate"] == authority["completion_gate"]
        dependency = task["id"]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**里斯-索林插值定理**" in catalog
    assert "- 提出者: Marcel Riesz/Thorvald Thorin" in catalog
    assert "- 时间: 1939" in catalog
    assert "- 陈述: 算子的插值理论" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0296 里斯-索林插值定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0295",
        "THM-M-0297",
        "THM-M-0374",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(actual_files)
    ]
    assert receipt["changed_paths"] == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "provisional:S56-M-0296-INTAKE:940588d3:lp-three-lines-probe-438e7f69"
    assert receipt["selftest_id"] == "S56-M-0296-INTAKE-worker-selftest"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["intent"] == "intake" and receipt["validated_scope"]
    assert isinstance(receipt["attestor"], str) and receipt["attestor"]
    assert receipt["platform"] == {
        "system": "Linux",
        "machine": "x86_64",
        "lean_version": "4.29.0",
        "lean_commit": "98dc76e3c0a9b856c9b98726b713fb04fab16740",
        "lake_version": "5.0.0-src+98dc76e",
        "mathlib_revision": MATHLIB_REVISION,
        "mathlib_tree": MATHLIB_TREE,
    }
    assert isinstance(receipt["environment_boundary"], str) and receipt["environment_boundary"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["owned_input_manifest_sha256"] == path_manifest_hash(
        [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    )
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["output_summary"] and receipt["known_failures"]
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field])
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}"

    recipes = receipt["structured_validation_recipes"]
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
    assert len(recipes) == 2 and all(set(recipe) == required_recipe_keys for recipe in recipes)
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert {action["action_id"] for action in actions} == {
        "S56-M-0296-INTAKE-ACTION-STRUCTURE",
        "S56-M-0296-INTAKE-ACTION-LEAN-PROBE",
    }
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        identity = {
            "cwd": recipe["cwd"],
            "argv": recipe["argv"],
            "env_allowlist": recipe["env_allowlist"],
            "timeout_seconds": recipe["timeout_seconds"],
            "network_policy": recipe["network_policy"],
            "expected_exit": recipe["expected_exit"],
        }
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
    action_by_id = {action["action_id"]: action for action in actions}
    structure_inputs = [ROOT / relative for relative in SOURCE_HASH_FIELDS.values()] + [
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
        ROOT / ".stage1-worker-selftest.json",
        ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/Hadamard.lean",
        ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean",
    ]
    structure_inputs = list(dict.fromkeys(structure_inputs))
    assert action_by_id["S56-M-0296-INTAKE-ACTION-STRUCTURE"]["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert action_by_id["S56-M-0296-INTAKE-ACTION-LEAN-PROBE"]["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    structure_stdout = b"intake invariant check: ok (THM-M-0296 planned; H1/M4/R4; six open tasks)\n"
    structure_hash = hashlib.sha256(structure_stdout).hexdigest()
    structure_action = action_by_id["S56-M-0296-INTAKE-ACTION-STRUCTURE"]
    assert structure_action["stdout_sha256"] == structure_action["log_sha256"] == structure_hash
    lean_action = action_by_id["S56-M-0296-INTAKE-ACTION-LEAN-PROBE"]
    lean_stdout = run_recorded_action(recipes_by_id[lean_action["recipe_id"]])
    lean_hash = hashlib.sha256(lean_stdout).hexdigest()
    assert lean_action["stdout_sha256"] == lean_action["log_sha256"] == lean_hash
    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        public_text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    print("intake invariant check: ok (THM-M-0296 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
