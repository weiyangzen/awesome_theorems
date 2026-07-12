#!/usr/bin/env python3
"""Generate the frozen THM-M-0324 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0324-OBLIGATION_TREE"
THEOREM = "THM-M-0324"
PREFIX = "M0324-"

# The architecture is frozen before proof work. Planned signatures are
# deliberately descriptive where the primary-source formulation is still open.
ROWS = [
    ("M0324-ROOT", "root", "The exact selected existential no-Schauder-basis target.", "Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget", "critical", "required", "required"),
    ("M0324-S-ENCODING", "definition", "Audit the bundled real Banach-space carrier, universe, separability, infinite dimension, and countable Schauder-basis encoding.", "Stage1Instances.THM_M_0324.{RealBanachSpace,EnfloNoSchauderBasisTarget}", "critical", "required", "not_applicable"),
    ("M0324-D-APPROX", "definition", "Select and crosswalk the exact approximation-property formulation used by Enflo, including topology and finite-rank operator conventions.", "planned exact approximation-property predicate after primary-source review", "critical", "required", "required"),
    ("M0324-C-SPACE", "construction", "Construct the specific real counterexample space with the structure required by the source argument.", "planned Enflo counterexample carrier and construction data", "critical", "required", "required"),
    ("M0324-C-BANACH", "construction", "Prove the constructed carrier is a complete real normed vector space and package it as RealBanachSpace.", "planned RealBanachSpace witness", "critical", "required", "required"),
    ("M0324-L-SEPARABLE", "lemma", "Prove the constructed Banach space is separable without using nonseparability as a basis obstruction.", "planned TopologicalSpace.SeparableSpace witness.carrier", "high", "required", "required"),
    ("M0324-L-INFINITE", "lemma", "Prove the constructed Banach space is not finite-dimensional.", "planned Not (FiniteDimensional Real witness.carrier)", "high", "required", "required"),
    ("M0324-L-NO-AP", "core_lemma", "Prove the constructed space fails the exact frozen approximation-property predicate by Enflo's construction.", "planned Not (ApproximationProperty witness.carrier)", "critical", "required", "required"),
    ("M0324-L-BASIS-TO-AP", "bridge", "Prove that a countable Schauder basis supplies the exact approximation property through finite-rank partial-sum projections.", "planned Nonempty (SchauderBasis Real X) -> ApproximationProperty X", "critical", "required", "required"),
    ("M0324-L-PROJECTIONS", "lemma", "Verify that Schauder partial-sum projections are finite-rank and converge in the topology required by the selected approximation property.", "mathlib SchauderBasis.proj/tendsto_proj and GeneralSchauderBasis.finrank_range_proj bridge", "critical", "required", "required"),
    ("M0324-T-NO-BASIS", "transport", "Combine failure of approximation with basis-implies-approximation to exclude every countable Schauder basis.", "Stage1Instances.THM_M_0324.noBasis_of_basis_implies_property", "high", "required", "required"),
    ("M0324-T-ASSEMBLE", "transport", "Package the constructed Banach space and its three properties into the exact existential root.", "Stage1Instances.THM_M_0324.root_of_witness", "high", "required", "required"),
    ("M0324-X-SOURCE", "source_boundary", "Map every construction and analytic inference to inspected primary-source theorem text, assumptions, pages, and errata.", "primary-source node map pending exact theorem-text review", "critical", "not_applicable", "required"),
    ("M0324-X-FOUNDATION", "certificate", "Audit classical choice, quotient/completion use, imported axioms, kernel dependencies, and computation boundaries.", "planned foundation and axiom report", "critical", "required", "not_applicable"),
    ("M0324-X-PROVENANCE", "certificate", "Record every terminal body, immutable revision, license, receipt, invalidation input, and revocation.", "planned provenance ledger", "critical", "informational", "not_applicable"),
]

PROOF_REQUIRES = [
    ("M0324-ROOT", "M0324-T-ASSEMBLE"),
    ("M0324-T-ASSEMBLE", "M0324-C-SPACE"),
    ("M0324-T-ASSEMBLE", "M0324-C-BANACH"),
    ("M0324-T-ASSEMBLE", "M0324-L-SEPARABLE"),
    ("M0324-T-ASSEMBLE", "M0324-L-INFINITE"),
    ("M0324-T-ASSEMBLE", "M0324-T-NO-BASIS"),
    ("M0324-T-NO-BASIS", "M0324-L-NO-AP"),
    ("M0324-T-NO-BASIS", "M0324-L-BASIS-TO-AP"),
    ("M0324-L-NO-AP", "M0324-D-APPROX"),
    ("M0324-L-BASIS-TO-AP", "M0324-D-APPROX"),
    ("M0324-L-BASIS-TO-AP", "M0324-L-PROJECTIONS"),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
ids = [row[0] for row in ROWS]
obligations = []
for oid, kind, human, formal, risk, machine, source in ROWS:
    terminal = None
    if oid == "M0324-T-NO-BASIS":
        terminal = "local:Stage1_Instances/THM-M-0324/ObligationTree.lean#noBasis_of_basis_implies_property"
    elif oid == "M0324-T-ASSEMBLE":
        terminal = "local:Stage1_Instances/THM-M-0324/ObligationTree.lean#root_of_witness"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if oid in {"M0324-ROOT", "M0324-S-ENCODING"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0324-X-SOURCE" else ("release_overlay_no_proof_credit" if oid == "M0324-X-PROVENANCE" else None),
        "terminal_proof_body_id": terminal,
    })

denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated conservative statement and bounded anchor audit; Enflo-construction plus approximation-property contradiction architecture selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0324-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0324-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, target change, exclusion, or eligibility change requires a new version and append-only old/new ID delta; old denominators remain reportable.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, risk, machine, source in ROWS:
    checked = oid in {"M0324-S-ENCODING", "M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": human,
        "formal_target": formal,
        "output": human,
        "human_debt": "H1" if oid in {"M0324-ROOT", "M0324-X-SOURCE"} else "H2",
        "machine_debt": "M0-L" if oid in {"M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"} else ("M3" if oid in {"M0324-ROOT", "M0324-S-ENCODING"} else "M4"),
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if source == "required" else "not-applicable",
        "provenance_id": "local-composition-body" if checked and oid != "M0324-S-ENCODING" else "none",
        "foundation_profile": "lean4-mathlib; construction-level classical/choice/quotient audit pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive terminal closure pending",
        "computation_record": "none; no experiment, oracle, or external computation is credited",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only the exact typed proof-requires children listed in the proof graph.",
            "inference": human,
            "output": human,
            "source_anchors": "Primary-source pinpoint pending for source-eligible nodes; pinned mathlib anchors are recorded in anchor-audit.json.",
            "outgoing_use": "Only typed parent composition or separately typed support edges may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0324/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface" + (" with a checked local logical composition body; substantive children remain open." if checked else "; no proof closure or source acceptance is supplied."),
        "task_ids": [ITEM, "S56-M-0324-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0324/ObligationTree.lean"] if oid in {"M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"} else [],
        "owner": "THM-M-0324 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["canonical statement", "registry", "primary-source map", "toolchain", "terminal body"],
            "revocation_state": "provisional" if checked else "open",
        },
    })

def graph(edges):
    out = {oid: [] for oid in ids}
    incoming = {oid: [] for oid in ids}
    for edge in edges:
        out[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

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
        ("M0324-ROOT", "M0324-S-ENCODING"),
        ("M0324-C-SPACE", "M0324-C-BANACH"),
        ("M0324-L-BASIS-TO-AP", "M0324-L-PROJECTIONS"),
    ])),
    "provenance": graph(edges("V", "provenance_of", [("M0324-X-PROVENANCE", oid) for oid in ids if oid != "M0324-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0324-X-SOURCE", oid) for oid in ["M0324-C-SPACE", "M0324-C-BANACH", "M0324-L-SEPARABLE", "M0324-L-INFINITE", "M0324-L-NO-AP", "M0324-L-BASIS-TO-AP"]])),
    "trust": graph(edges("T", "trusts", [(oid, "M0324-X-FOUNDATION") for oid in ["M0324-ROOT", "M0324-C-SPACE", "M0324-L-NO-AP", "M0324-L-BASIS-TO-AP", "M0324-T-ASSEMBLE"]])),
    "documentation": graph(edges("D", "documents", [("M0324-X-SOURCE", "M0324-ROOT"), ("M0324-X-PROVENANCE", "M0324-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0324-ROOT", oid) for oid in ["M0324-X-SOURCE", "M0324-X-FOUNDATION", "M0324-X-PROVENANCE"]])),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-0324-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M0324-ROOT",
    "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent; non-proof graphs confer no proof credit.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": ["M0324-D-APPROX", "M0324-C-SPACE", "M0324-X-SOURCE", "M0324-X-FOUNDATION"],
        "checked_compositions": ["M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"],
    },
}

recipes = []
for oid in ids:
    recipes.append({
        "recipe_id": "VAL-" + oid,
        "cwd": "Stage1_Instances/THM-M-0324",
        "argv": ["python3", "check_obligation_tree.py"] if oid not in {"M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"} else ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0324/ObligationTree.lean"],
        "env_allowlist": {},
        "timeout_seconds": 120,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "receipt-bound at execution"}],
        "covered_obligation_ids": [oid],
        "covered_declarations": ["Stage1Instances.THM_M_0324.noBasis_of_basis_implies_property", "Stage1Instances.THM_M_0324.root_of_witness"] if oid in {"M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"} else [],
        "state": "provisional" if oid in {"M0324-S-ENCODING", "M0324-T-NO-BASIS", "M0324-T-ASSEMBLE"} else "open",
        "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"],
    })
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
