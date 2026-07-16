#!/usr/bin/env python3
"""Validate the rev-5.6 planned intake for THM-M-0387."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0387"
ITEM_ID = "S56-M-0387-INTAKE"
BASE_REVISION = "c5037228977a81948bbd6119e1728b4b65b9924e"
BASE_TREE = "78b2627e717156dffe240bea12d14205af667d2a"
GRAPH_SHA256 = "fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518"
CONTEXT_SHA256 = "90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
SHARED_GROUPS = [
    "SHARED-MODULE-12060056b1f9fd84",
    "SHARED-MODULE-2884526d078231ae",
    "SHARED-MODULE-4f11ecbb9eb91fb0",
    "SHARED-MODULE-97c08d929c8c634f",
    "SHARED-MODULE-d59c2e49212cb785",
]
ROLE_PATHS = {
    "instance_manifest": "Stage1_Instances/THM-M-0387/intake.json",
    "scope_map": "Stage1_Instances/THM-M-0387/scope-map.md",
    "source_crosswalk": "Stage1_Instances/THM-M-0387/source-statement-crosswalk.md",
    "open_task_dag": "Stage1_Instances/THM-M-0387/task-dag.json",
    "phase_receipt": "Stage1_Instances/THM-M-0387/intake-receipt.json",
}
PHASES = (
    ("STATEMENT", "statement"),
    ("ANCHOR_AUDIT", "anchor_audit"),
    ("OBLIGATION_TREE", "obligation_tree"),
    ("PROOF", "proof"),
    ("VALIDATION", "validation"),
    ("RELEASE", "release"),
)
SEMANTIC = {
    "schema_version": "stage1-validator-semantic-result/1.0",
    "item_id": ITEM_ID,
    "theorem_id": THEOREM_ID,
    "phase": "intake",
    "status": "passed",
    "verdict": "phase_accepted",
    "phase_accepted": True,
    "audit_complete": False,
    "theorem_complete": False,
    "phase_predicate_proven": True,
    "first_failed_gate": None,
    "open_obligations": 0,
    "stale_inputs": [],
    "blocked": False,
}


def load(relative: str) -> dict:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{relative} must contain a JSON object"
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check() -> None:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    instance = load(ROLE_PATHS["instance_manifest"])
    task_dag = load(ROLE_PATHS["open_task_dag"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0387/dependency-reuse-ledger.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == 1
    assert target["legacy_priority_slot"] == instance["legacy_priority_slot"] == "S1-M-001"
    assert target["name"] == instance["name_zh"] == "费马大定理"
    assert target["category"] == instance["category"] == "数论 / 丢番图方程"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 279
    assert target["source_status_untrusted"] == instance["source_status_untrusted"]
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    authoritative = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert authoritative["theorem_id"] == THEOREM_ID
    assert authoritative["phase"] == "intake" and authoritative["layer"] == 0
    assert authoritative["state"] == "[_]" and authoritative["attempts"] == 1
    assert authoritative["depends_on"] == []
    assert authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert authoritative["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert authoritative["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 1 and node["topological_layer"] == 0
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == []
    assert sorted(node["shared_lemma_group_ids"]) == SHARED_GROUPS
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert sha256("Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256

    phase_contract = next(row for row in contract["phases"] if row["phase"] == "intake")
    assert contract["schema_version"] == "stage1-phase-acceptance-contracts/1.0"
    assert sha256("Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256
    assert phase_contract["intent"] == "intake" and phase_contract["layer"] == 0
    assert phase_contract["worker_verdicts_eligible_for_review"] == [
        "accepted", "no_state_change"
    ]
    assert phase_contract["phase_acceptance_does_not_claim"] == [
        "exact_statement_accepted", "proof_credit", "audit_complete", "theorem_complete"
    ]
    selected = {
        row["role"]: next(path for path in row["path_candidates"] if (ROOT / path.format(theorem_id=THEOREM_ID)).is_file()).format(theorem_id=THEOREM_ID)
        for row in phase_contract["required_artifact_roles"]
    }
    assert selected == ROLE_PATHS
    assert [row["path_pattern"] for row in phase_contract["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_intake.py"
    ]

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["item_id"] == ITEM_ID and instance["intent"] == "intake"
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["canonical_statement"] and instance["domain_and_universes"]
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4" and formal["module"] == "Mathlib.NumberTheory.FLT.Basic"
    assert formal["declaration_or_expression"] == "FermatLastTheorem"
    assert formal["elaborated_expression_hash"] is None
    assert formal["environment_fingerprint"] is None
    assert formal["gate_state"] == "open_pending_statement_phase" and formal["open_boundary"]
    assert instance["ordered_binders"] == ["n : Nat", "x : Nat", "y : Nat", "z : Nat"]
    assert instance["quantifiers"] and len(instance["hypotheses"]) == 4
    assert instance["conclusion"] == "x ^ n + y ^ n != z ^ n"
    assert len(instance["alternate_encodings"]) == 4
    assert all(row["checked_witness"] is None for row in instance["alternate_encodings"])
    assert instance["candidate_encodings_not_credited"] is True
    assert instance["excluded_degenerate_cases"]
    for profile in ("foundation_profile", "tcb_profile", "computation_profile"):
        assert isinstance(instance[profile], dict) and instance[profile].get("profile_id")
    assert instance["formal_system"]["toolchain_file"] == "Formalizations/Lean/lean-toolchain"
    assert instance["source_revisions"]["repository_base"] == BASE_REVISION
    assert instance["source_revisions"]["repository_base_tree"] == BASE_TREE
    revision_paths = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "v2_blueprint_sha256": "Docs/Stage1_Blueprint_v2.md",
        "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
        "phase_contract_sha256": "Docs/Stage1_Phase_Acceptance_Contracts.json",
        "theorem_dag_sha256": "Docs/Stage1_Theorem_DAG_v2.json",
        "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
        "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
        "repository_math_source_sha256": "Docs/researches/math_theorems.md",
        "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
        "mathlib_flt_basic_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/FLT/Basic.lean",
    }
    for field, relative in revision_paths.items():
        assert instance["source_revisions"][field] == sha256(relative)
    assert instance["source_revisions"]["repository_source_record_blob"] == git(
        "rev-parse", f"{BASE_REVISION}:Docs/researches/math_theorems.md"
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == instance["source_revisions"]["mathlib"]
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == instance["source_revisions"]["mathlib_tree"]
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["downstream_blockers"] and instance["status_boundary"]
    assert instance["owners_and_reviewers"]["acceptance_owner"] == "Stage1 integration lane"
    freshness = instance["freshness_and_revocation_policy"]
    assert freshness["review_due"] and freshness["invalidation_inputs"] and freshness["incident_path"]

    expected_tasks = []
    predecessor = ITEM_ID
    for layer, (suffix, phase) in enumerate(PHASES, start=1):
        task_id = f"S56-M-0387-{suffix}"
        row = next(task for task in task_dag["tasks"] if task["id"] == task_id)
        authority = next(task for task in execution["items"] if task["id"] == task_id)
        assert row["phase"] == authority["phase"] == phase
        assert row["layer"] == authority["layer"] == layer
        assert row["depends_on"] == [predecessor]
        assert row["owned_paths"] == authority["owned_paths"]
        assert row["deliverable"] == authority["deliverable"]
        assert row["completion_gate"] == authority["completion_gate"]
        assert row["state"] == "open" and row["evidence_ids"] == []
        expected_tasks.append(task_id)
        predecessor = task_id
    assert task_dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert task_dag["theorem_id"] == THEOREM_ID
    assert task_dag["lifecycle_mode"] == "planned"
    assert task_dag["accepted_states"] == [] and task_dag["theorem_complete"] is False
    assert [row["id"] for row in task_dag["tasks"]] == expected_tasks

    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    assert ledger["direct_parent_ids"] == ledger["transitive_ancestor_ids"] == []
    assert ledger["hard_edge_ids"] == ledger["reuse_hint_ids"] == []
    assert ledger["shared_group_ids"] == SHARED_GROUPS
    assert ledger["inspections"] == [] and ledger["unresolved_compatibility_obligations"] == []
    decisions = ledger["reuse_decisions"]
    assert [row["source_id"] for row in decisions] == SHARED_GROUPS
    assert all(row["provider_theorem_id"] == "THM-M-0133" for row in decisions)
    assert all(row["decision"] == "not_applicable" for row in decisions)
    assert all(row["context_digest"] == CONTEXT_SHA256 for row in decisions)
    assert all(row["non_reuse_reason"] for row in decisions)
    for row in decisions:
        for relative, digest in row["inspected_member_artifacts"].items():
            assert relative.startswith("Stage1_Instances/THM-M-0133/")
            assert digest == sha256(relative)
    assert ledger["closure_audit"]["parent_inspection_order"] == []

    scope = (ROOT / ROLE_PATHS["scope_map"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    assert "all-exponent root" in scope and "Out of scope" in scope
    assert "n = 3" in scope and "regular primes" in scope
    assert "Repository source record" in crosswalk and "Exact-statement choices still open" in crosswalk
    assert "10.2307/2118559" in crosswalk and "10.2307/2118560" in crosswalk

    required_receipt_fields = {
        pointer.split("/")[-1]
        for pointer in phase_contract["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    assert required_receipt_fields <= set(receipt)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "intake" and receipt["intent"] == "intake"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "accepted"
    assert receipt["selftest_status"] == "passed_with_expected_projection_drift"
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]
    expected_command_results = [1, 1, 0, 0, 0, 0, 1]
    assert [row["exit_code"] for row in receipt["selftest_result"]["commands"]] == expected_command_results
    assert receipt["first_failed_gate"] == "master_replay.validator_base_identity_pending"
    assert receipt["retry_condition"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["known_failures"] and receipt["invalidation_inputs"]
    assert receipt["status_boundary"]
    assert receipt["inputs"]["theorem_dag_sha256"] == GRAPH_SHA256
    assert receipt["inputs"]["dependency_context_sha256"] == CONTEXT_SHA256
    assert receipt["inputs"]["phase_contract_sha256"] == CONTRACT_SHA256
    assert receipt["inputs"]["accepted_receipt_ids"] == []
    worker_packet = load(".stage1-worker-selftest.json")
    assert worker_packet["item_id"] == ITEM_ID and worker_packet["state"] == "[_]"
    assert worker_packet["base_revision"] == receipt["base_revision"]
    assert worker_packet["commands"] == receipt["selftest_result"]["commands"]
    assert worker_packet["known_failures"] == receipt["known_failures"]
    changed = set(worker_packet["changed_paths"])
    assert changed == {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0387/check_intake.py",
        "Stage1_Instances/THM-M-0387/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0387/intake-receipt.json",
        "Stage1_Instances/THM-M-0387/intake-validation.md",
        "Stage1_Instances/THM-M-0387/intake.json",
        "Stage1_Instances/THM-M-0387/scope-map.md",
        "Stage1_Instances/THM-M-0387/source-statement-crosswalk.md",
        "Stage1_Instances/THM-M-0387/task-dag.json",
    }
    bindings = receipt["artifact_bindings"]
    assert set(bindings) == set(ROLE_PATHS)
    for role, relative in ROLE_PATHS.items():
        binding = bindings[role]
        assert binding["role"] == role and binding["path"] == relative
        if role == "phase_receipt":
            assert binding["sha256"] == "self_referential_excluded"
            assert binding["git_blob"] == "self_referential_excluded"
        else:
            assert binding["sha256"] == sha256(relative)
            assert binding["git_blob"] == git_blob(relative)

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    checked_paths = {
        *ROLE_PATHS.values(),
        "Stage1_Instances/THM-M-0387/check_intake.py",
        "Stage1_Instances/THM-M-0387/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0387/intake-validation.md",
    }
    for relative in checked_paths:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {relative}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    selected_text = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in ROLE_PATHS.values())
    assert "/home/" not in selected_text and ".cron/" not in selected_text


def main() -> None:
    check()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
