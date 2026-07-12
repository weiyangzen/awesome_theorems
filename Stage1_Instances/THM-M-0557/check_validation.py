#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0557-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0557"
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
    "Statement.lean": "1ec079a5f017753fdb28a74e97f0f053c906ec22116f290e150b7604240f04fa",
    "ObligationTree.lean": "f0ba6ee5e79840c32ef5c4ec56ff4eb05ad541bdca1f0dade7410c61eba1756f",
    "Proof.lean": "1e4c2b44d3d6f3a3b7ef29da6279bfd8a6666cc91488285e265a34c87806e0c8",
    "statement.json": "bad01478d729f10abc88b2599467ae57177af85df70e030f8156fbe3da8d5f75",
    "anchor-audit.json": "083b24eda51e2348a6e269b0f42a929577a12941808c1a8cb3794ba017d10ce3",
    "obligation-registry.json": "2c9cc125ec4d529ad64dc166c5ec29fb3267e249c27dea07d61190c9aa033e2e",
    "typed-graphs.json": "d4d3fb29cb61ee3673c0ee0471b4288821652a4116a6c0dfd2ea1c2936384640",
    "proof-receipt.json": "16a12fc4f805f6e237ca9c9e8f3be0c0061e86a77482ed110c2871e49d3221dd",
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

upstream = mathlib / "Mathlib/Topology/Homotopy/HomotopyGroup.lean"
assert sha256(upstream) == "0233597af0b0db82315ec206cacf9b88d62ae7d2cd05a099a8e4c36b17c39104"
upstream_text = upstream.read_text()
for terminal_source in (
    "instance group (N) [DecidableEq N] [Nonempty N]",
    "theorem auxGroup_indep",
    "theorem transAt_distrib",
    "instance commGroup [Nontrivial N]",
    "@EckmannHilton.commGroup",
):
    assert terminal_source in upstream_text, f"missing terminal route: {terminal_source}"

proof = (HERE / "Proof.lean").read_text()
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(proof) is None, "proof contains a prohibited trust token"

# Recheck exact expression identity independently of the proof-phase validator.
statement = (HERE / "Statement.lean").read_text()
target = re.search(
    r"def HomotopyGroupStructureTarget : Prop :=\n(?P<body>.*?)\n\n-- Separately",
    statement,
    re.DOTALL,
)
proved = re.search(
    r"theorem homotopyGroupStructureTarget :\n(?P<body>.*?) := by", proof, re.DOTALL
)
assert target and proved
normalize = lambda value: "".join(value.split())
assert normalize(target.group("body")) == normalize(proved.group("body"))

# Copy only the claimed source into a fresh directory, preventing acceptance of a
# stale dossier-local olean while reusing only the already-pinned dependency cache.
with tempfile.TemporaryDirectory(prefix="m0557-validation-", dir=LEAN_ROOT) as tmp_name:
    copied = Path(tmp_name) / "Proof.lean"
    copied.write_bytes((HERE / "Proof.lean").read_bytes())
    output = run(
        ["lake", "env", "lean", str(copied)], cwd=LEAN_ROOT, env=os.environ.copy()
    )

for declaration in (
    "groupStructureBranch",
    "commutativeStructureBranch",
    "homotopyGroupStructureTarget",
):
    qualified = f"Stage1Instances.THM_M_0557.Proof.{declaration}"
    report = re.search(
        rf"'{re.escape(qualified)}' depends on axioms: \[(?P<axioms>.*?)\]",
        output,
        re.DOTALL,
    )
    assert report, f"missing trust report for {declaration}\n{output}"
    axioms = [value.strip() for value in report.group("axioms").split(",")]
    assert axioms == ["propext", "Classical.choice", "Quot.sound"], (
        f"unexpected trust report for {declaration}: {axioms}"
    )
assert "sorryAx" not in output

receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert receipt["exact_declaration"] == (
    "Stage1Instances.THM_M_0557.Proof.homotopyGroupStructureTarget"
)
assert receipt["proof_body"]["source_sha256"] == expected_hashes["Proof.lean"]
assert receipt["proof_body"]["mathlib_revision"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert receipt["result"]["root_proof_body_closed"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0557 validation: fresh-source kernel replay closed the exact frozen root")
print("PASS trust: all three declarations use only propext, Classical.choice, and Quot.sound")
print("PASS provenance: dossier hashes, proof receipt, dependency pins, and terminal mathlib source agree")
print("OPEN hermetic gate: replay reused the canonical pinned warm dependency cache")
print("OPEN independent gate: this worker is not a separately provisioned and attested runner")
