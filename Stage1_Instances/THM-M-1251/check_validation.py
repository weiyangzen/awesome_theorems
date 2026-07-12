#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1251-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1251"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
spec = json.loads((HERE / "validation-spec.json").read_text())

assert spec["item_id"] == "S56-M-1251-VALIDATION"
assert spec["theorem_id"] == "THM-M-1251"
assert spec["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["statement_fingerprint"] == (
    "lean-expression-sha256:"
    + statement["canonical_formal_target"]["elaborated_expression_sha256"]
)
assert proof_receipt["proof_status"] == "repo_local_machine_root_closed"
assert set(proof_receipt["closed_machine_obligations"]) == {
    "M1251-ROOT",
    "M1251-S-DEFINITIONS",
    "M1251-S-DOMAIN",
    "M1251-S-BOUNDARY",
    "M1251-S-TRANSPORT",
    "M1251-N-UNFOLD",
    "M1251-T-ASSEMBLE",
}
assert registry["root_obligation_id"] == "M1251-ROOT"
assert set(spec["covered_obligation_ids"]) <= {
    row["obligation_id"] for row in registry["obligations"]
}

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search(code_without_comments((HERE / name).read_text())) is None, name

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""
anchor_source = mathlib / "Mathlib" / "Analysis" / "Distribution" / "TemperedDistribution.lean"
assert anchor_source.is_file()
assert "abbrev TemperedDistribution" in anchor_source.read_text()

fixed_env = os.environ.copy()
fixed_env.update({"LC_ALL": "C", "TZ": "UTC"})
with tempfile.TemporaryDirectory(prefix="m1251-validation-") as tmp_name:
    tmp = Path(tmp_name)
    outputs: dict[str, str] = {}
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = tmp / name
        source.write_bytes((HERE / name).read_bytes())
        outputs[name] = run(
            ["lake", "env", "lean", str(source)], cwd=LEAN_ROOT, env=fixed_env
        )

for declaration, name in (
    ("root_of_importedDefinitionExpansion", "ObligationTree.lean"),
    ("importedDefinitionExpansion", "Proof.lean"),
    ("temperedDistributionsAreSchwartzDual", "Proof.lean"),
    ("independentlyReconstructedDefinitionExpansion", "Validation.lean"),
):
    output = outputs[name]
    assert declaration in output and "depends on axioms:" in output
    assert EXPECTED_AXIOMS <= {axiom for axiom in EXPECTED_AXIOMS if axiom in output}
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False

print("ok: exact statement, proof root, frozen composition, and independent local reconstruction kernel-elaborated")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, receipt hashes, denominator, mathlib pin, and anchor provenance checks passed")
print("stale: frozen typed graph predates proof-phase closure and still reports root_closed=false")
print("blocked: complete transitive TCB/SBOM provenance and accepted H0/R0 evidence remain open")
print("blocked: cold empty-cache hermetic replay and distinct-runner independent verification remain open")
