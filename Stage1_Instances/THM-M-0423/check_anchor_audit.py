#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
STATEMENT = json.loads((HERE / "statement.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0423-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0423"
assert AUDIT["audited_target"]["declaration"] == STATEMENT["declaration"]
assert AUDIT["audited_target"]["elaborated_expression_sha256"] == STATEMENT["elaborated_expression_sha256"]
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert all(candidate["type_checked"] for candidate in AUDIT["mathlib_candidates"])
assert {candidate["classification"] for candidate in AUDIT["external_candidates"]} == {"M5"}

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert AUDIT["immutable_environment"]["mathlib_revision"] == mathlib["rev"]
head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == mathlib["rev"]

source = (HERE / "AnchorAudit.lean").read_text()
for candidate in AUDIT["mathlib_candidates"]:
    for declaration in candidate["declarations"]:
        assert f"#check {declaration}" in source

assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == STATEMENT["source_sha256"]
print("check_anchor_audit: ok (4 mathlib families, 8 probes, 2 immutable external candidates; exact root open)")
