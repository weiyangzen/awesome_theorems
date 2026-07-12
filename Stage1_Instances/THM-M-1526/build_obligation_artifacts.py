#!/usr/bin/env python3
"""Build the frozen THM-M-1526 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATE = "2026-07-12"
STATEMENT_HASH = "956e5d9f215473f7e3a896cbe5f4e1254d64dd1a29aacd695dc1984a71f06215"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# id, kind, human statement, formal target, output, machine, source, risk, budget
SPECS = [
    ("M1526-ROOT", "root", "Prove the frozen free Dirac factorization and its pointwise Klein-Gordon consequence.",
     "Stage1Instances.THM_M_1526.FreeDiracFactorizationTarget", "The exact canonical conjunction.", "required", "required", "critical", "split-required"),
    ("M1526-S-DEFINITIONS", "definition", "Fix the slash and metric-contracted Klein-Gordon endomorphisms.",
     "Stage1Instances.THM_M_1526.slash and kleinGordon", "The two checked finite-sum operator definitions.", "required", "not_applicable", "high", 6),
    ("M1526-S-DOMAIN", "definition", "Fix finite indices, a complex module, and constant complex-linear endomorphisms.",
     "The ordered binders of FreeDiracFactorizationTarget", "The exact universe and typeclass context.", "required", "required", "high", 6),
    ("M1526-S-BOUNDARY", "terminal", "Retain zero mass, empty index types, and the zero spinor space without strengthening the target.",
     "Boundary cases admitted by FreeDiracFactorizationTarget", "An explicit degenerate-case certificate.", "required", "required", "high", 8),
    ("M1526-S-TRANSPORT", "transport", "Relate the named direct consequence shape to the canonical target.",
     "Stage1Instances.THM_M_1526.freeDiracFactorizationTarget_iff_directConsequenceShape", "Checked equivalence in both directions.", "required", "not_applicable", "normal", 2),
    ("M1526-S-FOUNDATION", "certificate", "Audit every terminal body's axioms and transitive trust boundary.",
     "Axiom-policy and transitive TCB certificate", "Accepted foundation and TCB boundary.", "required", "not_applicable", "critical", 8),
    ("M1526-N-PRODUCT", "normalization", "Normalize the product of conjugate factors to slash squared minus mass squared.",
     "(slash D + m * 1) * (slash D - m * 1) = slash D * slash D - m^2 * 1", "The scalar cross terms cancel in the endomorphism ring.", "required", "required", "high", 12),
    ("M1526-C-PAIR-SPLIT", "construction", "Partition the double finite sum into diagonal terms and unordered off-diagonal pairs.",
     "Finite-index pair partition and recombination certificate", "A duplicate-free diagonal/off-diagonal expansion.", "required", "required", "critical", "split-required"),
    ("M1526-L-SLASH-SQUARE", "core_lemma", "Identify slash squared with the metric-contracted commuting second derivatives.",
     "slash D * slash D = kleinGordon D", "The central operator identity.", "required", "required", "critical", "split-required"),
    ("M1526-L-DIAGONAL", "lemma", "Rewrite diagonal gamma products by the diagonal Clifford law.",
     "Diagonal part = sum mu, g mu mu scalar-multiplied by deriv mu squared", "All diagonal summands of kleinGordon.", "required", "required", "high", 14),
    ("M1526-L-OFFDIAGONAL", "lemma", "Pair off-diagonal terms and apply gamma/derivative commutation plus the polarized Clifford law.",
     "Off-diagonal pair (mu,nu) = (g mu nu + g nu mu) times deriv mu * deriv nu", "All off-diagonal summands of kleinGordon.", "required", "required", "critical", "split-required"),
    ("M1526-T-FACTOR", "terminal", "Combine product normalization and slash-square identification into the exact factorization identity.",
     "Stage1Instances.THM_M_1526.FactorizationPackage", "The factorization conjunct for every admissible D.", "required", "required", "critical", 8),
    ("M1526-T-CONSEQUENCE", "terminal", "Apply the factorization to a vector killed by the right Dirac factor.",
     "factorization D -> rightFactor D psi = 0 -> kleinGordonMass D psi = 0", "The pointwise consequence without a new analytic premise.", "required", "required", "high", 5),
    ("M1526-T-ASSEMBLE", "terminal", "Assemble factorization and its derived consequence into the canonical conjunction.",
     "Stage1Instances.THM_M_1526.root_of_factorization", "Conditional checked composition into the exact root.", "required", "required", "critical", 6),
    ("M1526-X-MATHLIB", "bridge", "Audit and use the pinned finite-sum, endomorphism, matrix, and Clifford support boundary.",
     "mathlib@8a178386ffc0f5fef0b77738bb5449d50efeea95", "Pinned supporting declarations with no terminal-target credit.", "required", "required", "critical", "split-required"),
    ("M1526-X-SOURCE", "terminal", "Pinpoint-map the historical factorization, conventions, and consequence to each mathematical node.",
     "Human-source crosswalk and errata record", "Accepted source-fidelity ledger.", "not_applicable", "required", "high", 10),
    ("M1526-X-PROVENANCE", "certificate", "Trace wrappers and terminal bodies without duplicate semantic credit.",
     "Transitive conclusion/body provenance certificate", "Release provenance boundary.", "informational", "not_applicable", "critical", 8),
]


def obligation(spec):
    oid, kind, _, formal, output, machine, source, risk, _ = spec
    fingerprint = ("lean-expression-sha256:" + STATEMENT_HASH if oid == "M1526-ROOT"
                   else "planned:v1:sha256:" + digest(formal + "\n" + output))
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "provenance_overlay_no_independent_proof_credit"
    body = ("local:Stage1_Instances/THM-M-1526/ObligationTree.lean#root_of_factorization"
            if oid == "M1526-T-ASSEMBLE" else None)
    return {
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": source, "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": exclusion,
        "terminal_proof_body_id": body,
    }


def node(spec):
    oid, kind, human, formal, output, machine, source, _, budget = spec
    debt = "M4"
    if oid in {"M1526-ROOT", "M1526-L-SLASH-SQUARE", "M1526-X-MATHLIB"}:
        debt = "M3"
    if oid in {"M1526-S-DEFINITIONS", "M1526-S-DOMAIN", "M1526-S-TRANSPORT", "M1526-T-CONSEQUENCE", "M1526-T-ASSEMBLE"}:
        debt = "M0-P"
    ledger = {
        "premises": f"Only the exact typed proof children recorded for {oid}; documentation and provenance edges provide no premises.",
        "inference": human,
        "output": output,
        "source_anchors": "anchor-audit-and-source-crosswalk" if source == "required" else "not-applicable",
        "outgoing_use": "Consumed only through recorded typed edges; no stronger conclusion or duplicate credit is permitted.",
    }
    return {
        "node_id": "THM-" + oid, "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-and-source-crosswalk" if source == "required" else "not-applicable",
        "provenance_id": "anchor-audit:pinned-support" if oid == "M1526-X-MATHLIB" else "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-open",
        "tcb_profile": "lean-4.29.0-mathlib-8a178386/transitive-audit-open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1526/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture and debt record only; open premises receive no proof or completion credit.",
        "task_ids": ["S56-M-1526-OBLIGATION_TREE", "S56-M-1526-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-1526/ObligationTree.lean#root_of_factorization"]
                          if oid == "M1526-T-ASSEMBLE" else []),
        "owner": "THM-M-1526 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": f"frozen-{DATE}; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source,body change; revocation=none",
    }


def graph(name, edge_type, pairs):
    edges, incoming, outgoing = [], {}, {}
    for index, (start, end) in enumerate(pairs, 1):
        edge_id = f"E-{name.upper()}-{index:02d}"
        row = {"edge_id": edge_id, "from": start, "to": end, "type": edge_type}
        edges.append(row)
        outgoing.setdefault(start, []).append(edge_id)
        incoming.setdefault(end, []).append(edge_id)
    return {"edges": edges, "out": outgoing, "in": incoming}


def proof_graph(pairs):
    edges, incoming, outgoing = [], {}, {}
    for index, (parent, child) in enumerate(pairs, 1):
        forward, reverse = f"E-PROOF-{index:02d}-REQ", f"E-PROOF-{index:02d}-COMPOSE"
        for row in (
            {"edge_id": forward, "from": parent, "to": child, "type": "proof_requires", "reciprocal_edge_id": reverse},
            {"edge_id": reverse, "from": child, "to": parent, "type": "composes", "reciprocal_edge_id": forward},
        ):
            edges.append(row)
            outgoing.setdefault(row["from"], []).append(row["edge_id"])
            incoming.setdefault(row["to"], []).append(row["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


obligations = [obligation(spec) for spec in SPECS]
ids = [row["obligation_id"] for row in obligations]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator_hash = digest(json.dumps(projection, sort_keys=True, separators=(",", ":")))

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-1526-OBLIGATION_TREE", "theorem_id": "THM-M-1526",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated statement and bounded immutable anchor audit, with eligibility fixed before proof execution.",
    "frozen_against_statement_expression_sha256": STATEMENT_HASH,
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1526-ROOT", "denominator_sha256": denominator_hash,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_pairs = [
    ("M1526-ROOT", "M1526-T-ASSEMBLE"),
    ("M1526-T-ASSEMBLE", "M1526-T-FACTOR"),
    ("M1526-T-FACTOR", "M1526-N-PRODUCT"),
    ("M1526-T-FACTOR", "M1526-L-SLASH-SQUARE"),
    ("M1526-L-SLASH-SQUARE", "M1526-C-PAIR-SPLIT"),
    ("M1526-L-SLASH-SQUARE", "M1526-L-DIAGONAL"),
    ("M1526-L-SLASH-SQUARE", "M1526-L-OFFDIAGONAL"),
    ("M1526-L-SLASH-SQUARE", "M1526-X-MATHLIB"),
]
proof_children = {child for _, child in proof_pairs}
refinement_pairs = [("M1526-ROOT", oid) for oid in ids[1:] if oid not in proof_children]
graphs = {
    "proof": proof_graph(proof_pairs),
    "refinement": graph("refinement", "logical_decomposition", refinement_pairs),
    "provenance": graph("provenance", "provenance_of", [("M1526-X-PROVENANCE", "M1526-X-MATHLIB"), ("M1526-X-PROVENANCE", "M1526-T-ASSEMBLE")]),
    "evidence": graph("evidence", "evidence_for", [("M1526-S-TRANSPORT", "M1526-S-DEFINITIONS")]),
    "trust": graph("trust", "trusts", [("M1526-ROOT", "M1526-S-FOUNDATION"), ("M1526-X-MATHLIB", "M1526-S-FOUNDATION")]),
    "documentation": graph("documentation", "documents", [("M1526-X-SOURCE", "M1526-ROOT"), ("M1526-X-PROVENANCE", "M1526-ROOT")]),
    "workflow": graph("workflow", "workflow_depends_on", [("M1526-T-ASSEMBLE", "M1526-T-FACTOR"), ("M1526-T-FACTOR", "M1526-L-SLASH-SQUARE"), ("M1526-X-PROVENANCE", "M1526-T-ASSEMBLE")]),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1526-OBLIGATION_TREE",
    "theorem_id": "THM-M-1526", "registry_denominator_sha256": denominator_hash,
    "nodes": [node(spec) for spec in SPECS], "graphs": graphs,
    "composition_certificate": {
        "declaration": "Stage1Instances.THM_M_1526.root_of_factorization",
        "parent": "M1526-ROOT", "children": ["M1526-T-FACTOR"],
        "status": "kernel_checked_conditional_composition",
        "boundary": "The factorization package remains open; the certificate derives only the consequence and conjunction.",
    },
    "closure_boundary": {
        "closed_obligations": ["M1526-S-DEFINITIONS", "M1526-S-DOMAIN", "M1526-S-TRANSPORT", "M1526-T-CONSEQUENCE", "M1526-T-ASSEMBLE"],
        "provisional_only": True, "root_machine_debt": "M3", "theorem_complete": False,
        "remaining_root_cut_set": ["M1526-N-PRODUCT", "M1526-L-SLASH-SQUARE"],
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(ids)} obligations; denominator {denominator_hash}")
