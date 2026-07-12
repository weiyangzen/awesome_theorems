#!/usr/bin/env python3
"""Generate the frozen THM-M-1009 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1009-OBLIGATION_TREE"
THEOREM = "THM-M-1009"
PREFIX = "M1009-"

ROWS = [
    ("ROOT", "root", "Exact generalized Borel-Cantelli lower-bound target", "critical", 8),
    ("S-EVENTS", "definition", "Freeze measurable events and probability-space binders", "high", 10),
    ("S-DIVERGE", "definition", "Freeze divergence of real probability partial sums", "high", 10),
    ("B-ZERO", "branch", "Account for n = 0 and zero-denominator real division", "high", 12),
    ("N-COUNT", "normalization", "Represent finite event counts and identify first and second moments", "critical", 28),
    ("L-SECOND-MOMENT", "core_lemma", "Prove the finite second-moment lower bound for a finite event count", "critical", 55),
    ("L-TAIL", "core_lemma", "Apply the finite bound to shifted finite windows and tail unions", "critical", 48),
    ("L-RATIO", "limit", "Relate tail-window ratios to the frozen initial-segment filter limsup", "critical", 70),
    ("L-CONTINUITY", "limit", "Pass decreasing measurable tail unions to the event limsup", "critical", 45),
    ("T-ASSEMBLE", "terminal", "Compose finite, tail, ratio, and continuity results into the root", "critical", 30),
    ("X-SOURCE", "source", "Primary-source formula, assumptions, and nomenclature crosswalk", "high", 35),
    ("X-ANCHOR", "provenance", "Record nearby mathlib anchors without proof credit", "normal", 12),
    ("X-TCB", "trust", "Kernel, dependency, and transitive trust boundary", "high", 20),
    ("D-READABLE", "documentation", "Readable reconstruction linked to every semantic leaf", "high", 80),
    ("W-VALIDATE", "workflow", "Node-scoped proof, trust, provenance, and composition recipes", "high", 30),
]

MACHINE = {PREFIX + x for x, *_ in ROWS[:10]}
HUMAN = {PREFIX + x for x in ("ROOT", "N-COUNT", "L-SECOND-MOMENT", "L-TAIL", "L-RATIO", "L-CONTINUITY", "T-ASSEMBLE", "X-SOURCE")}

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

obligations = []
for suffix, kind, statement, risk, budget in ROWS:
    oid = PREFIX + suffix
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + sha(statement),
        "kind": kind,
        "root_relevant": oid in MACHINE,
        "machine_eligibility": "required" if oid in MACHINE else "informational",
        "human_source_eligibility": "required" if oid in HUMAN else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": "repo:Stage1Instances.THM_M_1009.ObligationTree.root_compose" if suffix == "T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
digest = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [r["obligation_id"] for r in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Statement and anchor receipts; roles assigned before proof closure is observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": PREFIX + "ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [x for x in ids if x in MACHINE],
        "required_human_source": [x for x in ids if x in HUMAN],
        "required_readable": ids,
        "informational_overlays": [x for x in ids if x not in MACHINE],
    },
    "delta_policy": "Any correction, split, merge, eligibility, risk, or exclusion change requires version 2 and an append-only ID delta.",
    "obligations": obligations,
}

nodes = []
for (suffix, kind, statement, risk, budget), row in zip(ROWS, obligations):
    oid = row["obligation_id"]
    formal = {
        "ROOT": "Stage1Instances.THM_M_1009.ErdosRenyiLowerBoundTarget",
        "B-ZERO": "Stage1Instances.THM_M_1009.ObligationTree.zero_ratio",
        "T-ASSEMBLE": "Stage1Instances.THM_M_1009.ObligationTree.root_compose",
    }.get(suffix, "planned:v1:" + suffix.lower())
    nodes.append({
        "node_id": THEOREM + "-" + suffix, "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": statement,
        "human_debt": "H1", "machine_debt": "M3", "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "SRC-M1009-PRIMARY-OPEN" if oid in HUMAN else "not-applicable",
        "provenance_id": "ANCHOR-M1009-AUDIT" if suffix == "X-ANCHOR" else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; full trust audit open",
        "tcb_profile": "Lean 4.29.0; mathlib 8a178386; release replay open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed proof children"], "inference": formal, "output": statement, "outgoing_use": "typed parent or root"},
        "public_readable_target": f"Stage1_Instances/THM-M-1009/obligation-tree.md#{suffix.lower()}",
        "validation_spec_id": "VAL-M1009-" + suffix,
        "status_boundary": "Architecture only; no closure or acceptance credit.",
        "task_ids": [ITEM, "S56-M-1009-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1009/obligation-registry.json", "Stage1_Instances/THM-M-1009/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "anchor provenance"], "revocation_state": "not-accepted"},
    })

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "S-EVENTS"), ("T-ASSEMBLE", "S-DIVERGE"),
    ("T-ASSEMBLE", "B-ZERO"), ("T-ASSEMBLE", "L-TAIL"), ("T-ASSEMBLE", "L-RATIO"),
    ("T-ASSEMBLE", "L-CONTINUITY"), ("L-TAIL", "L-SECOND-MOMENT"),
    ("L-SECOND-MOMENT", "N-COUNT"),
]
graphs = {name: {"edges": []} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
counter = 0
for parent, child in proof_pairs:
    counter += 1
    a, b = PREFIX + parent, PREFIX + child
    e1, e2 = f"P{counter}a", f"P{counter}b"
    graphs["proof"]["edges"] += [
        {"edge_id": e1, "from": a, "to": b, "type": "proof_requires", "reciprocal_edge_id": e2},
        {"edge_id": e2, "from": b, "to": a, "type": "composes", "reciprocal_edge_id": e1},
    ]
extras = {
    "refinement": [("ROOT", "S-EVENTS", "logical_decomposition"), ("ROOT", "S-DIVERGE", "logical_decomposition"), ("ROOT", "B-ZERO", "logical_decomposition")],
    "provenance": [("X-ANCHOR", "L-TAIL", "provenance_of"), ("X-SOURCE", "ROOT", "source_map")],
    "evidence": [("W-VALIDATE", "ROOT", "evidence_for")],
    "trust": [("X-TCB", "ROOT", "trusts")],
    "documentation": [("D-READABLE", "ROOT", "documents")],
    "workflow": [("W-VALIDATE", "T-ASSEMBLE", "workflow_depends_on"), ("D-READABLE", "L-SECOND-MOMENT", "workflow_depends_on")],
}
for graph, triples in extras.items():
    for i, (a, b, typ) in enumerate(triples, 1):
        graphs[graph]["edges"].append({"edge_id": graph[0].upper() + str(i), "from": PREFIX+a, "to": PREFIX+b, "type": typ})
for graph in graphs.values():
    graph["out"], graph["in"] = {x: [] for x in ids}, {x: [] for x in ids}
    for e in graph["edges"]:
        graph["out"][e["from"]].append(e["edge_id"]); graph["in"][e["to"]].append(e["edge_id"])

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": digest, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
      "remaining_root_cut_set": [PREFIX+x for x in ("L-SECOND-MOMENT", "L-TAIL", "L-RATIO", "L-CONTINUITY")]},
}

recipes = [{"recipe_id": "VAL-M1009-"+suffix, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1009/check_obligation_tree.py"], "env": {}, "timeout_seconds": 60, "network": "forbidden", "covered_ids": [PREFIX+suffix]} for suffix, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
write("obligation-registry.json", registry); write("typed-graphs.json", bundle); write("validation-specs.json", specs)
print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {digest}")
