#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0170-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0170"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
intake = load("intake.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(item for item in targets["targets"] if item["theorem_id"] == "THM-M-0170")

assert target["execution_rank"] == 123
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
assert intake["root_vector"] == {"human": "H1", "machine": "M3", "readability": "R3"}
assert registry["root_obligation_id"] == "M0170-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0170-RELEASE"
assert decision["theorem_id"] == "THM-M-0170"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R3"]
assert decision["root_vector"]["best_provisional_evidence"] == ["H1", "M4", "R3"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0170-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

root = decision["reconciled_root"]
closure = graphs["closure_boundary"]
assert root["machine_debt"] == "M4"
assert root["kernel_closed"] is validation["root_decision"]["kernel_closed"] is False
assert root["remaining_root_cut_set"] == closure["remaining_root_cut_set"]
assert root["remaining_root_cut_set"] == ["M0170-B-COMPACT", "M0170-B-NONCOMPACT"]
assert root["audit_complete"] is validation["root_decision"]["audit_complete"] is False
assert root["theorem_complete"] is validation["root_decision"]["theorem_complete"] is False
assert proof["root_closed"] is False and proof["theorem_complete"] is False

terminal = decision["terminal_decisions"]
assert terminal == {
    "audit_z": "blocked",
    "theorem_z": "blocked",
    "release": "blocked",
    "worker_item_selftest": "pass",
}
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_theorem_gate"] == "root.kernel_closure"
assert decision["failed_gates"][0] == "S56-10.2-DEPENDENCY-ACCEPTANCE"

cut_set = "\n".join(decision["remaining_release_cut_set"])
for fragment in (
    "master acceptance", "M0170-B-COMPACT", "AUDIT-Z", "H0 primary-source",
    "R0 structured", "accepted axiom policy", "empty-cache network-denied cold build",
    "SBOM and license", "two signed attestations", "minimal release verifier",
    "deterministic content-addressed signed release bundle",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_reconciliation", "human_source_acceptance", "readability_acceptance",
    "complete_trust_closure", "hermetic_release_reproduction", "supply_chain_archive",
    "independent_release_verification", "release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

graph_check = subprocess.run(
    ["python3", str(HERE / "check_obligation_tree.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=False,
)
assert graph_check.returncode == 0, graph_check.stdout
assert "17 obligations" in graph_check.stdout and "root closure: open (M4)" in graph_check.stdout

lean_check = subprocess.run(
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0170/Validation.lean"],
    cwd=ROOT / "Formalizations" / "Lean", text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=False,
)
assert lean_check.returncode == 0, lean_check.stdout

print("release reconciliation ok: validation receipt hash and frozen root state agree")
print("release blocked: exact Nash root remains M4 with compact/noncompact branches open")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
