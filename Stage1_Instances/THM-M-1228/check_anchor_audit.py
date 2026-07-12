#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1228-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1228"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
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

assert len(AUDIT["immutable_tree_evidence"]) == 4
assert all(not row["truncated"] for row in AUDIT["immutable_tree_evidence"])
assert all(len(row["revision"]) == 40 for row in AUDIT["immutable_tree_evidence"])
assert all(len(row["response_sha256"]) == 64 for row in AUDIT["immutable_tree_evidence"])

print("ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts")
