#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
STATEMENT = json.loads((HERE / "statement.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0420-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0420"
assert AUDIT["target_expression_sha256"] == STATEMENT["canonical_formal_target"]["elaborated_expression_sha256"]
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False and AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
mathlib_row = next(row for row in AUDIT["candidates"] if row["project"] == "mathlib4")
assert mathlib_row["revision"] == mathlib["rev"]

probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in mathlib_row["declarations"]:
    assert f"#check {declaration}" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == mathlib["rev"]

search = subprocess.run(
    ["rg", "-n", "-i", "Hilbert class field|HilbertClassField|class field theory|Artin reciprocity|maximal unramified abelian", str(mathlib_root / "Mathlib"), "--glob", "*.lean"],
    capture_output=True, text=True
)
assert search.returncode == 1, search.stdout

for row in AUDIT["candidates"][2:]:
    assert len(row["revision"]) == 40
    assert row["tree_complete"] is True
    assert row["project_mathlib_revision"] != mathlib["rev"]

print("ok: target hash, mathlib pin, 10 Lean probes, bounded negative search, and 4 candidate classifications agree")
