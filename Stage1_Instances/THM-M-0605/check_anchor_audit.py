#!/usr/bin/env python3
"""Verify THM-M-0605's pinned anchor inventory and source boundary."""

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
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


assert AUDIT["item_id"] == "S56-M-0605-ANCHOR_AUDIT"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["machine_debt"] == "formalization_debt"
assert AUDIT["theorem_proved"] is False and AUDIT["theorem_complete"] is False

packages = {p["name"]: p["rev"] for p in MANIFEST["packages"]}
env = AUDIT["immutable_environment"]
assert packages["mathlib"] == env["mathlib_revision"] == git_head(MATHLIB)
assert packages["batteries"] == env["batteries_revision"] == git_head(BATTERIES)

mathlib_source = MATHLIB / "Mathlib/Geometry/Manifold/PoincareConjecture.lean"
batteries_source = BATTERIES / "Batteries/Util/ProofWanted.lean"
assert hashlib.sha256(mathlib_source.read_bytes()).hexdigest() == env["mathlib_source_sha256"]
assert hashlib.sha256(batteries_source.read_bytes()).hexdigest() == env["proof_wanted_source_sha256"]

source = mathlib_source.read_text()
assert "proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven :" in source
assert "IsEmpty (M ≃ₘ⟮𝓡 7, 𝓡 7⟯ 𝕊⁷)" in source

proof_wanted = batteries_source.read_text()
assert "withoutModifyingEnv do" in proof_wanted
assert "axiom helper {α : Sort _} : α" in proof_wanted
assert "but it's then removed from the environment" in proof_wanted

candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0605-A-MATHLIB-MARKER")
assert candidate["revision"] == packages["mathlib"]
assert candidate["classification"] == "M4_statement_only"

print("ok: pinned exact marker, discard semantics, and M4 formalization-debt boundary verified")
