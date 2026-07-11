#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0133-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0133"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0133-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0133"
assert spec["network_policy"] == "denied"
assert isinstance(spec["argv"], list) and spec["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["root_obligation_id"] == "M0133-ROOT"
assert graphs["closure_boundary"]["root_machine_debt"] == "M2"
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
    "M0133-L-MOD",
    "M0133-L-LOWER",
]

for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"

lean_source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(lean_source) is None

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0133-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )

assert "root_compose" in obligation_output
for declaration in (
    "proofTarget_iff_mathlib",
    "exponentFour_proof",
    "exactTarget_of_oddPrimeCases",
):
    assert declaration in proof_output
assert "[propext]" in proof_output
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert axiom in obligation_output
    assert axiom in proof_output

assert receipt["root_decision"] == {
    "machine_debt": "M2",
    "kernel_closed": False,
    "theorem_complete": False,
}
assert receipt["first_failed_gates"] == [
    "proof.root_kernel_closure",
    "hermetic.cold_empty_cache",
    "independent.distinct_runner",
]

print("validation ok: exact target and admitted conditional proof bodies re-elaborated")
print("validation ok: source hygiene, frozen hashes, and clean pinned mathlib checks passed")
print("root open: all-odd-prime premise remains; cut set M0133-L-MOD and M0133-L-LOWER")
print("blocked: cold hermetic replay and distinct-runner independent verification")
