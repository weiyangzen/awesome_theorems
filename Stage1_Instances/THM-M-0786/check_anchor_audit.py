#!/usr/bin/env python3
"""Verify immutable anchors and fail-closed classifications for THM-M-0786."""

import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = HERE / "anchor-audit.json"
SNAPSHOT = HERE / "external-anchor-snapshot.json"


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
assert audit["item_id"] == "S56-M-0786-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0786"
assert audit["root_decision"]["classification"] == "M3"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
assert "def BorelDeterminacyTarget : Prop" in statement
assert "theorem target_iff_expanded" in statement
local_lean = "\n".join(
    path.read_text(encoding="utf-8")
    for path in ROOT.rglob("*.lean")
    if MATHLIB not in path.parents and HERE not in path.parents
)
assert not re.search(r"borel[_ ]determinacy|GaleStewart", local_lean, re.IGNORECASE)

candidate = next(c for c in audit["candidates"] if c["id"] == "M0786-A-BORELDET-EXTERNAL")
revision = candidate["revision"]
assert snapshot["revision"] == revision
assert snapshot["tree_revision"] == candidate["tree_revision"]
assert snapshot["module"] == candidate["module"]
assert snapshot["declaration"] == candidate["declaration"]
assert snapshot["source_file_sha256"] == candidate["source_file_sha256"]
assert snapshot["lean_toolchain"] == candidate["toolchain"]
assert snapshot["mathlib_revision"] == candidate["mathlib_revision"]
assert snapshot["manifest_sha256"] == candidate["manifest_sha256"]
assert snapshot["license"] == candidate["license"]
assert snapshot["declaration_header"].startswith("theorem borel_determinacy")
assert "MeasurableSet[borel _] G.payoff" in snapshot["declaration_header"]
assert "Tree.IsPruned G.tree" in snapshot["declaration_header"]
assert snapshot["defensive_source_scan"]["matches"] == []
assert snapshot["github_actions_runs_for_revision"] == 0

assert candidate["classification"] == "M5"
assert candidate["toolchain"] != env["lean_toolchain"]
assert candidate["mathlib_revision"] != env["mathlib_revision"]
print(
    "anchor audit verified: local mathlib pin and negative local inventory match; "
    f"BorelDet {revision} source anchor and pins match; root=M3, external=M5"
)
