#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1131-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1131"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation failed: command exited {result.returncode}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
anchor = json.loads((HERE / "anchor-audit.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

assert spec["item_id"] == "S56-M-1131-VALIDATION"
assert spec["theorem_id"] == "THM-M-1131"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert registry["root_obligation_id"] == "M1131-ROOT"

sources = {
    name: (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
}
combined_source = "\n".join(sources.values())
for pattern in (r"\b(?:sorry|admit)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, combined_source, re.MULTILINE) is None, pattern
assert "import Proof" not in sources["Validation.lean"]
assert "import ObligationTree" not in sources["Validation.lean"]

assert digest(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == anchor["immutable_environment"]["mathlib_revision"]
assert run(["git", "status", "--short"], cwd=mathlib) == ""
upstream = mathlib / "Mathlib/Analysis/Calculus/FDeriv/Add.lean"
assert digest(upstream) == anchor["candidates"][1]["source_sha256"]["Mathlib/Analysis/Calculus/FDeriv/Add.lean"]

with tempfile.TemporaryDirectory(prefix="m1131-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in sources:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    base_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{base_path}"
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT, env=env)
    tree_output = run(["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    independent_output = run(["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

assert "sorryAx" not in tree_output + proof_output + independent_output
for declaration in ("fderiv_const_mul_apply", "divergence_const_mul", "fluxDivergencePackage", "fourierHeatConductionLaw"):
    assert declaration in proof_output
assert "independentRoot" in independent_output
for output in (proof_output, independent_output):
    assert {axiom for axiom in EXPECTED_AXIOMS if axiom in output} == EXPECTED_AXIOMS

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False

print("ok: exact statement, frozen composition, proof root, and independent direct root elaborated in a fresh temporary directory")
print("ok: both root paths report only propext, Classical.choice, and Quot.sound; placeholder and unsafe scans passed")
print("ok: frozen hashes, toolchain, mathlib pin, clean dependency checkout, and terminal source provenance passed")
print("stale: the pre-proof typed graph retains its open M3 root pending master reconciliation")
print("blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
