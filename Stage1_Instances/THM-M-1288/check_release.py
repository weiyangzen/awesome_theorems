#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1288 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1288"

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

decision = load(HERE / "release-decision.json")
validation = load(HERE / "validation-receipt.json")
graphs = load(HERE / "typed-graphs.json")
intake = load(HERE / "intake.json")
targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

target = next(x for x in targets["targets"] if x["theorem_id"] == "THM-M-1288")
assert target["execution_rank"] == 459
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
assert decision["item_id"] == "S56-M-1288-RELEASE"
assert decision["theorem_id"] == "THM-M-1288" and decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-1288-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False

items = {item["id"]: item for item in dag["items"]}
assert items["S56-M-1288-VALIDATION"]["state"] == "[_]"
assert items["S56-M-1288-RELEASE"]["state"] == "[ ]"
result = validation["result"]
boundary = graphs["closure_boundary"]
assert result["root_kernel_closed"] is False and result["root_machine_debt"] == "M3"
assert result["audit_complete"] is False and result["theorem_complete"] is False
assert boundary["root_closed"] is False
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
assert decision["remaining_root_cut_set"] == result["remaining_root_cut_set"]
assert decision["remaining_root_cut_set"] == boundary["remaining_root_cut_set"]
assert decision["root_vector"]["accepted_before"] == ["H1", "M4", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M4", "R3"]
assert decision["root_vector"]["best_provisional_evidence"] == ["H1", "M3", "R3"]
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"

for name, expected in decision["input_hashes"].items():
    assert sha256(HERE / name) == expected, name
required = ("master acceptance", "kernel closure", "accepted AUDIT-Z", "accepted H0",
            "accepted R0", "empty-cache network-denied cold replay", "SBOM and license",
            "independently provisioned runners", "minimal release verifier",
            "deterministic content-addressed release bundle")
release_cut = "\n".join(decision["release_gate_cut_set"])
for fragment in required:
    assert fragment in release_cut, fragment

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=150, check=False,
)
assert replay.returncode == 0, replay.stdout
assert "open: exact root remains M3" in replay.stdout
assert "blocked: cold empty-cache hermetic replay" in replay.stdout

print("ok: release decision is bound to the provisional validation receipt")
print("open: exact root M3 with admissibility and optimality packages unproved")
print("open: audit H1/R3; AUDIT-Z and THEOREM-Z are false")
print("blocked: dependency, hermetic, supply-chain, independent-verifier, bundle, and master gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false")
