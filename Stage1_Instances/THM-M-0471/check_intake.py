#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0471."""

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
THEOREM_ID = "THM-M-0471"
ITEM_ID = "S56-M-0471-INTAKE"
RANK = 1353
BASE_REVISION = "8a13381618b241479a4786ca67704af7322f77aa"
BASE_TREE = "0cc75f807f4c75d2a0aa8a72062e025083bd18ad"
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
    "mathlib_nat_factors_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Nat/Factors.lean"
    ),
    "mathlib_nat_factorization_defs_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Nat/Factorization/Defs.lean"
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert len(targets) == 1
    target = targets[0]
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "算术基本定理",
        "category": "数论 / 初等数论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    assert canonical_sha256(target) == instance["source_revisions"]["target_entry_canonical_sha256"]

    authoritative_intakes = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(authoritative_intakes) == 1
    intake_item = authoritative_intakes[0]
    assert intake_item["theorem_id"] == THEOREM_ID
    assert intake_item["execution_rank"] == RANK
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] == "[ ]" and intake_item["depends_on"] == []
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake_item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["execution_rank"] == RANK
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []

    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    assert formal["module"] is None
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is None
    assert formal["environment_fingerprint"] is None
    assert formal["gate_state"] == "open_pending_statement_phase"
    assert len(instance["ordered_binders"]) == 4
    assert len(instance["alternate_encodings"]) == 3
    assert all(row["checked_witness"] is None for row in instance["alternate_encodings"])
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == (
        "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    )
    assert revisions["repository_source_record_blob"] == (
        "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
    )
    assert revisions["repository_record_excerpt_sha256"] == (
        "bceb698f679a295016ac8f0b3528128bc1d729613e8184892d4ba4a42868283d"
    )
    assert revisions["stage0_projection_excerpt_sha256"] == (
        "26c58f00783669a4f1ebc5c1170eb6ae6929db21604cb11acafa08ae862e8b14"
    )
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0471-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**算术基本定理**") == 1
    assert "- 提出者: 欧几里得" in catalog
    assert "- 时间: 约公元前300年" in catalog
    assert catalog.count("- 陈述: 大于1的整数可唯一分解为素数乘积") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0471 算术基本定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    factors_source = (mathlib / "Mathlib/Data/Nat/Factors.lean").read_text(encoding="utf-8")
    assert "/-- **Fundamental theorem of arithmetic** -/" in factors_source
    assert "theorem primeFactorsList_unique" in factors_source
    factorization_source = (
        mathlib / "Mathlib/Data/Nat/Factorization/Defs.lean"
    ).read_text(encoding="utf-8")
    assert "theorem prod_factorization_pow_eq_self" in factorization_source
    assert "def factorizationEquiv" in factorization_source

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    status_paths = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    assert status_paths == expected_changed | {"Formalizations/Lean/.lake"}

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["selftest_result"] == "pass"
    for relative, tagged_hash in receipt["source_inputs"].items():
        assert tagged_hash == f"sha256:{sha256(ROOT / relative)}"
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0471 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
