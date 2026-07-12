#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1289-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1289"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
receipt = load("validation-receipt.json")
proof = load("proof.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(item for item in targets["targets"] if item["theorem_id"] == "THM-M-1289")

assert target["execution_rank"] == 460
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert decision["item_id"] == "S56-M-1289-RELEASE"
assert decision["theorem_id"] == "THM-M-1289"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H2", "M4", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M4", "R3"]

dependency = decision["dependency"]
assert dependency["item_id"] == receipt["item_id"] == "S56-M-1289-VALIDATION"
assert dependency["receipt_id"] == receipt["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["support_state"] == receipt["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is receipt["release_grade"] is False
assert dependency["master_accepted"] is False

open_cut = {"M1289-L-PDE", "M1289-L-FUN-NORM", "M1289-L-GRAD-NORM", "M1289-T-EXTREMAL"}
assert set(decision["minimal_mathematical_open_root_cut_set"]) == open_cut
assert set(receipt["result"]["minimal_mathematical_open_root_cut_set"]) == open_cut
assert receipt["result"]["root_kernel_closed"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert proof["theorem_proved"] is False and proof["theorem_complete"] is False
assert set(proof["remaining_component_premises"]) == {
    "PDEComponent", "FunctionNormComponent", "GradientNormComponent", "ExtremalComponent"
}
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
assert len(decision["remaining_release_cut_set"]) >= 10

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=150,
    check=False,
)
assert replay.returncode == 0, replay.stdout
assert "open: exact root retains PDE" in replay.stdout
assert "blocked: cold empty-cache hermetic replay" in replay.stdout

print("ok: provisional validation receipt is content-bound and replayed")
print("open: exact root retains four analytic component premises")
print("blocked: dependency acceptance, AUDIT-Z, hermetic, and independent release gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; accepted receipts=[]")
