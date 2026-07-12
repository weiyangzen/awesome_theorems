#!/usr/bin/env python3
"""Build the frozen THM-M-0540 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0540-OBLIGATION_TREE"
THEOREM = "THM-M-0540"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0540-ROOT", "root", "critical", "For every small space X and n, integral singular homology is degree-n homology of the integral singular chain complex.", "Stage1.THM_M_0540.CanonicalTarget", "The exact universally quantified construction identity."),
    ("M0540-D-CHAINS", "definition", "high", "Specialize singularChainComplexFunctor to ModuleCat Int, its integer coefficient object, and TopCat.of X.", "Stage1.THM_M_0540.IntegralSingularChains", "The exact Nat-indexed integral singular chain complex used at the root."),
    ("M0540-D-HOMOLOGY", "definition", "high", "Specialize singularHomologyFunctor to ModuleCat Int, degree n, integer coefficients, and TopCat.of X.", "Stage1.THM_M_0540.IntegralSingularHomology", "The exact integral singular homology object used at the root."),
    ("M0540-N-SPECIALIZE", "normalization", "critical", "Normalize the pinned singularHomologyFunctor definition as singularChainComplexFunctor followed by homologyFunctor at n.", "AlgebraicTopology.singularHomologyFunctor", "A definitionally aligned categorical expression at the canonical coefficients, space, and degree."),
    ("M0540-T-UNFOLD", "terminal", "critical", "Unfold the two local abbreviations and pinned functor definition to establish the exact pointwise equality.", "Stage1.THM_M_0540.UnfoldingEquation", "The equality required for every X and n, without changed binders or coefficients."),
    ("M0540-T-ASSEMBLE", "transport", "high", "Consume the exact unfolding equation as the canonical proposition without weakening or adding assumptions.", "Stage1.THM_M_0540.root_of_unfolding", "The exact canonical root, conditional on UnfoldingEquation."),
    ("M0540-X-SOURCE", "terminal", "high", "Map singular simplices, chains, differential, coefficients, and homology to pinpoint reviewed primary-source passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0540-X-PROVENANCE", "certificate", "critical", "Bind the local composition and wrapper to the pinned mathlib definition, terminal body identity, source hash, and dependency closure.", "planned machine-derived provenance packet", "Formal provenance without duplicate wrapper credit."),
    ("M0540-X-TRUST", "certificate", "critical", "Audit terminal axioms, imports, placeholders, kernel, compiled artifacts, and the no-oracle computation boundary.", "planned transitive trust and TCB report", "An accepted foundation and trust boundary for later proof credit."),
]

source_na = {"M0540-D-CHAINS", "M0540-D-HOMOLOGY", "M0540-N-SPECIALIZE", "M0540-X-PROVENANCE", "M0540-X-TRUST"}
machine_special = {"M0540-X-SOURCE": "not_applicable", "M0540-X-PROVENANCE": "informational", "M0540-X-TRUST": "informational"}
conditional = {"M0540-T-ASSEMBLE"}
statement_hash = hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = "lean-statement-json:v1:sha256:" + statement_hash if oid == "M0540-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "assurance_overlay_no_semantic_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-0540/ObligationTree.lean#root_of_unfolding" if oid == "M0540-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0540-" + oid.removeprefix("M0540-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in conditional else ("M3" if oid == "M0540-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if body else ("pinned-mathlib-body-audit-pending" if oid in {"M0540-N-SPECIALIZE", "M0540-T-UNFOLD"} else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; noncomputable categorical construction, with no evaluator, certificate, or oracle credited",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only conclusions arriving through declared typed edges and the frozen formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed edges may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0540/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no unlisted premise or accepted root promotion.",
        "task_ids": [ITEM, "S56-M-0540-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0540/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0540 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in conditional else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["statement.json", "anchor-audit.json", "obligation-registry.json", "toolchain"],
                     "revocation_state": "provisional" if oid in conditional else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated construction target and pre-proof architecture; eligibility is frozen without crediting the already observed rfl anchor.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0540-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0540-X-PROVENANCE", "M0540-X-TRUST"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"conditionally_checked_obligations": sorted(conditional), "accepted_root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; no proof-phase root receipt, H0, R0, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M0540-ROOT": ["M0540-T-ASSEMBLE"], "M0540-T-ASSEMBLE": ["M0540-T-UNFOLD"], "M0540-T-UNFOLD": ["M0540-N-SPECIALIZE", "M0540-D-CHAINS", "M0540-D-HOMOLOGY"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-CHAINS", "M0540-ROOT", "logical_decomposition", "M0540-D-CHAINS"), edge("REF-ROOT-HOMOLOGY", "M0540-ROOT", "logical_decomposition", "M0540-D-HOMOLOGY")],
    "provenance": [edge("SRC-DEFS", "M0540-D-CHAINS", "source_map", "M0540-X-SOURCE"), edge("SRC-HOMOLOGY", "M0540-D-HOMOLOGY", "source_map", "M0540-X-SOURCE"), edge("PROV-UNFOLD", "M0540-X-PROVENANCE", "provenance_of", "M0540-T-UNFOLD"), edge("PROV-ASSEMBLE", "M0540-X-PROVENANCE", "provenance_of", "M0540-T-ASSEMBLE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0540-ROOT", "trusts", "M0540-X-TRUST"), edge("TRUST-UNFOLD", "M0540-T-UNFOLD", "trusts", "M0540-X-TRUST")],
    "documentation": [edge("DOC-SOURCE", "M0540-X-SOURCE", "documents", "M0540-ROOT"), edge("DOC-PROVENANCE", "M0540-X-PROVENANCE", "documents", "M0540-T-UNFOLD")],
    "workflow": [edge("FLOW-ASSEMBLE-UNFOLD", "M0540-T-ASSEMBLE", "workflow_depends_on", "M0540-T-UNFOLD"), edge("FLOW-UNFOLD-NORM", "M0540-T-UNFOLD", "workflow_depends_on", "M0540-N-SPECIALIZE"), edge("FLOW-PROV-UNFOLD", "M0540-X-PROVENANCE", "workflow_depends_on", "M0540-T-UNFOLD"), edge("FLOW-TRUST-PROV", "M0540-X-TRUST", "workflow_depends_on", "M0540-X-PROVENANCE")],
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
    "registry_id": "THM-M-0540-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0540-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"conditionally_checked_obligations": sorted(conditional), "accepted_root_closed": False,
                         "accepted_root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0540-T-UNFOLD"],
                         "composition_certificates": ["Stage1.THM_M_0540.root_of_unfolding"],
                         "reason": "The checked composition is conditional; the audited rfl candidate has no proof-phase receipt."},
}
recipes = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "cwd": ".",
                 "argv": ["python3", "Stage1_Instances/THM-M-0540/check_obligation_tree.py"],
                 "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied",
                 "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0540 obligation tree"}],
                 "covered_obligation_ids": [oid], "covered_declarations": ["Stage1.THM_M_0540.root_of_unfolding"] if oid == "M0540-T-ASSEMBLE" else []}
                for oid, *_ in rows],
}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
