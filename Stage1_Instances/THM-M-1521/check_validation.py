#!/usr/bin/env python3
"""Fail-closed node validator for S56-M-1521-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1521"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-1521-VALIDATION"
assert spec["theorem_id"] == "THM-M-1521"
assert spec["network_policy"] == "denied"
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(HERE / "ObligationTree.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(HERE / "obligation-registry.json")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
terminal_source = MATHLIB / "Mathlib" / "Dynamics" / "Ergodic" / "Conservative.lean"
terminal_olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / "Mathlib" / "Dynamics" / "Ergodic" / "Conservative.olean"
assert digest(terminal_source) == proof_receipt["proof_body"]["terminal_source_sha256"]
assert digest(terminal_olean) == proof_receipt["proof_body"]["terminal_olean_sha256"]
assert digest(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"

prohibited = re.compile(
    r"\b(?:s" + r"orry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search((HERE / name).read_text()) is None, name

with tempfile.TemporaryDirectory(prefix="thm-m-1521-validation-") as directory:
    cache = Path(directory)
    modules = cache / "Stage1_Instances" / "THM-M-1521"
    modules.mkdir(parents=True)
    common = ["lake", "env", "lean", "-R", str(ROOT)]
    run(common + ["-o", str(modules / "Statement.olean"), str(HERE / "Statement.lean")], cwd=LEAN_ROOT)
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    run(common + ["-o", str(modules / "ObligationTree.olean"), str(HERE / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    proof_output = run(common + [str(HERE / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    independent_output = run(common + [str(HERE / "Validation.lean")], cwd=LEAN_ROOT, env=env)

expected = "depends on axioms: [propext, Classical.choice, Quot.sound]"
assert " ".join(proof_output.split()).count(expected) == 5
assert " ".join(independent_output.split()).count(expected) == 1
assert "declaration uses 'sorry'" not in proof_output + independent_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == {
    "M1521-L-CONSERVATIVE", "M1521-L-RECURRENCE"
}

print("PASS narrow kernel replay: exact proof and independent direct exact-target probe elaborated")
print("PASS trust observation: six checked declarations report only propext, Classical.choice, and Quot.sound")
print("PASS provenance: proof inputs, pinned clean mathlib revision, terminal source, and terminal olean hashes agree")
print("STALE authoritative graph: frozen proof cut remains open although the proof receipt proposes root closure")
print("BLOCKED release gates: warm shared cache, incomplete TCB/SBOM archive, and no distinct independently provisioned runner")
