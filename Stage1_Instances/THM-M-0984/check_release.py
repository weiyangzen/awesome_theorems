#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0984."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0984"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0984")

assert target["execution_rank"] == 264
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert decision["item_id"] == "S56-M-0984-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0984-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

closure = graphs["closure_boundary"]
assert registry["root_obligation_id"] == "M0984-ROOT"
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0984-L-TERMINAL"]
terminal = decision["terminal_decisions"]
assert terminal["audit_complete"] is False and terminal["theorem_complete"] is False
assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance", "M0984-L-TERMINAL", "H0 primary-source", "R0 structured",
    "transitive declaration provenance", "empty-cache network-denied cold build",
    "SBOM and license", "two signed attestations", "minimal release verifier",
    "deterministic content-addressed",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "human_source_acceptance", "readability_acceptance", "complete_trust_closure",
    "hermetic_release_reproduction", "supply_chain_archive",
    "independent_release_verification", "release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

validation_check = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=False,
)
assert validation_check.returncode == 0, validation_check.stdout
assert "STALE authoritative graph" in validation_check.stdout
assert "BLOCKED release gates" in validation_check.stdout

print("release reconciliation ok: provisional validation receipt and frozen graph agree")
print("release blocked: dependency unaccepted; H1/R3 and release-assurance gates remain open")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
