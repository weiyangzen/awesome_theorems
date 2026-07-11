#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0009-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0009"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
UPSTREAM_SHA256 = "0aa08f6a0505e9ef22e03937f2d55e3f35287b4a731282cd7cd1d3e9c0fb7242"
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
anchor_audit = json.loads((HERE / "anchor-audit.json").read_text())
spec = json.loads((HERE / "validation-spec.json").read_text())

assert spec["item_id"] == "S56-M-0009-VALIDATION"
assert spec["theorem_id"] == "THM-M-0009"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["result"]["root_closed"] is True

required_closed = {
    "M0009-ROOT",
    "M0009-B-COV",
    "M0009-B-CONTRA",
    "M0009-C-COV-SEQ",
    "M0009-C-CONTRA-SEQ",
    "M0009-L-COV-EXACT",
    "M0009-L-CONTRA-EXACT",
    "M0009-T-ASSEMBLE",
}
assert set(proof_receipt["closed_obligation_ids"]) == required_closed
assert registry["root_obligation_id"] == "M0009-ROOT"
assert set(registry["frozen_denominators"]["inventory"]) == {
    item["obligation_id"] for item in registry["obligations"]
}

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = code_without_comments((HERE / name).read_text())
    assert prohibited.search(source) is None, f"prohibited source token in {name}"

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""
upstream = mathlib / "Mathlib/Algebra/Homology/DerivedCategory/Ext/ExactSequences.lean"
assert digest(upstream) == UPSTREAM_SHA256
for candidate in anchor_audit["candidates"]:
    assert candidate["revision"] == MATHLIB_REVISION
    assert candidate["file_sha256"] == UPSTREAM_SHA256

with tempfile.TemporaryDirectory(prefix="m0009-validation-", dir=LEAN_ROOT) as tmp_name:
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
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    validation_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

for declaration, output in (
    ("root_compose", obligation_output),
    ("longExactExtSequence", proof_output),
    ("independentlyReconstructedLongExactExtSequence", validation_output),
):
    assert declaration in output and "depends on axioms:" in output
    assert all(axiom in output for axiom in EXPECTED_AXIOMS)
    assert "sorryAx" not in output

for declaration in ("covariantSequence_exact", "contravariantSequence_exact"):
    assert declaration in validation_output and "depends on axioms:" in validation_output

assert graphs["closure_boundary"]["root_closed"] is False
assert set(graphs["closure_boundary"]["remaining_root_cut_set"]) == {
    "M0009-L-COV-EXACT",
    "M0009-L-CONTRA-EXACT",
}

print("ok: exact proof and independently reconstructed wrapper elaborated in a fresh temporary module directory")
print("ok: root and terminal declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, proof-receipt hashes, frozen denominator, and clean pinned mathlib provenance passed")
print("stale: frozen graph predates proof closure and still reports both exactness leaves open")
print("blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner independent verification")
