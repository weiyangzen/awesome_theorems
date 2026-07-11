#!/usr/bin/env python3
"""Fail-closed verifier for the THM-M-0390 validation handoff."""

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0390"


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


registry = json.loads((DOSSIER / "obligation-registry.json").read_text())
graphs = json.loads((DOSSIER / "typed-graphs.json").read_text())
units = json.loads((DOSSIER / "proof-units.json").read_text())

obligations = registry.get("obligations", registry.get("nodes", []))
registry_ids = {
    node.get("obligation_id", node.get("node_id")) for node in obligations
}
graph_nodes = graphs.get("nodes", {})
graph_ids = set(graph_nodes if isinstance(graph_nodes, dict) else graph_nodes)
if None in registry_ids or registry_ids != graph_ids:
    fail("frozen obligation registry and typed graph node sets disagree")

if units.get("theorem_complete") is not False or units.get("audit_complete") is not False:
    fail("open theorem or audit is overstated as complete")

root = next(
    (node for node in units.get("nodes", []) if node.get("node_id") == "THM-M-0390-ROOT"),
    None,
)
if root is None or root.get("machine_debt") not in {"M3", "M4", "M5"}:
    fail("root must remain explicitly machine-open")

proof = (DOSSIER / "Proof.lean").read_text()
probe = (DOSSIER / "Validation.lean").read_text()
prohibited = re.compile(r"\b(sorry|admit)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
if prohibited.search(proof) or prohibited.search(probe):
    fail("proof or validation probe contains a prohibited construct")
if "theorem solution_bases_coprime" not in proof:
    fail("implemented proof declaration is absent")
if "theorem independent_solution_bases_coprime" not in probe:
    fail("independent validation declaration is absent")

open_branches = {"BranchQEqTwo", "BranchQNeTwoPEqTwo", "BranchNeitherExponentTwo"}
if any(re.search(rf"^\s*theorem\s+{name}\b", proof, re.MULTILINE) for name in open_branches):
    fail("Proof.lean unexpectedly asserts a frozen open branch")

print(
    "validation: ok (14-node registry/graph identity, fail-closed root state, "
    "partial proof identity, independent probe, and placeholder policy verified)"
)
