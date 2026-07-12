#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0500-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0500"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_HEAD = "1f79a3f74a8e206d44c27513f4016a26dd7050e3"
EXPECTED_TREE = "5024086eeb6994ff53242ac82b32b2d9af8b2462"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def git_value(expression: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", expression],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


decision = load("release-decision.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
validation_spec = load("validation-phase-spec.json")
dag = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8"))
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0500")
validation_item = next(row for row in dag["items"] if row["id"] == "S56-M-0500-VALIDATION")
release_item = next(row for row in dag["items"] if row["id"] == "S56-M-0500-RELEASE")

assert decision["base_revision"] == EXPECTED_HEAD
assert decision["base_tree"] == EXPECTED_TREE
assert git_value(f"{decision['base_revision']}^{{tree}}") == decision["base_tree"]
ancestor = subprocess.run(
    ["git", "merge-base", "--is-ancestor", decision["base_revision"], "HEAD"],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=10,
    check=False,
)
assert ancestor.returncode == 0, ancestor.stdout.decode(errors="replace")
assert target["execution_rank"] == 877
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert validation_item["state"] == "[_]"
assert release_item["state"] == "[ ]"
assert release_item["depends_on"] == [validation_item["id"]]

assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert registry["root_obligation_id"] == "M0500-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0500-RELEASE"
assert decision["theorem_id"] == "THM-M-0500"
assert decision["verdict"] == "blocked" and decision["release_grade"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R4"]
assert decision["root_vector"]["best_provisional_evidence"] == ["H1", "M0-W", "R4"]
assert decision["terminal_decisions"] == {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
}

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"reconciled input drifted: {name}"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["receipt_base_revision"] == validation["base_revision"]
assert dependency["receipt_base_tree"] == validation["base_tree"]
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert validation["base_revision"] != decision["base_revision"]
assert validation["base_tree"] != decision["base_tree"]

recipe = validation_spec["recipes"][0]
assert recipe["argv"] == ["python3", "Stage1_Instances/THM-M-0500/check_validation.py"]
assert recipe["expected_exit"] == 0
replay = subprocess.run(
    recipe["argv"],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=recipe["timeout_seconds"],
    check=False,
)
assert replay.returncode == 1, replay.stdout
assert "receipt[\"base_revision\"]" in replay.stdout
assert "AssertionError" in replay.stdout

proof_replay = subprocess.run(
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0500/Proof.lean"],
    cwd=LEAN_ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=60,
    check=False,
)
assert proof_replay.returncode == 0, proof_replay.stdout
for fragment in (
    "Stage1Instances.THM_M_0500.dirichletPrimesInAP_proof : DirichletPrimesInAPTarget",
    "'Nat.infinite_setOf_prime_and_eq_mod' depends on axioms: [propext, Classical.choice, Quot.sound]",
    "'Stage1Instances.THM_M_0500.dirichletPrimesInAP_proof' depends on axioms: [propext, Classical.choice, Quot.sound]",
):
    assert fragment in proof_replay.stdout, f"exact-root replay output omitted {fragment!r}"

assert proof["result"]["root_machine_proof_body_present"] is True
assert proof["result"]["theorem_complete"] is False
assert proof["proof_body"]["classification"] == "local_wrapper_upstream_mathlib"
assert proof["proof_body"]["terminal_declaration"] == "Nat.infinite_setOf_prime_and_eq_mod"
assert set(proof["closed_obligation_ids"]) == set(
    registry["frozen_denominators"]["required_machine"]
)
assert proof["recipe"]["covered_ids"] == ["M0500-ROOT"]
assert set(proof["closed_obligation_ids"]) != set(proof["recipe"]["covered_ids"])
assert validation["result"]["exact_root_kernel_closed_locally"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["audit_complete"] is False and closure["theorem_complete"] is False
assert closure["minimal_open_root_cut"] == ["M0500-T-NONSUM", "M0500-L-SUPPORT"]
root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0500-ROOT")
assert root_node["human_debt"] == "H1"
assert root_node["machine_debt"] == "M3"
assert root_node["readability_debt"] == "R4"

assert decision["first_observed_failed_gate"]["gate_id"] == "S56-9.1-RECEIPT-FRESHNESS"
assert decision["first_dependency_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
assert decision["evidence_reconciliation"]["validation_recipe_freshness"].startswith("failed:")
assert decision["evidence_reconciliation"]["structured_state_freshness"].startswith("failed:")

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "Fresh replayable validation receipt",
    "Master acceptance",
    "Node-scoped receipts",
    "typed-graph reconciliation",
    "AUDIT-Z",
    "H0 primary-source",
    "R0 node-by-node",
    "transitive declaration",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "Two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
    "THEOREM-Z",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_reconciliation",
    "human_source_acceptance",
    "readability_acceptance",
    "complete_provenance_and_trust_closure",
    "hermetic_release_reproduction",
    "supply_chain_closure",
    "independent_release_verification",
    "deterministic_release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE
)
for path in HERE.glob("*.lean"):
    source = re.sub(r"/-.*?-/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited construct in {path.name}"

print("release-decision: ok (blocked; stale validation receipt; dependency unaccepted)")
print("exact-root replay: pass (provisional M0-W candidate; authoritative H1/M3/R4 unchanged)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
