#!/usr/bin/env python3
"""Verify the immutable local anchors and fail-closed audit classification."""

import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

source = (MATHLIB / "Mathlib/Probability/Kernel/Composition/Comp.lean").read_text()
assert "theorem pow_add (kappa".replace("kappa", "κ") in source
assert "theorem pow_add_apply_eq_lintegral (κ" in source
assert "κ ^ (m + n) = (κ ^ m) ∘ₖ (κ ^ n) := _root_.pow_add κ m n" in source
assert "rw [add_comm]; simp [pow_add, comp_apply' _ _ _ hs]" in source
assert "sorry" not in source

assert audit["root_decision"]["classification"] == "M0-P candidate"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is True
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: pinned mathlib revision and clean worktree match; "
    "exact kernel and integral bridges recorded; audit complete; theorem incomplete"
)
