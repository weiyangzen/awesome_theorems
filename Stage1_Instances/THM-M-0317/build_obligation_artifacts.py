#!/usr/bin/env python3
"""Build the frozen THM-M-0317 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0317-OBLIGATION_TREE"
THEOREM = "THM-M-0317"
PREFIX = "M0317"

def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()

rows = [
 ("ROOT", "root", "critical", "The exact Tychonoff fixed-point target.", "AwesomeTheorems.THM_M_0317.TychonoffFixedPointTarget", "The canonical proposition."),
 ("S-DEFINITIONS", "definition", "high", "Freeze fixed point, displacement, compactness, convexity, continuity, and invariance predicates.", "AwesomeTheorems.THM_M_0317.{TychonoffFixedPointTarget,HasArbitrarilySmallDisplacement}", "Exact statement and approximation vocabulary."),
 ("S-DOMAINS", "transport", "high", "Preserve the ambient/subtype self-map encoding and all real locally convex Hausdorff structures.", "AwesomeTheorems.THM_M_0317.ambient_subtype_fixed_point_iff", "Checked equivalence of fixed-point conclusions."),
 ("S-BOUNDARY", "terminal", "high", "Preserve nonemptiness, membership, binder scope, and MapsTo boundary conditions.", "AwesomeTheorems.THM_M_0317.{empty_boundary_rejects_removed_nonempty,ambient_domain_does_not_imply_member_domain,fixed_point_cannot_precede_map_binder,interval_rejects_removed_mapsTo}", "Checked rejection of four non-equivalent mutations."),
 ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, separation, imported axioms, TCB, and absence of computational oracles.", "planned exact axiom and transitive dependency report", "Accepted foundation and trust boundary."),
 ("N-NEIGHBORHOODS", "normalization", "critical", "Reduce equality f x = x to displacement membership in every zero neighbourhood, with the correct directed limit formulation.", "planned neighbourhood/separation reduction", "An exact small-displacement criterion for fixed points."),
 ("C-FINITE-COVER", "construction", "critical", "For a chosen convex zero neighbourhood, extract finitely many control points covering f(K) by translates.", "planned compact-image finite subcover construction", "Finite control points and a subordinate cover of K."),
 ("C-PARTITION", "construction", "critical", "Construct continuous nonnegative weights subordinate to the finite cover, summing to one on K.", "planned finite partition-of-unity construction on compact K", "Continuous barycentric weights with support invariants."),
 ("C-FINITE-MAP", "construction", "critical", "Build the finite-rank barycentric self-map whose image lies in a finite-dimensional compact convex hull and prove it approximates f.", "planned finite-rank approximation map and invariants", "A continuous finite-dimensional self-map uniformly close to f."),
 ("L-BROUWER", "bridge", "critical", "Prove the fixed-point theorem for the resulting finite-dimensional compact convex hull, including affine-span and degenerate cases.", "planned exact finite-dimensional compact-convex fixed-point theorem", "A fixed point of the finite-rank approximation."),
 ("L-APPROX-FIXED", "core_lemma", "critical", "Transfer the finite-rank fixed point and approximation bound to a point x in K with f x - x in the chosen neighbourhood.", "planned approximate-fixed-point transfer", "One approximate fixed point at each neighbourhood scale."),
 ("L-COMPACT-LIMIT", "core_lemma", "critical", "Use compactness of K and Hausdorff separation to turn arbitrarily small displacements into an exact fixed point.", "AwesomeTheorems.THM_M_0317.CompactnessLimitPackage", "An in-K exact fixed point."),
 ("T-APPROX", "terminal", "critical", "Assemble finite cover, partition, finite-rank map, Brouwer, and transfer for every zero neighbourhood.", "AwesomeTheorems.THM_M_0317.ApproximationPackage", "Arbitrarily small displacement for every admissible K and f."),
 ("T-LIMIT", "terminal", "critical", "Assemble neighbourhood normalization and compactness into the exact limit package.", "AwesomeTheorems.THM_M_0317.CompactnessLimitPackage", "Exact fixed point from the approximation property."),
 ("T-ASSEMBLE", "transport", "high", "Compose the approximation and compactness-limit packages into the exact canonical target.", "AwesomeTheorems.THM_M_0317.root_of_approximation_and_limit", "The exact root conditional on both packages."),
 ("X-SOURCE", "terminal", "high", "Map every material construction and limiting argument to reviewed theorem/page/assumption/errata records.", "non-machine node-level primary-source crosswalk", "Human-source coverage without machine proof credit."),
 ("X-PROVENANCE", "certificate", "critical", "Inventory imports, terminal bodies, wrappers, axiom closure, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"S-DEFINITIONS", "S-DOMAINS", "S-BOUNDARY", "T-ASSEMBLE"}
source_na = {"S-DEFINITIONS", "S-DOMAINS", "S-BOUNDARY", "S-FOUNDATION", "X-PROVENANCE"}
machine_special = {"X-SOURCE": "not_applicable", "X-PROVENANCE": "informational"}
obligations, nodes = [], []
for suffix, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{suffix}"
    machine = machine_special.get(suffix, "required")
    fp = "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
      "root_relevant": True, "machine_eligibility": machine,
      "human_source_eligibility": "not_applicable" if suffix in source_na else "required",
      "readable_eligibility": "required", "risk_class": risk,
      "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
      "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0317/ObligationTree.lean#root_of_approximation_and_limit" if suffix == "T-ASSEMBLE" else None})
    nodes.append({"node_id": f"THM-M-0317-{suffix}", "obligation_id": oid, "kind": kind,
      "human_statement": claim, "formal_target": target, "output": output,
      "human_debt": "H1", "machine_debt": "M0-L" if suffix in checked else ("M3" if suffix == "ROOT" else "M4"), "readability_debt": "R4",
      "evidence_ids": [], "source_crosswalk_id": "not-applicable" if suffix in source_na else "primary-source-node-map-pending",
      "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
      "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
      "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
      "computation_record": "none; no numerical approximation or oracle closes an existence node",
      "step_budget": 100 if suffix in {"C-PARTITION", "C-FINITE-MAP", "L-BROUWER", "L-COMPACT-LIMIT"} else 40,
      "semantic_step_ledger": {"premises": "The exact stated context and incoming proof_requires conclusions only.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
      "public_readable_target": f"Stage1_Instances/THM-M-0317/obligation-tree.md#{oid.lower()}",
      "validation_spec_id": f"VAL-{oid}", "status_boundary": "Architecture or conditional interface only; no unlisted premise or root proof is supplied.",
      "task_ids": [ITEM, "S56-M-0317-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0317/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
      "owner": "THM-M-0317 proof lane", "reviewer": "independent Stage1 integration lane",
      "validity": {"validated_at": "2026-07-12" if suffix in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if suffix in checked else "open"}})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: o[k] for k in fields} for o in obligations])
ids = [o["obligation_id"] for o in obligations]
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
 "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
 "freeze_basis": "Exact 1935 real Hausdorff statement and immutable anchor audit; finite-dimensional approximation plus compactness architecture; eligibility fixed before closure observation.",
 "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
 "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
 "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
 "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
 "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
 "obligations": obligations, "append_only_delta": [],
 "status_observed_after_freeze": {"closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked), "root_machine_debt": "M3"},
 "status_boundary": "Frozen scope only; both substantive packages remain open and no root, audit, or theorem completion is claimed."}

def edge(eid, source, typ, target, reciprocal=None):
    out = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal: out["reciprocal_edge_id"] = reciprocal
    return out

requires = {
 f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
 f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-APPROX", f"{PREFIX}-T-LIMIT"],
 f"{PREFIX}-T-APPROX": [f"{PREFIX}-C-FINITE-COVER", f"{PREFIX}-C-PARTITION", f"{PREFIX}-C-FINITE-MAP", f"{PREFIX}-L-BROUWER", f"{PREFIX}-L-APPROX-FIXED"],
 f"{PREFIX}-T-LIMIT": [f"{PREFIX}-N-NEIGHBORHOODS", f"{PREFIX}-L-COMPACT-LIMIT"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {
 "proof": proof,
 "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-DOMAINS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DOMAINS"), edge("REF-ROOT-BOUNDARY", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
 "provenance": [edge("SRC-APPROX", f"{PREFIX}-T-APPROX", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-LIMIT", f"{PREFIX}-T-LIMIT", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
 "evidence": [],
 "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
 "documentation": [edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-ROOT"), edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT")],
 "workflow": [edge("FLOW-ASSEMBLE-APPROX", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-APPROX"), edge("FLOW-ASSEMBLE-LIMIT", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-LIMIT"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
 "registry_id": "THM-M-0317-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
 "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
 "nodes": nodes, "graphs": graphs,
 "closure_boundary": {"closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-APPROX", f"{PREFIX}-T-LIMIT"], "composition_certificates": ["AwesomeTheorems.THM_M_0317.root_of_approximation_and_limit"], "reason": "The checked final composition is conditional; neither package has a proof body."}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
 "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0317/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
