#!/usr/bin/env python3
"""Build the frozen THM-M-0529 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0529-OBLIGATION_TREE"
THEOREM = "THM-M-0529"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0529-ROOT", "root", "critical", "The exact degreewise integral singular-homology invariance target.", "AwesomeTheorems.THM_M_0529.CanonicalTarget", "The canonical proposition."),
    ("M0529-C-MAP", "composition", "critical", "Apply the integral degree-n singular-homology functor to the morphism underlying the homeomorphism-induced TopCat isomorphism.", "AwesomeTheorems.THM_M_0529.map_isIso_of_source_isIso", "IsIso for the exact mapped morphism."),
    ("M0529-B-HOMEO", "bridge", "critical", "Show that the hom morphism of TopCat.isoOfHomeo e carries an IsIso instance.", "CategoryTheory.Iso.isIso_hom applied to TopCat.isoOfHomeo", "IsIso (TopCat.isoOfHomeo e).hom."),
    ("M0529-B-FUNCTOR", "bridge", "high", "Use the generic fact that every functor maps an IsIso morphism to an IsIso morphism.", "CategoryTheory.Functor.map_isIso", "Preservation of IsIso by the exact homology functor."),
    ("M0529-S-STATEMENT", "definition", "high", "Preserve all binders, TopCat domains, integral coefficients, natural degree, and the exact map-level conclusion.", "AwesomeTheorems.THM_M_0529.CanonicalTarget", "Frozen exact statement interface."),
    ("M0529-X-SOURCE", "source_boundary", "high", "Crosswalk the invariance claim and conventions to an accepted primary mathematical source.", "non-machine primary-source crosswalk", "Human-source coverage without proof credit."),
    ("M0529-X-PROVENANCE", "certificate", "critical", "Resolve terminal bodies, imports, transitive declarations, axioms, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
source_na = {"M0529-S-STATEMENT", "M0529-X-PROVENANCE"}
machine_special = {"M0529-X-SOURCE": "not_applicable", "M0529-X-PROVENANCE": "informational"}
obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    machine = machine_special.get(oid, "required")
    fp = ("lean-expression-sha256:346202448f85225bd2460d494524132adb745ad2711c1c4c587a816499c30aea"
          if oid in {"M0529-ROOT", "M0529-S-STATEMENT"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": "THM-M-0529-" + oid.removeprefix("M0529-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M3" if oid == "M0529-ROOT" else ("M0-L" if oid in {"M0529-C-MAP", "M0529-S-STATEMENT"} else "M0-W_candidate" if oid in {"M0529-B-HOMEO", "M0529-B-FUNCTOR"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "conditional-composition-only" if oid == "M0529-C-MAP" else "none",
        "foundation_profile": "lean4-mathlib-classical; terminal audit pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure pending",
        "computation_record": "none; no oracle or external computation",
        "step_budget": 20,
        "semantic_step_ledger": {
            "premises": "Only the typed proof children and the stated formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or support edge may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0529/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no proof-phase root closure is accepted.",
        "task_ids": [ITEM, "S56-M-0529-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0529/ObligationTree.lean"] if oid == "M0529-C-MAP" else [],
        "owner": "THM-M-0529 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in {"M0529-C-MAP", "M0529-S-STATEMENT"} else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in {"M0529-C-MAP", "M0529-S-STATEMENT"} else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable pinned-anchor audit; eligibility frozen before proof-phase acceptance.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0529-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0529-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M0529-C-MAP", "M0529-S-STATEMENT"], "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the later proof node must discharge the bridge and exact root and independently audit provenance.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M0529-ROOT": ["M0529-C-MAP"], "M0529-C-MAP": ["M0529-B-HOMEO", "M0529-B-FUNCTOR"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-STMT", "M0529-ROOT", "logical_decomposition", "M0529-S-STATEMENT")],
    "provenance": [edge("SRC-BRIDGES", "M0529-B-HOMEO", "source_map", "M0529-X-SOURCE"), edge("PROV-ROOT", "M0529-X-PROVENANCE", "provenance_of", "M0529-ROOT")],
    "evidence": [edge("EVID-COMPOSE", "M0529-C-MAP", "evidenced_by", "M0529-X-PROVENANCE")],
    "trust": [edge("TRUST-ROOT", "M0529-ROOT", "trusts", "M0529-X-PROVENANCE")],
    "documentation": [edge("DOC-STMT", "M0529-S-STATEMENT", "documents", "M0529-ROOT"), edge("DOC-SOURCE", "M0529-X-SOURCE", "documents", "M0529-B-HOMEO")],
    "workflow": [edge("FLOW-PROOF-AUDIT", "M0529-C-MAP", "workflow_depends_on", "M0529-X-PROVENANCE"), edge("FLOW-ROOT-COMP", "M0529-ROOT", "workflow_depends_on", "M0529-C-MAP")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0529-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0529-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0529-C-MAP", "M0529-S-STATEMENT"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0529-B-HOMEO", "M0529-B-FUNCTOR"], "composition_certificates": ["AwesomeTheorems.THM_M_0529.map_isIso_of_source_isIso"], "reason": "The checked certificate is conditional; proof-phase acceptance and transitive provenance remain open."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0529/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network": "denied", "covered_ids": [oid], "expected_exit": 0})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
