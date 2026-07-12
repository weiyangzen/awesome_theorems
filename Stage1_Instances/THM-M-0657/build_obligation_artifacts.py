#!/usr/bin/env python3
"""Generate THM-M-0657 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0657-OBLIGATION_TREE"
THEOREM = "THM-M-0657"
PREFIX = "M0657-"

# These are semantic packages, not claims of closure. The modern stability/
# saturation route is frozen provisionally pending a primary-source node map.
ROWS = [
    ("M0657-ROOT", "root", "The exact countable-language uncountable-categoricity transfer target.", "Stage1Instances.THM_M_0657.MorleyCategoricityTarget", "critical", "required", "required"),
    ("M0657-S-ENCODING", "definition", "Audit language countability, bundled models, exact cardinality, nonvacuous categoricity, universes, and structure isomorphism.", "Stage1Instances.THM_M_0657.{HasModelCardinality,CategoricalWithExistence}", "critical", "required", "not_applicable"),
    ("M0657-N-SOURCE-SHAPE", "transport", "Transport between a selected source cardinal and the checked existential-source formulation.", "Stage1Instances.THM_M_0657.morleyCategoricityTarget_iff_existentialSourceShape", "high", "required", "required"),
    ("M0657-L-COMPLETENESS", "reduction", "Derive the complete-theory working context from categoricity plus an uncountable model without adding completeness to the root.", "planned Los-Vaught completeness reduction at the exact root assumptions", "critical", "required", "required"),
    ("M0657-C-MORLEY-RANK", "construction", "Develop the countable-language type/rank apparatus used to control definable sets and types.", "planned Morley-rank and degree construction", "critical", "required", "required"),
    ("M0657-L-STABILITY", "core_lemma", "Derive the required stability bound from categoricity in the selected uncountable cardinal.", "planned categoricity-to-stability theorem", "critical", "required", "required"),
    ("M0657-L-SATURATION", "core_lemma", "Show every model of the theory in an arbitrary uncountable target cardinal is saturated at the strength required for uniqueness.", "planned uncountable-model saturation transfer", "critical", "required", "required"),
    ("M0657-C-EXISTENCE", "construction", "Construct a model of each requested uncountable target cardinal, with exact cardinality, using audited Löwenheim-Skolem/chain steps.", "planned exact-cardinality target-model construction", "critical", "required", "required"),
    ("M0657-L-SATURATED-ISO", "core_lemma", "Prove that two saturated models of the complete theory with the same uncountable cardinality are isomorphic as language structures.", "planned saturated-model back-and-forth uniqueness theorem", "critical", "required", "required"),
    ("M0657-T-TARGET-CAT", "terminal", "Combine target-model existence and pairwise isomorphism into CategoricalWithExistence at an arbitrary uncountable target cardinal.", "planned target-cardinal categoricity package", "critical", "required", "required"),
    ("M0657-T-ASSEMBLE", "transport", "Abstract the binders and return the exact canonical MorleyCategoricityTarget.", "Stage1Instances.THM_M_0657.root_of_transferPackage", "high", "required", "required"),
    ("M0657-X-SOURCE", "certificate", "Map every substantive package to an inspected primary proof, assumptions, terminology, and errata before assigning H0.", "primary source node map pending", "critical", "not_applicable", "required"),
    ("M0657-X-FOUNDATION", "certificate", "Audit classical choice, quotients, cardinal arithmetic, compactness/completeness machinery, Lean TCB, and reproducibility boundaries.", "planned foundation and transitive-axiom report", "critical", "required", "not_applicable"),
    ("M0657-X-PROVENANCE", "certificate", "Record terminal bodies, immutable origins, licenses, receipts, freshness, and revocation state without creating proof credit.", "planned provenance ledger", "critical", "informational", "not_applicable"),
]

PROOF_REQUIRES = [
    ("M0657-ROOT", "M0657-T-ASSEMBLE"),
    ("M0657-T-ASSEMBLE", "M0657-T-TARGET-CAT"),
    ("M0657-T-TARGET-CAT", "M0657-C-EXISTENCE"),
    ("M0657-T-TARGET-CAT", "M0657-L-SATURATED-ISO"),
    ("M0657-L-SATURATED-ISO", "M0657-L-SATURATION"),
    ("M0657-L-SATURATION", "M0657-L-STABILITY"),
    ("M0657-L-STABILITY", "M0657-C-MORLEY-RANK"),
    ("M0657-L-STABILITY", "M0657-L-COMPLETENESS"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())


statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, risk, machine, human_source in ROWS:
    checked = oid in {"M0657-ROOT", "M0657-S-ENCODING", "M0657-N-SOURCE-SHAPE"}
    exclusion = None
    if oid == "M0657-X-SOURCE":
        exclusion = "human_source_boundary_only"
    elif oid == "M0657-X-PROVENANCE":
        exclusion = "release_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if checked else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human_source,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0657/ObligationTree.lean#root_of_transferPackage" if oid == "M0657-T-ASSEMBLE" else None),
    })

denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
ids = [row[0] for row in ROWS]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and bounded anchor audit; a modern completeness, stability, saturation, existence, and saturated-uniqueness architecture frozen before proof closure observation. Primary-source alignment remains an explicit open obligation.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0657-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0657-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, route replacement, or eligibility change requires registry v2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, risk, machine, human_source in ROWS:
    checked_interface = oid in {"M0657-S-ENCODING", "M0657-N-SOURCE-SHAPE", "M0657-T-ASSEMBLE"}
    machine_debt = "M3" if oid in {"M0657-ROOT", "M0657-S-ENCODING", "M0657-N-SOURCE-SHAPE", "M0657-T-ASSEMBLE"} else "M4"
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": human,
        "formal_target": formal,
        "output": human,
        "human_debt": "H1",
        "machine_debt": machine_debt,
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "morley-1965-node-map-pending" if human_source == "required" else "not-applicable",
        "provenance_id": "none",
        "foundation_profile": "lean4-mathlib-classical/model-theory-transitive-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no experiment, oracle, or generated result may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only the exact formal context and declared proof_requires children; source/trust/workflow edges are not premises.",
            "inference": human,
            "output": human,
            "outgoing_use": "Consumed only by the declared typed parent edge or by non-proof audit edges.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0657/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen project-level interface only; no open semantic package or exact root proof is supplied.",
        "task_ids": [ITEM, "S56-M-0657-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-0657/Statement.lean"] if oid in {"M0657-S-ENCODING", "M0657-N-SOURCE-SHAPE"} else (["Stage1_Instances/THM-M-0657/ObligationTree.lean"] if oid == "M0657-T-ASSEMBLE" else [])),
        "owner": "THM-M-0657 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if checked_interface else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "source map", "toolchain"],
            "revocation_state": "provisional" if checked_interface else "open",
        },
    })


def graph(edge_rows):
    out = {oid: [] for oid in ids}
    incoming = {oid: [] for oid in ids}
    for edge in edge_rows:
        out[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edge_rows, "out": out, "in": incoming}


proof_edges = []
for i, (parent, child) in enumerate(PROOF_REQUIRES, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges.extend([
        {"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req},
    ])


def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]


graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [
        ("M0657-ROOT", "M0657-S-ENCODING"),
        ("M0657-ROOT", "M0657-N-SOURCE-SHAPE"),
        ("M0657-L-STABILITY", "M0657-C-MORLEY-RANK"),
        ("M0657-T-TARGET-CAT", "M0657-C-EXISTENCE"),
        ("M0657-T-TARGET-CAT", "M0657-L-SATURATED-ISO"),
    ])),
    "provenance": graph(edges("V", "provenance_of", [("M0657-X-PROVENANCE", oid) for oid in ids if oid != "M0657-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0657-X-SOURCE", oid) for oid in ids if oid not in {"M0657-X-SOURCE", "M0657-X-FOUNDATION", "M0657-X-PROVENANCE", "M0657-S-ENCODING"}])),
    "trust": graph(edges("T", "trusts", [(oid, "M0657-X-FOUNDATION") for oid in ["M0657-ROOT", "M0657-L-COMPLETENESS", "M0657-L-STABILITY", "M0657-L-SATURATION", "M0657-C-EXISTENCE", "M0657-L-SATURATED-ISO", "M0657-T-ASSEMBLE"]])),
    "documentation": graph(edges("D", "documents", [("M0657-X-SOURCE", "M0657-ROOT"), ("M0657-X-PROVENANCE", "M0657-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0657-ROOT", "M0657-X-SOURCE"), ("M0657-ROOT", "M0657-X-FOUNDATION"), ("M0657-ROOT", "M0657-X-PROVENANCE")])),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-0657-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M0657-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": ["M0657-C-EXISTENCE", "M0657-C-MORLEY-RANK", "M0657-L-COMPLETENESS", "M0657-X-SOURCE", "M0657-X-FOUNDATION"],
        "note": "The terminal Lean identity checks the output type only and is not proof closure.",
    },
}

recipes = [{
    "recipe_id": "VAL-" + oid,
    "obligation_id": oid,
    "state": "provisional_interface" if oid in {"M0657-S-ENCODING", "M0657-N-SOURCE-SHAPE", "M0657-T-ASSEMBLE"} else "open",
    "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"],
} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
