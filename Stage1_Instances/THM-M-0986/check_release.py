#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0986 release decision."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0986"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)

target = next(
    (entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0986"),
    None,
)
if target is None or target["execution_rank"] != 266:
    fail("target membership or rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the recorded open state")

if decision["item_id"] != "S56-M-0986-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker reconciliation must not advance lifecycle")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open and unaccepted evidence cannot support a terminal decision")
if decision["accepted_receipt_ids"]:
    fail("worker evidence was represented as accepted")

for name, expected in decision["reconciled_inputs"].items():
    if digest(name) != expected:
        fail(f"reconciled input drifted: {name}")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation receipt identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation receipt hash mismatch")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation evidence support state drifted")
if dependency["master_accepted"] is not False:
    fail("worker cannot claim dependency acceptance")

result = validation["result"]
if result["root_closed"] is not True or result["theorem_complete"] is not False:
    fail("validation root/completion boundary changed")
boundary = graphs["closure_boundary"]
if boundary["root_closed"] is not False or boundary["theorem_complete"] is not False:
    fail("frozen graph no longer records its pre-proof open boundary")
if decision["root_vector"]["before"] != ["H1", "M3", "R3"]:
    fail("root vector does not match the frozen graph")
if decision["root_vector"]["after"] != decision["root_vector"]["before"]:
    fail("release silently changed the root vector")

required_fragments = (
    "master acceptance",
    "frozen obligation graph",
    "H0 primary-source",
    "R0 node-by-node",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
    timeout=180,
    check=False,
)
if replay.returncode != 0:
    fail(f"validation replay failed:\n{replay.stdout}{replay.stderr}")

print(
    "release-decision: ok (blocked; validation unaccepted; frozen H1/M3/R3; "
    "AUDIT-Z=false; THEOREM-Z=false)"
)
