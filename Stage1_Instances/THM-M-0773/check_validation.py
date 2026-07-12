#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0773-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0773"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0773-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0773"
assert spec["depends_on"] == ["S56-M-0773-PROOF"]
assert all(r["network_policy"] == "denied" and r["expected_exit"] == 0 for r in spec["recipes"])
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert registry["denominator_sha256"] == proof_receipt["inputs"]["obligation_denominator_sha256"]
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["result"]["root_closed"] is True

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"
validation_source = (HERE / "Validation.lean").read_text()
assert "import Proof" not in validation_source and "import ObligationTree" not in validation_source
assert "pointed_maximal_proof" not in validation_source and "pointed_implies_unpointed" not in validation_source

assert digest(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
terminal = mathlib / "Mathlib" / "Order" / "TeichmullerTukey.lean"
assert digest(terminal) == receipt["provenance"]["terminal_source_sha256"]
assert prohibited.search(terminal.read_text()) is None

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, env=env)
assert "4.29.0" in version and LEAN_COMMIT in version
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
assert digest(lean) == receipt["environment"]["lean_executable_sha256"]
env["LEAN_PATH"] = lean_path

outputs = {}
with tempfile.TemporaryDirectory(prefix="m0773-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    outputs["Statement.lean"] = run(
        [str(lean), "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=tmp, env=env,
    )
    module_env = env.copy()
    module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    for name in ("Proof.lean", "Validation.lean"):
        outputs[name] = run([str(lean), str(tmp / name)], cwd=tmp, env=module_env)

for name, declarations in {
    "Proof.lean": ("pointed_maximal_proof", "teichmullerTukey_proof"),
    "Validation.lean": ("independentlyReconstructedRoot",),
}.items():
    for declaration in declarations:
        line = next(line for line in outputs[name].splitlines() if declaration in line and "depends on axioms" in line)
        assert {a for a in EXPECTED_AXIOMS if a in line} == EXPECTED_AXIOMS, line
        assert "sorryAx" not in line

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False and closure["root_machine_classification"] == "M3"
assert receipt["result"]["theorem_complete"] is False
print("PASS THM-M-0773 narrow kernel replay: exact proof and differential root elaborated")
print("PASS THM-M-0773 trust/provenance: exact classical axiom set and pinned clean mathlib source")
print("STALE frozen graph: pre-proof M3 state awaits master reconciliation")
print("BLOCKED hermetic gate: shared warm .lake is not a cold offline restored cache")
print("BLOCKED independent gate: differential probe ran in this worker and shared cache")
