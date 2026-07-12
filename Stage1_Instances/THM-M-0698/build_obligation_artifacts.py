#!/usr/bin/env python3
"""Build the frozen THM-M-0698 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0698-OBLIGATION_TREE"
THEOREM = "THM-M-0698"


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0698-ROOT", "root", "critical", "The exact universe-polymorphic satisfiable iff finitely satisfiable target frozen in Statement.lean.", "Stage1Instances.THM_M_0698.FirstOrderCompactnessTarget", "The exact first-order compactness equivalence."),
    ("M0698-S-DEFINITIONS", "definition", "high", "Freeze Theory, ModelType, IsSatisfiable, and the Finset-subtheory definition of IsFinitelySatisfiable.", "FirstOrder.Language.Theory.{IsSatisfiable,IsFinitelySatisfiable}", "The exact semantic predicates used by the root."),
    ("M0698-S-UNIVERSES", "normalization", "high", "Track Language.{u,v}, the max u v model carrier, closed sentences, coercions from Finset to Theory, and implicit binder order.", "checked universe and coercion interface in Statement.lean", "No hidden countability, cardinality, or universe premise."),
    ("M0698-S-BOUNDARY", "branch", "normal", "Account for the empty theory, empty finite subtheory, finite theories, empty symbol families, and mathlib's nonempty model convention.", "planned exact boundary ledger for FirstOrderCompactnessTarget", "All degenerate cases remain inside the canonical quantifiers."),
    ("M0698-S-FOUNDATION", "certificate", "critical", "Fix the classical choice, quotient, propositional extensionality, ultrafilter, TCB, and no-oracle policy.", "planned transitive axiom and trust report", "An accepted foundation and trust boundary."),
    ("M0698-B-FORWARD", "branch", "normal", "Restrict any model of T to every finite subtheory contained in T.", "Stage1Instances.THM_M_0698.SatisfiableToFinite", "T.IsSatisfiable implies T.IsFinitelySatisfiable."),
    ("M0698-B-REVERSE", "branch", "critical", "Construct a model of T from models of all finite subtheories.", "Stage1Instances.THM_M_0698.FiniteToSatisfiable", "T.IsFinitelySatisfiable implies T.IsSatisfiable."),
    ("M0698-C-FINITE-MODELS", "construction", "critical", "For each Finset of sentence subtypes of T, choose a model of its mapped finite subtheory and audit the subtype/map containment bridge.", "mathlib compactness body: family M indexed by Finset T", "A nonempty model carrier and structure for every finite index."),
    ("M0698-C-ULTRAFILTER", "construction", "critical", "Use an ultrafilter extending the atTop filter on Finset T and record the choice and properness boundary.", "Ultrafilter.of (Filter.atTop : Filter (Finset T))", "The ultrafilter used by the compactness construction."),
    ("M0698-C-PRODUCT", "construction", "critical", "Form the filter product of the chosen finite models and its induced first-order structure.", "Filter.Product (Ultrafilter.of (Filter.atTop : Filter (Finset T))) M", "The candidate ultraproduct carrier M'."),
    ("M0698-L-LOS", "bridge", "critical", "Apply Los's sentence theorem for the ultraproduct; keep this imported major theorem as its own bridge obligation.", "FirstOrder.Language.Ultraproduct.sentence_realize", "Truth of each sentence is characterized by ultrafilter eventual truth."),
    ("M0698-L-EVENTUALLY", "core_lemma", "critical", "For each phi in T, prove eventual realization by choosing the singleton finite index and monotonicity in the atTop filter.", "eventual-atTop singleton argument in Mathlib.ModelTheory.Satisfiability", "Every sentence of T holds in the product structure."),
    ("M0698-T-MODEL", "terminal", "high", "Package the product structure satisfying T as ModelType.of and hence as T.IsSatisfiable.", "ModelType.of T M'", "A witness of T.IsSatisfiable."),
    ("M0698-T-ASSEMBLE", "terminal", "high", "Combine the independently typed forward and reverse implications into the exact iff target.", "Stage1Instances.THM_M_0698.firstOrderCompactness_of_directions", "The exact FirstOrderCompactnessTarget."),
    ("M0698-X-SOURCE", "terminal", "high", "Map the semantic compactness architecture and every material construction to pinpoint reviewed human sources.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0698-X-PROVENANCE", "certificate", "critical", "Bind the imported mathlib terminal body, Los bridge, imports, axioms, placeholders, revisions, and replay evidence.", "pinned mathlib proof-body provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0698-S-DEFINITIONS", "M0698-S-UNIVERSES", "M0698-B-FORWARD", "M0698-T-ASSEMBLE"}
source_na = {"M0698-S-DEFINITIONS", "M0698-S-UNIVERSES", "M0698-S-BOUNDARY", "M0698-S-FOUNDATION", "M0698-B-FORWARD", "M0698-X-PROVENANCE"}
machine_special = {"M0698-X-SOURCE": "not_applicable", "M0698-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    if oid in {"M0698-ROOT", "M0698-S-DEFINITIONS", "M0698-S-UNIVERSES"}:
        fingerprint = "lean-source:v1:sha256:" + statement_hash
    else:
        fingerprint = "planned:v1:sha256:" + canonical_hash([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = None
    if oid == "M0698-B-FORWARD":
        body = "local:Stage1_Instances/THM-M-0698/ObligationTree.lean#satisfiableToFinite_checked"
    elif oid == "M0698-T-ASSEMBLE":
        body = "local:Stage1_Instances/THM-M-0698/ObligationTree.lean#firstOrderCompactness_of_directions"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    machine_debt = "M0-L" if oid in checked else ("M3" if oid == "M0698-ROOT" else "M4")
    nodes.append({
        "node_id": "THM-M-0698-" + oid.removeprefix("M0698-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": machine_debt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if body else ("pinned-mathlib-body-audit-pending-proof-gate" if oid in {"M0698-B-REVERSE", "M0698-L-LOS"} else "none"),
        "foundation_profile": "lean4-mathlib-classical/propext-choice-quotient-policy-review-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no solver, oracle, or unchecked computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires conclusions and the frozen formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only a declared typed parent or non-proof support edge may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0698/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0698-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0698/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0698 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = canonical_hash([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit; the two-direction ultraproduct architecture was enumerated before proof-gate status was assigned.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0698-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0698-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the reverse compactness construction, source/readability review, audit completion, and theorem completion are not claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0698-ROOT": ["M0698-T-ASSEMBLE"],
    "M0698-T-ASSEMBLE": ["M0698-B-FORWARD", "M0698-B-REVERSE"],
    "M0698-B-REVERSE": ["M0698-C-FINITE-MODELS", "M0698-C-ULTRAFILTER", "M0698-C-PRODUCT", "M0698-L-LOS", "M0698-L-EVENTUALLY", "M0698-T-MODEL"],
    "M0698-C-PRODUCT": ["M0698-C-FINITE-MODELS", "M0698-C-ULTRAFILTER"],
    "M0698-L-EVENTUALLY": ["M0698-C-FINITE-MODELS"],
    "M0698-T-MODEL": ["M0698-C-PRODUCT", "M0698-L-LOS", "M0698-L-EVENTUALLY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [
        edge("REF-ROOT-DEFS", "M0698-ROOT", "logical_decomposition", "M0698-S-DEFINITIONS"),
        edge("REF-ROOT-UNIV", "M0698-ROOT", "logical_decomposition", "M0698-S-UNIVERSES"),
        edge("REF-ROOT-BOUND", "M0698-ROOT", "logical_decomposition", "M0698-S-BOUNDARY"),
        edge("REF-ROOT-FOUND", "M0698-ROOT", "logical_decomposition", "M0698-S-FOUNDATION"),
    ],
    "provenance": [
        edge("SRC-REVERSE", "M0698-B-REVERSE", "source_map", "M0698-X-SOURCE"),
        edge("SRC-LOS", "M0698-L-LOS", "source_map", "M0698-X-SOURCE"),
        edge("PROV-REVERSE", "M0698-X-PROVENANCE", "provenance_of", "M0698-B-REVERSE"),
        edge("PROV-ROOT", "M0698-X-PROVENANCE", "provenance_of", "M0698-ROOT"),
    ],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUND", "M0698-ROOT", "trusts", "M0698-S-FOUNDATION"),
        edge("TRUST-PROV", "M0698-ROOT", "trusts", "M0698-X-PROVENANCE"),
    ],
    "documentation": [
        edge("DOC-DEFS", "M0698-S-DEFINITIONS", "documents", "M0698-ROOT"),
        edge("DOC-SOURCE", "M0698-X-SOURCE", "documents", "M0698-B-REVERSE"),
    ],
    "workflow": [
        edge("FLOW-ASSEMBLE-REVERSE", "M0698-T-ASSEMBLE", "workflow_depends_on", "M0698-B-REVERSE"),
        edge("FLOW-REVERSE-CONSTRUCTIONS", "M0698-B-REVERSE", "workflow_depends_on", "M0698-C-PRODUCT"),
        edge("FLOW-PROV-ASSEMBLE", "M0698-X-PROVENANCE", "workflow_depends_on", "M0698-T-ASSEMBLE"),
    ],
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
    "registry_id": "THM-M-0698-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0698-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0698-B-REVERSE"],
        "composition_certificates": ["Stage1Instances.THM_M_0698.firstOrderCompactness_of_directions"],
        "reason": "The exact root composition is conditional; FiniteToSatisfiable has no local proof body in this phase.",
    },
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    declarations = []
    if oid == "M0698-B-FORWARD":
        declarations = ["Stage1Instances.THM_M_0698.satisfiableToFinite_checked"]
    elif oid == "M0698-T-ASSEMBLE":
        declarations = ["Stage1Instances.THM_M_0698.firstOrderCompactness_of_directions"]
    recipes["recipes"].append({
        "recipe_id": "VAL-" + oid, "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0698/check_obligation_tree.py"],
        "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0698 obligation tree"}],
        "covered_obligation_ids": [oid], "covered_declarations": declarations,
    })

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
