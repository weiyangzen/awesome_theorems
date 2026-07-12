#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1091-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-1091-VALIDATION"
assert spec["theorem_id"] == "THM-M-1091"
assert receipt["item_id"] == spec["item_id"]
assert receipt["theorem_id"] == spec["theorem_id"]
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["result"]["theorem_complete"] is False
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert digest(HERE / "validation-phase-spec.json") == receipt["validation_spec_sha256"]
assert digest(HERE / "check_validation.py") == receipt["validator_sha256"]

recipe = spec["recipes"][0]
assert isinstance(recipe["argv"], list)
assert recipe["network_policy"] == "denied"
assert recipe["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""
terminal_source = mathlib / "Mathlib" / "Probability" / "Kernel" / "Composition" / "Comp.lean"
assert digest(terminal_source) == receipt["provenance"]["terminal_source_sha256"]
terminal_text = re.sub(r"/-.*?-/", "", terminal_source.read_text(), flags=re.DOTALL)
terminal_text = re.sub(r"--.*$", "", terminal_text, flags=re.MULTILINE)
assert prohibited.search(terminal_text) is None

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
env = os.environ.copy()
env.update({
    "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
})
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m1091-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), "Statement.lean"],
        cwd=tmp,
        env=env,
    )
    outputs["ObligationTree.lean"] = run(
        [lean, "-o", str(tmp / "ObligationTree.olean"), "ObligationTree.lean"],
        cwd=tmp,
        env=env,
    )
    outputs["Proof.lean"] = run([lean, "Proof.lean"], cwd=tmp, env=env)
    outputs["Validation.lean"] = run(
        [lean, "Validation.lean"], cwd=tmp, env=env
    )

for name, declaration in (
    ("Proof.lean", "chapmanKolmogorov"),
    ("Proof.lean", "chapmanKolmogorov_integral"),
    ("Validation.lean", "independentChapmanKolmogorov"),
):
    normalized = " ".join(outputs[name].split())
    report = re.search(
        rf"'[^']*\.{re.escape(declaration)}' depends on axioms: \[(.*?)\]", normalized
    )
    assert report, f"missing axiom report for {declaration}"
    observed = {axiom for axiom in EXPECTED_AXIOMS if axiom in report.group(1)}
    assert observed == EXPECTED_AXIOMS, f"unexpected axiom profile for {declaration}: {report.group(0)}"
    assert "sorryAx" not in report.group(0)

assert receipt["result"]["frozen_graph_state"] == "stale_pre_proof_open_root_pending_master_reconciliation"
print("PASS THM-M-1091 validation: exact statement, composition, proof roots, and independent root kernel-replayed")
print("PASS trust: checked roots report only propext, Classical.choice, and Quot.sound")
print("PASS provenance: frozen local hashes and clean pinned mathlib source revision agree")
print("BLOCKED release gates: graph freshness, cold empty-cache hermetic replay, and distinct-runner verification")
