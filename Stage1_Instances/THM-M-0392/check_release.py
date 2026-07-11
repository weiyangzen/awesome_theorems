#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0392 release decision."""

import hashlib
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0392"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
nodes = load("obligation-nodes.json")
tasks = load("tasks.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0392"), None)
if target is None or target["execution_rank"] != 2:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the fail-closed decision")
assurance = instance.get("assurance", {})
if instance.get("lifecycle_mode") != "planned" or assurance.get("theorem_complete") is not False:
    fail("instance authority no longer has the recorded planned/open state")
if [assurance.get("human_debt"), assurance.get("machine_debt"), assurance.get("readability_debt")] != ["H5", "M4", "R4"]:
    fail("accepted root vector drifted")

if decision.get("item_id") != "S56-M-0392-RELEASE" or decision.get("verdict") != "blocked":
    fail("release decision has the wrong item or verdict")
if decision.get("lifecycle_before") != "planned" or decision.get("lifecycle_after") != "planned":
    fail("a blocked worker decision must not promote lifecycle")
terminal = decision.get("terminal_decisions", {})
if terminal.get("audit_complete") is not False or terminal.get("theorem_complete") is not False:
    fail("open assurance gates require both terminal booleans to remain false")
if decision.get("accepted_receipt_ids"):
    fail("worker-provisional receipts must not be represented as accepted")

dependency = decision.get("dependency", {})
if dependency.get("item_id") != validation.get("item_id"):
    fail("release dependency does not identify the validation receipt")
if validation.get("support_state") != "provisional_worker_selftest" or dependency.get("master_accepted") is not False:
    fail("validation evidence is not eligible for release dependency acceptance")
if dependency.get("receipt_sha256") != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
validation_task = next((task for task in tasks.get("tasks", []) if task.get("id") == "S56-M-0392-VALIDATION"), None)
if validation_task is None or validation_task.get("status") != "open":
    fail("task authority no longer records the validation dependency as open")

registry_ids = {entry["obligation_id"] for entry in registry.get("obligations", [])}
node_ids = {entry["obligation_id"] for entry in nodes.get("nodes", [])}
if len(registry_ids) != 8 or registry_ids != node_ids:
    fail("frozen eight-obligation denominator drifted")
expected_closed = {"M0392-C-CURVE", "M0392-L-NONSINGULAR", "M0392-T-COORDINATES"}
if set(proof.get("closed_obligation_ids", [])) != expected_closed:
    fail("proof receipt partial closure boundary drifted")
result = validation.get("result", {})
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("validation no longer supports an open-root release decision")
reconciliation = decision.get("evidence_reconciliation", {})
if set(reconciliation.get("closed_obligation_ids", [])) != expected_closed:
    fail("release reconciliation overstates or understates partial closure")
if reconciliation.get("open_root_relevant_obligation_count") != 5:
    fail("release reconciliation has the wrong open-obligation count")

required_cut_fragments = (
    "authoritative disambiguation",
    "M0392-X-SIEGEL",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision.get("remaining_root_cut_set", []))
for fragment in required_cut_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "exact_root_kernel_check",
    "integral_points_terminal_body",
    "root_composition",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

print(
    "release-decision: ok (blocked; dependency unaccepted; source ambiguous; "
    "root open with 5 obligations; audit_complete=false; theorem_complete=false)"
)
