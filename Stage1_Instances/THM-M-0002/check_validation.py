#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0002-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0002"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


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
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

assert spec["item_id"] == "S56-M-0002-VALIDATION"
assert spec["theorem_id"] == "THM-M-0002"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False

source = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(r"\b(?:sorry|admit)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
code = "\n".join(
    line for line in source.splitlines()
    if not line.lstrip().startswith(("--", "/-", "*", "-/"))
)
assert prohibited.search(code) is None

assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
four_source = MATHLIB / "Mathlib/CategoryTheory/Abelian/DiagramLemmas/Four.lean"
assert digest(four_source) == (
    "ba493086183f2aa2ffdd607f6ce25bbf96f9fedd19a89f9db0ef10067303ce3a"
)

with tempfile.TemporaryDirectory(prefix="m0002-validation-", dir=LEAN_ROOT) as tmp_name:
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
    ("fiveLemma", proof_output),
    ("independentFiveLemma", validation_output),
):
    assert declaration in output
    for allowed_axiom in ("propext", "Classical.choice", "Quot.sound"):
        assert allowed_axiom in output
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == {"M0002-B-MONO", "M0002-B-EPI"}

print("ok: frozen statement, obligation composition, and proof elaborate in a fresh temporary module directory")
print("ok: an independently implemented exact-root probe elaborates through the pinned mathlib five lemma")
print("ok: placeholder scan, source hashes, registry denominator, dependency pin, and mathlib cleanliness passed")
print("observed axioms: propext, Classical.choice, Quot.sound")
print("stale: frozen graph predates the proof receipt and still reports B-MONO/B-EPI open")
print("blocked: cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
