#!/usr/bin/env python3
"""Narrow fail-closed validation for S56-M-1082-VALIDATION."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_PROJECT = ROOT / "Formalizations" / "Lean"
EXPECTED_HASHES = {
    "Statement.lean": "a744c3af153df269d6a69f5ad8e18a7fa6e832841bac28ff43538df2e646efdd",
    "ObligationTree.lean": "9d384441427c109e1d09170517e3b5eb7f3b4e7506c67be8c1cf25f402d13d5a",
    "Proof.lean": "54dc117b3e8857dcdb48bdf1f45df0b16a7c2ccc839714733cfea11b66816e9f",
    "statement.json": "b948be7a584a51462828ef86cbb4aa0d4fb34826fac0976ba8b2b94b79abcfe1",
    "anchor-audit.json": "8d13938920a5f59e945b8e271eb2b5c1d9cd754ded93aff077981902eb29a917",
    "obligation-registry.json": "3a0ebf56523f05f6db22b1d2092fefb5bfd228630c43acbf4380cf87c2057809",
    "typed-graphs.json": "6a3339f9bcbfdd4fa642c180d16cc57169306f29b8afc7a274a44139b543f731",
}
EXPECTED_AXIOMS = "[propext, Classical.choice, Quot.sound]"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=120, check=False
    )
    if result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}{result.stderr}"
        )
    return result.stdout + result.stderr


for name, expected in EXPECTED_HASHES.items():
    assert sha256(HERE / name) == expected, f"frozen input drift: {name}"

for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    for pattern in (r"\bsorry\b", r"\badmit\b", r"\bsorryAx\b", r"\bunsafe\b", r"^\s*axiom\b"):
        assert re.search(pattern, source, re.MULTILINE) is None, f"forbidden token in {name}: {pattern}"

mathlib = LEAN_PROJECT / ".lake" / "packages" / "mathlib"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--porcelain"], cwd=mathlib) == ""

base_lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_PROJECT).strip()
with tempfile.TemporaryDirectory(prefix="thm-m-1082-validation-") as raw_tmp:
    tmp = Path(raw_tmp)
    env = os.environ.copy()
    env.update({
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
    })

    statement_out = run(
        ["lake", "env", "lean", str(HERE / "Statement.lean")], cwd=LEAN_PROJECT, env=env
    )
    validation_out = run(
        ["lake", "env", "lean", str(HERE / "Validation.lean")], cwd=LEAN_PROJECT, env=env
    )
    env["LEAN_PATH"] = f"{tmp}:{base_lean_path}"
    obligation_out = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), "ObligationTree.lean"],
        cwd=HERE,
        env=env,
    )
    proof_out = run(
        ["lake", "env", "lean", "Proof.lean"], cwd=HERE, env=env
    )

assert statement_out.strip() == ""
normalized_obligation = " ".join(obligation_out.split())
normalized_proof = " ".join(proof_out.split())
normalized_validation = " ".join(validation_out.split())
for declaration in ("forward_from_projection", "reverse_from_constructor", "root_of_directions"):
    assert declaration in normalized_obligation and EXPECTED_AXIOMS in normalized_obligation
assert (
    "'AwesomeTheorems.THM_M_1082.Proof.gaussianProcess_iff_finiteDimensionalGaussian' depends on axioms: "
    f"{EXPECTED_AXIOMS}"
) in normalized_proof
assert (
    "'AwesomeTheorems.THM_M_1082.Validation.independentRoot' depends on axioms: "
    f"{EXPECTED_AXIOMS}"
) in normalized_validation

print("PASS THM-M-1082 validation: exact statement, composition, proof root, and direct probe elaborated")
print("PASS trust: checked roots report only propext, Classical.choice, and Quot.sound")
print("PASS provenance: frozen local hashes and clean pinned mathlib revision agree")
print("BLOCKED release gates: cold empty-cache hermetic replay and distinct-runner verification")
