#!/usr/bin/env python3
"""Verify the immutable local and external inputs to the THM-M-0392 audit."""

import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT_PATH = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


with AUDIT_PATH.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
manifest_digest = hashlib.sha256((LEAN_ROOT / "lake-manifest.json").read_bytes()).hexdigest()
assert manifest_digest == env["lake_manifest_sha256"]

affine = (MATHLIB / "Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Basic.lean").read_text()
normal = (MATHLIB / "Mathlib/AlgebraicGeometry/EllipticCurve/NormalForms.lean").read_text()
northcott = (MATHLIB / "Mathlib/NumberTheory/Height/Northcott.lean").read_text()
require(affine, "def Equation (x y : R) : Prop", "affine equation object")
require(affine, "lemma equation_iff (x y : R)", "affine equation normalization")
require(normal, "class IsShortNF : Prop", "short Weierstrass normal form")
require(normal, "theorem Δ_of_isShortNF", "short-form discriminant theorem")
require(northcott, "class Northcott", "conditional Northcott infrastructure")

revision = "baba2049f3bfe4d2cc184f8205997333e7c58638"
external = next(candidate for candidate in audit["candidates"] if candidate["id"] == "M0392-A-LEAN3-MORDELL")
assert external["revision"] == revision
assert external["toolchain"] == "leanprover-community/lean:3.49.1"
assert external["mathlib_revision"] == "cf9386b56953fb40904843af98b7a80757bbe7f9"
assert external["declarations"] == [
    "Mordell_minus1",
    "Mordell_minus2",
    "Mordell_minus5",
    "Mordell_minus6",
    "Mordell_minus13",
]

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is True
assert audit["theorem_complete"] is False
print(
    "anchor audit verified: mathlib pin and source anchors match; "
    f"Lean 3 Mordell source {revision} is fixed-parameter only; root=M2"
)
