#!/usr/bin/env python3
"""Build the frozen THM-M-0590 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0590-OBLIGATION_TREE"
THEOREM = "THM-M-0590"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# Architecture is frozen before consulting proof closure.  Each tuple is
# id, kind, risk, human statement, formal target, output, source eligibility.
rows = [
    ("M0590-ROOT", "root", "critical", "The exact Brown-Douglas-Fillmore operator-classification target frozen in Statement.lean.", "THMM0590.brownDouglasFillmoreTarget", "The canonical proposition.", "required"),
    ("M0590-S-DEFINITIONS", "definition", "high", "Freeze Fredholmness, index, essential spectrum, essential normality, and unitary equivalence modulo compact operators with exactly the statement conventions.", "THMM0590.{IsFredholm,fredholmIndex,essentialSpectrum,IsEssentiallyNormal,UnitaryEquivalentModuloCompacts}", "The exact elaborated definition interface.", "not_applicable"),
    ("M0590-S-DOMAINS", "definition", "high", "Preserve separable infinite-dimensional complex Hilbert domains, universe-polymorphic operator spaces, and the ordered hypotheses.", "binder prefix of THMM0590.brownDouglasFillmoreTarget", "The canonical domain and typeclass context.", "not_applicable"),
    ("M0590-S-BOUNDARY", "terminal", "high", "Account for normal operators, distinct but unitarily isomorphic domains, and exclusion of essential-spectrum points from the index comparison.", "planned exact boundary lemmas for THMM0590 definitions", "Checked boundary behavior without weakening the root.", "required"),
    ("M0590-S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotient, extensionality, Lean kernel, mathlib, and no-oracle policies for all terminal bodies.", "planned transitive foundation and axiom report", "Accepted trust boundary.", "not_applicable"),
    ("M0590-N-CALKIN", "normalization", "critical", "Construct the Calkin quotient and prove that compact self-commutator is equivalent to normality of the quotient image.", "planned Lean Calkin quotient and essentially-normal transport", "Normal Calkin elements representing T and S.", "required"),
    ("M0590-N-FREDHOLM", "transport", "critical", "Relate the local kernel/cokernel/closed-range Fredholm predicate and T-minus-lambda index to invertibility and boundary data in the Calkin algebra.", "planned Atkinson theorem and index-sign transport", "Checked equivalence of the analytic and quotient invariants.", "required"),
    ("M0590-L-FWD-SPECTRUM", "core_lemma", "high", "Unitary conjugacy modulo compacts preserves the essential spectrum.", "planned exact Lean forward essential-spectrum invariance theorem", "Equality of essential spectra.", "required"),
    ("M0590-L-FWD-INDEX", "core_lemma", "critical", "Unitary conjugacy and compact perturbation preserve the Fredholm index of T minus lambda I at every off-spectrum lambda.", "planned exact Lean compact-perturbation index theorem", "Pointwise equality of off-spectrum indices.", "required"),
    ("M0590-B-FORWARD", "branch", "high", "Combine spectrum and index invariance to prove the forward implication of the exact root.", "THMM0590.ForwardInvariantPackage", "The invariant conjunction from unitary equivalence modulo compacts.", "required"),
    ("M0590-C-BUSBY", "construction", "critical", "From an essentially normal operator with essential spectrum X, construct the unital extension of C(X) by compact operators, proving well-definedness and independence of functional-calculus choices.", "planned Busby-invariant construction in Lean", "A well-defined extension class attached to each operator.", "required"),
    ("M0590-L-EXT-CLASS", "bridge", "critical", "Classify the relevant extensions of C(X) by compact operators up to the equivalence needed for operator conjugacy modulo compacts.", "planned exact BDF extension-classification theorem", "Equality of extension classes exactly when the required unitary equivalence holds.", "required"),
    ("M0590-L-INDEX-COMPLETE", "bridge", "critical", "Prove that equality of the off-spectrum Fredholm-index functions is a complete invariant for the two extension classes over the common essential spectrum.", "planned index-to-Ext completeness theorem", "Equality of the Busby extension classes.", "required"),
    ("M0590-T-BACKWARD", "terminal", "critical", "Transport equal spectrum and index data through the Calkin and extension classifications to produce a unitary whose conjugacy error is compact.", "THMM0590.BackwardClassificationPackage", "The backward implication of the exact root.", "required"),
    ("M0590-T-ASSEMBLE", "transport", "high", "Compose the exact forward and backward packages into the canonical biconditional with no additional premise.", "THMM0590.root_of_directional_packages", "The exact canonical root conditional on both packages.", "required"),
    ("M0590-X-SOURCE", "terminal", "high", "Map every material analytic and extension-theoretic node to reviewed primary-source theorem passages, conventions, and hypotheses.", "node-specific non-machine primary-source crosswalk", "Human-source coverage without machine proof credit.", "required"),
    ("M0590-X-PROVENANCE", "certificate", "critical", "Inventory terminal proof bodies, imports, transitive declarations, axioms, TCB, licenses, and replay evidence.", "planned machine-derived provenance closure", "Release provenance coverage without mathematical proof credit.", "not_applicable"),
]

checked = {"M0590-S-DEFINITIONS", "M0590-S-DOMAINS", "M0590-T-ASSEMBLE"}
machine_special = {"M0590-X-SOURCE": "not_applicable", "M0590-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, source_eligibility in rows:
    exact = oid in {"M0590-ROOT", "M0590-S-DEFINITIONS"}
    fingerprint = ("lean-source-sha256:" + statement_hash if exact else
                   "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": source_eligibility,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0590/ObligationTree.lean#root_of_directional_packages" if oid == "M0590-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": "THM-M-0590-" + oid.removeprefix("M0590-"),
        "obligation_id": oid, "kind": kind, "human_statement": claim,
        "formal_target": target, "output": output, "human_debt": "H1",
        "machine_debt": "M0-L" if oid in checked else ("M4" if oid != "M0590-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "bdf-primary-source-pinpoint-pending" if source_eligibility == "required" else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M0590-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical-quotient/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, solver, or numerical spectrum computation may close this node",
        "step_budget": 100 if risk == "critical" else 60,
        "semantic_step_ledger": {
            "premises": "Only the exact proof_requires children and the formal context named by this node.",
            "inference": claim, "output": output,
            "outgoing_use": "Consumed only by the declared typed parent; support edges confer no proof credit."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0590/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no unlisted premise and no open BDF package is proved.",
        "task_ids": [ITEM, "S56-M-0590-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0590/ObligationTree.lean"] if oid == "M0590-T-ASSEMBLE" else [],
        "owner": "THM-M-0590 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "source map", "toolchain"],
                     "revocation_state": "provisional" if oid in checked else "open"}
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded negative anchor audit; BDF Calkin/extension architecture; eligibility assigned independently of proof availability.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0590-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0590-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; no BDF proof, H0 source acceptance, or theorem completion."
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0590-ROOT": ["M0590-T-ASSEMBLE"],
    "M0590-T-ASSEMBLE": ["M0590-B-FORWARD", "M0590-T-BACKWARD"],
    "M0590-B-FORWARD": ["M0590-L-FWD-SPECTRUM", "M0590-L-FWD-INDEX"],
    "M0590-L-FWD-SPECTRUM": ["M0590-N-CALKIN"],
    "M0590-L-FWD-INDEX": ["M0590-N-FREDHOLM"],
    "M0590-T-BACKWARD": ["M0590-N-CALKIN", "M0590-N-FREDHOLM", "M0590-C-BUSBY", "M0590-L-EXT-CLASS", "M0590-L-INDEX-COMPLETE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0590-ROOT", "logical_decomposition", "M0590-S-DEFINITIONS"), edge("REF-ROOT-DOMAINS", "M0590-ROOT", "logical_decomposition", "M0590-S-DOMAINS"), edge("REF-ROOT-BOUNDARY", "M0590-ROOT", "logical_decomposition", "M0590-S-BOUNDARY")],
    "provenance": [edge("SRC-FORWARD", "M0590-B-FORWARD", "source_map", "M0590-X-SOURCE"), edge("SRC-BACKWARD", "M0590-T-BACKWARD", "source_map", "M0590-X-SOURCE"), edge("PROV-ROOT", "M0590-X-PROVENANCE", "provenance_of", "M0590-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0590-ROOT", "trusts", "M0590-S-FOUNDATION"), edge("TRUST-PROV", "M0590-ROOT", "trusts", "M0590-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0590-S-DEFINITIONS", "documents", "M0590-ROOT"), edge("DOC-SOURCE", "M0590-X-SOURCE", "documents", "M0590-T-BACKWARD")],
    "workflow": [edge("FLOW-ASSEMBLE-FWD", "M0590-T-ASSEMBLE", "workflow_depends_on", "M0590-B-FORWARD"), edge("FLOW-ASSEMBLE-BACK", "M0590-T-ASSEMBLE", "workflow_depends_on", "M0590-T-BACKWARD"), edge("FLOW-PROV-ASSEMBLE", "M0590-X-PROVENANCE", "workflow_depends_on", "M0590-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0590-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0590-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False,
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0590-B-FORWARD", "M0590-T-BACKWARD"],
        "composition_certificates": ["THMM0590.root_of_directional_packages"],
        "reason": "The final composition is conditional; both directional BDF packages lack proof bodies."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({
        "recipe_id": "VAL-" + oid, "obligation_id": oid,
        "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0590/check_obligation_tree.py"],
        "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact PASS prefix plus recomputed registry digest"}],
        "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
