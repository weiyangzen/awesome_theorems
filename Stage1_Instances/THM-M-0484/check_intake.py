#!/usr/bin/env python3
"""Validate the THM-M-0484 planned dossier through its statement proposal."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0484"
ITEM_ID = "S56-M-0484-INTAKE"
RANK = 1365
BASE_REVISION = "2226f559136f12fde46b1bf73cdf629043b8a648"
BASE_TREE = "33cb254ed06b1391379b8e7f88c5e23188957b62"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
NECESSITY_ORIGIN = "9067089938d4c3675c1193f1b6e8378620ea611a"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
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
    "check_statement_artifacts.py",
    "statement.json",
    "statement-receipt.json",
    "statement-validation.md",
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
PROBE_DECLARATIONS = [
    "mersenne",
    "LucasLehmer.s",
    "LucasLehmer.sZMod",
    "LucasLehmer.sMod",
    "LucasLehmer.lucasLehmerResidue",
    "LucasLehmer.LucasLehmerTest",
    "lucas_lehmer_sufficiency",
    "lucas_lehmer_necessity",
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
    "mathlib_lucas_lehmer_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/LucasLehmer.lean"
    ),
    "mathlib_mersenne_examples_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Archive/Examples/MersennePrimes.lean"
    ),
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
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
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]


def check_authorities(instance: dict, dag: dict) -> list[dict]:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["scope"]["covered_targets"] == 1546
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "卢卡斯-莱默检验",
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
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
    ):
        assert instance[field] == target[field]
    assert instance["theorem_complete"] is target["theorem_complete"] is False
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]

    items = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": RANK,
        "phase": "intake",
        "layer": 0,
        "state": "[_]",
        "depends_on": [],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
        "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 1,
        "children": [],
    }

    dependency = ITEM_ID
    assert len(dag["tasks"]) == 6
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), start=1):
        task_id = f"S56-M-0484-{suffix}"
        authoritative = next(row for row in items if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        for field in ("owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authoritative[field]
        dependency = task_id
    return items


def check_instance(instance: dict, dag: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"].startswith("For every natural p with 3 <= p")
    formal = instance["canonical_formal_target"]
    assert formal["module"] == f"Stage1_Instances/{THEOREM_ID}/Statement.lean"
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0484.LucasLehmerTestTarget"
    )
    assert formal["elaborated_expression_hash"] == (
        "sha256:6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
    )
    assert formal["environment_fingerprint"] is not None
    assert formal["module_candidates"] == ["Mathlib.NumberTheory.LucasLehmer"]
    assert formal["declaration_candidates"] == PROBE_DECLARATIONS
    assert formal["candidate_expression"].startswith("forall p : Nat, 3 <= p")
    assert instance["ordered_binders"] == ["p : Nat", "hp : 3 <= p"]
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["root_vector_status"] == (
        "provisional_intake_classification_pending_master_acceptance"
    )
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is False
    assert "exact statement proposal" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        if relative.startswith("Formalizations/Lean/.lake/"):
            assert revisions[field] == sha256(ROOT / relative), f"stale dependency hash: {field}"
            continue
        base_bytes = subprocess.check_output(
            ["git", "show", f"{BASE_REVISION}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
        )
        assert revisions[field] == hashlib.sha256(base_bytes).hexdigest(), (
            f"integrated intake source snapshot changed: {field}"
        )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert git("rev-parse", "HEAD:Mathlib/NumberTheory/LucasLehmer.lean", cwd=mathlib) == revisions[
        "mathlib_lucas_lehmer_blob"
    ]
    assert git("rev-parse", "HEAD:Archive/Examples/MersennePrimes.lean", cwd=mathlib) == revisions[
        "mathlib_mersenne_examples_blob"
    ]
    assert git("cat-file", "-e", f"{NECESSITY_ORIGIN}^{{commit}}", cwd=mathlib) == ""
    assert git("rev-parse", f"{NECESSITY_ORIGIN}^{{tree}}", cwd=mathlib) == revisions[
        "mathlib_necessity_origin_tree"
    ]
    assert git(
        "rev-parse", f"{NECESSITY_ORIGIN}:Mathlib/NumberTheory/LucasLehmer.lean", cwd=mathlib
    ) == revisions["mathlib_necessity_origin_blob"]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**卢卡斯-莱默检验**") == 1
    assert catalog.count("- 提出者: Édouard Lucas/Derrick Lehmer") == 1
    assert catalog.count("- 时间: 1930") >= 1
    assert catalog.count("- 陈述: 梅森素数的快速检验") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0484 卢卡斯-莱默检验" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0483",
        "THM-M-0405",
    }


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    for key in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["dirty_input_evidence"]["preexisting_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    for relative, tagged_digest in receipt["source_inputs"].items():
        base_bytes = subprocess.check_output(
            ["git", "show", f"{BASE_REVISION}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
        )
        assert tagged_digest == f"sha256:{hashlib.sha256(base_bytes).hexdigest()}"
    recipes = receipt["structured_validation_recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0484-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0484-INTAKE-RECIPE-LEAN-PROBE",
    }
    for recipe in recipes:
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_node_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
    lean_recipe = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("LEAN-PROBE"))
    assert lean_recipe["covered_declarations"] == PROBE_DECLARATIONS
    result = subprocess.run(
        lean_recipe["argv"],
        cwd=ROOT / lean_recipe["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=lean_recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == lean_recipe["expected_exit"] == 0
    assert hashlib.sha256(result.stdout).hexdigest() == (
        "27164568a5367c07303ed7d023ea02af91721972fb6bae221a212b7a5519031a"
    )


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES
    assert set(instance["owned_artifacts"]) == actual
    intake_files = actual - {
        "Statement.lean",
        "check_statement.py",
        "check_statement_artifacts.py",
        "statement.json",
        "statement-receipt.json",
        "statement-validation.md",
    }
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(intake_files)
    ]
    assert receipt["changed_paths"] == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in intake_files}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            base_bytes = subprocess.check_output(
                ["git", "show", f"HEAD:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
            )
            assert hashlib.sha256(base_bytes).hexdigest() == expected, (
                f"integrated intake snapshot hash changed: {relative}"
            )
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_authorities(instance, dag)
    check_instance(instance, dag)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-0484 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
