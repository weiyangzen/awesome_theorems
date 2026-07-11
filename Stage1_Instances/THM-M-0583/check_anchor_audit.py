#!/usr/bin/env python3
"""Verify the immutable source candidates recorded by the anchor audit."""

import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"
AUDIT_PATH = Path(__file__).with_name("anchor-audit.json")


def command(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


def remote(repo: str, revision: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{repo}/{revision}/{path}"
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode()


audit = json.loads(AUDIT_PATH.read_text())
env = audit["immutable_environment"]
assert command("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert command("git", "status", "--short", cwd=MATHLIB) == ""

mathlib_source = (MATHLIB / "Mathlib/Geometry/Manifold/PoincareConjecture.lean").read_text()
require(
    mathlib_source,
    "proof_wanted ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere",
    "mathlib generalized source marker",
)

legacy = (LEAN / "AwesomeTheorems/Stage1/S1_M_116.lean").read_text()
require(legacy, "def terminalLeanProofBodyValidatedLocally : Bool :=", "legacy proof gate")
require(legacy, "def externalTerminalProofCandidateFound : Bool :=", "legacy external gate")

millennium_rev = "540da94826f70f3edf4d4fc66ce6cda20e903f61"
millennium = remote(
    "lean-dojo/LeanMillenniumPrizeProblems",
    millennium_rev,
    "Problems/Poincare/Millennium.lean",
)
require(millennium, "def GeneralizedPoincareConjecture : Prop :=", "external generalized target")
require(millennium, "theorem generalizedPoincareConjecture_zero", "dimension-zero proof")
if "generalizedPoincareConjecture_four" in millennium:
    raise SystemExit("unexpected four-dimensional terminal theorem in pinned Millennium source")

formal_rev = "686d32e672974920ca8525aef4a87281bd0cf146"
formal = remote(
    "google-deepmind/formal-conjectures",
    formal_rev,
    "FormalConjectures/Millenium/Poincare.lean",
)
require(
    formal,
    "theorem poincare_conjecture.variants.dimension_four : ConjectureFor 4 := by\n  sorry",
    "external dimension-four placeholder",
)

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is True
assert audit["theorem_complete"] is False
print(
    "anchor audit verified: pinned mathlib is source-only; immutable external "
    "candidates are dimension-0-only or sorry; root=M2"
)
