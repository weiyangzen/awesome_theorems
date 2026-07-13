#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0302."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-0302"
ITEM_ID = "S56-M-0302-INTAKE"
BASE = "940588d30669014430d5a1beb187f2bca118e816"
BASE_TREE = "42d80725ccbabcdd826ed2bc8b3622ac31ac7695"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "08909af0054f54d0ac8dd28ad295b87428595d89c3266da6a09653573f4ac458",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "cecbf4cd9e214c479597683c5ffa4c49a4635e198b96563a327df34cc45886a3",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = REPO) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_packet(path: Path, receipt: dict) -> None:
    packet = load(path if path.is_absolute() else REPO / path)
    required = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert required <= packet.keys()
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and command["argv"]
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert packet["accepted_receipt_ids"] == []
    assert packet["root_vector_after"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["owner"] == "Stage1 integration lane"
    assert packet["support_state"] == "provisional_worker_only"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(REPO / "Docs/Stage1_Targets_rev-5.6.json")
    authority = load(REPO / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(OWNED / "instance.json")
    dag = load(OWNED / "task-dag.json")
    receipt = load(OWNED / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == 1305
    assert target["name"] == instance["name_zh"] == "约翰-尼伦伯格不等式"
    assert target["category"] == instance["category_zh"] == "分析学 / 实分析"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    item = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1305
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

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
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_blob_at_origin"] == SOURCE_BLOB
    assert excerpt_sha256(REPO / "Docs/researches/math_theorems.md", 2167, 2172) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_sha256(REPO / "Docs/Stage0_Blueprint.md", 8332, 8357) == revisions["stage0_excerpt_sha256"]
    assert excerpt_sha256(REPO / "Docs/Stage1_Targets_rev-5.6.json", 19585, 19598) == revisions["target_manifest_excerpt_sha256"]
    assert excerpt_sha256(REPO / "Docs/researches/math_theorems.md", 1829, 1834) == revisions["neighbor_repository_record_excerpt_sha256"]
    assert excerpt_sha256(REPO / "Docs/Stage0_Blueprint.md", 7031, 7056) == revisions["neighbor_stage0_excerpt_sha256"]
    assert revisions["mathlib"] == MATHLIB and revisions["mathlib_tree"] == MATHLIB_TREE

    for relative, expected in SOURCE_HASHES.items():
        assert sha256(REPO / relative) == expected, f"stale pinned input: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"

    suffixes = ["STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF", "VALIDATION", "RELEASE"]
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(suffixes, start=1):
        task_id = f"S56-M-0302-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authoritative_task = next(row for row in authority["items"] if row["id"] == task_id)
        assert task["phase"] == authoritative_task["phase"]
        assert task["layer"] == authoritative_task["layer"] == layer
        assert task["owned_paths"] == authoritative_task["owned_paths"]
        assert task["deliverable"] == authoritative_task["deliverable"]
        assert task["completion_gate"] == authoritative_task["completion_gate"]
        assert task["authoritative_state"] == authoritative_task["state"] == "[ ]"
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])

    actual_files = {path.name for path in OWNED.iterdir() if path.is_file()}
    assert actual_files == OWNED_FILES == set(instance["owned_artifacts"])
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert all((REPO / relative).is_file() for relative in instance["public_merge_targets"])
    assert set(receipt["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(OWNED / name) == expected, f"owned artifact hash mismatch: {name}"
    for path in OWNED.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at <= validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["covered_task_ids"] == receipt["covered_node_ids"] == [ITEM_ID]
    for field in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
    ):
        assert receipt[field] == []
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert len(receipt["structured_validation_recipes"]) == 2
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["observed_exit"] == recipe["expected_exit"] == 0
        assert recipe["stdout_sha256"].startswith("sha256:")
        assert recipe["stderr_sha256"].startswith("sha256:")

    lake_target = (REPO / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        public_text = (OWNED / name).read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    if args.worker_packet is not None:
        check_packet(args.worker_packet, receipt)

    print("THM-M-0302 intake invariant check: ok (planned H1/M4/R4; six downstream tasks open)")


if __name__ == "__main__":
    main()
