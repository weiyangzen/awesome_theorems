#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0648-OBLIGATION_TREE"
THEOREM = "THM-M-0648"

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

ROWS = [
    ("M0648-ROOT", "root", "critical", "The exact conjunction of the distinguished-subset downward and elementary-embedding upward Loewenheim-Skolem targets.", "Stage1Instances.THM_M_0648.CanonicalTarget", "The frozen paired proposition."),
    ("M0648-S-EXACT", "definition", "critical", "Preserve all ordered binders, universes, typeclasses, cardinal lifts, containment, exact cardinalities, and embedding orientation.", "Statement.lean definitions", "An exact statement interface."),
    ("M0648-S-BOUNDARY", "branch", "high", "Retain empty A and language, equality bounds, kappa = aleph0, and exclude finite M only in the upward half.", "statement.json degenerate_cases", "The complete boundary policy."),
    ("M0648-D", "bridge", "critical", "Obtain the exact downward target for every distinguished subset and admissible infinite cardinal.", "FirstOrder.Language.exists_elementarySubstructure_card_eq", "DownwardTarget L."),
    ("M0648-D-SKOLEM", "core_lemma", "critical", "Construct and cardinal-control the elementary Skolem hull containing A.", "Mathlib.ModelTheory.Skolem terminal body", "The elementary substructure, containment, and cardinal equality."),
    ("M0648-U", "bridge", "critical", "Obtain the exact upward target with a forward elementary embedding into an exact-size model.", "FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge", "UpwardTarget L."),
    ("M0648-U-DIAGRAM", "construction", "critical", "Form the elementary diagram of M with constants naming its elements.", "Satisfiability.lean upward terminal body", "A theory whose models induce a forward elementary embedding."),
    ("M0648-U-COMPACT", "core_lemma", "critical", "Apply compactness with fresh constants to obtain a sufficiently large model of the elementary diagram.", "Satisfiability.lean compactness route", "An elementary extension with cardinality at least kappa."),
    ("M0648-U-SHRINK", "bridge", "critical", "Apply the downward cardinal wrapper to shrink the diagram model to exact cardinality kappa while retaining named M.", "Satisfiability.lean downward-cardinal wrapper", "An exact-size model and forward elementary embedding."),
    ("M0648-T-COMPOSE", "terminal", "high", "Combine both exact direction packages into the canonical conjunction without an extra premise.", "Stage1Instances.THM_M_0648.ObligationTree.root_compose", "CanonicalTarget L."),
    ("M0648-X-SOURCE", "terminal", "high", "Map every mathematical layer to pinpoint primary sources and checked errata.", "source-statement-crosswalk.md; pinpoint review pending", "Human-source coverage only."),
    ("M0648-X-TRUST", "certificate", "critical", "Audit terminal bodies, imports, axioms, TCB, licenses, and reproducible replay.", "anchor-audit-receipt.json plus future transitive validation", "Trust and provenance coverage without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
root_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit-receipt.json").read_bytes()).hexdigest()
source_na = {"M0648-S-EXACT", "M0648-S-BOUNDARY", "M0648-X-TRUST"}
machine_overlay = {"M0648-X-SOURCE": "not_applicable", "M0648-X-TRUST": "informational"}
terminal_ids = {
    "M0648-D": "mathlib:8a178386:FirstOrder.Language.exists_elementarySubstructure_card_eq",
    "M0648-U": "mathlib:8a178386:FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge",
    "M0648-T-COMPOSE": "local:ObligationTree.lean#root_compose",
}

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in ROWS:
    machine = machine_overlay.get(oid, "required")
    fp = "lean-expression-sha256:" + root_fp if oid in {"M0648-ROOT", "M0648-S-EXACT"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": oid not in {"M0648-X-SOURCE", "M0648-X-TRUST"},
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_overlay_only", "informational": "trust_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": terminal_ids.get(oid)})
    debt = "M1" if oid in {"M0648-D", "M0648-U"} else ("M3" if oid == "M0648-T-COMPOSE" else "M4")
    nodes.append({"node_id": THEOREM + "-" + oid.removeprefix("M0648-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "pinpoint-primary-source-review-pending",
        "provenance_id": "anchor-audit-receipt.json" if oid in {"M0648-D", "M0648-U", "M0648-X-TRUST"} else "none",
        "foundation_profile": "Lean dependent type theory; propext, Classical.choice, Quot.sound observed; acceptance pending",
        "tcb_profile": "Lean 4.29.0 and mathlib 8a178386; transitive release audit pending",
        "computation_record": "none; no computation or oracle is credited",
        "step_budget": 40 if oid not in {"M0648-ROOT", "M0648-U"} else "split-required",
        "semantic_step_ledger": [{"premise_ids": [], "inference": claim, "output": output, "outgoing_use": "only the declared typed parent or support edge"}],
        "public_readable_target": f"Stage1_Instances/THM-M-0648/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture only; this phase credits no proof, source review, readability, validation, or release closure.",
        "task_ids": [ITEM, "S56-M-0648-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0648/ObligationTree.lean"] if oid == "M0648-T-COMPOSE" else [],
        "owner": "THM-M-0648 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "typed edges", "source map", "toolchain", "mathlib revision"], "revocation_state": "open"}})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [o["obligation_id"] for o in obligations]
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "freeze_basis": "Exact elaborated paired statement and immutable anchor audit; eligibility fixed independently of later closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0648-ROOT", "frozen_denominators": {"inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0648-X-SOURCE", "M0648-X-TRUST"]},
    "denominator_sha256": denominator, "delta_policy": "Any target, split, merge, exclusion, risk, or eligibility change requires registry v2 and an append-only old/new ID delta.",
    "append_only_delta": [], "obligations": obligations,
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M4"},
    "status_boundary": "Registry and interfaces only; no theorem or audit completion is claimed."}

def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal: result["reciprocal_edge_id"] = reciprocal
    return result

requires = {"M0648-ROOT": ["M0648-S-EXACT", "M0648-S-BOUNDARY", "M0648-T-COMPOSE"],
    "M0648-T-COMPOSE": ["M0648-D", "M0648-U"], "M0648-D": ["M0648-D-SKOLEM"],
    "M0648-U": ["M0648-U-DIAGRAM", "M0648-U-COMPACT", "M0648-U-SHRINK"],
    "M0648-U-SHRINK": ["M0648-D"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-BOUNDARY", "M0648-ROOT", "logical_decomposition", "M0648-S-BOUNDARY")],
    "provenance": [edge("PROV-D", "M0648-X-TRUST", "provenance_of", "M0648-D"), edge("PROV-U", "M0648-X-TRUST", "provenance_of", "M0648-U"), edge("SRC-D", "M0648-D-SKOLEM", "source_map", "M0648-X-SOURCE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0648-ROOT", "trusts", "M0648-X-TRUST")],
    "documentation": [edge("DOC-SOURCE", "M0648-X-SOURCE", "documents", "M0648-ROOT"), edge("DOC-BOUNDARY", "M0648-S-BOUNDARY", "documents", "M0648-ROOT")],
    "workflow": [edge("FLOW-COMPOSE-D", "M0648-T-COMPOSE", "workflow_depends_on", "M0648-D"), edge("FLOW-COMPOSE-U", "M0648-T-COMPOSE", "workflow_depends_on", "M0648-U"), edge("FLOW-TRUST-U", "M0648-X-TRUST", "workflow_depends_on", "M0648-U")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0648-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0648-ROOT", "edge_direction": "proof requirements parent-to-child; reciprocal composition child-to-parent",
    "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": [], "root_closed": False,
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0648-D-SKOLEM", "M0648-U-DIAGRAM", "M0648-U-COMPACT", "M0648-U-SHRINK"],
        "composition_certificates": ["Stage1Instances.THM_M_0648.ObligationTree.root_compose"],
        "reason": "The checked certificate is conditional and the two anchors remain uncredited until proof/provenance/validation phases."}}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0648/check_obligation_tree.py"],
    "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
    "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}],
    "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THM_M_0648.ObligationTree.root_compose"] if oid == "M0648-T-COMPOSE" else []} for oid, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
