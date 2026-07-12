#!/usr/bin/env python3
"""Build the frozen THM-M-1012 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(path): return hashlib.sha256((HERE / path).read_bytes()).hexdigest()
def planned(text): return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()

rows = [
    ("M1012-ROOT", "root", "Exact known-limit Levy continuity equivalence", "critical", "M3", "H1"),
    ("M1012-S-DEFINITIONS", "definition", "Freeze weak convergence, characteristic functions, coercions, binders, and topology", "high", "M3", "H1"),
    ("M1012-S-BOUNDARIES", "normalization", "Cover zero frequency, zero-dimensional E, constant sequences, and both directions", "high", "M3", "H1"),
    ("M1012-S-FOUNDATION", "certificate", "Audit classical choice, quotient soundness, extensionality, imports, and TCB", "high", "M3", "H1"),
    ("M1012-B-FORWARD", "branch", "Weak convergence implies pointwise characteristic-function convergence", "critical", "M1", "H1"),
    ("M1012-B-REVERSE", "branch", "Pointwise characteristic-function convergence implies weak convergence", "critical", "M1", "H1"),
    ("M1012-C-TIGHTNESS", "construction", "Construct tightness of the range from characteristic-function convergence", "critical", "M1", "H1"),
    ("M1012-L-TIGHT-ANALYTIC", "core_lemma", "Prove tightness using the integral bound, dominated convergence, and continuity at zero", "critical", "M1", "H1"),
    ("M1012-L-WEAK-FROM-TIGHT", "bridge", "Derive weak convergence from tightness and convergence on the characteristic polynomial algebra", "critical", "M1", "H1"),
    ("M1012-L-CHARPOLY", "core_lemma", "Extend pointwise characteristic convergence to integrals of characteristic polynomials", "high", "M1", "H1"),
    ("M1012-L-SEPARATION", "core_lemma", "Show the characteristic-polynomial star subalgebra separates points", "high", "M1", "H1"),
    ("M1012-T-COMPOSE", "transport", "Compose forward and reverse branches into the exact canonical equivalence", "critical", "M3", "H1"),
    ("M1012-X-PROVENANCE", "certificate", "Bind wrapper, terminal mathlib body, source object, revision, and imported dependencies", "high", "M3", "H1"),
    ("M1012-X-SOURCE", "certificate", "Map every root-relevant mathematical node to a pinpoint primary human source", "high", "M3", "H1"),
]

machine_info = {"M1012-X-PROVENANCE", "M1012-X-SOURCE"}
human_na = {"M1012-S-DEFINITIONS", "M1012-S-FOUNDATION", "M1012-X-PROVENANCE"}
lean_fps = {
    "M1012-ROOT": "lean-expression-sha256:1baa1f00d8cab4be7e0121d56f06dd7c6b5455d7a87d5befd7604f629c44a618",
}
obligations = []
for oid, kind, statement, risk, machine, human in rows:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": lean_fps.get(oid, planned(statement)),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": "informational" if oid in machine_info else "required",
        "human_source_eligibility": "not_applicable" if oid in human_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"code": "formal_or_provenance_only", "justification": "No independent human mathematical claim; source eligibility is carried by the mapped semantic nodes.", "approval": "pending independent review"} if oid in human_na else None),
        "terminal_proof_body_id": ("mathlib:8a178386:Mathlib.MeasureTheory.Measure.LevyConvergence#ProbabilityMeasure.tendsto_iff_tendsto_charFun" if oid in {"M1012-B-FORWARD", "M1012-B-REVERSE"} else ("local:ObligationTree.lean#root_of_directions" if oid == "M1012-T-COMPOSE" else None)),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r[0] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1012-OBLIGATION_TREE", "theorem_id": "THM-M-1012",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Statement and anchor audit were frozen before this phase; eligibility is architectural and does not depend on observed closure labels.",
    "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M1012-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": sorted(machine_info),
    },
    "delta_policy": "Any split, merge, correction, exclusion, or eligibility change creates a new version and append-only ID delta.",
    "obligations": obligations,
}

formal = {
    "M1012-ROOT": "Stage1Instances.THM_M_1012.ObligationTree.RootTarget",
    "M1012-B-FORWARD": "Stage1Instances.THM_M_1012.ObligationTree.ForwardTarget",
    "M1012-B-REVERSE": "Stage1Instances.THM_M_1012.ObligationTree.ReverseTarget",
    "M1012-C-TIGHTNESS": "Stage1Instances.THM_M_1012.ObligationTree.TightnessTarget",
    "M1012-L-WEAK-FROM-TIGHT": "Stage1Instances.THM_M_1012.ObligationTree.WeakFromTightTarget",
    "M1012-T-COMPOSE": "root_of_directions : ForwardTarget -> ReverseTarget -> RootTarget",
}
nodes = []
for oid, kind, statement, risk, machine, human in rows:
    nodes.append({
        "node_id": "THM-M-1012-" + oid.removeprefix("M1012-"), "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal.get(oid, "planned signature: " + statement),
        "output": statement, "human_debt": human, "machine_debt": machine, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md#crosswalk" if oid not in human_na else "not-applicable",
        "provenance_id": "M1012-PROV-MATHLIB-LEVY" if oid != "M1012-X-SOURCE" else "none",
        "foundation_profile": "Lean4-mathlib-classical-v1-pending-validation", "tcb_profile": "lean-kernel+pinned-mathlib-v1-pending-validation",
        "computation_record": "none; no oracle, solver, or finite certificate",
        "step_budget": 12 if oid == "M1012-L-TIGHT-ANALYTIC" else 6,
        "semantic_step_ledger": {"premises": ["typed incoming graph edges"], "inference": statement, "output": statement, "outgoing_use": ["typed outgoing graph edges"]},
        "public_readable_target": "Stage1_Instances/THM-M-1012/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "M1012-VAL-STRUCTURE" if oid not in formal else "M1012-VAL-LEAN",
        "status_boundary": "Registry classification only; no proof-phase acceptance, H0/R0, release receipt, or theorem completion.",
        "task_ids": ["S56-M-1012-OBLIGATION_TREE", "S56-M-1012-PROOF", "S56-M-1012-VALIDATION"],
        "owned_sources": (["ObligationTree.lean"] if oid in formal else ["obligation-registry.json", "typed-graphs.json"]),
        "owner": "THM-M-1012 integration lane", "reviewer": "independent master reviewer pending",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "ObligationTree.lean"], "revocation_state": "not_revoked"},
    })

def graph(edges):
    out = {i: [] for i in ids}; incoming = {i: [] for i in ids}
    for e in edges: out[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("M1012-ROOT", "M1012-B-FORWARD"), ("M1012-ROOT", "M1012-B-REVERSE"), ("M1012-B-REVERSE", "M1012-C-TIGHTNESS"), ("M1012-B-REVERSE", "M1012-L-WEAK-FROM-TIGHT")]
proof_edges = []
for n, (parent, child) in enumerate(proof_pairs, 1):
    a, b = f"M1012-P{n}R", f"M1012-P{n}C"
    proof_edges += [{"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b}, {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a}]

refine_pairs = [("M1012-ROOT", "M1012-S-DEFINITIONS"), ("M1012-ROOT", "M1012-S-BOUNDARIES"), ("M1012-ROOT", "M1012-S-FOUNDATION"), ("M1012-C-TIGHTNESS", "M1012-L-TIGHT-ANALYTIC"), ("M1012-L-WEAK-FROM-TIGHT", "M1012-L-CHARPOLY"), ("M1012-L-WEAK-FROM-TIGHT", "M1012-L-SEPARATION"), ("M1012-ROOT", "M1012-T-COMPOSE")]
ref_edges = [{"edge_id": f"M1012-R{i}", "type": "logical_decomposition", "from": a, "to": b} for i, (a,b) in enumerate(refine_pairs,1)]
prov_edges = [{"edge_id": f"M1012-V{i}", "type": "provenance_of", "from": "M1012-X-PROVENANCE", "to": target} for i,target in enumerate(("M1012-B-FORWARD","M1012-B-REVERSE","M1012-C-TIGHTNESS","M1012-L-TIGHT-ANALYTIC","M1012-L-WEAK-FROM-TIGHT","M1012-L-CHARPOLY","M1012-L-SEPARATION"),1)]
source_edges = [{"edge_id": f"M1012-SM{i}", "type": "source_map", "from": "M1012-X-SOURCE", "to": target} for i,target in enumerate(ids,1) if target not in human_na]
trust_edges = [{"edge_id": f"M1012-TR{i}", "type": "trusts", "from": target, "to": "M1012-S-FOUNDATION"} for i,target in enumerate(("M1012-ROOT","M1012-B-FORWARD","M1012-B-REVERSE","M1012-T-COMPOSE"),1)]
doc_edges = [{"edge_id": f"M1012-D{i}", "type": "documents", "from": "M1012-X-SOURCE", "to": target} for i,target in enumerate(ids,1) if target != "M1012-X-SOURCE"]
workflow_order = ["M1012-S-DEFINITIONS","M1012-S-BOUNDARIES","M1012-S-FOUNDATION","M1012-B-FORWARD","M1012-C-TIGHTNESS","M1012-L-TIGHT-ANALYTIC","M1012-L-CHARPOLY","M1012-L-SEPARATION","M1012-L-WEAK-FROM-TIGHT","M1012-B-REVERSE","M1012-T-COMPOSE","M1012-ROOT"]
workflow_edges = [{"edge_id": f"M1012-W{i}", "type": "workflow_depends_on", "from": b, "to": a} for i,(a,b) in enumerate(zip(workflow_order,workflow_order[1:]),1)]

bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": "THM-M-1012", "registry_denominator_sha256": denominator, "nodes": nodes,
          "graphs": {"proof": graph(proof_edges), "refinement": graph(ref_edges), "provenance": graph(prov_edges + source_edges), "evidence": graph([]), "trust": graph(trust_edges), "documentation": graph(doc_edges), "workflow": graph(workflow_edges)},
          "closure_boundary": {"root_closed": False, "theorem_complete": False, "current_root_machine_debt": "M3", "remaining_root_cut_set": ["M1012-B-FORWARD", "M1012-C-TIGHTNESS", "M1012-L-WEAK-FROM-TIGHT"], "reason": "The graph is frozen, but proof, validation, source, readability, and release acceptance remain downstream."}}

specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": registry["item_id"], "theorem_id": "THM-M-1012", "recipes": [
    {"recipe_id": "M1012-VAL-LEAN", "command": "lake env lean ../../Stage1_Instances/THM-M-1012/ObligationTree.lean", "working_directory": "Formalizations/Lean", "network_policy": "denied", "expected_exit": 0, "covered_obligation_ids": list(formal)},
    {"recipe_id": "M1012-VAL-STRUCTURE", "command": "python3 Stage1_Instances/THM-M-1012/check_obligation_tree.py", "working_directory": ".", "network_policy": "denied", "expected_exit": 0, "covered_obligation_ids": [i for i in ids if i not in formal]},
]}

for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
print(f"built {len(ids)} obligations; denominator {denominator}")
