#!/usr/bin/env python3
"""Build the frozen THM-M-1036 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1036-OBLIGATION_TREE"
THEOREM = "THM-M-1036"
PREFIX = "M1036"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen finite-dimensional Brownian Ito SDE strong-existence and indistinguishability target.", "Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the Problem, IntegralSemantics, StrongSolution, and Indistinguishable vocabulary without weakening any field.", "Stage1Instances.THM_M_1036.{Problem,IntegralSemantics,StrongSolution,Indistinguishable}", "The exact elaborated vocabulary and contexts."),
    ("S-BOUNDARY", "terminal", "high", "Cover positive horizon, zero state/noise dimensions, endpoint times, null events, and indistinguishability rather than fixed-time equality.", "planned boundary-case lemmas for the exact frozen structures", "All degenerate cases required by the quantified root."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, Bochner integration, probability-measure instances, imports, axioms, and the kernel/TCB closure.", "planned transitive foundation and axiom certificate", "Accepted foundation and trust profile."),
    ("X-INTEGRAL-SEMANTICS", "bridge", "critical", "Construct standard Bochner time integration and Ito integration with all laws used below, and connect those laws to the two frozen standard-integral propositions.", "planned pinned stochastic-integral API and checked transport into IntegralSemantics", "Integral linearity, isometry, measurability, continuity, and limit laws for the exact interpretation."),
    ("C-PICARD", "construction", "critical", "Construct Picard iterates from the initial process using the drift time integral and diffusion Ito integral.", "planned Picard sequence in StrongSolution process space", "A well-defined adapted sequence of approximate solution processes."),
    ("L-PICARD-INVARIANTS", "core_lemma", "critical", "Prove adaptedness, joint measurability, continuous paths, and square-integrability uniformly for every Picard iterate.", "planned exact iterate-invariant theorem", "Every iterate lies in the analytic process class required downstream."),
    ("L-PICARD-ESTIMATE", "core_lemma", "critical", "Use global Lipschitz bounds, deterministic integral estimates, and Ito isometry to bound successive Picard differences.", "planned factorial/supremum L2 Picard estimate", "A summable quantitative bound for successive iterates."),
    ("L-PICARD-CONVERGENCE", "core_lemma", "critical", "Derive convergence in the required process norm and an almost-sure continuous adapted limiting process.", "planned complete-process-space convergence theorem", "A candidate limiting process with continuity, adaptedness, and integrability."),
    ("C-LIMIT-SOLUTION", "construction", "critical", "Construct the limit process as a StrongSolution by passing both integrals through the Picard limit.", "planned StrongSolution constructor from the Picard limit", "Nonempty (StrongSolution D I)."),
    ("L-UNIQUENESS-ESTIMATE", "core_lemma", "critical", "For two strong solutions derive the stopped/supremum L2 difference inequality using Lipschitz and Ito estimates.", "planned exact two-solution difference estimate", "A Gronwall-ready nonnegative difference bound."),
    ("L-GRONWALL", "bridge", "high", "Apply a pinned integral Gronwall theorem in the exact time/domain representation and discharge its measurability and integrability premises.", "planned checked Gronwall bridge", "The two solutions agree almost everywhere at all horizon times."),
    ("L-INDISTINGUISHABLE", "core_lemma", "critical", "Upgrade the quantitative equality and continuous paths to one conull event on which the solutions agree for every time.", "planned continuity/dense-time indistinguishability theorem", "Indistinguishable X Y."),
    ("T-EXISTENCE", "terminal", "critical", "Assemble integral semantics, Picard invariants, convergence, and limit passage into strong existence for every root input.", "Stage1Instances.THM_M_1036.StrongExistencePackage", "The complete strong-existence package."),
    ("T-UNIQUENESS", "terminal", "critical", "Assemble the difference estimate, Gronwall, and continuity upgrade into pathwise uniqueness for every root input.", "Stage1Instances.THM_M_1036.PathwiseUniquenessPackage", "The complete pathwise-uniqueness package."),
    ("T-ASSEMBLE", "transport", "high", "Conjoin the exact existence and uniqueness packages without changing binders, hypotheses, or conclusion.", "Stage1Instances.THM_M_1036.root_of_existence_and_uniqueness", "The exact canonical root conditional on both packages."),
    ("X-SOURCE", "terminal", "high", "Map every analytic obligation to a reviewed primary-source theorem/page, assumptions, conventions, and errata record.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory every terminal body, wrapper, import, axiom, trust edge, and replay receipt.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fp = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1036/ObligationTree.lean#root_of_existence_and_uniqueness" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-4.29.0+mathlib-8a178386/stochastic-calculus-extension-pending",
        "tcb_profile": "lean-kernel+mathlib/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if suffix in {"X-INTEGRAL-SEMANTICS", "L-PICARD-ESTIMATE", "L-PICARD-CONVERGENCE", "C-LIMIT-SOLUTION"} else 50,
        "semantic_step_ledger": {"premises": "Only the exact formal context and declared proof children.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parent edges may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1036/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen obligation or conditional interface only; no analytic proof or root closure unless explicit evidence is attached.",
        "task_ids": [ITEM, "S56-M-1036-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1036/ObligationTree.lean"] if suffix in {"T-EXISTENCE", "T-UNIQUENESS", "T-ASSEMBLE"} else [],
        "owner": "THM-M-1036 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "obligation registry", "source map", "toolchain", "integral semantics"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable-revision negative anchor audit; Picard iteration plus Gronwall architecture; eligibility frozen independently of closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": oids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Architecture and denominators only; no SDE existence or uniqueness proof, H0 source acceptance, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-EXISTENCE", f"{PREFIX}-T-UNIQUENESS"],
    f"{PREFIX}-T-EXISTENCE": [f"{PREFIX}-C-LIMIT-SOLUTION"],
    f"{PREFIX}-C-LIMIT-SOLUTION": [f"{PREFIX}-L-PICARD-CONVERGENCE", f"{PREFIX}-X-INTEGRAL-SEMANTICS"],
    f"{PREFIX}-L-PICARD-CONVERGENCE": [f"{PREFIX}-L-PICARD-ESTIMATE", f"{PREFIX}-L-PICARD-INVARIANTS"],
    f"{PREFIX}-L-PICARD-ESTIMATE": [f"{PREFIX}-C-PICARD", f"{PREFIX}-X-INTEGRAL-SEMANTICS"],
    f"{PREFIX}-L-PICARD-INVARIANTS": [f"{PREFIX}-C-PICARD", f"{PREFIX}-X-INTEGRAL-SEMANTICS"],
    f"{PREFIX}-T-UNIQUENESS": [f"{PREFIX}-L-INDISTINGUISHABLE"],
    f"{PREFIX}-L-INDISTINGUISHABLE": [f"{PREFIX}-L-GRONWALL", f"{PREFIX}-L-UNIQUENESS-ESTIMATE"],
    f"{PREFIX}-L-GRONWALL": [f"{PREFIX}-L-UNIQUENESS-ESTIMATE"],
    f"{PREFIX}-L-UNIQUENESS-ESTIMATE": [f"{PREFIX}-X-INTEGRAL-SEMANTICS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-PICARD", f"{PREFIX}-C-PICARD", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-UNIQUE", f"{PREFIX}-L-UNIQUENESS-ESTIMATE", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-INTEGRAL", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-INTEGRAL-SEMANTICS"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-C-PICARD")],
    "workflow": [edge("FLOW-EXIST", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-EXISTENCE"), edge("FLOW-UNIQUE", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-UNIQUENESS"), edge("FLOW-PROV", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {
        "closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": [f"{PREFIX}-X-INTEGRAL-SEMANTICS", f"{PREFIX}-C-PICARD", f"{PREFIX}-L-UNIQUENESS-ESTIMATE"],
        "composition_certificates": ["Stage1Instances.THM_M_1036.root_of_existence_and_uniqueness"],
        "modeling_warning": "IntegralSemantics.standard_time_integral and standard_ito_integral are opaque propositions with no laws in Statement.lean. A proof cannot soundly use standard integral laws until a checked construction/transport makes this bridge substantive; strengthening the frozen target would require a new statement fingerprint.",
        "reason": "Final composition is conditional; both analytic packages and the integral-semantics bridge remain open.",
    },
}
specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids],
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
