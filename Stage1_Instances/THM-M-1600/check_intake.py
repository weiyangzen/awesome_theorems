#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1600."""

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
THEOREM_ID = "THM-M-1600"
ITEM_ID = "S56-M-1600-INTAKE"
RANK = 1220
BASE_REVISION = "62fad55ced807fdc06921c45d6fcd1f9ad86a1c2"
BASE_TREE = "9d7c8fe49a4c859d90f3069dc47973ffc5ced768"
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
    "repository_cs_source_sha256": "Docs/researches/cs_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_HASHES = {
    "mathlib_language_source_sha256": "Mathlib/Computability/Language.lean",
    "mathlib_turing_computable_source_sha256": "Mathlib/Computability/TuringMachine/Computable.lean",
    "mathlib_pmf_monad_source_sha256": "Mathlib/Probability/ProbabilityMassFunction/Monad.lean",
    "mathlib_superpolynomial_decay_source_sha256": "Mathlib/Analysis/Asymptotics/SuperpolynomialDecay.lean",
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
    assert target["name"] == instance["name_zh"] == "零知识证明"
    assert target["category"] == instance["category"] == "其他重要领域 / 离散数学"
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
    assert "not_identify_one_stable_truth_valued_proposition" in instance["canonical_claim_status"]

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
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
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
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_math_source_current_blob"]
    assert git("rev-parse", "HEAD:Docs/researches/cs_theorems.md") == revisions["repository_cs_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib source hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-1600-{suffix}"
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
    assert "**零知识证明**" in catalog
    assert "- 提出者: Goldwasser/Micali/Rackoff" in catalog
    assert "- 时间: 1985" in catalog
    assert "- 陈述: 不泄露信息的证明" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1600 零知识证明" in stage0
    assert "THM-C-0181 GMR零知识定义" in stage0
    assert "THM-C-0182 GMW定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0727", "THM-C-0181", "THM-C-0182", "THM-C-0183"}

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
            continue
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "integration lane"
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

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(recipe["covered_node_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert recipes[0]["covered_declarations"] == []
    assert recipes[1]["covered_declarations"] == [
        "Language",
        "Turing.TM2ComputableInPolyTime",
        "PMF",
        "PMF.pure",
        "PMF.bind",
        "Asymptotics.SuperpolynomialDecay",
    ]

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    for field in MATHLIB_SOURCE_HASHES:
        assert worker_inputs[field] == revisions[field]

    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["axiom_and_placeholder_result"]
    assert receipt["known_failures"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("THM-M-1600 intake self-check: ok")


if __name__ == "__main__":
    main()
