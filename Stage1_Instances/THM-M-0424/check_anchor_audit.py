#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
AUDIT = json.loads((OWNED / "anchor-audit.json").read_text())
STATEMENT = json.loads((OWNED / "statement.json").read_text())

assert AUDIT["item_id"] == "S56-M-0424-ANCHOR_AUDIT"
assert AUDIT["canonical_expression_sha256"] == STATEMENT["canonical_formal_target"]["elaborated_expression_sha256"]
assert hashlib.sha256((OWNED / "Statement.lean").read_bytes()).hexdigest() == AUDIT["statement_file_sha256"]
assert hashlib.sha256((ROOT / "Formalizations/Lean/lake-manifest.json").read_bytes()).hexdigest() == AUDIT["environment"]["lake_manifest_sha256"]

head = subprocess.check_output(["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True).strip()
tree = subprocess.check_output(["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True).strip()
assert head == AUDIT["environment"]["mathlib_revision"]
assert tree == AUDIT["environment"]["mathlib_tree"]
assert not subprocess.check_output(["git", "-C", str(MATHLIB), "status", "--short"], text=True).strip()

files = {}
for candidate in AUDIT["candidates"]:
    if "file" in candidate and "git_blob" in candidate:
        files[candidate["file"]] = (candidate["git_blob"], candidate["file_sha256"])
    for entry in candidate.get("files", []):
        files[entry["path"]] = (entry["git_blob"], entry["sha256"])

for relative, (blob, digest) in files.items():
    path = MATHLIB / relative
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    actual_blob = subprocess.check_output(
        ["git", "-C", str(MATHLIB), "rev-parse", f"HEAD:{relative}"], text=True
    ).strip()
    assert actual_blob == blob

brauer = (MATHLIB / "Mathlib/Algebra/BrauerGroup/Defs.lean").read_text()
for witness in ["structure CSA", "abbrev IsBrauerEquivalent", "def Brauer.CSA_Setoid", "abbrev BrauerGroup"]:
    assert witness in brauer
assert "Prove that the Brauer group is an abelian group" in brauer
assert "CommGroup (BrauerGroup" not in brauer

scoped = "\n".join((MATHLIB / relative).read_text() for relative in files)
for forbidden in ["sorry", "axiom ", "unsafe def", "unsafe theorem"]:
    assert forbidden not in scoped

assert len(AUDIT["candidates"]) == 6
assert AUDIT["audit_result"]["exact_external_closure_found"] is False
assert AUDIT["audit_result"]["theorem_complete"] is False
print("check_anchor_audit: ok (6 candidates classified; immutable mathlib sources verified; exact root remains M3)")

