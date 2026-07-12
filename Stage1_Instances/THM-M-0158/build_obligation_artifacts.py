#!/usr/bin/env python3
"""Build the frozen THM-M-0158 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0158-OBLIGATION_TREE"
THEOREM = "THM-M-0158"
ROOT_FP = "lean-expression-sha256:62594b8173c0478a49cafb93c7f668b9a8a9302e6f2b194ce7d4e6bd0668eb9a"


def planned(text):
    return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()


rows = [
    ("M0158-ROOT", "root", "The exact frozen local-coordinate Weingarten-equations proposition.", "critical", "required", "required", "required", ROOT_FP),
    ("M0158-S-DEFINITIONS", "definition", "Freeze partialWithin, I, II, index order, and scalar-action conventions.", "high", "required", "not_applicable", "required", ROOT_FP),
    ("M0158-S-DOMAIN", "terminal", "Preserve the open-domain, interior-point, C2/C1, unit-normal, orthogonality, and nonsingular-Gram hypotheses.", "high", "required", "required", "required", None),
    ("M0158-S-BOUNDARY", "terminal", "Exclude singular and outside-domain cases and record orientation reversal behavior.", "high", "required", "required", "required", None),
    ("M0158-S-FOUNDATION", "certificate", "Audit classical choice, imports, axioms, TCB, and the no-oracle boundary.", "critical", "required", "not_applicable", "required", None),
    ("M0158-N-WITHIN", "normalization", "Reduce within derivatives at the interior point to ordinary local derivative rules needed for product differentiation.", "critical", "required", "required", "required", None),
    ("M0158-N-SIGN-INDEX", "normalization", "Fix the sign and column convention relating differentiated orthogonality to II k i.", "critical", "required", "required", "required", None),
    ("M0158-L-UNIT", "core_lemma", "Differentiate norm-one to prove each coordinate derivative N_i is orthogonal to N.", "critical", "required", "required", "required", None),
    ("M0158-L-ORTHOG", "core_lemma", "Differentiate inner(N,x_k)=0 to obtain inner(x_k,N_i)=-II k i for every k,i.", "critical", "required", "required", "required", None),
    ("M0158-C-BASIS", "construction", "Use det(I) nonzero to prove x_0,x_1 are independent and, with unit N, form a basis of ambient R3.", "critical", "required", "required", "required", None),
    ("M0158-L-GRAM-SOLVE", "core_lemma", "Use the nonsingular inverse identities to solve I*c_i=-II_i as c_i=-(I^-1*II)_i.", "critical", "required", "required", "required", None),
    ("M0158-T-RECONSTRUCT", "terminal", "Reconstruct N_i from its inner products with the basis N,x_0,x_1 and the solved tangent coefficients.", "critical", "required", "required", "required", None),
    ("M0158-T-ASSEMBLE", "transport", "Discharge the ordered binders and hypotheses and return the exact canonical target from the derivation package.", "high", "required", "required", "required", None),
    ("M0158-X-SOURCE", "terminal", "Map each mathematical leaf to an exact stable human source and convention record.", "high", "not_applicable", "required", "required", None),
    ("M0158-X-PROVENANCE", "certificate", "Record terminal bodies, imports, declaration dependencies, axioms, and replay provenance.", "critical", "informational", "not_applicable", "required", None),
]

obligations = []
for oid, kind, statement, risk, machine, human, readable, fingerprint in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint or planned(statement),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ({"M0158-X-SOURCE": "human_source_boundary_only", "M0158-X-PROVENANCE": "release_provenance_overlay_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0158/ObligationTree.lean#root_of_derivation_package" if oid == "M0158-T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus completed negative exact-anchor audit; differential and Gram-system route selected before proof status inspection.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": "M0158-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": ["M0158-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M0158-S-DEFINITIONS", "M0158-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Architecture and a conditional assembly only; all analytic and linear-algebra proof leaves remain open, so there is no root proof or theorem completion.",
}

node_by_id = {}
for oid, kind, statement, _risk, _machine, human, _readable, _fp in rows:
    closed = oid in ("M0158-S-DEFINITIONS", "M0158-T-ASSEMBLE")
    formal = {
        "M0158-ROOT": "Stage1Instances.THM_M_0158.WeingartenEquationsTarget",
        "M0158-S-DEFINITIONS": "Stage1Instances.THM_M_0158.{partialWithin,firstFundamentalForm,secondFundamentalForm}",
        "M0158-T-ASSEMBLE": "Stage1Instances.THM_M_0158.root_of_derivation_package",
    }.get(oid, "planned exact Lean signature: " + statement)
    node_by_id[oid] = {
        "node_id": "THM-M-0158-" + oid.removeprefix("M0158-"), "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal,
        "output": "The exact claim described by this obligation, usable only along declared proof edges.",
        "human_debt": "H1" if human == "required" else "H3", "machine_debt": "M0-L" if closed else ("M3" if oid == "M0158-ROOT" else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable", "provenance_id": "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node", "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the frozen formal context.", "inference": statement, "output": "The stated node output.", "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0158/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0158-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0158/ObligationTree.lean"] if oid == "M0158-T-ASSEMBLE" else [],
        "owner": "THM-M-0158 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    }

graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}

def edge(graph, eid, typ, src, dst, reciprocal=None):
    value = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal: value["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(value); graphs[graph]["out"][src].append(eid); graphs[graph]["in"][dst].append(eid)

proof_pairs = [
    ("ROOT", "M0158-ROOT", "M0158-T-ASSEMBLE"), ("ASSEMBLE", "M0158-T-ASSEMBLE", "M0158-T-RECONSTRUCT"),
    ("RECON-BASIS", "M0158-T-RECONSTRUCT", "M0158-C-BASIS"), ("RECON-UNIT", "M0158-T-RECONSTRUCT", "M0158-L-UNIT"),
    ("RECON-GRAM", "M0158-T-RECONSTRUCT", "M0158-L-GRAM-SOLVE"), ("GRAM-ORTHOG", "M0158-L-GRAM-SOLVE", "M0158-L-ORTHOG"),
    ("GRAM-SIGN", "M0158-L-GRAM-SOLVE", "M0158-N-SIGN-INDEX"), ("UNIT-WITHIN", "M0158-L-UNIT", "M0158-N-WITHIN"),
    ("ORTHOG-WITHIN", "M0158-L-ORTHOG", "M0158-N-WITHIN"),
]
for label, parent, child in proof_pairs:
    req, comp = "P-" + label + "-REQ", "P-" + label + "-COMP"
    edge("proof", req, "proof_requires", parent, child, comp); edge("proof", comp, "composes", child, parent, req)

for oid in ("M0158-S-DEFINITIONS", "M0158-S-DOMAIN", "M0158-S-BOUNDARY", "M0158-N-WITHIN", "M0158-N-SIGN-INDEX"):
    edge("refinement", "R-" + oid, "logical_decomposition", "M0158-ROOT", oid)
edge("provenance", "PV-ROOT", "provenance_of", "M0158-X-PROVENANCE", "M0158-ROOT")
edge("evidence", "EV-ASSEMBLY", "evidence_for", "M0158-X-PROVENANCE", "M0158-T-ASSEMBLE")
edge("trust", "TR-ROOT", "trusts", "M0158-ROOT", "M0158-S-FOUNDATION")
for oid in ids:
    if oid != "M0158-X-SOURCE": edge("documentation", "D-" + oid, "documents", "M0158-X-SOURCE", oid)
workflow_order = ["M0158-S-DEFINITIONS", "M0158-N-WITHIN", "M0158-L-UNIT", "M0158-L-ORTHOG", "M0158-C-BASIS", "M0158-L-GRAM-SOLVE", "M0158-T-RECONSTRUCT", "M0158-T-ASSEMBLE", "M0158-ROOT"]
for index, (before, after) in enumerate(zip(workflow_order, workflow_order[1:]), 1):
    edge("workflow", f"W-{index:02d}", "workflow_depends_on", after, before)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0158-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0158-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": list(node_by_id.values()), "graphs": graphs,
    "closure_boundary": {"root_closed": False, "minimal_open_root_cut": ["M0158-T-RECONSTRUCT"], "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(digest)
