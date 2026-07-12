#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1524-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1524"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT,
        env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=120, check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-1524-VALIDATION"
assert spec["theorem_id"] == "THM-M-1524"
assert spec["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

expected_inputs = {
    "Statement.lean": "2913314de7466b4ed37d90d6cf58a522f7a682943dcde0686962e6927478563f",
    "ObligationTree.lean": "ff4f6a2946f958888ed4b8b14c59ac89b1a9f100bb0610594760b4eb13dcf7f6",
    "Proof.lean": "c34bd2e9c8ac4fd203fed534d8eceb7809f1d1971c4b91959c90c73a0860e9d5",
}
for name, expected in expected_inputs.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"

assert digest(LEAN_ROOT / "lean-toolchain") == \
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == \
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""

prohibited = re.compile(
    r"\b(?:s" + r"orry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    assert prohibited.search((HERE / name).read_text()) is None, name

with tempfile.TemporaryDirectory(prefix="thm-m-1524-validation-") as directory:
    cache = Path(directory)
    module_dir = cache / "Stage1_Instances" / "THM-M-1524"
    module_dir.mkdir(parents=True)
    common = ["lake", "env", "lean", "-R", str(ROOT)]
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    outputs = []
    for source in ("Statement", "ObligationTree", "Proof"):
        outputs.append(run(
            common + ["-o", str(module_dir / f"{source}.olean"),
                      str(HERE / f"{source}.lean")],
            cwd=LEAN_ROOT, env=env,
        ))
    probe_output = run(common + [str(HERE / "Validation.lean")], cwd=LEAN_ROOT, env=env)

proof_output = outputs[-1]
expected_axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
assert " ".join(proof_output.split()).count(expected_axioms) == 3
assert " ".join(probe_output.split()).count(expected_axioms) == 1
assert "declaration uses 'sorry'" not in proof_output + probe_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False

print("PASS narrow kernel replay: exact components, root proof, and exact-type probe elaborated")
print("PASS trust observation: four declarations report only propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen hashes, clean pinned mathlib, toolchain, and manifest agree")
print("STALE authoritative graph: root remains open pending master reconciliation with proof evidence")
print("BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner")
