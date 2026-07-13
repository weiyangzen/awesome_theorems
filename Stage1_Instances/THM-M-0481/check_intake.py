#!/usr/bin/env python3
"""Scoped structural validator for the THM-M-0481 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0481"
ITEM_ID = "S56-M-0481-INTAKE"
RANK = 1362
BASE_REVISION = "bd80ad137c187dda02bcfcb2529360ef6d9b53eb"
BASE_TREE = "65fb1d54476897700b46e671380377bdd27c4e0b"
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
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    assert target["name"] == instance["name_zh"] == "伯特兰假设"
    assert target["category"] == instance["category"] == "数论 / 初等数论"
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
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert manifest["scope"]["canonical_sorted_target_id_set_sha256"] == revisions["target_id_set_sha256"]
    assert execution["target_id_set_sha256"] == revisions["target_id_set_sha256"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    bertrand = mathlib / "Mathlib/NumberTheory/Bertrand.lean"
    assert revisions["bertrand_source_sha256"] == sha256(bertrand)
    assert git("rev-parse", "HEAD:Mathlib/NumberTheory/Bertrand.lean", cwd=mathlib) == revisions["bertrand_source_blob"]

    suffixes = ("STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF", "VALIDATION", "RELEASE")
    dependency = ITEM_ID
    expected = []
    for suffix in suffixes:
        task_id = f"S56-M-0481-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        expected.append(
            (
                task_id,
                authoritative["phase"],
                authoritative["layer"],
                [dependency],
                "open",
                authoritative["owned_paths"],
                authoritative["deliverable"],
                authoritative["completion_gate"],
                [],
            )
        )
        dependency = task_id
    assert [
        (
            row["id"],
            row["phase"],
            row["layer"],
            row["depends_on"],
            row["state"],
            row["owned_paths"],
            row["deliverable"],
            row["completion_gate"],
            row["evidence_ids"],
        )
        for row in dag["tasks"]
    ] == expected

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**伯特兰假设**" in catalog
    assert "- 提出者: Joseph Bertrand" in catalog
    assert "- 时间: 1845" in catalog
    assert "- 陈述: n与2n之间必有素数" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0481 伯特兰假设" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [row["id"] for row in dag["tasks"]]

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert "#check Nat.exists_prime_lt_and_le_two_mul" in probe
    assert "#check Nat.bertrand" in probe
    assert "#check Nat.exists_prime_lt_and_le_two_mul_eventually" in probe
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert not any(token in probe for token in forbidden)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in ("README.md", "instance.json", "intake-receipt.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet:
        packet = load(args.worker_packet.resolve())
        assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
        assert packet["intent"] == "intake" and packet["state"] == "[_]"
        assert packet["verdict"] == "no_state_change"
        assert packet["base_revision"] == BASE_REVISION and packet["base_tree"] == BASE_TREE
        assert set(packet["changed_paths"]) == expected_changed
        assert packet["receipt_id"] == receipt["receipt_id"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["accepted_receipt_ids"] == []
        assert packet["audit_complete"] is packet["theorem_complete"] is False

    print("THM-M-0481 intake invariant check: ok (planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
