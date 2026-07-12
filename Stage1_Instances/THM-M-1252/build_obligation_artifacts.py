#!/usr/bin/env python3
"""Build the frozen THM-M-1252 registry and its typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1252-OBLIGATION_TREE"
THEOREM = "THM-M-1252"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M1252-ROOT", "root", "critical", "The exact support-localization target frozen in Statement.lean.", "Stage1Instances.THM_M_1252.DistributionSupportLocalizationTarget", "The complement of dsupport is the union of all open vanishing regions."),
    ("M1252-S-DEFINITIONS", "definition", "high", "Unfold IsVanishingOn into evaluation on every test function whose topological support lies in U.", "Stage1Instances.THM_M_1252.distributionSupportLocalizationTarget_iff_expandedTarget", "The checked test-function formulation."),
    ("M1252-S-DOMAIN", "normalization", "high", "Specialize the generic FunLike support API to real-valued distributions on Opens E with E finite-dimensional over Real.", "Stage1Instances.THM_M_1252.ObligationTree.SpecializedAnchor", "The exact ordered binders and scalar/order parameters of the root."),
    ("M1252-S-BOUNDARY", "branch", "normal", "Retain zero distributions, empty domains, and zero-dimensional spaces without adding nondegeneracy assumptions.", "canonical quantifiers in DistributionSupportLocalizationTarget", "Boundary cases remain inside the universal statement."),
    ("M1252-S-TRANSPORT", "transport", "high", "Transport the canonical target to the fully expanded test-function formulation in the declared direction.", "Stage1Instances.THM_M_1252.ObligationTree.expanded_of_root", "ExpandedTarget follows from the canonical root."),
    ("M1252-S-FOUNDATION", "certificate", "critical", "Audit extensionality, choice, quotient, imports, kernel, and the absence of oracle or placeholder boundaries.", "planned transitive axiom and TCB report", "An accepted foundation and trust boundary."),
    ("M1252-N-SPECIALIZE", "reduction", "critical", "Instantiate the generic pinned theorem dsupport_compl_eq at the distribution test-function FunLike instance.", "Distribution.dsupport_compl_eq specialized to Distribution Omega Real top", "SpecializedAnchor."),
    ("M1252-L-UPSTREAM", "bridge", "critical", "Account for the terminal pinned mathlib proof body implementing the generic support identity.", "Distribution.dsupport_compl_eq", "The generic complement-of-support equality."),
    ("M1252-T-COMPOSE", "terminal", "high", "Consume SpecializedAnchor and return the exact canonical target.", "Stage1Instances.THM_M_1252.ObligationTree.root_of_specializedAnchor", "DistributionSupportLocalizationTarget."),
    ("M1252-X-SOURCE", "terminal", "high", "Map the localization definition and support identity to a pinpoint reviewed human source.", "non-machine primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M1252-X-PROVENANCE", "certificate", "critical", "Inventory the imported terminal body, revisions, declarations, axioms, TCB, license, and replay receipts.", "machine-derived provenance closure", "Release provenance without independent proof credit."),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M1252-S-DEFINITIONS", "M1252-S-DOMAIN", "M1252-S-TRANSPORT", "M1252-T-COMPOSE"}
source_na = {"M1252-S-DEFINITIONS", "M1252-S-DOMAIN", "M1252-S-BOUNDARY", "M1252-S-TRANSPORT", "M1252-S-FOUNDATION", "M1252-X-PROVENANCE"}
machine_special = {"M1252-X-SOURCE": "not_applicable", "M1252-X-PROVENANCE": "informational"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = "lean-source:v1:sha256:" + statement_hash if oid == "M1252-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "provenance_overlay_no_proof_credit"}.get(machine)
    body = None
    if oid == "M1252-L-UPSTREAM":
        body = "pinned-mathlib:8a178386ffc0f5fef0b77738bb5449d50efeea95#Distribution.dsupport_compl_eq"
    elif oid == "M1252-T-COMPOSE":
        body = "local:Stage1_Instances/THM-M-1252/ObligationTree.lean#root_of_specializedAnchor"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-1252-" + oid.removeprefix("M1252-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M0-W" if oid == "M1252-L-UPSTREAM" else ("M3" if oid == "M1252-ROOT" else "M4")),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "anchor-audit:Distribution.dsupport_compl_eq" if oid == "M1252-L-UPSTREAM" else ("local-conditional-composition" if oid == "M1252-T-COMPOSE" else "none"),
        "foundation_profile": "Lean4-4.29.0; accepted-foundation-policy-review-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive-closure/release-audit-pending",
        "computation_record": "none; no computation, solver, oracle, or certificate closes this node",
        "step_budget": 30 if risk != "critical" else 60,
        "semantic_step_ledger": {"premises": "Only the exact formal context and incoming proof_requires conclusions.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1252/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture/interface status only; no proof-phase installation, H0, release provenance closure, or theorem completion.",
        "task_ids": [ITEM, "S56-M-1252-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1252/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-1252 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and the already completed immutable-anchor audit; semantic layers follow the generic upstream theorem body and do not clone wrapper credit.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1252-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1252-X-PROVENANCE"],
    },
    "layer_exclusions": {
        "construction": {"status": "not_applicable_pending_independent_approval", "reason": "The selected theorem is a definitional set identity and constructs no mathematical object."},
        "case_split": {"status": "not_applicable_pending_independent_approval", "reason": "The generic upstream proof is uniform and contains no mathematical case split; S-BOUNDARY records retained degenerate inputs."},
        "computation": {"status": "not_applicable_pending_independent_approval", "reason": "No finite or numerical computation, reflection, solver, or certificate is used."},
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 with an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"interface_checked_obligations": sorted(checked), "audited_upstream_candidate": "M1252-L-UPSTREAM", "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and typed architecture only; proof installation and every validation/release gate remain downstream.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1252-ROOT": ["M1252-T-COMPOSE"],
    "M1252-T-COMPOSE": ["M1252-N-SPECIALIZE"],
    "M1252-N-SPECIALIZE": ["M1252-L-UPSTREAM", "M1252-S-DOMAIN"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1252-ROOT", "logical_decomposition", "M1252-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", "M1252-ROOT", "logical_decomposition", "M1252-S-BOUNDARY"), edge("REF-ROOT-TRANSPORT", "M1252-ROOT", "logical_decomposition", "M1252-S-TRANSPORT")],
    "provenance": [edge("SRC-UPSTREAM", "M1252-L-UPSTREAM", "source_map", "M1252-X-SOURCE"), edge("PROV-UPSTREAM", "M1252-X-PROVENANCE", "provenance_of", "M1252-L-UPSTREAM")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M1252-ROOT", "trusts", "M1252-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M1252-ROOT", "trusts", "M1252-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M1252-S-DEFINITIONS", "documents", "M1252-ROOT"), edge("DOC-SOURCE", "M1252-X-SOURCE", "documents", "M1252-L-UPSTREAM")],
    "workflow": [edge("FLOW-COMPOSE-SPECIALIZE", "M1252-T-COMPOSE", "workflow_depends_on", "M1252-N-SPECIALIZE"), edge("FLOW-SPECIALIZE-UPSTREAM", "M1252-N-SPECIALIZE", "workflow_depends_on", "M1252-L-UPSTREAM"), edge("FLOW-PROVENANCE-UPSTREAM", "M1252-X-PROVENANCE", "workflow_depends_on", "M1252-L-UPSTREAM")],
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
    "registry_id": "THM-M-1252-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1252-ROOT", "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"interface_checked_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1252-N-SPECIALIZE"], "composition_certificates": ["Stage1Instances.THM_M_1252.ObligationTree.root_of_specializedAnchor", "Stage1Instances.THM_M_1252.ObligationTree.expanded_of_root"], "reason": "The exact root composition is conditional; installing and validating the audited pinned anchor is assigned to later phases."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1252/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1252 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in graph_edges.values())} typed edges")
print(denominator)
