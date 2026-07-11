#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0085-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0085"
assert AUDIT["audit_complete"] is True
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert AUDIT["gate_state"] == "self_tested_pending_master_acceptance"

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
pin = AUDIT["immutable_environment"]["mathlib_revision"]
assert mathlib["rev"] == pin
installed = subprocess.check_output(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"), "rev-parse", "HEAD"],
    text=True,
).strip()
assert installed == pin

candidates = {c["candidate_id"]: c for c in AUDIT["candidates"]}
exact = candidates["S56-M-0085-C02"]
assert exact["revision"] == pin
assert exact["declaration"] == "CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers"
assert exact["classification"] == "M0-P candidate anchor"
assert "eqv" in exact["exact_projection"]
assert "no repo-local integration blocker" in AUDIT["integration_decision"]
assert "does not own the canonical proof wrapper" in AUDIT["status_boundary"]

source = (ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/CategoryTheory/Monad/Monadicity.lean").read_text()
assert "def monadicOfCreatesGSplitCoequalizers" in source
assert "exact monadicOfHasPreservesReflectsGSplitCoequalizers adj" in source

print(f"anchor audit ok: exact pinned candidate at mathlib {pin}")
