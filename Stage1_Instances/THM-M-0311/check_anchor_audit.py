#!/usr/bin/env python3
"""Verify the immutable local sources and structured THM-M-0311 anchor ledger."""

import json
import pathlib
import re
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
HERE = pathlib.Path(__file__).resolve().parent


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


with (HERE / "anchor-audit.json").open(encoding="utf-8") as stream:
    audit = json.load(stream)

assert audit["item_id"] == "S56-M-0311-ANCHOR_AUDIT"
assert audit["canonical_target"] == "Stage1Instances.THM_M_0311.RieszFischerTarget"
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == audit["immutable_environment"]["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

complete = (MATHLIB / "Mathlib/MeasureTheory/Function/LpSpace/Complete.lean").read_text()
assert "instance instCompleteSpace [CompleteSpace E] [hp : Fact (1 ≤ p)]" in complete
assert "completeSpace_lp_of_cauchy_complete_eLpNorm fun _f hf _B hB h_cau =>" in complete
assert "cauchy_complete_eLpNorm hp.elim hf hB.ne h_cau" in complete
assert not re.search(r"\b(sorry|admit|unsafe)\b|^\s*axiom\b", complete, re.MULTILINE)

lp_sequence = (MATHLIB / "Mathlib/Analysis/Normed/Lp/lpSpace.lean").read_text()
assert "instance completeSpace : CompleteSpace (lp E p)" in lp_sequence

wrapper = (HERE / "AnchorAudit.lean").read_text()
statement = (HERE / "Statement.lean").read_text()
target_body = """forall (α : Type u) [MeasurableSpace α] (μ : Measure α),
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) ∧
      CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ)"""
assert target_body in statement
assert target_body in wrapper
assert "theorem rieszFischerTarget_of_pinned_mathlib : AnchorAuditTarget.{u}" in wrapper
assert "constructor <;> infer_instance" in wrapper
assert audit["root_decision"]["classification"] == "M0-P candidate"
assert audit["root_decision"]["kernel_closed_in_anchor_probe"] is True
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: immutable mathlib pin, exact Lp completeness body, "
    "placeholder-free source, exact wrapper, and fail-closed status match"
)
