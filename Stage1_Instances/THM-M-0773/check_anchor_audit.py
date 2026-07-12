#!/usr/bin/env python3
"""Verify the immutable mathlib anchor and fail-closed audit decisions."""

import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
SOURCE = MATHLIB / "Mathlib" / "Order" / "TeichmullerTukey.lean"
ZORN = MATHLIB / "Mathlib" / "Order" / "Zorn.lean"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
assert digest(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
assert digest(LEAN_ROOT / "lean-toolchain") == env["toolchain_file_sha256"]

candidate = next(c for c in audit["candidates"] if c["id"] == "M0773-A-MATHLIB-POINTED")
assert digest(SOURCE) == candidate["source_sha256"]
text = SOURCE.read_text(encoding="utf-8")
assert "theorem IsOfFiniteCharacter.exists_maximal" in text
assert "refine zorn_subset_nonempty F" in text
assert all(marker not in text and marker not in ZORN.read_text(encoding="utf-8") for marker in ("sorry", "admit", "\naxiom ", "unsafe"))

assert candidate["classification"] == "M0-W"
assert candidate["evidence_level"] == "E1"
assert audit["root_decision"]["classification"] == "M0-W"
assert audit["root_decision"]["kernel_closed"] is True
assert audit["audit_phase_complete"] is True
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: immutable mathlib source/body and clean pin match; "
    "exact wrapper evidence is M0-W/E1; theorem_complete=false"
)
