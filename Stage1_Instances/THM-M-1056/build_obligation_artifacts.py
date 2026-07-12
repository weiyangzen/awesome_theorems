#!/usr/bin/env python3
"""Build the frozen THM-M-1056 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1056-OBLIGATION_TREE"
THEOREM = "THM-M-1056"
PREFIX = "M1056"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen invertible finite-dimensional real Oseledets target.", "Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget", "The canonical proposition."),
    ("S-INTERFACE", "definition", "critical", "Freeze cocycle iteration, logPlus, measurable equivalence, finite-dimensional fiber, and projection-valued splitting conventions.", "Stage1Instances.THM_M_1056.{cocycleVector,logPlus,LyapunovSplitting}", "The exact elaborated vocabulary and binder context."),
    ("S-BOUNDARY", "branch", "high", "Handle positive fiber dimension, exclusion of zero vectors, repeated exponent blocks, one common conull set, and null-set invariance.", "planned exact boundary lemmas for LyapunovSplitting", "All degenerate and almost-everywhere cases required by the target."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, measurable selection, quotient/extensionality principles, imports, and the no-oracle policy.", "planned transitive axiom and TCB certificate", "An accepted foundation profile for every terminal body."),
    ("N-ITERATES", "normalization", "high", "Relate cocycleVector to forward products and derive the cocycle law used by all asymptotic estimates.", "planned iterate/product normalization declarations", "Canonical forward cocycle iterates with product and norm identities."),
    ("N-COORDINATES", "transport", "critical", "Transport the arbitrary finite-dimensional normed real fiber to a measurable Euclidean coordinate model without changing growth rates.", "planned basis/measurability/norm-equivalence transport", "A checked bridge between the canonical polymorphic fiber and a matrix cocycle."),
    ("L-SUBADDITIVE", "core_lemma", "critical", "Establish the integrable subadditive exterior-power processes controlling singular-value growth.", "planned exterior-power subadditivity theorem", "Integrable subadditive processes for every exterior degree."),
    ("L-KINGMAN", "bridge", "critical", "Apply a fully audited subadditive ergodic theorem to obtain almost-sure deterministic exterior-power growth limits.", "planned Kingman bridge (absent from pinned mathlib)", "Almost-sure deterministic sums of Lyapunov exponents."),
    ("C-FORWARD-FLAG", "construction", "critical", "Construct a strongly measurable forward Oseledets filtration with dimensions, invariance, and growth characterization.", "planned measurable forward filtration construction", "The complete forward flag and its invariants."),
    ("C-BACKWARD-FLAG", "construction", "critical", "Apply the inverse cocycle over the inverse base to construct the compatible backward filtration.", "planned inverse-cocycle filtration construction", "The complete backward flag and its invariants."),
    ("L-TRANSVERSAL", "core_lemma", "critical", "Prove forward and backward flags are almost surely transverse and their intersections have the required dimensions.", "planned transversality and dimension theorem", "Nonzero invariant Lyapunov subspaces forming a direct sum."),
    ("C-PROJECTIONS", "construction", "critical", "Turn the transverse measurable subspaces into strongly measurable complementary continuous projections.", "planned measurable projection construction", "Idempotent, disjoint, nonzero projections summing to identity."),
    ("L-EQUIVARIANCE", "core_lemma", "critical", "Prove the constructed splitting is equivariant under the one-step cocycle on a common invariant conull set.", "planned projection intertwining theorem", "The equivariance field of LyapunovSplitting."),
    ("L-GROWTH", "core_lemma", "critical", "Prove the normalized logarithmic norm limit for every nonzero vector in every projected subspace, simultaneously on one conull set.", "planned vector growth theorem", "The growth field of LyapunovSplitting."),
    ("T-CORE", "terminal", "critical", "Assemble exponents, projections, measurability, algebraic splitting, equivariance, and growth into Nonempty LyapunovSplitting.", "Stage1Instances.THM_M_1056.OseledetsCorePackage", "The complete still-open analytic package."),
    ("T-ASSEMBLE", "transport", "high", "Compose the exact Oseledets core package into the canonical target without weakening any binder or hypothesis.", "Stage1Instances.THM_M_1056.root_of_oseledetsCorePackage", "The exact root conditional on T-CORE."),
    ("X-EXTERNAL", "bridge", "critical", "Integrate or reprove the pinned external matrix splitting anchor and check every coordinate/projection mismatch.", "ErgodicTheory.oseledets_splitting@ed3fa6b8a30594eeb791160563942ba115581aa0 (not imported)", "A dependency-compatible exact bridge, currently absent."),
    ("X-SOURCE", "terminal", "high", "Map every analytic transition to primary-source theorem/page, assumptions, conventions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory every terminal body, wrapper, imported revision, axiom, TCB edge, and replay receipt.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-INTERFACE", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-INTERFACE", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:8e1a96a304ce3dd43838f934406d58ac3594b9d34c6e1617461abc17e65d403b"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fp = statement_fp if suffix in {"ROOT", "S-INTERFACE"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1056/ObligationTree.lean#root_of_oseledetsCorePackage" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else ("external-anchor-audit-record" if suffix == "X-EXTERNAL" else "none"),
        "foundation_profile": "lean4-mathlib-measure-theory/classical-and-measurable-selection-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if suffix in {"L-KINGMAN", "C-FORWARD-FLAG", "C-BACKWARD-FLAG", "L-TRANSVERSAL", "L-GROWTH"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1056/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1056-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1056/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1056 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus immutable anchor audit; exterior-power, two-sided-filtration, transversality, and measurable-projection architecture selected independently of closure.",
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
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Oseledets proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-CORE"],
    f"{PREFIX}-T-CORE": [f"{PREFIX}-C-PROJECTIONS", f"{PREFIX}-L-EQUIVARIANCE", f"{PREFIX}-L-GROWTH"],
    f"{PREFIX}-C-PROJECTIONS": [f"{PREFIX}-L-TRANSVERSAL"],
    f"{PREFIX}-L-EQUIVARIANCE": [f"{PREFIX}-C-FORWARD-FLAG", f"{PREFIX}-C-BACKWARD-FLAG"],
    f"{PREFIX}-L-GROWTH": [f"{PREFIX}-C-FORWARD-FLAG", f"{PREFIX}-C-BACKWARD-FLAG", f"{PREFIX}-L-KINGMAN"],
    f"{PREFIX}-L-TRANSVERSAL": [f"{PREFIX}-C-FORWARD-FLAG", f"{PREFIX}-C-BACKWARD-FLAG"],
    f"{PREFIX}-C-FORWARD-FLAG": [f"{PREFIX}-L-KINGMAN", f"{PREFIX}-N-COORDINATES"],
    f"{PREFIX}-C-BACKWARD-FLAG": [f"{PREFIX}-L-KINGMAN", f"{PREFIX}-N-COORDINATES"],
    f"{PREFIX}-L-KINGMAN": [f"{PREFIX}-L-SUBADDITIVE"],
    f"{PREFIX}-L-SUBADDITIVE": [f"{PREFIX}-N-ITERATES"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-INTERFACE", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-INTERFACE"), edge("REF-ROOT-BOUNDARY", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-CORE", f"{PREFIX}-T-CORE", "source_map", f"{PREFIX}-X-SOURCE"), edge("EXT-COORD", f"{PREFIX}-N-COORDINATES", "source_map", f"{PREFIX}-X-EXTERNAL"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-INTERFACE", f"{PREFIX}-S-INTERFACE", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-T-CORE")],
    "workflow": [edge("FLOW-ASSEMBLE-CORE", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-CORE"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-CORE"], "composition_certificates": ["Stage1Instances.THM_M_1056.root_of_oseledetsCorePackage"], "reason": "Final composition is conditional; the complete analytic Oseledets package has no proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

intake_path = HERE / "intake.json"
intake = json.loads(intake_path.read_text())
intake["obligation_registry_hash"] = "sha256:" + denominator
intake["obligation_registry_version"] = 1
intake["obligation_tree_state"] = "self_tested_pending_master_acceptance"
intake["status_boundary"] = "Exact statement and obligation architecture are self-tested pending master acceptance. Root remains H1/M3/R3; no Oseledets proof, H0 source fidelity, audit completion, or theorem completion is claimed."
intake_path.write_text(json.dumps(intake, indent=2, ensure_ascii=True) + "\n")
print(denominator)
