#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1550-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1550"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


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


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


spec = load("validation-spec.json")
statement_record = load("statement.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
assert spec["item_id"] == "S56-M-1550-VALIDATION"
assert spec["theorem_id"] == "THM-M-1550"
assert spec["recipes"][0]["network_policy"] == "denied"
assert registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert statement_record["canonical_formal_target"]["declaration_or_expression"] == \
    "Stage1Instances.THM_M_1550.LaxPairIsospectrality"

expected_inputs = {
    "Statement.lean": "86bca95cf466a9086b94a5f5dd3e24abf422d999c8c4da0547f25030c1bd5445",
    "ObligationTree.lean": "94e7d7039df20cf55a9faf01125cc786dd8ae78eb066bd45dbf7895ebddccc7b",
    "Proof.lean": "9901a5d7670ad898090601fd72104512d97073e1dc344c646a8169b94d4b73da",
    "obligation-registry.json": "38a78bd887a27ae5ad4c0a4415862515aa22d2ef6fed78037ee171a548520e73",
    "typed-graphs.json": "7ef7d777205a5999351f5e6487f7c3b66b3052e87ab849fea7014f32ef579071",
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
    assert prohibited.search((HERE / name).read_text(encoding="utf-8")) is None, name

with tempfile.TemporaryDirectory(prefix="thm-m-1550-validation-") as directory:
    cache = Path(directory)
    common = ["lake", "env", "lean", "-R", str(ROOT)]
    statement_output = run(common + ["-o", str(cache / "Statement.olean"),
                                     str(HERE / "Statement.lean")], cwd=LEAN_ROOT)
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    obligation_output = run(common + ["-o", str(cache / "ObligationTree.olean"),
                                      str(HERE / "ObligationTree.lean")], cwd=LEAN_ROOT,
                            env=env)
    proof_output = run(common + [str(HERE / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    independent_output = run(common + [str(HERE / "Validation.lean")], cwd=LEAN_ROOT, env=env)

all_output = statement_output + obligation_output + proof_output + independent_output
assert "declaration uses 'sorry'" not in all_output
expected_axioms = ("propext", "Classical.choice", "Quot.sound")
for name in expected_axioms:
    assert name in statement_output, f"statement axiom observation omitted {name}"
    assert name in proof_output, f"proof axiom observation omitted {name}"
    assert name in independent_output, f"independent axiom observation omitted {name}"

closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_machine_debt"] == "M3"
assert closure["theorem_complete"] is False

print("PASS narrow kernel replay: statement, composition, proof, and separate reconstruction elaborated")
print("PASS trust observation: checked declarations report only the allowed classical kernel axioms")
print("PASS local provenance: frozen hashes, clean pinned mathlib, toolchain, and manifest agree")
print("STALE authoritative graph: root remains M3 with zero accepted closure pending master reconciliation")
print("BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner")
