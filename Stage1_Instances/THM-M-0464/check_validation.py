#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-0464-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0464"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def run(argv: list[str], *, cwd: Path = ROOT, stdin: str | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, input=stdin, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode != 0:
        fail(f"recipe exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_record = json.loads((HERE / "proof.json").read_text(encoding="utf-8"))
if spec.get("item_id") != "S56-M-0464-VALIDATION":
    fail("validation specification item identity mismatch")
if registry.get("root_obligation_id") != "M0464-ROOT":
    fail("registry root identity mismatch")
if registry.get("denominator_sha256") != graphs.get("registry_denominator_sha256"):
    fail("registry and typed-graph denominator mismatch")
if registry.get("frozen_against_statement_sha256") != digest(HERE / "Statement.lean"):
    fail("registry is stale against Statement.lean")
if proof_record.get("proof_file_sha256") != digest(HERE / "Proof.lean"):
    fail("proof record is stale against Proof.lean")
if proof_record.get("root_closed") is not False or proof_record.get("root_machine_state") != "M3":
    fail("proof record does not preserve the open M3 root")

pins = {
    LEAN_ROOT / "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    LEAN_ROOT / "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
for path, expected in pins.items():
    if digest(path) != expected:
        fail(f"dependency pin changed: {path.name}")
if not MATHLIB.resolve().is_dir():
    fail("pinned mathlib checkout is missing")
if run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() != \
        "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    fail("mathlib revision differs from the pin")
if run(["git", "status", "--short"], cwd=MATHLIB):
    fail("mathlib checkout is dirty")

tree_output = run(["python3", str(HERE / "check_obligation_tree.py")])
if "root closure: open (M3)" not in tree_output:
    fail("obligation validator did not preserve the open M3 root")

block_comment = re.compile(r"/-.*?-/", re.DOTALL)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
for name in names:
    source = block_comment.sub("", (HERE / name).read_text(encoding="utf-8"))
    source = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
    if prohibited.search(source):
        fail(f"prohibited local token in {name}")

common = "import Mathlib\n" + (HERE / "Statement.lean").read_text(encoding="utf-8") + \
    (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
proof_output = run(
    ["lake", "env", "lean", "/dev/stdin"], cwd=LEAN_ROOT,
    stdin=common + (HERE / "Proof.lean").read_text(encoding="utf-8"),
)
validation_output = run(
    ["lake", "env", "lean", "/dev/stdin"], cwd=LEAN_ROOT,
    stdin=common + (HERE / "Validation.lean").read_text(encoding="utf-8"),
)
for declaration in (
    "countingConclusion_empty", "countingConclusion_of_semialgebraic_connected"
):
    if declaration not in proof_output:
        fail(f"missing proof axiom report for {declaration}")
for declaration in (
    "independent_countingConclusion_empty",
    "independent_countingConclusion_of_semialgebraic_connected",
):
    if declaration not in validation_output:
        fail(f"missing independent axiom report for {declaration}")
for label, output in (("proof", proof_output), ("independent validation", validation_output)):
    if "sorryAx" in output:
        fail(f"Lean reported sorryAx for {label}")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if axiom not in output:
            fail(f"{label} trust report omitted {axiom}")

root_body = re.compile(r"\b(?:theorem|def)\s+\w+[^\n]*:\s*PilaWilkieStatement")
if root_body.search((HERE / "Proof.lean").read_text(encoding="utf-8")):
    fail("Proof.lean unexpectedly asserts an unconditional PilaWilkieStatement root")

print("ok: frozen statement, conditional composition, and seven partial proof bodies re-elaborated")
print("ok: two boundary results independently reconstructed without importing or invoking Proof.lean")
print("ok: hashes, pins, clean mathlib, placeholders, trust output, and open graph passed")
print("blocked: general Pila-Wilkie root remains M3; cold hermetic and distinct-runner gates remain open")
