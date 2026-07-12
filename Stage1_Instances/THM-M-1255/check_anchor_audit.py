#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "Stage1_Instances" / "THM-M-1255"
audit = json.loads((TARGET / "anchor-audit.json").read_text())

assert audit["item_id"] == "S56-M-1255-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1255"
assert audit["mathlib"]["revision"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert audit["mathlib"]["terminal_candidate_found"] is False
assert len(audit["mathlib"]["positive_anchors"]) >= 6
assert all(not row["terminal"] for row in audit["mathlib"]["positive_anchors"])
assert audit["classification"]["anchor_audit_complete"] is True
assert audit["classification"]["theorem_complete"] is False

manifest = json.loads((ROOT / "Formalizations" / "Lean" / "lake-manifest.json").read_text())
mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == audit["mathlib"]["revision"]
actual = subprocess.check_output(
    ["git", "-C", str(ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"), "rev-parse", "HEAD"],
    text=True,
).strip()
assert actual == audit["mathlib"]["revision"]

for name in ("AnchorAudit.lean", "anchor-audit.json", "anchor-audit.md"):
    assert (TARGET / name).is_file()

print(f"THM-M-1255 anchor audit: ok; mathlib={actual}; positive_anchors={len(audit['mathlib']['positive_anchors'])}; terminal=none")
