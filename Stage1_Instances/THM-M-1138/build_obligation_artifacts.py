#!/usr/bin/env python3
"""Deterministically build the THM-M-1138 obligation registry and graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEOREM = "THM-M-1138"
ITEM = "S56-M-1138-OBLIGATION_TREE"

ROWS = [
    ("ROOT", "root", "Exact frozen weak harmonic maximum principle.", "Stage1Instances.THM_M_1138.HarmonicWeakMaximumPrinciple", "canonical theorem", "critical", "required", "required"),
    ("S-DEFINITIONS", "definition", "Fix Euclidean space, harmonic-on-neighborhood, closure continuity, frontier, and order conventions.", "Types and predicates elaborated by Statement.lean", "typed vocabulary", "normal", "required", "not_applicable"),
    ("S-BOUNDARIES", "branch", "Discharge positive dimension, nonempty domain, empty-frontier, and closure membership boundary behavior.", "Planned boundary lemmas for the frozen binders", "legal boundary cases", "high", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit classical compactness, choice, topology, imports, axioms, and TCB closure.", "Planned trust and axiom certificate", "release trust boundary", "critical", "required", "not_applicable"),
    ("N-COMPACT-CLOSURE", "normalization", "Derive compactness and nonemptiness of closure U from finite dimensionality and bounded nonempty U.", "Planned IsCompact (closure U) and (closure U).Nonempty", "compact nonempty search domain", "normal", "required", "required"),
    ("C-CLOSURE-MAXIMIZER", "construction", "Use closure continuity on the compact closure to construct a point maximizing u on closure U.", "Planned exists z in closure U, IsMaxOn u (closure U) z", "closure maximizer and invariant", "high", "required", "required"),
    ("B-MAXIMIZER-LOCATION", "branch", "Split the closure maximizer into frontier and interior cases and prove the split exhaustive.", "Planned z in frontier U or z in U", "exhaustive location branches", "normal", "required", "required"),
    ("L-INTERIOR-LOCAL", "core_lemma", "An interior local maximum of a harmonic function forces local constancy by the mean-value argument.", "Planned local strong maximum lemma", "local constancy near an interior maximizer", "critical", "required", "required"),
    ("L-CONNECTED-PROPAGATION", "core_lemma", "Propagate the local maximum level through connected U, yielding constancy on U.", "Planned connected open/closed propagation lemma", "u is constant on U", "critical", "required", "required"),
    ("L-FRONTIER-NONEMPTY", "core_lemma", "A nonempty bounded open subset of positive-dimensional Euclidean space has nonempty frontier.", "Planned frontier nonemptiness lemma", "a frontier witness", "high", "required", "required"),
    ("L-CONTINUITY-EXTENSION", "core_lemma", "Extend constancy from U to closure U using density in its closure and continuity on closure U.", "Planned closure extension lemma", "boundary witness has the maximum value", "high", "required", "required"),
    ("T-BOUNDARY-MAX", "terminal", "Merge the direct frontier case and interior-constancy case into a frontier maximizer dominating closure U.", "Stage1Instances.THM_M_1138.BoundaryMaximumPackage", "terminal analytic package", "critical", "required", "required"),
    ("T-ROOT-TRANSPORT", "transport", "Transport the terminal package to the definitionally identical exact root.", "Stage1Instances.THM_M_1138.root_of_boundaryMaximumPackage", "exact canonical root", "low", "required", "not_applicable"),
    ("X-SOURCE", "terminal", "Map every analytic and topological node to a primary source with assumptions and errata.", "Human-source crosswalk, pending", "source provenance only", "high", "informational", "required"),
    ("X-PROVENANCE", "terminal", "Record terminal proof bodies, imports, axiom closure, and replay provenance.", "Formal provenance ledger, pending", "formal provenance only", "critical", "informational", "not_applicable"),
]

CHILDREN = {
    "ROOT": ["T-ROOT-TRANSPORT"],
    "T-ROOT-TRANSPORT": ["T-BOUNDARY-MAX"],
    "T-BOUNDARY-MAX": ["C-CLOSURE-MAXIMIZER", "B-MAXIMIZER-LOCATION", "L-INTERIOR-LOCAL", "L-CONNECTED-PROPAGATION", "L-FRONTIER-NONEMPTY", "L-CONTINUITY-EXTENSION", "S-BOUNDARIES"],
    "C-CLOSURE-MAXIMIZER": ["N-COMPACT-CLOSURE", "S-DEFINITIONS"],
    "L-INTERIOR-LOCAL": ["S-DEFINITIONS"],
}

def oid(short):
    return f"M1138-{short}"

def fingerprint(short, formal):
    return hashlib.sha256(f"{THEOREM}\0{short}\0{formal}".encode()).hexdigest()

def edge(graph, number, source, target, kind, reciprocal=None):
    row = {"edge_id": f"M1138-{graph.upper()}-{number:02d}", "from": oid(source), "to": oid(target), "type": kind}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row

def graph(edges):
    ids = [oid(row[0]) for row in ROWS]
    return {"edges": edges, "out": {i: [e["edge_id"] for e in edges if e["from"] == i] for i in ids}, "in": {i: [e["edge_id"] for e in edges if e["to"] == i] for i in ids}}

def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    nodes = []
    for short, kind, human, formal, output, risk, machine, human_source in ROWS:
        terminal_body = "local:root_of_boundaryMaximumPackage" if short == "T-ROOT-TRANSPORT" else "unknown"
        registry_kind = {"normalization": "reduction", "core_lemma": "lemma", "certificate": "computation"}.get(kind, kind)
        obligations.append({
            "obligation_id": oid(short), "statement_fingerprint": fingerprint(short, formal), "kind": registry_kind,
            "root_relevant": short not in {"X-SOURCE", "X-PROVENANCE"}, "machine_eligibility": machine,
            "human_source_eligibility": human_source, "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": "source/provenance overlay; cannot supply machine proof credit" if machine == "informational" else None,
            "terminal_proof_body_id": terminal_body,
        })
        children = CHILDREN.get(short, [])
        checked = short in {"S-DEFINITIONS", "T-ROOT-TRANSPORT"}
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H1", "machine_debt": "M0-L" if checked else ("M3" if short == "ROOT" else "M4"),
            "readability_debt": "R3", "evidence_ids": [],
            "source_crosswalk_id": "primary-source-node-map-pending" if human_source == "required" else "not-applicable",
            "provenance_id": "local-obligation-tree-composition" if short == "T-ROOT-TRANSPORT" else ("anchor-audit-v1" if short == "X-PROVENANCE" else "none"),
            "foundation_profile": "lean4-4.29.0+mathlib-8a178386/classical-policy-audit-pending",
            "tcb_profile": "lean-kernel+mathlib-transitive-closure-pending",
            "computation_record": "none; no computation or oracle receives proof credit",
            "step_budget": "split-required" if children else 40,
            "semantic_step_ledger": {"premises": ", ".join(oid(c) for c in children) if children else "Exact frozen context", "inference": human, "output": output, "outgoing_use": "Only declared proof/composition edges may consume this output."},
            "public_readable_target": f"Stage1_Instances/THM-M-1138/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}", "status_boundary": "Architecture or checked conditional interface only; no open analytic premise is credited.",
            "task_ids": [ITEM, "S56-M-1138-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-1138/ObligationTree.lean"] if short == "T-ROOT-TRANSPORT" else [],
            "owner": "THM-M-1138 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"},
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{key: row[key] for key in fields} for row in obligations]
    digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact elaborated statement and bounded anchor audit; eligibility frozen before proof-phase closure inspection.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"), "denominator_sha256": digest,
        "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]},
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version with an append-only old/new ID delta.",
        "obligations": obligations,
    }

    proof_edges = []
    number = 1
    for parent, children in CHILDREN.items():
        for child in children:
            req = f"M1138-PROOF-{number:02d}R"
            comp = f"M1138-PROOF-{number:02d}C"
            proof_edges.append({"edge_id": req, "from": oid(parent), "to": oid(child), "type": "proof_requires", "reciprocal_edge_id": comp})
            proof_edges.append({"edge_id": comp, "from": oid(child), "to": oid(parent), "type": "composes", "reciprocal_edge_id": req})
            number += 1
    refinement = [edge("refine", i + 1, "ROOT", s, "logical_decomposition") for i, s in enumerate(["S-DEFINITIONS", "S-BOUNDARIES", "S-FOUNDATION"])]
    provenance = [edge("prov", 1, "T-BOUNDARY-MAX", "X-PROVENANCE", "provenance_of")]
    evidence = [edge("evidence", 1, "T-ROOT-TRANSPORT", "S-FOUNDATION", "evidence_for")]
    trust = [edge("trust", 1, "ROOT", "S-FOUNDATION", "trusts"), edge("trust", 2, "T-BOUNDARY-MAX", "X-PROVENANCE", "trusts")]
    docs = [edge("docs", 1, "ROOT", "X-SOURCE", "documents"), edge("docs", 2, "ROOT", "X-PROVENANCE", "documents")]
    workflow = [edge("workflow", 1, "T-BOUNDARY-MAX", "X-SOURCE", "workflow_depends_on"), edge("workflow", 2, "T-BOUNDARY-MAX", "X-PROVENANCE", "workflow_depends_on"), edge("workflow", 3, "ROOT", "T-ROOT-TRANSPORT", "workflow_depends_on")]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-1138-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
        "root_node_id": oid("ROOT"), "edge_direction": "proof_requires is parent to child; composes is child to parent.", "nodes": nodes,
        "graphs": {"proof": graph(proof_edges), "refinement": graph(refinement), "provenance": graph(provenance), "evidence": graph(evidence), "trust": graph(trust), "documentation": graph(docs), "workflow": graph(workflow)},
        "closure_boundary": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-ROOT-TRANSPORT")], "root_closed": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-BOUNDARY-MAX")], "root_machine_debt": "M3"},
    }
    recipes = [{"recipe_id": f"VAL-{oid(short)}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1138/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1138 obligation tree"}], "covered_obligation_ids": [oid(short)], "covered_declarations": [formal] if formal.startswith("Stage1Instances.") else []} for short, _, _, formal, _, _, _, _ in ROWS]
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "Structural recipes validate the freeze and conditional composition, not open analytic proofs."}
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

if __name__ == "__main__":
    main()
