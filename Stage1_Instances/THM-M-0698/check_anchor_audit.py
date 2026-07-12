#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0698-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0698"
assert AUDIT["root_machine_classification"] == "M0-W_candidate_pending_ordered_proof_gate"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
candidate = next(c for c in AUDIT["candidates"] if c["project"] == "mathlib4")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert candidate["revision"] == mathlib["rev"]

source = (ROOT / "Stage1_Instances/THM-M-0698/AnchorAudit.lean").read_text()
assert "#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable" in source
assert "#print axioms FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable" in source
assert "theorem pinnedMathlibCandidateClosesAuditedTarget" in source

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: exact anchor, immutable mathlib pin, workflow boundary, and audit schema")
