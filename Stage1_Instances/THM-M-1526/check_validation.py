#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1526-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1526"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT,
        env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
assert spec["item_id"] == "S56-M-1526-VALIDATION"
assert spec["theorem_id"] == "THM-M-1526"
assert spec["network_policy"] == "denied"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

expected_inputs = {
    "Statement.lean": "023a6d029577126ca940736995b65869bc9554d1b81e487c53b322765eb910a2",
    "ObligationTree.lean": "b5a3a6060aaee8b2e70000f3306586adbf4ebb5e9542838a03f95f69db19f095",
    "Proof.lean": "efc83011b65c378508516320ba9f8b95d9c25d71d7f5fb035e8c5330c0fb85d0",
    "obligation-registry.json": "7ce1d193e4343f71fa350e64d16bf1ebd0e2295e8bcfe1d99c7d06025826c42f",
    "typed-graphs.json": "b7390031772cdde7c2a6e331221b8cbf3121178b5a0ed65ca9f2bdaf5b9e47c1",
}
for name, expected in expected_inputs.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"

assert digest(LEAN_ROOT / "lean-toolchain") == \
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == \
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""

prohibited = re.compile(
    r"\b(?:s" + r"orry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search((HERE / name).read_text()) is None, name

with tempfile.TemporaryDirectory(prefix="thm-m-1526-validation-") as directory:
    cache = Path(directory)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    env = {**os.environ, "LEAN_PATH": lean_path}
    run([lean, "-o", str(cache / "Statement.olean"), "Statement.lean"], cwd=HERE, env=env)
    env["LEAN_PATH"] = f"{cache}:{lean_path}"
    run([lean, "-o", str(cache / "ObligationTree.olean"), "ObligationTree.lean"], cwd=HERE, env=env)
    proof_output = run([lean, "Proof.lean"], cwd=HERE, env=env)
    independent_output = run([lean, "Validation.lean"], cwd=HERE, env=env)

expected_axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
assert " ".join(proof_output.split()).count(expected_axioms) == 4
assert " ".join(independent_output.split()).count(expected_axioms) == 3
assert "declaration uses 'sorry'" not in proof_output + independent_output

closure = graphs["closure_boundary"]
assert closure["root_machine_debt"] == "M3"
assert closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == {
    "M1526-N-PRODUCT", "M1526-L-SLASH-SQUARE"
}

print("PASS narrow kernel replay: exact proof and separate exact-target reconstruction elaborated")
print("PASS trust observation: seven declarations report only propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen source hashes, clean pinned mathlib, toolchain, and manifest agree")
print("STALE authoritative graph: product and slash-square nodes remain open pending master reconciliation")
print("BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner")
