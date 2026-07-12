#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0652 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0652"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
intake = load("intake.json")
registry = load("obligation-registry.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((x for x in targets["targets"] if x["theorem_id"] == "THM-M-0652"), None)
if target is None or target["execution_rank"] != 298:
    fail("target membership or rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the fail-closed decision")
if intake["lifecycle_mode"] != "planned" or intake["theorem_complete"] is not False:
    fail("instance intake no longer records the planned, incomplete state")

if decision["item_id"] != "S56-M-0652-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker reconciliation must not promote lifecycle")
if decision["accepted_receipt_ids"]:
    fail("provisional evidence was represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open audit and theorem gates require false terminal booleans")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("release dependency does not match validation receipt")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation receipt identity drifted")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation receipt digest drifted")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation support state is not provisional worker evidence")
if validation["release_grade"] is not False or dependency["master_accepted"] is not False:
    fail("validation evidence is not eligible for release acceptance")

result = validation["result"]
if result["machine_root_closed"] is not False or result["theorem_complete"] is not False:
    fail("validation no longer records an open exact root")
expected_cut = ["M0652-B-COMPLETENESS", "M0652-T-SYNTACTIC", "M0652-B-SOUNDNESS"]
if result["remaining_root_cut_set"] != expected_cut:
    fail("validation root cut set drifted")
if decision["remaining_root_cut_set"] != expected_cut:
    fail("release decision does not preserve the validated root cut set")
if registry["root_obligation_id"] != "M0652-ROOT":
    fail("canonical root identity drifted")

reconciliation = decision["evidence_reconciliation"]
if reconciliation["machine_root_closed"] is not False:
    fail("release reconciliation silently closed the root")
if reconciliation["accepted_closed_obligation_ids"]:
    fail("partial worker checks were promoted to accepted obligations")
for key in (
    "exact_root_kernel_check",
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "release_bundle",
):
    if reconciliation[key] != "missing":
        fail(f"release blocker {key!r} was silently cleared")
if reconciliation["root_composition"] != "conditional_only":
    fail("conditional composition boundary drifted")

required_fragments = (
    "H0 primary-source",
    "R0 anchored",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
release_gates = "\n".join(decision["remaining_release_gates"])
for fragment in required_fragments:
    if fragment not in release_gates:
        fail(f"remaining release gates omit {fragment!r}")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=150,
    check=False,
)
if replay.returncode != 0:
    fail(f"upstream validation replay failed:\n{replay.stdout}")
if "general Craig interpolation root remains M3" not in replay.stdout:
    fail("upstream replay did not preserve the open-root boundary")

print("release-decision: ok (blocked; validation unaccepted; exact root M3)")
print("audit_complete=false; theorem_complete=false")
print("root cut: M0652-B-COMPLETENESS, M0652-T-SYNTACTIC, M0652-B-SOUNDNESS")
