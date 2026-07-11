#!/usr/bin/env python3
"""Independent fail-closed validator for the THM-M-0391 partial proof receipt."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0391"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load(name: str) -> dict:
    with (OWNED / name).open(encoding="utf-8") as handle:
        return json.load(handle)


manifest = load("instance.json")
registry = load("obligation-registry.json")
nodes = load("obligation-nodes.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

if manifest.get("theorem_id") != "THM-M-0391":
    fail("instance theorem identity mismatch")
if manifest.get("canonical_formal_target", {}).get("declaration") != \
        "Stage1Instances.THMM0391.MihailescuTarget":
    fail("canonical target mismatch")
if manifest.get("theorem_complete") is not False:
    fail("open theorem is falsely marked complete")

obligation_ids = {item["obligation_id"] for item in registry["obligations"]}
node_ids = {item["obligation_id"] for item in nodes["nodes"]}
if obligation_ids != node_ids or len(obligation_ids) != 15:
    fail("registry/node identity mismatch")
if registry.get("root_obligation_id") != "M0391-ROOT":
    fail("root identity mismatch")
if set(proof_receipt.get("closed_obligation_ids", [])) != {"M0391-B-EE"}:
    fail("proof receipt claims an unexpected closure set")
if proof_receipt.get("result", {}).get("root_closed") is not False:
    fail("proof receipt falsely closes the root")

proof_edges = graphs.get("graphs", {}).get("proof", [])
adjacency = {item: [] for item in obligation_ids}
for edge in proof_edges:
    if edge["from"] not in obligation_ids or edge["to"] not in obligation_ids:
        fail("proof graph edge escapes the obligation registry")
    adjacency[edge["from"]].append(edge["to"])

seen: set[str] = set()
active: set[str] = set()


def visit(node: str) -> None:
    if node in active:
        fail("proof graph contains a cycle")
    if node in seen:
        return
    active.add(node)
    for child in adjacency[node]:
        visit(child)
    active.remove(node)
    seen.add(node)


visit("M0391-ROOT")
if seen != obligation_ids:
    fail("proof root does not reach every registered obligation")

expected_hashes = {
    "Statement.lean": "a8665695641932dcea97bab10143a73155e45c685fff03cfec6a19689b3f936f",
    "Proof.lean": "17723aea0ba702c2598c498797fef79b4c8056b65edb1ce952d53914cf8089b1",
    "obligation-registry.json": "c340453b27db47a49d59c81af6cfa88037cd3b8a4572f3fdf7df47425db7af1f",
    "typed-graphs.json": "3f7ae2e9cf98aa7ee05ccd0c8cadcc0f2b9c3aec9eb1ea64500f6bd5252d0b17",
}
for name, expected in expected_hashes.items():
    actual = digest(OWNED / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

toolchain_hash = digest(LEAN_ROOT / "lean-toolchain")
if toolchain_hash != "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    fail("Lean toolchain pin changed")
lake_manifest_hash = digest(LEAN_ROOT / "lake-manifest.json")
if lake_manifest_hash != "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    fail("Lake manifest changed")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    text = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        fail(f"prohibited placeholder/trust token in {name}")

commands = [
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0391/Proof.lean"],
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0391/Validation.lean"],
]
outputs = []
for command in commands:
    result = subprocess.run(command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    if result.returncode != 0:
        fail(f"recipe exited {result.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel report contains sorryAx: {' '.join(command)}")
    outputs.append(output)

if "[propext, Quot.sound]" not in outputs[0]:
    fail("proof axiom report differs from the accepted local profile")
if not all(name in outputs[1] for name in ("propext", "Classical.choice", "Quot.sound")):
    fail("independent probe axiom report is incomplete")

print("validation ok: exact partial proof re-elaborated; independent M0391-B-EE probe passed; root remains open")
