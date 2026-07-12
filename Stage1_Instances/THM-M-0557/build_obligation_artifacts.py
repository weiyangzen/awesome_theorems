#!/usr/bin/env python3
"""Generate the frozen THM-M-0557 registry and typed graph bundle."""

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


rows = [
    ("M0557-ROOT", "root", "The exact positive-dimensional group and higher commutative-group target.", "ExactTarget", "The conjunction for every X, x, and n.", "critical", "M3", 20),
    ("M0557-COMPOSE", "composition", "Compose the group and commutative branches at identical binders.", "exactTarget_of_branches", "ExactTarget", "high", "M0-L", 10),
    ("M0557-GROUP", "construction", "Construct Group on Pi (n+1).", "GroupStructureBranch", "Nonempty Group for every positive dimension.", "high", "M3", 40),
    ("M0557-GROUP-TRANSFER", "bridge", "Transfer the fundamental-group structure along the generalized-loop equivalence.", "HomotopyGroup.group; homotopyGroupEquivFundamentalGroup", "The group branch's terminal structure.", "high", "M3", 100),
    ("M0557-COMM", "construction", "Construct CommGroup on Pi (n+2).", "CommutativeStructureBranch", "Nonempty CommGroup for every dimension at least two.", "critical", "M3", 40),
    ("M0557-EH", "bridge", "Apply Eckmann-Hilton to the two coordinate multiplications.", "HomotopyGroup.commGroup; HomotopyGroup.auxGroup_indep", "Commutativity of the transferred group law.", "critical", "M3", 100),
    ("M0557-DISTRIB", "core_lemma", "Prove interchange for concatenation in two distinct cube coordinates.", "GenLoop.transAt_distrib", "The distributivity premise used by Eckmann-Hilton.", "critical", "M3", 100),
    ("M0557-PROVENANCE", "provenance_boundary", "Resolve terminal bodies, transitive dependencies, axioms, license, and source ownership.", "planned transitive provenance/trust report", "Accepted proof-body provenance and TCB boundary.", "critical", "M4", 100),
    ("M0557-SOURCE", "source_boundary", "Map the modern formal construction to an immutable human theorem locator.", "not a Lean proof premise", "Reviewed source crosswalk.", "high", "M4", 100),
]

statement_hash = sha(HERE / "Statement.lean")
anchor_hash = sha(HERE / "anchor-audit.json")
obligations = []
nodes = []
for oid, kind, human, formal, output, risk, machine, budget in rows:
    fp = hashlib.sha256((oid + "\0" + human + "\0" + formal).encode()).hexdigest()
    machine_req = oid != "M0557-SOURCE"
    source_req = oid in {"M0557-ROOT", "M0557-GROUP", "M0557-GROUP-TRANSFER", "M0557-COMM", "M0557-EH", "M0557-DISTRIB", "M0557-SOURCE"}
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": "architecture:v1:sha256:" + fp,
        "kind": kind, "root_relevant": True,
        "machine_eligibility": "required" if machine_req else "not_applicable",
        "human_source_eligibility": "required" if source_req else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None, "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": "THM-M-0557-" + oid.removeprefix("M0557-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": machine, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "pending" if source_req else "not_applicable",
        "provenance_id": "pinned-mathlib-route-pending-transitive-audit" if oid not in {"M0557-SOURCE", "M0557-PROVENANCE"} else "none",
        "foundation_profile": "Lean 4 quotient/choice/extensionality boundary pending validation",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive closure pending",
        "computation_record": "none; computation and external oracles receive no proof credit",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only incoming proof_requires outputs and the frozen formal context.", "inference": human, "output": output, "outgoing_use": "Only typed parent edges may consume this output."},
        "public_readable_target": "obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture only; no downstream proof or release credit.",
        "task_ids": ["S56-M-0557-OBLIGATION_TREE", "S56-M-0557-PROOF"], "owned_sources": [],
        "owner": "THM-M-0557 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M0557-COMPOSE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid == "M0557-COMPOSE" else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [x[0] for x in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0557-OBLIGATION_TREE", "theorem_id": "THM-M-0557",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and pinned-anchor audit; group transfer and Eckmann-Hilton routes expanded before proof integration.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0557-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {"inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0557-PROVENANCE", "M0557-SOURCE"]},
    "delta_policy": "Any split, merge, correction, exclusion, or eligibility change requires registry v2 with an append-only ID delta.",
    "obligations": obligations,
}

proof_pairs = [("M0557-ROOT", "M0557-COMPOSE"), ("M0557-COMPOSE", "M0557-GROUP"), ("M0557-COMPOSE", "M0557-COMM"), ("M0557-GROUP", "M0557-GROUP-TRANSFER"), ("M0557-COMM", "M0557-EH"), ("M0557-EH", "M0557-DISTRIB")]
graphs = {name: {"edges": [], "out": {i: [] for i in ids}, "in": {i: [] for i in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def edge(graph, eid, typ, src, dst, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e); graphs[graph]["out"][src].append(eid); graphs[graph]["in"][dst].append(eid)
for n, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{n:02d}-REQ", f"P{n:02d}-COMP"
    edge("proof", req, "proof_requires", parent, child, comp); edge("proof", comp, "composes", child, parent, req)
for n, child in enumerate(("M0557-GROUP-TRANSFER", "M0557-EH", "M0557-DISTRIB"), 1):
    edge("refinement", f"R{n:02d}", "logical_decomposition", "M0557-ROOT", child)
    edge("provenance", f"V{n:02d}", "provenance_of", "M0557-PROVENANCE", child)
    edge("trust", f"T{n:02d}", "trusts", child, "M0557-PROVENANCE")
for n, oid in enumerate(ids, 1):
    edge("evidence", f"E{n:02d}", "evidence_for", oid, oid)
    edge("documentation", f"D{n:02d}", "documents", oid, oid)
for n, (src, dst) in enumerate((("M0557-SOURCE", "M0557-ROOT"), ("M0557-PROVENANCE", "M0557-ROOT")), 1):
    edge("provenance", f"S{n:02d}", "source_map", src, dst)
for n, oid in enumerate(ids[1:], 1): edge("workflow", f"W{n:02d}", "workflow_depends_on", "M0557-ROOT", oid)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0557-OBLIGATION_TREE", "theorem_id": "THM-M-0557",
    "registry_id": "THM-M-0557-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0557-ROOT", "edge_direction": "proof_requires parent-to-child; composes child-to-parent; other graph types never provide proof credit.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "closed_obligations": ["M0557-COMPOSE"], "remaining_root_cut_set": ["M0557-GROUP", "M0557-COMM"], "audit_complete": False, "theorem_complete": False},
}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(digest)
