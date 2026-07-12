#!/usr/bin/env python3
"""Generate the frozen THM-M-0786 obligation registry and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0786-OBLIGATION_TREE"
THEOREM = "THM-M-0786"

# This inventory describes the integration architecture selected after the
# bounded anchor audit. It deliberately does not invent the unaudited internal
# proof decomposition of the external Borel-determinacy theorem.
ROWS = [
    ("M0786-ROOT", "root", "Every Borel payoff on Baire space is determined in the frozen total-strategy encoding.", "Stage1Instances.THM_M_0786.BorelDeterminacyTarget", "required", "required", 20),
    ("M0786-S-ENCODING", "definition", "Preserve Nat plays, chronological finite histories, parity-sensitive total strategies, compatibility, and complement payoff conventions.", "Stage1Instances.THM_M_0786.{Play,History,Strategy,Compatible,FirstWins,SecondWins}", "required", "required", 60),
    ("M0786-N-BOREL", "normalization", "Identify the canonical product MeasurableSet predicate with the Borel structure required by the imported game theorem.", "planned exact measurable-space transport", "required", "required", 80),
    ("M0786-N-STRATEGY", "normalization", "Relate canonical total history strategies to the imported legal-position strategy representation in both player directions.", "planned bidirectional strategy and compatible-play transport", "required", "required", 100),
    ("M0786-B-WINNER", "branch", "Preserve the Player-I/Player-II winning disjunction and payoff-complement convention through the adapter.", "planned determined-game disjunction transport", "required", "required", 60),
    ("M0786-C-FULLGAME", "construction", "Construct the full pruned Nat-move Gale-Stewart game corresponding to an arbitrary canonical payoff.", "planned full-tree GaleStewartGame construction", "required", "required", 100),
    ("M0786-L-BORELDET", "external_bridge", "Kernel-check and apply GaleStewartGame.borel_determinacy at immutable external revision 42bc874b2357ca7e7573b31854a0d09761e11e41.", "external:BorelDet.Proof.borel_determinacy#GaleStewartGame.borel_determinacy", "required", "required", 100),
    ("M0786-T-ADAPTER", "transport", "Compose full-game, Borel, strategy, and winner transports into a canonical payoff solver.", "Stage1Instances.THM_M_0786.ObligationTree.PayoffSolver", "required", "required", 80),
    ("M0786-T-ASSEMBLE", "transport", "Universally introduce payoff and its Borel witness and assemble the canonical root from the payoff solver.", "Stage1Instances.THM_M_0786.ObligationTree.root_of_payoffSolver", "required", "required", 20),
    ("M0786-X-SOURCE", "source_boundary", "Map every mathematical node to reviewed pages, definitions, assumptions, and errata in Martin's primary source.", "primary source node map pending", "not_applicable", "required", 100),
    ("M0786-X-FOUNDATION", "trust_boundary", "Audit choice, transfinite principles, kernel axioms, unsafe boundaries, and the complete imported dependency closure.", "foundation and transitive axiom report pending", "required", "required", 80),
    ("M0786-X-PROVENANCE", "certificate", "Bind the external terminal body and adapter to immutable revision, license, exact type, body location, and placeholder evidence.", "provenance ledger pending integration", "informational", "required", 50),
    ("M0786-X-COMPUTATION", "computation_boundary", "Record that no oracle, native computation, or unverified generated certificate supplies proof credit.", "computation profile audit pending release", "required", "not_applicable", 30),
    ("M0786-X-WORKFLOW", "workflow_gate", "Require proof, node validation, independent replay, and release receipts before any root promotion.", "rev-5.6 proof -> validation -> release workflow", "informational", "not_applicable", 20),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    excluded = machine in {"not_applicable", "informational"}
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if oid in {"M0786-ROOT", "M0786-S-ENCODING"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in {"M0786-ROOT", "M0786-N-STRATEGY", "M0786-C-FULLGAME", "M0786-L-BORELDET", "M0786-X-SOURCE", "M0786-X-FOUNDATION"} else "high",
        "step_budget": budget,
        "exclusion_reason": "non_machine_boundary_no_proof_credit" if excluded else None,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0786/ObligationTree.lean#root_of_payoffSolver" if oid == "M0786-T-ASSEMBLE" else None,
    })

ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated Gale-Stewart target plus bounded anchor audit; immutable external theorem integration and explicit encoding transports selected before observing local proof closure.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0786-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or re-fingerprint requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

checked = {"M0786-S-ENCODING", "M0786-T-ASSEMBLE"}
nodes = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0786-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0786-ROOT" else ("M5" if oid == "M0786-L-BORELDET" else "M4")), "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md; primary page-level map pending",
        "provenance_id": "anchor-audit.json#M0786-A-BORELDET-EXTERNAL" if oid in {"M0786-L-BORELDET", "M0786-X-PROVENANCE"} else "none",
        "foundation_profile": "classical set-theoretic proof expected; precise choice/transfinite and imported axiom closure pending",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386 locally; external Lean 4.28.0-rc1 + mathlib b94b918 integration pending",
        "computation_record": "none; no oracle, solver, or external computation credited", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the exact formal context and declared proof-requires children.", "inference": human, "output": human, "outgoing_use": "Only declared typed proof or support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0786/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": ("Kernel-checked conditional interface only; " if oid in checked else "Frozen architecture only; ") + "no proof of Borel determinacy or imported closure is supplied.",
        "task_ids": [ITEM, "S56-M-0786-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0786/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0786 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

def graph(edges):
    out, inc = {x: [] for x in ids}, {x: [] for x in ids}
    for edge in edges:
        out[edge["from"]].append(edge["edge_id"]); inc[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": inc}

proof_pairs = [
    ("M0786-ROOT", "M0786-S-ENCODING"), ("M0786-ROOT", "M0786-T-ASSEMBLE"),
    ("M0786-T-ASSEMBLE", "M0786-T-ADAPTER"), ("M0786-T-ADAPTER", "M0786-N-BOREL"),
    ("M0786-T-ADAPTER", "M0786-N-STRATEGY"), ("M0786-T-ADAPTER", "M0786-B-WINNER"),
    ("M0786-T-ADAPTER", "M0786-C-FULLGAME"), ("M0786-T-ADAPTER", "M0786-L-BORELDET"),
]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]

def simple(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(simple("R", "logical_decomposition", [("M0786-ROOT", x) for x in ["M0786-S-ENCODING", "M0786-N-BOREL", "M0786-N-STRATEGY", "M0786-B-WINNER", "M0786-C-FULLGAME", "M0786-L-BORELDET", "M0786-T-ADAPTER", "M0786-T-ASSEMBLE"]])),
    "provenance": graph(simple("V", "provenance_of", [("M0786-X-PROVENANCE", x) for x in ["M0786-L-BORELDET", "M0786-T-ADAPTER", "M0786-T-ASSEMBLE", "M0786-ROOT"]])),
    "evidence": graph(simple("E", "source_map", [("M0786-X-SOURCE", x) for x in ["M0786-ROOT", "M0786-N-BOREL", "M0786-N-STRATEGY", "M0786-B-WINNER", "M0786-L-BORELDET"]])),
    "trust": graph(simple("T", "trusts", [(x, "M0786-X-FOUNDATION") for x in ["M0786-ROOT", "M0786-L-BORELDET", "M0786-T-ADAPTER"]] + [("M0786-ROOT", "M0786-X-COMPUTATION")])),
    "documentation": graph(simple("D", "documents", [("M0786-X-SOURCE", "M0786-ROOT"), ("M0786-X-PROVENANCE", "M0786-L-BORELDET")])),
    "workflow": graph(simple("W", "workflow_depends_on", [("M0786-ROOT", x) for x in ["M0786-X-SOURCE", "M0786-X-FOUNDATION", "M0786-X-PROVENANCE", "M0786-X-COMPUTATION", "M0786-X-WORKFLOW"]])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0786-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0786-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0786-N-BOREL", "M0786-N-STRATEGY", "M0786-B-WINNER", "M0786-C-FULLGAME", "M0786-L-BORELDET", "M0786-X-SOURCE", "M0786-X-FOUNDATION", "M0786-X-PROVENANCE"]},
}
specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in checked else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids],
}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
