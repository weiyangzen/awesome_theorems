#!/usr/bin/env python3
"""Fail-closed node validation for S56-M-0417-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0417"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        fail(f"recipe exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


statement = load("statement.json")
registry = load("obligation-registry.json")
nodes = load("obligation-nodes.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")
spec = load("validation-spec.json")

if spec.get("item_id") != "S56-M-0417-VALIDATION":
    fail("validation specification item identity mismatch")
if (
    spec.get("theorem_id") != "THM-M-0417"
    or statement.get("theorem_id") != "THM-M-0417"
):
    fail("theorem identity mismatch")
if spec.get("network_policy") != "denied" or spec.get("expected_exit") != 0:
    fail("validation recipe is not a denied-network exit-zero recipe")
if registry.get("canonical_root") != "M0417-ROOT":
    fail("registry root mismatch")

registry_ids = {row["obligation_id"] for row in registry["obligations"]}
if set(spec.get("covered_obligation_ids", [])) != registry_ids:
    fail("validation specification does not cover the frozen denominator")
if {row["obligation_id"] for row in nodes["nodes"]} != registry_ids:
    fail("node registry differs from the frozen denominator")
if set(graphs["nodes"]) != registry_ids:
    fail("typed graph node set differs from the frozen denominator")

expected_inputs = {
    "Statement.lean": "fc5125d7afbcd9b11aa00f4f3bf2c55367faf662968bd223928f8f935ce756fe",
    "ObligationTree.lean": "cd0f4bdc3d1773145d1ab1e3cd23f111f00cd671bf7ba6bc3ffd2fad74812798",
    "Proof.lean": "19a759e2c5fcfd113585ce416eed7341ac55ab0aa2618b66da1587d4eb5a132b",
    "statement.json": "8a0bc1fb8fd159005cd2c5f6d308801daf7108e208ae483a34717b912d0f0c8c",
    "obligation-registry.json": "51e3afc110ee9f8c90264b54306979e6b6a56553bbeeb24fd506c2b71696eb56",
    "obligation-nodes.json": "f89fa1effdc64237d921402ab9affb5bab26effacc141ba6136d5efe4c914c42",
    "typed-graphs.json": "69095d48e63ae9dff0901ee41e4b0f77961da69348cbc734d10ad10443c284c4",
    "proof-receipt.json": "8fca2d81f7b332a94003366d57c81893025adddd3e1df6322ea18e4d77d28195",
}
for name, expected in expected_inputs.items():
    actual = digest(HERE / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

if statement["canonical_formal_target"]["statement_file_sha256"] != expected_inputs["Statement.lean"]:
    fail("statement record is stale against Statement.lean")
if proof_receipt["proof_body"]["wrapper_sha256"] != expected_inputs["Proof.lean"]:
    fail("proof receipt is stale against Proof.lean")
if proof_receipt["result"]["machine_root_closed"] is not True:
    fail("proof receipt does not claim provisional exact-root closure")
if proof_receipt["result"]["theorem_complete"] is not False:
    fail("proof receipt has an illegal completion claim")

source = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(
    r"\b(?:s" + r"orry|admit|sorryAx|native_decide)\b|"
    r"^[ \t]*(?:axiom|unsafe|external)\b",
    re.MULTILINE,
)
if prohibited.search(source):
    fail("local Lean source contains a placeholder, oracle, or unsafe declaration")

if digest(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
    fail("Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
    fail("Lake manifest changed")
if not MATHLIB.resolve().is_dir():
    fail("pinned mathlib checkout is missing")
if run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() != MATHLIB_REVISION:
    fail("mathlib revision differs from the manifest pin")
if run(["git", "status", "--short"], cwd=MATHLIB):
    fail("mathlib checkout is dirty")

terminal_source = MATHLIB / "Mathlib/MeasureTheory/Group/GeometryOfNumbers.lean"
if digest(terminal_source) != "262ce99e30915f9e41dc35e9ceb8f44ef6194316c9607b8387c19bcc65358d62":
    fail("terminal source digest changed")
terminal_text = terminal_source.read_text(encoding="utf-8")
start = terminal_text.find(
    "theorem exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure"
)
end = terminal_text.find("set_option backward.isDefEq.respectTransparency", start)
if start < 0 or end < 0:
    fail("terminal declaration boundary not found")
terminal_body = terminal_text[start:end]
if ":= by" not in terminal_body or prohibited.search(terminal_body):
    fail("terminal declaration is bodyless or contains a prohibited construct")

with tempfile.TemporaryDirectory(prefix="m0417-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    independent_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

axiom_report = re.compile(
    r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", re.MULTILINE
)
expected_axioms = {"propext", "Classical.choice", "Quot.sound"}
for declaration, output in (
    ("root_compose", obligation_output),
    ("minkowskiConvexBody", proof_output),
    ("closesFrozenStatementViaComposition", proof_output),
    ("independentMinkowskiConvexBody", independent_output),
):
    if declaration not in output or "depends on axioms" not in output:
        fail(f"missing axiom report for {declaration}")
    reports = {
        match.group(1): {
            name.strip() for name in match.group(2).split(",") if name.strip()
        }
        for match in axiom_report.finditer(output)
    }
    matching = [axioms for name, axioms in reports.items() if name.endswith(declaration)]
    if not matching:
        fail(f"could not parse the axiom report for {declaration}")
    if matching[-1] != expected_axioms:
        fail(
            f"unexpected axiom set for {declaration}: "
            f"expected {sorted(expected_axioms)}, got {sorted(matching[-1])}"
        )

print("PASS narrow kernel replay: exact root, composition, proof, and separate reconstruction elaborated")
print("PASS axiom observation: checked declarations report exactly the three recorded baseline axioms")
print("PASS local provenance: frozen hashes, clean pinned mathlib, toolchain, and terminal source agree")
print("OPEN source/trust boundaries: foundation approval, H0/R0 review, and transitive TCB closure are absent")
print("BLOCKED release gates: warm shared .lake and no distinct independently provisioned verifier")
