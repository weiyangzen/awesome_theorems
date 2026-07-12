#!/usr/bin/env python3
"""Build the frozen THM-M-0984 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0984-OBLIGATION_TREE"
THEOREM = "THM-M-0984"

specs = [
    ("M0984-ROOT", "root", "Exact frozen Banach-valued strong-law target", "critical", "H1", "M3", 8),
    ("M0984-S-TARGET", "definition", "Preserve universes, measure, codomain, binders, and almost-everywhere conclusion", "critical", "H1", "M3", 20),
    ("M0984-H-INTEGRABLE", "hypothesis", "Require Bochner integrability of X 0", "high", "H1", "M3", 10),
    ("M0984-H-INDEPENDENT", "hypothesis", "Require pairwise IndepFun on the indexed sequence", "critical", "H1", "M3", 12),
    ("M0984-H-IDENTDIST", "hypothesis", "Require every X i identically distributed with X 0 under mu", "critical", "H1", "M3", 12),
    ("M0984-L-TERMINAL", "terminal", "Supply the exact strong-law implication and almost-everywhere limit", "critical", "H1", "M0-W", 100),
    ("M0984-T-COMPOSE", "composition", "Compose the terminal exact-type bridge into the frozen root", "critical", "H1", "M3", 8),
    ("M0984-X-SOURCE", "documentation", "Resolve Borel 1909 versus the modern Etemadi-strength target", "critical", "H1", "M5", 40),
    ("M0984-X-PROVENANCE", "provenance", "Verify the pinned terminal body, import closure, and deduplication", "critical", "H1", "M0-W", 30),
    ("M0984-X-TRUST", "trust", "Recheck axioms and exclude oracle, unsafe, and placeholder boundaries", "critical", "H1", "M0-W", 20),
]

rows = []
for oid, kind, statement, risk, h, m, budget in specs:
    overlay = kind in {"documentation", "provenance", "trust"}
    rows.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + hashlib.sha256(statement.encode()).hexdigest(),
        "kind": kind,
        "root_relevant": not overlay,
        "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "required" if kind != "trust" else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "non-proof assurance overlay" if overlay else None,
        "terminal_proof_body_id": "mathlib:ProbabilityTheory.strong_law_ae@8a178386" if oid == "M0984-L-TERMINAL" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable pinned-anchor audit; closure metrics were not accepted while choosing this denominator.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0984-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any statement, anchor, eligibility, split, merge, correction, or exclusion change requires registry v2 plus an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for (oid, kind, statement, risk, h, m, budget), row in zip(specs, rows):
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": statement,
        "formal_target": "Stage1Instances.THM_M_0984.ObligationTree.Root" if oid in {"M0984-ROOT", "M0984-L-TERMINAL", "M0984-T-COMPOSE"} else "typed architecture ledger: " + statement,
        "output": statement, "human_debt": h, "machine_debt": m, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "anchor-audit:human_source_status",
        "provenance_id": "mathlib:ProbabilityTheory.strong_law_ae@8a178386", 
        "foundation_profile": "lean4-mathlib-classical/5.6", "tcb_profile": "lean-4.29.0-pinned/transitive-validation-open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": [], "inference": "frozen architecture; no new proof closure credited", "output": statement, "outgoing_use": "typed graph edges"},
        "public_readable_target": f"Stage1_Instances/THM-M-0984/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture node only; proof and release credit remain gated.",
        "task_ids": [ITEM], "owned_sources": ["Stage1_Instances/THM-M-0984"],
        "owner": "Stage1 rev-5.6 execution lane", "reviewer": "independent integration-lane reviewer",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "anchor audit", "registry", "toolchain"], "revocation_state": "active"},
    })

def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT-COMPOSE", "M0984-ROOT", "M0984-T-COMPOSE"), ("COMPOSE-TERMINAL", "M0984-T-COMPOSE", "M0984-L-TERMINAL")]
proof_edges = []
for name, parent, child in proof_pairs:
    proof_edges += [
        {"edge_id": "REQ-" + name, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": "COMP-" + name},
        {"edge_id": "COMP-" + name, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": "REQ-" + name},
    ]
ref_edges = [{"edge_id": "REF-" + child, "from": "M0984-ROOT", "type": "logical_decomposition", "to": child}
             for child in ("M0984-S-TARGET", "M0984-H-INTEGRABLE", "M0984-H-INDEPENDENT", "M0984-H-IDENTDIST")]
graphs = {
    "proof": graph(proof_edges), "refinement": graph(ref_edges),
    "provenance": graph([{"edge_id": "PROV-TERMINAL", "from": "M0984-X-PROVENANCE", "type": "provenance_of", "to": "M0984-L-TERMINAL"}]),
    "evidence": graph([{"edge_id": "EVIDENCE-ROOT", "from": "M0984-X-PROVENANCE", "type": "evidence_for", "to": "M0984-ROOT"}]),
    "trust": graph([{"edge_id": "TRUST-ROOT", "from": "M0984-ROOT", "type": "trusts", "to": "M0984-X-TRUST"}]),
    "documentation": graph([{"edge_id": "DOC-SOURCE", "from": "M0984-X-SOURCE", "type": "documents", "to": "M0984-ROOT"}]),
    "workflow": graph([
        {"edge_id": "FLOW-PROOF", "from": "M0984-T-COMPOSE", "type": "workflow_depends_on", "to": "M0984-S-TARGET"},
        {"edge_id": "FLOW-PROVENANCE", "from": "M0984-X-PROVENANCE", "type": "workflow_depends_on", "to": "M0984-L-TERMINAL"},
        {"edge_id": "FLOW-TRUST", "from": "M0984-X-TRUST", "type": "workflow_depends_on", "to": "M0984-X-PROVENANCE"},
    ]),
}
bundle = {
    "schema_version": "stage1-typed-graph-bundle/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0984-L-TERMINAL"],
        "composition_certificates": ["Stage1Instances.THM_M_0984.ObligationTree.root_of_terminal"],
        "reason": "Exact child-to-parent composition is checked conditionally; the deep pinned terminal theorem remains uncredited until the proof phase. Source identity remains H1.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

lines = ["# THM-M-0984 frozen obligation tree", "", "The registry is frozen before proof-phase closure credit. Every semantic node has a stable ID, typed graph membership, and a step budget of at most 100.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"] + ".", "", f"Debt: `{node['human_debt']} / {node['machine_debt']} / {node['readability_debt']}`. Budget: {node['step_budget']} semantic steps. {node['status_boundary']}", ""]
lines += ["## Closure boundary", "", "`root_of_terminal` checks composition only. No obligation is marked closed here; the proof cut set is `M0984-L-TERMINAL`, and historical source identity remains independently open.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(rows)} obligations; denominator {denominator}")
