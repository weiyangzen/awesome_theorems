#!/usr/bin/env python3
"""Build the frozen THM-M-0082 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0082-OBLIGATION_TREE"
THEOREM = "THM-M-0082"

specs = [
    ("M0082-ROOT", "root", "Exact explicit-hypothesis general right-adjoint target.", "Stage1Instances.THM_M_0082.GeneralRightAdjointTarget", "The canonical proposition.", "required", "required", "critical", "M3"),
    ("M0082-S-DEFINITIONS", "definition", "Freeze SolutionSetCondition, HasLimits, preservation, and IsRightAdjoint notation.", "definitions used by GeneralRightAdjointTarget", "The exact statement vocabulary.", "required", "not_applicable", "high", "M0-L"),
    ("M0082-S-UNIVERSES", "terminal", "Preserve independent object and morphism universes and the vD-small solution family.", "GeneralRightAdjointTarget.{vC,vD,uC,uD}", "The exact universe and typeclass context.", "required", "not_applicable", "critical", "M0-L"),
    ("M0082-S-BOUNDARY", "terminal", "Add no nonempty, well-powered, coseparating, or equal-universe premise.", "statement mutation and boundary policy", "The accepted degenerate-case scope.", "required", "not_applicable", "high", "M0-L"),
    ("M0082-S-TRANSPORT", "transport", "Transport explicit completeness and preservation values to the typeclass-shaped bridge.", "Stage1Instances.THM_M_0082.ObligationTree.root_of_bridge", "Exact canonical root from the bridge.", "required", "not_applicable", "critical", "M0-L"),
    ("M0082-X-BRIDGE", "bridge", "The pinned general adjoint functor theorem at its exact type.", "CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition", "G.IsRightAdjoint.", "required", "required", "critical", "M4"),
    ("M0082-C-STRUCTURED", "construction", "For each A, reduce right-adjoint existence to an initial object of StructuredArrow A G.", "isRightAdjointOfStructuredArrowInitials", "Initial-object obligations for all structured-arrow categories.", "required", "required", "critical", "M4"),
    ("M0082-C-SOLUTION-FAMILY", "construction", "Turn the solution-set witnesses into structured arrows B' with a morphism to every object.", "SolutionSetCondition and StructuredArrow.mk/homMk", "A small weakly initial family in StructuredArrow A G.", "required", "required", "high", "M4"),
    ("M0082-L-WEAKLY-INITIAL", "core_lemma", "Use products to combine the small weakly initial family into one weakly initial object.", "has_weakly_initial_of_weakly_initial_set_and_hasProducts", "A weakly initial structured arrow.", "required", "required", "critical", "M4"),
    ("M0082-L-INITIAL", "core_lemma", "Use wide equalizers to refine a weakly initial object to an initial object.", "hasInitial_of_weakly_initial_and_hasWideEqualizers", "An initial structured arrow.", "required", "required", "critical", "M4"),
    ("M0082-S-FOUNDATION", "certificate", "Freeze classical choice, quotient, extensionality, kernel, and no-oracle boundaries.", "transitive #print axioms and trust inventory", "Accepted foundation and TCB profile.", "informational", "not_applicable", "critical", "M4"),
    ("M0082-X-SOURCE", "terminal", "Map every proof transition to pinpoint primary sources and errata.", "planned human-source crosswalk", "Accepted node-level human provenance.", "not_applicable", "required", "high", "M4"),
    ("M0082-X-PROVENANCE", "certificate", "Bind wrapper, terminal body, imports, revision, license, and replay evidence.", "planned transitive provenance receipt", "Accepted terminal-body provenance.", "informational", "not_applicable", "critical", "M4"),
]

def planned(text):
    return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = []
for oid, kind, human, formal, output, machine, human_source, risk, _debt in specs:
    rows.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-expression-sha256:7650acd20b1eb8822d24997cddb64fd35dd1a316cee5976171588cf4bc5c541f" if oid == "M0082-ROOT" else planned(formal)),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human_source,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_or_governance_boundary", "informational": "release_overlay_no_independent_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0082/ObligationTree.lean#root_of_bridge" if oid == "M0082-S-TRANSPORT" else ("mathlib:8a178386:CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition" if oid == "M0082-X-BRIDGE" else None)),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit, expanded through every central construction and imported theorem used by the pinned terminal body; eligibility assigned before proof integration.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0082-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in rows],
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in rows],
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version with an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for oid, kind, human, formal, output, _machine, human_source, _risk, debt in specs:
    nodes.append({
        "node_id": "THM-M-0082-" + oid.removeprefix("M0082-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if human_source == "not_applicable" else "pinpoint-primary-source-map-pending",
        "provenance_id": "anchor-audit-candidate" if oid == "M0082-X-BRIDGE" else "none",
        "foundation_profile": "lean4-dependent-type-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no solver, oracle, or finite computation",
        "step_budget": 35 if oid not in {"M0082-X-BRIDGE", "M0082-C-STRUCTURED"} else 80,
        "semantic_step_ledger": {"premises": "Only the exact typed children and frozen formal context.", "inference": human, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0082/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional composition only; no open child, source boundary, or trust overlay is thereby closed.",
        "task_ids": [ITEM, "S56-M-0082-PROOF"], "owned_sources": (["Stage1_Instances/THM-M-0082/ObligationTree.lean"] if oid == "M0082-S-TRANSPORT" else []),
        "owner": "THM-M-0082 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if debt == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor", "toolchain"], "revocation_state": "provisional" if debt == "M0-L" else "open"},
    })

graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
graphs = {name: {"edges": [], "out": {}, "in": {}} for name in graph_names}
edge_counter = 0
def edge(graph, src, dst, typ, reciprocal=None):
    global edge_counter
    edge_counter += 1
    eid = f"E{edge_counter:03d}"
    row = {"edge_id": eid, "from": src, "to": dst, "type": typ}
    if reciprocal: row["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(row)
    graphs[graph]["out"].setdefault(src, []).append(eid)
    graphs[graph]["in"].setdefault(dst, []).append(eid)
    return eid
def proof_pair(parent, child):
    global edge_counter
    first = f"E{edge_counter + 1:03d}"; second = f"E{edge_counter + 2:03d}"
    edge("proof", parent, child, "proof_requires", second)
    edge("proof", child, parent, "composes", first)

proof_pair("M0082-ROOT", "M0082-S-TRANSPORT")
proof_pair("M0082-S-TRANSPORT", "M0082-X-BRIDGE")
for child in ("M0082-C-STRUCTURED", "M0082-C-SOLUTION-FAMILY", "M0082-L-WEAKLY-INITIAL", "M0082-L-INITIAL"):
    edge("refinement", "M0082-X-BRIDGE", child, "logical_decomposition")
for child in ("M0082-S-DEFINITIONS", "M0082-S-UNIVERSES", "M0082-S-BOUNDARY"):
    edge("refinement", "M0082-ROOT", child, "expository_decomposition")
edge("provenance", "M0082-X-PROVENANCE", "M0082-X-BRIDGE", "provenance_of")
edge("evidence", "M0082-X-BRIDGE", "M0082-X-SOURCE", "source_map")
edge("trust", "M0082-ROOT", "M0082-S-FOUNDATION", "trusts")
for oid, *_ in specs: edge("documentation", oid, oid, "documents")
for oid, *_ in specs:
    if oid != "M0082-ROOT": edge("workflow", "M0082-ROOT", oid, "workflow_depends_on")

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0082-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0082-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "closed_obligations": ["M0082-S-DEFINITIONS", "M0082-S-UNIVERSES", "M0082-S-BOUNDARY", "M0082-S-TRANSPORT"], "remaining_root_cut_set": ["M0082-X-BRIDGE"], "human_source_cut_set": ["M0082-X-SOURCE"], "release_overlays_open": ["M0082-S-FOUNDATION", "M0082-X-PROVENANCE"], "audit_complete": False, "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(digest)
