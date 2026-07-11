#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0399 release decision."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0399"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision failed: {message}")


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((OWNED / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-phase.json")
proof = load("proof-phase.json")
registry = load("obligation-registry.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((row for row in targets["targets"] if row["theorem_id"] == "THM-M-0399"), None)
if target is None or target["execution_rank"] != 12:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the blocked decision")

if decision.get("item_id") != "S56-M-0399-RELEASE" or decision.get("verdict") != "blocked":
    fail("wrong release item or verdict")
if decision.get("lifecycle_before") != "planned" or decision.get("lifecycle_after") != "planned":
    fail("a blocked worker decision promoted lifecycle")
if decision.get("accepted_receipt_ids") != []:
    fail("provisional evidence was represented as accepted")
terminal = decision.get("terminal_decisions", {})
if terminal.get("audit_complete") is not False or terminal.get("theorem_complete") is not False:
    fail("open assurance gates were represented as terminally complete")

dependency = decision.get("dependency", {})
if dependency.get("item_id") != validation.get("item_id"):
    fail("validation dependency identity mismatch")
if dependency.get("master_accepted") is not False or validation.get("accepted_receipt_ids") != []:
    fail("worker validation was represented as master accepted")
if dependency.get("artifact_sha256") != digest("validation-phase.json"):
    fail("validation artifact digest drifted")
if validation.get("verdict") != "blocked" or validation.get("theorem_complete") is not False:
    fail("validation no longer supports a blocked theorem verdict")

if registry.get("denominator", {}).get("root_relevant_total") != 11:
    fail("frozen obligation denominator drifted")
if proof.get("closed_obligation_ids") != ["M0399-ROOT-COMPOSE"]:
    fail("proof closure boundary drifted")
if validation.get("remaining_root_cut_set") != ["M0399-STRONG-FINITE"]:
    fail("minimal open proof cut drifted")
if validation.get("root_vector") != {"H": "H1", "M": "M4", "R": "R4"}:
    fail("validation debt vector drifted")

reconciliation = decision.get("evidence_reconciliation", {})
if reconciliation.get("worker_closed_obligation_ids") != ["M0399-ROOT-COMPOSE"]:
    fail("release reconciliation lost the conditional composition boundary")
if reconciliation.get("accepted_closed_obligation_ids") != []:
    fail("provisional closure was represented as accepted")
if reconciliation.get("minimal_open_proof_cut") != ["M0399-STRONG-FINITE"]:
    fail("release reconciliation open cut drifted")
for key in (
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "supply_chain_closure",
    "independent_release_verification",
    "deterministic_release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

cut_text = "\n".join(decision.get("remaining_root_cut_set", []))
for fragment in (
    "master acceptance",
    "M0399-STRONG-FINITE",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "independently implemented minimal release verifier",
    "deterministic content-addressed release bundle",
):
    if fragment not in cut_text:
        fail(f"remaining cut set omits {fragment!r}")

replay = subprocess.run(
    ["python3", str(OWNED / "check_validation_phase.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
    timeout=180,
)
if replay.returncode != 0 or "release gates truthfully blocked" not in replay.stdout:
    fail(f"upstream validation replay failed\n{replay.stdout}{replay.stderr}")

print(
    "release-decision: ok (blocked; validation unaccepted; H1/M4/R4; "
    "StrongFiniteStatement/root open; audit_complete=false; theorem_complete=false)"
)
