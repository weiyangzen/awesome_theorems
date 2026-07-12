#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0557-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0557"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


decision = json.loads((HERE / "release-decision.json").read_text())
assert decision["item_id"] == "S56-M-0557-RELEASE"
assert decision["theorem_id"] == "THM-M-0557"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H1", "M4", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M4", "R4"]
assert decision["terminal_decisions"] == {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
}
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert len(decision["remaining_root_cut_set"]) == 10

for name, expected in decision["reconciled_inputs"].items():
    actual = sha256(HERE / name)
    assert actual == expected, f"stale {name}: expected {expected}, got {actual}"

validation = json.loads((HERE / "validation-receipt.json").read_text())
dependency = decision["dependency"]
assert validation["receipt_id"] == dependency["receipt_id"]
assert validation["support_state"] == dependency["support_state"]
assert validation["release_grade"] is dependency["release_grade"] is False
assert dependency["master_accepted"] is False
assert validation["result"]["root_proof_body_closed"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"

instance = json.loads((HERE / "instance.json").read_text())
assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is False
assert instance["theorem_complete"] is False

# Replay the dependency's actual structured validation recipe rather than trusting prose.
result = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=180,
    check=False,
)
if result.returncode != 0:
    raise RuntimeError(f"validation replay failed ({result.returncode})\n{result.stdout}")
assert "PASS THM-M-0557 validation" in result.stdout
assert "OPEN hermetic gate" in result.stdout
assert "OPEN independent gate" in result.stdout

print("release-decision: ok (blocked; validation dependency is provisional and unaccepted)")
print("provisional root replay: pass; accepted root vector remains H1/M4/R4")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
print("first release failure: S56-10.6-HERMETIC-COLD-BUILD")
