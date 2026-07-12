#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
audit = json.loads((ROOT / "anchor-audit.json").read_text())
statement = json.loads((ROOT / "statement.json").read_text())

assert audit["item_id"] == "S56-M-1041-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1041"
assert audit["canonical_target"]["expression_sha256"] == statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert len(audit["candidates"]) == 3
assert all(len(c["revision"]) == 40 for c in audit["candidates"])
assert audit["environment"]["mathlib_revision"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert audit["root_decision"]["machine_status"] == "M4"
assert audit["root_decision"]["proof_credit"] is False
assert audit["root_decision"]["audit_complete_for_phase"] is True
assert audit["root_decision"]["theorem_complete"] is False
assert "not M1" in audit["candidates"][2]["classification"]

manifest_hash = hashlib.sha256((ROOT.parents[1] / "Formalizations/Lean/lake-manifest.json").read_bytes()).hexdigest()
assert manifest_hash == audit["environment"]["lake_manifest_sha256"]
print("anchor audit invariant check: ok")

