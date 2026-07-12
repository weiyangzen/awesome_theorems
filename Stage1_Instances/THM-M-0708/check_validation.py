#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0708-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0708"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env=None) -> str:
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


registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
spec = json.loads((HERE / "validation-spec.json").read_text())
validation_receipt = json.loads((HERE / "validation-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0708-VALIDATION"
assert spec["theorem_id"] == registry["theorem_id"] == "THM-M-0708"
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False
assert validation_receipt["inputs"]["validation_spec_sha256"] == digest(
    HERE / "validation-spec.json"
)
assert validation_receipt["inputs"]["independent_probe_sha256"] == digest(
    HERE / "Validation.lean"
)
assert validation_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert validation_receipt["inputs"]["typed_graphs_sha256"] == digest(HERE / "typed-graphs.json")

for recipe in spec["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["argv"]
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0

sources = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(sources) is None
validation_source = (HERE / "Validation.lean").read_text()
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source

assert digest(LEAN_ROOT / "lean-toolchain") == \
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == \
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0708-validation-", dir=LEAN_ROOT) as tmp_name:
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
    tree_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    independent_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )


def observed_axioms(output: str, declaration: str) -> set[str]:
    lines = output.splitlines()
    start = next(i for i, line in enumerate(lines) if declaration in line and "depends on axioms" in line)
    report = "\n".join(lines[start:])
    bracketed = re.search(r"depends on axioms: \[([^]]*)\]", report, re.DOTALL)
    if bracketed:
        return {axiom.strip() for axiom in bracketed.group(1).split(",") if axiom.strip()}
    axioms = set()
    for line in lines[start + 1:]:
        if not line.startswith("  "):
            break
        match = re.match(r"  ([^:]+)", line)
        if match:
            axioms.add(match.group(1))
    return axioms


for declaration, output in (
    ("root_of_riceBridge", tree_output),
    ("riceBridge", proof_output),
    ("riceTheorem", proof_output),
    ("riceTheorem_direct", proof_output),
    ("riceTheorem_independent", independent_output),
    ("ComputablePred.rice", independent_output),
):
    assert observed_axioms(output, declaration) == EXPECTED_AXIOMS, (
        declaration,
        observed_axioms(output, declaration),
    )

assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["root_machine_debt"] == "M3"

print("PASS isolated warm-cache kernel replay: statement, composition, proof root, and independent direct root elaborated")
print("PASS trust observation: six declarations report exactly propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen statement/registry/proof hashes and clean pinned mathlib revision agree")
print("STALE frozen graph: pre-proof M3 root remains pending master reconciliation")
print("BLOCKED release gates: shared warm .lake, incomplete transitive TCB/SBOM, and no distinct independent runner")
