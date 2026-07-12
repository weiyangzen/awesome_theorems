#!/usr/bin/env python3
"""Deterministically build the THM-M-0311 rev-5.6 architecture freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def fp(oid, statement, formal):
    return "planned:v1:sha256:" + digest({"id": oid, "statement": statement, "formal": formal})


specs = [
    ("M0311-ROOT", "root", "Exact real-and-complex L2 completeness target over every measure.",
     "Stage1Instances.THM_M_0311.RieszFischerTarget", "critical", "M3", 10),
    ("M0311-S-ENCODING", "definition", "Preserve the MeasureTheory.Lp almost-everywhere quotient, exponent two, arbitrary measure, and both scalar fields.",
     "Stage1Instances.THM_M_0311.RieszFischerTarget", "high", "M0-L", 20),
    ("M0311-B-REAL", "branch", "The real-valued L2 space is complete for every measure.",
     "Stage1Instances.THM_M_0311.RealL2Complete", "high", "M3", 10),
    ("M0311-B-COMPLEX", "branch", "The complex-valued L2 space is complete for every measure.",
     "Stage1Instances.THM_M_0311.ComplexL2Complete", "high", "M3", 10),
    ("M0311-T-ASSEMBLE", "transport", "Combine the real and complex scalar conclusions into the exact conjunction and binder order.",
     "Stage1Instances.THM_M_0311.obligationTreeTarget_of_scalar_children", "high", "M0-L", 8),
    ("M0311-L-LP-COMPLETE", "core_lemma", "Pinned mathlib supplies completeness of Lp E p mu from completeness of E and Fact (1 <= p).",
     "MeasureTheory.Lp.instCompleteSpace", "critical", "M3", 15),
    ("M0311-L-CRITERION", "reduction", "Reduce metric completeness of Lp to convergence of suitably controlled Cauchy representatives.",
     "MeasureTheory.Lp.completeSpace_lp_of_cauchy_complete_eLpNorm", "critical", "M3", 60),
    ("M0311-L-CAUCHY", "core_lemma", "Construct a MemLp limit and prove eLpNorm convergence for a controlled Cauchy sequence.",
     "MeasureTheory.Lp.cauchy_complete_eLpNorm", "critical", "M3", 80),
    ("M0311-L-AE-LIMIT", "construction", "Construct a strongly measurable pointwise almost-everywhere limit of the representative sequence.",
     "MeasureTheory.Lp.exists_stronglyMeasurable_limit_of_tendsto_ae", "high", "M3", 80),
    ("M0311-L-AE-CAUCHY", "core_lemma", "Derive almost-everywhere pointwise convergence from the eLpNorm Cauchy control.",
     "MeasureTheory.Lp.ae_tendsto_of_cauchy_eLpNorm", "high", "M3", 80),
    ("M0311-L-NORM-LIMIT", "core_lemma", "Upgrade pointwise almost-everywhere convergence and Cauchy control to eLpNorm convergence.",
     "MeasureTheory.Lp.cauchy_tendsto_of_tendsto", "high", "M3", 80),
    ("M0311-L-MEMLP", "core_lemma", "Show the constructed limit belongs to MemLp using convergence to zero in eLpNorm.",
     "MeasureTheory.Lp.memLp_of_cauchy_tendsto", "high", "M3", 60),
    ("M0311-X-SOURCE", "certificate", "Pinpoint-map the abstract completeness route to an accepted primary human source.",
     "non-Lean source-review boundary", "critical", "M3", 40),
    ("M0311-X-PROVENANCE", "certificate", "Bind each wrapper and shared upstream terminal body to immutable source and declaration identities.",
     "anchor-audit.json#source_provenance", "high", "M3", 30),
    ("M0311-X-FOUNDATION", "certificate", "Audit transitive axioms, declarations, TCB, and the admissibility of classical choice and quotient soundness.",
     "planned transitive trust-closure report", "critical", "M3", 40),
    ("M0311-X-COMPUTATION", "certificate", "Confirm that no oracle, native decision procedure, experiment, or unchecked certificate contributes proof credit.",
     "planned computation-boundary report", "normal", "M3", 15),
    ("M0311-X-WORKFLOW", "certificate", "Enforce statement, anchor, architecture, proof, validation, and release ordering without granting proof credit.",
     "task-dag.json", "normal", "M3", 15),
]

proof_children = {
    "M0311-ROOT": ["M0311-S-ENCODING", "M0311-B-REAL", "M0311-B-COMPLEX", "M0311-T-ASSEMBLE"],
    "M0311-B-REAL": ["M0311-L-LP-COMPLETE"],
    "M0311-B-COMPLEX": ["M0311-L-LP-COMPLETE"],
    "M0311-L-LP-COMPLETE": ["M0311-L-CRITERION", "M0311-L-CAUCHY"],
    "M0311-L-CAUCHY": ["M0311-L-AE-LIMIT", "M0311-L-AE-CAUCHY", "M0311-L-NORM-LIMIT", "M0311-L-MEMLP"],
}

overlay_ids = {"M0311-X-SOURCE", "M0311-X-PROVENANCE", "M0311-X-WORKFLOW"}
obligations = []
nodes = []
for oid, kind, human, formal, risk, machine, budget in specs:
    statement_fp = (
        "lean-expression-sha256:38cbb055cfb3734633dad981d0bd36dfb2dd89720a64e09659a1c19aae4c3d84"
        if oid in {"M0311-ROOT", "M0311-S-ENCODING"} else fp(oid, human, formal)
    )
    machine_eligibility = "informational" if oid in overlay_ids else "required"
    human_eligibility = "not_applicable" if oid in {"M0311-X-COMPUTATION", "M0311-X-WORKFLOW"} else "required"
    terminal = None
    if oid == "M0311-T-ASSEMBLE":
        terminal = "local:Stage1_Instances/THM-M-0311/ObligationTree.lean#obligationTreeTarget_of_scalar_children"
    elif oid.startswith("M0311-L-"):
        terminal = "mathlib:8a178386ffc0:" + formal
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": statement_fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine_eligibility,
        "human_source_eligibility": human_eligibility, "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": "non_proof_overlay_no_machine_credit" if oid in overlay_ids else None,
        "terminal_proof_body_id": terminal,
    })
    children = proof_children.get(oid, [])
    nodes.append({
        "node_id": "THM-M-0311-" + oid.removeprefix("M0311-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": machine, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md; pinpoint primary proof map open",
        "provenance_id": terminal or "none", "foundation_profile": "lean4-dependent-type-theory; transitive policy audit pending",
        "tcb_profile": "Lean 4.29.0 + pinned mathlib 8a178386ffc0; full declaration closure pending",
        "computation_record": "none credited; dedicated no-computation gate remains open",
        "step_budget": "split-required" if children else budget,
        "semantic_step_ledger": {"premises": children, "inference": human, "output": human},
        "public_readable_target": "Stage1_Instances/THM-M-0311/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture-phase record only; candidate bodies are not accepted proof state.",
        "task_ids": ["S56-M-0311-OBLIGATION_TREE", "S56-M-0311-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0311/ObligationTree.lean"] if oid in {"M0311-ROOT", "M0311-S-ENCODING", "M0311-B-REAL", "M0311-B-COMPLEX", "M0311-T-ASSEMBLE"} else [],
        "owner": "THM-M-0311 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if machine == "M0-L" else None, "review_due": "before proof acceptance",
                     "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"],
                     "revocation_state": "provisional" if machine == "M0-L" else "open"},
    })

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
                     "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in projection_fields} for row in obligations]
denominator = digest(projection)

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0311-OBLIGATION_TREE",
    "theorem_id": "THM-M-0311", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and immutable anchor audit, with eligibility assigned independently of candidate closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0311-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or re-fingerprint requires a new version and append-only delta.",
    "obligations": obligations,
}

def edge(eid, source, typ, target):
    return {"edge_id": eid, "from": source, "type": typ, "to": target}

graph_edges = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
for parent, children in proof_children.items():
    for child in children:
        graph_edges["proof"].append(edge("REQ-" + parent + "-" + child, parent, "proof_requires", child))
        graph_edges["proof"].append(edge("COMP-" + child + "-" + parent, child, "composes", parent))
graph_edges["refinement"] = [edge("REF-ROOT-ENC", "M0311-ROOT", "logical_decomposition", "M0311-S-ENCODING")]
graph_edges["provenance"] = [
    edge("PROV-INST-BODY", "M0311-L-LP-COMPLETE", "provenance_of", "M0311-X-PROVENANCE"),
    edge("PROV-ROOT-SOURCE", "M0311-ROOT", "source_map", "M0311-X-SOURCE"),
]
graph_edges["evidence"] = [edge("EVID-ANCHOR", "M0311-X-PROVENANCE", "evidence_for", "M0311-L-LP-COMPLETE")]
graph_edges["trust"] = [
    edge("TRUST-ROOT-FOUND", "M0311-ROOT", "trusts", "M0311-X-FOUNDATION"),
    edge("TRUST-ROOT-COMP", "M0311-ROOT", "trusts", "M0311-X-COMPUTATION"),
]
graph_edges["documentation"] = [edge("DOC-ROOT-TREE", "M0311-ROOT", "documents", "M0311-X-SOURCE")]
graph_edges["workflow"] = [
    edge("FLOW-SOURCE-TREE", "M0311-X-SOURCE", "workflow_depends_on", "M0311-X-WORKFLOW"),
    edge("FLOW-TREE-ROOT", "M0311-X-WORKFLOW", "workflow_depends_on", "M0311-ROOT"),
]

graphs = {}
for name, edges in graph_edges.items():
    outgoing, incoming = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0311-OBLIGATION_TREE",
    "theorem_id": "THM-M-0311", "registry_id": "THM-M-0311-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator, "root_node_id": "M0311-ROOT",
    "edge_direction": "proof_requires is parent-to-child; composes is the reciprocal child-to-parent edge.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0311-S-ENCODING", "M0311-T-ASSEMBLE"],
                         "candidate_not_accepted": ["M0311-B-REAL", "M0311-B-COMPLEX", "M0311-L-LP-COMPLETE"],
                         "root_machine_debt": "M3", "remaining_root_cut_set": ["M0311-B-REAL", "M0311-B-COMPLEX"],
                         "composition_certificates_checked": ["Stage1Instances.THM_M_0311.obligationTreeTarget_of_scalar_children"],
                         "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in graph_edges.values())} typed edges")
