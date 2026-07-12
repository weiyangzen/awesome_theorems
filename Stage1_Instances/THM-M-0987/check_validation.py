#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0987-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0987"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "4ac6a7cdb7139df6bca2f3eb6b0e211c4ff108ab89b1b99d60186dde75734363",
    "ObligationTree.lean": "3a0d90a9b7416c358948645a6af20490e6273fda37c7f096b2e6de59d4fdb383",
    "Proof.lean": "234794e150172dc78b5fe2534150918151500bff7446ff44365df1c22ba486ae",
    "Validation.lean": "0b3d0f1b9964a50d59008c0f85be737a6b20eb12657a298a3669cddbeb22a8ea",
    "statement.json": "33cd8b56d31822cd9aff38806a80e278172140c383deb65335c0c7a92eb048f3",
    "obligation-registry.json": "640e6bb334b771e1cecbff10c8d780b58fc05fb5758ce4455be4cc850c9e2267",
    "typed-graphs.json": "50a58b7533c89583aa0d3aa8e8dbc6c761bd3640a29fed22beac6a2d99c8c700",
    "anchor-audit.json": "771f3208ee8be64e15edf397da31f76d1142a98c3217383302a8c2f111fd789c",
    "validation-phase-spec.json": "4162dc612a0ade68add4152f138383ec074d71b953e60a4fb6fce3b74b6d84ff",
}


def digest(path: Path) -> str:
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
audit = json.loads((HERE / "anchor-audit.json").read_text())
assert spec["item_id"] == "S56-M-0987-VALIDATION"
assert spec["theorem_id"] == "THM-M-0987"
recipe = spec["recipes"][0]
assert recipe["argv"] == ["python3", "Stage1_Instances/THM-M-0987/check_validation.py"]
assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert audit["eligible_anchor"] == "S56-M-0987-C02"

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
terminal_source = mathlib / "Mathlib" / "Probability" / "CentralLimitTheorem.lean"
assert digest(terminal_source) == "4b42bad9589ec3772fe0e884ad70789c89fd0c11566d980f3df1c862bbc7f03d"
assert "theorem tendstoInDistribution_inv_sqrt_mul_sum_sub" in terminal_source.read_text()

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
assert digest(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0987-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env = os.environ.copy()
    env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT, env=env
    )
    outputs["ObligationTree.lean"] = run(
        [lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env
    )
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["Proof.lean"] = run([lean, str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    outputs["Validation.lean"] = run([lean, str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

for name, declaration in (
    ("Proof.lean", "centralLimitTheorem_proof"),
    ("Proof.lean", "canonicalRoot_proof"),
    ("Validation.lean", "independentlyReconstructedTarget"),
    ("Validation.lean", "tendstoInDistribution_inv_sqrt_mul_sum_sub"),
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
