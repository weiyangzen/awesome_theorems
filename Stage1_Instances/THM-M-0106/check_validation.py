#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0106-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0106"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
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
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'(?:[^']*\.)?{re.escape(declaration)}' depends on axioms:\s*\[(?P<body>[^]]*)\]",
        output,
    )
    if not match:
        raise SystemExit(f"validation failed: missing axiom report for {declaration}")
    return {item.strip() for item in match.group("body").split(",") if item.strip()}


instance = json.loads((HERE / "instance.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert instance["theorem_id"] == statement["theorem_id"] == "THM-M-0106"
assert instance["canonical_formal_target"]["declaration_or_expression"] == (
    "Stage1Instances.THM_M_0106.NoetherNormalizationTarget"
)
assert instance["execution"]["theorem_complete"] is False
assert registry["root_obligation_id"] == "M0106-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["item_id"] == "S56-M-0106-PROOF"
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert set(proof_receipt["closed_obligation_ids"]) == {
    "M0106-L-FINITE", "M0106-L-SPEC", "M0106-T-ASSEMBLE", "M0106-ROOT"
}

source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
code = "\n".join(
    line for line in source.splitlines()
    if not line.lstrip().startswith(("--", "/-", "*"))
)
assert prohibited.search(code) is None
assert "noetherNormalization_proof" not in (HERE / "Validation.lean").read_text()

manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
assert next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib") == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0106-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    probe_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

proof_axioms = reported_axioms(proof_output, "noetherNormalization_proof")
probe_axioms = reported_axioms(
    probe_output, "noetherNormalization_independent_probe"
)
assert proof_axioms <= ALLOWED_AXIOMS and probe_axioms <= ALLOWED_AXIOMS
assert "sorryAx" not in proof_output + probe_output

print("PASS THM-M-0106 narrow validation")
print("kernel: exact proof and independently written exact-target probe elaborated")
print("trust: reported axioms are within propext, Classical.choice, Quot.sound")
print("provenance: proof receipt hashes, pinned clean mathlib revision, and registry identity agree")
print("hygiene: no local sorry/admit/axiom/unsafe token")
print("boundary: warm shared cache; hermetic cold replay and distinct-runner verification remain open")
