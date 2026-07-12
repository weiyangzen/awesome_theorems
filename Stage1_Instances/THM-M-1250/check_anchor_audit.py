#!/usr/bin/env python3
"""Verify the immutable local evidence recorded by the THM-M-1250 audit."""

import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
mathlib_entry = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_entry["rev"] == env["mathlib_revision"]

basic = (MATHLIB / "Mathlib/Analysis/Distribution/SchwartzSpace/Basic.lean").read_text(
    encoding="utf-8"
)
require(basic, "structure SchwartzMap where", "bundled Schwartz definition")
require(basic, "smooth' : ContDiff ℝ ∞ toFun", "smoothness field")
require(
    basic,
    "decay' : ∀ k n : ℕ, ∃ C : ℝ, ∀ x, ‖x‖ ^ k * ‖iteratedFDeriv ℝ n toFun x‖ ≤ C",
    "rapid-decay field",
)
require(basic, "theorem smooth (f : 𝓢(E, F))", "smooth projection theorem")
require(basic, "theorem decay (f : 𝓢(E, F))", "decay projection theorem")
require(basic, "theorem le_seminorm", "pointwise-to-seminorm anchor")
require(basic, "theorem seminorm_le_bound", "seminorm bound anchor")

assert audit["root_decision"]["classification"] == "M1"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is True
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: mathlib pin/worktree/source candidates match; "
    "root remains M1 and theorem_complete=false"
)
