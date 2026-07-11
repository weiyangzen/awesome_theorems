#!/usr/bin/env python3
"""Fail-closed validation checks for S56-M-0087-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0087"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0087-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0087"
assert len(spec["recipes"]) == 2
assert len({r["recipe_id"] for r in spec["recipes"]}) == 2
assert all(isinstance(r["argv"], list) and r["argv"] for r in spec["recipes"])
assert all(r["network_policy"] == "denied_by_recipe_contract" for r in spec["recipes"])

for name, expected in receipt["inputs"].items():
    path = LEAN_ROOT / name if name in ("lean-toolchain", "lake-manifest.json") else HERE / name
    assert digest(path) == expected, f"stale validation input: {name}"

source = "\n".join((HERE / name).read_text() for name in (
    "Statement.lean", "ObligationTree.lean", "Proof.lean"
))
prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
assert prohibited.search(source) is None

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == receipt["provenance"]["mathlib_revision"]
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == receipt["provenance"]["mathlib_tree"]
assert run(["git", "status", "--porcelain"], cwd=mathlib) == ""

terminal_source = mathlib / receipt["provenance"]["terminal_source_path"]
terminal_olean = mathlib / receipt["provenance"]["terminal_olean_path"]
assert digest(terminal_source) == receipt["provenance"]["terminal_source_sha256"]
assert digest(terminal_olean) == receipt["provenance"]["terminal_olean_sha256"]
assert receipt["provenance"]["terminal_source_sha256"] == proof_receipt["proof_body"]["terminal_source_sha256"]
assert receipt["provenance"]["terminal_olean_sha256"] == proof_receipt["proof_body"]["terminal_olean_sha256"]

with tempfile.TemporaryDirectory(prefix="m0087-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env.update({"LEAN_PATH": f"{tmp}:{lean_path}", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    run(["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)

for declaration in (
    "Proof.fullPackage", "Proof.faithfulPackage", "Proof.adjunctionPackage",
    "Proof.finiteLimitsPackage", "Proof.gabrielPopescu_via_frozen_composition",
    "Proof.gabrielPopescu", "GabrielPopescuAux.kernel_ι_d_comp_d",
    "GabrielPopescuAux.exists_d_comp_eq_d", "GabrielPopescu.preservesInjectiveObjects",
):
    assert declaration in output
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert axiom in output

assert receipt["result"]["exact_root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["failed_gates"] == [
    "trust.accepted_foundation_and_transitive_tcb",
    "hermetic.cold_empty_cache_and_offline_restore",
    "independent.distinct_runner_and_minimal_verifier",
    "source.H0",
    "readability.R0",
    "master.acceptance",
]

print("PASS THM-M-0087 validation: exact root and frozen composition kernel-check")
print("PASS provenance: pinned clean mathlib source and olean hashes agree")
print("FAIL CLOSED release: trust, cold hermetic, and independent gates remain open")
