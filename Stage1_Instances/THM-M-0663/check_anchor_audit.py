#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0663 anchor-audit receipt."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "Stage1_Instances" / "THM-M-0663"

audit = json.loads((DIR / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0663-ANCHOR_AUDIT"
assert audit["depends_on"] == ["S56-M-0663-STATEMENT"]
assert audit["theorem_id"] == "THM-M-0663"
assert audit["canonical_declaration"] == "Stage1Instances.THM_M_0663.OMinimalMonotonicity"
assert hashlib.sha256((DIR / "Statement.lean").read_bytes()).hexdigest() == audit[
    "canonical_statement_file_sha256"
]
assert audit["repo_local"]["mathlib_revision"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert audit["repo_local"]["exact_closure_found"] is False
assert audit["repo_local"]["terminal_declaration"] is None
assert audit["machine_classification"] == "M3"
assert len(audit["external_candidates"]) == 3
assert all(len(c["revision"]) == 40 for c in audit["external_candidates"])
assert all(len(c["source_archive_sha256"]) == 64 for c in audit["external_candidates"])
assert all(c["statement_match"] is False for c in audit["external_candidates"])
assert all(c["classification"] == "M5" for c in audit["external_candidates"])
assert audit["audit_complete_for_phase"] is True
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False

lean_text = (DIR / "AnchorAudit.lean").read_text().lower()
for token in ("sorry", "admit", "axiom"):
    assert token not in lean_text, f"forbidden Lean token {token!r}"

print("anchor audit invariant check: ok")
