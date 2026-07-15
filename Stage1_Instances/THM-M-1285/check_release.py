#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-1285-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1285"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


if sys.flags.optimize:
    raise SystemExit("release reconciliation requires Python assertions")


targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
intake = load(HERE / "intake.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
validation = load(HERE / "validation-receipt.json")
decision = load(HERE / "release-decision.json")
packet = load(ROOT / ".stage1-worker-selftest.json")

target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-1285")
item = next(row for row in execution["items"] if row["id"] == "S56-M-1285-RELEASE")
predecessor = next(
    row for row in execution["items"] if row["id"] == "S56-M-1285-VALIDATION"
)

assert target["execution_rank"] == item["execution_rank"] == 456
assert git("rev-parse", "HEAD") == decision["base_revision"]
assert git("rev-parse", "HEAD^{tree}") == decision["base_tree"]
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["lifecycle_mode"] == intake["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is intake["theorem_complete"] is False
assert item["theorem_id"] == "THM-M-1285" and item["phase"] == "release"
assert item["layer"] == 6 and item["state"] == "[ ]"
assert item["depends_on"] == ["S56-M-1285-VALIDATION"]
assert item["owned_paths"] == ["Stage1_Instances/THM-M-1285"]
assert predecessor["state"] == "[_]"

assert decision["schema_version"] == "stage1-release-decision/1.0"
assert decision["item_id"] == item["id"]
assert decision["theorem_id"] == target["theorem_id"]
assert decision["execution_rank"] == 456
assert decision["phase"] == decision["intent"] == "release"
assert decision["attestor"] == "stage1-rev56-worker-slot9"
assert decision["proposed_state"] == "[_]"
assert decision["root_obligation_id"] == registry["root_obligation_id"] == "M1285-ROOT"
assert decision["canonical_target"] == validation["canonical_target"]
assert decision["canonical_target_expression_sha256"] == (
    validation["canonical_target_expression_sha256"]
)
assert decision["registry_denominator_sha256"] == registry["denominator_sha256"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == predecessor["id"]
assert dependency["worker_projection"] == predecessor["state"] == "[_]"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert proof["accepted"] is validation["accepted"] is False
assert proof["accepted_closed_obligation_ids"] == []
assert validation["accepted_closed_obligation_ids"] == []

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M3", "R3"]
assert result["audit_complete"] is result["theorem_complete"] is False
assert result["release_accepted"] is False
assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
assert decision["accepted_receipt_ids"] == []
assert decision["provisional_receipt_ids_inspected"] == [
    proof["receipt_id"],
    validation["receipt_id"],
]
assert decision["changed_paths"] == [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1285/check_release.py",
    "Stage1_Instances/THM-M-1285/release-decision.json",
    "Stage1_Instances/THM-M-1285/release-validation.md",
]
assert decision["known_failures"]
assert packet["item_id"] == decision["item_id"]
assert packet["base_revision"] == decision["base_revision"]
assert packet["state"] == decision["proposed_state"] == "[_]"
assert packet["changed_paths"] == decision["changed_paths"]
assert packet["known_failures"]
for path in (
    Path(__file__),
    HERE / "release-decision.json",
    HERE / "release-validation.md",
    ROOT / ".stage1-worker-selftest.json",
):
    assert_text_hygiene(path)

assert validation["result"]["network_isolated_trust_zero_replay"] == "pass"
assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
assert validation["result"]["observed_axioms"] == [
    "propext",
    "Classical.choice",
    "Quot.sound",
]
assert validation["result"]["accepted_root_machine_debt"] == "M3"
assert validation["result"]["accepted_root_closed"] is False
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["accepted_closed_obligations"] == []

assert registry["denominator_sha256"] == proof["registry_denominator_sha256"]
assert registry["denominator_sha256"] == validation["registry_denominator_sha256"]
assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
assert graphs["closure_boundary"] == {
    "minimal_open_root_cut": ["M1285-T-PACKAGE"],
    "root_closed": False,
    "root_machine_debt": "M3",
    "theorem_complete": False,
}

gates = decision["evidence_reconciliation"]
assert gates["exact_statement_kernel_replay"] == "provisional_pass"
assert gates["exact_root_kernel_replay"] == "provisional_pass"
assert gates["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert gates["accepted_root_machine_state"] == "M3_open"
for gate in (
    "dependency_master_accepted",
    "authoritative_graph_reconciled",
    "audit_z_accepted",
    "primary_source_h0_review",
    "independent_r0_review",
    "accepted_foundation_and_complete_tcb",
    "complete_transitive_provenance",
    "immutable_clean_release_input",
    "hermetic_cold_offline_replay",
    "sbom_and_license_closure",
    "independent_clean_runner_attestations",
    "independently_implemented_minimal_verifier",
    "mutation_and_metamorphic_ci",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert gates[gate] is False, gate

cut_set = "\n".join(result["remaining_root_cut_set"])
for fragment in (
    "validation dependency",
    "node-specific proof evidence",
    "H0 primary-source",
    "R0",
    "foundation, axiom, trust, and TCB",
    "transitive provenance",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set, fragment

print("PASS S56-M-1285-RELEASE reconciliation")
print("verdict=blocked lifecycle=planned root_vector=H2/M3/R3")
print("audit_complete=false theorem_complete=false accepted_receipts=0")
print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("first_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")
