#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0295."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0295"
ITEM_ID = "S56-M-0295-INTAKE"
RANK = 1299
BASE_REVISION = "940588d30669014430d5a1beb187f2bca118e816"
BASE_TREE = "42d80725ccbabcdd826ed2bc8b3622ac31ac7695"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SUCCESS = "intake invariant check: ok (THM-M-0295 planned; H1/M4/R4; six open tasks)\n"
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
MATHLIB_HASH_FIELDS = {
    "mathlib_fourier_transform_source_sha256": "Mathlib/Analysis/Fourier/FourierTransform.lean",
    "mathlib_lp_space_source_sha256": "Mathlib/Analysis/Fourier/LpSpace.lean",
    "mathlib_schwartz_fourier_source_sha256": "Mathlib/Analysis/Distribution/SchwartzSpace/Fourier.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"{path} is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_file(path.resolve())
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
    assert packet["known_failures"] == receipt["known_failures"]
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
    assert target["name"] == instance["name_zh"] == "豪斯多夫-杨不等式"
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

    items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(items) == 7
    intake_item = next(row for row in items if row["id"] == ITEM_ID)
    assert intake_item["execution_rank"] == RANK and intake_item["phase"] == "intake"
    assert intake_item["layer"] == 0 and intake_item["state"] == "[ ]"
    assert intake_item["depends_on"] == []
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
    assert "duplicate_target" in instance["canonical_claim_status"]
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
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_math_source_blob_at_base"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    for candidate in instance["bibliographic_discovery_candidates_not_credited"]:
        if "crossref_response_sha256" in candidate:
            assert re.fullmatch(r"[0-9a-f]{64}", candidate["crossref_response_sha256"])

    neighbor_ids = [row["theorem_id"] for row in instance["neighbor_target_boundaries"]]
    assert len(neighbor_ids) == len(set(neighbor_ids))
    target_by_id = {row["theorem_id"]: row for row in manifest["targets"]}
    for neighbor in instance["neighbor_target_boundaries"]:
        assert target_by_id[neighbor["theorem_id"]]["name"] == neighbor["name"]

    expected = []
    dependency = ITEM_ID
    authoritative = {row["id"]: row for row in items}
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0295-{suffix}"
        expected.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        auth = authoritative[task_id]
        assert task["phase"] == auth["phase"] and task["layer"] == auth["layer"]
        assert task["deliverable"] == auth["deliverable"]
        assert task["completion_gate"] == auth["completion_gate"]
        assert task["owned_paths"] == auth["owned_paths"]
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for marker in (
        "**豪斯多夫-杨不等式**",
        "- 陈述: 傅里叶变换的L^p估计",
        "**豪斯多夫-杨定理**",
        "- 陈述: 傅里叶变换的范数不等式",
    ):
        assert marker in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0295 豪斯多夫-杨不等式" in stage0
    assert "THM-M-0103 豪斯多夫-杨定理" in stage0
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for marker in ("THM-M-0103", "10.1007/BF01175679", "10.1112/plms/s2-12.1.71", "H1"):
        assert marker in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for name in actual_files:
        check_text_file(HERE / name)
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected_hash in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected_hash == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected_hash, f"stale owned hash: {relative}"

    assert receipt["worker_packet_sha256"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["selftest_result"] == "pass"
    assert receipt["known_failures"] and receipt["first_failed_gate"].startswith("S56-M-0295-STATEMENT")

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print(SUCCESS, end="")


if __name__ == "__main__":
    main()
