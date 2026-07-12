#!/usr/bin/env python3
"""Build the frozen THM-M-1245 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1245-OBLIGATION_TREE"
THEOREM = "THM-M-1245"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1245-ROOT", "root", "critical", "The exact frozen compact-support Euclidean Sobolev inequality.", "Stage1Instances.THM_M_1245.SobolevInequalityTarget", "The canonical proposition."),
    ("M1245-S-STATEMENT", "definition", "high", "Preserve dimensions, exponents, binder order, compact support, C1 regularity, volume, and the uniform constant.", "Stage1Instances.THM_M_1245.sobolevInequalityTarget_iff_expanded", "The checked canonical statement interface."),
    ("M1245-B-FINRANK", "bridge", "high", "Identify the real finrank of EuclideanSpace Real (Fin n) with n and transport positivity.", "by simpa using hn : 0 < Module.finrank Real (EuclideanSpace Real (Fin n))", "The positive-finrank hypothesis required by the anchor."),
    ("M1245-B-EXPONENT", "bridge", "high", "Transport the frozen inverse-exponent equation across the Euclidean finrank identity.", "AnchorAudit.lean#hconj", "The terminal anchor's exact conjugacy hypothesis."),
    ("M1245-A-TERMINAL", "terminal", "critical", "Instantiate the pinned mathlib inner-product Sobolev theorem for scalar-valued compactly supported C1 functions.", "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner", "The required inequality with mathlib's uniform explicit constant."),
    ("M1245-T-WITNESS", "transport", "high", "Use the terminal theorem's constant as the existential witness outside the function binder.", "Stage1Instances.THM_M_1245.root_of_audited_terminal_estimate", "The exact canonical root, conditional only on the terminal estimate."),
    ("M1245-X-SOURCE", "source_boundary", "high", "Map the norm, derivative, endpoint, compact-support, and constant conventions to reviewed primary-source passages.", "non-machine primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M1245-X-TRUST", "certificate", "critical", "Audit terminal transitive proof bodies, axioms, imports, TCB, and no-oracle policy.", "planned trust-closure evidence", "Accepted trust boundary."),
    ("M1245-X-PROVENANCE", "certificate", "critical", "Bind immutable source revisions, terminal bodies, wrappers, validation recipes, and replay evidence.", "planned machine-derived provenance closure", "Release provenance coverage without mathematical proof credit."),
]

checked = {"M1245-S-STATEMENT", "M1245-B-FINRANK", "M1245-B-EXPONENT", "M1245-T-WITNESS"}
source_required = {"M1245-ROOT", "M1245-A-TERMINAL", "M1245-T-WITNESS", "M1245-X-SOURCE"}
machine_special = {"M1245-X-SOURCE": "not_applicable", "M1245-X-PROVENANCE": "informational"}
root_fp = "lean-expression-sha256:de06a2c7b1515429a72b45e2c3042fff34d75cc97f778af4a98eb320d6125e80"

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = root_fp if oid in {"M1245-ROOT", "M1245-S-STATEMENT"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "required" if oid in source_required else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "mathlib:8a178386ffc0f5fef0b77738bb5449d50efeea95#MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner" if oid == "M1245-A-TERMINAL" else ("local:Stage1_Instances/THM-M-1245/ObligationTree.lean#root_of_audited_terminal_estimate" if oid == "M1245-T-WITNESS" else None),
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M1245-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M1" if oid in {"M1245-ROOT", "M1245-A-TERMINAL"} else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid in source_required else "not-applicable",
        "provenance_id": "pinned-mathlib-anchor-audit" if oid == "M1245-A-TERMINAL" else ("local-conditional-composition" if oid == "M1245-T-WITNESS" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation supplies proof credit",
        "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only the typed proof-requirement children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parent or support edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1245/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise or root proof is supplied.",
        "task_ids": [ITEM, "S56-M-1245-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1245/ObligationTree.lean"] if oid == "M1245-T-WITNESS" else [],
        "owner": "THM-M-1245 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus immutable pinned-anchor audit; direct finrank, exponent, terminal-anchor, and existential-witness architecture; eligibility assigned before proof integration.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1245-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1245-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M1"},
    "status_boundary": "Frozen denominators and checked conditional composition only; the proof node must install the named terminal wrapper. No H0, M0 root, R0, audit completion, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1245-ROOT": ["M1245-T-WITNESS"],
    "M1245-T-WITNESS": ["M1245-A-TERMINAL"],
    "M1245-A-TERMINAL": ["M1245-B-FINRANK", "M1245-B-EXPONENT"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-STMT", "M1245-ROOT", "logical_decomposition", "M1245-S-STATEMENT")],
    "provenance": [edge("SRC-ANCHOR", "M1245-A-TERMINAL", "source_map", "M1245-X-SOURCE"), edge("PROV-ROOT", "M1245-X-PROVENANCE", "provenance_of", "M1245-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M1245-ROOT", "trusts", "M1245-X-TRUST"), edge("TRUST-PROV", "M1245-ROOT", "trusts", "M1245-X-PROVENANCE")],
    "documentation": [edge("DOC-STMT", "M1245-S-STATEMENT", "documents", "M1245-ROOT"), edge("DOC-SOURCE", "M1245-X-SOURCE", "documents", "M1245-A-TERMINAL")],
    "workflow": [edge("FLOW-WITNESS-ANCHOR", "M1245-T-WITNESS", "workflow_depends_on", "M1245-A-TERMINAL"), edge("FLOW-ANCHOR-FIN", "M1245-A-TERMINAL", "workflow_depends_on", "M1245-B-FINRANK"), edge("FLOW-ANCHOR-EXP", "M1245-A-TERMINAL", "workflow_depends_on", "M1245-B-EXPONENT"), edge("FLOW-PROV-WITNESS", "M1245-X-PROVENANCE", "workflow_depends_on", "M1245-T-WITNESS")],
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
    "registry_id": "THM-M-1245-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1245-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1245-A-TERMINAL"], "composition_certificates": ["Stage1Instances.THM_M_1245.root_of_audited_terminal_estimate"], "reason": "The terminal mathlib candidate is applicability-checked but the proof phase has not installed and validated a named root-relevant proof body."}
}

specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1245/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid, *_ in rows]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
