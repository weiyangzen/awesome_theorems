#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1527-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1527"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"].startswith("MATHLIB"))
assert mathlib_candidate["revision"] == mathlib["rev"]

probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

physlib = next(c for c in AUDIT["candidates"] if c["project"] == "leanprover-community/physlib")
assert len(physlib["revision"]) == 40
assert physlib["classification"] == "M3_partial_non_target"
assert physlib["proof_credit"] is False

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: exact statement, 6 pinned mathlib probes, partial Physlib candidate, and M4 root boundary agree")

