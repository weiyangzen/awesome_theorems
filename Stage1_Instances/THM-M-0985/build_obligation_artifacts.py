#!/usr/bin/env python3
"""Build the frozen THM-M-0985 obligation registry and graph projections."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0985-OBLIGATION_TREE"
THEOREM = "THM-M-0985"


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


rows = [
    ("M0985-ROOT", "root", "critical", "required", "required", "required"),
    ("M0985-S-DEFINITIONS", "definition", "high", "required", "not_applicable", "required"),
    ("M0985-S-BOUNDARY", "terminal", "high", "required", "not_applicable", "required"),
    ("M0985-S-FOUNDATION", "certificate", "critical", "required", "not_applicable", "required"),
    ("M0985-N-MUTUAL-TO-PAIRWISE", "bridge", "high", "required", "required", "required"),
    ("M0985-L-PINNED-STRONG-LAW", "terminal", "critical", "required", "required", "required"),
    ("M0985-T-ASSEMBLE", "transport", "critical", "required", "required", "required"),
    ("M0985-X-SOURCE", "terminal", "high", "not_applicable", "required", "required"),
    ("M0985-X-PROVENANCE", "certificate", "critical", "informational", "not_applicable", "required"),
    ("M0985-X-VALIDATION", "certificate", "critical", "required", "not_applicable", "required"),
]

obligations = []
for oid, kind, risk, machine, human, readable in rows:
    fingerprint = "lean-expression-sha256:" + sha("Statement.lean") if oid in {
        "M0985-ROOT", "M0985-S-DEFINITIONS"
    } else "planned:v1:sha256:" + hashlib.sha256((THEOREM + ":" + oid).encode()).hexdigest()
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk, "exclusion_reason": exclusion,
        "terminal_proof_body_id": (
            "pinned:mathlib@8a178386:ProbabilityTheory.strong_law_ae" if oid == "M0985-L-PINNED-STRONG-LAW"
            else "local:ObligationTree.lean#root_of_pairwiseStrongLawPackage" if oid == "M0985-T-ASSEMBLE"
            else None),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; eligibility frozen without using observed closure.",
    "frozen_against_statement_sha256": sha("Statement.lean"),
    "frozen_against_anchor_audit_sha256": sha("anchor_audit.json"),
    "root_obligation_id": "M0985-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": [o["obligation_id"] for o in obligations if o["readable_eligibility"] == "required"],
        "informational_overlays": ["M0985-X-PROVENANCE"],
    },
    "delta_policy": "Any split, merge, correction, exclusion, or eligibility change creates a new version with append-only delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {
        "closed_obligations": ["M0985-S-DEFINITIONS", "M0985-S-BOUNDARY", "M0985-N-MUTUAL-TO-PAIRWISE", "M0985-T-ASSEMBLE"],
        "root_machine_debt": "M3"
    },
    "status_boundary": "Registry and denominators only; no proof-phase credit, accepted receipt, audit completion, or theorem completion."
}

descriptions = {
    "M0985-ROOT": ("The exact frozen iid real strong law.", "Stage1Instances.THMM0985.KolmogorovStrongLaw", "canonical proposition", "M3", 20),
    "M0985-S-DEFINITIONS": ("Fix zero-based arithmetic means and Bochner expectation.", "Stage1Instances.THMM0985.arithmeticMean", "exact vocabulary", "M0-L", 10),
    "M0985-S-BOUNDARY": ("Check the n=0 and n=1 mean conventions.", "arithmeticMean_zero; arithmeticMean_one", "boundary equalities", "M0-L", 10),
    "M0985-S-FOUNDATION": ("Audit classical principles, imports, kernel, and TCB.", "planned transitive trust certificate", "accepted trust profile", "M4", 40),
    "M0985-N-MUTUAL-TO-PAIRWISE": ("Derive pairwise functional independence from mutual independence.", "ObligationTree.pairwise_of_mutual", "pairwise IndepFun", "M0-L", 10),
    "M0985-L-PINNED-STRONG-LAW": ("Supply the pinned pairwise iid integrable strong law terminal body.", "ProbabilityTheory.strong_law_ae", "a.e. convergence of range averages", "M3", 100),
    "M0985-T-ASSEMBLE": ("Compose independence bridge and imported terminal into the exact root.", "ObligationTree.root_of_pairwiseStrongLawPackage", "canonical proposition conditionally", "M0-L", 15),
    "M0985-X-SOURCE": ("Map a primary human proof to every substantive proof node.", "non-machine source crosswalk", "accepted source mapping", "not_applicable", 100),
    "M0985-X-PROVENANCE": ("Bind wrapper, terminal body, revision, source hash, and trust closure.", "planned provenance packet", "release provenance", "informational", 50),
    "M0985-X-VALIDATION": ("Replay exact type, axiom, placeholder, freshness, and independent checks.", "planned validation receipts", "accepted validation evidence", "M4", 60),
}

nodes = []
for o in obligations:
    oid = o["obligation_id"]
    human_statement, formal, output, machine, budget = descriptions[oid]
    nodes.append({
        "node_id": "THM-M-0985-" + oid.removeprefix("M0985-"), "obligation_id": oid,
        "kind": o["kind"], "human_statement": human_statement, "formal_target": formal,
        "output": output, "human_debt": "H1", "machine_debt": machine,
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source_statement_crosswalk.md" if o["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "anchor_audit.json" if oid in {"M0985-L-PINNED-STRONG-LAW", "M0985-T-ASSEMBLE"} else "none",
        "foundation_profile": "lean4-mathlib-classical/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only declared typed proof children and frozen context.", "inference": human_statement, "output": output, "outgoing_use": "Only declared typed parent edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0985/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional interface only; no root proof credit.",
        "task_ids": [ITEM, "S56-M-0985-PROOF"], "owned_sources": [],
        "owner": "THM-M-0985 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if machine == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor", "toolchain"], "revocation_state": "provisional" if machine == "M0-L" else "open"}
    })

graphs = {name: {"edges": [], "out": {i: [] for i in ids}, "in": {i: [] for i in ids}}
          for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}

def edge(graph, eid, typ, source, target, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": source, "to": target}
    if reciprocal:
        e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e); graphs[graph]["out"][source].append(eid); graphs[graph]["in"][target].append(eid)

requirements = [
    ("M0985-ROOT", "M0985-T-ASSEMBLE"),
    ("M0985-T-ASSEMBLE", "M0985-N-MUTUAL-TO-PAIRWISE"),
    ("M0985-T-ASSEMBLE", "M0985-L-PINNED-STRONG-LAW"),
]
for n, (parent, child) in enumerate(requirements, 1):
    edge("proof", f"P{n}R", "proof_requires", parent, child, f"P{n}C")
    edge("proof", f"P{n}C", "composes", child, parent, f"P{n}R")
for n, child in enumerate(("M0985-S-DEFINITIONS", "M0985-S-BOUNDARY", "M0985-S-FOUNDATION"), 1):
    edge("refinement", f"R{n}", "logical_decomposition", "M0985-ROOT", child)
edge("provenance", "PR1", "provenance_of", "M0985-X-PROVENANCE", "M0985-L-PINNED-STRONG-LAW")
edge("evidence", "E1", "evidence_for", "M0985-X-VALIDATION", "M0985-ROOT")
edge("trust", "TR1", "trusts", "M0985-ROOT", "M0985-S-FOUNDATION")
for n, target in enumerate(ids, 1):
    edge("documentation", f"D{n}", "documents", "M0985-X-SOURCE", target)
edge("workflow", "W1", "workflow_depends_on", "M0985-X-VALIDATION", "M0985-T-ASSEMBLE")

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0985-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0985-ROOT", "edge_direction": "proof_requires parent-to-child; composes child-to-parent",
    "nodes": nodes, "graphs": graphs,
    "mandatory_layer_disposition": {
        "statement": ["M0985-S-DEFINITIONS", "M0985-S-BOUNDARY", "M0985-S-FOUNDATION"],
        "normalization": ["M0985-N-MUTUAL-TO-PAIRWISE"], "branch": "not_applicable: no case split in selected exact anchor route",
        "construction": "not_applicable: no new mathematical object is constructed", "core_lemma": ["M0985-L-PINNED-STRONG-LAW"],
        "external": ["M0985-X-SOURCE", "M0985-X-PROVENANCE", "M0985-X-VALIDATION"], "terminal": ["M0985-T-ASSEMBLE"]
    },
    "closure_boundary": {"root_closed": False, "minimal_open_cut": ["M0985-L-PINNED-STRONG-LAW", "M0985-S-FOUNDATION", "M0985-X-VALIDATION"], "audit_complete": False, "theorem_complete": False}
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
         "recipes": [{"recipe_id": "VAL-" + oid, "scope": oid, "command": "phase-specific validation pending or recorded in obligation-tree-validation.md"} for oid in ids]}
for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2) + "\n")
print(digest)
