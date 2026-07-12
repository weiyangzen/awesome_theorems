#!/usr/bin/env python3
"""Generate the frozen THM-M-0711 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0711-OBLIGATION_TREE"
THEOREM = "THM-M-0711"
PREFIX = "M0711-"

spec = [
    ("ROOT", "root", "Exact NovikovBooneTarget", "Stage1.THM_M_0711.NovikovBooneTarget", "M4", "critical"),
    ("S-ENCODING", "definition", "Signed-list word encoding and evalWord semantics", "Stage1.THM_M_0711.evalWord", "M0-L", "high"),
    ("S-PRESENTATION", "definition", "Finite relators and PresentedGroup quotient semantics", "planned exact presentation interface", "M4", "high"),
    ("S-FOUNDATION", "certificate", "Classical, quotient, TCB, and no-oracle policy", "planned transitive axiom report", "M4", "critical"),
    ("N-EVAL", "normalization", "Compile source configurations into signed generator lists", "planned computable word encoder", "M4", "critical"),
    ("N-QUOTIENT", "transport", "Relate quotient identity to normal-closure membership", "planned use of PresentedGroup.mk_eq_one_iff", "M4", "high"),
    ("B-REDUCTION", "reduction", "Reduce a pinned undecidable predicate to word identity", "planned many-one reduction theorem", "M4", "critical"),
    ("C-PRESENTATION", "construction", "Construct a fixed finite generator and relator presentation", "planned n and rels witness", "M4", "critical"),
    ("C-COMPILER", "construction", "Construct the effective configuration-to-word compiler", "planned computable compiler", "M4", "critical"),
    ("C-CORRECT", "core_lemma", "Prove compiler correctness in both directions", "planned iff with quotient identity", "M4", "critical"),
    ("L-HALTING", "bridge", "Import the exact noncomputability source predicate", "ComputablePred.halting_problem", "M1", "critical"),
    ("L-MANYONE", "core_lemma", "Transfer computability backwards through the compiler", "planned computability closure lemma", "M4", "critical"),
    ("L-NONCOMP", "terminal", "Derive noncomputability of identity for the constructed presentation", "FixedPresentationUndecidable n rels", "M4", "critical"),
    ("X-SOURCE", "certificate", "Pin primary Novikov/Boone passages to semantic nodes", "human source crosswalk pending", "M5", "high"),
    ("X-PROVENANCE", "certificate", "Record terminal bodies, wrappers, imports, and trust closure", "provenance ledger pending", "M5", "high"),
    ("T-WITNESS", "terminal", "Package the constructed presentation and its noncomputability proof", "exists n rels, FixedPresentationUndecidable n rels", "M4", "critical"),
    ("T-ASSEMBLE", "terminal", "Assemble the witness into the exact existential root", "novikovBooneTarget_of_witness", "M0-L", "normal"),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit-receipt.json").read_bytes()).hexdigest()
rows = []
for suffix, kind, human, formal, machine, risk in spec:
    oid = PREFIX + suffix
    fp = "lean-source:v1:sha256:" + statement_hash if suffix in {"ROOT", "S-ENCODING"} else "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + human + "\0" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": suffix not in {"X-SOURCE", "X-PROVENANCE"},
        "machine_eligibility": "required" if suffix not in {"X-SOURCE", "X-PROVENANCE"} else "informational",
        "human_source_eligibility": "required" if suffix not in {"S-ENCODING", "S-PRESENTATION", "S-FOUNDATION", "X-PROVENANCE"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "governance overlay; never proof credit" if suffix in {"X-SOURCE", "X-PROVENANCE"} else None,
        "terminal_proof_body_id": "lean:Stage1.THM_M_0711.novikovBooneTarget_of_witness" if suffix == "T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact fixed-presentation statement and bounded negative anchor audit; construction and reduction route expanded before proof execution.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": PREFIX + "ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [PREFIX + "X-SOURCE", PREFIX + "X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-WITNESS"), ("T-WITNESS", "L-NONCOMP"),
    ("L-NONCOMP", "B-REDUCTION"), ("B-REDUCTION", "C-PRESENTATION"), ("B-REDUCTION", "C-COMPILER"),
    ("B-REDUCTION", "C-CORRECT"), ("B-REDUCTION", "L-MANYONE"), ("B-REDUCTION", "L-HALTING"),
    ("C-COMPILER", "N-EVAL"), ("C-CORRECT", "N-QUOTIENT"), ("C-PRESENTATION", "S-PRESENTATION"),
    ("N-EVAL", "S-ENCODING"), ("ROOT", "S-FOUNDATION"),
]

def edges_for_pairs(pairs, reciprocal=False, edge_type="logical_decomposition"):
    edges = []
    for i, (a, b) in enumerate(pairs, 1):
        a, b = PREFIX + a, PREFIX + b
        if reciprocal:
            req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
            edges.extend([{"edge_id": req, "type": "proof_requires", "from": a, "to": b, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": b, "to": a, "reciprocal_edge_id": req}])
        else:
            edges.append({"edge_id": f"{edge_type[:3].upper()}{i:02d}", "type": edge_type, "from": a, "to": b})
    return edges

graph_edges = {
    "proof": edges_for_pairs(proof_pairs, reciprocal=True),
    "refinement": edges_for_pairs([("B-REDUCTION", "C-CORRECT"), ("T-WITNESS", "C-PRESENTATION")]),
    "provenance": edges_for_pairs([("X-PROVENANCE", "L-HALTING"), ("X-PROVENANCE", "T-ASSEMBLE")], edge_type="provenance_of"),
    "evidence": edges_for_pairs([("X-PROVENANCE", "ROOT")], edge_type="evidence_for"),
    "trust": edges_for_pairs([("ROOT", "S-FOUNDATION")], edge_type="trusts"),
    "documentation": edges_for_pairs([("X-SOURCE", "ROOT"), ("X-SOURCE", "B-REDUCTION")], edge_type="documents"),
    "workflow": edges_for_pairs([("ROOT", "X-PROVENANCE"), ("ROOT", "X-SOURCE")], edge_type="workflow_depends_on"),
}
graphs = {}
for name, edges in graph_edges.items():
    outgoing, incoming = {i: [] for i in ids}, {i: [] for i in ids}
    for e in edges:
        outgoing[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

nodes = []
for row, (_, kind, human, formal, machine, _) in zip(rows, spec):
    oid = row["obligation_id"]
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": machine, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "lean:Stage1.THM_M_0711.novikovBooneTarget_of_witness" if oid.endswith("T-ASSEMBLE") else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or experiment may close this node", "step_budget": 100 if row["risk_class"] == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof_requires children and the formal context.", "inference": human, "output": human, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0711/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture only; no open construction or reduction is claimed closed.",
        "task_ids": [ITEM, "S56-M-0711-PROOF"], "owned_sources": ["ObligationTree.lean"] if oid.endswith("T-ASSEMBLE") else [],
        "owner": "THM-M-0711 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if machine == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if machine == "M0-L" else "open"},
    })

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": THEOREM + "-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": PREFIX + "ROOT", "edge_direction": "proof_requires parent to child; composes child to parent",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "theorem_complete": False, "remaining_root_cut_set": [PREFIX + "B-REDUCTION", PREFIX + "S-FOUNDATION"]},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [
    {"recipe_id": "VAL-" + oid, "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0711/ObligationTree.lean"], "cwd": "Formalizations/Lean", "network_policy": "denied"} for oid in ids
]}
for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")
print(digest)
