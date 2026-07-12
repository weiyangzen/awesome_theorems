#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0981-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0981"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT,
        env: dict[str, str] | None = None) -> str:
    result = subprocess.run(argv, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=120, check=False)
    if result.returncode:
        raise SystemExit(
            f"validation command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert spec["item_id"] == "S56-M-0981-VALIDATION"
assert spec["theorem_id"] == "THM-M-0981"
assert spec["network_policy"] == "denied"
assert registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json")
assert json.loads((HERE / "statement.json").read_text())["canonical_formal_target"][
    "statement_file_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

expected_inputs = {
    "Statement.lean": "408aadc82cfb3f51828d957ef6f8a0e2b15287060ea0ae8defe56a24af3454b3",
    "ObligationTree.lean": "073916d54befff1ff0db0c9b80256b0c34fae7c323e1731cfdbd137f73b94eef",
    "Proof.lean": "3a29ae1d0ad5932aef7406dcd5b14aaa3d3c1e7905b6f965f441e7776ef2902d",
}
for name, expected in expected_inputs.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert receipt["inputs"]["statement_sha256"] == expected_inputs["Statement.lean"]
assert receipt["inputs"]["obligation_tree_sha256"] == expected_inputs["ObligationTree.lean"]
assert receipt["proof_body"]["source_sha256"] == expected_inputs["Proof.lean"]

assert digest(LEAN_ROOT / "lean-toolchain") == \
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == \
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""

prohibited = re.compile(
    r"\b(?:s" + r"orry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search((HERE / name).read_text()) is None, name

with tempfile.TemporaryDirectory(prefix="thm-m-0981-validation-") as directory:
    cache = Path(directory)
    common = ["lake", "env", "lean", "-R", str(ROOT)]
    run(common + ["-o", str(cache / "Statement.olean"),
                  str(HERE / "Statement.lean")], cwd=LEAN_ROOT)
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{run(['lake', 'env', 'printenv', 'LEAN_PATH'], cwd=LEAN_ROOT).strip()}"
    run(common + ["-o", str(cache / "ObligationTree.olean"),
                  str(HERE / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    proof_output = run(common + [str(HERE / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    independent_output = run(common + [str(HERE / "Validation.lean")], cwd=LEAN_ROOT, env=env)

expected_axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
assert " ".join(proof_output.split()).count(expected_axioms) == 5
assert " ".join(independent_output.split()).count(expected_axioms) == 1
assert "declaration uses 'sorry'" not in proof_output + independent_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False

print("PASS narrow kernel replay: exact proof, frozen composition, and independent exact-target probe elaborated")
print("PASS trust observation: six declarations report only propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen hashes, proof receipt, clean pinned mathlib, toolchain, and manifest agree")
print("STALE authoritative graph: root remains open pending master reconciliation with proof evidence")
print("BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner")
