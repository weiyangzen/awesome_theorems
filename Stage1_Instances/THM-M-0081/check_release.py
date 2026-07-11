#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0081 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0081"
EXPECTED = {
    "validation-receipt.json": "a0bb1a031222fe8131c266d8ce6ef4ecd805f06c3a2b5931c9102c750b1a72a8",
    "proof-receipt.json": "d13d6c58d89ce66b9cd80217f0d7e13ce116ed3984cc88f2d2d79ca039b87163",
    "instance.json": "7731ce870ece8d7df1538c07da8047a366d56535b31a00b01620e8c6904d560c",
    "obligation-registry.json": "f3b915d6851e344cab91aa505111e66df50c6f944077fd10545187eae60d388d",
    "typed-graphs.json": "845b8814a136237ad1edcc11f976717340a0ec7343b819fd87963b16d70d3935",
    "statement.json": "de2b6a2cff18fc493591ed1a86d17f54b0a0340e5475b9a220a19adfa07123be",
    "source-statement-crosswalk.md": "702c70cc1c35054fe6289378e342b842efd429e88b7fa0064828245814f5bb07"
}


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


for name, expected in EXPECTED.items():
    actual = hashlib.sha256((OWNED / name).read_bytes()).hexdigest()
    if actual != expected:
        fail(f"release input hash mismatch: {name}")

validation = load("validation-receipt.json")
decision = load("release-decision.json")
instance = load("instance.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
target = next((x for x in targets["targets"] if x["theorem_id"] == "THM-M-0081"), None)

if target is None or target["execution_rank"] != 138 or target["theorem_complete"] is not False:
    fail("target membership, rank, or completion baseline drifted")
if instance["lifecycle"] != "planned" or instance["root_vector"] != {"H": "H2", "M": "M4", "R": "R4"}:
    fail("instance lifecycle or accepted root vector drifted")
if decision["item_id"] != "S56-M-0081-RELEASE" or decision["verdict"] != "blocked":
    fail("release item identity or verdict is wrong")
if decision["lifecycle_after"] != "planned" or decision["accepted_receipt_ids"]:
    fail("a worker release decision cannot promote lifecycle or accept receipts")
if decision["terminal_decisions"] != {
    "audit_complete": False, "theorem_complete": False,
    "audit_z": "blocked", "theorem_z": "blocked"
}:
    fail("terminal decisions are not fail-closed")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("unexpected first failed gate")
dependency = decision["dependency"]
if dependency["receipt_sha256"] != EXPECTED["validation-receipt.json"]:
    fail("validation dependency digest is stale")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation dependency is incorrectly release-eligible")
if validation["result"]["root_closed"] is not True or validation["result"]["theorem_complete"] is not False:
    fail("provisional exact-root evidence boundary drifted")
if graphs["closure_boundary"]["theorem_complete"] is not False:
    fail("frozen graph unexpectedly claims theorem completion")

required = ("primary-source", "readable reconstruction", "provenance", "empty-cache",
            "SBOM", "two signed attestations", "minimal verifier", "deterministic")
cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in required:
    if fragment not in cut:
        fail(f"remaining cut set omits {fragment!r}")

result = subprocess.run(
    [sys.executable, str(OWNED / "check_validation.py")], cwd=ROOT,
    text=True, capture_output=True, timeout=60
)
if result.returncode != 0:
    fail(f"upstream validation replay failed\n{result.stdout}{result.stderr}")

print("release-decision: ok (blocked; validation dependency is provisional)")
print("evidence: exact-root local Lean validation replay passed without state promotion")
print("terminal: AUDIT-Z=false; THEOREM-Z=false; accepted receipts=none")
