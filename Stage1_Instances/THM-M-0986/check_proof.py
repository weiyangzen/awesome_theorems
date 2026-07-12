#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0986 proof phase."""

from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text(encoding="utf-8")

required = (
    "theorem averageMeasurabilityPackage",
    "theorem strongLawPackage",
    "theorem khinchinWeakLaw : KhinchinWeakLawTarget",
    "ProbabilityTheory.strong_law_ae",
    "root_of_strongLaw_packages strongLawPackage averageMeasurabilityPackage",
)
missing = [needle for needle in required if needle not in proof]
if missing:
    raise SystemExit(f"missing required proof surface: {missing}")

forbidden = re.compile(r"\b(sorry|admit)\b|^[ \t]*(axiom|unsafe)\b", re.MULTILINE)
match = forbidden.search(proof)
if match:
    raise SystemExit(f"forbidden proof token: {match.group(0)!r}")

print("PASS THM-M-0986 proof: exact root and both frozen packages have bodies")
