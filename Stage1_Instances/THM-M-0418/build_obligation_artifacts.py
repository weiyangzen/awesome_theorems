#!/usr/bin/env python3
"""Build the frozen THM-M-0418 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0418-OBLIGATION_TREE"
THEOREM = "THM-M-0418"


def digest(value):
    wire = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(wire).hexdigest()


# This inventory follows the terminal proof body in pinned ClassNumber.lean:77-100.
# Status is deliberately assigned only after the denominator below is computed.
rows = [
    ("M0418-ROOT", "root", "critical", "The exact frozen representative-form Minkowski bound for every ideal class.", "Stage1Instances.THM_M_0418.MinkowskiIdealClassBound", "The canonical proposition."),
    ("M0418-S-TARGET", "definition", "high", "Fix the nonzero integral-ideal subtype, class orientation, weak endpoint, and explicit real constant.", "Stage1Instances.THM_M_0418.{MinkowskiIdealClassBound,PinnedMathlibSourceShape}", "The checked exact target interface."),
    ("M0418-S-BOUNDARY", "terminal", "normal", "Retain degree-one, totally real, zero-complex-place, and endpoint-equality cases without extra hypotheses.", "checked by the literal statement transport and canonical binder inventory", "No degenerate case is silently excluded."),
    ("M0418-S-FOUNDATION", "certificate", "critical", "Account for classical choice, quotient soundness, propositional extensionality, the Lean kernel, and the pinned dependency closure.", "#print axioms NumberField.exists_ideal_in_class_of_norm_le", "The provisional foundation and trust boundary."),
    ("M0418-N-INVERSE-CLASS", "normalization", "high", "Choose a fractional ideal representative J of the inverse class C^-1.", "ClassGroup.mk0_surjective C⁻¹", "J with ClassGroup.mk0 J = C^-1."),
    ("M0418-L-MINKOWSKI-ELEMENT", "core_lemma", "critical", "Apply the geometry-of-numbers estimate to obtain a nonzero a in J with controlled norm.", "NumberField.exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr", "A nonzero a in J and the Minkowski norm inequality."),
    ("M0418-C-QUOTIENT-IDEAL", "construction", "high", "Extract an integral ideal I0 satisfying J * I0 = span(a) from membership a in J.", "dvd_iff_le.mpr combined with span_singleton_le_iff_mem", "An integral ideal I0 and the principal-product identity."),
    ("M0418-C-NONZERO-IDEAL", "construction", "high", "Prove I0 is nonzero and package it in the nonZeroDivisors subtype.", "the local `have : I₀ ≠ 0` and `let I` in ClassNumber.lean:84-89", "I : (Ideal (RingOfIntegers K))^0."),
    ("M0418-L-CLASS-IDENTITY", "lemma", "high", "Use the principal-product identity to show the constructed ideal represents C, undoing the inverse normalization.", "ClassGroup.mk0_eq_mk0_inv_iff", "ClassGroup.mk0 I = C."),
    ("M0418-L-NORM-TRANSPORT", "lemma", "critical", "Rewrite the fractional-ideal estimate to absNorm I and cancel the positive norm of J.", "FractionalIdeal.absNorm_span_singleton and NumberField.absNorm_ne_zero_of_nonZeroDivisors", "absNorm I is at most the explicit Minkowski constant."),
    ("M0418-T-UPSTREAM-BODY", "terminal", "critical", "Compose inverse-class choice, the Minkowski element, ideal construction, class identity, and norm transport.", "NumberField.exists_ideal_in_class_of_norm_le", "The literal pinned source proposition."),
    ("M0418-T-ADAPTER", "transport", "high", "Apply the pinned terminal declaration at every canonical binder without changing its type.", "Stage1Instances.THM_M_0418.minkowskiIdealClassBound_mathlibAnchor", "The exact frozen root proposition."),
    ("M0418-X-SOURCE", "terminal", "high", "Map each mathematical step to a reviewed primary human source with edition, page, assumptions, and errata.", "pending node-specific primary-source crosswalk", "Human-source coverage only."),
    ("M0418-X-PROVENANCE", "certificate", "critical", "Bind the wrapper, terminal body, direct body dependencies, source hashes, axioms, and replay evidence.", "anchor-audit.json candidate M0418-C01", "Proof-body provenance without duplicate proof credit."),
]

source_na = {"M0418-S-TARGET", "M0418-S-BOUNDARY", "M0418-S-FOUNDATION", "M0418-X-PROVENANCE"}
machine_special = {"M0418-X-SOURCE": "not_applicable", "M0418-X-PROVENANCE": "informational"}
obligations = []
for oid, kind, risk, claim, target, output in rows:
    if oid in {"M0418-ROOT", "M0418-S-TARGET", "M0418-T-ADAPTER"}:
        fingerprint = "lean-expression-sha256:d47f228d8edd29ddabc2cc6189f476d231e1a49870e134db0b83095cd3db1081"
    else:
        fingerprint = "source-step:v1:sha256:" + digest([oid, kind, claim, target, output])
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
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": "mathlib:8a178386:Mathlib.NumberTheory.NumberField.ClassNumber#NumberField.exists_ideal_in_class_of_norm_le" if oid == "M0418-T-UPSTREAM-BODY" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "registry_id": "THM-M-0418-OBLIGATIONS-v1",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus the bounded immutable anchor inventory; architecture follows the pinned terminal body before closure metrics are recorded.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0418-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0418-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {
        "closed_machine_obligations": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "root_machine_debt": "M0-W",
        "human_source_debt": "H1",
        "readability_debt": "R2",
    },
    "status_boundary": "The pinned mathlib body closes the machine route, but primary human-source acceptance, R0 reconstruction, release validation, and theorem completion remain open.",
}

closed = set(registry["status_observed_after_freeze"]["closed_machine_obligations"])
nodes = []
for oid, kind, risk, claim, target, output in rows:
    machine = next(row["machine_eligibility"] for row in obligations if row["obligation_id"] == oid)
    nodes.append({
        "node_id": "THM-M-0418-" + oid.removeprefix("M0418-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": "H1" if oid not in source_na else "H2",
        "machine_debt": "M0-W" if oid in closed else "M4",
        "readability_debt": "R2" if oid != "M0418-X-SOURCE" else "R3",
        "evidence_ids": ["M0418-C01"] if oid in closed else [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "M0418-C01-terminal-body" if oid in closed else "none",
        "foundation_profile": "Lean4-mathlib-classical: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive release closure pending",
        "computation_record": "none; no computation or oracle closes this node",
        "step_budget": 55 if oid in {"M0418-L-MINKOWSKI-ELEMENT", "M0418-L-NORM-TRANSPORT"} else 30,
        "semantic_step_ledger": {
            "premises": "The exact formal context and incoming proof_requires children only.",
            "inference": claim,
            "output": output,
            "outgoing_use": "Only declared typed proof composition or non-proof support edges may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0418/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Machine status is inherited from the single audited upstream terminal body; this node supplies no independent body credit and no theorem-completion claim.",
        "task_ids": [ITEM, "S56-M-0418-PROOF", "S56-M-0418-VALIDATION"],
        "owned_sources": ["Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/NumberField/ClassNumber.lean"] if oid in closed else [],
        "owner": "THM-M-0418 execution lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in closed else None, "review_due": "before release", "invalidation_inputs": ["statement hash", "registry hash", "mathlib revision", "terminal body"], "revocation_state": "provisional" if oid in closed else "open"},
    })


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0418-ROOT": ["M0418-T-ADAPTER"],
    "M0418-T-ADAPTER": ["M0418-T-UPSTREAM-BODY"],
    "M0418-T-UPSTREAM-BODY": ["M0418-N-INVERSE-CLASS", "M0418-L-MINKOWSKI-ELEMENT", "M0418-C-QUOTIENT-IDEAL", "M0418-C-NONZERO-IDEAL", "M0418-L-CLASS-IDENTITY", "M0418-L-NORM-TRANSPORT"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-TARGET", "M0418-ROOT", "logical_decomposition", "M0418-S-TARGET"), edge("REF-BOUNDARY", "M0418-ROOT", "logical_decomposition", "M0418-S-BOUNDARY")],
    "provenance": [edge("PROV-BODY", "M0418-X-PROVENANCE", "provenance_of", "M0418-T-UPSTREAM-BODY"), edge("SRC-ROOT", "M0418-ROOT", "source_map", "M0418-X-SOURCE")],
    "evidence": [edge("EVID-BODY", "M0418-X-PROVENANCE", "evidence_for", "M0418-T-UPSTREAM-BODY")],
    "trust": [edge("TRUST-ROOT", "M0418-ROOT", "trusts", "M0418-S-FOUNDATION"), edge("TRUST-PROV", "M0418-ROOT", "trusts", "M0418-X-PROVENANCE")],
    "documentation": [edge("DOC-TARGET", "M0418-S-TARGET", "documents", "M0418-ROOT"), edge("DOC-SOURCE", "M0418-X-SOURCE", "documents", "M0418-T-UPSTREAM-BODY")],
    "workflow": [edge("FLOW-PROOF", "M0418-T-ADAPTER", "workflow_depends_on", "M0418-T-UPSTREAM-BODY"), edge("FLOW-VALIDATE", "M0418-X-PROVENANCE", "workflow_depends_on", "M0418-T-ADAPTER"), edge("FLOW-SOURCE", "M0418-ROOT", "workflow_depends_on", "M0418-X-SOURCE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": registry["registry_id"],
    "registry_denominator_sha256": denominator,
    "root_node_id": "M0418-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": True,
        "root_machine_debt": "M0-W",
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": [],
        "remaining_release_cut_set": ["M0418-X-SOURCE", "R0 reconstruction", "hermetic and independent validation"],
        "composition_certificates": ["NumberField.exists_ideal_in_class_of_norm_le", "Stage1Instances.THM_M_0418.minkowskiIdealClassBound_mathlibAnchor"],
        "distinct_terminal_proof_bodies": ["mathlib:8a178386:Mathlib.NumberTheory.NumberField.ClassNumber#NumberField.exists_ideal_in_class_of_norm_le"],
    },
}

recipes = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [{
        "recipe_id": "VAL-" + oid,
        "obligation_id": oid,
        "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0418/check_obligation_tree.py"],
        "env": {},
        "timeout_seconds": 30,
        "network": "denied",
        "covered_ids": [oid],
        "expected_exit": 0,
    } for oid in ids],
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

instance = json.loads((HERE / "instance.json").read_text())
assert instance["obligation_registry_hash"] == "sha256:" + denominator
print(denominator)
