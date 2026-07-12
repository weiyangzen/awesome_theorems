#!/usr/bin/env python3
"""Build the frozen THM-M-0312 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0312-OBLIGATION_TREE"
THEOREM = "THM-M-0312"


def sha(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0312-ROOT", "root", "critical", "The exact polymorphic semilinear Uniform Boundedness target.", "Stage1Instances.THM_M_0312.UniformBoundednessTarget", "The canonical proposition."),
    ("M0312-S-INTERFACE", "definition", "high", "Fix pointwise and operator-norm boundedness with the original universes, scalar homomorphism, and binder scopes.", "Stage1Instances.THM_M_0312.{PointwiseBounded,UniformlyBounded}", "Exact premise and conclusion interfaces."),
    ("M0312-S-BOUNDARY", "terminal", "normal", "Preserve the empty index family, zero spaces, and the absence of codomain completeness or index nonemptiness.", "Stage1Instances.THM_M_0312.emptyIndexBoundary", "Checked empty-family behavior and frozen remaining boundaries."),
    ("M0312-S-ISUP", "transport", "high", "Relate the real-bound target to the ENNReal iSup formulation in both directions.", "Stage1Instances.THM_M_0312.uniformBoundednessTarget_iff_iSupTarget", "A checked iff without a second terminal proof-body credit."),
    ("M0312-S-FOUNDATION", "certificate", "critical", "Fix the permitted propext, Classical.choice, Quot.sound surface and audit the complete transitive TCB.", "planned foundation and transitive trust report", "Accepted foundation and TCB boundary."),
    ("M0312-B-EQUICONT", "bridge", "critical", "Derive uniform equicontinuity of the family from its pointwise real-norm boundedness.", "PointwiseBounded g -> UniformEquicontinuous ((\u2191) \u2218 g)", "Uniform equicontinuity of the coerced maps."),
    ("M0312-T-NORM-BOUND", "transport", "critical", "Transport uniform equicontinuity back to one common operator-norm bound.", "UniformEquicontinuous ((\u2191) \u2218 g) -> UniformlyBounded g", "The exact root conclusion."),
    ("M0312-T-TFAE", "bridge", "high", "Use the precise directions of NormedSpace.equicontinuous_TFAE connecting uniform equicontinuity, real norm bounds, and ENNReal bounds.", "NormedSpace.equicontinuous_TFAE", "Checked norm/equicontinuity equivalences in the required directions."),
    ("M0312-B-SEMINORM", "reduction", "critical", "Convert pointwise real bounds to boundedness for the singleton norm seminorm family.", "norm_withSeminorms K2 F and bddAbove_def/range conversion", "Pointwise seminorm boundedness required by the general theorem."),
    ("M0312-B-COMPLETE", "bridge", "high", "Supply the barrelled-space instance for the complete seminormed domain through its Baire-space structure.", "BaireSpace.instBarrelledSpace", "BarrelledSpace K E at the exact domain."),
    ("M0312-T-BARRELLED", "terminal", "critical", "Apply the general Banach-Steinhaus theorem for a barrelled domain and a seminorm-generated codomain.", "WithSeminorms.banach_steinhaus", "Uniform equicontinuity from pointwise seminorm boundedness."),
    ("M0312-L-ISUP-CONT", "core_lemma", "critical", "Prove continuity of the pointwise supremum seminorm using barrelledness after establishing its bounded range.", "Seminorm.continuous_iSup", "Continuity of each supremum seminorm."),
    ("M0312-L-COMP-RANGE", "core_lemma", "high", "Lift pointwise boundedness to boundedness of the range of composed seminorms.", "Seminorm.bddAbove_range_iff", "A well-defined supremum in the seminorm lattice."),
    ("M0312-X-SOURCE", "terminal", "high", "Map each analytic bridge and inference to a reviewed primary human source and its assumptions.", "non-machine primary-source node crosswalk", "Human-source coverage only."),
    ("M0312-X-PROVENANCE", "certificate", "critical", "Record wrapper/body identity, imports, declaration dependencies, axioms, hashes, and replay evidence.", "planned machine-derived provenance and trust closure", "Release provenance coverage without proof credit."),
]

interface_checked = {"M0312-S-INTERFACE", "M0312-S-BOUNDARY", "M0312-S-ISUP"}
source_na = {"M0312-S-INTERFACE", "M0312-S-BOUNDARY", "M0312-S-FOUNDATION", "M0312-X-PROVENANCE"}
machine_special = {"M0312-X-SOURCE": "not_applicable", "M0312-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    if oid == "M0312-ROOT":
        fingerprint = "lean-expression-sha256:8d8de4ab21686d451342fe90b92b7d11d8719ae9ce140609ce8ee6f3abd53725"
    else:
        fingerprint = "planned:v1:sha256:" + sha([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    terminal_body = None
    if oid in {"M0312-ROOT", "M0312-B-EQUICONT", "M0312-T-NORM-BOUND"}:
        terminal_body = "mathlib:8a178386:BanachSteinhaus.lean#banach_steinhaus"
    elif oid in {"M0312-T-BARRELLED", "M0312-L-ISUP-CONT", "M0312-L-COMP-RANGE"}:
        terminal_body = "mathlib:8a178386:Barrelled.lean#WithSeminorms.banach_steinhaus"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": terminal_body,
    })
    debt = "M0-L" if oid in interface_checked else ("M0-W_candidate" if terminal_body else "M3")
    nodes.append({
        "node_id": "THM-M-0312-" + oid.removeprefix("M0312-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": debt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "PIN-MATHLIB-BANACH-STEINHAUS" if terminal_body else "none",
        "foundation_profile": "lean4-mathlib-classical/provisional-propext-choice-quot",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, external computation, or certificate is used",
        "step_budget": 60 if risk == "critical" else 30,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires conclusions and the frozen typeclass context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed proof parent or non-proof overlay may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0312/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture, interface, or candidate classification only; no master-accepted proof or release claim.",
        "task_ids": [ITEM, "S56-M-0312-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0312/ObligationTree.lean"] if oid in {"M0312-ROOT", "M0312-B-EQUICONT", "M0312-T-NORM-BOUND"} else [],
        "owner": "THM-M-0312 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in interface_checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "mathlib pin", "source map", "toolchain"], "revocation_state": "provisional" if debt != "M3" else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = sha([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus the source-level decomposition of the pinned candidate; eligibility follows semantic roles and is independent of acceptance status.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0312-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0312-X-PROVENANCE"]},
    "distinct_terminal_proof_body_ids": sorted({o["terminal_proof_body_id"] for o in obligations if o["terminal_proof_body_id"]}),
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"accepted_closed_obligations": [], "candidate_obligations": sorted(o["obligation_id"] for o in obligations if o["terminal_proof_body_id"]), "root_machine_debt": "M0-W_candidate"},
    "status_boundary": "Frozen scope and candidate-aware architecture only; no M0-W acceptance, H0/R0, AUDIT-Z, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0312-ROOT": ["M0312-B-EQUICONT", "M0312-T-NORM-BOUND"],
    "M0312-B-EQUICONT": ["M0312-B-SEMINORM", "M0312-B-COMPLETE", "M0312-T-BARRELLED"],
    "M0312-T-NORM-BOUND": ["M0312-T-TFAE"],
    "M0312-T-BARRELLED": ["M0312-L-ISUP-CONT", "M0312-L-COMP-RANGE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-INTERFACE", "M0312-ROOT", "logical_decomposition", "M0312-S-INTERFACE"), edge("REF-ROOT-BOUNDARY", "M0312-ROOT", "logical_decomposition", "M0312-S-BOUNDARY"), edge("REF-ROOT-ISUP", "M0312-ROOT", "logical_decomposition", "M0312-S-ISUP")],
    "provenance": [edge("SRC-BARRELLED", "M0312-T-BARRELLED", "source_map", "M0312-X-SOURCE"), edge("PROV-ROOT", "M0312-X-PROVENANCE", "provenance_of", "M0312-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0312-ROOT", "trusts", "M0312-S-FOUNDATION"), edge("TRUST-PROV", "M0312-ROOT", "trusts", "M0312-X-PROVENANCE")],
    "documentation": [edge("DOC-INTERFACE", "M0312-S-INTERFACE", "documents", "M0312-ROOT"), edge("DOC-SOURCE", "M0312-X-SOURCE", "documents", "M0312-B-EQUICONT")],
    "workflow": [edge("FLOW-ROOT-EQUICONT", "M0312-ROOT", "workflow_depends_on", "M0312-B-EQUICONT"), edge("FLOW-ROOT-NORM", "M0312-ROOT", "workflow_depends_on", "M0312-T-NORM-BOUND"), edge("FLOW-PROV-BODY", "M0312-X-PROVENANCE", "workflow_depends_on", "M0312-T-BARRELLED")],
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
    "registry_id": "THM-M-0312-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0312-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "accepted_closed_obligations": [], "candidate_obligations": registry["status_observed_after_freeze"]["candidate_obligations"],
        "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0312-B-EQUICONT", "M0312-T-NORM-BOUND", "M0312-S-FOUNDATION", "M0312-X-PROVENANCE", "M0312-X-SOURCE"],
        "composition_certificates": ["Stage1Instances.THM_M_0312.root_of_equicontinuity_packages"],
        "reason": "The exact composition elaborates, but candidate proof bodies and their complete trust/source/readability evidence are not accepted at this phase."
    }
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0312/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
