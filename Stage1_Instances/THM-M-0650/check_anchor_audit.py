#!/usr/bin/env python3
"""Verify THM-M-0650's immutable anchor ledger and pinned sources."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(path: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


assert AUDIT["item_id"] == "S56-M-0650-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0650"
assert AUDIT["canonical_target_expression_sha256"] == (
    "33ef21b57b9433d0caa5188ed270e4d9ef70aaef44d308f2a8b839be3938a5e2"
)
assert AUDIT["root_machine_classification"] == "M0-P_candidate"
assert AUDIT["theorem_proved"] is False and AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
env = AUDIT["immutable_environment"]
assert mathlib["rev"] == mathlib["inputRev"] == env["mathlib_revision"]
assert git_head(MATHLIB) == env["mathlib_revision"]

substructures = MATHLIB / "Mathlib/ModelTheory/ElementarySubstructures.lean"
maps = MATHLIB / "Mathlib/ModelTheory/ElementaryMaps.lean"
license_file = MATHLIB / "LICENSE"
assert sha256(substructures) == env["elementary_substructures_sha256"]
assert sha256(maps) == env["elementary_maps_sha256"]
assert sha256(license_file) == env["license_file_sha256"]

substructure_source = substructures.read_text()
maps_source = maps.read_text()
assert "theorem isElementary_of_exists (S : L.Substructure M)" in substructure_source
assert "S.IsElementary := fun _ => S.subtype.isElementary_of_exists htv" in substructure_source
assert "theorem isElementary_of_exists (f : M ↪[L] N)" in maps_source
assert "refine fun n φ => φ.recOn ?_ ?_ ?_ ?_ ?_" in maps_source

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
for declaration in (
    "FirstOrder.Language.Substructure.isElementary_of_exists",
    "FirstOrder.Language.Embedding.isElementary_of_exists",
    "FirstOrder.Language.Substructure.toElementarySubstructure",
):
    assert f"#check {declaration}" in probe

exact = AUDIT["candidates"][0]
assert exact["revision"] == env["mathlib_revision"]
assert exact["declaration"] == "FirstOrder.Language.Substructure.isElementary_of_exists"
assert exact["terminal_body"] == "FirstOrder.Language.Embedding.isElementary_of_exists"

print("ok: exact anchor, terminal body, source hashes, license, and pinned mathlib revision verified")
