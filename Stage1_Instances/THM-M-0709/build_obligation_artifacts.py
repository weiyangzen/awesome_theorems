#!/usr/bin/env python3
"""Generate the frozen THM-M-0709 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0709-OBLIGATION_TREE"
THEOREM = "THM-M-0709"
PREFIX = "M0709-"

# IDs and eligibility are fixed before any PCP proof implementation is inspected.
ROWS = [
    ("M0709-ROOT", "root", "The exact binary PCP solvability predicate is not computable.", "Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable", "critical", "required", "required"),
    ("M0709-S-SEMANTICS", "definition", "Audit tiles, one shared nonempty index sequence, valid indices, concatenation, and empty-instance behavior.", "Stage1Instances.THM_M_0709.{PCPInstance,upperWord,lowerWord,IsSolution,HasSolution}", "critical", "required", "required"),
    ("M0709-S-COMPUTABILITY", "definition", "Fix Primcodable structured inputs and the exact ComputablePred negation boundary.", "Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable", "critical", "required", "required"),
    ("M0709-N-HALTING", "bridge", "Select a pinned undecidable source predicate and expose both its input coding and noncomputability theorem.", "ComputablePred.halting_problem plus a planned source-predicate wrapper", "critical", "required", "required"),
    ("M0709-C-MACHINE", "construction", "Normalize a source computation into a finite deterministic transition system with a distinguished accepting computation.", "planned exact machine-normalization signature", "critical", "required", "required"),
    ("M0709-C-MPCP", "construction", "Construct a finite modified-PCP tile system encoding legal configurations and transitions.", "planned effective modified-PCP construction", "critical", "required", "required"),
    ("M0709-L-MPCP-SOUND", "core_lemma", "Decode every modified-PCP match into a legal accepting source computation.", "planned modified-PCP soundness theorem", "critical", "required", "required"),
    ("M0709-L-MPCP-COMPLETE", "core_lemma", "Encode every accepting source computation as a modified-PCP match.", "planned modified-PCP completeness theorem", "critical", "required", "required"),
    ("M0709-T-MPCP-PCP", "reduction", "Convert modified PCP to ordinary PCP while preserving nonempty matches in both directions.", "planned effective MPCP-to-PCP reduction", "critical", "required", "required"),
    ("M0709-L-PCP-SOUND", "core_lemma", "Compose decoding to show an ordinary PCP solution implies source acceptance.", "planned ordinary-PCP soundness theorem", "critical", "required", "required"),
    ("M0709-L-PCP-COMPLETE", "core_lemma", "Compose encoding to show source acceptance implies an ordinary PCP solution.", "planned ordinary-PCP completeness theorem", "critical", "required", "required"),
    ("M0709-N-BINARY", "normalization", "Encode the finite working alphabet into nonempty self-synchronizing binary codewords.", "planned computable binary alphabet encoding", "critical", "required", "required"),
    ("M0709-L-BINARY-IFF", "transport", "Prove binary encoding preserves and reflects ordinary PCP solutions.", "planned HasSolution equivalence for binary encoding", "critical", "required", "required"),
    ("M0709-T-REDUCTION", "transport", "Package the full source-to-binary-PCP map as a computable function.", "planned Computable reduction function", "critical", "required", "required"),
    ("M0709-T-UNDECIDABLE", "terminal", "Derive the exact root by pulling a hypothetical PCP decider back along the checked reduction.", "planned exact theorem PostCorrespondenceUndecidable", "critical", "required", "required"),
    ("M0709-X-SOURCE", "certificate", "Map every reduction invariant to an inspected primary or accepted modern proof source.", "primary-source node map pending", "critical", "not_applicable", "required"),
    ("M0709-X-FOUNDATION", "certificate", "Audit axioms, imports, transitive declarations, kernel, TCB, and computation boundaries.", "planned trust and axiom report", "critical", "required", "not_applicable"),
    ("M0709-X-PROVENANCE", "certificate", "Record terminal bodies, immutable revisions, licenses, receipts, and revocations.", "planned provenance ledger", "critical", "informational", "not_applicable"),
]

PROOF_REQUIRES = [
    ("M0709-ROOT", "M0709-T-UNDECIDABLE"),
    ("M0709-T-UNDECIDABLE", "M0709-N-HALTING"),
    ("M0709-T-UNDECIDABLE", "M0709-T-REDUCTION"),
    ("M0709-T-UNDECIDABLE", "M0709-L-BINARY-IFF"),
    ("M0709-T-REDUCTION", "M0709-C-MACHINE"),
    ("M0709-T-REDUCTION", "M0709-C-MPCP"),
    ("M0709-T-REDUCTION", "M0709-T-MPCP-PCP"),
    ("M0709-T-REDUCTION", "M0709-N-BINARY"),
    ("M0709-L-BINARY-IFF", "M0709-L-PCP-SOUND"),
    ("M0709-L-BINARY-IFF", "M0709-L-PCP-COMPLETE"),
    ("M0709-L-BINARY-IFF", "M0709-N-BINARY"),
    ("M0709-L-PCP-SOUND", "M0709-T-MPCP-PCP"),
    ("M0709-L-PCP-SOUND", "M0709-L-MPCP-SOUND"),
    ("M0709-L-PCP-COMPLETE", "M0709-T-MPCP-PCP"),
    ("M0709-L-PCP-COMPLETE", "M0709-L-MPCP-COMPLETE"),
    ("M0709-L-MPCP-SOUND", "M0709-C-MPCP"),
    ("M0709-L-MPCP-SOUND", "M0709-C-MACHINE"),
    ("M0709-L-MPCP-COMPLETE", "M0709-C-MPCP"),
    ("M0709-L-MPCP-COMPLETE", "M0709-C-MACHINE"),
]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def planned(oid: str, statement: str) -> str:
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, risk, machine, human_source in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if oid in {"M0709-ROOT", "M0709-S-SEMANTICS", "M0709-S-COMPUTABILITY"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human_source,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"M0709-X-SOURCE": "human_source_boundary_only", "M0709-X-PROVENANCE": "release_overlay_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": None,
    })

ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated binary-PCP statement and bounded anchor audit; the standard halting-to-MPCP-to-PCP-to-binary architecture was selected without assigning proof closure.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0709-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0709-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or replacement of the reduction architecture requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, risk, machine, human_source in ROWS:
    interface_checked = oid in {"M0709-S-SEMANTICS", "M0709-S-COMPUTABILITY"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": human,
        "formal_target": formal,
        "output": human,
        "human_debt": "H1",
        "machine_debt": "M3" if oid in {"M0709-ROOT", "M0709-S-SEMANTICS", "M0709-S-COMPUTABILITY"} else "M4",
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human_source == "required" else "not-applicable",
        "provenance_id": "none",
        "foundation_profile": "lean4-mathlib/axiom-and-transitive-closure-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-declaration-closure-pending",
        "computation_record": "none; no oracle, generated result, or external solver is credited",
        "step_budget": 100,
        "semantic_step_ledger": {
            "premises": "Exactly the incoming proof children recorded in the proof graph and the node's stated formal context.",
            "inference": human,
            "output": human,
            "outgoing_use": "Only the recorded reciprocal composes edges may consume this output for proof closure.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0709/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen semantic interface only; it supplies no proof body, composition credit, source acceptance, or root closure.",
        "task_ids": [ITEM, "S56-M-0709-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0709/Statement.lean"] if interface_checked else [],
        "owner": "THM-M-0709 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if interface_checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement", "registry", "source map", "toolchain", "reduction architecture"],
            "revocation_state": "provisional" if interface_checked else "open",
        },
    })

def graph(edges):
    outgoing = {oid: [] for oid in ids}
    incoming = {oid: [] for oid in ids}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_edges = []
for index, (parent, child) in enumerate(PROOF_REQUIRES, 1):
    req, comp = f"P{index:02d}-REQ", f"P{index:02d}-COMP"
    proof_edges.extend([
        {"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req},
    ])

def edges(prefix, edge_type, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": edge_type, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M0709-ROOT", "M0709-S-SEMANTICS"), ("M0709-ROOT", "M0709-S-COMPUTABILITY"), ("M0709-T-MPCP-PCP", "M0709-L-PCP-SOUND"), ("M0709-T-MPCP-PCP", "M0709-L-PCP-COMPLETE")])),
    "provenance": graph(edges("V", "provenance_of", [("M0709-X-PROVENANCE", oid) for oid in ids if oid != "M0709-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0709-X-SOURCE", oid) for oid in ids if oid not in {"M0709-S-SEMANTICS", "M0709-S-COMPUTABILITY", "M0709-X-SOURCE", "M0709-X-FOUNDATION", "M0709-X-PROVENANCE"}])),
    "trust": graph(edges("T", "trusts", [(oid, "M0709-X-FOUNDATION") for oid in ["M0709-ROOT", "M0709-N-HALTING", "M0709-T-REDUCTION", "M0709-T-UNDECIDABLE"]])),
    "documentation": graph(edges("D", "documents", [("M0709-X-SOURCE", "M0709-ROOT"), ("M0709-X-PROVENANCE", "M0709-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0709-ROOT", "M0709-X-SOURCE"), ("M0709-ROOT", "M0709-X-FOUNDATION"), ("M0709-ROOT", "M0709-X-PROVENANCE")])),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-0709-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M0709-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": ["M0709-N-HALTING", "M0709-C-MACHINE", "M0709-C-MPCP", "M0709-X-SOURCE", "M0709-X-FOUNDATION"],
    },
}

recipes = []
for oid in ids:
    recipes.append({
        "recipe_id": "VAL-" + oid,
        "obligation_id": oid,
        "state": "provisional" if oid in {"M0709-S-SEMANTICS", "M0709-S-COMPUTABILITY"} else "open",
        "cwd": "Formalizations/Lean",
        "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0709/Statement.lean"],
        "env": {},
        "timeout_seconds": 120,
        "network": "forbidden",
        "covered_ids": [oid],
        "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"],
    })
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
