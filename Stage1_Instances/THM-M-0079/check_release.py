#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0079-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0079"
ITEM = "S56-M-0079-RELEASE"
THEOREM = "THM-M-0079"
BASE_REVISION = "bd80ad137c187dda02bcfcb2529360ef6d9b53eb"
BASE_TREE = "65fb1d54476897700b46e671380377bdd27c4e0b"
VALIDATION_SHA256 = "94af8d09e303279f7c95e4e5ad1c7106fec8512cf46ead187bd8f40674003c0f"
EXPRESSION_SHA256 = "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
DENOMINATOR_SHA256 = "88cf0ea4157fed371957616088fbbbbc9c0662d6d49d2ee1c502007b88956b92"
VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
VECTOR_LIST = ["H1", "M3", "R4"]
UNVERIFIED_CERTIFICATES = {
    "M0079-CERT-C-ACTION-GROUPOID-FREE",
    "M0079-CERT-C-ROOTED-CONNECTED",
    "M0079-CERT-C-GEODESIC-TREE",
    "M0079-CERT-L-GEODESIC-ARBORESCENCE",
    "M0079-CERT-C-TREE-LOOPS",
    "M0079-CERT-L-TREE-EDGE-IDENTITY",
    "M0079-CERT-C-FUNCTOR-END-HOM",
    "M0079-CERT-L-SPANNING-END-FREE",
    "M0079-CERT-L-CONNECTED-END-FREE",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    decision = load(HERE / "release-decision.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == decision["execution_rank"] == 1105
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0079-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1105,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0079-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-0079-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_dag["accepted_states"] == []

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0079-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_sha256"] == VALIDATION_SHA256
    assert dependency["receipt_base_revision"] == validation["base_revision"]
    assert dependency["support_state"] == validation["support_state"] == (
        "provisional_worker_selftest"
    )
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["master_accepted"] is False
    assert dependency["recorded_recipe_fresh_at_release_base"] is False
    assert validation["base_revision"] != BASE_REVISION
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_receipt_ids"] == instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        EXPRESSION_SHA256
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256

    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["root_machine_classification"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_required_machine_assurance_frontier"] == [
        "M0079-S-FOUNDATION"
    ]
    planned = {
        row["certificate_id"]
        for row in graphs["composition_certificates"]
        if row["status"] == "planned_source_composition_pending_exact_child_harness"
    }
    assert planned == UNVERIFIED_CERTIFICATES

    assert proof["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof["root_evidence"]["accepted_root_closed"] is False
    assert proof["root_evidence"]["internal_per_node_composition_credit"] is False
    assert set(proof["root_evidence"]["unverified_internal_composition_certificate_ids"]) == (
        UNVERIFIED_CERTIFICATES
    )
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["accepted"] is False

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == VECTOR_LIST
    assert result["audit_complete"] is False
    assert result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )

    gates = decision["evidence_reconciliation"]
    assert gates["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    for gate in (
        "validation_recipe_freshness",
        "dependency_master_accepted",
        "authoritative_graph_reconciled",
        "complete_child_composition_accepted",
        "foundation_and_transitive_trust_accepted",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "hermetic_cold_offline_replay",
        "tcb_sbom_license_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_adversarial_ci",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert gates[gate] is False, gate

    cut = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0079-VALIDATION",
        "M0079-S-FOUNDATION",
        "nine internal source-body composition",
        "H0 primary-source",
        "R0 structured",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed signed release bundle",
    ):
        assert fragment in cut, fragment

    expected_packet_keys = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert set(packet) == expected_packet_keys
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    }
    assert packet["known_failures"] == decision["known_failures"]
    release_command = ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert any(row["argv"] == release_command for row in packet["commands"])

    print("PASS S56-M-0079-RELEASE reconciliation")
    print("verdict=blocked lifecycle=planned root_vector=H1/M3/R4")
    print("audit_complete=false theorem_complete=false accepted_receipts=0")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("next_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")
    print("validation_recipe_freshness=fail_closed")


if __name__ == "__main__":
    main()
