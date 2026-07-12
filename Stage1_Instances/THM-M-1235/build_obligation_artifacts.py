#!/usr/bin/env python3
"""Build THM-M-1235's frozen registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1235-OBLIGATION_TREE"
THEOREM = "THM-M-1235"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M1235-ROOT", "root", "critical", "The exact finite-horizon global existence and uniqueness target for Wolibner's source data.", "Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness", "The canonical proposition."),
    ("M1235-S-DEFINITIONS", "definition", "critical", "Expand SourceDomain, SourceData, Motion, and conditions (I)-(VIII) into native analytic predicates without adding existence or uniqueness.", "planned checked refinement of Stage1Instances.THMM1235.{SourceDomain,SourceData,Motion}", "A source-faithful native PDE interface and checked transport to the frozen encoding."),
    ("M1235-S-BOUNDARY", "terminal", "high", "Preserve bounded and exterior analytic-boundary regions, positive density, zero interior circulations, Holder data, source decay, and strictly positive finite T.", "planned boundary and mutation certificates for the native interface", "Checked domain, regularity, circulation, and time-boundary cases."),
    ("M1235-S-FOUNDATION", "certificate", "critical", "Freeze classical choice, function extensionality, quotient, axiom, TCB, and no-oracle policy for every terminal body.", "planned exact foundation and transitive axiom report", "Accepted trust boundary."),
    ("M1235-N-FINITE-HORIZON", "normalization", "high", "Show that construction for an arbitrary finite T > 0 expresses the source's indefinitely long forward motion claim, without silently assuming compatible infinite-time solutions.", "planned source-to-finite-horizon normalization theorem", "The exact arbitrary-finite-horizon quantifier used by the canonical root."),
    ("M1235-C-APPROXIMATION", "construction", "critical", "Construct Wolibner's successive approximate Lagrangian motions and prove their domain, initial-value, and boundary invariants.", "planned approximation sequence and invariant package", "A sequence of admissible approximate five-function motions."),
    ("M1235-L-VORTICITY", "core_lemma", "critical", "Establish transport of vorticity and circulation together with the uniform source decay and Holder estimates needed on every finite interval.", "planned vorticity-transport and a-priori-estimate package", "Uniform estimates and preservation laws for the approximants."),
    ("M1235-L-COMPACTNESS", "core_lemma", "critical", "Extract a convergent subsequence on the prescribed finite interval and justify passage to the limiting five functions.", "planned compactness and limit-passage package", "Limit coordinate, velocity, and pressure functions with the required convergence."),
    ("M1235-L-CONDITIONS", "core_lemma", "critical", "Prove that the limiting functions satisfy each of source conditions (I)-(VIII), including the classical Euler equations and continuous spatial derivatives.", "planned conditions-I-VIII verification package", "A value of Motion D T."),
    ("M1235-T-EXISTENCE", "terminal", "critical", "Compose approximation, estimates, compactness, and condition verification into existence for every admissible D and T.", "Stage1Instances.THMM1235.WolibnerExistencePackage", "Existence of a source Motion on every prescribed finite positive interval."),
    ("M1235-L-UNIQUENESS-ESTIMATE", "core_lemma", "critical", "Derive the source stability estimate for the difference of two motions with the same initial data and normalization.", "planned two-motion stability estimate", "A zero-forcing inequality for the difference of two motions."),
    ("M1235-T-UNIQUENESS", "terminal", "critical", "Conclude equality of all five functions for any two motions satisfying the source conditions.", "Stage1Instances.THMM1235.WolibnerUniquenessPackage", "SameMotion for every pair of admissible motions."),
    ("M1235-T-ASSEMBLE", "transport", "high", "Compose exact existence and uniqueness packages into the frozen canonical target.", "Stage1Instances.THMM1235.root_of_existence_and_uniqueness", "The exact canonical root conditional on both packages."),
    ("M1235-X-SOURCE", "terminal", "high", "Map every construction and analytic lemma to reviewed pages and numbered arguments in Wolibner (1933), including errata review.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M1235-X-PROVENANCE", "certificate", "critical", "Inventory all terminal proof bodies, imports, wrappers, axioms, TCB inputs, and replay evidence.", "planned machine-derived declaration and provenance closure", "Release provenance coverage without mathematical proof credit."),
]

checked = {"M1235-T-ASSEMBLE"}
source_na = {"M1235-S-DEFINITIONS", "M1235-S-BOUNDARY", "M1235-S-FOUNDATION", "M1235-X-PROVENANCE"}
machine_special = {"M1235-X-SOURCE": "not_applicable", "M1235-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = (
        "lean-expression-sha256:77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23"
        if oid == "M1235-ROOT"
        else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    )
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1235/ObligationTree.lean#root_of_existence_and_uniqueness" if oid == "M1235-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1235-" + oid.removeprefix("M1235-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": "H3" if oid != "M1235-X-SOURCE" else "H4",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1235-ROOT" else "M4"),
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "wolibner-1933-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1235-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M1235-C-APPROXIMATION", "M1235-L-VORTICITY", "M1235-L-COMPACTNESS", "M1235-L-CONDITIONS"} else 40,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires children and the formal context named in this node.",
            "inference": claim,
            "output": output,
            "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1235/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-1235-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1235/ObligationTree.lean"] if oid == "M1235-T-ASSEMBLE" else [],
        "owner": "THM-M-1235 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if oid in checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
            "revocation_state": "provisional" if oid in checked else "open",
        },
    })

registry_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in registry_fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated source statement and bounded anchor audit; source proof architecture recorded before machine closure discovery; eligibility is independent of available proof bodies.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1235-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1235-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version with an append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; no existence package, uniqueness package, H0 review, or theorem completion.",
}


def edge(edge_id, source, edge_type, target, reciprocal=None):
    result = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1235-ROOT": ["M1235-T-ASSEMBLE"],
    "M1235-T-ASSEMBLE": ["M1235-T-EXISTENCE", "M1235-T-UNIQUENESS"],
    "M1235-T-EXISTENCE": ["M1235-N-FINITE-HORIZON", "M1235-C-APPROXIMATION", "M1235-L-VORTICITY", "M1235-L-COMPACTNESS", "M1235-L-CONDITIONS"],
    "M1235-T-UNIQUENESS": ["M1235-L-UNIQUENESS-ESTIMATE"],
}
proof_edges = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof_edges.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof_edges,
    "refinement": [
        edge("REF-ROOT-DEFS", "M1235-ROOT", "logical_decomposition", "M1235-S-DEFINITIONS"),
        edge("REF-ROOT-BOUND", "M1235-ROOT", "logical_decomposition", "M1235-S-BOUNDARY"),
        edge("REF-ROOT-FOUND", "M1235-ROOT", "logical_decomposition", "M1235-S-FOUNDATION"),
    ],
    "provenance": [
        edge("SRC-EXISTENCE", "M1235-T-EXISTENCE", "source_map", "M1235-X-SOURCE"),
        edge("SRC-UNIQUENESS", "M1235-T-UNIQUENESS", "source_map", "M1235-X-SOURCE"),
        edge("PROV-ROOT", "M1235-X-PROVENANCE", "provenance_of", "M1235-ROOT"),
    ],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUND", "M1235-ROOT", "trusts", "M1235-S-FOUNDATION"),
        edge("TRUST-PROV", "M1235-ROOT", "trusts", "M1235-X-PROVENANCE"),
    ],
    "documentation": [
        edge("DOC-DEFS", "M1235-S-DEFINITIONS", "documents", "M1235-ROOT"),
        edge("DOC-SOURCE", "M1235-X-SOURCE", "documents", "M1235-T-EXISTENCE"),
        edge("DOC-SOURCE-UNIQUE", "M1235-X-SOURCE", "documents", "M1235-T-UNIQUENESS"),
    ],
    "workflow": [
        edge("FLOW-ASSEMBLE-EXISTENCE", "M1235-T-ASSEMBLE", "workflow_depends_on", "M1235-T-EXISTENCE"),
        edge("FLOW-ASSEMBLE-UNIQUENESS", "M1235-T-ASSEMBLE", "workflow_depends_on", "M1235-T-UNIQUENESS"),
        edge("FLOW-EXISTENCE-CONDITIONS", "M1235-T-EXISTENCE", "workflow_depends_on", "M1235-L-CONDITIONS"),
        edge("FLOW-CONDITIONS-COMPACTNESS", "M1235-L-CONDITIONS", "workflow_depends_on", "M1235-L-COMPACTNESS"),
        edge("FLOW-COMPACTNESS-ESTIMATES", "M1235-L-COMPACTNESS", "workflow_depends_on", "M1235-L-VORTICITY"),
        edge("FLOW-ESTIMATES-APPROX", "M1235-L-VORTICITY", "workflow_depends_on", "M1235-C-APPROXIMATION"),
        edge("FLOW-UNIQUE-ESTIMATE", "M1235-T-UNIQUENESS", "workflow_depends_on", "M1235-L-UNIQUENESS-ESTIMATE"),
        edge("FLOW-PROV-ASSEMBLE", "M1235-X-PROVENANCE", "workflow_depends_on", "M1235-T-ASSEMBLE"),
    ],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming = {}
    outgoing = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-1235-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M1235-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(checked),
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1235-T-EXISTENCE", "M1235-T-UNIQUENESS"],
        "composition_certificates": ["Stage1Instances.THMM1235.root_of_existence_and_uniqueness"],
        "reason": "The exact final composition is conditional; neither analytic package has a proof body.",
    },
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({
        "recipe_id": "VAL-" + oid,
        "obligation_id": oid,
        "command": "python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py",
        "expected_exit": 0,
        "network_policy": "denied",
    })

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
