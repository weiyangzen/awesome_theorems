#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0311-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0311"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
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


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0311-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0311"
assert spec["network_policy"] == "denied"
assert isinstance(spec["argv"], list) and spec["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")

for name, digest in receipt["inputs"].items():
    if name in {"lean_toolchain", "lake_manifest"}:
        path = LEAN_ROOT / ("lean-toolchain" if name == "lean_toolchain" else "lake-manifest.json")
    else:
        path = HERE / name
    assert digest == sha256(path), (name, digest, sha256(path))

lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text() for name in lean_files)
for pattern in (
    r"\b(?:sorry|admit|sorryAx)\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern
validation_source = (HERE / "Validation.lean").read_text()
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source
assert "theorem rieszFischerTarget_direct : RieszFischerTarget.{u}" in validation_source

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0311-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_files:
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
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    validation_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

for declaration, output in (
    ("obligationTreeTarget_of_scalar_children", obligation_output),
    ("realL2Complete_proof", proof_output),
    ("complexL2Complete_proof", proof_output),
    ("obligationTreeTarget_proof", proof_output),
    ("rieszFischerTarget_proof", proof_output),
    ("rieszFischerTarget_direct", validation_output),
):
    match = re.search(
        rf"[^\n]*{re.escape(declaration)}[^\n]*depends on axioms:\s*\[([^]]+)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    observed = {part.strip() for part in match.group(1).replace("\n", " ").split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)

closure = graphs["closure_boundary"]
assert closure["root_machine_debt"] == "M3"
assert closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == {"M0311-B-REAL", "M0311-B-COMPLEX"}
assert receipt["result"]["exact_root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)

print("PASS narrow kernel replay: exact statement, scalar branches, composition, and exact root elaborated")
print("PASS trust observation: all proof and differential declarations report propext, Classical.choice, and Quot.sound")
print("PASS local provenance: source/receipt hashes, registry denominator, and clean pinned mathlib revision agree")
print("PASS same-worker differential probe: exact root reconstructed without importing Proof or ObligationTree")
print("STALE frozen graph: real and complex branches remain candidate M3 pending master reconciliation")
print("BLOCKED release gates: warm shared .lake, incomplete transitive TCB/SBOM closure, and no distinct independent runner")
