#!/usr/bin/env python3
"""Generate the frozen THM-M-0528 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0528-OBLIGATION_TREE"
THEOREM = "THM-M-0528"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("M0528-ROOT", "root", "critical", "The exact general uniqueness-of-covering-lifts target frozen in Statement.lean.", "Stage1Instances.THM_M_0528.CoveringLiftUniquenessTarget", "Equality g1 = g2 for the two continuous lifts."),
    ("M0528-S-DEFINITIONS", "definition", "high", "Fix covering maps, continuous lifts, function composition, and equality conventions.", "the definitions used by CoveringLiftUniquenessTarget", "The exact canonical interface and notation."),
    ("M0528-S-DOMAIN", "normalization", "high", "Account for independent universes and topologies, PreconnectedSpace A, and the explicit witness a : A.", "the binder and typeclass context of CoveringLiftUniquenessTarget", "A nonempty-at-use preconnected domain with no extra separation hypothesis."),
    ("M0528-S-TRANSPORT", "transport", "high", "Transport pointwise equality of the projections to equality of composites and back.", "Stage1Instances.THM_M_0528.coveringLiftUniquenessTarget_iff_pointwiseProjectionEncoding", "A checked equivalence between the canonical and pointwise targets."),
    ("M0528-S-FOUNDATION", "certificate", "critical", "Inventory extensionality, classical choice, quotient soundness, imports, and the no-oracle policy.", "planned transitive axiom and trust report", "An accepted foundation and TCB boundary."),
    ("M0528-L-SEPARATED", "core_lemma", "critical", "Derive that a covering map is a separated map by separating distinct points in each discrete fiber.", "IsCoveringMap.isSeparatedMap", "IsSeparatedMap p."),
    ("M0528-L-LOCAL-INJECTIVE", "core_lemma", "high", "Derive local injectivity from the covering map's local-homeomorphism structure.", "IsCoveringMap.isLocalHomeomorph.isLocallyInjective", "IsLocallyInjective p."),
    ("M0528-L-PROPAGATE", "core_lemma", "critical", "Propagate equality from one point across a preconnected domain for continuous maps with equal composites.", "IsSeparatedMap.eq_of_comp_eq", "Equality of the two maps from separatedness and local injectivity."),
    ("M0528-X-ANCHOR", "bridge", "critical", "Apply the pinned Proposition 1.34 implementation to every binder of the exact pointwise target.", "IsCoveringMap.eq_of_comp_eq", "Stage1Instances.THM_M_0528.ExactPointwiseAnchor"),
    ("M0528-T-ASSEMBLE", "transport", "high", "Consume the exact pointwise anchor and transport it to the canonical composite-equality target.", "Stage1Instances.THM_M_0528.root_of_exactPointwiseAnchor", "Stage1Instances.THM_M_0528.CoveringLiftUniquenessTarget"),
    ("M0528-X-SOURCE", "terminal", "high", "Map the root and propagation argument to an exact reviewed Hatcher edition, proposition, page, assumptions, and errata record.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0528-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, placeholders, pins, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0528-S-DEFINITIONS", "M0528-S-DOMAIN", "M0528-S-TRANSPORT", "M0528-T-ASSEMBLE"}
source_na = {"M0528-S-DEFINITIONS", "M0528-S-DOMAIN", "M0528-S-TRANSPORT", "M0528-S-FOUNDATION", "M0528-X-PROVENANCE"}
machine_special = {"M0528-X-SOURCE": "not_applicable", "M0528-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0528-ROOT", "M0528-S-DEFINITIONS", "M0528-S-DOMAIN"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    body = None
    if oid == "M0528-X-ANCHOR":
        body = "mathlib:8a178386ffc0f5fef0b77738bb5449d50efeea95#IsCoveringMap.eq_of_comp_eq"
    if oid == "M0528-T-ASSEMBLE":
        body = "local:Stage1_Instances/THM-M-0528/ObligationTree.lean#root_of_exactPointwiseAnchor"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0528-" + oid.removeprefix("M0528-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0528-ROOT" else "M1" if oid == "M0528-X-ANCHOR" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "pinned-mathlib-anchor" if oid == "M0528-X-ANCHOR" else "local-conditional-composition" if oid == "M0528-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation, solver, native code, or oracle closes this topological claim",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0528/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no accepted root proof, source closure, or release result is supplied.",
        "task_ids": [ITEM, "S56-M-0528-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0528/ObligationTree.lean"] if body and oid == "M0528-T-ASSEMBLE" else [],
        "owner": "THM-M-0528 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; the covering-to-separated/local-injective propagation architecture was expanded before proof-phase closure was observed.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0528-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0528-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "anchor_classification": "M1", "root_machine_debt": "M3"},
    "status_boundary": "Scope, denominators, and conditional composition only; no proof-phase installation, H0, validation closure, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M0528-ROOT": ["M0528-T-ASSEMBLE"], "M0528-T-ASSEMBLE": ["M0528-X-ANCHOR"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0528-ROOT", "logical_decomposition", "M0528-S-DEFINITIONS"), edge("REF-ROOT-DOMAIN", "M0528-ROOT", "logical_decomposition", "M0528-S-DOMAIN"), edge("REF-ROOT-TRANSPORT", "M0528-ROOT", "logical_decomposition", "M0528-S-TRANSPORT"), edge("REF-ANCHOR-SEP", "M0528-X-ANCHOR", "logical_decomposition", "M0528-L-SEPARATED"), edge("REF-ANCHOR-INJ", "M0528-X-ANCHOR", "logical_decomposition", "M0528-L-LOCAL-INJECTIVE"), edge("REF-ANCHOR-PROP", "M0528-X-ANCHOR", "logical_decomposition", "M0528-L-PROPAGATE")],
    "provenance": [edge("SRC-ANCHOR", "M0528-X-ANCHOR", "source_map", "M0528-X-SOURCE"), edge("PROV-ANCHOR", "M0528-X-PROVENANCE", "provenance_of", "M0528-X-ANCHOR")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0528-ROOT", "trusts", "M0528-S-FOUNDATION"), edge("TRUST-PROV", "M0528-ROOT", "trusts", "M0528-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0528-S-DEFINITIONS", "documents", "M0528-ROOT"), edge("DOC-SOURCE", "M0528-X-SOURCE", "documents", "M0528-X-ANCHOR")],
    "workflow": [edge("FLOW-ASSEMBLE-ANCHOR", "M0528-T-ASSEMBLE", "workflow_depends_on", "M0528-X-ANCHOR"), edge("FLOW-PROV-ASSEMBLE", "M0528-X-PROVENANCE", "workflow_depends_on", "M0528-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0528-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0528-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0528-X-ANCHOR"], "composition_certificates": ["Stage1Instances.THM_M_0528.root_of_exactPointwiseAnchor"], "reason": "The composition is conditional; this phase does not install or accept the audited anchor as the canonical proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0528/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0528 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
