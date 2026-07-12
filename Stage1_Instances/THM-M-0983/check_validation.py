#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0983-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0983"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(argv, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=120, check=False)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
assert spec["item_id"] == "S56-M-0983-VALIDATION"
assert spec["theorem_id"] == "THM-M-0983"
assert receipt["item_id"] == spec["item_id"]
assert receipt["theorem_id"] == spec["theorem_id"]
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
recipe = spec["recipes"][0]
assert isinstance(recipe["argv"], list) and recipe["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
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
assert run(["git", "status", "--short"], cwd=mathlib) == ""
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()

outputs = {}
with tempfile.TemporaryDirectory(prefix="m0983-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env = os.environ.copy()
    env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run([lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT, env=env)
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run([lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    outputs["Proof.lean"] = run([lean, str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    outputs["Validation.lean"] = run([lean, str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

for name, declaration in (
    ("Proof.lean", "bernoulliStrongLaw_proof"),
    ("Proof.lean", "obligationTarget_proof"),
    ("Validation.lean", "independentlyReconstructedTarget"),
):
    output = outputs[name]
    assert declaration in output and "depends on axioms:" in output
    assert EXPECTED_AXIOMS <= {a for a in EXPECTED_AXIOMS if a in output}
    assert "sorryAx" not in output

assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
print("ok: exact proof root and independently reconstructed exact target kernel-replayed")
print("ok: axiom output is exactly within the recorded classical profile; no sorryAx")
print("ok: frozen statement, denominator, structured recipe, placeholder scan, and pinned clean mathlib passed")
print("blocked: frozen structured state predates proof closure; cold hermetic and distinct-runner gates remain open")
