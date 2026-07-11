#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0420-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0420"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


statement_record = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_phase = json.loads((HERE / "proof-phase.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())

assert receipt["item_id"] == "S56-M-0420-VALIDATION"
assert receipt["theorem_id"] == "THM-M-0420"
assert specs["theorem_id"] == registry["theorem_id"] == graphs["theorem_id"]
assert statement_record["canonical_formal_target"]["statement_file_sha256"] == sha256(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_phase["statement_source_sha256"] == sha256(HERE / "Statement.lean")
assert proof_phase["closed_obligation_ids"] == ["M0420-N1"]
for name, digest in receipt["inputs"].items():
    assert digest == sha256(HERE / name), name

covered = set()
for recipe in specs["recipes"]:
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    covered.update(recipe["covered_obligation_ids"])
assert covered == {row["obligation_id"] for row in registry["obligations"]}

lean_source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
for pattern in (
    r"\b(?:sorry|admit|sorryAx)\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0420-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    module_dir = tmp / "Stage1_Instances" / "THM-M-0420"
    module_dir.mkdir(parents=True)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (module_dir / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    run(
        ["lake", "env", "lean", "-R", str(tmp), "-o", str(module_dir / "Statement.olean"),
         str(module_dir / "Statement.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    obligation_output = run(
        ["lake", "env", "lean", "-R", str(tmp), "-o", str(module_dir / "ObligationTree.olean"),
         str(module_dir / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", "-R", str(tmp), str(module_dir / "Proof.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )

assert "root_composition" in obligation_output
assert "everywhereUnramifiedAtFinitePrimes_iff_allPrimesOver" in proof_output
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert axiom in proof_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == [
    "M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4"
]
assert receipt["result"]["authoritative_root_closed"] is False
assert receipt["result"]["theorem_complete"] is False

print("ok: exact statement, conditional composition, and M0420-N1 proof kernel-elaborated")
print("ok: M0420-N1 reports only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, input hashes, recipe coverage, and clean pinned mathlib checks passed")
print("open: exact Hilbert class field root remains M3; construction and four property bodies are absent")
print("stale: frozen graph predates the proof phase and does not yet credit M0420-N1")
print("blocked: cold hermetic replay, complete TCB/provenance closure, and independent verification remain open")
