#!/usr/bin/env python3
"""Build the frozen THM-M-1054 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1054-OBLIGATION_TREE"
THEOREM = "THM-M-1054"
PREFIX = "M1054"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen real L2 Koopman mean-ergodic target.", "Stage1Instances.THM_M_1054.VonNeumannL2MeanErgodicTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze real L2, the Koopman map, Nat-indexed Cesaro averages, and the fixed-space orthogonal projection.", "Stage1Instances.THM_M_1054.{RealL2,Koopman,CesaroAverage,InvariantProjection}", "The elaborated vocabulary of the root."),
    ("S-BOUNDARY", "terminal", "high", "Preserve zero-length averaging and the identity and non-ergodic transformation boundaries without changing the limit.", "Stage1Instances.THM_M_1054.{zeroLengthAverage,target_iff_expandedIntakeShape}", "Checked statement and zero-index behavior."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotients, imported declarations, Lean TCB, and the no-oracle boundary.", "planned transitive axiom/import/TCB certificate", "An accepted foundation and trust profile."),
    ("C-KOOPMAN", "construction", "high", "Construct composition by a measure-preserving map as a linear isometry on real L2 and then as a continuous linear operator.", "MeasureTheory.Lp.compMeasurePreservingₗᵢ", "The Koopman continuous linear operator with its isometry witness."),
    ("L-CONTRACTION", "terminal", "high", "Derive that the Koopman continuous linear operator has norm at most one.", "LinearIsometry.norm_toContinuousLinearMap.le", "norm (Koopman T hT) <= 1."),
    ("B-SUBSINGLETON", "branch", "high", "In a subsingleton L2 space identify every average with the invariant projection and prove convergence of the constant sequence.", "Stage1Instances.THM_M_1054.root_of_nontrivialMeanErgodicPackage (subsingleton branch)", "Convergence for the degenerate L2 branch."),
    ("B-NONTRIVIAL", "branch", "critical", "In a nontrivial L2 space apply the abstract contraction mean-ergodic theorem to the Koopman operator.", "Stage1Instances.THM_M_1054.NontrivialMeanErgodicPackage", "Convergence for the nontrivial L2 branch."),
    ("L-ABSTRACT-MEAN-ERGODIC", "bridge", "critical", "Supply the pinned Hilbert-space theorem that Cesaro averages of a contraction converge to the orthogonal projection onto its fixed subspace.", "ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection", "The nontrivial mean-ergodic convergence package."),
    ("T-FIXED-PROJECTION", "transport", "high", "Identify the abstract fixed-point projection with the root's LinearMap.eqLocus orthogonal projection and its topology.", "LinearMap.eqLocus.orthogonalProjection", "The exact InvariantProjection limit."),
    ("T-ASSEMBLE", "transport", "critical", "Combine the exhaustive subsingleton/nontrivial split, contractivity, abstract theorem, and fixed-projection target.", "Stage1Instances.THM_M_1054.root_of_nontrivialMeanErgodicPackage", "The exact root conditional only on the nontrivial package."),
    ("X-SOURCE", "terminal", "high", "Map every mathematical transition to reviewed primary-source pages, hypotheses, conventions, and errata.", "non-machine node-specific source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory the wrapper, terminal mathlib body, imports, axioms, TCB edges, and replay receipts without alias inflation.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-C-KOOPMAN", f"{PREFIX}-L-CONTRACTION", f"{PREFIX}-B-SUBSINGLETON", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:4e5c59cd94c7ec79e12a1f6d97f339f501a0c154a1e45740e42f4561588f0cae"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1054/ObligationTree.lean#root_of_nontrivialMeanErgodicPackage" if suffix == "T-ASSEMBLE" else None,
    })
    machine_debt = "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4")
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": machine_debt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/allowed-profile-review-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 60 if suffix in {"L-ABSTRACT-MEAN-ERGODIC", "T-FIXED-PROJECTION"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1054/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root proof credit.",
        "task_ids": [ITEM, "S56-M-1054-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1054/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1054 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; Koopman/contraction/branch/abstract-mean-ergodic architecture; eligibility frozen independently of candidate closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": oids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"locally_checked_interfaces": sorted(checked), "anchor_candidate": "M1054-A-MATHLIB-EXACT", "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; anchor availability is not proof-node credit, and no H0/R0/audit/theorem completion is claimed.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-B-SUBSINGLETON", f"{PREFIX}-B-NONTRIVIAL", f"{PREFIX}-T-FIXED-PROJECTION"],
    f"{PREFIX}-B-NONTRIVIAL": [f"{PREFIX}-L-CONTRACTION", f"{PREFIX}-L-ABSTRACT-MEAN-ERGODIC"],
    f"{PREFIX}-L-CONTRACTION": [f"{PREFIX}-C-KOOPMAN"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-ANCHOR", f"{PREFIX}-L-ABSTRACT-MEAN-ERGODIC", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-ABSTRACT-MEAN-ERGODIC")],
    "workflow": [edge("FLOW-ASSEMBLE-ABSTRACT", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-L-ABSTRACT-MEAN-ERGODIC"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"locally_checked_interfaces": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-L-ABSTRACT-MEAN-ERGODIC"], "composition_certificates": ["Stage1Instances.THM_M_1054.root_of_nontrivialMeanErgodicPackage"], "reason": "Composition is conditional and the audited mathlib candidate receives no proof-node credit in this phase."},
}

recipes = []
for oid in oids:
    recipes.append({
        "recipe_id": f"VAL-{oid}", "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-1054/check_obligation_tree.py"],
        "env_allowlist": {"PYTHONHASHSEED": "0"}, "timeout_seconds": 120,
        "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact-pass-prefix-and-registry-digest"}],
        "covered_obligation_ids": [oid], "covered_declarations": [],
    })
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
state = {
    "schema_version": "stage1-obligation-state/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "base_revision": "ff4e83f798358bf80798541f0b3f627121e1e617",
    "registry_hash": "sha256:" + denominator, "registry_version": 1,
    "state": "self_tested_pending_master_acceptance", "root_vector": {"H": "H1", "M": "M3", "R": "R3"},
    "audit_complete": False, "theorem_complete": False,
    "status_boundary": "Only the obligation-tree phase is self-tested. The exact root remains open and every proof, source, readability, release, and master-acceptance gate remains pending.",
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs), ("obligation-tree-state.json", state)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
