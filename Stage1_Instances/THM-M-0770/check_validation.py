#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0770-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0770"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0770-VALIDATION"
assert spec["theorem_id"] == "THM-M-0770"
assert receipt["item_id"] == spec["item_id"]
assert receipt["theorem_id"] == spec["theorem_id"]
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert proof_receipt["result"]["root_closed"] is True
assert set(proof_receipt["closed_obligation_ids"]) == {
    "M0770-ROOT", "M0770-L-ZORN-ANCHOR", "M0770-T-ASSEMBLE"
}

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
terminal_source = mathlib / "Mathlib" / "Order" / "Zorn.lean"
assert digest(terminal_source) == receipt["provenance"]["terminal_source_sha256"]
assert prohibited.search(terminal_source.read_text()) is None

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0770-validation-") as tmp_name:
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
    ("Proof.lean", "zornsLemma"),
    ("Validation.lean", "independentlyReconstructedRoot"),
):
    output = outputs[name]
    assert declaration in output and "depends on axioms:" in output
    assert {axiom for axiom in EXPECTED_AXIOMS if axiom in output} == EXPECTED_AXIOMS
    assert "sorryAx" not in output

assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
print("ok: exact proof root and independently reconstructed zorn_le root kernel-replayed")
print("ok: clean pinned mathlib source, expected classical axioms, and placeholder policy verified")
print("blocked: master acceptance, graph freshness, cold hermetic replay, and distinct-runner gates remain open")
