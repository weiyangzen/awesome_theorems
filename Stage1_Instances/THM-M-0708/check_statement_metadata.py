#!/usr/bin/env python3
"""Check the frozen THM-M-0708 statement receipt metadata."""

from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
repo = root.parents[1]
data = json.loads((root / "statement.json").read_text(encoding="utf-8"))

assert data["item_id"] == "S56-M-0708-STATEMENT"
assert data["theorem_id"] == "THM-M-0708"
assert data["canonical_formal_target"]["declaration_or_expression"] == \
    "Stage1Instances.THM_M_0708.RiceTheoremTarget"
assert data["direct_imports"] == ["Mathlib.Computability.Halting"]
assert data["statement_elaborated"] is True
assert data["theorem_proved"] is False
assert data["theorem_complete"] is False

statement_hash = hashlib.sha256((root / "Statement.lean").read_bytes()).hexdigest()
assert statement_hash == data["canonical_formal_target"]["statement_file_sha256"]
toolchain_hash = hashlib.sha256(
    (repo / "Formalizations/Lean/lean-toolchain").read_bytes()
).hexdigest()
manifest_hash = hashlib.sha256(
    (repo / "Formalizations/Lean/lake-manifest.json").read_bytes()
).hexdigest()
assert toolchain_hash == data["environment_fingerprint"]["lean_toolchain_file_sha256"]
assert manifest_hash == data["environment_fingerprint"]["lake_manifest_sha256"]
print("check_statement_metadata: ok (THM-M-0708 exact statement receipt and hashes match)")
