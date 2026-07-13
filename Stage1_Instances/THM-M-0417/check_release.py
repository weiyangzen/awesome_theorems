#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0417."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0417"
EXPECTED = {
    "validation-receipt.json": "f5c0bdadc43763a46900d8d4ff1f9ede4b0518b3a38c9b6d18cda1f8b108cd9a",
    "proof-receipt.json": "8fca2d81f7b332a94003366d57c81893025adddd3e1df6322ea18e4d77d28195",
    "obligation-registry.json": "51e3afc110ee9f8c90264b54306979e6b6a56553bbeeb24fd506c2b71696eb56",
    "obligation-nodes.json": "f89fa1effdc64237d921402ab9affb5bab26effacc141ba6136d5efe4c914c42",
    "typed-graphs.json": "69095d48e63ae9dff0901ee41e4b0f77961da69348cbc734d10ad10443c284c4",
    "statement.json": "8a0bc1fb8fd159005cd2c5f6d308801daf7108e208ae483a34717b912d0f0c8c",
    "source_statement_crosswalk.md": "6abb154d403913eeb850ab90a04865ac799a83f3df52e82daea5e6eebc0b96cc",
    "intake.json": "953baa79d2264568edf49ce090c5874b2721f078a54e6525ad0f5344767e4f24",
    "Statement.lean": "fc5125d7afbcd9b11aa00f4f3bf2c55367faf662968bd223928f8f935ce756fe",
    "ObligationTree.lean": "cd0f4bdc3d1773145d1ab1e3cd23f111f00cd671bf7ba6bc3ffd2fad74812798",
    "Proof.lean": "19a759e2c5fcfd113585ce416eed7341ac55ab0aa2618b66da1587d4eb5a132b",
    "Validation.lean": "c1c15b10e7d64f3cd836d8f24e2a9a2c62e46be06689a9cce5ad380ad81ed65f",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest(name: str) -> str:
    return hashlib.sha256((OWNED / name).read_bytes()).hexdigest()


for name, expected in EXPECTED.items():
    actual = digest(name)
    if actual != expected:
        fail(f"release input hash mismatch: {name}: expected {expected}, got {actual}")

validation = json.loads((OWNED / "validation-receipt.json").read_text(encoding="utf-8"))
proof = json.loads((OWNED / "proof-receipt.json").read_text(encoding="utf-8"))
decision = json.loads((OWNED / "release-decision.json").read_text(encoding="utf-8"))
registry = json.loads((OWNED / "obligation-registry.json").read_text(encoding="utf-8"))
nodes = json.loads((OWNED / "obligation-nodes.json").read_text(encoding="utf-8"))
graphs = json.loads((OWNED / "typed-graphs.json").read_text(encoding="utf-8"))
intake = json.loads((OWNED / "intake.json").read_text(encoding="utf-8"))

result = subprocess.run(
    [sys.executable, str(OWNED / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=900,
    check=False,
)
if result.returncode != 0:
    fail(f"upstream validation replay failed\n{result.stdout}")

if validation["support_state"] != "provisional_worker_selftest" or validation["release_grade"]:
    fail("validation dependency is not the expected provisional nonrelease receipt")
if validation["result"]["provisional_machine_root_closed"] is not True:
    fail("validation receipt no longer records provisional exact-root closure")
if validation["result"]["audit_complete"] or validation["result"]["theorem_complete"]:
    fail("validation receipt unexpectedly claims a terminal decision")
if set(validation["result"]["open_obligation_ids"]) != {
    "M0417-X-SOURCE",
    "M0417-X-TRUST",
}:
    fail("validation open-obligation boundary changed")
if proof["result"]["machine_root_closed"] is not True:
    fail("proof receipt no longer records provisional exact-root closure")
if proof["result"]["audit_complete"] or proof["result"]["theorem_complete"]:
    fail("proof receipt unexpectedly claims a terminal decision")

if intake["lifecycle_mode"] != "planned" or intake["theorem_complete"]:
    fail("instance authority no longer records the planned, incomplete lifecycle")
if intake["root_vector"] != {"human": "H1", "machine": "M3", "readability": "R3"}:
    fail("accepted intake root vector changed")
if intake["canonical_formal_target"]["gate_state"] != "open_pending_statement_phase":
    fail("stale intake boundary was unexpectedly reconciled outside master acceptance")
if registry["audit_complete"] or registry["theorem_complete"]:
    fail("frozen registry unexpectedly claims a terminal decision")
if {row["obligation_id"] for row in nodes["nodes"]} != set(graphs["nodes"]):
    fail("frozen registry and typed graph node sets disagree")

evidence_targets = {
    edge["to"] for edge in graphs["graphs"]["evidence"] if edge["type"] == "evidence_for"
}
if evidence_targets != {"M0417-ROOT", "M0417-T-COMPOSE"}:
    fail("stale typed evidence graph boundary changed")
if any("VALIDATION" in edge["from"] or "PROOF" in edge["from"] for edge in graphs["graphs"]["evidence"]):
    fail("typed evidence graph unexpectedly binds provisional phase receipts")

if decision["verdict"] != "blocked" or decision["lifecycle_after"] != "planned":
    fail("release decision must remain blocked and planned")
if decision["release_grade"] or decision["accepted_receipt_ids"]:
    fail("worker release decision cannot claim release grade or accepted receipts")
if decision["terminal_decisions"] != {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
}:
    fail("terminal decisions are not fail-closed")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("unexpected first failed workflow gate")
if decision["next_failed_theorem_gate"]["gate_id"] != "S56-7.4-FOUNDATION-AND-TRANSITIVE-TCB-CLOSURE":
    fail("unexpected next failed theorem gate")
if decision["first_failed_release_gate"]["gate_id"] != "S56-10.6-HERMETIC-COLD-BUILD":
    fail("unexpected first failed release gate")

cut_text = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "S56-M-0417-VALIDATION",
    "M0417-X-SOURCE",
    "R0 structured reconstruction",
    "M0417-X-TRUST",
    "empty-cache network-denied cold build",
    "independently implemented minimal verifier",
    "deterministic evidence bundle",
):
    if fragment not in cut_text:
        fail(f"remaining cut set omits {fragment!r}")

print("ok: upstream narrow Lean validation replayed against pinned Lean/mathlib")
print("ok: provisional exact-root M0-W candidate evidence reconciled without promotion")
print("open: M0417-X-SOURCE, M0417-X-TRUST, H0/R0, and stale structured state; AUDIT-Z is false")
print("blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts")
