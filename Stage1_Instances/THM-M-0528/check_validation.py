#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0528-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0528"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BASIC_SOURCE_SHA256 = "c9f48cf15f3740dea92c17c6943bf718865d9e4d28410433f4cf219f17843890"
BASIC_OLEAN_SHA256 = "24f220addb5c422a90b954236031b6736a508ac4cb2fa0cc242b07fd4f2f7af0"
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
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
spec = json.loads((HERE / "validation-spec.json").read_text())

assert spec["item_id"] == "S56-M-0528-VALIDATION"
assert spec["theorem_id"] == "THM-M-0528"
recipe = spec["recipes"][0]
assert recipe["argv"] == [
    "python3",
    "Stage1_Instances/THM-M-0528/check_validation.py",
]
assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["result"]["root_kernel_closed"] is True

required_machine = set(registry["frozen_denominators"]["required_machine"])
assert required_machine == {
    "M0528-ROOT",
    "M0528-S-DEFINITIONS",
    "M0528-S-DOMAIN",
    "M0528-S-TRANSPORT",
    "M0528-S-FOUNDATION",
    "M0528-L-SEPARATED",
    "M0528-L-LOCAL-INJECTIVE",
    "M0528-L-PROPAGATE",
    "M0528-X-ANCHOR",
    "M0528-T-ASSEMBLE",
}
assert set(proof_receipt["closed_obligation_ids"]) <= required_machine
assert set(registry["frozen_denominators"]["inventory"]) == {
    row["obligation_id"] for row in registry["obligations"]
}

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = code_without_comments((HERE / name).read_text())
    assert prohibited.search(source) is None, f"prohibited source token in {name}"

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
basic_source = mathlib / "Mathlib/Topology/Covering/Basic.lean"
basic_olean = mathlib / ".lake/build/lib/lean/Mathlib/Topology/Covering/Basic.olean"
assert digest(basic_source) == BASIC_SOURCE_SHA256
assert digest(basic_olean) == BASIC_OLEAN_SHA256
terminal_source = basic_source.read_text()
assert "theorem eq_of_comp_eq [PreconnectedSpace A]" in terminal_source
assert "hf.isSeparatedMap.eq_of_comp_eq hf.isLocalHomeomorph.isLocallyInjective" in terminal_source

with tempfile.TemporaryDirectory(prefix="m0528-validation-", dir=LEAN_ROOT) as tmp_name:
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
    ("root_of_exactPointwiseAnchor", obligation_output),
    ("coveringLiftUniqueness", proof_output),
    ("independentlyReconstructedCoveringLiftUniqueness", validation_output),
    ("IsCoveringMap.eq_of_comp_eq", validation_output),
):
    assert declaration in output and "depends on axioms:" in output
    assert all(axiom in output for axiom in EXPECTED_AXIOMS)
    assert "sorryAx" not in output

assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M0528-X-ANCHOR"]

print("ok: exact statement, conditional composition, proof root, and independent exact-root reconstruction elaborated freshly")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: frozen hashes, proof receipt, clean mathlib pin, terminal source, and compiled artifact passed")
print("stale: frozen graph predates proof closure and still reports M0528-X-ANCHOR open")
print("blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner verification")
