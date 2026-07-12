#!/usr/bin/env python3
"""Build the frozen THM-M-1018 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM, THEOREM, PREFIX = "S56-M-1018-OBLIGATION_TREE", "THM-M-1018", "M1018"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact atom-free-endpoint Levy interval inversion proposition frozen in Statement.lean.", "Stage1Instances.THM_M_1018.LevyInversionTarget", "The canonical universally quantified proposition."),
    ("S-EXACT", "definition", "high", "Fix probability measures on Real, ordered atom-free endpoints, the positive-sign characteristic function, the half-open interval, and the symmetric atTop limit.", "Stage1Instances.THM_M_1018.LevyInversionTarget binders", "The exact elaborated scope and conclusion."),
    ("S-KERNEL", "definition", "high", "Use the half-open interval Fourier kernel with removable value b-a at t=0 and mathlib's characteristic-function sign convention.", "Stage1Instances.THM_M_1018.levyIntervalKernel", "A total complex-valued interval kernel."),
    ("S-BOUNDARY", "branch", "critical", "Keep a<b and both endpoint atom hypotheses; distinguish t=0 and reject the atom, reversed-order, closed-interval, and opposite-sign mutations.", "checked statement mutation and boundary ledger", "The exhaustive boundary policy for the selected theorem variant."),
    ("S-TRANSPORT", "transport", "normal", "Transport only between the canonical definition and its binder-explicit encoding.", "Stage1Instances.THM_M_1018.target_iff_expanded", "A checked bidirectional syntactic transport without new proof credit."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, integration, measure extensionality, transitive axioms, imports, and the pinned TCB.", "planned axiom/import/TCB certificate", "An accepted foundation and trust profile."),
    ("N-FUBINI", "reduction", "critical", "Rewrite the truncated characteristic-function integral as the mu-integral of the truncated interval kernel, justifying complex Fubini and all integrability conditions.", "planned truncated Fubini identity", "A physical-space integral of the truncated inversion kernel."),
    ("N-SCALE", "normalization", "high", "Normalize the inner oscillatory integral by translating x-a and x-b and scaling the symmetric truncation parameter.", "planned change-of-variables identities", "Canonical one-dimensional sine-integral expressions."),
    ("B-POSITION", "branch", "critical", "Split x into x<=a, a<x<=b, and b<x, including x=a and x=b, and prove exhaustiveness and recomposition.", "planned endpoint-aware position split", "The pointwise indicator limit with all boundary branches exposed."),
    ("C-APPROX", "construction", "critical", "Construct the truncated inversion kernel as a measurable function of x and establish the exact algebraic identity used by Fubini.", "planned measurable approximate-indicator package", "A measurable family approximating the half-open interval indicator."),
    ("L-DIRICHLET", "core_lemma", "critical", "Prove the required improper Dirichlet sine-integral limits with the exact sign, normalization, and one-sided endpoint values.", "planned Dirichlet integral theorem", "Pointwise limits for every position branch."),
    ("L-INTEGRAL-LIMIT", "core_lemma", "critical", "Pass the pointwise approximate-indicator limit through integration against an arbitrary probability measure without an invalid global dominated-convergence bound.", "planned finite-measure inversion limit argument", "Convergence of the mu-integrals to the endpoint-correct interval mass."),
    ("L-ENDPOINTS", "core_lemma", "high", "Use mu {a}=mu {b}=0 to turn the boundary-valued limiting kernel into mu(Ioc a b).", "planned endpoint-null mass identity", "The selected half-open interval mass."),
    ("T-ANALYTIC", "terminal", "critical", "Combine Fubini, normalization, Dirichlet limits, the measure-level limit argument, and endpoint-null identities for fixed mu, a, and b.", "Stage1Instances.THM_M_1018.ObligationTree.InversionFor", "The exact inversion limit for fixed admissible data."),
    ("T-ASSEMBLE", "terminal", "normal", "Quantify the fixed-data analytic result into a binder-explicit expression identical to the canonical root.", "Stage1Instances.THM_M_1018.ObligationTree.root_compose", "The exact binder-expanded canonical root conditional on T-ANALYTIC."),
    ("X-SOURCE", "terminal", "high", "Map each analytic node to a reviewed primary theorem/page, assumptions, conventions, genealogy, and errata record.", "non-machine primary-source crosswalk", "Human-source coverage without kernel credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, wrappers, axioms, trust boundaries, and replay evidence.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-EXACT", f"{PREFIX}-S-KERNEL", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-EXACT", f"{PREFIX}-S-KERNEL", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
obligations, nodes = [], []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": suffix not in {"X-SOURCE", "X-PROVENANCE"},
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1Instances.THM_M_1018.ObligationTree.root_compose" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix in {"ROOT", "T-ANALYTIC"} else "M4"),
        "readability_debt": "R3" if oid in checked else "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "SRC-M1018-PRIMARY-OPEN",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "Lean4/mathlib measure-integration; classical and transitive axiom audit pending",
        "tcb_profile": "Lean 4.29.0 plus mathlib 8a178386; transitive closure and release replay pending",
        "computation_record": "none; no numerical, native, oracle, or external computation is credited",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": ["only exact children in the typed proof graph and the frozen formal context"], "inference": claim, "output": output, "outgoing_use": "only declared typed parent edges may consume this result as proof"},
        "public_readable_target": f"Stage1_Instances/THM-M-1018/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Architecture or conditional interface only; no undeclared premise, accepted closure, or theorem completion.",
        "task_ids": [ITEM, "S56-M-1018-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1018/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1018 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before master acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated interval-mass target and immutable anchor audit determine an endpoint-aware Fubini/Dirichlet/measure-limit architecture before proof closure is inspected.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, eligibility, risk, or terminal-body change requires registry version 2 with an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen denominators and architecture only; no analytic proof, H0 source acceptance, audit completion, theorem completion, or release credit.",
}


def edge(eid, source, kind, target, reciprocal=None):
    item = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        item["reciprocal_edge_id"] = reciprocal
    return item


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-ANALYTIC"],
    f"{PREFIX}-T-ANALYTIC": [f"{PREFIX}-N-FUBINI", f"{PREFIX}-L-INTEGRAL-LIMIT", f"{PREFIX}-L-ENDPOINTS"],
    f"{PREFIX}-N-FUBINI": [f"{PREFIX}-C-APPROX"],
    f"{PREFIX}-L-INTEGRAL-LIMIT": [f"{PREFIX}-C-APPROX", f"{PREFIX}-N-SCALE", f"{PREFIX}-B-POSITION", f"{PREFIX}-L-DIRICHLET"],
    f"{PREFIX}-L-ENDPOINTS": [f"{PREFIX}-B-POSITION"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-EXACT", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-EXACT"), edge("REF-ROOT-KERNEL", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-KERNEL"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY"), edge("REF-EXACT-TRANSPORT", f"{PREFIX}-S-EXACT", "logical_decomposition", f"{PREFIX}-S-TRANSPORT")],
    "provenance": [edge("SRC-ANALYTIC", f"{PREFIX}-T-ANALYTIC", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-BOUND", f"{PREFIX}-S-BOUNDARY", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-T-ANALYTIC")],
    "workflow": [edge("FLOW-ASSEMBLE-ANALYTIC", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-ANALYTIC"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-ANALYTIC"], "composition_certificates": ["Stage1Instances.THM_M_1018.ObligationTree.root_compose"], "reason": "Binder composition is checked, but the fixed-data analytic inversion theorem has no proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1018/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network": "forbidden", "covered_ids": [oid]} for oid in oids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
