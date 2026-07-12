#!/usr/bin/env python3
"""Build the deterministic THM-M-1177 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

SPECS = [
    ("ROOT", "root", "The exact determinant-weighted classical ABP target.", 100, "critical"),
    ("S-DATA", "definition", "Freeze the domain, regularity, coefficient, contact-set, and weighted-integral interfaces.", 70, "high"),
    ("S-FOUNDATION", "certificate", "Audit classical analysis, Lebesgue integration, derivatives, and the no-oracle boundary.", 100, "critical"),
    ("B-SPLIT", "branch", "Split exhaustively on whether the domain supremum is nonpositive or positive.", 25, "high"),
    ("B-DEGENERATE", "branch", "Prove the exact estimate when the domain supremum is nonpositive, including sign of the right side.", 55, "high"),
    ("B-POSITIVE", "branch", "Run the contact-set argument when the domain supremum is strictly positive.", 100, "critical"),
    ("C-CONTACT", "construction", "Construct upper supporting slopes and retain contact points inside the frozen upper contact set.", 100, "critical"),
    ("L-SLOPE-BALL", "core_lemma", "Show a slope ball controlled by the positive maximum and diameter is covered by supporting slopes.", 100, "critical"),
    ("L-GRADIENT-IMAGE", "bridge", "Identify supporting slopes with the gradient image on the differentiable contact set.", 100, "critical"),
    ("L-AREA", "bridge", "Bound the measure of the gradient image by the integral of the absolute Hessian determinant.", 100, "critical"),
    ("L-HESSIAN", "core_lemma", "Derive negative semidefiniteness of the Hessian at upper contact points.", 80, "critical"),
    ("L-DET-TRACE", "core_lemma", "Prove the positive-definite matrix determinant/trace AM-GM inequality with the selected signs.", 100, "critical"),
    ("L-OPERATOR", "bridge", "Use the PDE inequality and determinant/trace bound to control det(-D2u) by (f-)^n/det(A).", 100, "critical"),
    ("L-INTEGRAL", "core_lemma", "Integrate the pointwise determinant bound over the measurable contact set.", 90, "critical"),
    ("L-BALL-VOLUME", "core_lemma", "Evaluate the Euclidean slope-ball measure and isolate a dimensional constant.", 75, "high"),
    ("L-SUP", "core_lemma", "Combine slope-ball inclusion and its volume to bound the positive supremum.", 100, "critical"),
    ("T-POSITIVE", "terminal", "Compose all geometric and analytic leaves into the positive-maximum package.", 90, "critical"),
    ("T-ASSEMBLE", "composition", "Compose the two exhaustive packages using one dimensional constant into the exact root.", 45, "high"),
    ("X-SOURCE", "source_boundary", "Map primary-source assumptions and proof steps to every mathematical node.", 100, "high"),
    ("X-PROVENANCE", "certificate", "Resolve terminal bodies, imports, aliases, wrappers, and evidence ownership.", 100, "critical"),
    ("X-TCB", "certificate", "Close transitive axioms, dependencies, TCB, reproducibility, and invalidation policy.", 100, "critical"),
]

ids = [f"M1177-{suffix}" for suffix, *_ in SPECS]
math_ids = ids[:18]


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


rows = []
for suffix, kind, statement, budget, risk in SPECS:
    oid = f"M1177-{suffix}"
    source = "required" if oid not in {"M1177-S-FOUNDATION", "M1177-X-PROVENANCE", "M1177-X-TCB"} else "not_applicable"
    machine = "required" if oid in math_ids else "informational"
    exclusion = None if machine == "required" else "release_overlay_no_proof_credit"
    body = "local:Stage1_Instances/THM-M-1177/ObligationTree.lean#root_of_architecture" if suffix == "T-ASSEMBLE" else None
    fingerprint = ("lean-expression-sha256:bb3ff2384920048fe79eb0bad3c47a32db31bdaf4e4595898cbd5c7dbfb6ac41"
                   if suffix == "ROOT" else f"planned:v1:sha256:{digest_text(statement)}")
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint,
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": source, "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": exclusion,
        "terminal_proof_body_id": body,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-1177-OBLIGATION_TREE", "theorem_id": "THM-M-1177",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated ABP statement and bounded anchor audit; classical contact-set/area-formula architecture; eligibility fixed independently of closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1177-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids, "required_machine": math_ids,
        "required_human_source": [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1177-X-PROVENANCE", "M1177-X-TCB"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1177-T-ASSEMBLE"], "root_machine_debt": "M4"},
    "status_boundary": "Architecture and conditional composition only; no geometric or analytic ABP package, source acceptance, or theorem completion is supplied.",
}

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "B-SPLIT"),
    ("T-ASSEMBLE", "B-DEGENERATE"), ("T-ASSEMBLE", "T-POSITIVE"),
    ("T-POSITIVE", "B-POSITIVE"), ("T-POSITIVE", "L-SUP"),
    ("T-POSITIVE", "L-INTEGRAL"), ("L-SUP", "L-SLOPE-BALL"),
    ("L-SUP", "L-BALL-VOLUME"), ("L-SLOPE-BALL", "C-CONTACT"),
    ("L-INTEGRAL", "L-GRADIENT-IMAGE"), ("L-INTEGRAL", "L-AREA"),
    ("L-INTEGRAL", "L-OPERATOR"), ("L-GRADIENT-IMAGE", "C-CONTACT"),
    ("L-AREA", "L-HESSIAN"), ("L-OPERATOR", "L-HESSIAN"),
    ("L-OPERATOR", "L-DET-TRACE"),
]


def make_graph(name, triples):
    edges = []
    for index, (left, right, edge_type) in enumerate(triples, 1):
        edges.append({"edge_id": f"{name.upper()}-{index:03d}", "type": edge_type,
                      "from": f"M1177-{left}", "to": f"M1177-{right}"})
    incoming = {oid: [] for oid in ids}
    outgoing = {oid: [] for oid in ids}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_triples = []
for index, (parent, child) in enumerate(proof_pairs, 1):
    proof_triples.extend([(parent, child, "proof_requires"), (child, parent, "composes")])
proof = make_graph("proof", proof_triples)
for index in range(0, len(proof["edges"]), 2):
    a, b = proof["edges"][index:index + 2]
    a["reciprocal_edge_id"] = b["edge_id"]
    b["reciprocal_edge_id"] = a["edge_id"]

refinement = make_graph("refinement", [("ROOT", "S-DATA", "logical_decomposition"),
    ("ROOT", "B-SPLIT", "logical_decomposition"), ("B-POSITIVE", "C-CONTACT", "logical_decomposition")])
provenance = make_graph("provenance", [(suffix, "X-PROVENANCE", "provenance_of") for suffix, *_ in SPECS[:18]])
evidence = make_graph("evidence", [("T-ASSEMBLE", "ROOT", "provenance_of")])
trust = make_graph("trust", [(suffix, "X-TCB", "trusts") for suffix in ("ROOT", "L-AREA", "L-OPERATOR", "T-ASSEMBLE")])
documentation = make_graph("documentation", [("X-SOURCE", suffix, "documents") for suffix in ("ROOT", "C-CONTACT", "L-SLOPE-BALL", "L-AREA", "L-OPERATOR")])
workflow = make_graph("workflow", [("ROOT", "S-DATA", "workflow_depends_on"),
    ("ROOT", "X-SOURCE", "workflow_depends_on"), ("ROOT", "X-PROVENANCE", "workflow_depends_on"),
    ("ROOT", "X-TCB", "workflow_depends_on")])

nodes = []
for (suffix, kind, statement, budget, _), row in zip(SPECS, rows):
    oid = row["obligation_id"]
    formal = ("Stage1Instances.THM_M_1177.AlexandrovBakelmanPucciTarget" if suffix == "ROOT"
              else "Stage1Instances.THM_M_1177.root_of_architecture" if suffix == "T-ASSEMBLE"
              else "planned exact Lean interface")
    nodes.append({
        "node_id": f"THM-M-1177-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": statement,
        "human_debt": "H1", "machine_debt": "M0-L" if suffix == "T-ASSEMBLE" else "M4",
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk/pinpoint-node-map-pending",
        "provenance_id": "conditional-local-body" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Exact typed children and the frozen canonical context.",
            "inference": statement, "output": statement,
            "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1177/obligation-tree.md#m1177-{suffix.lower()}",
        "validation_spec_id": f"VAL-M1177-{suffix}",
        "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise or root proof credit.",
        "task_ids": ["S56-M-1177-OBLIGATION_TREE", "S56-M-1177-PROOF"],
        "owned_sources": [], "owner": "THM-M-1177 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if suffix == "T-ASSEMBLE" else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
            "revocation_state": "provisional" if suffix == "T-ASSEMBLE" else "open"},
    })

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"],
    "theorem_id": "THM-M-1177", "registry_id": "THM-M-1177-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator, "root_node_id": "M1177-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": {"proof": proof, "refinement": refinement,
        "provenance": provenance, "evidence": evidence, "trust": trust,
        "documentation": documentation, "workflow": workflow},
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M4",
        "audit_complete": False, "theorem_complete": False,
        "minimal_open_root_cut_set": ["M1177-B-DEGENERATE", "M1177-T-POSITIVE"]},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(denominator)
