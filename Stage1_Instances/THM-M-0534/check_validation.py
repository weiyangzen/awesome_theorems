#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0534-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0534"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-0534-VALIDATION"
assert spec["theorem_id"] == "THM-M-0534"
assert receipt["item_id"] == spec["item_id"]
assert receipt["theorem_id"] == spec["theorem_id"]
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
for recipe in spec["recipes"]:
    assert isinstance(recipe["argv"], list)
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0

assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""
terminal_source = mathlib / "Mathlib" / "Algebra" / "Homology" / "HomologySequence.lean"
assert digest(terminal_source) == receipt["provenance"]["terminal_source_sha256"]
assert prohibited.search(terminal_source.read_text()) is None

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0534-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env = os.environ.copy()
    env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=tmp,
        env=env,
    )
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        [lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=tmp,
        env=env,
    )
    outputs["Proof.lean"] = run([lean, str(tmp / "Proof.lean")], cwd=tmp, env=env)
    outputs["Validation.lean"] = run(
        [lean, str(tmp / "Validation.lean")], cwd=tmp, env=env
    )

for filename, declaration in (
    ("Proof.lean", "longExactHomologySequence"),
    ("Proof.lean", "longExactHomologySequence_via_families"),
    ("Validation.lean", "independentlyReconstructedLongExactHomologySequence"),
):
    output = outputs[filename]
    assert declaration in output and "depends on axioms:" in output
    observed = {axiom for axiom in EXPECTED_AXIOMS if axiom in output}
    assert observed == EXPECTED_AXIOMS, f"incomplete axiom report for {declaration}"
    assert "sorryAx" not in output

# The graph is intentionally the pre-proof frozen snapshot. A worker must not rewrite
# authoritative state merely because a later proof replay succeeds.
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["root_machine_debt"] == "M1"
assert closure["theorem_complete"] is False

print("PASS S56-M-0534-VALIDATION: exact proof and independent root reconstruction kernel-replayed")
print("PASS pinned clean mathlib source, source hashes, placeholder policy, and classical axiom observation")
print("FAIL-CLOSED authoritative graph freshness, cold hermetic replay, complete transitive TCB/provenance, and distinct-runner independence remain open")
