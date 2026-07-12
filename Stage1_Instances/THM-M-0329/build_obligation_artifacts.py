#!/usr/bin/env python3
"""Generate the frozen THM-M-0329 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0329-OBLIGATION_TREE"
THEOREM = "THM-M-0329"

ROWS = [
    ("M0329-ROOT", "root", "Exact real-Hilbert-space variational existence and uniqueness target.", "Stage1Instances.THM_M_0329.LaxMilgramTarget", "critical", "required"),
    ("M0329-T-ASSEMBLE", "transport", "Compose Riesz datum representation and the coercive operator equivalence into the exact root.", "Stage1Instances.THM_M_0329.ObligationTree.root_of_packages", "critical", "required"),
    ("M0329-D-RIESZ", "bridge", "Represent every continuous real functional by inner product with a vector.", "Stage1Instances.THM_M_0329.ObligationTree.RieszPackage", "high", "required"),
    ("M0329-D-ORIENTATION", "transport", "Preserve the convention B u v = F v with the unknown in the first argument.", "checked inner-product and bilinear-form orientation transport", "high", "required"),
    ("M0329-O-EQUIV", "construction", "Construct a continuous linear equivalence from the coercive bilinear operator.", "IsCoercive.continuousLinearEquivOfBilin", "critical", "required"),
    ("M0329-O-APPLY", "lemma", "Identify the equivalence output by inner product: inner (e u) v = B u v.", "IsCoercive.continuousLinearEquivOfBilin_apply", "critical", "required"),
    ("M0329-O-UNIQUE", "lemma", "Use injectivity and inner-product extensionality to prove uniqueness of the solution.", "local adapter uniqueness branch", "high", "required"),
    ("M0329-A-BOUNDED", "lemma", "Derive a positive lower norm bound for the operator from coercivity.", "IsCoercive.bounded_below", "high", "required"),
    ("M0329-A-ANTILIPSCHITZ", "lemma", "Convert the lower norm bound to an antilipschitz estimate.", "IsCoercive.antilipschitz", "high", "required"),
    ("M0329-A-KERNEL", "lemma", "Deduce that the induced operator has trivial kernel.", "IsCoercive.ker_eq_bot", "high", "required"),
    ("M0329-A-CLOSED", "lemma", "Prove the induced operator has closed range.", "IsCoercive.isClosed_range", "high", "required"),
    ("M0329-A-SURJECTIVE", "lemma", "Use orthogonal-complement coercivity to prove the range is all of V.", "IsCoercive.range_eq_top", "critical", "required"),
    ("M0329-C-COERCIVITY", "definition", "Audit the positive coercivity constant and diagonal inequality, including zero-space behavior.", "IsCoercive", "critical", "required"),
    ("M0329-X-SOURCE", "source_boundary", "Crosswalk every substantive proof step to an inspected source and errata record.", "primary-source node map pending", "critical", "not_applicable"),
    ("M0329-X-FOUNDATION", "certificate", "Audit axioms, TCB, imports, and the transitive declaration trust closure.", "Lean/mathlib trust closure pending", "critical", "required"),
    ("M0329-X-PROVENANCE", "certificate", "Bind terminal bodies, immutable revisions, licenses, and validation receipts.", "provenance ledger pending", "critical", "informational"),
    ("M0329-X-WORKFLOW", "workflow", "Enforce statement, anchor, proof, validation, review, and release ordering.", "Stage1 rev-5.6 task lane", "high", "not_applicable"),
]

PROOF_REQUIRES = [
    ("M0329-ROOT", "M0329-T-ASSEMBLE"),
    ("M0329-T-ASSEMBLE", "M0329-D-RIESZ"),
    ("M0329-T-ASSEMBLE", "M0329-D-ORIENTATION"),
    ("M0329-T-ASSEMBLE", "M0329-O-EQUIV"),
    ("M0329-T-ASSEMBLE", "M0329-O-APPLY"),
    ("M0329-T-ASSEMBLE", "M0329-O-UNIQUE"),
    ("M0329-O-EQUIV", "M0329-A-KERNEL"),
    ("M0329-O-EQUIV", "M0329-A-SURJECTIVE"),
    ("M0329-A-KERNEL", "M0329-A-ANTILIPSCHITZ"),
    ("M0329-A-ANTILIPSCHITZ", "M0329-A-BOUNDED"),
    ("M0329-A-BOUNDED", "M0329-C-COERCIVITY"),
    ("M0329-A-SURJECTIVE", "M0329-A-CLOSED"),
    ("M0329-A-CLOSED", "M0329-A-ANTILIPSCHITZ"),
    ("M0329-A-SURJECTIVE", "M0329-C-COERCIVITY"),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, risk, machine in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-source-sha256:" + statement_sha) if oid in {"M0329-ROOT", "M0329-C-COERCIVITY"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in {"M0329-D-ORIENTATION", "M0329-X-FOUNDATION", "M0329-X-PROVENANCE", "M0329-X-WORKFLOW"} else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"M0329-X-SOURCE": "human_source_boundary_only", "M0329-X-PROVENANCE": "release_overlay_no_proof_credit", "M0329-X-WORKFLOW": "workflow_only_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0329/ObligationTree.lean#root_of_packages" if oid == "M0329-T-ASSEMBLE" else ("mathlib:8a178386:" + formal if oid.startswith("M0329-A-") or oid in {"M0329-O-EQUIV", "M0329-O-APPLY"} else None),
    })

ids = [r[0] for r in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated variational statement plus immutable mathlib anchor audit; the Riesz/operator and pinned Lax-Milgram dependency architecture is frozen without granting proof acceptance.",
    "frozen_against_statement_sha256": statement_sha, "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0329-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0329-X-PROVENANCE", "M0329-X-WORKFLOW"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and an append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
candidate_nodes = {"M0329-D-RIESZ", "M0329-D-ORIENTATION", "M0329-O-EQUIV", "M0329-O-APPLY", "M0329-O-UNIQUE", "M0329-A-BOUNDED", "M0329-A-ANTILIPSCHITZ", "M0329-A-KERNEL", "M0329-A-CLOSED", "M0329-A-SURJECTIVE", "M0329-C-COERCIVITY"}
for oid, kind, human, formal, risk, machine in ROWS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0329-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": "M0-W-candidate" if oid in candidate_nodes else ("M0-L-provisional-composition" if oid == "M0329-T-ASSEMBLE" else "M3"),
        "readability_debt": "R3", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending",
        "provenance_id": "M0329-C01" if oid in candidate_nodes else "none",
        "foundation_profile": "Lean4+mathlib classical; accepted profile pending",
        "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive trust closure pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 50,
        "semantic_step_ledger": {"premises": "Only declared proof-requires children and the exact frozen context.", "inference": human, "output": human, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0329/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface and candidate classification only; no accepted proof or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0329-PROOF"], "owned_sources": [],
        "owner": "THM-M-0329 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M0329-T-ASSEMBLE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor inventory", "toolchain"], "revocation_state": "provisional" if oid == "M0329-T-ASSEMBLE" else "open"},
    })

def graph(es):
    out = {i: [] for i in ids}; incoming = {i: [] for i in ids}
    for e in es:
        out[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": es, "out": out, "in": incoming}

proof_edges = []
for i, (parent, child) in enumerate(PROOF_REQUIRES, 1):
    a, b = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b}, {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a}]

def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

core = [i for i in ids if not i.startswith("M0329-X-")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M0329-ROOT", "M0329-D-RIESZ"), ("M0329-ROOT", "M0329-O-EQUIV"), ("M0329-O-EQUIV", "M0329-A-SURJECTIVE")])),
    "provenance": graph(edges("V", "provenance_of", [("M0329-X-PROVENANCE", x) for x in core])),
    "evidence": graph(edges("E", "source_map", [("M0329-X-SOURCE", x) for x in core])),
    "trust": graph(edges("T", "trusts", [(x, "M0329-X-FOUNDATION") for x in ["M0329-ROOT", "M0329-T-ASSEMBLE", "M0329-D-RIESZ", "M0329-O-EQUIV"]])),
    "documentation": graph(edges("D", "documents", [("M0329-X-SOURCE", "M0329-ROOT"), ("M0329-X-PROVENANCE", "M0329-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0329-X-WORKFLOW", "M0329-ROOT"), ("M0329-X-WORKFLOW", "M0329-X-SOURCE"), ("M0329-X-WORKFLOW", "M0329-X-FOUNDATION"), ("M0329-X-WORKFLOW", "M0329-X-PROVENANCE")])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0329-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0329-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M0-W-candidate_pending_proof_and_acceptance", "theorem_complete": False, "first_open_cut": ["M0329-X-SOURCE", "M0329-X-FOUNDATION", "M0329-X-PROVENANCE", "M0329-X-WORKFLOW"]},
}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid == "M0329-T-ASSEMBLE" else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
