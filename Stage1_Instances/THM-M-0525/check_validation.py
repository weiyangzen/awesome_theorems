#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0525-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0525"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0525-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0525"
assert len(spec["recipes"]) == 1
assert spec["recipes"][0]["argv"] == [
    "python3", "Stage1_Instances/THM-M-0525/check_validation.py"
]
assert statement["canonical_formal_target"]["source_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["root_obligation_id"] == "M0525-ROOT"
assert set(registry["frozen_denominators"]["inventory"]) == {
    item["obligation_id"] for item in registry["obligations"]
}
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

for name, expected in receipt["inputs"].items():
    path = LEAN_ROOT / name if name in ("lean-toolchain", "lake-manifest.json") else HERE / name
    assert digest(path) == expected, f"stale validation input: {name}"

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = code_without_comments((HERE / name).read_text())
    assert prohibited.search(source) is None, f"prohibited source token in {name}"

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--porcelain"], cwd=mathlib) == ""

for key in ("path_laws_source", "path_laws_olean", "minimal_axioms_source", "minimal_axioms_olean"):
    record = receipt["provenance"][key]
    assert digest(mathlib / record["path"]) == record["sha256"], f"provenance drift: {key}"

with tempfile.TemporaryDirectory(prefix="m0525-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env.update({"LEAN_PATH": f"{tmp}:{lean_path}", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    validation_output = run(["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

for declaration, output in (
    ("statement_of_left_laws", obligation_output),
    ("statement_proof", proof_output),
    ("independentlyReconstructedStatement", validation_output),
):
    assert declaration in output and "depends on axioms:" in output
    assert EXPECTED_AXIOMS.issubset(set(re.findall(r"(?:propext|Classical\.choice|Quot\.sound)", output)))
    assert "sorryAx" not in output

for declaration in ("trans_assoc", "refl_trans", "symm_trans"):
    assert declaration in validation_output

assert registry["status_observed_after_freeze"]["root_closed"] is False
assert receipt["result"]["exact_root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0525: exact root, frozen composition, and independent local reconstruction kernel-check")
print("PASS trust observation: declarations report only propext, Classical.choice, and Quot.sound")
print("PASS provenance: pinned clean mathlib source and olean hashes agree; placeholder/unsafe scan passed")
print("FAIL CLOSED release: stale structured state, cold hermetic replay, full TCB, and distinct-runner gates remain open")
