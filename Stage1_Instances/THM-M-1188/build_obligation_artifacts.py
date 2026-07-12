#!/usr/bin/env python3
"""Build the frozen THM-M-1188 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1188-OBLIGATION_TREE"
THEOREM = "THM-M-1188"


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("M1188-ROOT", "root", "critical", "Exact attained-boundary weak maximum principle on the frozen closed heat cylinder.", "Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget", 12),
    ("M1188-S-DOMAIN", "definition", "high", "Preserve positive finite dimension, nonempty bounded open U, positive T, and the exact cylinder.", "closedCylinder U T", 18),
    ("M1188-S-BOUNDARY", "definition", "critical", "Preserve initial plus lateral boundary and exclude the terminal interior face.", "parabolicBoundary U T", 20),
    ("M1188-S-REGULARITY", "definition", "critical", "Preserve continuity, C2 spatial, C1 temporal, and the pointwise heat-subsolution sign.", "HasClassicalHeatRegularity U T u / IsHeatSubsolution U T u", 24),
    ("M1188-S-FOUNDATION", "certificate", "high", "Freeze classical compactness, extrema, derivative, Laplacian, axiom, and TCB boundaries.", "foundation and transitive trust profile", 16),
    ("M1188-C-COMPACT", "construction", "critical", "Prove the closed cylinder and parabolic boundary are compact and the boundary is nonempty.", "planned compactness and nonemptiness package", 45),
    ("M1188-L-ATTAIN", "core_lemma", "critical", "Use continuity on the compact cylinder and boundary to obtain attained maxima.", "planned IsCompact.exists_isMaxOn bridge", 35),
    ("M1188-C-PERTURB", "construction", "critical", "For epsilon > 0 form v(x,t)=u(x,t)-epsilon*t and derive the strict heat inequality.", "planned strict perturbation package", 40),
    ("M1188-L-SPATIAL", "core_lemma", "critical", "At a positive-time cylinder maximum with x in U, prove the spatial Laplacian is nonpositive.", "planned local spatial maximum/Laplacian lemma", 70),
    ("M1188-L-TEMPORAL", "core_lemma", "critical", "At a maximum over earlier times, including t=T, prove the one-sided temporal derivative is nonnegative.", "planned temporal endpoint derivative lemma", 65),
    ("M1188-B-INTERIOR", "branch", "critical", "Combine strict inequality and derivative signs to exclude a perturbed maximum at x in U and t>0.", "planned interior contradiction", 42),
    ("M1188-N-BOUNDARY", "normalization", "critical", "Show every cylinder maximizer not in the positive-time spatial interior lies on the frozen parabolic boundary.", "planned set-theoretic boundary identification", 38),
    ("M1188-L-EPSILON", "core_lemma", "critical", "Remove epsilon after boundary domination for u-epsilon*t, without changing the attained-witness conclusion.", "planned epsilon-limit and compact boundary extraction", 75),
    ("M1188-T-ENGINE", "terminal", "critical", "Assemble compactness, extrema, perturbation, derivative signs, boundary identification, and epsilon removal.", "AnalyticMaximumEngine", 30),
    ("M1188-T-ASSEMBLE", "transport", "high", "Consume the analytic engine and yield the exact canonical root with identical binder order.", "root_compose", 10),
    ("M1188-X-SOURCE", "terminal", "high", "Map every analytic node to exact source pages, assumptions, sign conventions, and errata.", "node-specific human source record", 28),
    ("M1188-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imported anchors, axioms, compiled dependencies, and replay evidence.", "machine provenance and trust record", 24),
]

checked = {"M1188-S-DOMAIN", "M1188-S-BOUNDARY", "M1188-S-REGULARITY", "M1188-T-ASSEMBLE"}
source_na = {"M1188-S-FOUNDATION", "M1188-X-PROVENANCE"}
machine_special = {"M1188-X-SOURCE": "not_applicable", "M1188-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, budget in rows:
    machine = machine_special.get(oid, "required")
    fingerprint = ("lean-expression-sha256:0564abe47c982ec2eea57b707d8e761b8f00999b3d35fc307f18e406c163ffd8"
                   if oid == "M1188-ROOT" else "planned:v1:sha256:" + sha([oid, claim, target]))
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": oid not in {"M1188-X-SOURCE", "M1188-X-PROVENANCE"},
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1188/ObligationTree.lean#root_compose" if oid == "M1188-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M1188-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": claim,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid in {"M1188-ROOT", "M1188-S-FOUNDATION", "M1188-X-PROVENANCE"} else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "SRC-M1188-NODE-MAP-OPEN" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1188-T-ASSEMBLE" else "none",
        "foundation_profile": "Lean classical real finite-dimensional analysis; release axiom audit open",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none; no numerical or oracle evidence is eligible", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["exact incoming proof_requires children where present"], "inference": claim, "output": claim, "outgoing_use": "only the declared typed parent or support edge"},
        "public_readable_target": f"Stage1_Instances/THM-M-1188/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no analytic premise or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-1188-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1188/ObligationTree.lean"] if oid == "M1188-T-ASSEMBLE" else [],
        "owner": "THM-M-1188 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain", "anchor provenance"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = sha([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated heat-cylinder statement and bounded anchor audit; epsilon-perturbation maximum-principle architecture; eligibility fixed before proof closure is observed.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1188-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1188-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_interface_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no maximum-principle proof, source acceptance, audit completion, or theorem completion.",
}


def make_edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1188-ROOT": ["M1188-T-ASSEMBLE"],
    "M1188-T-ASSEMBLE": ["M1188-T-ENGINE"],
    "M1188-T-ENGINE": ["M1188-C-COMPACT", "M1188-L-ATTAIN", "M1188-C-PERTURB", "M1188-B-INTERIOR", "M1188-N-BOUNDARY", "M1188-L-EPSILON"],
    "M1188-L-ATTAIN": ["M1188-C-COMPACT"],
    "M1188-B-INTERIOR": ["M1188-C-PERTURB", "M1188-L-SPATIAL", "M1188-L-TEMPORAL"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([make_edge(req, parent, "proof_requires", child, comp), make_edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [make_edge("REF-DOMAIN", "M1188-ROOT", "logical_decomposition", "M1188-S-DOMAIN"), make_edge("REF-BOUNDARY", "M1188-ROOT", "logical_decomposition", "M1188-S-BOUNDARY"), make_edge("REF-REG", "M1188-ROOT", "logical_decomposition", "M1188-S-REGULARITY"), make_edge("REF-FOUND", "M1188-ROOT", "logical_decomposition", "M1188-S-FOUNDATION")],
    "provenance": [make_edge("SRC-ANALYTIC", "M1188-X-SOURCE", "source_map", "M1188-T-ENGINE"), make_edge("PROV-ROOT", "M1188-X-PROVENANCE", "provenance_of", "M1188-ROOT")],
    "evidence": [make_edge("EVID-ASSEMBLE", "M1188-X-PROVENANCE", "evidence_for", "M1188-T-ASSEMBLE")],
    "trust": [make_edge("TRUST-FOUND", "M1188-ROOT", "trusts", "M1188-S-FOUNDATION"), make_edge("TRUST-PROV", "M1188-ROOT", "trusts", "M1188-X-PROVENANCE")],
    "documentation": [make_edge("DOC-ENGINE", "M1188-X-SOURCE", "documents", "M1188-T-ENGINE"), make_edge("DOC-BOUNDARY", "M1188-S-BOUNDARY", "documents", "M1188-ROOT")],
    "workflow": [make_edge("FLOW-COMPACT", "M1188-L-ATTAIN", "workflow_depends_on", "M1188-C-COMPACT"), make_edge("FLOW-INTERIOR", "M1188-B-INTERIOR", "workflow_depends_on", "M1188-C-PERTURB"), make_edge("FLOW-ENGINE", "M1188-T-ENGINE", "workflow_depends_on", "M1188-B-INTERIOR"), make_edge("FLOW-ASSEMBLE", "M1188-T-ASSEMBLE", "workflow_depends_on", "M1188-T-ENGINE"), make_edge("FLOW-PROV", "M1188-X-PROVENANCE", "workflow_depends_on", "M1188-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    outgoing, incoming = {oid: [] for oid in ids}, {oid: [] for oid in ids}
    for item in edges:
        outgoing[item["from"]].append(item["edge_id"])
        incoming[item["to"]].append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1188-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1188-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "checked_interfaces": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1188-C-COMPACT", "M1188-L-ATTAIN", "M1188-C-PERTURB", "M1188-L-SPATIAL", "M1188-L-TEMPORAL", "M1188-B-INTERIOR", "M1188-N-BOUNDARY", "M1188-L-EPSILON"], "composition_certificates": ["Stage1Instances.THM_M_1188.ObligationTree.root_compose"], "reason": "The exact composition is conditional; AnalyticMaximumEngine has no proof body."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1188/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid]})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {denominator}")
