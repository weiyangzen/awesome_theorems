#!/usr/bin/env python3
"""Build deterministic THM-M-0342 obligation and typed-graph artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0342-OBLIGATION_TREE"
THEOREM = "THM-M-0342"

rows = [
    ("M0342-ROOT", "root", "The exact frozen PlancherelTarget norm equality.", "critical"),
    ("M0342-S-ENCODING", "definition", "Preserve the finite-dimensional Euclidean domain, complex codomain, volume measure, exponent 2, and MemLp-to-Lp encoding.", "critical"),
    ("M0342-C-ANCHOR", "bridge", "Discharge the exact universal norm target using the pinned norm_fourier_eq declaration.", "critical"),
    ("M0342-N-PROJECTION", "projection", "Project norm preservation from the pinned L2 Fourier linear isometry equivalence.", "high"),
    ("M0342-I-ISOMETRY", "construction", "Construct the L2 Fourier linear isometry equivalence by extending the Schwartz-space Fourier equivalence.", "critical"),
    ("M0342-E-EXTEND", "bridge", "Verify the extendOfIsometry hypotheses and its agreement with the dense Schwartz embedding.", "critical"),
    ("M0342-D-DENSE-SOURCE", "density", "Establish dense range of the Schwartz-to-L2 map used as the extension source.", "high"),
    ("M0342-D-DENSE-TARGET", "density", "Establish dense range of the Schwartz-to-L2 map used as the extension target.", "high"),
    ("M0342-P-SCHWARTZ", "analytic_lemma", "Prove equality of L2 norms for the normalized Fourier transform on Schwartz functions.", "critical"),
    ("M0342-F-EQUIV", "construction", "Provide the Fourier linear equivalence on Schwartz space consumed by the extension.", "high"),
    ("M0342-T-ASSEMBLE", "transport", "Compose the exact norm-anchor interface into PlancherelTarget without changing binders or normalization.", "high"),
    ("M0342-X-SOURCE", "source_boundary", "Crosswalk the root, normalization, extension, density, and Schwartz identity to inspected primary sources.", "critical"),
    ("M0342-X-FOUNDATION", "certificate", "Audit the transitive axiom, classical-choice, quotient, computation, and Lean trust boundary.", "critical"),
    ("M0342-X-PROVENANCE", "certificate", "Record terminal proof-body provenance, dependency revisions, alias deduplication, and freshness.", "critical"),
    ("M0342-X-DOCUMENTATION", "documentation", "Produce a readable node-by-node reconstruction matching the frozen proof graph.", "high"),
]

machine_na = {"M0342-X-SOURCE", "M0342-X-DOCUMENTATION"}
informational = {"M0342-X-PROVENANCE"}
human_na = {"M0342-S-ENCODING", "M0342-X-FOUNDATION", "M0342-X-PROVENANCE"}
formal = {
    "M0342-ROOT": "Stage1Instances.THM_M_0342.PlancherelTarget",
    "M0342-C-ANCHOR": "Stage1Instances.THM_M_0342.ExactNormAnchor",
    "M0342-N-PROJECTION": "MeasureTheory.Lp.norm_fourier_eq",
    "M0342-I-ISOMETRY": "MeasureTheory.Lp.fourierTransform_l_i",
    "M0342-E-EXTEND": "LinearIsometryEquiv.extendOfIsometry",
    "M0342-D-DENSE-SOURCE": "SchwartzMap.denseRange_toLpCLM",
    "M0342-D-DENSE-TARGET": "SchwartzMap.denseRange_toLpCLM",
    "M0342-P-SCHWARTZ": "SchwartzMap.norm_fourier_toL2_eq",
    "M0342-F-EQUIV": "SchwartzMap.fourierEquiv",
    "M0342-T-ASSEMBLE": "Stage1Instances.THM_M_0342.root_of_exact_norm_anchor",
}

obligations = []
for oid, kind, text, risk in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest(),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "not_applicable" if oid in machine_na else ("informational" if oid in informational else "required"),
        "human_source_eligibility": "not_applicable" if oid in human_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_or_documentation_boundary_only" if oid in machine_na else ("release_overlay_no_proof_credit" if oid in informational else None),
        "terminal_proof_body_id": "pinned:mathlib@8a178386ffc0:Mathlib/Analysis/Fourier/LpSpace.lean#MeasureTheory.Lp.norm_fourier_eq" if oid == "M0342-N-PROJECTION" else ("local:ObligationTree.lean#root_of_exact_norm_anchor" if oid == "M0342-T-ASSEMBLE" else None),
    })

ids = [row[0] for row in rows]
denominator = hashlib.sha256(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated Plancherel norm target and pinned anchor inventory; the mathlib extension architecture was expanded before proof-phase closure credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": ids[0],
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": sorted(informational),
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_requires = [
    ("M0342-ROOT", "M0342-S-ENCODING"), ("M0342-ROOT", "M0342-C-ANCHOR"),
    ("M0342-ROOT", "M0342-T-ASSEMBLE"), ("M0342-C-ANCHOR", "M0342-N-PROJECTION"),
    ("M0342-N-PROJECTION", "M0342-I-ISOMETRY"), ("M0342-I-ISOMETRY", "M0342-E-EXTEND"),
    ("M0342-E-EXTEND", "M0342-D-DENSE-SOURCE"), ("M0342-E-EXTEND", "M0342-D-DENSE-TARGET"),
    ("M0342-E-EXTEND", "M0342-P-SCHWARTZ"), ("M0342-E-EXTEND", "M0342-F-EQUIV"),
    ("M0342-T-ASSEMBLE", "M0342-C-ANCHOR"),
]

def graph(name, triples):
    edges, outgoing, incoming = [], {oid: [] for oid in ids}, {oid: [] for oid in ids}
    for index, (source, target, edge_type) in enumerate(triples, 1):
        edge_id = f"{name.upper()}-{index:03d}"
        edge = {"edge_id": edge_id, "from": source, "to": target, "type": edge_type}
        edges.append(edge)
        outgoing[source].append(edge_id)
        incoming[target].append(edge_id)
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_triples = []
for parent, child in proof_requires:
    proof_triples.extend([(parent, child, "proof_requires"), (child, parent, "composes")])
proof_graph = graph("proof", proof_triples)
for index in range(0, len(proof_graph["edges"]), 2):
    forward, reverse = proof_graph["edges"][index:index + 2]
    forward["reciprocal_edge_id"] = reverse["edge_id"]
    reverse["reciprocal_edge_id"] = forward["edge_id"]

nodes = []
for oid, kind, text, _risk in rows:
    nodes.append({
        "node_id": f"THM-M-0342-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": text, "formal_target": formal.get(oid, "planned exact Lean interface"), "output": text,
        "human_debt": "H1", "machine_debt": "M2" if oid in {"M0342-ROOT", "M0342-C-ANCHOR", "M0342-N-PROJECTION", "M0342-T-ASSEMBLE"} else "M3",
        "readability_debt": "R3", "evidence_ids": [], "source_crosswalk_id": "node-specific-primary-source-map-pending",
        "provenance_id": "M0342-X-PROVENANCE", "foundation_profile": "lean4-mathlib-classical; transitive closure pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; independent trust review pending",
        "computation_record": "none; no native computation, oracle, or numerical experiment may close this node",
        "step_budget": 100,
        "semantic_step_ledger": {"premises": "Only the exact frozen context and declared proof-requires children.", "inference": text, "output": text, "outgoing_use": "Only declared typed edges may consume this output."},
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; no proof-phase closure is credited.",
        "owner": "THM-M-0342 proof lane", "reviewer": "independent Stage1 integration lane",
    })

support = {
    "refinement": [(parent, child, "refines_to") for parent, child in proof_requires],
    "provenance": [(oid, "M0342-X-PROVENANCE", "provenance_of") for oid in ids if oid != "M0342-X-PROVENANCE"],
    "evidence": [(oid, "M0342-X-PROVENANCE", "evidence_recorded_by") for oid in ids if oid != "M0342-X-PROVENANCE"],
    "trust": [(oid, "M0342-X-FOUNDATION", "trusts") for oid in ids if oid not in machine_na and oid != "M0342-X-FOUNDATION"],
    "documentation": [(oid, "M0342-X-DOCUMENTATION", "documented_by") for oid in ids if oid != "M0342-X-DOCUMENTATION"],
    "workflow": [("M0342-ROOT", oid, "workflow_depends_on") for oid in ("M0342-X-SOURCE", "M0342-X-FOUNDATION", "M0342-X-PROVENANCE", "M0342-X-DOCUMENTATION")],
    "source": [(oid, "M0342-X-SOURCE", "source_map") for oid in ids if oid not in human_na and oid != "M0342-X-SOURCE"],
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0342-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0342-ROOT", "edge_direction": "proof_requires/refines_to run parent to child; composes runs child to parent.",
    "nodes": nodes, "graphs": {"proof": proof_graph, **{name: graph(name, triples) for name, triples in support.items()}},
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M2", "theorem_complete": False, "open_cut_set": ["M0342-C-ANCHOR", "M0342-X-SOURCE", "M0342-X-FOUNDATION", "M0342-X-PROVENANCE", "M0342-X-DOCUMENTATION"]},
}
specs = {
    "schema_version": "stage1-node-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "required_checks": ["exact_type", "placeholder_hygiene", "provenance", "composition"]} for oid in ids],
}

for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
print(denominator)
