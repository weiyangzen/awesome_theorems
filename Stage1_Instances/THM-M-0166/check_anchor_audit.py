#!/usr/bin/env python3
"""Verify the immutable local anchors and fail-closed audit decision."""

import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"
AUDIT = Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(path: Path, needles: list[str]) -> None:
    source = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in source:
            raise SystemExit(f"missing audited declaration in {path}: {needle}")


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
revision = audit["immutable_environment"]["mathlib_revision"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == revision
assert output("git", "status", "--short", cwd=MATHLIB) == ""

require(
    MATHLIB / "Mathlib/Geometry/Manifold/Riemannian/PathELength.lean",
    [
        "lemma riemannianEDist_le_pathELength",
        "lemma exists_lt_of_riemannianEDist_lt",
        "lemma exists_lt_locally_constant_of_riemannianEDist_lt",
    ],
)
require(
    MATHLIB / "Mathlib/Geometry/Manifold/Riemannian/Basic.lean",
    [
        "def PseudoEMetricSpace.ofRiemannianMetric",
        "def EMetricSpace.ofRiemannianMetric",
        "class IsRiemannianManifold",
    ],
)
require(
    MATHLIB / "Mathlib/Topology/MetricSpace/ProperSpace.lean",
    ["isCompact_closedBall :", "complete_of_proper"],
)

manifold_sources = "\n".join(
    path.read_text(encoding="utf-8", errors="replace")
    for path in (MATHLIB / "Mathlib/Geometry/Manifold").rglob("*.lean")
)
for absent in ("HopfRinow", "Hopf-Rinow", "minimizing geodesic"):
    if absent.lower() in manifold_sources.lower():
        raise SystemExit(f"negative pinned-source search changed: {absent}")

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["external_search"]["candidate_revisions"] == []
assert audit["theorem_complete"] is False
print(f"anchor audit verified at mathlib {revision}: adjacent APIs present; root=M2")
