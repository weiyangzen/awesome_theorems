#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0541-VALIDATION."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0541"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


expected_hashes = {
    "Statement.lean": "5e799f4793bdba080beac5baba329a5d90a4c89e8beeadca6f6c0d1765bcc32d",
    "Proof.lean": "4fcaaaeff8998e50a7bdea2e670e02d9ea96861f48fdef9964e7e24840ee16ae",
    "obligation-registry.json": "fa62c038bcf08222c22cb315901d214106c5ed23dbde31868687b1ee29f2ae04",
    "typed-graphs.json": "2aa9d617b073acfc8b1ff5e72fc42993b95d5a209ee5b85eedf0e824fa3c8d9e",
    "anchor-audit.json": "aa40b58b2697782deb5c073a4d835b7fdb05267ea5f662e14cb8458c870a3bdb",
}
for name, expected in expected_hashes.items():
    actual = sha256(HERE / name)
    assert actual == expected, f"stale {name}: expected {expected}, got {actual}"

assert sha256(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert sha256(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir(), "pinned mathlib artifact is missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""

proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
assert prohibited.search(proof) is None, "proof contains a prohibited trust token"
for marker in (
    "def Simplex", "def face", "abbrev Chains", "def HasAlternatingBoundary",
    "def CanonicalTarget", "def StatementShape",
):
    assert marker in statement and marker in proof, f"frozen target marker missing: {marker}"
assert "theorem statementShape : StatementShape" in proof

# Copy only the attested proof source. This prevents a dossier-local olean or generated file
# from supplying the claimed declaration while retaining the canonical pinned dependency cache.
with tempfile.TemporaryDirectory(prefix="m0541-validation-", dir=LEAN_ROOT) as tmp_name:
    copied = Path(tmp_name) / "Proof.lean"
    copied.write_bytes((HERE / "Proof.lean").read_bytes())
    env = os.environ.copy()
    env.update({"TZ": "UTC", "LC_ALL": "C.UTF-8"})
    output = run(["lake", "env", "lean", str(copied)], cwd=LEAN_ROOT, env=env)

assert (
    "Stage1Instances.THM_M_0541.statementShape : "
    "Stage1Instances.THM_M_0541.StatementShape"
) in output
assert (
    "'Stage1Instances.THM_M_0541.statementShape' depends on axioms: "
    "[propext, Classical.choice, Quot.sound]"
) in output, f"unexpected trust report\n{output}"
assert "sorryAx" not in output

print("PASS THM-M-0541 validation: fresh-source kernel replay closed the exact declared root")
print("PASS trust: root uses only propext, Classical.choice, and Quot.sound")
print("PASS provenance: source hashes, obligation inputs, toolchain pins, and clean mathlib revision agree")
print("OPEN release: warm shared dependency cache is not a cold hermetic replay or independent runner")
