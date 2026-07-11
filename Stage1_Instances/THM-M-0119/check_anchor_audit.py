#!/usr/bin/env python3
"""Check the local immutable inputs and fail-closed boundaries of this audit."""

import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
PACKAGES = LEAN_ROOT / ".lake" / "packages"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=PACKAGES / "mathlib") == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=PACKAGES / "mathlib") == ""
assert output("git", "rev-parse", "HEAD", cwd=PACKAGES / "flt-regular") == "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"

statement = (ROOT / "Stage1_Instances/THM-M-0119/Statement.lean").read_text()
legacy = (LEAN_ROOT / "AwesomeTheorems/Stage1/S1_M_038.lean").read_text()
assert "def KawamataViehwegVanishingTarget : Prop" in statement
assert "theorem kawamataViehwegVanishingTarget_iff_expanded" in statement
assert "def StatementShape : Prop" in legacy

mathlib = PACKAGES / "mathlib"
search = subprocess.run(
    [
        "rg", "-n", "-i", "--glob", "*.lean",
        r"kawamata|viehweg|log.?canonical|\\bklt\\b|kodaira.?vanish",
        str(mathlib / "Mathlib"),
    ],
    text=True,
    capture_output=True,
    check=False,
)
assert search.returncode == 1 and search.stdout == ""

verdict = audit["audit_verdict"]
assert verdict["exact_external_root_found"] is False
assert verdict["theorem_complete"] is False
assert audit["status_boundary"].endswith("theorem completion.")

print(
    "anchor audit verified: immutable pins and local boundaries agree; "
    "no exact root candidate is claimed; theorem_complete=false"
)

