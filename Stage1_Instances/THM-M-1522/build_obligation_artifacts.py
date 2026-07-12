#!/usr/bin/env python3
"""Build the frozen THM-M-1522 registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATE = "2026-07-12"
STATEMENT_HASH = "1ae3d8a352060fb26372a07d0128af2f465933e4c3c08b6c752b0b5fe72c83b5"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# id, kind, human statement, formal target, output, machine, source, risk, budget
SPECS = [
    ("M1522-ROOT", "root", "The frozen ergodic probability-space Birkhoff target.",
     "Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget", "The exact canonical target.", "required", "required", "critical", "split-required"),
    ("M1522-S-DEFINITIONS", "definition", "Fix iterates, Birkhoff sums and Cesaro averages.",
     "birkhoffAverage Real T f n x = (n : Real)⁻¹ * ∑ k ∈ Finset.range n, f ((T^[k]) x)", "The checked finite-sum representation.", "required", "not_applicable", "high", 4),
    ("M1522-S-DOMAIN", "definition", "Fix the measurable probability space, real codomain, endomorphism, ergodicity, and integrability binders.",
     "The ordered binders of BirkhoffPointwiseErgodicTarget", "The exact domain and hypothesis context.", "required", "required", "high", 5),
    ("M1522-S-BOUNDARY", "terminal", "Retain the almost-everywhere qualifier and show that the n = 0 average does not affect the atTop limit.",
     "Boundary certificate for ae/Tendsto and birkhoffAverage at zero", "No strengthening to everywhere convergence and no deleted premise.", "required", "required", "high", 5),
    ("M1522-S-TRANSPORT", "transport", "Transport between birkhoffAverage and the direct finite-orbit sum.",
     "Stage1Instances.THM_M_1522.birkhoffTarget_iff_expandedFiniteSumTarget", "Checked equivalence in both directions.", "required", "not_applicable", "normal", 2),
    ("M1522-S-FOUNDATION", "certificate", "Audit the axiom and trust profile of every terminal body and composition declaration.",
     "Axiom-policy and transitive trust certificate", "Accepted foundation and TCB boundary.", "required", "not_applicable", "critical", 6),
    ("M1522-N-GENERAL", "reduction", "Reduce the ergodic constant-limit root to a general pointwise limit and invariant-limit identification.",
     "GeneralPointwiseLimitPackage and ErgodicInvariantLimitIdentification imply the root", "Two exact conditional packages for final assembly.", "required", "required", "critical", 8),
    ("M1522-C-LIMIT-DATA", "construction", "Construct an integrable invariant limit g whose integral equals that of f.",
     "Stage1Instances.THM_M_1522.InvariantLimitData mu T f g", "A well-formed invariant limit object with integral preservation.", "required", "required", "critical", "split-required"),
    ("M1522-L-POINTWISE", "core_lemma", "Prove almost-everywhere convergence of Birkhoff averages to the constructed invariant limit.",
     "Stage1Instances.THM_M_1522.GeneralPointwiseLimitPackage", "The general pointwise convergence package.", "required", "required", "critical", "split-required"),
    ("M1522-B-ERGODIC", "branch", "Use ergodicity to identify every integrable invariant limit as almost everywhere constant.",
     "Ergodic T mu -> Integrable g mu -> (g ∘ T = g ae) -> exists c, g = c ae", "Almost-everywhere constancy of g.", "required", "required", "critical", "split-required"),
    ("M1522-L-INTEGRAL-ID", "lemma", "Identify the invariant constant with integral mu f using probability normalization and integral preservation.",
     "g = c ae -> integral mu g = integral mu f -> c = integral mu f", "The exact constant-integral equality.", "required", "required", "high", 10),
    ("M1522-T-IDENTIFY", "terminal", "Combine ergodic constancy and integral identification.",
     "Stage1Instances.THM_M_1522.ErgodicInvariantLimitIdentification", "The ergodic invariant-limit identification package.", "required", "required", "critical", 8),
    ("M1522-T-ASSEMBLE", "terminal", "Substitute the identified limit into pointwise convergence and discharge the exact root.",
     "Stage1Instances.THM_M_1522.root_of_pointwise_and_identification", "Conditional checked composition into the canonical target.", "required", "required", "critical", 6),
    ("M1522-X-UPSTREAM", "bridge", "Integrate and audit the immutable external pointwise-Birkhoff proof body.",
     "lua-vr/pointwise-birkhoff@fc06094ca0506d8d74eba8b45b34882ce5930bf4", "A locally elaborated general pointwise package with audited dependencies.", "required", "required", "critical", "split-required"),
    ("M1522-X-SOURCE", "terminal", "Pinpoint-map the classical proof and ergodic specialization to every mathematical node.",
     "Human-source crosswalk and errata record", "Accepted source fidelity ledger.", "not_applicable", "required", "high", 8),
    ("M1522-X-PROVENANCE", "certificate", "Trace wrappers, imported declarations, and terminal proof bodies without duplicate credit.",
     "Transitive conclusion/body provenance certificate", "Release provenance boundary.", "informational", "not_applicable", "critical", 8),
]


def obligation(spec):
    oid, kind, human, formal, output, machine, source, risk, _ = spec
    fingerprint = ("lean-expression-sha256:" + STATEMENT_HASH if oid == "M1522-ROOT"
                   else "planned:v1:sha256:" + digest(formal + "\n" + output))
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "provenance_overlay_no_independent_proof_credit"
    body = ("local:Stage1_Instances/THM-M-1522/ObligationTree.lean#"
            "root_of_pointwise_and_identification" if oid == "M1522-T-ASSEMBLE" else None)
    return {
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": source, "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": exclusion,
        "terminal_proof_body_id": body,
    }


def node(spec):
    oid, kind, human, formal, output, machine, source, risk, budget = spec
    machine_debt = "M3" if oid in {"M1522-ROOT", "M1522-L-POINTWISE", "M1522-X-UPSTREAM"} else "M4"
    if oid in {"M1522-S-DEFINITIONS", "M1522-S-DOMAIN", "M1522-S-TRANSPORT", "M1522-T-ASSEMBLE"}:
        machine_debt = "M0-P"
    ledger = {
        "premises": f"The exact typed proof children recorded for {oid}; none may be inferred from documentation or provenance edges.",
        "inference": human,
        "output": output,
        "source_anchors": "anchor-audit-and-source-crosswalk" if source == "required" else "not-applicable",
        "outgoing_use": "Consumed only through the recorded reciprocal composes edge; no stronger conclusion is credited.",
    }
    anchor = oid.lower()
    return {
        "node_id": "THM-" + oid, "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": machine_debt, "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-and-source-crosswalk" if source == "required" else "not-applicable",
        "provenance_id": "anchor-audit:external-candidate" if oid in {"M1522-L-POINTWISE", "M1522-X-UPSTREAM"} else "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-open",
        "tcb_profile": "lean-4.29.0-mathlib-8a178386/transitive-audit-open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1522/obligation-tree.md#{anchor}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture and debt record only; open premises receive no proof or completion credit.",
        "task_ids": ["S56-M-1522-OBLIGATION_TREE", "S56-M-1522-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-1522/ObligationTree.lean#root_of_pointwise_and_identification"]
                          if oid == "M1522-T-ASSEMBLE" else []),
        "owner": "THM-M-1522 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": f"frozen-{DATE}; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source,body change; revocation=none",
    }


def graph(name, edge_type, pairs):
    edges = []
    incoming, outgoing = {}, {}
    for index, (parent, child) in enumerate(pairs, 1):
        edge_id = f"E-{name.upper()}-{index:02d}"
        row = {"edge_id": edge_id, "from": parent, "to": child, "type": edge_type}
        edges.append(row)
        outgoing.setdefault(parent, []).append(edge_id)
        incoming.setdefault(child, []).append(edge_id)
    return {"edges": edges, "out": outgoing, "in": incoming}


def proof_graph(pairs):
    edges = []
    incoming, outgoing = {}, {}
    for index, (parent, child) in enumerate(pairs, 1):
        forward_id, reverse_id = f"E-PROOF-{index:02d}-REQ", f"E-PROOF-{index:02d}-COMPOSE"
        for row in (
            {"edge_id": forward_id, "from": parent, "to": child, "type": "proof_requires", "reciprocal_edge_id": reverse_id},
            {"edge_id": reverse_id, "from": child, "to": parent, "type": "composes", "reciprocal_edge_id": forward_id},
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
    "item_id": "S56-M-1522-OBLIGATION_TREE", "theorem_id": "THM-M-1522",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated statement and bounded immutable anchor audit, with eligibility fixed before proof execution.",
    "frozen_against_statement_expression_sha256": STATEMENT_HASH,
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1522-ROOT", "denominator_sha256": denominator_hash,
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
    ("M1522-ROOT", "M1522-T-ASSEMBLE"),
    ("M1522-T-ASSEMBLE", "M1522-L-POINTWISE"),
    ("M1522-T-ASSEMBLE", "M1522-T-IDENTIFY"),
    ("M1522-L-POINTWISE", "M1522-C-LIMIT-DATA"),
    ("M1522-L-POINTWISE", "M1522-X-UPSTREAM"),
    ("M1522-T-IDENTIFY", "M1522-B-ERGODIC"),
    ("M1522-T-IDENTIFY", "M1522-L-INTEGRAL-ID"),
]
refinement_pairs = [("M1522-ROOT", oid) for oid in ids[1:] if oid not in {c for _, c in proof_pairs}]
graphs = {
    "proof": proof_graph(proof_pairs),
    "refinement": graph("refinement", "logical_decomposition", refinement_pairs),
    "provenance": graph("provenance", "provenance_of", [("M1522-X-PROVENANCE", "M1522-X-UPSTREAM"), ("M1522-X-PROVENANCE", "M1522-T-ASSEMBLE")]),
    "evidence": graph("evidence", "evidence_for", [("M1522-S-TRANSPORT", "M1522-S-DEFINITIONS")]),
    "trust": graph("trust", "trusts", [("M1522-ROOT", "M1522-S-FOUNDATION"), ("M1522-X-UPSTREAM", "M1522-S-FOUNDATION")]),
    "documentation": graph("documentation", "documents", [("M1522-X-SOURCE", "M1522-ROOT"), ("M1522-X-PROVENANCE", "M1522-ROOT")]),
    "workflow": graph("workflow", "workflow_depends_on", [("M1522-T-ASSEMBLE", "M1522-L-POINTWISE"), ("M1522-T-ASSEMBLE", "M1522-T-IDENTIFY"), ("M1522-X-PROVENANCE", "M1522-T-ASSEMBLE")]),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1522-OBLIGATION_TREE",
    "theorem_id": "THM-M-1522", "registry_denominator_sha256": denominator_hash,
    "nodes": [node(spec) for spec in SPECS], "graphs": graphs,
    "composition_certificate": {
        "declaration": "Stage1Instances.THM_M_1522.root_of_pointwise_and_identification",
        "parent": "M1522-ROOT", "children": ["M1522-L-POINTWISE", "M1522-T-IDENTIFY"],
        "status": "kernel_checked_conditional_composition",
        "boundary": "Both children remain open; this certificate introduces neither child proof.",
    },
    "closure_boundary": {
        "closed_obligations": ["M1522-S-DEFINITIONS", "M1522-S-DOMAIN", "M1522-S-TRANSPORT", "M1522-T-ASSEMBLE"],
        "provisional_only": True, "root_machine_debt": "M3", "theorem_complete": False,
        "remaining_root_cut_set": ["M1522-L-POINTWISE", "M1522-T-IDENTIFY"],
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(ids)} obligations; denominator {denominator_hash}")
