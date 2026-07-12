#!/usr/bin/env python3
"""Fail-closed validation for S56-M-0536-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0536"
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
    "Target.lean": "9aa4bda4f3240abe9fcb450b4012842a8a4635f1196fc2774fd97c1c97cc7294",
    "Proof.lean": "7a512d0b2d6a6d518b32d6697cda476f85159a5d575a1ed66f7cd8718b5a6b83",
    "ObligationTree.lean": "f6c6e52a829a143d0b099bb4cdea9b4d3c2923324385508f5d4e39446fc8fe43",
    "obligation-registry.json": "39a3c0582c7333e28077d947db03eefdb3958190fb24b127ab8c2c5499021db6",
    "typed-graphs.json": "07f1e96e60ab4d5c05a791d95e23e6204602133f5562b147f854fe08f08310ec",
    "proof-receipt.json": "d7a0dc65bd9b8f7bf6123b71f7d6d3de02c1b810cb62846189f8c1e20b9f86b8",
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
upstream = mathlib / "Mathlib/AlgebraicTopology/SingularHomology/HomotopyInvarianceTopCat.lean"
assert sha256(upstream) == "c6deda1716e42b6aab78cc2ac62bbd2e56a6502013ce8af8ca710481b1ad3dff"
assert "lemma congr_homologyMap_singularChainComplexFunctor" in upstream.read_text()

proof = (HERE / "Proof.lean").read_text()
target = (HERE / "Target.lean").read_text()
prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
assert prohibited.search(proof) is None, "proof contains a prohibited trust token"
target_body = target.split("def HomotopyInvarianceStatement : Prop :=", 1)[1].split(
    "#check HomotopyInvarianceStatement", 1
)[0].strip()
proof_body = proof.split("def HomotopyInvarianceStatement : Prop :=", 1)[1].split(
    "/-- The forward-then-inverse", 1
)[0].strip()
assert target_body == proof_body, "proof target differs from the frozen target"

# Copy only the claimed source into a fresh directory. This avoids accepting a stale local olean.
with tempfile.TemporaryDirectory(prefix="m0536-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    copied = tmp / "Proof.lean"
    copied.write_bytes((HERE / "Proof.lean").read_bytes())
    output = run(["lake", "env", "lean", str(copied)], cwd=LEAN_ROOT, env=os.environ.copy())

for declaration in ("induced_left_identity", "induced_right_identity", "homotopyInvariance"):
    line = (
        f"'Stage1.THM_M_0536.{declaration}' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]"
    )
    assert line in output, f"unexpected trust report for {declaration}\n{output}"
assert "sorryAx" not in output

receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert receipt["exact_declaration"] == "Stage1.THM_M_0536.homotopyInvariance"
assert receipt["proof_body"]["source_sha256"] == expected_hashes["Proof.lean"]
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0536 validation: fresh-source kernel replay closed the exact frozen root")
print("PASS trust: all declarations use only propext, Classical.choice, and Quot.sound")
print("PASS provenance: source hashes, proof receipt, toolchain pins, and clean mathlib revision agree")
print("OPEN release: shared warm dependency cache is not a cold hermetic replay or independent runner")
