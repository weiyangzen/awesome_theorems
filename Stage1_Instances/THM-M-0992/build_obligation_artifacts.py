#!/usr/bin/env python3
"""Build the frozen THM-M-0992 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0992-OBLIGATION_TREE"
THEOREM = "THM-M-0992"


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def fingerprint(text):
    return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()


rows = [
    ("M0992-ROOT", "root", "required", "required", "required", "critical", None),
    ("M0992-S-STATEMENT", "definition", "required", "not_applicable", "required", "high", None),
    ("M0992-B-PROB-FINITE", "transport", "required", "required", "required", "high", None),
    ("M0992-A-VARIANCE", "terminal", "required", "required", "required", "critical", "mathlib:ProbabilityTheory.meas_ge_le_variance_div_sq@8a178386ffc0f5fef0b77738bb5449d50efeea95"),
    ("M0992-T-COMPOSE", "transport", "required", "required", "required", "critical", "local:ObligationTree.lean#root_of_varianceAnchorPackage"),
    ("M0992-X-SOURCE", "source_boundary", "not_applicable", "required", "required", "high", None),
    ("M0992-X-PROVENANCE", "certificate", "informational", "not_applicable", "required", "critical", None),
    ("M0992-X-TRUST", "certificate", "informational", "not_applicable", "required", "critical", None),
]

obligations = []
for oid, kind, machine, human, readable, risk, body in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": (
            "lean-expression-sha256:b162195bc3a51eba84565f1c454e9005c8fec36f2e4f9e502a4ac6e8742cb8e2"
            if oid in {"M0992-ROOT", "M0992-S-STATEMENT"} else fingerprint(oid)
        ),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": machine, "human_source_eligibility": human,
        "readable_eligibility": readable, "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "non_machine_boundary", "informational": "release_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": body,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus immutable anchor audit, before downstream proof acceptance or closure metrics.",
    "frozen_against_statement_sha256": sha("Statement.lean"),
    "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M0992-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {
        "checked_interfaces": ["M0992-S-STATEMENT", "M0992-B-PROB-FINITE", "M0992-T-COMPOSE"],
        "candidate_only": ["M0992-A-VARIANCE"], "root_machine_debt": "M0-W candidate pending proof acceptance"
    },
    "status_boundary": "Architecture and conditional composition only; no proof-node acceptance, H0 source receipt, trust closure, or theorem completion."
}

descriptions = {
    "M0992-ROOT": ("The exact real-valued probability-space Chebyshev target.", "Stage1Instances.THM_M_0992.ChebyshevTarget", "M0-W candidate"),
    "M0992-S-STATEMENT": ("Preserve universes, binders, MemLp 2, positive real threshold, closed deviation event, and ENNReal variance quotient.", "Stage1Instances.THM_M_0992.ChebyshevTarget", "M0-L"),
    "M0992-B-PROB-FINITE": ("Discharge the anchor's finite-measure typeclass from IsProbabilityMeasure without changing the theorem.", "IsProbabilityMeasure P -> IsFiniteMeasure P", "M0-L"),
    "M0992-A-VARIANCE": ("Supply the exact pinned finite-measure variance tail theorem.", "ProbabilityTheory.meas_ge_le_variance_div_sq", "M0-W candidate"),
    "M0992-T-COMPOSE": ("Compose the exact anchor package and probability-to-finite instance into the frozen root.", "Stage1Instances.THM_M_0992.root_of_varianceAnchorPackage", "M0-L"),
    "M0992-X-SOURCE": ("Crosswalk every mathematical assumption and conclusion to a primary human proof source.", "human source receipt pending", "M4"),
    "M0992-X-PROVENANCE": ("Audit terminal-body identity, aliases, immutable revision, and transitive provenance.", "provenance receipt pending", "M4"),
    "M0992-X-TRUST": ("Audit the full axiom, TCB, foundation, computation, and no-oracle boundary.", "trust receipt pending", "M4"),
}
nodes = []
for row in obligations:
    oid = row["obligation_id"]
    human, formal, debt = descriptions[oid]
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0992-"), "obligation_id": oid,
        "kind": row["kind"], "human_statement": human, "formal_target": formal,
        "output": "The declared typed interface or audit certificate.",
        "human_debt": "H3", "machine_debt": debt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "pending" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": row["terminal_proof_body_id"] or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no external computation or oracle may close this node",
        "step_budget": 20,
        "semantic_step_ledger": {"premises": "Only typed proof_requires children and the formal context.", "inference": human, "output": "The declared typed interface or audit certificate.", "outgoing_use": "Only declared reciprocal composition or non-proof support edges may consume it."},
        "public_readable_target": "Stage1_Instances/THM-M-0992/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; downstream acceptance remains open.",
        "task_ids": [ITEM, "S56-M-0992-PROOF"], "owned_sources": [],
        "owner": "THM-M-0992 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in {"M0992-S-STATEMENT", "M0992-B-PROB-FINITE", "M0992-T-COMPOSE"} else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor pin", "toolchain"], "revocation_state": "provisional" if oid in {"M0992-S-STATEMENT", "M0992-B-PROB-FINITE", "M0992-T-COMPOSE"} else "open"}
    })

def graph(edge_specs):
    edges, out, incoming = [], {}, {}
    for eid, source, typ, target, *reciprocal in edge_specs:
        edge = {"edge_id": eid, "from": source, "type": typ, "to": target}
        if reciprocal: edge["reciprocal_edge_id"] = reciprocal[0]
        edges.append(edge); out.setdefault(source, []).append(eid); incoming.setdefault(target, []).append(eid)
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("M0992-ROOT", "M0992-T-COMPOSE"), ("M0992-T-COMPOSE", "M0992-B-PROB-FINITE"), ("M0992-T-COMPOSE", "M0992-A-VARIANCE")]
proof_specs = []
for parent, child in proof_pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_specs += [(req, parent, "proof_requires", child, comp), (comp, child, "composes", parent, req)]
graphs = {
    "proof": graph(proof_specs),
    "refinement": graph([("REF-ROOT-STATEMENT", "M0992-ROOT", "logical_decomposition", "M0992-S-STATEMENT")]),
    "provenance": graph([("SRC-ANCHOR", "M0992-A-VARIANCE", "source_map", "M0992-X-SOURCE"), ("PROV-ANCHOR", "M0992-X-PROVENANCE", "provenance_of", "M0992-A-VARIANCE")]),
    "evidence": graph([]),
    "trust": graph([("TRUST-ROOT", "M0992-ROOT", "trusts", "M0992-X-TRUST"), ("TRUST-PROV", "M0992-ROOT", "trusts", "M0992-X-PROVENANCE")]),
    "documentation": graph([("DOC-STATEMENT", "M0992-S-STATEMENT", "documents", "M0992-ROOT"), ("DOC-SOURCE", "M0992-X-SOURCE", "documents", "M0992-A-VARIANCE")]),
    "workflow": graph([("FLOW-PROOF-ARCH", "M0992-A-VARIANCE", "workflow_depends_on", "M0992-T-COMPOSE"), ("FLOW-PROV-PROOF", "M0992-X-PROVENANCE", "workflow_depends_on", "M0992-A-VARIANCE"), ("FLOW-TRUST-PROV", "M0992-X-TRUST", "workflow_depends_on", "M0992-X-PROVENANCE")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0992-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0992-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"checked_interfaces": ["M0992-S-STATEMENT", "M0992-B-PROB-FINITE", "M0992-T-COMPOSE"], "candidate_only": ["M0992-A-VARIANCE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0992-A-VARIANCE", "M0992-X-SOURCE", "M0992-X-PROVENANCE", "M0992-X-TRUST"], "composition_certificates": ["Stage1Instances.THM_M_0992.root_of_varianceAnchorPackage"], "reason": "The exact anchor is inventoried but has not received downstream proof, source, provenance, and trust acceptance."}
}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(denominator)
