#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0290."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0290"
ITEM_ID = "S56-M-0290-INTAKE"
RANK = 1296
BASE_REVISION = "f294137feee7840fd105a4d3f6073d5cf45508ea"
BASE_TREE = "234b8f273d252c2c42ce6860315ed973049c871a"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_BLOCK_SHA256 = "f929da8b6b10af1926974b81d7291945c69d197f490529a56319c2915bc2ac9b"
STAGE0_BLOCK_SHA256 = "12e41b9961e35b734e8adb32764fc54de504326e9822d71e910f7fc0f933c7b8"
TARGET_BLOCK_SHA256 = "20e2ed703ecfabbf8f0ec31f47941de59f006b854a9548099f4dbe188c98e5ac"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
EXTERNAL_CARLESON_REVISION = "80e151dff5ddce2426079ec6392616496a4ec927"
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
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def attested_input_sha256(relative: str, master_replay: bool) -> str:
    if master_replay and relative == "Docs/Stage1_Execution_DAG_rev-5.6.json":
        data = subprocess.check_output(
            ["git", "show", f"{BASE_REVISION}:{relative}"], cwd=ROOT
        )
        return hashlib.sha256(data).hexdigest()
    return sha256(ROOT / relative)


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
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_receipt_inputs(receipt: dict, master_replay: bool) -> None:
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{attested_input_sha256(relative, master_replay)}", (
            f"stale receipt input hash: {relative}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--master-replay", action="store_true")
    args = parser.parse_args()
    assert not (args.worker_packet and args.master_replay), "choose worker packet or master replay"

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_receipt_inputs(receipt, args.master_replay)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "卡尔松-亨特定理"
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

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    if args.master_replay:
        assert item["state"] in {"[ ]", "[_]"}
    else:
        assert item["state"] == "[ ]"
    assert item["depends_on"] == []
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
    assert "does_not_select_a_binder_complete_statement" in instance["canonical_claim_status"]

    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("cat-file", "-e", f"{BASE_REVISION}^{{commit}}") == ""
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob_at_origin_commit"]
    ) == SOURCE_RECORD_BLOB
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        revisions["repository_math_source_blob_at_base"]
    )
    assert block_sha256(ROOT / "Docs/researches/math_theorems.md", 2083, 2088) == (
        revisions["repository_record_excerpt_sha256"]
    ) == SOURCE_RECORD_BLOCK_SHA256
    assert block_sha256(ROOT / "Docs/Stage0_Blueprint.md", 8008, 8033) == (
        revisions["stage0_excerpt_sha256"]
    ) == STAGE0_BLOCK_SHA256
    assert block_sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json", 19451, 19463) == (
        revisions["target_manifest_excerpt_sha256"]
    ) == TARGET_BLOCK_SHA256
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == attested_input_sha256(relative, args.master_replay), (
            f"stale source hash: {field}"
        )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"
    assert revisions["mathlib_addcircle_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/Fourier/AddCircle.lean"
    )
    assert revisions["external_carleson_revision"] == EXTERNAL_CARLESON_REVISION
    assert revisions["external_carleson_bibliography_sha256"] == (
        receipt["worker_input_hashes"]["external_carleson_bibliography_sha256"]
    ) == "0974024f446ede17cc12e71dd9db10008775d9bb1f7c2cf8c1cf5bf74c30b0ad"
    assert revisions["external_carleson_hunt_source_sha256"] == (
        receipt["worker_input_hashes"]["external_carleson_hunt_source_sha256"]
    ) == "d9a8d0f084dd38fe383e0cee972392bb89ad52e7ebe05a9e73fd8f2abb71bf1c"
    assert revisions["external_carleson_basic_source_sha256"] == (
        receipt["worker_input_hashes"]["external_carleson_basic_source_sha256"]
    ) == "dcfd4cb122d04deb4e982ec509430385fbe4532fdfea4235ec52998adb4d364e"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0290-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
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
    assert catalog.count("**卡尔松-亨特定理**") == 1
    assert "- 提出者: Lennart Carleson/Richard Hunt" in catalog
    assert "- 时间: 1968" in catalog
    assert catalog.count("- 陈述: L^p函数的傅里叶级数几乎处处收敛") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0290 卡尔松-亨特定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0346", "THM-M-0291", "THM-M-0289"}
    formal_candidates = instance["formal_candidates_not_credited"]
    assert any(row.get("declaration") == "carleson_hunt" for row in formal_candidates)
    assert all("not credited" in row["boundary"] or "not pointwise" in row["boundary"] for row in formal_candidates)

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
    assert receipt["acceptance_authority"] == "rev-5.6 integration lane"
    assert receipt["worker_reference"] == "isolated Stage1 rev-5.6 automation clone slot46"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
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

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    ) == f"sha256:{LAKE_SYMLINK_TARGET_SHA256}"

    artifact_hashes = receipt["artifact_sha256_before_receipt"]
    assert set(artifact_hashes) == OWNED_FILES - {"intake-receipt.json"}
    for name, digest in artifact_hashes.items():
        assert digest == sha256(HERE / name), f"stale artifact hash: {name}"

    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] in {"not_required_provisional", "denied"}
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_declarations"] == []

    expected_public = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    assert set(instance["public_merge_targets"]) == expected_public
    assert len(instance["public_merge_targets"]) == len(expected_public)
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
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    mode = "master replay" if args.master_replay else "worker"
    print(f"intake invariant check: ok (THM-M-0290 planned; H1/M4/R4; six open tasks; {mode})")


if __name__ == "__main__":
    main()
