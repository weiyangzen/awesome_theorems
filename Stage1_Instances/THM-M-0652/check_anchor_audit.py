#!/usr/bin/env python3
"""Verify immutable source facts used by the THM-M-0652 anchor audit."""

import hashlib
import json
import pathlib
import re
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
AUDIT_PATH = pathlib.Path(__file__).with_name("anchor-audit.json")
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


with AUDIT_PATH.open(encoding="utf-8") as stream:
    audit = json.load(stream)

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
semantics = (MATHLIB / "Mathlib/ModelTheory/Semantics.lean").read_bytes()
assert digest(semantics) == env["mathlib_semantics_sha256"]

mathlib_text = "\n".join(
    path.read_text(encoding="utf-8")
    for path in (MATHLIB / "Mathlib/ModelTheory").rglob("*.lean")
)
for needle in ("Craig", "isInterpolant", "craigInterpolation"):
    assert needle not in mathlib_text

legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean").read_text()
assert "structure SemanticToDerivabilityBridge" in legacy
assert "structure InterpolantExtractionRules" in legacy
assert "structure ExtractedInterpolantTerminalObligations" in legacy
assert "left/right Craig correctness remains formalization_debt" in legacy

external = next(c for c in audit["candidates"] if c["candidate_id"] == "EXTERNAL-GL-COALGEBRAS")
base = f"https://raw.githubusercontent.com/{external['project']}/{external['revision']}"


def remote(path: str) -> bytes:
    with urllib.request.urlopen(f"{base}/{path}", timeout=30) as response:
        return response.read()


interpolation = remote("GL/Interpolation/Interpolation.lean")
manifest = remote("lake-manifest.json")
license_text = remote("LICENSE")
toolchain = remote("lean-toolchain").decode().strip()
assert digest(interpolation) == external["source_sha256"]
assert digest(manifest) == external["manifest_sha256"]
assert digest(license_text) == external["license_sha256"]
assert toolchain == external["toolchain"]
assert b"theorem interpolation (" in interpolation
assert b"def isInterpolant (" in interpolation
code_without_comments = re.sub(rb"/\-.*?\-/", b"", interpolation, flags=re.DOTALL)
code_without_comments = re.sub(rb"--[^\n]*", b"", code_without_comments)
assert re.search(rb"\bsorry\b", code_without_comments) is None
manifest_json = json.loads(manifest)
mathlib = next(p for p in manifest_json["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == external["mathlib_revision"]

assert audit["root_decision"]["classification"] == "M3"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False
print("anchor audit verified: pinned mathlib has no Craig root; legacy is conditional; external GL candidate is a domain mismatch; root=M3")
