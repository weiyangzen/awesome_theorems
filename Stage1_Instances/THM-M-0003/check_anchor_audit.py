#!/usr/bin/env python3
"""Validate immutable local facts in the THM-M-0003 anchor ledger."""

import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

mathlib = next(c for c in audit["candidates"] if c["id"] == "M0003-A-MATHLIB-SNAKE")
source = MATHLIB / mathlib["file"]
assert sha256(source) == mathlib["source_sha256"]
text = source.read_text(encoding="utf-8")
for needle in (
    "structure SnakeInput where",
    "noncomputable def d :",
    "lemma L0_exact",
    "lemma L1'_exact",
    "lemma L2'_exact",
    "lemma L3_exact",
    "lemma snake_lemma : S.composableArrows.Exact :=",
):
    # Source uses Unicode subscripts and delta; compare an ASCII-normalized view.
    normalized = text.translate(str.maketrans("δ₀₁₂₃", "d0123"))
    assert needle in normalized, needle

legacy = next(c for c in audit["candidates"] if c["id"] == "M0003-A-LEGACY-WRAPPER")
assert sha256(ROOT / legacy["file"]) == legacy["source_sha256"]
assert audit["root_decision"]["classification"] == "M1"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

print("anchor ledger verified: immutable mathlib source and legacy hash match; root=M1")
