#!/usr/bin/env python3
"""Verify immutable local and external candidates in the THM-M-0133 audit."""

import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ROOT / "Formalizations" / "Lean" / ".lake" / "packages"
AUDIT = Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: Path) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
for package, revision in (("mathlib", env["mathlib_revision"]),
                          ("flt-regular", env["flt_regular_revision"])):
    directory = PACKAGES / package
    assert output("git", "rev-parse", "HEAD", cwd=directory) == revision
    assert output("git", "status", "--short", cwd=directory) == ""

mathlib = PACKAGES / "mathlib" / "Mathlib" / "NumberTheory" / "FLT"
basic = (mathlib / "Basic.lean").read_text(encoding="utf-8")
three = (mathlib / "Three.lean").read_text(encoding="utf-8")
four = (mathlib / "Four.lean").read_text(encoding="utf-8")
polynomial = (mathlib / "Polynomial.lean").read_text(encoding="utf-8")
regular = (PACKAGES / "flt-regular/FltRegular/FltRegular.lean").read_text(encoding="utf-8")
require(basic, "def FermatLastTheorem : Prop", "mathlib root statement")
require(three, "theorem fermatLastTheoremThree : FermatLastTheoremFor 3", "exponent three")
require(four, "theorem fermatLastTheoremFour : FermatLastTheoremFor 4", "exponent four")
require(four, "theorem FermatLastTheorem.of_odd_primes", "conditional assembly")
require(polynomial, "theorem fermatLastTheoremWith'_polynomial", "polynomial variant")
require(regular, "theorem flt_regular", "regular-prime family")

imperial = next(c for c in audit["candidates"] if c["id"] == "M0133-A-IMPERIAL-FULL")
base = f"https://raw.githubusercontent.com/ImperialCollegeLondon/FLT/{imperial['revision']}"


def remote(path: str) -> str:
    request = urllib.request.Request(f"{base}/{path}", headers={"User-Agent": "stage1-anchor-audit"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


proof = remote("FLT/Proof.lean")
toolchain = remote("lean-toolchain").strip()
manifest = json.loads(remote("lake-manifest.json"))
require(proof, "theorem B4_proof : B4 :=\n  sorry", "direct external proof gap")
require(proof, "theorem B3_proof : B3 := B4_implies_B3 B4_proof", "B4 to B3 chain")
require(proof, "theorem B1_proof : B1 := B2_implies_B1 B2_proof", "root chain")
require(proof, "theorem flt : FermatLastTheorem :=\n  B1_proof", "external exact root")
assert toolchain == imperial["toolchain"]
pinned_mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert pinned_mathlib["rev"] == imperial["mathlib_revision"]
assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False and audit["theorem_complete"] is False

print("anchor audit verified: local immutable candidates match; "
      f"Imperial {imperial['revision']} exact root has a transitive proof gap; root=M2")
