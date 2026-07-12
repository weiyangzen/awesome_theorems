#!/usr/bin/env python3
"""Build the frozen THM-M-0594 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0594-OBLIGATION_TREE"
THEOREM = "THM-M-0594"
PREFIX = "M0594"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact unrestricted finite-dimensional Whitney embedding target.", "Stage1Instances.THM_M_0594.WhitneyEmbeddingTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Fix smoothness, topological embedding, manifold derivative, Euclidean target, and all ordered typeclass assumptions.", "Stage1Instances.THM_M_0594.WhitneyEmbeddingTarget", "The elaborated statement interface."),
    ("S-BOUNDARY", "transport", "high", "Retain empty and zero-dimensional manifolds, boundarylessness, second countability, and the existential target dimension without adding compactness.", "Stage1Instances.THM_M_0594.whitneyEmbeddingTarget_iff_expanded", "Checked statement expansion and scope boundary."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotients, extensionality, manifold foundations, imports, and the transitive TCB.", "planned transitive axiom and trust report", "Accepted foundation and TCB profile."),
    ("N-EXHAUSTION", "normalization", "critical", "Derive the countable, locally finite atlas and compact exhaustion data needed for the noncompact construction from second countability.", "planned Lean compact-exhaustion/local-finiteness package", "Normalized exhaustion and atlas data."),
    ("N-DIMENSION", "normalization", "high", "Choose a finite Euclidean target dimension large enough for simultaneous differential and point separation, without claiming an unproved sharp bound.", "planned finite target-dimension selection", "A finite index type for the global coordinate family."),
    ("C-LOCAL", "construction", "critical", "Construct smooth bump-supported chart-coordinate functions and prove smoothness, support, and local spanning invariants.", "planned Lean subordinate bump/chart-coordinate construction", "A locally finite family of smooth coordinate functions."),
    ("L-DIFFERENTIAL", "core_lemma", "critical", "Select finitely many combinations whose differentials are pointwise injective on the whole manifold.", "planned global immersion/general-position package", "Pointwise injectivity of the manifold derivative."),
    ("L-POINT-SEPARATION", "core_lemma", "critical", "Select finitely many smooth coordinates that separate all distinct points, including points in different exhaustion layers.", "planned global point-separation package", "Injectivity of the constructed map."),
    ("L-PROPERNESS", "core_lemma", "critical", "Add and control an exhaustion coordinate so inverse images of compact sets are compact.", "planned smooth properness package", "Properness of the constructed map."),
    ("C-GLOBAL", "construction", "critical", "Assemble the selected coordinates into one finite-dimensional smooth map and transport the local invariants componentwise.", "planned Euclidean tuple assembly", "A smooth map with injective derivative, injectivity, and properness."),
    ("L-TOPOLOGICAL", "bridge", "critical", "Show that the constructed proper injective map into Euclidean space is a topological embedding under the frozen separation assumptions.", "planned proper-injective-to-IsEmbedding bridge", "IsEmbedding for the constructed map."),
    ("T-ASSEMBLE", "terminal", "high", "Package finite dimension, map, smoothness, topological embedding, and derivative injectivity into the exact root.", "Stage1Instances.THM_M_0594.root_of_smooth_embedding_witness", "The exact canonical target, conditional on the witness package."),
    ("X-COMPACT", "terminal", "normal", "Track the pinned compact specialization as a strict subtarget with a shared upstream proof body and no unrestricted-root credit.", "Stage1Instances.THM_M_0594.compactSpecialization_of_mathlib", "Compact-only anchor provenance."),
    ("X-SOURCE", "terminal", "high", "Map every construction and central lemma to pinpoint primary-source passages, assumptions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage only."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory wrappers, terminal bodies, imports, axioms, trust, and replay evidence without duplicating compact-anchor credit.", "planned machine-derived provenance closure", "Release provenance coverage only."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-X-COMPACT"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_expr = json.loads((HERE / "statement.json").read_text())["elaborated_expression_sha256"]

obligations = []
nodes = []
for suffix, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{suffix}"
    fp = (f"lean-expression-sha256:{statement_expr}" if suffix in {"ROOT", "S-DEFINITIONS"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0594/ObligationTree.lean#root_of_smooth_embedding_witness" if suffix == "T-ASSEMBLE" else
                                   "mathlib:exists_embedding_euclidean_of_compact@8a178386ffc0f5fef0b77738bb5449d50efeea95" if suffix == "X-COMPACT" else None),
    })
    nodes.append({
        "node_id": f"THM-M-0594-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R3" if suffix in {"ROOT", "X-SOURCE"} else "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": ("local-conditional-composition" if suffix == "T-ASSEMBLE" else "pinned-compact-specialization" if suffix == "X-COMPACT" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no solver, oracle, or numerical computation may close this node",
        "step_budget": 100 if suffix in {"N-EXHAUSTION", "C-LOCAL", "L-DIFFERENTIAL", "L-POINT-SEPARATION", "L-PROPERNESS"} else 40,
        "semantic_step_ledger": {"premises": "Only typed proof children and the exact frozen context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0594/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Architecture or conditional interface only; no unrestricted Whitney embedding proof is supplied.",
        "task_ids": [ITEM, "S56-M-0594-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0594/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else (["Stage1_Instances/THM-M-0594/AnchorAudit.lean"] if suffix == "X-COMPACT" else []),
        "owner": "THM-M-0594 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: o[k] for k in fields} for o in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact unrestricted statement and bounded anchor audit; standard weak-Whitney exhaustion, coordinate construction, separation, immersion, properness, and assembly architecture; eligibility assigned without using closure status.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_candidates.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; the unrestricted Whitney theorem remains open in this dossier."
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-C-GLOBAL", f"{PREFIX}-L-TOPOLOGICAL"],
    f"{PREFIX}-C-GLOBAL": [f"{PREFIX}-N-EXHAUSTION", f"{PREFIX}-N-DIMENSION", f"{PREFIX}-C-LOCAL", f"{PREFIX}-L-DIFFERENTIAL", f"{PREFIX}-L-POINT-SEPARATION", f"{PREFIX}-L-PROPERNESS"],
    f"{PREFIX}-L-DIFFERENTIAL": [f"{PREFIX}-C-LOCAL", f"{PREFIX}-N-DIMENSION"],
    f"{PREFIX}-L-POINT-SEPARATION": [f"{PREFIX}-N-EXHAUSTION", f"{PREFIX}-C-LOCAL"],
    f"{PREFIX}-L-PROPERNESS": [f"{PREFIX}-N-EXHAUSTION", f"{PREFIX}-C-LOCAL"],
    f"{PREFIX}-L-TOPOLOGICAL": [f"{PREFIX}-L-POINT-SEPARATION", f"{PREFIX}-L-PROPERNESS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-ROOT", f"{PREFIX}-ROOT", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT"), edge("PROV-COMPACT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-X-COMPACT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-ROOT")],
    "workflow": [edge("FLOW-ASSEMBLE-GLOBAL", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-C-GLOBAL"), edge("FLOW-ASSEMBLE-TOPO", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-L-TOPOLOGICAL"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0594-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-C-GLOBAL", f"{PREFIX}-L-TOPOLOGICAL"], "composition_certificates": ["Stage1Instances.THM_M_0594.root_of_smooth_embedding_witness"], "reason": "The checked constructor consumes a witness; all noncompact construction packages remain open."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in oids:
    recipes["recipes"].append({"recipe_id": f"VAL-{oid}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0594/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 60, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact PASS prefix and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
