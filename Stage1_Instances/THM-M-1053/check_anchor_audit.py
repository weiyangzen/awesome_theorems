#!/usr/bin/env python3
"""Validate the locally reproducible boundaries of the THM-M-1053 anchor audit."""

from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT_PATH = Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

candidate = next(c for c in audit["candidates"] if c["id"] == "M1053-A-PINNED-MATHLIB-ADJACENT")
for relative, expected in candidate["source_sha256"].items():
    assert sha256(MATHLIB / relative) == expected

average_source = (MATHLIB / "Mathlib/Dynamics/BirkhoffSum/Average.lean").read_text(encoding="utf-8")
function_source = (MATHLIB / "Mathlib/Dynamics/Ergodic/Function.lean").read_text(encoding="utf-8")
assert "def birkhoffAverage" in average_source
assert "theorem birkhoffAverage_apply_sub_birkhoffAverage" in average_source
assert "theorem ae_eq_const_of_ae_eq_comp_ae" in function_source

all_mathlib_ergodic = "\n".join(
    path.read_text(encoding="utf-8")
    for path in (MATHLIB / "Mathlib/Dynamics/Ergodic").rglob("*.lean")
)
assert "pointwise ergodic theorem" not in all_mathlib_ergodic.lower()
assert "tendsto_birkhoffAverage_ae" not in all_mathlib_ergodic

assert audit["root_decision"]["classification"] == "M1"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

print("anchor ledger verified: pinned mathlib adjacent sources match; external exact candidate remains unintegrated; root=M1")
