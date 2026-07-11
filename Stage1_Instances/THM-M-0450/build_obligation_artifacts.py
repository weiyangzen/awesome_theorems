#!/usr/bin/env python3
"""Freeze the canonical THM-M-0450 denominator and graph adjacency."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry_path = HERE / "obligation-registry.json"
graphs_path = HERE / "typed-graphs.json"
registry = json.loads(registry_path.read_text())
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True,
    separators=(",", ":")).encode()).hexdigest()
registry["denominator_sha256"] = digest
registry_path.write_text(json.dumps(registry, indent=2) + "\n")

if graphs_path.exists():
    graphs = json.loads(graphs_path.read_text())
    graphs["registry_denominator_sha256"] = digest
    for graph in graphs["graphs"].values():
        graph["out"] = {}
        graph["in"] = {}
        for edge in graph["edges"]:
            graph["out"].setdefault(edge["from"], []).append(edge["edge_id"])
            graph["in"].setdefault(edge["to"], []).append(edge["edge_id"])
    graphs_path.write_text(json.dumps(graphs, indent=2) + "\n")
print(digest)
