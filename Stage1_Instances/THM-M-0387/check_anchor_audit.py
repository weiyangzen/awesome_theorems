#!/usr/bin/env python3
"""Verify immutable local and external anchors used by the audit ledger."""

import json
import pathlib
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
PACKAGES = LEAN_ROOT / ".lake" / "packages"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=PACKAGES / "mathlib") == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD", cwd=PACKAGES / "flt-regular") == env["flt_regular_revision"]
assert output("git", "status", "--short", cwd=PACKAGES / "mathlib") == ""
assert output("git", "status", "--short", cwd=PACKAGES / "flt-regular") == ""

basic = (PACKAGES / "mathlib/Mathlib/NumberTheory/FLT/Basic.lean").read_text()
three = (PACKAGES / "mathlib/Mathlib/NumberTheory/FLT/Three.lean").read_text()
four = (PACKAGES / "mathlib/Mathlib/NumberTheory/FLT/Four.lean").read_text()
regular = (PACKAGES / "flt-regular/FltRegular/FltRegular.lean").read_text()
require(basic, "def FermatLastTheorem : Prop", "mathlib root statement")
require(three, "theorem fermatLastTheoremThree : FermatLastTheoremFor 3", "exponent-three anchor")
require(four, "theorem fermatLastTheoremFour : FermatLastTheoremFor 4", "exponent-four anchor")
require(four, "theorem FermatLastTheorem.of_odd_primes", "conditional root assembly")
require(regular, "theorem flt_regular", "regular-prime anchor")

imperial_revision = next(
    candidate["revision"]
    for candidate in audit["candidates"]
    if candidate["id"] == "M0387-A-IMPERIAL-FULL"
)
base = f"https://raw.githubusercontent.com/ImperialCollegeLondon/FLT/{imperial_revision}"


def remote(path: str) -> str:
    with urllib.request.urlopen(f"{base}/{path}", timeout=30) as response:
        return response.read().decode()


proof = remote("FLT/Proof.lean")
toolchain = remote("lean-toolchain").strip()
manifest = json.loads(remote("lake-manifest.json"))
require(proof, "theorem B4_proof : B4 :=\n  sorry", "direct full-root proof gap")
require(proof, "theorem B1_proof : B1 := B2_implies_B1 B2_proof", "transitive root chain")
require(proof, "theorem flt : FermatLastTheorem :=\n  B1_proof", "exact external root")
assert toolchain == "leanprover/lean4:v4.32.0-rc1"
mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "0098dd94d810711e831b250902687d3edab9969b"
assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: local pins and declarations match; "
    f"Imperial {imperial_revision} exact root has a direct proof gap; root=M2"
)
