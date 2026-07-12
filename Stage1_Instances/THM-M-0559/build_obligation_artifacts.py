#!/usr/bin/env python3
"""Build the frozen THM-M-0559 registry and its seven typed graph projections."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(value):
    if isinstance(value, str):
        value = value.encode()
    return hashlib.sha256(value).hexdigest()


def planned(key, statement):
    return f"planned:v1:sha256:{sha(key + ':' + statement)}"


specs = [
    ("M0559-ROOT", "root", "The exact unbased, possibly disconnected WhiteheadTarget.", "Stage1Instances.THM_M_0559.WhiteheadTarget", "The canonical theorem for the given continuous map.", "critical", "required", "required", "required", 100),
    ("M0559-S-DEFINITIONS", "definition", "The induced maps on path components and every positive-dimensional based homotopy group have the frozen quotient definitions.", "zerothHomotopyMap; genLoopMap; homotopyGroupMap; IsWeakHomotopyEquivalence", "The exact weak-equivalence predicate used by the root.", "high", "required", "not_applicable", "required", 70),
    ("M0559-S-SCOPE", "definition", "Preserve two universes, whole-space CW instances, all basepoints, disconnected and empty spaces, and the given map.", "WhiteheadTarget binder and typeclass context", "A scope-faithful context with no connectedness or nonemptiness premise.", "critical", "required", "required", "required", 60),
    ("M0559-S-TRANSPORT", "transport", "Relate the named weak-equivalence target to its fully expanded statement in the checked direction.", "whiteheadTarget_iff_expandedSourceShape", "A checked equivalence with ExpandedSourceShape.", "high", "required", "not_applicable", "required", 20),
    ("M0559-S-FOUNDATION", "certificate", "Audit quotient soundness, function extensionality, classical choice, topology primitives, and every eventual axiom dependency.", "planned axiom and foundation report", "A named foundation policy for all proof nodes.", "critical", "informational", "not_applicable", "required", 60),
    ("M0559-N-COMPONENTS", "reduction", "Reduce the global map to matched path components using the bijection on ZerothHomotopy, without choosing nonexistent points.", "planned component reduction theorem", "Componentwise CW maps and a reconstruction rule for the whole space.", "critical", "required", "required", "required", 100),
    ("M0559-B-EMPTY", "branch", "Discharge empty source and target component boundary cases implied by the component bijection.", "planned empty-space branch theorem", "A homotopy equivalence for the empty boundary case.", "high", "required", "required", "required", 40),
    ("M0559-B-NONEMPTY", "branch", "For a matched nonempty component, choose compatible basepoints and retain every positive homotopy-group isomorphism.", "planned nonempty connected branch theorem", "A based connected weak equivalence on the selected components.", "critical", "required", "required", "required", 80),
    ("M0559-B-MERGE", "bridge", "Prove the empty and nonempty branches exhaustive and reassemble componentwise data without overlap.", "planned branch recomposition theorem", "The complete component reduction conclusion.", "critical", "required", "required", "required", 70),
    ("M0559-C-SKELETON", "construction", "Construct a candidate inverse on successive CW skeleta, including well-definedness and compatibility on attaching boundaries.", "planned skeletal inverse construction", "Compatible partial inverses on every skeleton.", "critical", "required", "required", "required", "split-required"),
    ("M0559-L-EXTENSION", "core_lemma", "Use surjectivity and injectivity on homotopy groups to extend the inverse and kill each obstruction at the next cell dimension.", "planned cellular extension and obstruction lemma", "Each skeletal partial inverse extends while preserving the required homotopy.", "critical", "required", "required", "required", "split-required"),
    ("M0559-L-COLIMIT", "core_lemma", "Pass compatible skeletal constructions to continuous whole-component maps and homotopies.", "planned CW weak-topology colimit lemma", "A continuous inverse and two componentwise homotopies.", "critical", "required", "required", "required", 100),
    ("M0559-T-FORWARD", "terminal", "Package the constructed inverse and homotopies as HomotopyEquiv with forward map definitionally or propositionally equal to the original f.", "planned exact-forward-map packaging theorem", "An e with e.toFun = f, not merely existence of an unrelated equivalence.", "critical", "required", "required", "required", 70),
    ("M0559-T-ASSEMBLE", "transport", "Consume the direct core and yield the exact WhiteheadTarget with no extra premise.", "root_of_directWhiteheadCore", "The canonical root conditional only on DirectWhiteheadCore.", "high", "required", "not_applicable", "required", 20),
    ("M0559-X-SOURCE", "terminal", "Pinpoint a primary proof and crosswalk component reduction, skeletal induction, obstruction killing, and recomposition.", "non-machine primary-source node crosswalk", "Human-source coverage without machine proof credit.", "high", "not_applicable", "required", "required", 80),
    ("M0559-X-EXTERNAL", "bridge", "Map the jzxia external theorem's custom CW complexes and weak-equivalence predicate to this target, or retain it as source-only.", "external WhiteheadTheorem@ee1d4a5; checked bridge absent", "An explicit non-credited external boundary unless every representation transport is checked.", "critical", "informational", "not_applicable", "required", 100),
    ("M0559-X-PROVENANCE", "certificate", "Bind wrappers and future terminal declarations to deduplicated proof-body identities and immutable source revisions.", "planned declaration/proof-body provenance report", "No wrapper or anchor-only double counting.", "critical", "informational", "not_applicable", "required", 60),
    ("M0559-X-TRUST", "certificate", "Record transitive imports, axioms, placeholders, unsafe/oracle boundaries, toolchain, and reproducibility inputs.", "planned trust closure and evidence bundle", "Release-gate trust evidence without semantic proof credit.", "critical", "informational", "not_applicable", "required", 70),
]

obligations = []
for oid, kind, human, formal, output, risk, machine, source, readable, budget in specs:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": (f"lean-statement-json:v1:sha256:{sha((HERE / 'statement.json').read_bytes())}" if oid == "M0559-ROOT" else planned(oid, formal)),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "non_machine_assurance_or_source_boundary", "informational": "assurance_overlay_no_semantic_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0559/ObligationTree.lean#root_of_directWhiteheadCore" if oid == "M0559-T-ASSEMBLE" else None),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))

ids = [row[0] for row in specs]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0559-OBLIGATION_TREE", "theorem_id": "THM-M-0559",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus the completed immutable anchor inventory; eligibility was selected before proof-phase closure inspection.",
    "frozen_against_statement_sha256": sha((HERE / "statement.json").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit-receipt.json").read_bytes()),
    "root_obligation_id": "M0559-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"conditionally_checked_obligations": ["M0559-S-TRANSPORT", "M0559-T-ASSEMBLE"], "accepted_root_machine_debt": "M4"},
    "status_boundary": "Frozen architecture and conditional composition only; the direct core, source review, proof bodies, validation, H0, R0, and theorem completion remain open.",
}

nodes = []
for oid, kind, human, formal, output, risk, machine, source, readable, budget in specs:
    checked = oid in {"M0559-S-TRANSPORT", "M0559-T-ASSEMBLE"}
    nodes.append({
        "node_id": "THM-" + oid, "obligation_id": oid, "kind": kind, "human_statement": human,
        "formal_target": formal, "output": output, "human_debt": "H3", "machine_debt": ("M0-L" if checked else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": ("anchor-audit-jzxia-ee1d4a5" if oid == "M0559-X-EXTERNAL" else ("primary-source-node-map-pending" if source == "required" else "not-applicable")),
        "provenance_id": ("local-conditional-composition" if oid == "M0559-T-ASSEMBLE" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation, evaluator, oracle, or certificate is credited", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only conclusions arriving through declared proof/refinement edges and the frozen formal context.", "inference": human, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0559/obligation-tree.md#{oid.lower()}", "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no open child, source overlay, or external anchor is credited as root proof.",
        "task_ids": ["S56-M-0559-OBLIGATION_TREE", "S56-M-0559-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-0559/ObligationTree.lean"] if oid == "M0559-T-ASSEMBLE" else []),
        "owner": "THM-M-0559 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": ("2026-07-12" if checked else None), "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "statement.json", "anchor-audit-receipt.json", "obligation-registry.json", "toolchain"], "revocation_state": ("provisional" if checked else "open")},
    })

graph_edges = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
counter = 0
def edge(graph, source, target, role):
    global counter
    counter += 1
    graph_edges[graph].append({"edge_id": f"E{counter:03d}", "from": source, "to": target, "type": role})

requirements = [
    ("M0559-ROOT", "M0559-T-ASSEMBLE"), ("M0559-T-ASSEMBLE", "M0559-S-TRANSPORT"), ("M0559-T-ASSEMBLE", "M0559-S-SCOPE"),
    ("M0559-T-ASSEMBLE", "M0559-S-DEFINITIONS"), ("M0559-T-ASSEMBLE", "M0559-N-COMPONENTS"), ("M0559-T-ASSEMBLE", "M0559-T-FORWARD"),
    ("M0559-N-COMPONENTS", "M0559-B-MERGE"), ("M0559-B-MERGE", "M0559-B-EMPTY"), ("M0559-B-MERGE", "M0559-B-NONEMPTY"),
    ("M0559-B-NONEMPTY", "M0559-C-SKELETON"), ("M0559-C-SKELETON", "M0559-L-EXTENSION"),
    ("M0559-L-EXTENSION", "M0559-L-COLIMIT"), ("M0559-T-FORWARD", "M0559-L-COLIMIT"),
]
for parent, child in requirements:
    edge("proof", parent, child, "proof_requires")
    edge("proof", child, parent, "composes")
for parent, child in [("M0559-N-COMPONENTS", "M0559-B-EMPTY"), ("M0559-N-COMPONENTS", "M0559-B-NONEMPTY"), ("M0559-N-COMPONENTS", "M0559-B-MERGE")]:
    edge("refinement", parent, child, "logical_decomposition")
for child in ("M0559-S-DEFINITIONS", "M0559-N-COMPONENTS", "M0559-C-SKELETON", "M0559-L-EXTENSION", "M0559-L-COLIMIT", "M0559-T-FORWARD"):
    edge("provenance", child, "M0559-X-PROVENANCE", "provenance_of")
edge("provenance", "M0559-X-EXTERNAL", "M0559-L-EXTENSION", "source_map")
for child in ("M0559-ROOT", "M0559-N-COMPONENTS", "M0559-C-SKELETON", "M0559-L-EXTENSION", "M0559-L-COLIMIT"):
    edge("evidence", child, "M0559-X-SOURCE", "evidence_for")
for child in ids:
    if child not in {"M0559-S-FOUNDATION", "M0559-X-TRUST"}:
        edge("trust", child, "M0559-X-TRUST", "trusts")
for child in ids:
    edge("documentation", child, "M0559-X-SOURCE", "documents")
for parent, child in requirements:
    edge("workflow", parent, child, "workflow_depends_on")

graphs = {}
for name, edges in graph_edges.items():
    outgoing, incoming = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0559-OBLIGATION_TREE", "theorem_id": "THM-M-0559",
    "registry_id": "THM-M-0559-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M0559-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0559-S-TRANSPORT", "M0559-T-ASSEMBLE"], "remaining_root_cut_set": ["M0559-N-COMPONENTS", "M0559-T-FORWARD"], "root_machine_debt": "M4", "audit_complete": False, "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, ensure_ascii=True, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, ensure_ascii=True, indent=2) + "\n")
print(f"built {len(obligations)} obligations, {counter} typed edges; denominator {denominator}")
