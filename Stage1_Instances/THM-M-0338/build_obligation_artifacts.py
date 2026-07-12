#!/usr/bin/env python3
"""Build deterministic THM-M-0338 obligation and graph artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0338-OBLIGATION_TREE"
THEOREM = "THM-M-0338"

rows = [
    ("M0338-ROOT", "root", "The exact KadisonSingerStatement.", "critical"),
    ("M0338-S-ENCODING", "definition", "Relate the custom State, purity, diagonal, and restriction encodings to the mathematical interfaces used below.", "critical"),
    ("M0338-C-COMPONENTS", "logical_decomposition", "Supply exact extension existence and at-most-one packages for every frozen input.", "critical"),
    ("M0338-E-EXTENSION", "bridge", "Extend every frozen pure diagonal state to a state on all bounded operators.", "high"),
    ("M0338-U-UNIQUE", "core_lemma", "Prove any two state extensions of the frozen pure diagonal state are equal.", "critical"),
    ("M0338-KS-PAVING", "equivalence", "Transport the unique-extension problem to the exact zero-diagonal operator paving formulation.", "critical"),
    ("M0338-P-WEAVER", "reduction", "Reduce the required paving bound to a precisely quantified Weaver KS2 discrepancy statement.", "critical"),
    ("M0338-W-MSS", "bridge", "Derive the Weaver partition from the finite-dimensional Marcus-Spielman-Srivastava theorem with constants tracked.", "critical"),
    ("M0338-M-MIXED", "core_lemma", "Establish the mixed characteristic polynomial expectation identity used by the MSS argument.", "critical"),
    ("M0338-M-INTERLACE", "core_lemma", "Build the interlacing family and select an outcome whose largest root is bounded by the averaged polynomial.", "critical"),
    ("M0338-M-REALROOT", "bridge", "Prove real stability and the barrier bound for the relevant mixed characteristic polynomial.", "critical"),
    ("M0338-F-FINITE", "transport", "Transfer finite matrix/vector discrepancy and paving results to bounded operators on the Nat-indexed Hilbert basis.", "critical"),
    ("M0338-T-ASSEMBLE", "transport", "Assemble existence and uniqueness into ExistsUnique at the exact root type.", "high"),
    ("M0338-X-SOURCE", "source_boundary", "Crosswalk every mathematical reduction and constant to reviewed primary sources.", "critical"),
    ("M0338-X-FOUNDATION", "certificate", "Audit classical choice, analytic dependencies, axioms, and the transitive Lean trust boundary.", "critical"),
    ("M0338-X-PROVENANCE", "certificate", "Record terminal proof-body provenance, alias deduplication, and evidence freshness.", "critical"),
]

machine_na = {"M0338-X-SOURCE"}
informational = {"M0338-X-PROVENANCE"}
human_na = {"M0338-S-ENCODING", "M0338-X-FOUNDATION", "M0338-X-PROVENANCE"}
formal = {
    "M0338-ROOT": "Stage1.THM_M_0338.KadisonSingerStatement",
    "M0338-C-COMPONENTS": "Stage1.THM_M_0338.KadisonSingerComponents",
    "M0338-E-EXTENSION": "Stage1.THM_M_0338.ExtensionExists",
    "M0338-U-UNIQUE": "Stage1.THM_M_0338.ExtensionAtMostOne",
    "M0338-T-ASSEMBLE": "Stage1.THM_M_0338.root_of_components",
}

obligations = []
for oid, kind, text, risk in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest(),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": "not_applicable" if oid in machine_na else ("informational" if oid in informational else "required"),
        "human_source_eligibility": "not_applicable" if oid in human_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid in machine_na else ("release_overlay_no_proof_credit" if oid in informational else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0338/ObligationTree.lean#root_of_components" if oid == "M0338-T-ASSEMBLE" else None,
    })

denominator = hashlib.sha256(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r[0] for r in rows]
reg = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated unique-extension statement and bounded negative anchor audit; KS/paving/Weaver/MSS architecture selected before proof closure observation.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": ids[0], "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": sorted(informational),
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_requires = [
    ("M0338-ROOT", "M0338-S-ENCODING"), ("M0338-ROOT", "M0338-C-COMPONENTS"), ("M0338-ROOT", "M0338-T-ASSEMBLE"),
    ("M0338-C-COMPONENTS", "M0338-E-EXTENSION"), ("M0338-C-COMPONENTS", "M0338-U-UNIQUE"),
    ("M0338-U-UNIQUE", "M0338-KS-PAVING"), ("M0338-KS-PAVING", "M0338-P-WEAVER"),
    ("M0338-P-WEAVER", "M0338-W-MSS"), ("M0338-W-MSS", "M0338-M-MIXED"),
    ("M0338-W-MSS", "M0338-M-INTERLACE"), ("M0338-W-MSS", "M0338-M-REALROOT"),
    ("M0338-P-WEAVER", "M0338-F-FINITE"), ("M0338-T-ASSEMBLE", "M0338-C-COMPONENTS"),
]

def graph(name, triples):
    edges, out, inc = [], {x: [] for x in ids}, {x: [] for x in ids}
    for i, (a, b, typ) in enumerate(triples, 1):
        eid = f"{name.upper()}-{i:03d}"
        e = {"edge_id": eid, "from": a, "to": b, "type": typ}
        edges.append(e); out[a].append(eid); inc[b].append(eid)
    return {"edges": edges, "out": out, "in": inc}

proof_triples = []
for i, (a, b) in enumerate(proof_requires, 1):
    proof_triples += [(a, b, "proof_requires"), (b, a, "composes")]
proof_graph = graph("proof", proof_triples)
for i in range(0, len(proof_graph["edges"]), 2):
    x, y = proof_graph["edges"][i:i+2]
    x["reciprocal_edge_id"] = y["edge_id"]; y["reciprocal_edge_id"] = x["edge_id"]

nodes = []
for oid, kind, text, _ in rows:
    nodes.append({
        "node_id": f"THM-M-0338-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": text, "formal_target": formal.get(oid, "planned exact Lean interface"), "output": text,
        "human_debt": "H1", "machine_debt": "M3" if oid in {"M0338-ROOT", "M0338-T-ASSEMBLE"} else "M4", "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending", "provenance_id": "none",
        "foundation_profile": "lean4-mathlib-classical/transitive-analytic-closure-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no oracle or numerical experiment may close this node",
        "step_budget": 100, "semantic_step_ledger": {"premises": "Only declared proof-requires children and the exact frozen context.", "inference": text, "output": text, "outgoing_use": "Only declared typed edges may consume this output."},
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; no proof closure is supplied.",
        "owner": "THM-M-0338 proof lane", "reviewer": "independent Stage1 integration lane",
    })

support = {
    "provenance": [(oid, "M0338-X-PROVENANCE", "provenance_of") for oid in ids if oid != "M0338-X-PROVENANCE"],
    "workflow": [("M0338-ROOT", oid, "workflow_depends_on") for oid in ("M0338-X-SOURCE", "M0338-X-FOUNDATION", "M0338-X-PROVENANCE")],
    "source": [(oid, "M0338-X-SOURCE", "source_map") for oid in ids if oid not in human_na and oid != "M0338-X-SOURCE"],
    "trust": [(oid, "M0338-X-FOUNDATION", "trusts") for oid in ids if oid not in machine_na and oid != "M0338-X-FOUNDATION"],
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0338-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0338-ROOT", "edge_direction": "proof_requires runs parent to child; composes runs child to parent.",
    "nodes": nodes, "graphs": {"proof": proof_graph, **{k: graph(k, v) for k, v in support.items()}},
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "open_cut_set": ["M0338-E-EXTENSION", "M0338-KS-PAVING", "M0338-W-MSS", "M0338-X-SOURCE", "M0338-X-FOUNDATION"]},
}
specs = {"schema_version": "stage1-node-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
         "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "required_checks": ["exact_type", "placeholder_hygiene", "provenance", "composition"]} for oid in ids]}

for name, obj in (("obligation-registry.json", reg), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")
print(denominator)
