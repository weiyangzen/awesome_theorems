#!/usr/bin/env python3
"""Build the frozen THM-M-1058 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

specs = [
    ("M1058-ROOT", "root", "The frozen large-deviation predicate for supplied data is exactly the conjunction of its closed-set upper and open-set lower bounds.", "LargeDeviationPrinciple E D", "Exact frozen LDP predicate, without asserting it for arbitrary data.", "split-required", "H1", "M3", "R3", "high"),
    ("M1058-TARGET", "definition", "Fix the universe, state space, topology, measurable structure, and supplied LDP data.", "LargeDeviationData E -> Prop", "Stable domain and binder boundary.", 5, "H1", "M4", "R3", "medium"),
    ("M1058-DATA", "definition", "Package the measures, speed, and rate function together with the hypotheses belonging to those data.", "LargeDeviationData E", "Well-scoped data record used by both bounds.", "split-required", "H1", "M4", "R3", "medium"),
    ("M1058-MEASURES", "definition", "Each member of the sequence is a probability measure on E.", "Nat -> ProbabilityMeasure E", "The measure sequence and its coercion to Measure E.", 4, "H1", "M4", "R3", "low"),
    ("M1058-SPEED", "definition", "The real speed is positive at every index and tends to positive infinity.", "(a : Nat -> Real) x (forall n, 0 < a n) x Tendsto a atTop atTop", "The normalization scale and its two hypotheses.", 6, "H1", "M4", "R3", "medium"),
    ("M1058-RATE", "definition", "The EReal-valued rate is nonnegative and lower semicontinuous.", "(I : E -> EReal) x (forall x, 0 <= I x) x LowerSemicontinuous I", "The base rate-function contract, excluding compact sublevel sets.", 6, "H1", "M4", "R3", "medium"),
    ("M1058-SCALED-LOG", "definition", "Normalize the logarithmic probability by the reciprocal speed, including the zero-probability convention.", "scaledLogProbability E D s n = (((D.speed n)^-1 : Real) : EReal) * ENNReal.log ((D.measures n : Measure E) s)", "A single normalized EReal expression used in both bounds.", 7, "H1", "M4", "R3", "high"),
    ("M1058-RATE-INF", "definition", "Take the EReal infimum of the rate over an event.", "rateInf E D s = sInf (D.rate '' s)", "The event rate, including the selected empty-set convention.", 5, "H1", "M4", "R3", "high"),
    ("M1058-UPPER", "semantic_leaf", "For every closed F, the normalized logarithmic limsup is at most minus the rate infimum on F.", "forall F : Set E, IsClosed F -> limsup (fun n => scaledLogProbability E D F n) atTop <= -rateInf E D F", "The full closed-set upper-bound branch, not the weak compact-set variant.", 9, "H1", "M3", "R3", "high"),
    ("M1058-LOWER", "semantic_leaf", "For every open G, minus the rate infimum on G is at most the normalized logarithmic liminf.", "forall G : Set E, IsOpen G -> -rateInf E D G <= liminf (fun n => scaledLogProbability E D G n) atTop", "The open-set lower-bound branch.", 9, "H1", "M3", "R3", "high"),
    ("M1058-COMPOSE", "composition", "Compose exactly the upper and lower branches as a conjunction.", "M1058-UPPER /\\ M1058-LOWER", "The body of LargeDeviationPrinciple with no hidden premise.", 4, "H1", "M3", "R3", "high"),
    ("M1058-TRANSPORT", "transport", "Relate the named predicate to the fully expanded source-shaped expression by definitional equality.", "LargeDeviationPrinciple E D <-> PinnedCandidateSourceShape E D", "Checked exact-shape transport; no proof that a particular D satisfies the predicate.", 4, "H1", "M4", "R3", "medium"),
    ("M1058-SOURCE", "source_boundary", "Map every material branch and convention to a pinpoint primary source and reviewed errata record.", "human-source crosswalk for M1058-UPPER, M1058-LOWER, M1058-SPEED, and M1058-RATE", "Node-specific H evidence; currently only a broad Definition 1.2.1 anchor.", 8, "H1", "M4", "R3", "high"),
    ("M1058-PROVENANCE", "provenance", "Resolve every terminal body and declaration dependency without crediting substrate as an LDP proof.", "declaration/proof-body provenance closure", "Pinned provenance boundary for local definitions and mathlib substrate.", 8, "H1", "M3", "R3", "high"),
    ("M1058-TRUST", "trust", "Audit axioms, unsafe paths, computation, toolchain, and transitive imports for any eventual closure claim.", "Lean kernel trust and axiom closure", "Node-specific trust record; release evidence remains open.", 8, "H1", "M3", "R3", "high"),
    ("M1058-IMPORTS", "import_boundary", "Pin and validate the four minimal mathlib modules used by the statement.", "ProbabilityMeasure; LiminfLimsup; Semicontinuity.Defs; ENNRealLog", "Immutable statement substrate, never terminal LDP proof credit.", 6, "H1", "M4", "R3", "medium"),
]

informational = {"M1058-SOURCE", "M1058-PROVENANCE", "M1058-TRUST", "M1058-IMPORTS"}
obligations = []
nodes = []
for oid, kind, human, formal, output, budget, h, m, r, risk in specs:
    machine = "informational" if oid in informational else "required"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": hashlib.sha256((oid + "\0" + formal).encode()).hexdigest(),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "required" if oid in {"M1058-ROOT", "M1058-SPEED", "M1058-RATE", "M1058-UPPER", "M1058-LOWER", "M1058-SOURCE"} else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "Typed overlay: required for assurance but excluded from mathematical proof coverage." if machine == "informational" else None,
        "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": "THM-M-1058-" + oid.removeprefix("M1058-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": human,
        "formal_target": formal,
        "output": output,
        "human_debt": h,
        "machine_debt": m,
        "readability_debt": r,
        "evidence_ids": [],
        "source_crosswalk_id": "source_statement_crosswalk.md" if oid in {"M1058-ROOT", "M1058-SPEED", "M1058-RATE", "M1058-UPPER", "M1058-LOWER", "M1058-SOURCE"} else "not-applicable-at-freeze",
        "provenance_id": "anchor-audit.json" if oid in {"M1058-PROVENANCE", "M1058-IMPORTS"} else "pending-node-provenance",
        "foundation_profile": "lean4-v4.29.0/policy-and-axiom-audit-pending",
        "tcb_profile": "mathlib-8a178386ffc0f5fef0b77738bb5449d50efeea95/transitive-closure-pending",
        "computation_record": "none; no native computation or oracle credited",
        "step_budget": budget,
        "semantic_step_ledger": human + " Produce only: " + output + " Record exact child fingerprints and evidence before any closure claim.",
        "public_readable_target": "Stage1_Instances/THM-M-1058/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Architecture freeze only. This node is open and supplies no proof, H0/R0 review, or release credit.",
        "task_ids": ["S56-M-1058-OBLIGATION_TREE", "S56-M-1058-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1058/Statement.lean"] if oid not in informational else [],
        "owner": "THM-M-1058 proof implementation lane",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def graph(name, pairs):
    edges = [{"edge_id": f"{name.upper()}-{i:02d}", "from": a, "to": b, "relation": rel} for i, (a, b, rel) in enumerate(pairs, 1)]
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

graphs = {
    "proof": graph("proof", [("M1058-ROOT", "M1058-COMPOSE", "root requires exact conjunction composition"), ("M1058-COMPOSE", "M1058-UPPER", "left conjunct"), ("M1058-COMPOSE", "M1058-LOWER", "right conjunct")]),
    "refinement": graph("refinement", [("M1058-ROOT", "M1058-TARGET", "binder and target refinement"), ("M1058-ROOT", "M1058-TRANSPORT", "expanded-shape refinement"), ("M1058-TARGET", "M1058-DATA", "data refinement"), ("M1058-DATA", "M1058-MEASURES", "measure component"), ("M1058-DATA", "M1058-SPEED", "speed component"), ("M1058-DATA", "M1058-RATE", "rate component"), ("M1058-TARGET", "M1058-SCALED-LOG", "normalization definition"), ("M1058-TARGET", "M1058-RATE-INF", "event-rate definition")]),
    "provenance": graph("provenance", [("M1058-ROOT", "M1058-PROVENANCE", "root provenance requirement"), ("M1058-PROVENANCE", "M1058-IMPORTS", "pinned substrate provenance")]),
    "evidence": graph("evidence", [("M1058-ROOT", "M1058-TRANSPORT", "statement-phase elaboration evidence only"), ("M1058-IMPORTS", "M1058-TARGET", "import elaboration supports target syntax")]),
    "trust": graph("trust", [("M1058-ROOT", "M1058-TRUST", "root trust closure requirement"), ("M1058-TRUST", "M1058-IMPORTS", "transitive dependency trust boundary")]),
    "documentation": graph("documentation", [("M1058-ROOT", "M1058-SOURCE", "root source review"), ("M1058-SOURCE", "M1058-UPPER", "upper branch crosswalk"), ("M1058-SOURCE", "M1058-LOWER", "lower branch crosswalk"), ("M1058-SOURCE", "M1058-SPEED", "speed convention crosswalk"), ("M1058-SOURCE", "M1058-RATE", "rate convention crosswalk")]),
    "workflow": graph("workflow", [("M1058-ROOT", "M1058-UPPER", "proof phase must classify/implement upper branch"), ("M1058-ROOT", "M1058-LOWER", "proof phase must classify/implement lower branch"), ("M1058-ROOT", "M1058-TRUST", "validation phase must close trust"), ("M1058-ROOT", "M1058-SOURCE", "audit must obtain pinpoint review")]),
}

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-1058-OBLIGATION_TREE",
    "theorem_id": "THM-M-1058",
    "registry_version": 1,
    "freeze_basis": "Exact statement SHA-256 60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33 and completed bounded anchor audit; closure status was not used to choose denominators.",
    "root_obligation_id": "M1058-ROOT",
    "frozen_denominators": {
        "inventory": [x["obligation_id"] for x in obligations],
        "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"],
        "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"],
        "required_readable": [x["obligation_id"] for x in obligations if x["readable_eligibility"] == "required"],
    },
    "denominator_sha256": denominator,
    "obligations": obligations,
    "status_boundary": "All obligations remain open. The registry records architecture and eligibility only.",
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": "S56-M-1058-OBLIGATION_TREE",
    "theorem_id": "THM-M-1058",
    "registry_denominator_sha256": denominator,
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [],
        "root_machine_debt": "M3",
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1058-UPPER", "M1058-LOWER"],
        "note": "The checked definitional transport is statement evidence, not evidence that supplied data satisfy either LDP branch.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
