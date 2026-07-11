#!/usr/bin/env python3
"""Verify the immutable local and external anchors in THM-M-0580's audit."""

import base64
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request


ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_ROOT = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())


def git(*args: str, cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


assert AUDIT["item_id"] == "S56-M-0580-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0580"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
env = AUDIT["immutable_environment"]
assert mathlib["rev"] == env["mathlib_revision"]
assert git("rev-parse", "HEAD", cwd=MATHLIB_ROOT) == env["mathlib_revision"]
assert git("status", "--short", cwd=MATHLIB_ROOT) == ""
assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB_ROOT) == env["mathlib_tree"]

module = MATHLIB_ROOT / "Mathlib/Geometry/Manifold/PoincareConjecture.lean"
source = module.read_text()
assert hashlib.sha256(module.read_bytes()).hexdigest() == env["mathlib_module_sha256"]
for marker in next(c for c in AUDIT["candidates"] if c["candidate_id"] == "S56-M-0580-C03")["source_entries"]:
    assert f"proof_wanted {marker}" in source

external = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "S56-M-0580-C04")
url = (
    "https://api.github.com/repos/lean-dojo/LeanMillenniumPrizeProblems/contents/"
    f"{external['module']}?ref={external['revision']}"
)
with urllib.request.urlopen(url, timeout=30) as response:
    payload = json.load(response)
external_source = base64.b64decode(payload["content"])
assert hashlib.sha256(external_source).hexdigest() == external["source_sha256"]
external_text = external_source.decode()
assert "def PoincareConjecture3 : Prop" in external_text
assert "def GeneralizedPoincareConjecture : Prop" in external_text
assert "theorem generalizedPoincareConjecture_zero" in external_text
assert "theorem PoincareConjecture3" not in external_text

print("ok: exact statement anchors are bodyless, external root is statement-only, root=M4")

