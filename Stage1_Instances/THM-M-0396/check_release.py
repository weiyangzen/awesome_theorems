#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0396 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0396"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0396"), None)
if target is None or target["execution_rank"] != 9:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the fail-closed decision")

if decision.get("item_id") != "S56-M-0396-RELEASE" or decision.get("verdict") != "blocked":
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
if validation.get("support_state") != "provisional_worker_selftest":
    fail("validation evidence is not worker-provisional")
if dependency.get("master_accepted") is not False:
    fail("worker-provisional validation was represented as master accepted")
if dependency.get("receipt_sha256") != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")

registry_ids = {entry["obligation_id"] for entry in registry.get("obligations", [])}
nodes = {entry["obligation_id"]: entry for entry in graphs.get("nodes", [])}
if len(registry_ids) != 15 or registry_ids != set(nodes):
    fail("frozen 15-obligation registry and typed graph drifted")
if registry.get("root_obligation_id") != "M0396-ROOT":
    fail("canonical root identity drifted")
root = nodes["M0396-ROOT"]
if [root.get(k) for k in ("human_debt", "machine_debt", "readability_debt")] != ["H1", "M3", "R3"]:
    fail("frozen dossier root vector drifted")

if proof.get("closed_obligation_ids") != ["M0396-N1"]:
    fail("proof receipt closure boundary drifted")
result = validation.get("result", {})
if result.get("validated_closed_obligation_ids") != ["M0396-N1"]:
    fail("validation receipt closure boundary drifted")
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("validation no longer supports an open-root release decision")
reconciliation = decision.get("evidence_reconciliation", {})
if reconciliation.get("worker_receipt_closed_obligation_ids") != ["M0396-N1"]:
    fail("release reconciliation lost the partial normalization evidence")
if reconciliation.get("accepted_closed_obligation_ids") != []:
    fail("provisional closure was represented as accepted")
if reconciliation.get("accepted_open_root_relevant_obligation_count") != 15:
    fail("release reconciliation has the wrong accepted open-obligation count")

required_cut_fragments = (
    "master acceptance", "M0396-N2", "M0396-C1", "M0396-L1",
    "M0396-T", "H0 primary-source", "R0 structured",
    "empty-cache network-denied cold build", "two signed attestations",
    "minimal release verifier", "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision.get("remaining_root_cut_set", []))
for fragment in required_cut_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "exact_root_kernel_check", "baker_matveev_terminal_proof_body",
    "hermetic_release_reproduction", "independent_release_verification",
    "human_source_acceptance", "readability_acceptance", "release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

print(
    "release-decision: ok (blocked; dependency unaccepted; root H1/M3/R3; "
    "only M0396-N1 provisionally closed; audit_complete=false; theorem_complete=false)"
)
