#!/usr/bin/env python3
"""Fail-closed checks for the THM-M-1272 immutable anchor audit."""

from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"anchor audit check failed: {message}")


require(AUDIT["item_id"] == "S56-M-1272-ANCHOR_AUDIT", "wrong item")
require(AUDIT["theorem_id"] == "THM-M-1272", "wrong theorem")
require(AUDIT["audit_complete"] is True, "bounded audit is not complete")
require(AUDIT["theorem_complete"] is False, "audit claims theorem completion")
require(AUDIT["accepted_receipts"] == [], "worker invented accepted receipts")
require(AUDIT["root_decision"]["kernel_closed"] is False, "root incorrectly closed")
require(AUDIT["discovery_protocol"]["exhaustive_public_search_claimed"] is False,
        "bounded search was described as exhaustive")
require(AUDIT["discovery_protocol"]["moving_dependency_fetched"] is False,
        "audit claims a moving fetch")
require(all(not row["exact_root_closed"] for row in AUDIT["candidates"]),
        "a candidate contradicts the open-root decision")

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
require(statement_hash == AUDIT["canonical_source_sha256"], "canonical statement drift")

manifest = json.loads((LEAN / "lake-manifest.json").read_text())
manifest_pins = {p["name"].strip("«»"): p["rev"] for p in manifest["packages"]}
for dependency in AUDIT["immutable_dependencies"]:
    name = dependency["name"]
    require(manifest_pins.get(name) == dependency["revision"], f"manifest pin drift: {name}")
    head = subprocess.check_output(
        ["git", "-C", str(LEAN / ".lake" / "packages" / name), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    require(head == dependency["revision"], f"checked-out revision drift: {name}")

legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_165.lean"
legacy_row = next(row for row in AUDIT["candidates"] if row["id"] == "repo-legacy-s1-m-165")
require(hashlib.sha256(legacy.read_bytes()).hexdigest() == legacy_row["source_sha256"],
        "legacy source drift")
legacy_text = legacy.read_text()
for witness in ("structure FountainHypotheses", "palaisSmaleCompactness : Prop",
                "minimaxConstruction : Prop", "def StatementShape"):
    require(witness in legacy_text, f"missing legacy boundary witness: {witness}")

mathlib = LEAN / ".lake/packages/mathlib/Mathlib"
for relative, witness in {
    "Analysis/Calculus/ContDiff/Defs.lean": "theorem ContDiff.differentiable_one",
    "Analysis/Calculus/LocalExtr/Basic.lean": "theorem IsLocalMin.fderiv_eq_zero",
    "Analysis/InnerProductSpace/l2Space.lean": "theorem Submodule.isHilbertSumOrthogonal",
}.items():
    require(witness in (mathlib / relative).read_text(), f"missing mathlib witness: {witness}")

print("anchor audit check: ok; 11 immutable dependency heads, 4 non-closing candidate rows")
