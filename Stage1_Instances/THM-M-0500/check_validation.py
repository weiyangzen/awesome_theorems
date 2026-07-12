#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0500-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0500"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
PRIMES_IN_AP_SOURCE_SHA256 = "d99edfb234cc2c044332951a16f32bbfad58c8c73cc51faf4e9219d3bc6684c2"
PRIMES_IN_AP_OLEAN_SHA256 = "916d658fa456549d080825404851956dd4aa23fc21f666c7299fab9a2d91e085"
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
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


spec = json.loads((HERE / "validation-phase-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
receipt = json.loads((HERE / "validation-receipt.json").read_text(encoding="utf-8"))

assert spec["item_id"] == "S56-M-0500-VALIDATION"
assert spec["theorem_id"] == statement["theorem_id"] == "THM-M-0500"
assert spec["depends_on"] == ["S56-M-0500-PROOF"]
assert receipt["item_id"] == spec["item_id"]
assert receipt["theorem_id"] == spec["theorem_id"]
assert receipt["depends_on"] == spec["depends_on"]
assert receipt["base_revision"] == run(
    ["git", "rev-parse", "HEAD"], cwd=ROOT
).strip()
assert receipt["base_tree"] == run(
    ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT
).strip()
assert len(spec["recipes"]) == 1
recipe = spec["recipes"][0]
assert recipe["argv"] == [
    "python3",
    "Stage1_Instances/THM-M-0500/check_validation.py",
]
assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert isinstance(recipe["argv"], list) and recipe["timeout_seconds"] == 120

for name, expected in receipt["inputs"].items():
    path = LEAN_ROOT / name if name in {"lean-toolchain", "lake-manifest.json"} else HERE / name
    assert digest(path) == expected, f"stale validation receipt input: {name}"

statement_sha256 = digest(HERE / "Statement.lean")
assert statement["canonical_formal_target"]["statement_file_sha256"] == statement_sha256
assert registry["frozen_against_statement_sha256"] == statement_sha256
assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
inventory = {row["obligation_id"] for row in registry["obligations"]}
assert set(registry["frozen_denominators"]["inventory"]) == inventory
required_machine = set(registry["frozen_denominators"]["required_machine"])
assert set(proof_receipt["closed_obligation_ids"]) == required_machine
assert proof_receipt["statement_sha256"] == statement_sha256
assert proof_receipt["proof_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["obligation_tree_sha256"] == digest(HERE / "ObligationTree.lean")
assert proof_receipt["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["proof_body"]["terminal_declaration"] == (
    "Nat.infinite_setOf_prime_and_eq_mod"
)
assert proof_receipt["proof_body"]["terminal_source_sha256"] == (
    PRIMES_IN_AP_SOURCE_SHA256
)
assert proof_receipt["result"]["root_machine_proof_body_present"] is True
assert proof_receipt["result"]["theorem_complete"] is False
assert receipt["canonical_target"]["elaborated_expression_sha256"] == statement[
    "canonical_formal_target"
]["elaborated_expression_sha256"]
assert receipt["result"]["exact_root_kernel_closed_locally"] is True
assert receipt["result"]["distinct_terminal_proof_body_checked"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
    assert prohibited.search(source) is None, f"prohibited construct in {name}"

validation_source = code_without_comments(
    (HERE / "Validation.lean").read_text(encoding="utf-8")
)
assert re.search(r"^\s*import\s+(?:Proof|ObligationTree)\b", validation_source, re.MULTILINE) is None
assert "Nat.forall_exists_prime_gt_and_eq_mod" in validation_source
assert "dirichletPrimesInAPTarget_iff_unbounded.mpr" in validation_source

assert digest(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
assert digest(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
mathlib_record = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib_record["rev"] == MATHLIB_REVISION

env = os.environ.copy()
env.update(
    {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
)
lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
assert digest(lean) == LEAN_EXECUTABLE_SHA256
version = run([str(lean), "--version"], cwd=LEAN_ROOT, env=env)
assert "4.29.0" in version and LEAN_COMMIT in version

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--porcelain"], cwd=mathlib) == ""
terminal_source = mathlib / "Mathlib/NumberTheory/LSeries/PrimesInAP.lean"
terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/NumberTheory/LSeries/PrimesInAP.olean"
assert digest(terminal_source) == PRIMES_IN_AP_SOURCE_SHA256
assert digest(terminal_olean) == PRIMES_IN_AP_OLEAN_SHA256
terminal_text = code_without_comments(terminal_source.read_text(encoding="utf-8"))
for fragment in (
    "theorem infinite_setOf_prime_and_eq_mod (ha : IsUnit a)",
    "not_summable_residueClass_prime_div ha",
    "support_residueClass_prime_div a",
    "theorem forall_exists_prime_gt_and_eq_mod (ha : IsUnit a) (n : ℕ)",
    "infinite_setOf_prime_and_eq_mod ha",
):
    assert fragment in terminal_text, f"terminal source drifted: {fragment}"
assert prohibited.search(terminal_text) is None

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
base_module_env = env.copy()
base_module_env["LEAN_PATH"] = lean_path
with tempfile.TemporaryDirectory(prefix="m0500-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())

    statement_output = run(
        [str(lean), "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=tmp,
        env=base_module_env,
    )
    module_env = base_module_env.copy()
    module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        [str(lean), str(tmp / "ObligationTree.lean")], cwd=tmp, env=module_env
    )
    proof_output = run([str(lean), str(tmp / "Proof.lean")], cwd=tmp, env=module_env)
    validation_output = run(
        [str(lean), str(tmp / "Validation.lean")], cwd=tmp, env=module_env
    )

assert reported_axioms(
    statement_output,
    "Stage1Instances.THM_M_0500.dirichletPrimesInAPTarget_iff_unbounded",
) == EXPECTED_AXIOMS
for output, declaration in (
    (
        obligation_output,
        "Stage1Instances.THM_M_0500.ObligationTree.root_of_terminal_packages",
    ),
    (proof_output, "Nat.infinite_setOf_prime_and_eq_mod"),
    (proof_output, "Stage1Instances.THM_M_0500.dirichletPrimesInAP_proof"),
    (validation_output, "Nat.forall_exists_prime_gt_and_eq_mod"),
    (
        validation_output,
        "Stage1Instances.THM_M_0500.Validation.independentlyReconstructedDirichletPrimesInAP",
    ),
):
    assert reported_axioms(output, declaration) == EXPECTED_AXIOMS

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["minimal_open_root_cut"] == ["M0500-T-NONSUM", "M0500-L-SUPPORT"]

print("PASS S56-M-0500-VALIDATION: exact statement, composition, proof root, and differential root kernel-replayed")
print("PASS trust observation: checked declarations report exactly propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen hashes, clean mathlib pin/tree, and terminal source/olean agree")
print("STALE authoritative graph: pre-proof M3 root and open terminal cut await master reconciliation")
print("BLOCKED transitive trust/provenance: complete declaration closure and release TCB inventory are absent")
print("BLOCKED hermetic/independent gates: shared warm cache and same-worker probe are not cold or distinct-runner evidence")
