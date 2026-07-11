#!/usr/bin/env python3
"""Fail-closed validator for the THM-M-0394 partial validation handoff."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0394"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load(name: str) -> dict:
    with (OWNED / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

if registry.get("theorem_id") != "THM-M-0394":
    fail("registry theorem identity mismatch")
if registry.get("root_obligation_id") != "M0394-ROOT":
    fail("canonical root identity mismatch")

obligation_ids = {item["obligation_id"] for item in registry["obligations"]}
graph_ids = {item["obligation_id"] for item in graphs["nodes"]}
if obligation_ids != graph_ids or len(obligation_ids) != 17:
    fail("17-node frozen registry and typed graph identity mismatch")
if set(proof_receipt.get("closed_obligation_ids", [])) != {"M0394-S3", "M0394-B"}:
    fail("proof receipt claims an unexpected closure set")
result = proof_receipt.get("result", {})
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("partial proof receipt falsely closes the root")

nodes = {item["obligation_id"]: item for item in graphs["nodes"]}
root = nodes["M0394-ROOT"]
if root.get("machine_debt") not in {"M3", "M4", "M5"}:
    fail("root does not remain explicitly machine-open")
for open_id in ("M0394-N", "M0394-N1", "M0394-B1", "M0394-B2", "M0394-T"):
    if nodes[open_id].get("machine_debt") not in {"M3", "M4", "M5"}:
        fail(f"required open obligation {open_id} is overstated")

expected_hashes = {
    "Statement.lean": "7db337b7285aa5908d1504574e09bb3ba02d13bdada499da93f3d79035a27cc8",
    "ObligationTree.lean": "ce0f74f06cc67321aaee95997590dba92826b48daa7091617e30e94f119bb944",
    "Proof.lean": "1216a9cadcbcd2f661bac210a64e98283102d43880d622a441e85b468bf7968f",
    "obligation-registry.json": "62e1d333dc8d1537643609c6820d3f3c3d478b2d302c609f4bdb7f33b53f0378",
    "typed-graphs.json": "e2ec6dc22e909aee78b509f11ce5389ef1082f32bb97dac630085d464221a9d5",
    "proof-receipt.json": "25761626ee114363705bef54ef10a5914bd038117ca5e937674f4e62921e1967",
}
for name, expected in expected_hashes.items():
    actual = digest(OWNED / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

if digest(LEAN_ROOT / "lean-toolchain") != \
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    fail("Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != \
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    fail("Lake manifest pin changed")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith(("--", "/-", "*"))
    )
    if prohibited.search(code):
        fail(f"prohibited placeholder or trust declaration in {name}")

commands = [
    ["bash", "../../Stage1_Instances/THM-M-0394/check_proof.sh"],
    ["bash", "../../Stage1_Instances/THM-M-0394/check_validation_lean.sh"],
]
outputs = []
for command in commands:
    completed = subprocess.run(
        command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=120
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        fail(f"recipe exited {completed.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel report contains sorryAx: {' '.join(command)}")
    outputs.append(output)

required_axioms = ("propext", "Classical.choice", "Quot.sound")
if not all(name in outputs[0] for name in required_axioms):
    fail("proof axiom report is incomplete")
if not all(name in outputs[1] for name in required_axioms):
    fail("independent probe axiom report is incomplete")

print(
    "validation ok: frozen inputs and 17-node boundary verified; "
    "partial proof and independent probes elaborated; root remains open"
)
