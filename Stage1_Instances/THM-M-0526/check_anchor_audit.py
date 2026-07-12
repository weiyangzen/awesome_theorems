#!/usr/bin/env python3
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"

audit = json.loads((HERE / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0526-ANCHOR_AUDIT"
assert audit["canonical_target"] == "Stage1Instances.THM_M_0526.SeifertVanKampenTarget"
assert audit["mathlib"]["exact_candidate"] is None
assert audit["classification"]["machine_state"] == "not_repo_local_closed"
assert audit["classification"]["integration_debt"] is False
assert audit["theorem_proved"] is False and audit["theorem_complete"] is False
assert len(audit["external_candidates"]) == 4

revision = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert revision == audit["mathlib"]["revision"], (revision, audit["mathlib"]["revision"])

needle = ("seifert", "van_kampen", "vankampen")
matches = []
for path in (MATHLIB / "Mathlib/AlgebraicTopology").rglob("*.lean"):
    text = path.read_text(errors="replace").lower()
    if any(term in text for term in needle):
        matches.append(str(path.relative_to(MATHLIB)))
assert not matches, matches

print(f"anchor audit ok; mathlib={revision}; exact algebraic-topology name matches=0; external inventories=4")
