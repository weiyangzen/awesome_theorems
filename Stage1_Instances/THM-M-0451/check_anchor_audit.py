#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0451-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0451"
assert AUDIT["exact_target"] == "Stage1Instances.THM_M_0451.NeronTateCanonicalHeightTarget"
decision = AUDIT["decision"]
assert decision["frozen_inventory_candidate_ids"] == decision["classified_candidate_ids"]
assert len(decision["frozen_inventory_candidate_ids"]) == 4
assert decision["root_machine_classification"] == "M3"
assert decision["exact_external_closure_found"] is False
assert decision["theorem_proved"] is False
assert decision["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0451-MATHLIB-SUBSTRATE")
assert candidate["revision"] == mathlib["rev"]
mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == candidate["revision"]
for record in candidate["files"]:
    digest = hashlib.sha256((mathlib_root / record["path"]).read_bytes()).hexdigest()
    assert digest == record["sha256"]

statement = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0451-LOCAL-EXACT-STATEMENT")
assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == statement["source_sha256"]
probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in candidate["declarations"]:
    assert declaration in probe
assert "theorem NeronTateCanonicalHeightTarget" not in probe

print("ok: 4/4 candidates classified; statement and 3 mathlib source hashes verified; pinned anchor probes present; root remains M3")
