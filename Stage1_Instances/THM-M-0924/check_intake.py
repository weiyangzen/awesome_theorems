#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0924."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0924"
ITEM_ID = "S56-M-0924-INTAKE"
RANK = 1544
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STANDARD_OUTPUT = (
    b"check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, "
    b"1546 uniform-L0 Lean 4 targets, execution skill present)\n"
)
TARGET_CHECK_OUTPUT = (
    b"stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)\n"
)
PROBE_OUTPUT_SHA256 = "2860e9bc98e492ac65d7b24ca8a322694a7c4e304b20347cc1fa2738480d5429"
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
    "mathlib_linear_recurrence_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/LinearRecurrence.lean"
    ),
    "mathlib_nat_fib_basic_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Nat/Fib/Basic.lean"
    ),
    "mathlib_elliptic_divisibility_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/"
        "EllipticDivisibilitySequence.lean"
    ),
    "legacy_s1_m_018_source_sha256": (
        "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_018.lean"
    ),
}


def load(path: Path) -> dict:
    def unique_object(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"{path} contains duplicate JSON key {key!r}"
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


def check_receipt_inputs(receipt: dict) -> None:
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale receipt input hash: {relative}"
        )


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
    check_receipt_inputs(receipt)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "卢卡斯数"
    assert target["category"] == instance["category"] == "组合数学 / 计数组合"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 78
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == [] and item["attempts"] == 0
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
    assert "does_not_supply_one_stable_truth_valued_proposition" in instance["canonical_claim_status"]

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert set(formal["module_candidates"]) == {
        "Mathlib.Algebra.LinearRecurrence",
        "Mathlib.Data.Nat.Fib.Basic",
    }
    assert "LinearRecurrence.mkSol" in formal["declaration_candidates"]
    assert "Nat.fib_add_two" in formal["declaration_candidates"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["root_vector_status"] == "proposed_pending_master_acceptance"
    assert "H5 applies only" in instance["human_debt_scope"]
    assert "H5 correction route" in instance["execution_routing"]
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    source_commit = revisions["repository_source_record_commit"]
    assert git("rev-parse", f"{source_commit}:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob"]
    assert revisions["target_id_set_sha256"] == manifest["scope"]["canonical_sorted_target_id_set_sha256"]
    assert revisions["target_id_set_sha256"] == execution["target_id_set_sha256"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"

    assert subprocess.check_output(
        ["python3", "Docs/tools/check_stage1_standard.py"], cwd=ROOT
    ) == STANDARD_OUTPUT
    assert subprocess.check_output(
        ["python3", "scripts/stage1_target.py", "check"], cwd=ROOT
    ) == TARGET_CHECK_OUTPUT
    probe_env = os.environ.copy()
    probe_env.update({"LC_ALL": "C", "TZ": "UTC"})
    probe_output = subprocess.check_output(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0924/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        env=probe_env,
    )
    assert hashlib.sha256(probe_output).hexdigest() == PROBE_OUTPUT_SHA256

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0924-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert authoritative["state"] == "[ ]" and authoritative["attempts"] == 0
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert "target correction or redirection" in dag["tasks"][0]["first_blocker"]
    assert all("blocked_by" in task for task in dag["tasks"][1:])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**卢卡斯数**") == 1
    assert "- 提出者: Édouard Lucas" in catalog and "- 时间: 1878" in catalog
    assert catalog.count("- 陈述: 斐波那契数列的推广") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0924 卢卡斯数" in stage0 and "精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0925", "THM-M-0926", "THM-M-0927", "THM-M-0405"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0925": "斐波那契数列",
        "THM-M-0926": "卡西尼恒等式",
        "THM-M-0927": "比内公式",
        "THM-M-0405": "比拉斯基定理",
    }

    package_search = subprocess.run(
        [
            "rg", "-n", "-i", "--glob", "*.lean", "Lucas numbers|Lucas number|Lucas sequence",
            "Formalizations/Lean/.lake/packages",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        check=False,
    )
    assert package_search.returncode == 0
    hits = package_search.stdout.splitlines()
    assert hits == [
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/"
        "EllipticDivisibilitySequence.lean:27:* certain terms of Lucas sequences, and"
    ]
    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_018.lean").read_text(encoding="utf-8")
    assert "def lucasSequence (P Q : Int) : Nat -> Int" in legacy
    assert "| 0 => 0" in legacy and "| 1 => 1" in legacy
    assert "not evidence" in legacy

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["lifecycle_before"] == "L0 / rework_required with no rev-5.6 instance"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["first_failed_gate"].startswith(
        "S56-M-0924-INTAKE master acceptance"
    )
    assert receipt["first_failed_downstream_gate"].startswith("S56-M-0924-STATEMENT")
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert set(receipt["readable_ownership"]) == {
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
    }
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["diff_summary"] == {
        "added_target_owned_files": 9,
        "modified_or_deleted_preexisting_files": 0,
        "scheduler_metadata_files": [".stage1-worker-selftest.json"],
    }
    assert receipt["exact_statement_change"] == {
        "canonical_statements_added_or_changed": [],
        "boundary": "No canonical human or Lean statement was selected, added, or changed.",
    }
    assert receipt["source_revision_and_proof_body_summary"]["proof_body_locations"] == []
    assert receipt["axiom_and_placeholder_result"]["target_proof_audit"] == "not_applicable_no_target_or_proof_body"
    assert receipt["debt_delta_basis"]["after"] == {"H": "H5", "M": "M4", "R": "R4"}

    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert set(dirty["owned_untracked_paths"]) == set(receipt["changed_paths"])
    assert "excluded" in dirty["hash_boundary"]

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    assert worker_inputs["intake_probe_output_sha256"] == PROBE_OUTPUT_SHA256
    for field in (
        "mathlib_linear_recurrence_source_sha256",
        "mathlib_nat_fib_basic_source_sha256",
        "mathlib_elliptic_divisibility_source_sha256",
        "legacy_s1_m_018_source_sha256",
    ):
        assert worker_inputs[field] == revisions[field]

    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "exit_code", "covered_task_ids",
        "covered_obligation_ids", "covered_declarations", "result",
    }
    for recipe in receipt["structured_validation_recipes"]:
        assert set(recipe) == required_recipe_keys
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        if recipe["recipe_id"].endswith("LEAN-PROBE"):
            assert set(recipe["covered_declarations"]) == {
                "LinearRecurrence",
                "LinearRecurrence.IsSolution",
                "LinearRecurrence.mkSol",
                "LinearRecurrence.is_sol_mkSol",
                "LinearRecurrence.mkSol_eq_init",
                "LinearRecurrence.eq_mk_of_is_sol_of_eq_init'",
                "LinearRecurrence.sol_eq_of_eq_init",
                "Nat.fib",
                "Nat.fib_zero",
                "Nat.fib_one",
                "Nat.fib_add_two",
            }
        else:
            assert recipe["covered_declarations"] == []

    commands = receipt["commands_and_results"]
    assert isinstance(commands, list) and commands
    for command in commands:
        assert set(command) == {"cwd", "argv", "exit_code", "result"}
        assert isinstance(command["argv"], list) and command["argv"]
        assert isinstance(command["exit_code"], int)
        assert isinstance(command["result"], str) and command["result"]

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

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = (
        "sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ",
        "theorem ", "lemma ", "example ",
    )
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0924 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
