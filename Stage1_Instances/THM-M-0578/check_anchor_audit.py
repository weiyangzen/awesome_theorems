#!/usr/bin/env python3
"""Verify the pinned source boundary and structured THM-M-0578 audit ledger."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"
BATTERIES = LEAN_ROOT / ".lake/packages/batteries"
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

def git_head(path: Path) -> str:
    return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()

assert AUDIT["item_id"] == "S56-M-0578-ANCHOR_AUDIT"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["machine_debt"] == "formalization_debt"
assert AUDIT["theorem_proved"] is False and AUDIT["theorem_complete"] is False
packages = {p["name"]: p["rev"] for p in MANIFEST["packages"]}
env = AUDIT["immutable_environment"]
assert packages["mathlib"] == env["mathlib_revision"] == git_head(MATHLIB)
assert packages["batteries"] == env["batteries_revision"] == git_head(BATTERIES)

source_path = MATHLIB / "Mathlib/Geometry/Manifold/PoincareConjecture.lean"
source = source_path.read_text()
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == env["mathlib_source_sha256"]
assert "proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven :" in source
assert "IsEmpty (M ≃ₘ⟮𝓡 7, 𝓡 7⟯ 𝕊⁷)" in source

proof_wanted = (BATTERIES / "Batteries/Util/ProofWanted.lean").read_text()
assert "withoutModifyingEnv do" in proof_wanted
assert "axiom helper {α : Sort _} : α" in proof_wanted
assert "but it's then removed from the environment" in proof_wanted
candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0578-A-MATHLIB-MARKER")
assert candidate["revision"] == packages["mathlib"]
assert candidate["classification"] == "M4_statement_only"

print("ok: exact proof_wanted marker and discard semantics verified at pins; root=M4 formalization_debt")
