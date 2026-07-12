#!/usr/bin/env python3
"""Generate the frozen THM-M-0663 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0663-OBLIGATION_TREE"
THEOREM = "THM-M-0663"

rows = [
    ("M0663-ROOT", "root", "The exact canonical o-minimal unary monotonicity proposition.", "critical", "required", "required"),
    ("M0663-S-ENCODING", "definition", "Audit o-minimality, parameter-definability, restricted graphs, topology, and partition encodings.", "critical", "required", "not_applicable"),
    ("M0663-N-DOMAIN", "normalization", "Normalize a definable partial unary function to the frozen total-function/restricted-domain interface.", "high", "required", "required"),
    ("M0663-B-DEGENERATE", "branch", "Discharge empty and singleton domains and prove the nondegenerate branch split exhaustive.", "normal", "required", "required"),
    ("M0663-C-EXCEPTIONAL", "construction", "Construct a finite definable exceptional set containing every change of local behavior and discontinuity.", "critical", "required", "required"),
    ("M0663-L-LOCAL-CONT", "core_lemma", "Prove continuity on each nonexceptional order-convex component.", "critical", "required", "required"),
    ("M0663-L-LOCAL-ORDER", "core_lemma", "Prove that each nonexceptional component is constant, strictly increasing, or strictly decreasing.", "critical", "required", "required"),
    ("M0663-L-FINITENESS", "core_lemma", "Use one-dimensional o-minimality to prove that exceptional points and complementary components are finite.", "critical", "required", "required"),
    ("M0663-T-PARTITION", "transport", "Turn the exceptional-set decomposition into a finite pairwise-disjoint Finset of order-convex subsets of A.", "high", "required", "required"),
    ("M0663-T-ASSEMBLE", "transport", "Attach continuity and behavior certificates to every piece and assemble the exact root witness.", "critical", "required", "required"),
    ("M0663-X-SOURCE", "source_boundary", "Pin the human monotonicity theorem and map every mathematical node to exact source hypotheses and steps.", "critical", "not_applicable", "required"),
    ("M0663-X-FOUNDATION", "certificate", "Audit classical logic, choice, topology, definability, imports, and the transitive trust boundary.", "critical", "required", "not_applicable"),
    ("M0663-X-PROVENANCE", "certificate", "Record terminal proof-body identities and reject wrappers, assumed fields, and placeholder-bearing candidates.", "critical", "informational", "not_applicable"),
    ("M0663-X-READABLE", "certificate", "Provide a source-aligned readable reconstruction with explicit local-to-global and branch ledgers.", "high", "not_applicable", "required"),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
obligations = []
for oid, kind, text, risk, machine, human in rows:
    fp = f"lean-source-sha256:{statement_hash}" if oid in {"M0663-ROOT", "M0663-S-ENCODING"} else "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()
    exclusion = None
    if oid == "M0663-X-SOURCE": exclusion = "human_source_boundary_only"
    if oid == "M0663-X-PROVENANCE": exclusion = "release_overlay_no_proof_credit"
    if oid == "M0663-X-READABLE": exclusion = "readable_boundary_only"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": None,
    })

denominator = hashlib.sha256(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [x[0] for x in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and completed bounded anchor audit; exceptional-set/local-to-global architecture selected without proof credit.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0663-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0663-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility, or edge change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

formal_targets = {
    "M0663-ROOT": "Stage1Instances.THM_M_0663.OMinimalMonotonicity",
    "M0663-S-ENCODING": "Stage1Instances.THM_M_0663.{IsOMinimal,restrictedGraph,HasMonotoneBehavior}",
    "M0663-B-DEGENERATE": "Stage1Instances.THM_M_0663.emptyDomainPartition",
    "M0663-T-ASSEMBLE": "Stage1Instances.THM_M_0663.root_of_partition_package",
}
nodes = []
for oid, kind, text, risk, machine, human in rows:
    provisional = oid in {"M0663-S-ENCODING", "M0663-B-DEGENERATE", "M0663-T-ASSEMBLE"}
    nodes.append({
        "node_id": f"THM-M-0663-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": text, "formal_target": formal_targets.get(oid, "planned exact Lean signature: " + oid),
        "output": text, "human_debt": "H3", "machine_debt": "M3" if provisional else "M4",
        "readability_debt": "R4", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending",
        "provenance_id": "local-conditional-interface" if oid == "M0663-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib/classical-and-choice-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation or oracle is eligible to close this node",
        "step_budget": 100 if risk == "critical" else 60,
        "semantic_step_ledger": {"premises": "Only typed proof-requires children and the frozen formal context.", "inference": text, "output": text, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0663/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; no unlisted premise or theorem closure is supplied.",
        "task_ids": [ITEM, "S56-M-0663-PROOF"], "owned_sources": [], "owner": "THM-M-0663 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if provisional else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if provisional else "open"},
    })

proof_pairs = [
    ("M0663-ROOT", "M0663-S-ENCODING"), ("M0663-ROOT", "M0663-N-DOMAIN"),
    ("M0663-ROOT", "M0663-T-ASSEMBLE"), ("M0663-ROOT", "M0663-X-FOUNDATION"),
    ("M0663-T-ASSEMBLE", "M0663-B-DEGENERATE"), ("M0663-T-ASSEMBLE", "M0663-T-PARTITION"),
    ("M0663-T-PARTITION", "M0663-C-EXCEPTIONAL"), ("M0663-T-PARTITION", "M0663-L-FINITENESS"),
    ("M0663-C-EXCEPTIONAL", "M0663-L-LOCAL-CONT"), ("M0663-C-EXCEPTIONAL", "M0663-L-LOCAL-ORDER"),
]

def graph(edges):
    out = {i: [] for i in ids}; inc = {i: [] for i in ids}
    for e in edges: out[e["from"]].append(e["edge_id"]); inc[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inc}

proof_edges = []
for n, (parent, child) in enumerate(proof_pairs, 1):
    a, b = f"P{n:02d}-REQ", f"P{n:02d}-COMP"
    proof_edges += [{"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b}, {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a}]

def star(prefix, typ, targets):
    return [{"edge_id": f"{prefix}{n:02d}", "type": typ, "from": x, "to": "M0663-ROOT"} for n, x in enumerate(targets, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"R{n:02d}", "type": "logical_decomposition", "from": p, "to": c} for n, (p, c) in enumerate(proof_pairs, 1)]),
    "provenance": graph(star("V", "provenance_of", ["M0663-X-PROVENANCE"])),
    "evidence": graph(star("E", "evidence_for", ["M0663-X-PROVENANCE"])),
    "trust": graph(star("U", "trusts", ["M0663-X-FOUNDATION"])),
    "documentation": graph(star("D", "documents", ["M0663-X-SOURCE", "M0663-X-READABLE"])),
    "workflow": graph([{"edge_id": "W01", "type": "workflow_depends_on", "from": "M0663-ROOT", "to": "M0663-X-PROVENANCE"}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0663-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0663-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0663-N-DOMAIN", "M0663-L-LOCAL-CONT", "M0663-L-LOCAL-ORDER", "M0663-L-FINITENESS", "M0663-X-SOURCE", "M0663-X-FOUNDATION"]},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in {"M0663-S-ENCODING", "M0663-B-DEGENERATE", "M0663-T-ASSEMBLE"} else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
