#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1045-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1045"
assert AUDIT["canonical_target_expression_sha256"] == json.loads(
    (Path(__file__).with_name("statement.json")).read_text()
)["canonical_formal_target"]["elaborated_expression_sha256"]
assert AUDIT["root_decision"]["classification"] == "M3"
assert AUDIT["root_decision"]["kernel_closed"] is False
assert AUDIT["audit_complete"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert AUDIT["immutable_environment"]["mathlib_revision"] == mathlib["rev"]
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

probe = (Path(__file__).with_name("AnchorAudit.lean")).read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: THM-M-1045 anchor inventory, 10 Lean probes, target fingerprint, and mathlib pin agree")
