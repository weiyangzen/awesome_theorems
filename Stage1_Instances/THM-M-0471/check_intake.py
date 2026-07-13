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
HANDOFF_ITEM_ID = "S56-M-0471-STATEMENT"
RANK = 1353
BASE_REVISION = "8a13381618b241479a4786ca67704af7322f77aa"
BASE_TREE = "0cc75f807f4c75d2a0aa8a72062e025083bd18ad"
HANDOFF_BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
HANDOFF_BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
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
    "Statement.lean",
    "check_statement.py",
    "statement.json",
    "statement-receipt.json",
    "statement-validation.md",
    "AnchorAudit.lean",
    "anchor-audit.json",
    "check_anchor_audit.py",
    "anchor-audit-validation.md",
    "anchor-audit-receipt.json",
    "anchor-discovery-protocol.json",
    "ObligationTree.lean",
    "build_obligation_artifacts.py",
    "check_obligation_tree.py",
    "obligation-registry.json",
    "typed-graphs.json",
    "validation-specs.json",
    "obligation-tree.md",
    "obligation-tree-validation.md",
    "obligation-tree-receipt.json",
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
    assert packet["item_id"] in {
        HANDOFF_ITEM_ID,
        "S56-M-0471-ANCHOR_AUDIT",
        "S56-M-0471-OBLIGATION_TREE",
    }
    assert packet["state"] == "[_]"
    if packet["item_id"] == HANDOFF_ITEM_ID:
        assert packet["base_revision"] == HANDOFF_BASE_REVISION
        statement_receipt = load(HERE / "statement-receipt.json")
        assert set(packet["changed_paths"]) == set(statement_receipt["changed_paths"])
        assert packet["commands"] == statement_receipt["commands_and_results"]
        assert packet["output_summary"] == statement_receipt["output_summary"]
        assert packet["known_failures"] == statement_receipt["known_failures"]


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
    assert intake_item["state"] == "[_]" and intake_item["depends_on"] == []
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
    assert formal["module"] == f"Stage1_Instances/{THEOREM_ID}/Statement.lean"
    assert formal["minimal_imports"] == ["Mathlib.Data.Nat.Prime.Defs"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget"
    )
    assert formal["elaborated_expression_hash"].startswith("sha256:")
    assert formal["environment_fingerprint"]
    assert formal["gate_state"] == "self_tested_pending_master_acceptance"
    assert len(instance["ordered_binders"]) == 4
    assert len(instance["alternate_encodings"]) == 4
    checked = [row for row in instance["alternate_encodings"] if row["checked_witness"]]
    assert checked == [{
        "target": "Stage1Instances.THM_M_0471.ExpandedPrimeListTarget",
        "relationship": "iff",
        "checked_witness": (
            "Stage1Instances.THM_M_0471."
            "fundamentalTheoremOfArithmeticTarget_iff_expanded"
        ),
    }]
    assert instance["obligation_registry_hash"] == (
        "sha256:d3f11762e2a0f4c384d094d53e44100f20a21f81eb6ce527cd5f9897a9bc445c"
    )
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
    mutable_authorities = {
        "authoritative_blueprint_sha256",
        "execution_dag_sha256",
    }
    for field, relative in SOURCE_HASHES.items():
        if field in mutable_authorities:
            assert revisions[field], f"missing historical source hash: {field}"
        else:
            assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    assert git("rev-parse", "HEAD") == "5fe11f4b5e32a06ffb4432460319fc8ae906fe7b"
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
    # Downstream phases append owned artifacts; their scoped checkers bind the current worktree.

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
        if relative in {
            "Docs/Stage1_Blueprint_rev-5.6.md",
            "Docs/Stage1_Execution_DAG_rev-5.6.json",
        }:
            continue
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

    print("dossier invariant check: ok (THM-M-0471 exact statement; H1/M3/R4; tasks open)")


if __name__ == "__main__":
    main()
