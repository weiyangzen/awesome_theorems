#!/usr/bin/env python3
"""Fail-closed reconciliation check for the THM-M-0400 release decision."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0400"


def fail(message: str) -> None:
    raise SystemExit(f"release reconciliation failed: {message}")


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((OWNED / name).read_bytes()).hexdigest()


release = load("release-receipt.json")
tree = load("obligation-tree.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")

if release.get("item_id") != "S56-M-0400-RELEASE":
    fail("release item identity mismatch")
if release.get("depends_on") != ["S56-M-0400-VALIDATION"]:
    fail("validation dependency mismatch")

expected_inputs = {
    "intake_sha256": "intake.json",
    "statement_record_sha256": "statement.json",
    "anchor_audit_sha256": "anchor-audit.json",
    "obligation_tree_sha256": "obligation-tree.json",
    "proof_receipt_sha256": "proof-receipt.json",
    "validation_receipt_sha256": "validation-receipt.json",
    "validation_specs_sha256": "validation-specs.json",
}
for key, name in expected_inputs.items():
    actual = digest(name)
    if release.get("reconciled_inputs", {}).get(key) != actual:
        fail(f"stale or unbound release input: {name}")

decision = release.get("decision", {})
if decision.get("verdict") != "blocked":
    fail("open root must yield a blocked release verdict")
if decision.get("lifecycle_before") != "planned" or decision.get("lifecycle_after") != "planned":
    fail("release decision must not advance lifecycle")
if decision.get("audit_complete") is not False or decision.get("theorem_complete") is not False:
    fail("release decision falsely reports a terminal result")
if decision.get("root_closed") is not False or decision.get("accepted_receipt_ids") != []:
    fail("release decision falsely reports root closure or acceptance")

root_vector = {"H": "H1", "M": "M3", "R": "R3"}
if decision.get("root_vector_before") != root_vector or decision.get("root_vector_after") != root_vector:
    fail("release decision changed the reconciled root vector")
if tree.get("root_vector") != root_vector or tree.get("theorem_complete") is not False:
    fail("obligation tree does not support the blocked decision")
if tree.get("denominators", {}).get("closed_machine_ids") != []:
    fail("obligation tree unexpectedly claims machine closure")
if proof.get("closed_obligation_ids") != [] or proof.get("theorem_complete") is not False:
    fail("proof receipt unexpectedly supports release")
result = validation.get("result", {})
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("validation receipt unexpectedly supports release")
if validation.get("support_state") != "provisional_worker_selftest":
    fail("validation receipt is not correctly classified as provisional")

required_cut = {
    "M0400-N-COEFFICIENT-FIELD",
    "M0400-N-TRANSPORT",
    "M0400-C-AUXILIARY",
    "M0400-L-NONVANISH",
    "M0400-L-GAP",
    "M0400-C-SUBSPACE",
    "M0400-L-FINITE-COVER",
    "M0400-T-COMPOSE",
    "M0400-X-FOUNDATION",
    "M0400-X-SOURCE",
}
if set(release.get("remaining_root_cut_set", [])) != required_cut:
    fail("remaining root cut set is incomplete or changed")

completed = subprocess.run(
    ["python3", str(OWNED / "check_validation.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
    timeout=180,
)
if completed.returncode != 0:
    fail(f"prerequisite validation replay failed:\n{completed.stdout}{completed.stderr}")
if "root remains M3/open" not in completed.stdout:
    fail("prerequisite replay did not attest the open root")

print("release reconciliation ok: evidence is current; verdict blocked; AUDIT-Z=false; THEOREM-Z=false")
