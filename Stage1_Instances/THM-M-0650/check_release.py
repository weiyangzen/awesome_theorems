#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0650-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0650"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
instance = load("instance.json")
graphs = load("typed-graphs.json")
spec = load("release-spec.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())

target = next(t for t in targets["targets"] if t["theorem_id"] == "THM-M-0650")
assert target["execution_rank"] == 696
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}

assert spec["item_id"] == decision["item_id"] == "S56-M-0650-RELEASE"
assert spec["theorem_id"] == decision["theorem_id"] == "THM-M-0650"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == instance["root_vector"]
assert decision["terminal_decisions"] == {"audit_complete": False, "theorem_complete": False}
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0650-VALIDATION"
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["master_accepted"] is False
assert decision["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"

assert validation["release_grade"] is False
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["stale_structured_cut_set"] == ["M0650-T-EMBEDDING"]
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M0650-T-EMBEDDING"]

reconciliation = decision["evidence_reconciliation"]
for gate in (
    "authoritative_graph_freshness", "human_source_acceptance",
    "readability_acceptance", "hermetic_release_reproduction",
    "independent_release_verification", "deterministic_release_bundle",
    "master_acceptance",
):
    assert reconciliation[gate] == "missing"

result = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT,
    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=150,
)
assert result.returncode == 0, result.stdout
assert "exact Tarski-Vaught statement and proof wrappers elaborated" in result.stdout
assert "blocked: cold empty-cache hermetic replay" in result.stdout

receipt_path = HERE / "release-receipt.json"
if receipt_path.exists():
    receipt = load("release-receipt.json")
    assert receipt["inputs"]["release_spec_sha256"] == sha256("release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256("release-decision.json")
    assert receipt["inputs"]["validation_receipt_sha256"] == sha256("validation-receipt.json")
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["release_grade"] is False

print("PASS S56-M-0650-RELEASE blocked: dependency unaccepted; audit and theorem completion false")
