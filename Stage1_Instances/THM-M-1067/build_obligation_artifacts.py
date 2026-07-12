#!/usr/bin/env python3
"""Build the frozen THM-M-1067 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1067-OBLIGATION_TREE"
THEOREM = "THM-M-1067"
PREFIX = "M1067"

# id, kind, human statement, formal interface, output, risk, human debt
SPECS = [
    ("M1067-ROOT", "root", "Construct jointly continuous Brownian local time with the simultaneous occupation-density identity.", "Stage1Instances.THM_M_1067.BrownianLocalTimeTarget", "The exact canonical target.", "critical", "H2"),
    ("M1067-S-DEFINITIONS", "definition", "Freeze BrownianPath, Wiener measure, nonnegative Lebesgue measure, and local-time field types.", "Statement.lean definitions used by BrownianLocalTimeTarget", "Exact objects and binder order for every node.", "high", "not_applicable"),
    ("M1067-S-BOUNDARY", "normalization", "Preserve one common null set, all nonnegative times, all measurable ENNReal tests, and occupation normalization.", "Boundary package for IsBrownianLocalTime", "No fixed-level, fixed-test, Tanaka-only, or assumed-field substitution.", "critical", "H2"),
    ("M1067-S-FOUNDATION", "certificate", "Freeze classical noncomputable measure theory and the kernel trust policy.", "Foundation and trust certificate", "Auditable foundation profile for eventual bodies.", "critical", "not_applicable"),
    ("M1067-N-WIENER", "normalization", "Derive usable increment, covariance, Gaussian-density, and path-law facts from IsWienerMeasure.", "IsWienerMeasure W -> Wiener finite-dimensional interface", "Brownian estimates without assuming local time.", "critical", "H2"),
    ("M1067-C-APPROX", "construction", "Define nonnegative mollified occupation densities from time spent near each level.", "approxLocalTime epsilon w t x", "A measurable nonnegative approximate field.", "high", "H2"),
    ("M1067-L-MOMENTS", "core_lemma", "Prove spatial and temporal moment bounds for increments of the approximate fields.", "Uniform moment estimates for approxLocalTime", "Bounds strong enough for convergence and continuity.", "critical", "H2"),
    ("M1067-L-CAUCHY", "core_lemma", "Prove the approximations are Cauchy on compact time-space rectangles.", "Cauchy approxLocalTime in a compact-field norm", "A coherent limiting occupation-density field.", "critical", "H2"),
    ("M1067-C-LIMIT", "construction", "Choose the limiting nonnegative field without changing versions between downstream properties.", "limitLocalTime : BrownianPath -> NNReal -> Real -> NNReal", "One common candidate L for all obligations.", "critical", "H2"),
    ("M1067-L-JOINT-CONT", "core_lemma", "Use the moment bounds and a two-parameter continuity theorem to obtain a jointly continuous version.", "forall_aᵐ w ∂W, Continuous (Function.uncurry (L w))", "Joint continuity on a single full-measure event.", "critical", "H2"),
    ("M1067-L-MEAS", "core_lemma", "Prove measurability of every time-level evaluation of the selected version.", "forall t x, AEMeasurable (fun w => L w t x) W", "The pointwise measurability conjunct.", "high", "H2"),
    ("M1067-L-OCC-CORE", "core_lemma", "Pass the mollifier identity to the limit for a countable determining class of tests and times.", "Occupation identity on a countable continuous/simple determining class", "A common full-measure event for the core identity.", "critical", "H2"),
    ("M1067-L-OCC-EXTEND", "bridge", "Extend the core identity pathwise to every time and every measurable ENNReal-valued test.", "OccupationIdentityAE W L", "The exact simultaneous occupation identity.", "critical", "H2"),
    ("M1067-T-FIELD", "terminal", "Combine evaluation measurability, joint continuity, and occupation identity for the same selected field.", "IsBrownianLocalTime W L", "The exact witness property for a fixed Wiener measure.", "critical", "H2"),
    ("M1067-T-COMPOSE", "terminal", "Construct the field for each Wiener measure and package the exact existential conclusion.", "BrownianLocalTimeTarget from the registered field components", "The canonical root proposition.", "critical", "H2"),
    ("M1067-X-SOURCE", "terminal", "Map every mathematical node to exact source pinpoints, assumptions, normalization, and errata.", "Human-source crosswalk overlay", "Source classification only; no machine credit.", "high", "H2"),
    ("M1067-X-PROVENANCE", "terminal", "Record proof-body, wrapper, transitive dependency, axiom, unsafe, and computation provenance.", "Formal provenance overlay", "Provenance only; no proof credit without checked bodies.", "critical", "not_applicable"),
]

IDS = [row[0] for row in SPECS]
MACHINE = IDS[:-2]
HUMAN = [row[0] for row in SPECS if row[6] != "not_applicable"]
DENOMINATORS = {
    "inventory": IDS,
    "required_machine": MACHINE,
    "required_human_source": HUMAN,
    "required_readable": IDS,
    "informational_overlays": IDS[-2:],
}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def fingerprint(oid: str, formal: str) -> str:
    if oid == "M1067-ROOT":
        return "lean-expression-sha256:3a760f8d4cb9898c637755e90fc9ca8402c9427103006981081a7378ec46d2e1"
    raw = f"{THEOREM}/registry-v1/{oid}/{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(raw).hexdigest()


obligations = []
nodes = []
for oid, kind, human, formal, output, risk, human_debt in SPECS:
    required = oid in MACHINE
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(oid, formal),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if required else "informational",
        "human_source_eligibility": "required" if oid in HUMAN else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None if required else "overlay-no-proof-credit",
        "terminal_proof_body_id": None,
    })
    ledger = (["Consume every incoming child at its exact registered interface.", f"Derive: {output}", "Discharge the parent composition edge without an undeclared premise."]
              if kind in {"root", "terminal"} else
              ["Freeze the exact hypotheses and named interfaces.", f"Establish: {human}", f"Derive: {output}", "Pass the output through its typed edge without weakening the target."])
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": human_debt, "machine_debt": "M3" if kind == "definition" else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "pending-node-pinpoint-review" if oid != "M1067-X-PROVENANCE" else "not-applicable",
        "provenance_id": "none",
        "foundation_profile": "lean4-dependent-type-theory/classical-noncomputable-measure-theory-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": len(ledger), "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1067/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture only; no accepted proof body or closure evidence.",
        "task_ids": [ITEM, "S56-M-1067-PROOF"], "owned_sources": [],
        "owner": "THM-M-1067 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "freeze_basis": "Exact elaborated statement and bounded immutable anchor audit; architecture selected before observing proof closure.",
    "root_obligation_id": "M1067-ROOT", "frozen_denominators": DENOMINATORS,
    "eligibility_policy": "Every semantic node needed by the mollified-occupation-density route is required regardless of current library availability; overlays earn no proof credit.",
    "exclusions": [
        "A fixed level, fixed test function, Tanaka identity alone, or an assumed local-time field is not the root.",
        "Continuity and occupation identities must hold for one selected field on one common full-measure event.",
        "Aliases, wrappers, transports, source rows, and presentation splits add no semantic or terminal-body credit."
    ], "obligations": obligations,
}

PROOF = [
    ("M1067-S-DEFINITIONS", "M1067-C-APPROX", "proof_requires"),
    ("M1067-S-BOUNDARY", "M1067-L-OCC-EXTEND", "proof_requires"),
    ("M1067-S-FOUNDATION", "M1067-T-COMPOSE", "proof_requires"),
    ("M1067-N-WIENER", "M1067-C-APPROX", "proof_requires"),
    ("M1067-N-WIENER", "M1067-L-MOMENTS", "proof_requires"),
    ("M1067-C-APPROX", "M1067-L-MOMENTS", "proof_requires"),
    ("M1067-C-APPROX", "M1067-L-OCC-CORE", "proof_requires"),
    ("M1067-L-MOMENTS", "M1067-L-CAUCHY", "proof_requires"),
    ("M1067-L-CAUCHY", "M1067-C-LIMIT", "proof_requires"),
    ("M1067-C-LIMIT", "M1067-L-JOINT-CONT", "proof_requires"),
    ("M1067-L-MOMENTS", "M1067-L-JOINT-CONT", "proof_requires"),
    ("M1067-C-LIMIT", "M1067-L-MEAS", "proof_requires"),
    ("M1067-C-LIMIT", "M1067-L-OCC-CORE", "proof_requires"),
    ("M1067-L-OCC-CORE", "M1067-L-OCC-EXTEND", "proof_requires"),
    ("M1067-L-JOINT-CONT", "M1067-L-OCC-EXTEND", "proof_requires"),
    ("M1067-L-MEAS", "M1067-T-FIELD", "composes"),
    ("M1067-L-JOINT-CONT", "M1067-T-FIELD", "composes"),
    ("M1067-L-OCC-EXTEND", "M1067-T-FIELD", "composes"),
    ("M1067-T-FIELD", "M1067-T-COMPOSE", "composes"),
    ("M1067-T-COMPOSE", "M1067-ROOT", "composes"),
]
REFINEMENT = [
    ("M1067-L-MOMENTS", "M1067-L-CAUCHY", "logical_decomposition"),
    ("M1067-L-MOMENTS", "M1067-L-JOINT-CONT", "logical_decomposition"),
    ("M1067-L-OCC-CORE", "M1067-L-OCC-EXTEND", "logical_decomposition"),
    ("M1067-L-MEAS", "M1067-T-FIELD", "logical_decomposition"),
    ("M1067-L-JOINT-CONT", "M1067-T-FIELD", "logical_decomposition"),
    ("M1067-L-OCC-EXTEND", "M1067-T-FIELD", "logical_decomposition"),
]


def graph(name: str, pairs: list[tuple[str, str, str]]) -> dict:
    edges, out, incoming = [], {}, {}
    for index, (src, dst, role) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{index:03d}"
        edges.append({"edge_id": eid, "from": src, "to": dst, "type": role})
        out.setdefault(src, []).append(eid)
        incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": out, "in": incoming}


graphs = {
    "proof": graph("proof", PROOF),
    "refinement": graph("refinement", REFINEMENT),
    "provenance": graph("provenance", [("M1067-X-PROVENANCE", oid, "provenance_of") for oid in MACHINE]),
    "evidence": graph("evidence", []),
    "trust": graph("trust", [("M1067-S-FOUNDATION", oid, "trusts") for oid in MACHINE if oid != "M1067-S-FOUNDATION"]),
    "documentation": graph("documentation", [("M1067-X-SOURCE", oid, "documents") for oid in HUMAN]),
    "workflow": graph("workflow", [("M1067-X-SOURCE", "M1067-X-PROVENANCE", "workflow_depends_on"), ("M1067-X-PROVENANCE", "M1067-ROOT", "workflow_depends_on")]),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1067/registry-v1", "registry_denominator_sha256": digest(DENOMINATORS),
    "statement_source_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "root_node_id": "M1067-ROOT", "edge_direction": "prerequisite_or_child -> consumer_or_parent",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [
        {"certificate_id": "COMP-M1067-FIELD-V1", "parent": "M1067-T-FIELD", "required_children": ["M1067-L-MEAS", "M1067-L-JOINT-CONT", "M1067-L-OCC-EXTEND"], "checked_declaration": "Stage1Instances.THM_M_1067.ObligationTree.isBrownianLocalTime_of_components", "status": "interface-composition-kernel-checked; children-open"},
        {"certificate_id": "COMP-M1067-ROOT-V1", "parent": "M1067-ROOT", "required_children": ["M1067-T-COMPOSE"], "checked_declaration": "Stage1Instances.THM_M_1067.ObligationTree.brownianLocalTimeTarget_of_constructor", "status": "interface-composition-kernel-checked; child-open"},
    ],
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1067-N-WIENER", "M1067-L-MOMENTS", "M1067-L-CAUCHY", "M1067-L-JOINT-CONT", "M1067-L-OCC-CORE", "M1067-L-OCC-EXTEND"]},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
lines = ["# THM-M-1067 obligation tree", "", "Registry v1 freezes the mollified-occupation-density route before proof closure is observed. Every semantic node below remains open.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
    lines += ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(IDS)} obligations; denominator sha256 {digest(DENOMINATORS)}")
