#!/usr/bin/env python3
"""Validate the THM-M-1526 bounded immutable anchor audit."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((HERE / "anchor-audit.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-1526-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1526"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert audit["root_machine_classification"] == "M3"
assert audit["debt_classification"] == "formalization_debt"
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False

mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
mathlib_candidate = next(c for c in audit["candidates"] if c["project"] == "mathlib4")
assert mathlib_candidate["revision"] == mathlib["rev"]

mathlib_root = LEAN / ".lake" / "packages" / "mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]
assert not subprocess.run(
    ["git", "-C", str(mathlib_root), "status", "--porcelain"],
    check=True, capture_output=True, text=True,
).stdout.strip()

probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

basic = (mathlib_root / "Mathlib/LinearAlgebra/CliffordAlgebra/Basic.lean").read_text()
to_lin = (mathlib_root / "Mathlib/LinearAlgebra/Matrix/ToLin.lean").read_text()
for needle in ("theorem ι_sq_scalar", "theorem lift_ι_apply", "theorem ι_mul_ι_add_swap"):
    assert needle in basic
for needle in ("theorem Matrix.toLin_one", "theorem Matrix.toLin_mul", "theorem Matrix.toLin_mul_apply"):
    assert needle in to_lin

external = next(c for c in audit["candidates"] if c["project"] == "HEPLean/PhysLean")
assert external["revision"] == "cd22b0c28882412447d12d5cfde677c4ad999994"
assert external["toolchain"] == "leanprover/lean4:v4.29.1"
assert external["classification"] == "M3_external_support_only"
assert "no terminal proof body" in external["integration_status"]

print("ok: exact target binding, clean mathlib pin, 12 Lean probes, and immutable external support classification")
