#!/usr/bin/env python3
"""Build the frozen THM-M-0322 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0322-OBLIGATION_TREE"
THEOREM = "THM-M-0322"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# Status is deliberately absent here: architecture and eligibility are frozen first.
ROWS = [
    ("M0322-ROOT", "root", "critical", "The exact universe-polymorphic real Krein-Milman equality.", "Stage1Instances.THM_M_0322.KreinMilmanTarget", "The canonical proposition."),
    ("M0322-S-DEFINITIONS", "definition", "high", "Fix real convex hull, topological closure, extreme points, and subset/equality conventions.", "definitions used by Stage1Instances.THM_M_0322.KreinMilmanTarget", "An exact statement interface."),
    ("M0322-S-BOUNDARY", "terminal", "high", "Retain the empty-set case and absence of a nonemptiness premise.", "Stage1Instances.THM_M_0322.empty_boundary", "The checked empty boundary."),
    ("M0322-S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotient, extensionality, kernel, and no-oracle policy.", "planned transitive axiom and trust report", "The accepted foundation boundary."),
    ("M0322-T-ASSEMBLE", "transport", "high", "Combine both exact inclusions by set antisymmetry.", "Stage1Instances.THM_M_0322.root_of_inclusions", "The canonical equality from both inclusions."),
    ("M0322-L-FORWARD", "core_lemma", "normal", "The closed convex hull of the extreme points is contained in the compact convex set.", "Stage1Instances.THM_M_0322.hullExtreme_subset", "closure (convexHull Real (s.extremePoints Real)) ⊆ s."),
    ("M0322-L-REVERSE", "core_lemma", "critical", "Every point of the compact convex set lies in the closed convex hull of its extreme points.", "planned exact reverse-inclusion declaration", "s ⊆ closure (convexHull Real (s.extremePoints Real))."),
    ("M0322-B-OUTSIDE", "branch", "critical", "Assume a point of s lies outside the closed convex hull and expose the contradiction branch.", "planned not_subset witness reduction", "A witness x in s outside the closed convex hull."),
    ("M0322-X-HB-CLOSED-POINT", "bridge", "critical", "Strictly separate the outside point from the closed convex hull by geometric Hahn-Banach.", "geometric_hahn_banach_closed_point", "A continuous linear functional and strict separating bounds."),
    ("M0322-C-MAX-FACE", "construction", "critical", "Choose a maximizer on s and construct its exposed maximizing face with compactness and nonemptiness.", "IsCompact.exists_isMaxOn and IsExposed.isCompact", "A nonempty compact exposed face of s."),
    ("M0322-L-EXTREME-NONEMPTY", "bridge", "critical", "Every nonempty compact subset in the ambient locally convex space has an extreme point.", "IsCompact.extremePoints_nonempty", "An extreme point of the maximizing face."),
    ("M0322-C-ZORN-MINIMAL", "construction", "critical", "Use Zorn to obtain a minimal nonempty closed extreme subset of a compact set.", "zorn_superset plus compact directed-intersection argument", "A minimal nonempty closed extreme subset."),
    ("M0322-B-NONSINGLETON", "branch", "critical", "Assume the minimal extreme subset contains distinct points and derive a smaller extreme subset.", "planned singleton contradiction branch", "The minimal subset is a singleton."),
    ("M0322-X-HB-POINT-POINT", "bridge", "critical", "Separate two distinct points by geometric Hahn-Banach.", "geometric_hahn_banach_point_point", "A continuous linear functional distinguishing the points."),
    ("M0322-C-MINIMAL-FACE", "construction", "high", "Maximize the point-separating functional and form a proper exposed face.", "IsCompact.exists_isMaxOn and IsExposed.isExtreme", "A nonempty proper closed extreme subset contradicting minimality."),
    ("M0322-L-FACE-TRANSFER", "core_lemma", "critical", "Transfer an extreme point of the exposed face to an extreme point of s.", "IsExtreme.extremePoints_subset_extremePoints", "The selected face point belongs to s.extremePoints Real."),
    ("M0322-T-SEPARATION-CONTRA", "terminal", "critical", "Combine face maximality, hull membership, and strict separation to contradict the outside witness.", "planned exact inequality contradiction (linarith in pinned body)", "False, hence the reverse inclusion."),
    ("M0322-X-SOURCE", "terminal", "high", "Map each material node to reviewed primary-source passages and assumptions.", "node-specific primary-source crosswalk pending", "Human-source coverage without machine credit."),
    ("M0322-X-PROVENANCE", "certificate", "critical", "Inventory wrappers, terminal bodies, imports, axioms, licenses, and replay evidence transitively.", "planned provenance and trust closure", "Release provenance without mathematical proof credit."),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M0322-S-DEFINITIONS", "M0322-S-BOUNDARY", "M0322-T-ASSEMBLE", "M0322-L-FORWARD"}
source_na = {"M0322-S-DEFINITIONS", "M0322-S-BOUNDARY", "M0322-S-FOUNDATION", "M0322-X-PROVENANCE"}
machine_special = {"M0322-X-SOURCE": "not_applicable", "M0322-X-PROVENANCE": "informational"}
body_ids = {
    "M0322-L-FORWARD": "local:Stage1_Instances/THM-M-0322/ObligationTree.lean#hullExtreme_subset",
    "M0322-T-ASSEMBLE": "local:Stage1_Instances/THM-M-0322/ObligationTree.lean#root_of_inclusions",
    "M0322-L-EXTREME-NONEMPTY": "mathlib:8a178386:Mathlib.Analysis.Convex.KreinMilman#IsCompact.extremePoints_nonempty",
}

obligations = []
for oid, kind, risk, claim, target, output in ROWS:
    machine = machine_special.get(oid, "required")
    fp = "lean-expression-sha256:785719abddfc881edb6ec8cb60f1175995b433ae42f12727d7d3a1479955579f" if oid == "M0322-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_overlay_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body_ids.get(oid),
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row[0] for row in ROWS]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus pinned mathlib source architecture, expanded through both geometric Hahn-Banach boundaries and the Zorn-minimality proof of extreme-point existence; eligibility assigned independently of closure status.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0322-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0322-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen architecture only. The pinned exact proof is known, but transitive provenance, node validation, source review, and proof-phase acceptance remain open.",
}

nodes = []
for oid, kind, risk, claim, target, output in ROWS:
    nodes.append({
        "node_id": "THM-M-0322-" + oid.removeprefix("M0322-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0322-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": body_ids.get(oid, "none"),
        "foundation_profile": "lean4-mathlib-classical/propext+Classical.choice+Quot.sound/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation, oracle, or unchecked certificate closes this node",
        "step_budget": 100 if oid in {"M0322-L-EXTREME-NONEMPTY", "M0322-L-REVERSE"} else 40,
        "semantic_step_ledger": {"premises": "The exact formal context and incoming proof_requires conclusions only.", "inference": claim, "output": output, "outgoing_use": "Only declared typed proof or support edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0322/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or scoped conditional interface only; no unlisted premise, accepted receipt, or theorem completion.",
        "task_ids": [ITEM, "S56-M-0322-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0322/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0322 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0322-ROOT": ["M0322-T-ASSEMBLE"],
    "M0322-T-ASSEMBLE": ["M0322-L-FORWARD", "M0322-L-REVERSE"],
    "M0322-L-REVERSE": ["M0322-B-OUTSIDE", "M0322-X-HB-CLOSED-POINT", "M0322-C-MAX-FACE", "M0322-L-EXTREME-NONEMPTY", "M0322-L-FACE-TRANSFER", "M0322-T-SEPARATION-CONTRA"],
    "M0322-L-EXTREME-NONEMPTY": ["M0322-C-ZORN-MINIMAL", "M0322-B-NONSINGLETON", "M0322-X-HB-POINT-POINT", "M0322-C-MINIMAL-FACE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0322-ROOT", "logical_decomposition", "M0322-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M0322-ROOT", "logical_decomposition", "M0322-S-BOUNDARY")],
    "provenance": [edge("SRC-REVERSE", "M0322-L-REVERSE", "source_map", "M0322-X-SOURCE"), edge("SRC-LEMMA", "M0322-L-EXTREME-NONEMPTY", "source_map", "M0322-X-SOURCE"), edge("PROV-ROOT", "M0322-X-PROVENANCE", "provenance_of", "M0322-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0322-ROOT", "trusts", "M0322-S-FOUNDATION"), edge("TRUST-PROV", "M0322-ROOT", "trusts", "M0322-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0322-S-DEFINITIONS", "documents", "M0322-ROOT"), edge("DOC-SOURCE", "M0322-X-SOURCE", "documents", "M0322-L-REVERSE")],
    "workflow": [edge("FLOW-ASSEMBLE-FWD", "M0322-T-ASSEMBLE", "workflow_depends_on", "M0322-L-FORWARD"), edge("FLOW-ASSEMBLE-REV", "M0322-T-ASSEMBLE", "workflow_depends_on", "M0322-L-REVERSE"), edge("FLOW-PROV-ASSEMBLE", "M0322-X-PROVENANCE", "workflow_depends_on", "M0322-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0322-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0322-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0322-L-REVERSE", "M0322-S-FOUNDATION", "M0322-X-SOURCE", "M0322-X-PROVENANCE"], "composition_certificates": ["Stage1Instances.THM_M_0322.root_of_inclusions"], "reason": "The exact pinned proof is known but is not credited by this phase; reverse-inclusion node evidence and transitive source/trust/provenance gates remain open."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0322/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
