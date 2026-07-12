#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1515-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1515"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "60b548f2032771a84c7da069e9343a74544294380dec21d041f492c880989add",
    "ObligationTree.lean": "46fe18ed3c9a8f7f490ac2898fa891dd2344991ad22996c721facc61893c4f27",
    "Proof.lean": "bab403a8dbb3f4bbfd0b4180190218913640246d2eac233bebfb451acd91552a",
    "statement.json": "b9aa35f6b647cfd61b96eadeb2fe4f789acb8730f5a30adcecd667dfbf777394",
    "obligation-registry.json": "6d0a1f5348ec5947a7d4f1c0437eb302cbfbcf346cbdc02ad2a9e88be23de3b1",
    "typed-graphs.json": "08d454c3243edac8f0e03bd17078f57b379f5a52282d6ca30fc1931067bb7a43",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-1515-VALIDATION"
assert spec["theorem_id"] == "THM-M-1515"
for name, expected in EXPECTED_HASHES.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert registry["root_obligation_id"] == "M1515-ROOT"
assert {item["obligation_id"] for item in registry["obligations"]} == set(
    registry["frozen_denominators"]["inventory"]
)

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search(code_without_comments((HERE / name).read_text())) is None, (
        f"prohibited source token in {name}"
    )

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m1515-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Proof.olean"), str(tmp / "Proof.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    validation_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

for declaration, output in (
    ("root_of_derivative_packages", obligation_output),
    ("boundary_along_curve_derivative", proof_output),
    ("momentum_pairing_derivative", proof_output),
    ("noether_first_theorem", proof_output),
    ("exact_root_probe", validation_output),
):
    assert declaration in output and "depends on axioms:" in output
    assert all(axiom in output for axiom in EXPECTED_AXIOMS)
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert set(closure["minimal_open_root_cut"]) == {
    "M1515-L-MOMENTUM-DERIV",
    "M1515-L-BOUNDARY-DERIV",
}

print("ok: exact frozen target, composition, proof, and exact-type probe elaborated in a fresh temporary module directory")
print("ok: root and analytic declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, frozen hashes and denominator, toolchain pins, and clean pinned mathlib checks passed")
print("stale: frozen graph predates proof closure and still reports both analytic packages and root open")
print("blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner independent verification")
