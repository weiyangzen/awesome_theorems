#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).with_name("anchor-audit.json")

data = json.loads(AUDIT.read_text())
assert data["item_id"] == "S56-M-0657-ANCHOR_AUDIT"
assert data["theorem_id"] == "THM-M-0657"
assert data["canonical_target"] == "Stage1Instances.THM_M_0657.MorleyCategoricityTarget"
assert len(data["mathlib_candidates"]) == 4
assert len(data["external_candidates"]) == 5
assert all(not candidate["exact_root_closure"] for candidate in
           data["mathlib_candidates"] + data["external_candidates"])
assert data["classification"]["machine"] == "M3"
assert data["classification"]["debt"] == "formalization_debt"
assert data["theorem_proved"] is False and data["theorem_complete"] is False

manifest = ROOT / "Formalizations/Lean/lake-manifest.json"
digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
assert digest == data["environment"]["lake_manifest_sha256"]
lake = json.loads(manifest.read_text())
mathlib = next(package for package in lake["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == data["environment"]["mathlib_revision"]

print("ok: 4 pinned mathlib anchors, 5 immutable external repositories, no exact closure")
