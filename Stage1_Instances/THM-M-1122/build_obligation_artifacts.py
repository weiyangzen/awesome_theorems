#!/usr/bin/env python3
"""Build the frozen THM-M-1122 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1122-OBLIGATION_TREE"
THEOREM = "THM-M-1122"

rows = [
    ("M1122-ROOT", "root", "critical", "required", "required", "required"),
    ("M1122-S-INTERFACES", "definition", "critical", "required", "required", "required"),
    ("M1122-S-FOUNDATION", "certificate", "critical", "required", "not_applicable", "required"),
    ("M1122-C-CONJECTURE", "source_boundary", "critical", "required", "required", "required"),
    ("M1122-C-LERW", "construction", "critical", "required", "required", "required"),
    ("M1122-C-BROWNIAN", "construction", "critical", "required", "required", "required"),
    ("M1122-C-LOEWNER", "construction", "critical", "required", "required", "required"),
    ("M1122-L-IDENTIFICATION", "core_lemma", "critical", "required", "required", "required"),
    ("M1122-T-ASSEMBLE", "transport", "high", "required", "required", "required"),
    ("M1122-X-SOURCE", "certificate", "high", "not_applicable", "required", "required"),
    ("M1122-X-PROVENANCE", "certificate", "critical", "informational", "not_applicable", "required"),
]

descriptions = {
    "M1122-ROOT": ("The exact conditional Schramm (2000), Theorem 1.3 target.", "The canonical proposition."),
    "M1122-S-INTERFACES": ("Give faithful measurable curve, LERW limit, circle Brownian, and radial Loewner interfaces.", "Definitions matching the source objects rather than opaque predicates."),
    "M1122-S-FOUNDATION": ("Freeze axioms, choice, TCB, imports, and no-oracle policy.", "An accepted trust boundary."),
    "M1122-C-CONJECTURE": ("Formalize Conjecture 1.2 with its topology, convergence mode, and quantifiers.", "A typed hypothesis capable of supporting Theorem 1.3."),
    "M1122-C-LERW": ("Construct the measurable LERW scaling-limit random curve from 0 to the unit-circle boundary.", "The target law and its measurability certificate."),
    "M1122-C-BROWNIAN": ("Construct circle Brownian motion with uniform initial law and the source variance convention.", "A measurable driver B with the required law."),
    "M1122-C-LOEWNER": ("Construct the normalized radial Loewner trace solving (1.1)-(1.3), including the terminal point.", "A measurable trace sigma driven by B(-2t)."),
    "M1122-L-IDENTIFICATION": ("Prove that Conjecture 1.2 identifies every specified Loewner trace law with the LERW limit law.", "ConditionalIdentification, hence the equality-in-distribution conclusion."),
    "M1122-T-ASSEMBLE": ("Transport ConditionalIdentification to the definitionally equal canonical root.", "The exact canonical proposition, conditional on the core package."),
    "M1122-X-SOURCE": ("Map every semantic node to theorem/page/equation/assumption/errata evidence.", "Accepted H-side node crosswalk."),
    "M1122-X-PROVENANCE": ("Resolve terminal bodies, imports, axioms, licenses, receipts, and replay inputs.", "Accepted provenance and evidence closure."),
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

obligations = []
for oid, kind, risk, machine, human, readable in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + sha((oid + ":" + descriptions[oid][0]).encode()),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-1122/ObligationTree.lean#root_of_conditionalIdentification" if oid == "M1122-T-ASSEMBLE" else None),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
digest = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact selected statement plus immutable anchor audit; source-faithful SLE architecture frozen independently of closure.",
    "frozen_against_statement_sha256": sha((HERE / "Statement.lean").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": "M1122-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1122-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1122-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope only. Opaque statement parameters and conditional composition provide no proof of Schramm's identification theorem."
}

nodes = []
for oid, kind, *_ in rows:
    statement, output = descriptions[oid]
    checked = oid == "M1122-T-ASSEMBLE"
    nodes.append({
        "node_id": "THM-M-1122-" + oid.removeprefix("M1122-"), "obligation_id": oid, "kind": kind,
        "human_statement": statement,
        "formal_target": ({"M1122-ROOT": "Stage1Instances.THM_M_1122.SchrammLoewnerEvolutionTarget", "M1122-L-IDENTIFICATION": "Stage1Instances.THM_M_1122.ConditionalIdentification", "M1122-T-ASSEMBLE": "Stage1Instances.THM_M_1122.root_of_conditionalIdentification"}.get(oid, "planned exact Lean declaration")),
        "output": output, "human_debt": "H2", "machine_debt": "M0-L" if checked else ("M3" if oid == "M1122-ROOT" else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md", "provenance_id": "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; numerical SLE simulations receive no proof credit", "step_budget": 100 if oid == "M1122-L-IDENTIFICATION" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof children and the frozen formal context.", "inference": statement, "output": output, "outgoing_use": "Only the declared typed parent or support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1122/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no unlisted premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1122-PROOF"], "owned_sources": [], "owner": "THM-M-1122 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"},
    })

proof_pairs = [("M1122-ROOT", "M1122-T-ASSEMBLE"), ("M1122-T-ASSEMBLE", "M1122-L-IDENTIFICATION")]
graphs = {name: {"edges": [], "out": {}, "in": {}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def edge(graph, eid, src, typ, dst, reciprocal=None):
    e = {"edge_id": eid, "from": src, "type": typ, "to": dst}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e); graphs[graph]["out"].setdefault(src, []).append(eid); graphs[graph]["in"].setdefault(dst, []).append(eid)
for i, (parent, child) in enumerate(proof_pairs, 1):
    edge("proof", f"P{i}-REQ", parent, "proof_requires", child, f"P{i}-COMP")
    edge("proof", f"P{i}-COMP", child, "composes", parent, f"P{i}-REQ")
for i, child in enumerate(("M1122-S-INTERFACES", "M1122-C-CONJECTURE", "M1122-C-LERW", "M1122-C-BROWNIAN", "M1122-C-LOEWNER"), 1):
    edge("refinement", f"R{i}", "M1122-L-IDENTIFICATION", "logical_decomposition", child)
edge("provenance", "PROV1", "M1122-X-PROVENANCE", "provenance_of", "M1122-T-ASSEMBLE")
edge("evidence", "EVID1", "M1122-X-PROVENANCE", "provenance_of", "M1122-ROOT")
edge("trust", "TRUST1", "M1122-ROOT", "trusts", "M1122-S-FOUNDATION")
edge("documentation", "DOC1", "M1122-X-SOURCE", "documents", "M1122-L-IDENTIFICATION")
for i, child in enumerate(("M1122-L-IDENTIFICATION", "M1122-C-CONJECTURE", "M1122-C-LERW", "M1122-C-BROWNIAN", "M1122-C-LOEWNER", "M1122-X-PROVENANCE"), 1):
    edge("workflow", f"FLOW{i}", "M1122-T-ASSEMBLE" if i == 1 else "M1122-L-IDENTIFICATION", "workflow_depends_on", child)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1122-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M1122-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M1122-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False,
      "remaining_root_cut_set": ["M1122-L-IDENTIFICATION"], "composition_certificates": ["Stage1Instances.THM_M_1122.root_of_conditionalIdentification"],
      "reason": "The checked assembly consumes the entire substantive conditional identification as an explicit premise."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
  "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1122/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network_policy": "denied", "covered_ids": [oid], "expected_exit": 0} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(digest)
