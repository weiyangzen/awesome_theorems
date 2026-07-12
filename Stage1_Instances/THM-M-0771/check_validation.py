#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0771-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0771"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0771-VALIDATION"
assert spec["theorem_id"] == "THM-M-0771"
assert spec["depends_on"] == ["S56-M-0771-PROOF"]
assert receipt["item_id"] == spec["item_id"]
assert receipt["theorem_id"] == spec["theorem_id"]
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert registry["denominator_sha256"] == proof_receipt["inputs"]["obligation_denominator_sha256"]
assert graphs["theorem_id"] == registry["theorem_id"]
assert {node["obligation_id"] for node in graphs["nodes"]} == {
    obligation["obligation_id"] for obligation in registry["obligations"]
}
for recipe in spec["recipes"]:
    assert isinstance(recipe["argv"], list)
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"
independent_source = (HERE / "Validation.lean").read_text()
assert "import Proof" not in independent_source
assert "import ObligationTree" not in independent_source
assert "wellOrderingTheorem_proof" not in independent_source

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
terminal_source = mathlib / "Mathlib" / "SetTheory" / "Cardinal" / "Order.lean"
assert digest(terminal_source) == receipt["provenance"]["terminal_source_sha256"]
assert prohibited.search(terminal_source.read_text()) is None

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip()
assert digest(Path(lean)) == receipt["environment"]["lean_executable_sha256"]
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0771-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    base_env = env.copy()
    base_env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=tmp, env=base_env,
    )
    module_env = base_env.copy()
    module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        [lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=tmp, env=module_env,
    )
    for name in ("Proof.lean", "Validation.lean"):
        outputs[name] = run([lean, str(tmp / name)], cwd=tmp, env=module_env)

for name, declaration in (
    ("Proof.lean", "wellOrderingTheorem_proof"),
    ("Validation.lean", "independentlyReconstructedRoot"),
):
    output = outputs[name]
    assert declaration in output and "depends on axioms:" in output
    observed = {axiom for axiom in EXPECTED_AXIOMS if axiom in output}
    assert observed == EXPECTED_AXIOMS, f"incomplete axiom report for {name}: {observed}"
    assert "sorryAx" not in output
assert "does not depend on any axioms" in outputs["ObligationTree.lean"]

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert receipt["result"]["theorem_complete"] is False
print("PASS THM-M-0771 narrow kernel replay: exact proof and separately written exact root elaborated")
print("PASS THM-M-0771 trust/provenance: pinned clean mathlib and exact classical axiom set")
print("BLOCKED release gates: provisional proof dependency, stale graph, cold hermetic replay, distinct runner, H0/R0")
