#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0403"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


spec = load("release-spec.json")
receipt = load("release-receipt.json")
validation = load("validation-receipt.json")
proof = load("proof-receipt.json")
registry = load("obligation-registry.json")
graphs = load("obligation-graphs.json")

assert spec["item_id"] == receipt["item_id"] == "S56-M-0403-RELEASE"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0403"
for name, digest in receipt["inputs"].items():
    assert digest == sha256(HERE / name), name

result = subprocess.run(
    ["python3", str(HERE / "validate_phase.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=120,
    check=False,
)
assert result.returncode == 0, result.stdout
assert "open: root M4" in result.stdout
assert "blocked: cold hermetic replay" in result.stdout

assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False
assert validation["result"]["root_machine_debt"] == "M4"
assert validation["result"]["closed_obligation_ids"] == []
assert validation["result"]["composition_certificates"] == []
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"
assert proof["closed_obligation_ids"] == []
assert proof["result"]["root_closed"] is False
assert registry["status_observed_after_freeze"] == {
    "closed_obligations": [], "root_machine_debt": "M4"
}
boundary = graphs["closure_boundary"]
assert boundary["minimal_open_root_cut_set"] == ["M0403-L-ESS-FINITE"]
assert boundary["theorem_complete"] is False

decision = receipt["decision"]
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == ["H1", "M4", "R3"]
assert decision["audit_complete"] is False
assert decision["theorem_complete"] is False
assert decision["accepted_receipt_ids"] == []
assert decision["first_failed_gate"] == "exact_root_kernel_closure"
assert decision["remaining_root_cut_set"] == ["M0403-L-ESS-FINITE"]
assert receipt["release_grade"] is False
assert receipt["master_acceptance"] == "pending_and_not_claimed"

print("ok: upstream node-scoped validation replayed against pinned Lean/mathlib")
print("open: exact root M4; no closed obligation or composition certificate")
print("open: audit H1/R3; AUDIT-Z is not established")
print("blocked: hermetic, supply-chain, independent-verifier, and master-acceptance gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; cut M0403-L-ESS-FINITE")
