#!/usr/bin/env python3
"""Validate the immutable, locally checkable parts of the anchor ledger."""

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


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

candidate = next(c for c in audit["candidates"] if c["id"] == "M0001-A-MATHLIB-EXACTNESS-FAMILY")
source = MATHLIB / candidate["file"]
assert sha256(source) == candidate["source_sha256"]
text = source.read_text(encoding="utf-8")
for needle in (
    "noncomputable def δ",
    "lemma homology_exact₁",
    "lemma homology_exact₂",
    "lemma homology_exact₃",
    "by_cases h : c.Rel i (c.next i)",
):
    assert needle in text, needle

legacy = next(c for c in audit["candidates"] if c["id"] == "M0001-A-LEGACY-WRAPPER")
assert sha256(ROOT / legacy["file"]) == legacy["source_sha256"]
assert audit["root_decision"]["classification"] == "M1"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

print("anchor ledger verified: immutable mathlib source and legacy candidate match; root=M1")
