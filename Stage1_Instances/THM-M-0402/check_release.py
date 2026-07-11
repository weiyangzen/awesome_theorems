#!/usr/bin/env python3
"""Fail-closed consistency check for THM-M-0402's release decision."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0402"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((OWNED / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("obligation-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next(
    (row for row in targets["targets"] if row["theorem_id"] == "THM-M-0402"), None
)
if target is None or target["execution_rank"] != 15:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the blocked decision")

if decision.get("item_id") != "S56-M-0402-RELEASE":
    fail("wrong release item")
if decision.get("verdict") != "blocked":
    fail("release verdict is not blocked")
if decision.get("lifecycle_before") != "planned" or decision.get("lifecycle_after") != "planned":
    fail("a worker decision promoted lifecycle")
if decision.get("accepted_receipt_ids") != []:
    fail("provisional evidence was represented as accepted")
terminal = decision.get("terminal_decisions", {})
if terminal.get("audit_complete") is not False or terminal.get("theorem_complete") is not False:
    fail("an open assurance gate was represented as terminally complete")

dependency = decision.get("dependency", {})
if dependency.get("item_id") != validation.get("item_id"):
    fail("validation dependency identity mismatch")
if validation.get("support_state") != "provisional_worker_selftest":
    fail("validation receipt is not worker-provisional")
if dependency.get("master_accepted") is not False:
    fail("worker validation was represented as master-accepted")
if dependency.get("receipt_sha256") != digest("validation-receipt.json"):
    fail("validation receipt digest drifted")

assurance = instance.get("assurance", {})
if assurance.get("root_vector") != ["H1", "M3", "R4"]:
    fail("instance root vector drifted")
if assurance.get("audit_complete") is not False or assurance.get("theorem_complete") is not False:
    fail("instance no longer supports the negative terminal decisions")

obligations = registry.get("obligations", [])
registry_ids = {row["obligation_id"] for row in obligations}
if len(registry_ids) != 10 or sum(row.get("root_relevant") is True for row in obligations) != 10:
    fail("frozen obligation denominator drifted")

boundary = graphs.get("closure_boundary", {})
expected_cut = ["M0402-L-SUNIT-FG", "M0402-L-NONDEGENERATE-UNIT-EQUATION"]
if boundary.get("root_machine_debt") != "M3":
    fail("root machine debt is no longer M3")
if boundary.get("closed_obligations") != [] or boundary.get("composition_certificates") != []:
    fail("graph authority now makes a closure claim")
if boundary.get("minimal_open_root_cut_set") != expected_cut:
    fail("minimal open root cut drifted")
if boundary.get("audit_complete") is not False or boundary.get("theorem_complete") is not False:
    fail("graph authority now makes a terminal completion claim")

result = validation.get("result", {})
if result.get("validated_partial_obligation_ids") != ["M0402-N-PROJECTIVE-NORMALIZATION"]:
    fail("validation partial-work boundary drifted")
if result.get("accepted_closed_obligation_ids") != [] or result.get("root_closed") is not False:
    fail("validation receipt no longer supports an open-root decision")

reconciliation = decision.get("evidence_reconciliation", {})
if reconciliation.get("accepted_closed_obligation_ids") != []:
    fail("release reconciliation promoted provisional closure")
if reconciliation.get("minimal_open_root_cut_set") != expected_cut:
    fail("release reconciliation cut set drifted")
for key in (
    "exact_root_kernel_check",
    "root_composition",
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "supply_chain_closure",
    "independent_release_verification",
    "deterministic_release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

replay = subprocess.run(
    ["python3", str(OWNED / "check_validation.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
    timeout=180,
)
if replay.returncode != 0 or "root remains open M3" not in replay.stdout:
    fail(f"upstream validation replay failed\n{replay.stdout}{replay.stderr}")

print(
    "release-decision: ok (blocked; validation unaccepted; root H1/M3/R4; "
    "partial normalization only; audit_complete=false; theorem_complete=false)"
)
