#!/usr/bin/env python3
"""Build the rev-5.6 architecture freeze from the retained discovery tree.

The retained dossier is used only for node discovery and decomposition.  This
script deliberately discards every historical status and evidence field.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEGACY = ROOT / "THM-M-0387" / "proof_units.json"

REGISTRY_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def canonical_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def planned_fingerprint(node):
    payload = {
        "id": node["node_id"],
        "kind": node["kind"],
        "human_statement": node["human_statement"],
        "formal_target": node["formal_target"],
        "inputs": node["inputs"],
        "output": node["output"],
    }
    return "planned:v1:sha256:" + canonical_hash(payload)


def edge(edge_id, source, edge_type, target):
    return {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}


legacy = json.loads(LEGACY.read_text())
source_nodes = legacy["nodes"]
ids = [node["node_id"] for node in source_nodes]
assert len(ids) == 132 and len(ids) == len(set(ids))

obligations = []
nodes = []
for source in source_nodes:
    oid = source["node_id"]
    has_children = bool(source["child_ids"])
    is_trust_overlay = oid.startswith("M0387-X")
    is_statement = oid in {"M0387-S-S01", "M0387-S-S02", "M0387-S-S03"}
    risk = "critical" if oid == "M0387-ROOT" or oid.startswith("M0387-WTW") else (
        "high" if has_children or oid.startswith(("M0387-RP", "M0387-B4")) else "normal"
    )
    terminal_body = None
    if is_statement:
        terminal_body = "local:Stage1_Instances/THM-M-0387/Statement.lean"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": (
            "lean-expression-sha256:8e0d406e9e5ba4504c1930352fde324a02df4a30cbfd75f796b9a3d2627113c"
            if oid in {"M0387-ROOT", "M0387-S-S03"} else planned_fingerprint(source)
        ),
        "kind": source["kind"],
        "root_relevant": not is_trust_overlay,
        "machine_eligibility": "required" if not is_trust_overlay else "informational",
        "human_source_eligibility": "required" if not is_trust_overlay else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "typed_trust_or_provenance_overlay" if is_trust_overlay else None,
        "terminal_proof_body_id": terminal_body,
    })

    old_budget = source.get("step_budget")
    budget = "split-required" if has_children else (
        old_budget if isinstance(old_budget, int) and 0 < old_budget <= 100 else 100
    )
    ledger = source.get("step_ledger") or []
    if ledger:
        ledger_text = "; ".join(
            str(item.get("claim", item)) if isinstance(item, dict) else str(item)
            for item in ledger
        )
    else:
        ledger_text = source.get("inputs", "") + "; deliver: " + source.get("output", "")
    nodes.append({
        "node_id": "THM-M-0387-" + oid.removeprefix("M0387-"),
        "obligation_id": oid,
        "kind": source["kind"],
        "human_statement": source["human_statement"],
        "formal_target": source["formal_target"],
        "output": source["output"],
        "human_debt": "H1",
        "machine_debt": "M2" if oid == "M0387-ROOT" else "M4",
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-source-boundary" if oid == "M0387-ROOT" else "not-yet-pinpoint-mapped",
        "provenance_id": terminal_body or "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0/transitive-closure-pending",
        "computation_record": "none",
        "step_budget": budget,
        "semantic_step_ledger": ledger_text,
        "public_readable_target": "Stage1_Instances/THM-M-0387/obligation-tree.md#" + oid.lower().replace(".", ""),
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Architecture record only; no historical proof status or body is admitted by this freeze.",
        "task_ids": ["S56-M-0387-OBLIGATION_TREE", "S56-M-0387-PROOF"],
        "owned_sources": [],
        "owner": "THM-M-0387 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

required_machine = [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"]
required_human = [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"]
required_readable = [o["obligation_id"] for o in obligations if o["readable_eligibility"] == "required"]
projection = [{key: row[key] for key in REGISTRY_FIELDS} for row in obligations]

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-0387-OBLIGATION_TREE",
    "theorem_id": "THM-M-0387",
    "registry_version": 1,
    "freeze_basis": "Section 12.2 mandatory tree recursively expanded using the retained dossier only as discovery input; all historical proof credit was discarded before eligibility was assigned.",
    "root_obligation_id": "M0387-ROOT",
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": required_machine,
        "required_human_source": required_human,
        "required_readable": required_readable,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "denominator_sha256": canonical_hash(projection),
    "delta_policy": "Any split, merge, eligibility change, or exclusion requires registry_version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_edges = []
refinement_edges = []
trust_edges = []
for source in source_nodes:
    parent = source["node_id"]
    for child in source["child_ids"]:
        if parent == "M0387-ROOT" and child == "M0387-X":
            trust_edges.append(edge("TRUST-ROOT-X", parent, "trust_boundary", child))
        elif parent.startswith("M0387-X"):
            trust_edges.append(edge("TRUST-" + parent + "-" + child, parent, "trust_refines", child))
        elif parent.startswith("M0387-S"):
            refinement_edges.append(edge("REF-" + parent + "-" + child, parent, "refines", child))
        else:
            proof_edges.append(edge("PROOF-" + parent + "-" + child, parent, "proof_requires", child))

graph_edges = {
    "proof": proof_edges,
    "refinement": refinement_edges,
    "provenance": [
        edge("PROV-ROOT-AUDIT", "M0387-ROOT", "classified_by", "M0387-X"),
        edge("PROV-RP-PIN", "M0387-RP", "body_boundary", "M0387-X-X.4"),
        edge("PROV-SPECIAL-PIN", "M0387-B3", "body_boundary", "M0387-X-X.3"),
        edge("PROV-B4-PIN", "M0387-B4", "body_boundary", "M0387-X-X.3"),
    ],
    "evidence": [edge("EVID-ROOT-ANCHOR", "M0387-ROOT", "evidence_pending", "M0387-X-IMPERIAL")],
    "trust": trust_edges,
    "documentation": [
        edge("DOC-ROOT-TREE", "M0387-ROOT", "documented_by", "M0387-T"),
        edge("DOC-WTW-TREE", "M0387-WTW", "documented_by", "M0387-T"),
    ],
    "workflow": [
        edge("FLOW-ANCHOR-TREE", "M0387-X", "workflow_precedes", "M0387-ROOT"),
        edge("FLOW-TREE-PROOF", "M0387-ROOT", "workflow_precedes", "M0387-T"),
    ],
}

graphs = {}
for name, edges in graph_edges.items():
    out = {}
    incoming = {}
    for row in edges:
        out.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": out, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": "S56-M-0387-OBLIGATION_TREE",
    "theorem_id": "THM-M-0387",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [],
        "root_machine_debt": "M2",
        "remaining_root_cut_set": ["M0387-WTW"],
        "composition_certificates_checked": [],
        "theorem_complete": False,
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in graph_edges.values())} typed edges")
