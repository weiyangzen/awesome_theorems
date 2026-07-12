#!/usr/bin/env python3
"""Build the frozen THM-M-1161 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

rows = [
    ("ROOT", "root", "Exact second-kind Fredholm alternative for the frozen kernel model.", "Root", "critical", "H1", "M4", 8),
    ("S-MODEL", "definition", "Fix the compact measured domain, Hilbert space, kernel realization, and compact operator witnesses.", "Model", "high", "H1", "M3", 18),
    ("S-SOLVES", "definition", "The pointwise integral equation is exactly the operator equation transported through realize.", "Solves", "high", "H1", "M3", 12),
    ("S-BOUNDARY", "branch", "Retain lambda zero, zero kernel, zero datum, and both homogeneous-kernel cases.", "Root boundary instances", "high", "H1", "M4", 16),
    ("S-FOUNDATION", "certificate", "Fix classical complex Hilbert-space foundations and the kernel/dependency trust boundary.", "axiom and TCB profile", "high", "H1", "M3", 12),
    ("N-OPERATOR", "normalization", "Normalize the pointwise equation to A phi = f for A = I - lambda T.", "operator/integral equivalence", "critical", "H1", "M4", 24),
    ("N-TRANSPORT", "transport", "Transport equality, existence, uniqueness, kernel membership, and range membership through realize_injective.", "faithful pointwise/operator transport", "critical", "H1", "M4", 28),
    ("B-DICHOTOMY", "branch", "Either the homogeneous kernel is trivial or it contains a nonzero vector, with exhaustive recomposition.", "KernelDichotomy", "high", "H1", "M4", 12),
    ("B-TRIVIAL", "branch", "Under trivial homogeneous kernel, every datum has a unique solution.", "FirstBranchBridge", "critical", "H1", "M4", 32),
    ("B-NONTRIVIAL", "branch", "Under nontrivial homogeneous kernel, solvability is exactly adjoint orthogonality.", "SecondBranchBridge", "critical", "H1", "M4", 36),
    ("C-ADJOINT", "construction", "Construct the adjoint of I - lambda T and identify its homogeneous solutions.", "ContinuousLinearMap.adjoint A", "critical", "H1", "M3", 24),
    ("L-BIJECTIVE", "core_lemma", "For compact T, injectivity of I - lambda T implies bijectivity, including lambda zero.", "injective_to_bijective planned signature", "critical", "H1", "M4", 48),
    ("L-CLOSED-RANGE", "core_lemma", "The range of I - lambda T is closed.", "closed_range planned signature", "critical", "H1", "M4", 55),
    ("L-ORTHOGONAL", "core_lemma", "Range membership is equivalent to orthogonality to the kernel of the adjoint.", "range_iff_adjoint_orthogonal planned signature", "critical", "H1", "M4", 42),
    ("X-SPECTRAL", "bridge", "Audit and use the pinned compact-operator eigenvalue/resolvent theorem without treating it as the root.", "IsCompactOperator.hasEigenvalue_or_mem_resolventSet", "high", "H1", "M3", 35),
    ("X-ADJOINT", "bridge", "Audit and use pinned adjoint range/orthogonal-complement identities.", "ContinuousLinearMap.orthogonal_range", "high", "H1", "M3", 30),
    ("X-SOURCE", "terminal", "Map every analytic node to exact primary-source pages, assumptions, and errata.", "human source record", "high", "H1", "M3", 20),
    ("X-TCB", "terminal", "Close transitive declarations, axioms, compiled artifacts, and reproducibility inputs.", "trust evidence record", "high", "H1", "M3", 24),
    ("T-ASSEMBLE", "terminal", "Consume the dichotomy and both conditional branch bridges to yield the exact root.", "root_compose", "critical", "H1", "M3", 10),
]

oid = lambda short: f"M1161-{short}"
statement_hash = hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
audit_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
for short, kind, human, formal, risk, h, m, budget in rows:
    fingerprint = hashlib.sha256((human + "\0" + formal).encode()).hexdigest()
    obligations.append({
        "obligation_id": oid(short),
        "statement_fingerprint": f"planned:v1:sha256:{fingerprint}" if short != "ROOT" else "source:statement.json#canonical_expression_sha256",
        "kind": kind,
        "root_relevant": short not in {"X-SOURCE", "X-TCB"},
        "machine_eligibility": "informational" if short in {"X-SOURCE", "X-TCB"} else "required",
        "human_source_eligibility": "not_applicable" if short in {"S-FOUNDATION", "X-TCB"} else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": "repo:AwesomeTheorems.Stage1.THM_M_1161.ObligationTree.root_compose" if short == "T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-1161-OBLIGATION_TREE",
    "theorem_id": "THM-M-1161",
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated canonical target and completed bounded anchor audit determine this architecture; eligibility is frozen without proof-phase closure credit.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": audit_hash,
    "root_obligation_id": oid("ROOT"),
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations],
        "informational_overlays": [oid("X-SOURCE"), oid("X-TCB")],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for short, kind, human, formal, risk, h, m, budget in rows:
    nodes.append({
        "node_id": f"THM-M-1161-{short}", "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal,
        "output": human, "human_debt": h, "machine_debt": m, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "SRC-M1161-PRIMARY-OPEN" if short != "S-FOUNDATION" else "not-applicable",
        "provenance_id": "PROV-M1161-ANCHORS" if short.startswith("X-") else "none",
        "foundation_profile": "Lean classical complex Hilbert-space functional analysis; release axiom audit open",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed proof children where present"], "inference": formal, "output": human, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": f"Stage1_Instances/THM-M-1161/obligation-tree.md#{short.lower()}",
        "validation_spec_id": f"VAL-M1161-{short}",
        "status_boundary": "Architecture only; this phase credits no analytic premise or root closure.",
        "task_ids": ["S56-M-1161-OBLIGATION_TREE", "S56-M-1161-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1161/obligation-registry.json", "Stage1_Instances/THM-M-1161/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

graphs = {name: {"edges": [], "out": {oid(s): [] for s, *_ in rows}, "in": {oid(s): [] for s, *_ in rows}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}

def edge(graph, typ, source, target, reciprocal=None):
    eid = f"E-{graph.upper()}-{len(graphs[graph]['edges']) + 1:02d}"
    item = {"edge_id": eid, "type": typ, "from": oid(source), "to": oid(target)}
    if reciprocal:
        item["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(item)
    graphs[graph]["out"][oid(source)].append(eid)
    graphs[graph]["in"][oid(target)].append(eid)
    return eid

for parent, child in [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "B-DICHOTOMY"), ("T-ASSEMBLE", "B-TRIVIAL"), ("T-ASSEMBLE", "B-NONTRIVIAL"), ("B-TRIVIAL", "L-BIJECTIVE"), ("B-TRIVIAL", "N-TRANSPORT"), ("B-NONTRIVIAL", "L-CLOSED-RANGE"), ("B-NONTRIVIAL", "L-ORTHOGONAL"), ("B-NONTRIVIAL", "C-ADJOINT"), ("L-BIJECTIVE", "X-SPECTRAL"), ("L-ORTHOGONAL", "X-ADJOINT"), ("N-TRANSPORT", "N-OPERATOR"), ("N-OPERATOR", "S-SOLVES")]:
    req = edge("proof", "proof_requires", parent, child)
    comp = edge("proof", "composes", child, parent, req)
    graphs["proof"]["edges"][-2]["reciprocal_edge_id"] = comp

for child in ("S-MODEL", "S-SOLVES", "S-BOUNDARY", "S-FOUNDATION", "N-OPERATOR", "N-TRANSPORT"):
    edge("refinement", "logical_decomposition", "ROOT", child)
for source, target in (("X-SPECTRAL", "L-BIJECTIVE"), ("X-ADJOINT", "L-ORTHOGONAL"), ("X-SOURCE", "ROOT")):
    edge("provenance", "provenance_of", source, target)
for target in ("ROOT", "X-SPECTRAL", "X-ADJOINT"):
    edge("evidence", "evidence_for", "X-TCB", target)
for target in ("ROOT", "X-SPECTRAL", "X-ADJOINT"):
    edge("trust", "trusts", target, "X-TCB")
for short, *_ in rows:
    if short != "ROOT": edge("documentation", "documents", "ROOT", short)
for source, target in (("S-MODEL", "N-OPERATOR"), ("N-OPERATOR", "B-DICHOTOMY"), ("B-DICHOTOMY", "T-ASSEMBLE"), ("X-SPECTRAL", "L-BIJECTIVE"), ("X-ADJOINT", "L-ORTHOGONAL"), ("T-ASSEMBLE", "ROOT")):
    edge("workflow", "workflow_depends_on", target, source)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1161-OBLIGATION_TREE", "theorem_id": "THM-M-1161",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": [oid("B-DICHOTOMY"), oid("L-BIJECTIVE"), oid("L-CLOSED-RANGE"), oid("L-ORTHOGONAL")]},
}

recipes = []
for short, *_ in rows:
    recipes.append({"recipe_id": f"VAL-M1161-{short}", "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1161/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(short)]})
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": "S56-M-1161-OBLIGATION_TREE", "theorem_id": "THM-M-1161", "recipes": recipes}

for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {denominator}")
