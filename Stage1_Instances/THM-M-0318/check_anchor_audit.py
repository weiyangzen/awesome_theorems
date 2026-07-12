#!/usr/bin/env python3
"""Verify the immutable source anchors and fail-closed root decision."""

import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


audit = json.loads(AUDIT.read_text())
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

contracting = (MATHLIB / "Mathlib/Topology/MetricSpace/Contracting.lean").read_text()
interval = (MATHLIB / "Mathlib/Topology/Order/IntermediateValue.lean").read_text()
require(contracting, "theorem exists_fixedPoint'", "complete contraction anchor")
require(interval, "theorem exists_mem_Icc_isFixedPt_of_mapsTo", "interval anchor")

lean_files = list((MATHLIB / "Mathlib").rglob("*.lean"))
schauder_hits = []
for path in lean_files:
    text = path.read_text(errors="replace")
    low = text.lower()
    if "schauder" in low:
        schauder_hits.append((path, low))
assert schauder_hits
assert all("fixed" not in low for _, low in schauder_hits)

external = next(c for c in audit["candidates"] if c["id"] == "M0318-A-HARFE-BROUWER")
base = (
    "https://raw.githubusercontent.com/harfe/fixed-point-theorems-lean4/"
    + external["revision"]
)


def remote(path: str) -> str:
    request = urllib.request.Request(f"{base}/{path}", headers={"User-Agent": "stage1-anchor-audit"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


brouwer = remote("FixedPointTheorems/brouwer.lean")
toolchain = remote("lean-toolchain").strip()
manifest = json.loads(remote("lake-manifest.json"))
require(brouwer, "theorem brouwer_fixed_point", "external Brouwer anchor")
require(brouwer, "[FiniteDimensional ℝ V]", "finite-dimensional restriction")
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in brouwer.lower()
assert toolchain == external["toolchain"]
mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == external["mathlib_revision"]

root = audit["root_decision"]
assert root["classification_after"] == "M3"
assert root["kernel_closed"] is False
assert audit["audit_phase_complete"] is True
assert audit["theorem_complete"] is False
print(
    "anchor audit verified: pinned mathlib has no Schauder fixed-point root; "
    "nearby declarations and immutable external Brouwer source match; root=M3"
)
