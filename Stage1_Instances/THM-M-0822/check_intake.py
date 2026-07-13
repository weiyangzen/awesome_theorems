#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0822."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0822"
ITEM_ID = "S56-M-0822-INTAKE"
RANK = 1380
BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
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
    "mathlib_kruskal_katona_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SetFamily/KruskalKatona.lean",
    "mathlib_intersecting_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SetFamily/Intersecting.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def excerpt_hash(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    data = ("\n".join(lines[start - 1:end]) + "\n").encode()
    return hashlib.sha256(data).hexdigest()


def ekr_source_block_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index("/-- The **Erdős–Ko–Rado theorem**.")
    end = text.index("\nend Finset", start)
    return hashlib.sha256((text[start:end] + "\n").encode()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
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
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Erdős-Ko-Rado定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
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
    assert formal["declaration_candidate"] == "Finset.erdos_ko_rado"
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    catalog_path = ROOT / "Docs/researches/math_theorems.md"
    assert revisions["repository_record_excerpt_sha256"] == excerpt_hash(catalog_path, 6040, 6045)
    assert revisions["repository_duplicate_excerpt_sha256"] == excerpt_hash(catalog_path, 7036, 7041)
    assert revisions["repository_record_excerpt_sha256"] == revisions["repository_duplicate_excerpt_sha256"]
    assert revisions["stage0_excerpt_sha256"] == excerpt_hash(ROOT / "Docs/Stage0_Blueprint.md", 22442, 22467)
    assert revisions["mathlib_ekr_source_block_sha256"] == ekr_source_block_hash(
        ROOT / SOURCE_HASHES["mathlib_kruskal_katona_sha256"]
    )
    assert revisions["primary_source"]["observed_pdf_sha256"] == (
        "e53f1ec72accc8e55ec8da360588b224542a9133216d4b82a6918bbe309ac821"
    )

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0822-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["theorem_id"] == THEOREM_ID and task["execution_rank"] == RANK
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["attempts"] == authoritative["attempts"] == 0
        assert task["children"] == authoritative["children"] == []
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = catalog_path.read_text(encoding="utf-8")
    assert catalog.count("**Erdős-Ko-Rado定理**") == 2
    assert catalog.count("- 提出者: Erdős/Ko/Rado") == 2
    assert catalog.count("- 时间: 1961") >= 2
    assert catalog.count("- 陈述: 相交族的最大大小") == 2
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0822 Erdős-Ko-Rado定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0

    dirty = receipt["dirty_input_evidence"]
    artifact_hashes = dirty["owned_and_packet_sha256"]
    assert set(artifact_hashes) == set(receipt["changed_paths"])
    receipt_path = f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    assert artifact_hashes[receipt_path] == "self_referential_excluded"
    snapshot_lines = []
    for relative in sorted(receipt["changed_paths"]):
        if relative == receipt_path:
            continue
        observed = sha256(ROOT / relative)
        assert artifact_hashes[relative] == observed, f"stale worker artifact hash: {relative}"
        snapshot_lines.append(f"{observed}  {relative}\n")
    assert dirty["canonical_snapshot_sha256"] == sha256_bytes("".join(snapshot_lines).encode())
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT
    )
    assert dirty["git_status_porcelain_v1_sha256"] == sha256_bytes(status)

    outputs = receipt["validation_output_hashes"]
    empty_sha256 = sha256_bytes(b"")
    checker_line = b"intake invariant check: ok (THM-M-0822 planned; H1/M3/R4; six open tasks)\n"
    assert outputs["intake_checker_worker_stdout_sha256"] == sha256_bytes(checker_line)
    assert outputs["intake_checker_public_stdout_sha256"] == sha256_bytes(checker_line)
    assert outputs["intake_checker_stderr_sha256"] == empty_sha256
    assert outputs["lean_probe_stdout_sha256"] == (
        "d83eb287bde141cbe259daedb12cae423ad9c80ece8f00e2e27ddbe8efec9f21"
    )
    assert outputs["lean_probe_stderr_sha256"] == empty_sha256
    assert outputs["prohibited_scan_stdout_sha256"] == empty_sha256
    assert outputs["whitespace_checks_stdout_sha256"] == empty_sha256
    assert outputs["pinned_mathlib_status_stdout_sha256"] == empty_sha256
    assert outputs["stage1_standard_stdout_sha256"] == (
        "5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf"
    )
    assert outputs["target_check_stdout_sha256"] == (
        "dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd"
    )
    assert outputs["target_show_stdout_sha256"] == (
        "76d8bce733a2bf575810e74cbcafbc52eb19035d911009e8939e64b55e28861e"
    )
    assert outputs["git_revision_stdout_sha256"] == (
        "0fc5722fef206591d812d4094cc7b75d28c9d6f34e4b38d9951a78695b843d1c"
    )
    assert outputs["lean_version_stdout_sha256"] == (
        "ac621a3ad32f6ec6565dfbd280c238851658a370c170ad3a695571907d1a90f4"
    )
    assert outputs["lake_version_stdout_sha256"] == (
        "7e442087d756927b66453c9939f901a37864f4eb82b47cf88739ac45e24905bc"
    )
    assert outputs["mathlib_revision_stdout_sha256"] == (
        "3f0d75e7a3a904eec609d05de5b6c5d89615885506b78fa6cec14e05da4ff8d7"
    )

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    assert worker_inputs["mathlib_kruskal_katona_sha256"] == revisions["mathlib_kruskal_katona_sha256"]
    assert worker_inputs["mathlib_ekr_source_block_sha256"] == revisions["mathlib_ekr_source_block_sha256"]
    assert worker_inputs["primary_source_pdf_sha256"] == revisions["primary_source"]["observed_pdf_sha256"]
    assert worker_inputs["primary_source_archive_index_sha256"] == (
        revisions["primary_source"]["observed_archive_index_sha256"]
    )
    assert worker_inputs["primary_source_text_sha256"] == revisions["primary_source"]["observed_text_sha256"]
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"{path.name} is missing a final newline"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"{path.name} has trailing whitespace"
        )

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0822 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
