#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0082-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0082"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
UPSTREAM_SOURCE_SHA256 = "38a9febac8fd666a6fdaa7167e8b5291f2d01d43fa131849a7124f1bb2de30e1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


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
            f"command failed ({result.returncode}): {' '.join(argv)}\n{result.stdout}"
        )
    return result.stdout


spec = load("validation-spec.json")
statement = load("statement.json")
anchor = load("anchor-audit.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")

assert spec["item_id"] == "S56-M-0082-VALIDATION"
assert spec["theorem_id"] == "THM-M-0082"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert anchor["environment"]["mathlib_revision"] == MATHLIB_PIN
assert anchor["environment"]["mathlib_source_sha256"] == UPSTREAM_SOURCE_SHA256

source = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
code = "\n".join(
    line for line in source.splitlines()
    if not line.lstrip().startswith(("--", "/-", "*", "-/"))
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(code) is None

assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
assert digest(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert digest(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
upstream = MATHLIB / "Mathlib/CategoryTheory/Adjunction/AdjointFunctorTheorems.lean"
assert digest(upstream) == UPSTREAM_SOURCE_SHA256
upstream_text = upstream.read_text(encoding="utf-8")
assert "lemma isRightAdjoint_of_preservesLimits_of_solutionSetCondition" in upstream_text
assert "has_weakly_initial_of_weakly_initial_set_and_hasProducts" in upstream_text
assert "hasInitial_of_weakly_initial_and_hasWideEqualizers" in upstream_text

with tempfile.TemporaryDirectory(prefix="m0082-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    module_dir = tmp / "Stage1_Instances" / "THM-M-0082"
    module_dir.mkdir(parents=True)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (module_dir / name).write_bytes((HERE / name).read_bytes())
    statement_output = run(
        ["lake", "env", "lean", "-o", str(module_dir / "Statement.olean"), str(module_dir / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(module_dir / "ObligationTree.olean"), str(module_dir / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(module_dir / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    validation_output = run(
        ["lake", "env", "lean", str(module_dir / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

assert "GeneralRightAdjointTarget" in statement_output
for declaration, output in (
    ("root_of_bridge", obligation_output),
    ("generalRightAdjointBridge", proof_output),
    ("generalRightAdjointTarget", proof_output),
    ("independentGeneralRightAdjointTarget", validation_output),
):
    assert declaration in output
    for allowed_axiom in ("propext", "Classical.choice", "Quot.sound"):
        assert allowed_axiom in output
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0082-X-BRIDGE"]

print("ok: exact statement, obligation composition, and proof elaborate in a fresh temporary module tree")
print("ok: independent exact-root reconstruction elaborates directly through the pinned mathlib declaration")
print("ok: placeholder scan, source hashes, registry denominator, dependency pin, and mathlib cleanliness passed")
print("observed axioms: propext, Classical.choice, Quot.sound")
print("stale: frozen graph predates Proof.lean and still reports M0082-X-BRIDGE open")
print("blocked: H0/R0, authoritative reconciliation, cold hermetic replay, complete TCB/SBOM closure, and distinct-runner verification")
