#!/usr/bin/env python3
"""Build the frozen THM-M-0508 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0508-OBLIGATION_TREE"
PREFIX = "M0508-"

# ID, kind, statement, formal target, machine debt, risk, machine/source eligibility.
ROWS = [
    ("ROOT", "root", "Every sufficiently large odd natural is a sum of three primes.",
     "VinogradovThreePrimesTarget", "M4", "critical", "required", "required"),
    ("S-COUNT", "definition", "Define the finite ordered count of prime triples summing to n.",
     "representationCount", "M1", "high", "required", "not_applicable"),
    ("L-COUNT-POS", "bridge", "Positive representation count is equivalent to three-prime existence.",
     "representationCount_pos_iff", "M0-L", "high", "required", "not_applicable"),
    ("N-FOURIER", "normalization", "Express the representation count by the ternary prime exponential-sum integral.",
     "planned: ternaryFourierIdentity", "M4", "critical", "required", "required"),
    ("B-ARCS", "branch", "Partition the integration domain into disjoint major and minor arcs with full coverage.",
     "planned: majorMinorArcPartition", "M4", "critical", "required", "required"),
    ("C-MAJOR", "construction", "Define major arcs and parameters uniformly over the eventual range.",
     "planned: majorArcParameters", "M4", "high", "required", "required"),
    ("L-MAJOR", "core_lemma", "Obtain the major-arc main term with a uniform error estimate.",
     "planned: majorArcAsymptotic", "M4", "critical", "required", "required"),
    ("L-SINGULAR", "core_lemma", "Prove the ternary singular series has a uniform positive lower bound on odd inputs.",
     "planned: singularSeriesPositive", "M4", "critical", "required", "required"),
    ("C-MINOR", "construction", "Define the complementary minor arcs using the same parameters.",
     "planned: minorArcs", "M4", "high", "required", "required"),
    ("L-MINOR", "core_lemma", "Bound the minor-arc contribution below the positive major-arc margin.",
     "planned: minorArcBound", "M4", "critical", "required", "required"),
    ("L-POSITIVE", "terminal", "Combine arc estimates to prove eventual positivity of the representation count.",
     "EventualPositiveRepresentationCount", "M4", "critical", "required", "required"),
    ("T-ASSEMBLE", "transport", "Transport eventual count positivity through the checked finite-count equivalence to the root.",
     "root_of_eventualPositiveRepresentationCount", "M0-L", "high", "required", "required"),
    ("X-SOURCE", "source_boundary", "Pin primary sources and crosswalk every analytic leaf and convention.",
     "non-Lean source receipt", "M4", "high", "not_applicable", "required"),
    ("X-FOUNDATION", "trust_boundary", "Audit axioms, imports, terminal bodies, and computation boundaries.",
     "kernel/trust receipt", "M4", "critical", "required", "not_applicable"),
    ("X-PROVENANCE", "certificate", "Trace every proof body and bridge to immutable owned or pinned source.",
     "provenance receipt", "M4", "high", "informational", "not_applicable"),
    ("X-READABLE", "documentation", "Reconstruct the proof with a node-complete public ledger.",
     "readable reconstruction", "M4", "high", "not_applicable", "not_applicable"),
    ("X-WORKFLOW", "workflow_gate", "Replay validation, freshness, independence, and release gates.",
     "workflow receipt", "M4", "critical", "informational", "not_applicable"),
]

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def file_hash(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()

obligations = []
for short, kind, statement, target, debt, risk, machine, source in ROWS:
    oid = PREFIX + short
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-declaration:" + target if not target.startswith("planned:")
                                  else "planned:v1:sha256:" + hashlib.sha256(statement.encode()).hexdigest()),
        "kind": kind, "root_relevant": not short.startswith("X-"),
        "machine_eligibility": machine, "human_source_eligibility": source,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ("release_overlay_no_proof_credit" if machine == "informational" else
                             "non_machine_boundary" if machine == "not_applicable" else None),
        "terminal_proof_body_id": ({"L-COUNT-POS": "local:ObligationTree.lean#representationCount_pos_iff",
                                    "T-ASSEMBLE": "local:ObligationTree.lean#root_of_eventualPositiveRepresentationCount"}.get(short)),
    })

ids = [row["obligation_id"] for row in obligations]
denom = digest(obligations)
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-0508", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated eventual three-primes target and bounded M4 anchor audit; classical ternary circle-method architecture selected without analytic closure credit.",
    "frozen_against_statement_sha256": file_hash("Statement.lean"),
    "frozen_against_anchor_audit_sha256": file_hash("anchor-audit.json"),
    "root_obligation_id": PREFIX + "ROOT", "denominator_sha256": denom,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, risk, or fingerprint change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-POSITIVE"), ("T-ASSEMBLE", "L-COUNT-POS"),
    ("L-POSITIVE", "N-FOURIER"), ("L-POSITIVE", "B-ARCS"),
    ("L-POSITIVE", "L-MAJOR"), ("L-POSITIVE", "L-SINGULAR"), ("L-POSITIVE", "L-MINOR"),
    ("N-FOURIER", "S-COUNT"), ("L-MAJOR", "C-MAJOR"),
    ("L-SINGULAR", "C-MAJOR"), ("L-MINOR", "C-MINOR"),
    ("C-MAJOR", "B-ARCS"), ("C-MINOR", "B-ARCS"),
]

def graph(edges):
    out = {i: [] for i in ids}; inside = {i: [] for i in ids}
    for e in edges:
        out[e["from"]].append(e["edge_id"]); inside[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inside}

proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    p, c = PREFIX + parent, PREFIX + child
    proof_edges += [
        {"edge_id": f"P{i:02}-REQ", "type": "proof_requires", "from": p, "to": c,
         "reciprocal_edge_id": f"P{i:02}-COMP"},
        {"edge_id": f"P{i:02}-COMP", "type": "composes", "from": c, "to": p,
         "reciprocal_edge_id": f"P{i:02}-REQ"},
    ]

def edges(kind, source, targets):
    return [{"edge_id": f"{kind}{i:02}", "type": {"R":"logical_decomposition", "V":"provenance_of", "E":"evidence_for", "T":"trusts", "D":"documents", "W":"workflow_depends_on"}[kind],
             "from": PREFIX + source, "to": PREFIX + target} for i, target in enumerate(targets, 1)]

analytic = [x[0] for x in ROWS if x[0] not in ("X-SOURCE", "X-FOUNDATION", "X-PROVENANCE", "X-READABLE", "X-WORKFLOW")]
nodes = []
for short, kind, statement, target, debt, risk, machine, source in ROWS:
    oid = PREFIX + short
    nodes.append({
        "node_id": "THM-M-0508-" + short, "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": statement,
        "human_debt": "H1", "machine_debt": debt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "SRC-M0508-PRIMARY-OPEN" if source == "required" else "not_applicable",
        "provenance_id": "local-checked" if debt == "M0-L" else "open",
        "foundation_profile": "Lean 4 Prop; analytic leaves may require classical Fourier analysis; release axiom audit open",
        "tcb_profile": "Lean 4.29.0 (98dc76e3); mathlib 8a178386; transitive release audit open",
        "computation_record": "Finset enumeration used only for a logical equivalence; no evaluation or oracle credited",
        "step_budget": 24 if risk == "critical" else 16,
        "semantic_step_ledger": {"premises": [PREFIX + c for p, c in proof_pairs if p == short],
                                 "inference": target, "output": statement,
                                 "outgoing_use": [PREFIX + p for p, c in proof_pairs if c == short]},
        "public_readable_target": "Stage1_Instances/THM-M-0508/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M0508-" + short, "status_boundary": "Architecture only; no open analytic or release leaf is credited.",
        "task_ids": [ITEM, "S56-M-0508-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0508/obligation-registry.json", "Stage1_Instances/THM-M-0508/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance",
                     "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"],
                     "revocation_state": "not-accepted"},
    })

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "ROOT", [x for x in analytic if x != "ROOT"])),
    "provenance": graph(edges("V", "X-PROVENANCE", analytic)),
    "evidence": graph(edges("E", "X-PROVENANCE", ["L-COUNT-POS", "T-ASSEMBLE"])),
    "trust": graph(edges("T", "X-FOUNDATION", analytic)),
    "documentation": graph(edges("D", "X-READABLE", [x[0] for x in ROWS if x[0] != "X-READABLE"])),
    "workflow": graph(edges("W", "X-WORKFLOW", ["X-SOURCE", "X-FOUNDATION", "X-PROVENANCE", "X-READABLE", "ROOT"])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0508",
    "registry_id": "THM-M-0508/obligation-registry@1", "registry_denominator_sha256": denom,
    "root_node_id": "THM-M-0508-ROOT",
    "edge_direction": "proof_requires is parent-to-child; composes is child-to-parent; other directions are named by edge type",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M4", "theorem_complete": False,
                         "closed_local_nodes": [PREFIX + "L-COUNT-POS", PREFIX + "T-ASSEMBLE"],
                         "first_open_cut_set": [PREFIX + "N-FOURIER", PREFIX + "B-ARCS", PREFIX + "L-MAJOR", PREFIX + "L-SINGULAR", PREFIX + "L-MINOR"],
                         "status_boundary": "Only finite-count equivalence and conditional composition elaborate; the circle-method proof, sources, trust, readability, independent replay, and release remain open."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, ensure_ascii=True, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, ensure_ascii=True, indent=2) + "\n")
print(f"built {len(ids)} obligations, denominator {denom}")
