#!/usr/bin/env python3
"""Fail-closed structural checks for the frozen THM-M-1119 architecture."""

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
ids = reg["frozen_denominators"]["inventory"]
assert len(ids) == len(set(ids)) == 15
assert set(ids) == {n["obligation_id"] for n in graphs["nodes"]}
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in graphs["nodes"]:
    assert required <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert not node["evidence_ids"]
for name in ("proof", "provenance", "trust", "documentation", "workflow"):
    assert graphs["graphs"][name]
proof = graphs["graphs"]["proof"]
assert {e["edge_type"] for e in proof} == {"proof_requires", "composes"}
premises = {e["source"] for e in proof if e["edge_type"] == "composes" and e["target"] == "M1119-T-COMPOSE"}
assert premises == {"M1119-T-SUBCRITICAL", "M1119-T-SUPERCRITICAL"}
text = (HERE / "ObligationTree.lean").read_text()
assert "sorry" not in text and "axiom " not in text and "le_antisymm supercritical subcritical" in text
subprocess.run(["python3", str(HERE / "build_obligation_artifacts.py")], check=True)
print("PASS: 15 frozen obligations, five typed graphs, <=100-step ledgers, and exact two-bound composition")
