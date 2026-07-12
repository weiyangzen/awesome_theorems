#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0984-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0984"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT,
        env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False)
    if result.returncode:
        raise SystemExit(
            f"validation command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
assert spec["item_id"] == "S56-M-0984-VALIDATION"
assert spec["theorem_id"] == "THM-M-0984"
assert spec["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

expected_inputs = {
    "Statement.lean": "29fd61ee29db46ea9871743ee6f3d2eb3e0b765ae759d908df9dc4a7a5358cfe",
    "ObligationTree.lean": "2182acb84c0651c5fd14b51ca1dec3cbddb39e55da2c0c8922a33d39cc7e8d64",
    "Proof.lean": "00acf210d8546cb6e11f1ed7cbadf91af7c58ec85c552b4dbb68d967fd600f30",
    "obligation-registry.json": "8daf50371304430ca469d63ac68b7d1af8cf03a2f9ada5fd002d154d0e651e89",
    "typed-graphs.json": "5f7f4b2e08b6a6c6494959c0783d3e4adf03ea4912a26792926eb03d13f8454b",
}
for name, expected in expected_inputs.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"

assert digest(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""

prohibited = re.compile(
    r"\b(?:s" + r"orry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search((HERE / name).read_text()) is None, name

with tempfile.TemporaryDirectory(
        prefix="thm-m-0984-validation-", dir=LEAN_ROOT) as directory:
    cache = Path(directory)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (cache / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{lean_path}"
    run(["lake", "env", "lean", "-o", str(cache / "Statement.olean"),
         str(cache / "Statement.lean")], cwd=LEAN_ROOT, env=env)
    run(["lake", "env", "lean", "-o", str(cache / "ObligationTree.olean"),
         str(cache / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    proof_output = run(["lake", "env", "lean", str(cache / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    probe_output = run(["lake", "env", "lean", str(cache / "Validation.lean")], cwd=LEAN_ROOT, env=env)

normalized_proof = " ".join(proof_output.split())
normalized_probe = " ".join(probe_output.split())
expected_axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
assert normalized_proof.count(expected_axioms) == 2
assert normalized_probe.count(expected_axioms) == 1
assert "declaration uses 'sorry'" not in proof_output + probe_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0984-L-TERMINAL"]

print("PASS narrow kernel replay: exact proof, frozen composition, and separately written exact-target probe elaborated")
print("PASS trust observation: three root-relevant declarations report only propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen input hashes, registry denominator, clean pinned mathlib, toolchain, and manifest agree")
print("STALE authoritative graph: terminal/root remain open pending master reconciliation with proof evidence")
print("BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, unresolved H1/R3, and no distinct runner")
