#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0987-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0987"
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["eligible_anchor"] == "S56-M-0987-C02"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

candidates = {candidate["candidate_id"]: candidate for candidate in AUDIT["candidates"]}
mathlib_candidate = candidates["S56-M-0987-C02"]
external_candidate = candidates["S56-M-0987-C04"]
mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib_candidate["revision"] == mathlib["rev"]
assert mathlib_candidate["classification"] == "M0-W_candidate"
assert external_candidate["revision"] == "0ed57e943d642eaa95fe547780024b9e3a0dfbdf"
assert external_candidate["classification"] == "M5_external_placeholder_mismatch"

probe = (HERE / "AnchorAudit.lean").read_text()
assert "theorem pinnedMathlibCandidate" in probe
assert "exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub" in probe
for declaration in mathlib_candidate["transitive_route_probes"]:
    assert f"#check {declaration}" in probe
assert "#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub" in probe
assert "#print axioms Stage1Instances.THM_M_0987.AnchorAudit.pinnedMathlibCandidate" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

source = mathlib_root / mathlib_candidate["source_path"]
blob = subprocess.run(
    ["git", "-C", str(mathlib_root), "hash-object", str(source)],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert blob == mathlib_candidate["source_blob"]
source_text = source.read_text()
assert "theorem tendstoInDistribution_inv_sqrt_mul_sum_sub" in source_text
for forbidden in ("sorry", "axiom", "admit", "unsafe"):
    assert forbidden not in source_text

print("ok: 4 candidates classified, exact mathlib probe present, pin/blob agree, and status boundary is conservative")
