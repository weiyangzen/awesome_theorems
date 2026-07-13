#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0903 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0903"
ITEM_ID = "S56-M-0903-INTAKE"
RANK = 1446
BASE_REVISION = "0c019b7194c9c43fa5f683fa82d637a0b275410d"
BASE_TREE = "43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e"
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
MATHLIB_SOURCE_FIELDS = {
    "matrix_basic_source_sha256": "Mathlib/Data/Matrix/Basic.lean",
    "fintype_equiv_fin_source_sha256": "Mathlib/Data/Fintype/EquivFin.lean",
    "fintype_big_operators_source_sha256": "Mathlib/Data/Fintype/BigOperators.lean",
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


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    return hashlib.sha256("".join(lines[first_line - 1 : last_line]).encode()).hexdigest()


def path_digest(paths: list[Path], *, manifest: bool) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        digest.update(path.relative_to(ROOT).as_posix().encode() + b"\0")
        data = path.read_bytes()
        digest.update(hashlib.sha256(data).digest() if manifest else data)
    return digest.hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["selftest_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["dirty_input_evidence"]["worker_packet_sha256"] == sha256(path)


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
    assert target["name"] == instance["name_zh"] == "Bose-Shrikhande-Parker定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    intake_item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake_item["theorem_id"] == THEOREM_ID and intake_item["execution_rank"] == RANK
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] == "[ ]" and intake_item["depends_on"] == []
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert intake_item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

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
    assert instance["target_decision"] == "source_root_selection_and_independent_review_required_before_statement_execution"
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 6607, 6612
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 24629, 24654
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0903-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
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
    assert catalog.count("**Bose-Shrikhande-Parker定理**") == 1
    assert "- 提出者: Bose/Shrikhande/Parker" in catalog
    assert "- 时间: 1960" in catalog
    assert catalog.count("- 陈述: Euler猜想的否定") == 1
    assert "**Euler猜想**" in catalog and "- 陈述: 正交拉丁方的存在性" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0903 Bose-Shrikhande-Parker定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0901", "THM-M-0902"
    }
    primary_hash = "cbd6489e0c3f7657a65b75ca4c2e09b3b7c9906919ed2a6b9cdc56bad6925107"
    assert revisions["inspected_primary_source_sha256"] == primary_hash
    assert instance["source_candidates_not_credited_as_H0"][0]["observed_source_sha256"] == primary_hash
    crossref_hash = "706ed0be2b21971ede7d51d90a2e6ee05faf52eef92776847d1eb541e9d1c256"
    assert revisions["crossref_response_observed_sha256"] == crossref_hash
    assert instance["bibliographic_observation"]["observed_sha256"] == crossref_hash

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
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    nonreceipt = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_nonreceipt_bytes_sha256"] == path_digest(nonreceipt, manifest=False)
    assert dirty["owned_nonreceipt_manifest_sha256"] == path_digest(nonreceipt, manifest=True)

    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    assert worker_inputs["lean_probe_output_sha256"] == "0deef5ed9e409b65e0ccfbaf71e0233f3cd94985ff1aeae9e68f8bf6a8cba51a"
    recipes = receipt["structured_validation_recipes"]
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_node_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
    assert recipes[0]["covered_declarations"] == []
    probe_declarations = [
        "Matrix", "Fin", "Fintype.card", "Fintype.equivFin", "Function.Bijective",
        "Equiv.ofBijective", "Prod",
    ]
    probe_expressions = [
        "Matrix (Fin 3) (Fin 3) (Fin 3)",
        "fun (A B : Matrix (Fin 3) (Fin 3) (Fin 3)) i j => (A i j, B i j)",
    ]
    assert recipes[1]["covered_declarations"] == probe_declarations
    assert recipes[1]["covered_expressions"] == probe_expressions
    assert recipes[0]["argv"][-2:] == [
        "--worker-packet", ".stage1-worker-selftest.json"
    ]
    actions = {action["action_id"]: action for action in receipt["validation_actions"]}
    assert set(actions) == {
        "S56-M-0903-INTAKE-ACTION-STRUCTURE-WORKER",
        "S56-M-0903-INTAKE-ACTION-LEAN-PROBE",
    }
    assert actions["S56-M-0903-INTAKE-ACTION-STRUCTURE-WORKER"]["stdout_sha256"] == (
        "c14e76efd85e6212ee17cd71f2362d1ad0b46309268e25416c324f94bb8e5876"
    )
    assert actions["S56-M-0903-INTAKE-ACTION-LEAN-PROBE"]["stdout_sha256"] == (
        worker_inputs["lean_probe_output_sha256"]
    )
    for action in actions.values():
        assert action["exit_code"] == 0
        assert action["log_sha256"] == action["stdout_sha256"]
        assert action["covered_node_ids"] == [ITEM_ID]
        assert action["covered_obligation_ids"] == []
    assert actions["S56-M-0903-INTAKE-ACTION-STRUCTURE-WORKER"]["covered_declarations"] == []
    lean_action = actions["S56-M-0903-INTAKE-ACTION-LEAN-PROBE"]
    assert lean_action["covered_declarations"] == probe_declarations
    assert lean_action["covered_expressions"] == probe_expressions

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md", "instance.json", "intake-receipt.json", "scope-map.md",
        "source-statement-crosswalk.md", "task-dag.json", "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-0903 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
