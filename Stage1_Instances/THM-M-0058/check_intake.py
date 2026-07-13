#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0058 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0058"
ITEM_ID = "S56-M-0058-INTAKE"
RANK = 1525
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
MATHLIB_SOURCE_FIELDS = {
    "mathlib_singular_values_source_sha256":
        "Mathlib/Analysis/InnerProductSpace/SingularValues.lean",
    "mathlib_inner_product_trace_source_sha256":
        "Mathlib/Analysis/InnerProductSpace/Trace.lean",
    "mathlib_matrix_trace_source_sha256": "Mathlib/LinearAlgebra/Matrix/Trace.lean",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256((data + "\n").encode()).hexdigest()


def recipe_sha256(recipe: dict) -> str:
    identity = {
        "cwd": recipe["cwd"],
        "argv": recipe["argv"],
        "env_allowlist": recipe["env_allowlist"],
        "timeout_seconds": recipe["timeout_seconds"],
        "network_policy": recipe["network_policy"],
        "expected_exit": recipe["expected_exit"],
    }
    data = json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    return hashlib.sha256("".join(lines[first_line - 1 : last_line]).encode()).hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    sandbox = shutil.which("bwrap")
    assert sandbox is not None, "bubblewrap is required for the network-denied replay"
    lake = (ROOT / "Formalizations/Lean/.lake").resolve(strict=True)
    command = [
        sandbox,
        "--bind", "/", "/",
        "--dev", "/dev",
        "--proc", "/proc",
        "--unshare-net",
        "--die-with-parent",
        "--ro-bind", os.fspath(lake), os.fspath(lake),
        "--chdir", os.fspath(ROOT / recipe["cwd"]),
        *recipe["argv"],
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    data = path.resolve().read_bytes()
    assert data.endswith(b"\n"), "worker packet is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    mandatory = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert mandatory <= set(packet)
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["theorem_id"] == THEOREM_ID
    assert packet["node_ids"] == [ITEM_ID]
    assert packet["intent"] == "intake" and packet["verdict"] == "no_state_change"
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["canonical_obligation_ids"] == packet["statement_fingerprints"] == []
    assert packet["typed_graph_changes"] == packet["composition_certificates"] == []
    assert packet["content_addressed_recipe_ids"] == []
    assert isinstance(packet["retry_condition"], str) and packet["retry_condition"]


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
    assert target["name"] == instance["name_zh"] == "冯·诺依曼迹不等式"
    assert target["category"] == instance["category"] == "代数学 / 线性代数"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 78
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
    assert "classical_theorem_family_identified" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["provisional_family_intake_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["root_vector"] is None
    assert instance["root_vector_status"].startswith("unclassified_until_canonical_statement")
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
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert manifest["scope"]["canonical_sorted_target_id_set_sha256"] == revisions["canonical_sorted_target_id_set_sha256"]
    assert canonical_sha256(target) == revisions["manifest_entry_canonical_sha256"]
    target_rows = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert canonical_sha256(target_rows) == revisions["target_dag_rows_canonical_sha256"]
    assert len(target_rows) == 7
    assert all(row["state"] == "[ ]" and row["attempts"] == 0 and row["children"] == [] for row in target_rows)
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 433, 438
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 1699, 1724
    )
    assert revisions["neighbor_catalog_block_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 389, 445
    )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    flt_regular = ROOT / "Formalizations/Lean/.lake/packages/flt-regular"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--porcelain", cwd=mathlib)
    for field, relative in MATHLIB_SOURCE_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    assert git("rev-parse", "HEAD", cwd=flt_regular) == (
        "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
    )
    assert git("rev-parse", "HEAD^{tree}", cwd=flt_regular) == (
        "32c9eace926573a9981787ae97643e520353c893"
    )
    assert not git("status", "--porcelain", cwd=flt_regular)

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0058-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        assert authoritative["state"] == "[ ]"
        assert authoritative["attempts"] == 0 and authoritative["children"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**冯·诺依曼迹不等式**") == 1
    assert "- 提出者: John von Neumann" in catalog
    assert "- 时间: 1937" in catalog
    assert catalog.count("- 陈述: 矩阵迹的最大值不等式") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0058 冯·诺依曼迹不等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0055", "THM-M-0056", "THM-M-0057", "THM-M-0059"
    }
    legacy = (ROOT / instance["legacy_discovery_boundary"]["path"]).read_text(encoding="utf-8")
    assert "THM-M-0430: Langlands reciprocity" in legacy

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
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
    if args.worker_packet is not None:
        assert receipt["worker_packet_sha256"] == sha256(args.worker_packet.resolve())
        non_self_referential = [
            HERE / name for name in OWNED_FILES if name != "intake-receipt.json"
        ] + [args.worker_packet.resolve()]
        assert dirty["non_self_referential_changed_bytes_sha256"] == path_bytes_hash(
            non_self_referential
        )
        assert dirty["non_self_referential_changed_manifest_sha256"] == path_manifest_hash(
            non_self_referential
        )
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]
    ]
    assert receipt["selftest_result"] == "pass"
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert isinstance(receipt["retry_condition"], str) and receipt["retry_condition"]
    assert receipt["commands_and_results"]
    assert all(
        isinstance(record["command"], str)
        and isinstance(record["exit_code"], int)
        and isinstance(record["result"], str)
        for record in receipt["commands_and_results"]
    )
    for field in ("reviewer_policy", "validated_at", "review_due", "support_state", "incident_path"):
        assert isinstance(receipt[field], str) and receipt[field]
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()

    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    for field, relative in MATHLIB_SOURCE_FIELDS.items():
        assert worker_inputs[field] == sha256(mathlib / relative)
    recipes = receipt["structured_validation_recipes"]
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_task_ids"] == [ITEM_ID]
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert {action["action_id"] for action in actions} == {
        "S56-M-0058-INTAKE-ACTION-STRUCTURE",
        "S56-M-0058-INTAKE-ACTION-LEAN-PROBE",
    }
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        assert action["recipe_sha256"] == recipe_sha256(recipe)
        assert action["exit_code"] == 0
        assert action["covered_task_ids"] == [ITEM_ID]
        assert action["log_sha256"] == action["stdout_sha256"]
        action_started = datetime.fromisoformat(action["started_at"])
        action_ended = datetime.fromisoformat(action["ended_at"])
        assert action_started <= action_ended <= validated_at
    by_id = {action["action_id"]: action for action in actions}
    structure_inputs = [
        ROOT / relative for relative in SOURCE_HASH_FIELDS.values()
    ] + [
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_058.lean"
    ] + [
        HERE / name for name in OWNED_FILES if name != "intake-receipt.json"
    ]
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        mathlib / "Mathlib/Analysis/InnerProductSpace/SingularValues.lean",
        mathlib / "Mathlib/Analysis/InnerProductSpace/Trace.lean",
        mathlib / "Mathlib/LinearAlgebra/Matrix/Trace.lean",
        HERE / "IntakeProbe.lean",
    ]
    if args.worker_packet is not None:
        structure_inputs.append(args.worker_packet.resolve())
        assert by_id["S56-M-0058-INTAKE-ACTION-STRUCTURE"]["input_manifest_sha256"] == (
            path_manifest_hash(structure_inputs)
        )
    assert by_id["S56-M-0058-INTAKE-ACTION-LEAN-PROBE"]["input_manifest_sha256"] == (
        path_manifest_hash(lean_inputs)
    )
    structure_stdout = (
        b"intake invariant check: ok (THM-M-0058 planned; "
        b"H1/M4/R4 provisional; six open tasks)\n"
    )
    assert by_id["S56-M-0058-INTAKE-ACTION-STRUCTURE"]["stdout_sha256"] == hashlib.sha256(
        structure_stdout
    ).hexdigest()
    assert by_id["S56-M-0058-INTAKE-ACTION-LEAN-PROBE"]["stdout_sha256"] == (
        "e18b90204be5fcc95fc6ee4af29178d62c2af16eafdf5bb91d162a9d885fd427"
    )
    lean_recipe = recipes_by_id["S56-M-0058-INTAKE-RECIPE-LEAN-PROBE"]
    assert hashlib.sha256(run_recorded_action(lean_recipe)).hexdigest() == (
        by_id["S56-M-0058-INTAKE-ACTION-LEAN-PROBE"]["stdout_sha256"]
    )

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
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

    print("intake invariant check: ok (THM-M-0058 planned; H1/M4/R4 provisional; six open tasks)")


if __name__ == "__main__":
    main()
