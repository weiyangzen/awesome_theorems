#!/usr/bin/env python3
"""Independent fail-closed validator for THM-M-0152 partial validation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0152"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    with (OWNED / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


instance = load("instance.json")
statement = load("statement.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

if instance.get("theorem_id") != "THM-M-0152":
    fail("instance theorem identity mismatch")
if statement.get("canonical_formal_target", {}).get("declaration_or_expression") != \
        "Stage1Instances.THM_M_0152.TheoremaEgregiumTarget":
    fail("canonical target mismatch")
if instance.get("theorem_complete") is not False:
    fail("open theorem is falsely marked complete")

obligation_ids = {row["obligation_id"] for row in registry["obligations"]}
node_ids = {row["obligation_id"] for row in graphs["nodes"]}
if obligation_ids != node_ids or len(obligation_ids) != 17:
    fail("registry/graph identity mismatch")
if registry.get("root_obligation_id") != "M0152-ROOT":
    fail("root identity mismatch")
if set(proof_receipt.get("closed_obligation_ids", [])) != {"M0152-B-ORIENTATION"}:
    fail("proof receipt claims an unexpected closure set")
if proof_receipt.get("result", {}).get("root_closed") is not False:
    fail("proof receipt falsely closes the root")
if graphs.get("closure_boundary") != {
        "root_closed": False,
        "minimal_open_root_cut": ["M0152-L-INTRINSIC-FORMULA", "M0152-T-INVARIANCE"],
        "audit_complete": False,
        "theorem_complete": False,
}:
    fail("graph closure boundary changed")

proof_graph = graphs.get("graphs", {}).get("proof", {})
children: dict[str, list[str]] = {item: [] for item in obligation_ids}
for edge in proof_graph.get("edges", []):
    if edge["from"] not in obligation_ids or edge["to"] not in obligation_ids:
        fail("proof graph edge escapes the registry")
    if edge["type"] == "proof_requires":
        children[edge["from"]].append(edge["to"])

seen: set[str] = set()
active: set[str] = set()


def visit(node: str) -> None:
    if node in active:
        fail("proof graph contains a cycle")
    if node in seen:
        return
    active.add(node)
    for child in children[node]:
        visit(child)
    active.remove(node)
    seen.add(node)


visit("M0152-ROOT")
if "M0152-B-ORIENTATION" not in seen:
    fail("validated obligation is not root-relevant")

expected_hashes = {
    "Statement.lean": "411162ea683f92ccd9dae93e7c2a9b0cbfba3c15996da8be28e33980e143058d",
    "Proof.lean": "af4248cf6607df0b7c0ab05d97773f2b92f1950c4f1ec95a8d74a59e158c99e3",
    "obligation-registry.json": "c1c1588dc67d00af3d8a01236c23e8066e41080aef6521078c87be07a2663fd7",
    "typed-graphs.json": "864fcd7c62763bb03236d873634b116650f1c4359ef6eef492e8a1ecd1e34c2f",
    "proof-receipt.json": "47df55d7413717fa543001ec9bbab3ebe6e5b6ea265bcd7ea67f3f47da09e2bd",
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
    fail("Lake manifest changed")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith(("--", "/-", "*"))
    )
    if prohibited.search(code):
        fail(f"prohibited placeholder/trust token in {name}")

outputs = []
for source in ("Statement.lean", "Proof.lean", "Validation.lean"):
    command = ["lake", "env", "lean", f"../../Stage1_Instances/THM-M-0152/{source}"]
    result = subprocess.run(
        command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        fail(f"recipe exited {result.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel report contains sorryAx: {source}")
    outputs.append(output)

for output, label in zip(outputs[1:], ("proof", "independent probe")):
    if not all(name in output for name in ("propext", "Classical.choice", "Quot.sound")):
        fail(f"{label} axiom report differs from the recorded profile")

print("validation ok: statement and exact M0152-B-ORIENTATION proof re-elaborated; independent probe passed; root remains open")
