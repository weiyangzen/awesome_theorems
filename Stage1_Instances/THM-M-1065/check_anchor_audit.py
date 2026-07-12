#!/usr/bin/env python3
"""Check the immutable local evidence and fail-closed anchor decision."""

import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKAGES = ROOT / "Formalizations" / "Lean" / ".lake" / "packages"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

mathlib = PACKAGES / "mathlib"
expected = audit["immutable_environment"]["mathlib_revision"]
assert output("git", "rev-parse", "HEAD", cwd=mathlib) == expected
assert output("git", "status", "--short", cwd=mathlib) == ""

gaussian = (mathlib / "Mathlib/Probability/Distributions/Gaussian/Real.lean").read_text()
independence = (mathlib / "Mathlib/Probability/Independence/Basic.lean").read_text()
assert "def gaussianReal" in gaussian
assert "def iIndepFun" in independence
assert audit["canonical_target_expression_sha256"] == (
    "b257ceb188a0b84aab11fd389b5df322129c283dbc38f5c226900a4fec5cebd0"
)
assert all(not candidate.get("declarations") or candidate["id"] == "M1065-A-MATHLIB-SUBSTRATE"
           for candidate in audit["candidates"])
assert audit["root_decision"]["classification"] == "M3"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: pinned mathlib revision and substrate declarations match; "
    "no terminal exact candidate is credited; root=M3"
)
