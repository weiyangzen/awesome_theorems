#!/usr/bin/env python3
"""Build the deterministic THM-M-1005 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1005-OBLIGATION_TREE"
THEOREM = "THM-M-1005"
PREFIX = "M1005-"

ROWS = [
    ("ROOT", "root", "The exact frozen strong finite-horizon Doob Lp inequality.",
     "Stage1Instances.THM_M_1005.Statement", "The canonical proposition.", "critical", "required", "required"),
    ("S-DEFINITIONS", "definition", "Freeze the filtration, martingale, running absolute maximum, eLpNorm, horizon, and constant.",
     "Stage1Instances.THM_M_1005.{runningAbsMax,DoobLpMomentEstimate}", "The elaborated vocabulary and binder context.", "high", "not_applicable", "required"),
    ("S-BOUNDARIES", "normalization", "Preserve p > 1, p < infinity, inclusive horizon, and the n = 0 case.",
     "planned exact boundary lemmas for p and Finset.range (n + 1)", "Nonempty maximum and finite conjugate-exponent regime.", "high", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit imports, classical principles, transitive axioms, and the noncomputable boundary.",
     "planned axiom/import/TCB certificate", "Accepted foundation profile for every admitted body.", "high", "not_applicable", "required"),
    ("N-ABS-SUBMARTINGALE", "normalization", "Derive that k maps to |f k| is a nonnegative submartingale from the real martingale f.",
     "planned exact Martingale-to-absolute-Submartingale declaration", "A nonnegative submartingale suitable for maximal_ineq.", "critical", "required", "required"),
    ("C-MAXIMUM", "construction", "Construct the finite running maximum and prove its measurability and required Lp interfaces.",
     "planned runningAbsMax measurability and eLpNorm interface package", "A measurable finite maximum with tail and norm representations.", "high", "required", "required"),
    ("L-WEAK-MAXIMAL", "bridge", "Apply the pinned weak maximal inequality to the absolute-value submartingale at every threshold.",
     "MeasureTheory.maximal_ineq specialized to fun k omega => |f k omega|", "The threshold/set-integral estimate used by layer cake.", "critical", "required", "required"),
    ("L-LAYER-CAKE", "core_lemma", "Convert the Lp moment of the running maximum to an integral of its tail distribution.",
     "planned layer-cake/Cavalieri identity compatible with eLpNorm", "An integral expression controlled pointwise by the weak estimate.", "critical", "required", "required"),
    ("L-HOLDER", "core_lemma", "Integrate the weak estimate and use Holder duality against the terminal value.",
     "planned exact integral and Holder estimate", "The p-th moment bound with conjugate-exponent factor.", "critical", "required", "required"),
    ("L-CONSTANT", "lemma", "Normalize ENNReal/toReal coercions and identify the factor p/(p-1).",
     "planned ENNReal conjugate-exponent arithmetic lemmas", "The exact coefficient in the frozen conclusion.", "high", "required", "required"),
    ("T-STRONG-ESTIMATE", "terminal", "Assemble the analytic leaves into the exact strong Doob estimate for every frozen binder.",
     "Stage1Instances.THM_M_1005.ObligationTree.StrongDoobTerminal", "The complete terminal proposition, still open.", "critical", "required", "required"),
    ("T-ROOT-TRANSPORT", "transport", "Transport the terminal estimate to the public canonical Statement without changing binders or conclusion.",
     "Stage1Instances.THM_M_1005.ObligationTree.root_of_strongDoobTerminal", "The exact public root from the exact terminal package.", "high", "required", "required"),
    ("X-WEAK-PROVENANCE", "certificate", "Record the immutable body provenance and trust closure of maximal_ineq.",
     "mathlib 8a178386: MeasureTheory.maximal_ineq provenance packet", "A classified support-only external boundary.", "high", "not_applicable", "required"),
    ("X-SOURCE", "terminal", "Pinpoint-map each material transition to a primary human source including assumptions and errata.",
     "planned primary-source node crosswalk", "Human-source coverage for the mathematical route.", "high", "required", "required"),
]

PROOF_CHILDREN = {
    "ROOT": ["T-ROOT-TRANSPORT"],
    "T-ROOT-TRANSPORT": ["T-STRONG-ESTIMATE"],
    "T-STRONG-ESTIMATE": ["N-ABS-SUBMARTINGALE", "C-MAXIMUM", "L-WEAK-MAXIMAL", "L-LAYER-CAKE", "L-HOLDER", "L-CONSTANT"],
    "N-ABS-SUBMARTINGALE": ["S-DEFINITIONS", "S-BOUNDARIES"],
    "C-MAXIMUM": ["S-DEFINITIONS", "S-BOUNDARIES"],
    "L-WEAK-MAXIMAL": ["N-ABS-SUBMARTINGALE", "C-MAXIMUM"],
    "L-LAYER-CAKE": ["C-MAXIMUM"],
    "L-HOLDER": ["L-WEAK-MAXIMAL", "L-LAYER-CAKE"],
    "L-CONSTANT": ["S-BOUNDARIES"],
}


def oid(short):
    return PREFIX + short


def planned_hash(short, statement, formal):
    raw = f"v1\n{oid(short)}\n{statement}\n{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(raw).hexdigest()


def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


def edge(graph_name, number, source, target, kind, reciprocal=None):
    row = {"edge_id": f"M1005-{graph_name.upper()}-{number:02d}", "from": oid(source), "to": oid(target), "type": kind}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    nodes = []
    for short, kind, human, formal, output, risk, human_eligibility, readable in ROWS:
        fingerprint = ("lean-file-sha256:" + statement_hash) if short in {"ROOT", "S-DEFINITIONS"} else planned_hash(short, human, formal)
        machine = "informational" if short.startswith("X-") else "required"
        exclusion = "provenance_or_human_source_boundary_only" if machine == "informational" else None
        terminal = "local:Stage1_Instances/THM-M-1005/ObligationTree.lean#root_of_strongDoobTerminal" if short == "T-ROOT-TRANSPORT" else None
        obligations.append({
            "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
            "root_relevant": True, "machine_eligibility": machine,
            "human_source_eligibility": human_eligibility, "readable_eligibility": readable,
            "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": terminal,
        })
        children = PROOF_CHILDREN.get(short, [])
        ledger = {
            "premises": "Exact frozen context" if not children else ", ".join(oid(child) for child in children),
            "inference": human,
            "output": output,
            "outgoing_use": "Only declared proof/composition edges may consume this output.",
        }
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H2", "machine_debt": "M0-L" if short in {"S-DEFINITIONS", "T-ROOT-TRANSPORT"} else ("M3" if short == "ROOT" else "M4"),
            "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "anchor-audit-weak-boundary" if short in {"L-WEAK-MAXIMAL", "X-WEAK-PROVENANCE"} else ("primary-source-node-map-pending" if human_eligibility == "required" else "not-applicable"),
            "provenance_id": "S56-M-1005-C02" if short in {"L-WEAK-MAXIMAL", "X-WEAK-PROVENANCE"} else ("local-obligation-tree-composition" if short == "T-ROOT-TRANSPORT" else "none"),
            "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none; no oracle or external computation supplies proof credit",
            "step_budget": "split-required" if children else 40, "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-1005/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}", "status_boundary": "Architecture or checked interface only; no undeclared premise and no proof closure.",
            "task_ids": [ITEM, "S56-M-1005-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1005/ObligationTree.lean"] if short == "T-ROOT-TRANSPORT" else [],
            "owner": "THM-M-1005 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if short in {"S-DEFINITIONS", "T-ROOT-TRANSPORT"} else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if short in {"S-DEFINITIONS", "T-ROOT-TRANSPORT"} else "open"},
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{key: row[key] for key in fields} for row in obligations]
    digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact elaborated statement and bounded immutable anchor audit; eligibility frozen before proof-phase closure inspection.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"), "denominator_sha256": digest,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version with an append-only old/new ID delta.",
        "obligations": obligations,
    }

    proof_edges = []
    number = 1
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            req_id = f"M1005-PROOF-{number:02d}R"
            comp_id = f"M1005-PROOF-{number:02d}C"
            proof_edges.append(edge("proof", number, parent, child, "proof_requires", comp_id))
            proof_edges[-1]["edge_id"] = req_id
            proof_edges.append(edge("proof", number, child, parent, "composes", req_id))
            proof_edges[-1]["edge_id"] = comp_id
            number += 1
    refinement_edges = [edge("refine", 1, "ROOT", "S-DEFINITIONS", "logical_decomposition"), edge("refine", 2, "ROOT", "S-BOUNDARIES", "logical_decomposition"), edge("refine", 3, "ROOT", "S-FOUNDATION", "logical_decomposition")]
    provenance_edges = [edge("prov", 1, "L-WEAK-MAXIMAL", "X-WEAK-PROVENANCE", "provenance_of")]
    evidence_edges = [edge("evidence", 1, "T-ROOT-TRANSPORT", "S-FOUNDATION", "evidence_for")]
    trust_edges = [edge("trust", 1, "ROOT", "S-FOUNDATION", "trusts"), edge("trust", 2, "L-WEAK-MAXIMAL", "X-WEAK-PROVENANCE", "trusts")]
    documentation_edges = [edge("docs", i + 1, "ROOT", short, "documents") for i, short in enumerate(["X-SOURCE", "X-WEAK-PROVENANCE"])]
    workflow_edges = [edge("workflow", 1, "T-STRONG-ESTIMATE", "X-SOURCE", "workflow_depends_on"), edge("workflow", 2, "T-STRONG-ESTIMATE", "X-WEAK-PROVENANCE", "workflow_depends_on"), edge("workflow", 3, "ROOT", "T-ROOT-TRANSPORT", "workflow_depends_on")]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-1005-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
        "root_node_id": oid("ROOT"), "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.",
        "nodes": nodes,
        "graphs": {"proof": graph(proof_edges), "refinement": graph(refinement_edges), "provenance": graph(provenance_edges), "evidence": graph(evidence_edges), "trust": graph(trust_edges), "documentation": graph(documentation_edges), "workflow": graph(workflow_edges)},
        "closure_boundary": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-ROOT-TRANSPORT")], "root_closed": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-STRONG-ESTIMATE")], "root_machine_debt": "M3"},
    }
    recipes = [{"recipe_id": f"VAL-{oid(short)}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1005/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1005 obligation tree"}], "covered_obligation_ids": [oid(short)], "covered_declarations": [formal] if formal.startswith("Stage1Instances.") else []} for short, _, _, formal, _, _, _, _ in ROWS]
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "Structural recipes validate the freeze and checked composition interface, not the open analytic proofs."}
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


if __name__ == "__main__":
    main()
