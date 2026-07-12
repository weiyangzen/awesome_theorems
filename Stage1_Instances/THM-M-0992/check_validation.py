#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0992-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0992"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "2bd4c5f2c324432d0544203ddb000385a2affbfc25748a415c9771e6469339aa",
    "ObligationTree.lean": "ade5f0e6af5c4b646568362d16da9319917508c45d642d98ee49187ac558a575",
    "Proof.lean": "27ee879c937dbfaa33d4175eb99c256e6554c0b9694f27fe0fed1bcf04849e54",
    "Validation.lean": "d887a798394af37cb7b7a44459032f781a5f6f07206e4297a3667ebd8fbb5f6b",
    "statement.json": "da2e4f52ad79378209dc66d4c0529dfed00d379cd492b45a6553a8f168fb6f2f",
    "obligation-registry.json": "5b015fa17f22b1689bf421131a470871c0771d486e19845e518c7b9be869da1b",
    "typed-graphs.json": "e561965d37e23db59959858defce7b7c868729afda9fbcab7d809347299536e1",
    "anchor-audit.json": "61967a6aa213bc6b1eea821b8b88bd6bf9ca4654280fa3e51545cc40c2b6b535",
    "validation-phase-spec.json": "934ca3d41017b93c98a48ae1a879c740b75b17b27c97b40b63c77b3870cffc04",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


for name, expected in EXPECTED_HASHES.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)

spec = json.loads((HERE / "validation-phase-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
assert spec["item_id"] == "S56-M-0992-VALIDATION"
assert spec["theorem_id"] == "THM-M-0992"
recipe = spec["recipes"][0]
assert recipe["argv"] == ["python3", "Stage1_Instances/THM-M-0992/check_validation.py"]
assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
terminal_source = mathlib / "Mathlib" / "Probability" / "Moments" / "Variance.lean"
assert digest(terminal_source) == "920c022075149257307335beccbc8a62c7360fb3d9d73571b8240093dc2d72f0"
assert "theorem meas_ge_le_variance_div_sq" in terminal_source.read_text()

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
assert digest(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0992-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env = os.environ.copy()
    env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=tmp, env=env
    )
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        [lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")], cwd=tmp, env=env
    )
    outputs["Proof.lean"] = run([lean, str(tmp / "Proof.lean")], cwd=tmp, env=env)
    outputs["Validation.lean"] = run([lean, str(tmp / "Validation.lean")], cwd=tmp, env=env)

for name, declaration in (
    ("Proof.lean", "chebyshev_inequality"),
    ("Validation.lean", "independentlyReconstructedTarget"),
    ("Validation.lean", "meas_ge_le_variance_div_sq"),
):
    output = outputs[name]
    assert declaration in output and "depends on axioms:" in output
    observed = {axiom for axiom in EXPECTED_AXIOMS if axiom in output}
    assert observed == EXPECTED_AXIOMS
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False and closure["theorem_complete"] is False
print("ok: exact frozen root, proof composition, and independent exact transcription kernel-replayed")
print("ok: observed axioms are propext, Classical.choice, and Quot.sound; no sorryAx")
print("ok: frozen hashes, denominator, recipe, placeholder policy, and clean pinned mathlib passed")
print("blocked: frozen state predates proof closure; cold hermetic and distinct-runner gates remain open")
