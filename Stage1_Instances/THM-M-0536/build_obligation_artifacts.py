#!/usr/bin/env python3
"""Build the frozen THM-M-0536 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0536-OBLIGATION_TREE"
THEOREM = "THM-M-0536"


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0536-ROOT", "root", "critical", "The exact induced-map IsIso target frozen in Target.lean.", "Stage1.THM_M_0536.HomotopyInvarianceStatement", "The forward induced map is an isomorphism in every degree."),
    ("M0536-S-DEFINITIONS", "definition", "high", "Fix unreduced integral singular homology, ModuleCat Z, natural grading, and the induced-map convention.", "Stage1.THM_M_0536.IntegralSingularHomology", "The exact homology functor and coefficient object used by the root."),
    ("M0536-S-DOMAINS", "normalization", "high", "Account for base-universe spaces, topology instances, TopCat coercions, degree zero, and empty spaces.", "planned exact context and coercion audit for HomotopyInvarianceStatement", "All quantified and boundary inputs retain the canonical meaning."),
    ("M0536-S-FOUNDATION", "certificate", "critical", "Fix the accepted propext, Classical.choice, Quot.sound, kernel, import, and no-oracle boundary.", "planned transitive axiom and trust report", "An accepted foundation and TCB profile for terminal bodies."),
    ("M0536-N-FUNCTOR", "normalization", "high", "Name the degree-n integral singular homology functor and normalize the two continuous maps as TopCat morphisms.", "local lets F, f, g in Stage1.THM_M_0536", "A common categorical context for both inverse equations."),
    ("M0536-C-INVERSE", "construction", "high", "Construct the proposed inverse morphism as the homology map induced by e.invFun.", "F.map (TopCat.ofHom e.invFun)", "A candidate inverse to the forward induced map."),
    ("M0536-L-LEFT-HOMOTOPY", "core_lemma", "critical", "Use e.left_inv to identify e.toFun followed by e.invFun with the identity up to homotopy.", "ContinuousMap.HomotopyEquiv.left_inv", "A TopCat.Homotopy (f ≫ g) (𝟙 _)."),
    ("M0536-L-RIGHT-HOMOTOPY", "core_lemma", "critical", "Use e.right_inv to identify e.invFun followed by e.toFun with the identity up to homotopy.", "ContinuousMap.HomotopyEquiv.right_inv", "A TopCat.Homotopy (g ≫ f) (𝟙 _)."),
    ("M0536-X-HOMOTOPY-MAP", "bridge", "critical", "Cross the pinned mathlib boundary turning a TopCat homotopy into equality of induced singular-homology maps.", "TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor", "Equality of the two induced maps for each supplied homotopy."),
    ("M0536-T-LEFT-IDENTITY", "terminal", "critical", "Combine functoriality, the left homotopy, and the homotopy-map bridge.", "planned F.map f ≫ F.map g = 𝟙 _", "The left inverse law for the proposed inverse."),
    ("M0536-T-RIGHT-IDENTITY", "terminal", "critical", "Combine functoriality, the right homotopy, and the homotopy-map bridge.", "planned F.map g ≫ F.map f = 𝟙 _", "The right inverse law for the proposed inverse."),
    ("M0536-T-INVERSE-LAWS", "terminal", "high", "Package both induced inverse equations without weakening either direction.", "Stage1.THM_M_0536.InducedInverseLaws", "Both equations required by CategoryTheory.IsIso."),
    ("M0536-T-ASSEMBLE", "transport", "high", "Consume the inverse-law package and install the candidate inverse in an IsIso instance.", "Stage1.THM_M_0536.root_of_inducedInverseLaws", "The exact canonical root, conditional only on InducedInverseLaws."),
    ("M0536-X-SOURCE", "terminal", "high", "Map the two homotopy laws, homotopy invariance, and categorical assembly to reviewed primary-source passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0536-X-PROVENANCE", "certificate", "critical", "Inventory wrapper, terminal mathlib body, imports, axioms, placeholders, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

conditional_checked = {"M0536-T-ASSEMBLE"}
source_na = {"M0536-S-DEFINITIONS", "M0536-S-DOMAINS", "M0536-S-FOUNDATION", "M0536-N-FUNCTOR", "M0536-C-INVERSE", "M0536-X-PROVENANCE"}
machine_special = {"M0536-X-SOURCE": "not_applicable", "M0536-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Target.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0536-ROOT", "M0536-S-DEFINITIONS"} else "planned:v1:sha256:" + canonical_hash([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-0536/ObligationTree.lean#root_of_inducedInverseLaws" if oid == "M0536-T-ASSEMBLE" else None
    obligations.append({"obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": "THM-M-0536-" + oid.removeprefix("M0536-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output, "human_debt": "H1",
        "machine_debt": "M0-L" if oid in conditional_checked else ("M3" if oid == "M0536-ROOT" else "M4"), "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if body else ("pinned-mathlib-terminal-body-audit-pending" if oid == "M0536-X-HOMOTOPY-MAP" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no evaluator, certificate, or oracle closes this node", "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only the declared incoming proof conclusions and exact formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0536/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; this node supplies no unlisted premise and does not promote the accepted root state.",
        "task_ids": [ITEM, "S56-M-0536-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0536/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0536 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in conditional_checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Target.lean", "obligation registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in conditional_checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = canonical_hash([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact induced-map statement and bounded anchor architecture; eligibility is fixed without crediting the observed audit candidate as root closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": "M0536-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0536-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"conditionally_checked_obligations": sorted(conditional_checked), "accepted_root_machine_debt": "M4"},
    "status_boundary": "Frozen scope and denominators only; no proof-phase root receipt, H0, R0, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0536-ROOT": ["M0536-T-ASSEMBLE"], "M0536-T-ASSEMBLE": ["M0536-T-INVERSE-LAWS", "M0536-C-INVERSE"],
    "M0536-T-INVERSE-LAWS": ["M0536-T-LEFT-IDENTITY", "M0536-T-RIGHT-IDENTITY"],
    "M0536-T-LEFT-IDENTITY": ["M0536-N-FUNCTOR", "M0536-L-LEFT-HOMOTOPY", "M0536-X-HOMOTOPY-MAP"],
    "M0536-T-RIGHT-IDENTITY": ["M0536-N-FUNCTOR", "M0536-L-RIGHT-HOMOTOPY", "M0536-X-HOMOTOPY-MAP"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0536-ROOT", "logical_decomposition", "M0536-S-DEFINITIONS"), edge("REF-ROOT-DOMAINS", "M0536-ROOT", "logical_decomposition", "M0536-S-DOMAINS"), edge("REF-ROOT-FOUND", "M0536-ROOT", "logical_decomposition", "M0536-S-FOUNDATION")],
    "provenance": [edge("SRC-LEFT", "M0536-L-LEFT-HOMOTOPY", "source_map", "M0536-X-SOURCE"), edge("SRC-RIGHT", "M0536-L-RIGHT-HOMOTOPY", "source_map", "M0536-X-SOURCE"), edge("PROV-BRIDGE", "M0536-X-PROVENANCE", "provenance_of", "M0536-X-HOMOTOPY-MAP"), edge("PROV-ROOT", "M0536-X-PROVENANCE", "provenance_of", "M0536-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0536-ROOT", "trusts", "M0536-S-FOUNDATION"), edge("TRUST-PROV", "M0536-ROOT", "trusts", "M0536-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0536-S-DEFINITIONS", "documents", "M0536-ROOT"), edge("DOC-SOURCE", "M0536-X-SOURCE", "documents", "M0536-X-HOMOTOPY-MAP")],
    "workflow": [edge("FLOW-ASSEMBLE-LAWS", "M0536-T-ASSEMBLE", "workflow_depends_on", "M0536-T-INVERSE-LAWS"), edge("FLOW-LAWS-LEFT", "M0536-T-INVERSE-LAWS", "workflow_depends_on", "M0536-T-LEFT-IDENTITY"), edge("FLOW-LAWS-RIGHT", "M0536-T-INVERSE-LAWS", "workflow_depends_on", "M0536-T-RIGHT-IDENTITY"), edge("FLOW-PROV-ASSEMBLE", "M0536-X-PROVENANCE", "workflow_depends_on", "M0536-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"]); incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-0536-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M0536-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"conditionally_checked_obligations": sorted(conditional_checked), "accepted_root_closed": False, "accepted_root_machine_debt": "M4", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0536-T-INVERSE-LAWS"], "composition_certificates": ["Stage1.THM_M_0536.root_of_inducedInverseLaws"], "reason": "The checked composition is conditional; InducedInverseLaws has no proof-phase body or accepted receipt."}}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0536/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0536 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1.THM_M_0536.root_of_inducedInverseLaws"] if oid == "M0536-T-ASSEMBLE" else []} for oid, *_ in rows]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
