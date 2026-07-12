#!/usr/bin/env python3
"""Build the deterministic THM-M-1271 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1271-OBLIGATION_TREE"

def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()

def planned(text):
    return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()

rows = [
    ("M1271-ROOT", "root", "The exact canonical mountain-pass target", "critical", "required", "required"),
    ("M1271-S-DEFINITIONS", "definition", "Freeze Palais-Smale, admissible paths, path height, and minimax level", "high", "required", "not_applicable"),
    ("M1271-S-FOUNDATION", "certificate", "Audit classical sInf/sSup, choice, TCB, and axiom closure", "critical", "required", "not_applicable"),
    ("M1271-C-PATH-MAX", "construction", "Show each admissible path has a finite attained height compatible with PathHeight", "high", "required", "required"),
    ("M1271-L-SPHERE-CROSSING", "core_lemma", "Every admissible path from zero to e crosses the rho sphere", "high", "required", "required"),
    ("M1271-T-BARRIER", "terminal", "Derive alpha <= MountainPassLevel Phi e from path crossing and minimax order", "critical", "required", "required"),
    ("M1271-C-PS-SEQUENCE", "construction", "Construct a sequence at the minimax level with derivative norm tending to zero", "critical", "required", "required"),
    ("M1271-L-PS-COMPACT", "core_lemma", "Apply the canonical Palais-Smale predicate to obtain a convergent subsequence", "critical", "required", "required"),
    ("M1271-L-LIMIT-PASSAGE", "core_lemma", "Pass functional values and Frechet derivatives to the subsequential limit", "critical", "required", "required"),
    ("M1271-T-CRITICAL", "terminal", "Produce a critical point whose value is exactly the minimax level", "critical", "required", "required"),
    ("M1271-T-ASSEMBLE", "terminal", "Compose barrier and critical packages into the exact canonical root", "critical", "required", "required"),
    ("M1271-X-SOURCE", "terminal", "Pinpoint primary-source premises and proof steps for each mathematical node", "high", "not_applicable", "required"),
    ("M1271-X-PROVENANCE", "certificate", "Track terminal bodies, wrappers, imports, and unique proof credit", "critical", "informational", "not_applicable"),
]

statement_fp = "lean-expression-sha256:686a7f777a77c3f91504e4c48cd3d0fab19ef802ce3df1751dc4288e62592d7b"
obligations = []
for oid, kind, text, risk, machine, human in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": statement_fp if oid in {"M1271-ROOT", "M1271-S-DEFINITIONS"} else planned(text),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"M1271-X-SOURCE": "human_source_boundary_only", "M1271-X-PROVENANCE": "provenance_overlay_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r[0] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-1271", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus the immutable anchor audit; eligibility was fixed before proof execution and independently of closure availability.",
    "frozen_against_statement_sha256": sha("Statement.lean"),
    "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M1271-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1271-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.",
    "obligations": obligations,
}

formal = {
    "M1271-ROOT": "Stage1Instances.THM_M_1271.MountainPassTarget",
    "M1271-S-DEFINITIONS": "Stage1Instances.THM_M_1271.{PalaisSmale,IsAdmissiblePath,PathHeight,MountainPassLevel}",
    "M1271-T-BARRIER": "Stage1Instances.THM_M_1271.MountainPassBarrierPackage",
    "M1271-T-CRITICAL": "Stage1Instances.THM_M_1271.MountainPassCriticalPackage",
    "M1271-T-ASSEMBLE": "Stage1Instances.THM_M_1271.root_of_barrier_and_critical_packages",
}
nodes = []
for oid, kind, text, risk, machine, human in rows:
    validated = "2026-07-12" if oid in {"M1271-S-DEFINITIONS", "M1271-T-ASSEMBLE"} else None
    mdebt = "M0-L" if oid == "M1271-S-DEFINITIONS" else ("M0-P" if oid == "M1271-T-ASSEMBLE" else ("M3" if oid == "M1271-ROOT" else "M4"))
    nodes.append({
        "node_id": "THM-M-1271-" + oid.removeprefix("M1271-"), "obligation_id": oid,
        "kind": kind, "human_statement": text,
        "formal_target": formal.get(oid, "planned exact Lean signature: " + text),
        "output": text, "human_debt": "H3", "machine_debt": mdebt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation is eligible",
        "step_budget": 100 if risk == "critical" else 60,
        "semantic_step_ledger": {"premises": "Only typed proof_requires children and the canonical formal context.", "inference": text, "output": text, "outgoing_use": "Consumed only by the declared typed parent or a non-proof support edge."},
        "public_readable_target": "Stage1_Instances/THM-M-1271/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional composition only; no open child or package is claimed proved.",
        "task_ids": [ITEM, "S56-M-1271-PROOF"], "owned_sources": (["Stage1_Instances/THM-M-1271/ObligationTree.lean"] if oid == "M1271-T-ASSEMBLE" else []),
        "owner": "THM-M-1271 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": validated, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if validated else "open"},
    })

proof_pairs = [
    ("M1271-ROOT", "M1271-T-ASSEMBLE"),
    ("M1271-T-ASSEMBLE", "M1271-T-BARRIER"), ("M1271-T-ASSEMBLE", "M1271-T-CRITICAL"),
    ("M1271-T-BARRIER", "M1271-C-PATH-MAX"), ("M1271-T-BARRIER", "M1271-L-SPHERE-CROSSING"),
    ("M1271-T-CRITICAL", "M1271-C-PS-SEQUENCE"), ("M1271-T-CRITICAL", "M1271-L-PS-COMPACT"),
    ("M1271-T-CRITICAL", "M1271-L-LIMIT-PASSAGE"),
]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    a, b = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b}, {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a}]

def graph(edges):
    incoming, outgoing = {i: [] for i in ids}, {i: [] for i in ids}
    for e in edges:
        outgoing[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

support = {
    "refinement": [("R01", "logical_decomposition", "M1271-T-BARRIER", "M1271-S-DEFINITIONS"), ("R02", "logical_decomposition", "M1271-T-CRITICAL", "M1271-S-FOUNDATION")],
    "provenance": [("V01", "provenance_of", "M1271-X-PROVENANCE", "M1271-ROOT")],
    "evidence": [], "trust": [("U01", "trusts", "M1271-ROOT", "M1271-S-FOUNDATION")],
    "documentation": [("D01", "source_map", "M1271-ROOT", "M1271-X-SOURCE"), ("D02", "documents", "M1271-X-SOURCE", "M1271-T-BARRIER"), ("D03", "documents", "M1271-X-SOURCE", "M1271-T-CRITICAL")],
    "workflow": [("W01", "workflow_depends_on", "M1271-T-ASSEMBLE", "M1271-T-BARRIER"), ("W02", "workflow_depends_on", "M1271-T-ASSEMBLE", "M1271-T-CRITICAL")],
}
graphs = {"proof": graph(proof_edges)}
for name, entries in support.items():
    graphs[name] = graph([{"edge_id": eid, "type": typ, "from": src, "to": dst} for eid, typ, src, dst in entries])

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1271",
    "registry_id": "THM-M-1271-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1271-ROOT", "edge_direction": "Proof requirements run parent to child; composes edges are reciprocal child-to-parent edges.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False, "first_open_cut_set": ["M1271-T-BARRIER", "M1271-T-CRITICAL"], "checked_composition": "Stage1Instances.THM_M_1271.root_of_barrier_and_critical_packages"},
}

recipes = []
for oid in ids:
    is_lean = oid in {"M1271-ROOT", "M1271-T-ASSEMBLE"}
    argv = ["python3", "Stage1_Instances/THM-M-1271/check_lean_composition.py"] if is_lean else ["python3", "Stage1_Instances/THM-M-1271/check_obligation_tree.py"]
    recipes.append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": argv, "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact exit and structural assertions"}], "covered_obligation_ids": [oid], "covered_declarations": ([formal[oid]] if oid in formal else [])})
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1271", "recipes": recipes}

for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1271 obligation tree", "", "Frozen denominator: `sha256:" + denominator + "`.", "", "The root remains `M3`. The Lean file checks only conditional composition of the open barrier and critical-point packages.", ""]
for oid, kind, text, *_ in rows:
    lines += ["## " + oid.lower(), "", f"**{kind}.** {text}.", "", "Boundary: architecture and ledger only; open proof work receives no closure credit.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(obligations)} obligations; denominator sha256: {denominator}")
