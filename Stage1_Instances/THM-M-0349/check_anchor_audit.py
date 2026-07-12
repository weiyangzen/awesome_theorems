#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())

assert AUDIT["item_id"] == "S56-M-0349-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0349"
assert AUDIT["immutable_environment"]["mathlib_revision"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert len(AUDIT["candidates"]) == 2
assert all(c["classification"] == "related_not_exact" for c in AUDIT["candidates"])
assert not AUDIT["decision"]["exact_external_closure_found"]
assert not AUDIT["decision"]["theorem_proved"]
assert not AUDIT["decision"]["theorem_complete"]

lean = (Path(__file__).with_name("AnchorAudit.lean")).read_text()
for declaration in ("span_fourierLp_closure_eq_top", "hasSum_fourier_series_L2"):
    assert declaration in lean
for prohibited in ("sorry", "admit", "axiom "):
    assert prohibited not in lean

instance = json.loads((Path(__file__).with_name("instance.json")).read_text())
assert instance["canonical_formal_target"]["declaration_or_expression"] == (
    "Stage1Instances.THM_M_0349.ConjugateFunctionTheoremTarget"
)
assert not instance["theorem_complete"]
assert (ROOT / "Docs/Stage1_Blueprint_rev-5.6.md").is_file()
print("anchor audit invariant check: ok")
