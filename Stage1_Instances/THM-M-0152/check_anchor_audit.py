#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
AUDIT = json.loads((OWNED / "anchor-audit.json").read_text())
STATEMENT = json.loads((OWNED / "statement.json").read_text())
MANIFEST_PATH = ROOT / "Formalizations/Lean/lake-manifest.json"
MANIFEST = json.loads(MANIFEST_PATH.read_text())

assert AUDIT["item_id"] == "S56-M-0152-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0152"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert AUDIT["audited_target"]["elaborated_expression_sha256"] == \
    STATEMENT["canonical_formal_target"]["elaborated_expression_sha256"]

statement_hash = hashlib.sha256((OWNED / "Statement.lean").read_bytes()).hexdigest()
assert statement_hash == AUDIT["audited_target"]["statement_file_sha256"]
manifest_hash = hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()
assert manifest_hash == AUDIT["immutable_environment"]["lake_manifest_sha256"]

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["immutable_environment"]["mathlib_revision"]
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

probe_source = (OWNED / "AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe_source

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]

assert AUDIT["candidates"][2]["classification"] == "M3_anchor_only"
assert AUDIT["candidates"][2]["revision"] == \
    "0f6734e222fd5e0b86c1ff02c2f5abde4c65e163"

print("ok: exact target identity, pins, 8 Lean probes, 3 candidates, and M4 boundary")

