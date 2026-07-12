#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Stage1_Instances/THM-M-0669/anchor-audit.json"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

data = json.loads(AUDIT.read_text())
errors = []
if data.get("item_id") != "S56-M-0669-ANCHOR_AUDIT":
    errors.append("wrong item_id")
if data.get("canonical_target") != "Stage1.THM_M_0669.TarskiQuantifierEliminationTarget":
    errors.append("wrong canonical target")
candidates = data.get("candidates", [])
if len(candidates) != 3 or len({c.get("candidate_id") for c in candidates}) != 3:
    errors.append("candidate inventory is not the frozen three-member set")
required = {"immutable_revision", "normalized_match", "terminal_body_provenance",
            "placeholder_or_trust_result", "dependency_feasibility", "classification"}
for candidate in candidates:
    missing = sorted(required - candidate.keys())
    if missing:
        errors.append(f"{candidate.get('candidate_id')}: missing {missing}")
if data.get("exact_candidate_found") is not False or data.get("root_machine_debt") != "M3":
    errors.append("fail-closed root classification changed")
if data.get("audit_complete_for_scoped_phase") is not True or data.get("audit_complete") is not False:
    errors.append("scoped/wider audit boundary changed")
if data.get("theorem_proved") or data.get("theorem_complete"):
    errors.append("audit improperly claims theorem completion")

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
actual_pin = subprocess.run(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False).stdout.strip()
if actual_pin != PIN:
    errors.append(f"mathlib pin mismatch: {actual_pin or 'unavailable'}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print("PASS: 3/3 frozen candidates classified; exact proof candidate absent; M3 retained")
