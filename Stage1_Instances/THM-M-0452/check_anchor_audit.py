#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0452-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0452"
assert AUDIT["exact_target"] == "Stage1Instances.THM_M_0452.NeronTatePairingTarget"
decision = AUDIT["decision"]
assert decision["frozen_inventory_candidate_ids"] == decision["classified_candidate_ids"]
assert len(decision["frozen_inventory_candidate_ids"]) == 4
assert decision["root_machine_classification"] == "M3"
assert decision["exact_external_closure_found"] is False
assert decision["theorem_proved"] is False
assert decision["theorem_complete"] is False

mathlib_pin = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0452-MATHLIB-SUBSTRATE")
assert candidate["revision"] == mathlib_pin["rev"]
mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == candidate["revision"]
for record in candidate["files"]:
    if record["sha256"] is not None:
        digest = hashlib.sha256((mathlib_root / record["path"]).read_bytes()).hexdigest()
        assert digest == record["sha256"]
    blob = subprocess.run(
        ["git", "-C", str(mathlib_root), "hash-object", record["path"]],
        check=True, capture_output=True, text=True
    ).stdout.strip()
    assert blob == record["git_blob"]

statement = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0452-LOCAL-EXACT-STATEMENT")
assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == statement["source_sha256"]
probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in candidate["declarations"]:
    assert declaration in probe
assert "theorem NeronTatePairingTarget" not in probe

print("ok: 4/4 candidates classified; statement, mathlib hashes and blobs, pin, and anchor probes verified; root remains M3")
