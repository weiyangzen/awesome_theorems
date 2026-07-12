#!/usr/bin/env python3
"""Verify the immutable local anchors and conservative root classification."""

import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

ident = (MATHLIB / "Mathlib/Probability/IdentDistribIndep.lean").read_text(encoding="utf-8")
independence = (MATHLIB / "Mathlib/Probability/Independence/Basic.lean").read_text(encoding="utf-8")
zero_one = (MATHLIB / "Mathlib/Probability/Independence/ZeroOne.lean").read_text(encoding="utf-8")
historical = (LEAN_ROOT / "AwesomeTheorems/Stage1/S1_M_288.lean").read_text(encoding="utf-8")

require(ident, "lemma IdentDistrib.pi", "path-law anchor")
require(independence, "lemma iIndepFun.precomp", "independence reindexing anchor")
require(zero_one, "theorem measure_eq_zero_or_one_of_indepSet_self", "self-independence endpoint")
require(zero_one, "theorem measure_zero_or_one_of_measurableSet_limsup_atTop", "Kolmogorov endpoint")
require(historical, "def StatementShape : Prop", "historical statement shape")
require(historical, "def externalAuditTerminalHewittSavageTheoremFound : Bool := false", "historical negative audit")

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False
assert all(row["terminal_hits"] == 0 for row in audit["external_search"]["repositories"])

print(
    "anchor audit verified: clean pinned mathlib at "
    f"{env['mathlib_revision']}; route declarations present; external hits=0; root=M2"
)
