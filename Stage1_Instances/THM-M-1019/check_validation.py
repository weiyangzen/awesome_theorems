#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1019-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1019"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
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
    if result.returncode:
        raise SystemExit(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
anchor = json.loads((HERE / "anchor-audit.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))

assert spec["item_id"] == "S56-M-1019-VALIDATION"
assert spec["theorem_id"] == "THM-M-1019"
assert spec["argv"] == ["python3", "Stage1_Instances/THM-M-1019/check_validation.py"]
assert spec["timeout_seconds"] == 120
assert spec["expected_exit"] == 0
assert spec["network_policy"] == "denied_by_recipe_no_network_operation"
assert set(spec["covered_obligation_ids"]) == set(registry["frozen_denominators"]["required_machine"])
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(HERE / "obligation-registry.json")
assert proof_receipt["inputs"]["typed_graphs_sha256"] == digest(HERE / "typed-graphs.json")
assert proof_receipt["inputs"]["anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert registry["root_obligation_id"] == "M1019-ROOT"
assert graphs["closure_boundary"]["theorem_complete"] is False

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text(encoding="utf-8")
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"
validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
assert "import Proof" not in validation_source
assert "proof-receipt" not in validation_source

assert digest(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "status", "--short"], cwd=mathlib) == ""
terminal = mathlib / anchor["candidates"][0]["source_path"]
assert digest(terminal) == anchor["candidates"][0]["source_file_sha256"]
assert prohibited.search(terminal.read_text(encoding="utf-8")) is None

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m1019-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=tmp,
        env=env,
    )
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["Proof.lean"] = run([lean, str(tmp / "Proof.lean")], cwd=tmp, env=env)
    outputs["Validation.lean"] = run([lean, str(tmp / "Validation.lean")], cwd=tmp, env=env)

for name, declaration in (
    ("Proof.lean", "characteristicFunctionUniqueness"),
    ("Validation.lean", "independentlyReconstructedRoot"),
):
    output = outputs[name]
    assert declaration in output and "depends on axioms:" in output
    observed = {axiom for axiom in EXPECTED_AXIOMS if axiom in output}
    assert observed == EXPECTED_AXIOMS, f"incomplete axiom report for {name}: {output}"
    assert "sorryAx" not in output

print("ok: exact proof root and independently reconstructed frozen root kernel-replayed")
print("ok: pinned clean mathlib provenance and observed classical axiom profile verified; no placeholders or unsafe declarations")
print("stale: frozen architecture graph remains open M1 pending master reconciliation")
print("blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner verification")
