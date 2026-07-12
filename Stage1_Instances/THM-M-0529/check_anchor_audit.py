#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0529-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0529"
assert AUDIT["root_machine_classification"] == "M0-W_candidate_pending_proof_phase"
assert AUDIT["theorem_proved"] is False and AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["candidates"][1]["revision"]
head = subprocess.run(
    ["git", "-C", str((ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()),
     "rev-parse", "HEAD"], check=True, capture_output=True, text=True
).stdout.strip()
assert head == mathlib["rev"]

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
for name in ["TopCat.isoOfHomeo", "Iso.isIso_hom", "Functor.map_isIso",
             "singularHomologyFunctor"]:
    assert f"#check {name}" in probe
assert "theorem anchorCandidate" in probe and "infer_instance" in probe
assert "sorry" not in probe and "axiom " not in probe

for component in AUDIT["candidates"][1]["components"]:
    path = ROOT / "Formalizations/Lean/.lake/packages/mathlib" / (component["module"].replace(".", "/") + ".lean")
    digest = subprocess.run(["sha256sum", str(path)], check=True, capture_output=True,
                            text=True).stdout.split()[0]
    assert digest == component["source_sha256"]

print("ok: exact anchor probe, audit boundary, mathlib pin, and three source hashes agree")
