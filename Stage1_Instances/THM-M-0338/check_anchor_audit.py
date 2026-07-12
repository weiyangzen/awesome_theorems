#!/usr/bin/env python3
"""Check the immutable pins and negative boundary of the anchor audit."""

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0338-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0338"
assert AUDIT["canonical_target"] == "Stage1.THM_M_0338.KadisonSingerStatement"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["debt_classification"] == "formalization_debt"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib_pin = next(p["rev"] for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert mathlib_pin == AUDIT["immutable_environment"]["mathlib_revision"]
mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib_pin

probe = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0338-C02")
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
assert "def KadisonSingerStatement : Prop" in statement
assert "theorem KadisonSingerStatement" not in statement

candidate_pattern = re.compile(
    r"kadison.?singer|anderson.?paving|weaver.?conjecture|weaverconjecture",
    re.IGNORECASE,
)
matches = []
for path in (mathlib_root / "Mathlib").rglob("*.lean"):
    source = path.read_text(encoding="utf-8", errors="ignore")
    if candidate_pattern.search(source):
        matches.append(str(path.relative_to(mathlib_root)))
assert matches == [], f"re-audit newly discovered pinned candidates: {matches}"

print(
    "ok: exact statement-only boundary, 8 pinned API probes, mathlib revision, "
    "and bounded no-candidate source scan agree; root=M4"
)
