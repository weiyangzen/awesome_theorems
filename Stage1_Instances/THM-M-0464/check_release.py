#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0464-RELEASE."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0464"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
intake = load("intake.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
targets = json.loads(
    (ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(
    (entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0464"),
    None,
)

if target is None or target["execution_rank"] != 310:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the planned/open decision")
if intake["lifecycle_mode"] != "planned" or intake["theorem_complete"] is not False:
    fail("intake authority no longer supports the planned/open decision")
if intake["root_vector"] != {"human": "H1", "machine": "M4", "readability": "R3"}:
    fail("accepted intake root vector drifted")

if decision["item_id"] != "S56-M-0464-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("a blocked worker decision must not advance lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional evidence was represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open audit and theorem gates require both terminal booleans to be false")

for name, expected in decision["reconciled_inputs"].items():
    if digest(name) != expected:
        fail(f"reconciled input drifted: {name}")
if graphs["registry_denominator_sha256"] != registry["denominator_sha256"]:
    fail("typed graph and frozen registry denominator disagree")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation receipt identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation receipt digest mismatch")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation receipt is not the recorded provisional worker evidence")
if validation["release_grade"] is not False or dependency["master_accepted"] is not False:
    fail("unaccepted validation evidence was promoted")

result = validation["result"]
if result["machine_root_closed"] is not False or result["theorem_complete"] is not False:
    fail("validation no longer records the open theorem root")
if result["audit_complete"] is not False:
    fail("validation no longer records the open audit")
if result["remaining_root_cut_set"] != registry["closure_boundary"]["immediate_root_cut_set"]:
    fail("validation and frozen registry root cut sets disagree")
if graphs["closure_boundary"]["root_closed"] is not False:
    fail("typed graph no longer records an open root")
if decision["root_vector"]["accepted_before"] != ["H1", "M4", "R3"]:
    fail("release decision does not match accepted intake state")
if decision["root_vector"]["accepted_after"] != decision["root_vector"]["accepted_before"]:
    fail("release decision silently changes accepted debt state")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("first failed dependency gate drifted")
if decision["next_failed_theorem_gate"]["gate_id"] != "S56-6.7-ROOT-COMPOSITION-INCOMPLETE":
    fail("next theorem-completion gate drifted")

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance", "M0464-S-DEFINITIONS", "M0464-N-CELL",
    "M0464-C-PARAM", "M0464-L-DETERMINANT", "M0464-B-ALGEBRAIC",
    "M0464-L-INDUCTION", "M0464-L-COUNT", "M0464-X-TRANSPORT",
    "H0 primary-source", "R0 readable", "empty-cache network-denied cold build",
    "SBOM", "two signed attestations", "minimal verifier",
    "deterministic content-addressed release bundle", "THEOREM-Z",
):
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "exact_root_kernel_closure", "root_composition", "audit_inventory_acceptance",
    "human_source_acceptance", "readability_acceptance",
    "complete_provenance_and_trust_closure", "hermetic_release_reproduction",
    "supply_chain_closure", "independent_release_verification",
    "deterministic_release_bundle",
):
    if decision["evidence_reconciliation"][key] != "missing":
        fail(f"release blocker {key!r} was silently cleared")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    timeout=150, check=False,
)
if replay.returncode != 0:
    fail(f"upstream validation replay failed:\n{replay.stdout}")
if "general Pila-Wilkie root remains M3" not in replay.stdout:
    fail("upstream validation did not preserve the open-root boundary")

print("release-decision: ok (blocked; validation dependency is unaccepted)")
print("validation replay: ok (seven partial bodies; exact Pila-Wilkie root remains M3)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
