#!/usr/bin/env python3
"""Build the frozen THM-M-1291 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1291-OBLIGATION_TREE"
THEOREM = "THM-M-1291"

# IDs and eligibility are fixed before any proof work.  Planned targets are
# intentionally descriptive until the proof lane gives them exact Lean types.
SPECS = [
    ("M1291-ROOT", "root", "The exact canonical BrezisLiebTarget.", "Stage1Instances.THM_M_1291.BrezisLiebTarget", "critical", "required", "required", "required", 20),
    ("M1291-S-STATEMENT", "definition", "Preserve the arbitrary measure space, complex scalar, p > 0, AE convergence, and one uniform integral bound.", "Stage1Instances.THM_M_1291.BrezisLiebTarget", "critical", "required", "required", "required", 20),
    ("M1291-S-MEASURABILITY", "normalization", "Derive the measurable and integrable density facts needed for f and fseq n - f.", "planned exact Lean density regularity package", "high", "required", "required", "required", 70),
    ("M1291-S-BOUNDARY", "branch", "Retain null-measure spaces and every exponent 0 < p, splitting the analytic estimates at p = 1 without excluding either branch.", "planned exact boundary and exponent split", "high", "required", "required", "required", 50),
    ("M1291-S-FOUNDATION", "certificate", "Audit imports, axioms, classical principles, and computation boundaries.", "planned transitive foundation report", "critical", "required", "not_applicable", "required", 40),
    ("M1291-B-SUBUNIT", "core_lemma", "For 0 < p <= 1, establish the subadditive rpow remainder estimate used by truncation.", "planned Lean rpow estimate for 0 < p <= 1", "critical", "required", "required", "required", 100),
    ("M1291-B-SUPERUNIT", "core_lemma", "For 1 < p, establish the epsilon remainder estimate controlling |a+b|^p - |a|^p.", "planned Lean epsilon rpow estimate for 1 < p", "critical", "required", "required", "required", 100),
    ("M1291-B-MERGE", "transport", "Merge the two exponent regimes into one pointwise remainder estimate for every p > 0.", "planned checked exponent-case merge", "high", "required", "required", "required", 40),
    ("M1291-L-POINTWISE", "lemma", "Use AE convergence and the merged scalar estimate to obtain AE convergence of the corrected remainder density.", "planned AE pointwise remainder convergence", "critical", "required", "required", "required", 80),
    ("M1291-L-TRUNCATION", "construction", "Construct a nonnegative truncated error density whose integral uniformly controls the corrected remainder.", "planned truncation/error-density construction", "critical", "required", "required", "required", 100),
    ("M1291-L-TAIL", "core_lemma", "Show the truncated error tails vanish uniformly using only the stated uniform p-power integral bound.", "planned uniform tail lemma", "critical", "required", "required", "required", 100),
    ("M1291-T-INTEGRAL", "bridge", "Convert AE pointwise convergence plus truncation and tail control into convergence of corrected remainder integrals to zero.", "planned exact integral-convergence theorem", "critical", "required", "required", "required", 100),
    ("M1291-T-ALGEBRA", "transport", "Rewrite corrected remainder convergence into the exact SplittingLimit expression without changing integral semantics.", "planned checked integral algebra transport", "high", "required", "required", "required", 40),
    ("M1291-T-ASSEMBLE", "terminal", "Quantify the analytic result over the canonical binders and discharge the exact public root.", "planned theorem of type Stage1Instances.THM_M_1291.BrezisLiebTarget", "critical", "required", "required", "required", 30),
    ("M1291-X-SOURCE", "terminal", "Pinpoint the primary proof and map every material transition to the analytic obligations.", "human source boundary; no Lean proposition", "high", "not_applicable", "required", "required", 70),
    ("M1291-X-PROVENANCE", "certificate", "Classify every terminal proof body, import, bridge, and transitive origin.", "planned content-addressed provenance closure", "critical", "informational", "not_applicable", "required", 50),
    ("M1291-X-TRUST", "certificate", "Record executable, compiled-artifact, automation, computation, and replay trust boundaries.", "planned release trust record", "critical", "informational", "not_applicable", "required", 50),
]


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def fingerprint(oid, target):
    if oid in {"M1291-ROOT", "M1291-S-STATEMENT"}:
        return "lean-expression-sha256:d33af3afa4d754bac48547f753d7bda319f46e538766e7c763fa437376599884"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()


obligations, nodes = [], []
for oid, kind, statement, target, risk, machine, human, readable, budget in SPECS:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ("governance_overlay_no_proof_credit" if machine == "informational" else "human_source_boundary_only" if machine == "not_applicable" else None),
        "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": "THM-M-1291-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": statement,
        "human_debt": "H2", "machine_debt": "M3" if oid == "M1291-ROOT" else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": "pending", "foundation_profile": "lean4-mathlib-classical/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none credited", "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "Canonical hypotheses plus the declared proof_requires children only.",
            "inference": statement, "output": statement,
            "outgoing_use": "Only through a declared reciprocal composes edge; support graphs carry no proof credit.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-1291/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Planned obligation only; no proof closure is credited.",
        "task_ids": [ITEM, "S56-M-1291-PROOF"], "owned_sources": [],
        "owner": "THM-M-1291 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "toolchain"], "revocation_state": "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated Brezis-Lieb statement and bounded immutable anchor audit; the exponent-split truncation route was selected before proof closure was observed.",
    "frozen_against_statement_sha256": sha("Statement.lean"),
    "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M1291-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; no analytic obligation, source review, provenance closure, or theorem root is closed.",
}

PAIRS = [
    ("M1291-ROOT", "M1291-T-ASSEMBLE"), ("M1291-T-ASSEMBLE", "M1291-T-ALGEBRA"),
    ("M1291-T-ALGEBRA", "M1291-T-INTEGRAL"), ("M1291-T-INTEGRAL", "M1291-L-POINTWISE"),
    ("M1291-T-INTEGRAL", "M1291-L-TRUNCATION"), ("M1291-T-INTEGRAL", "M1291-L-TAIL"),
    ("M1291-L-POINTWISE", "M1291-B-MERGE"), ("M1291-L-TRUNCATION", "M1291-B-MERGE"),
    ("M1291-L-TAIL", "M1291-L-TRUNCATION"), ("M1291-B-MERGE", "M1291-B-SUBUNIT"),
    ("M1291-B-MERGE", "M1291-B-SUPERUNIT"), ("M1291-B-MERGE", "M1291-S-BOUNDARY"),
    ("M1291-L-POINTWISE", "M1291-S-MEASURABILITY"), ("M1291-S-MEASURABILITY", "M1291-S-STATEMENT"),
]
proof = []
for parent, child in PAIRS:
    req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
    proof.extend([{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}])

OTHER = {
    "refinement": [("REF-ROOT-STATEMENT", "M1291-ROOT", "logical_decomposition", "M1291-S-STATEMENT")],
    "provenance": [("SRC-SCALAR", "M1291-B-MERGE", "source_map", "M1291-X-SOURCE"), ("SRC-INTEGRAL", "M1291-T-INTEGRAL", "source_map", "M1291-X-SOURCE"), ("PROV-ROOT", "M1291-X-PROVENANCE", "provenance_of", "M1291-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M1291-ROOT", "trusts", "M1291-S-FOUNDATION"), ("TRUST-RELEASE", "M1291-ROOT", "trusts", "M1291-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1291-X-SOURCE", "documents", "M1291-ROOT"), ("DOC-BOUNDARY", "M1291-S-BOUNDARY", "documents", "M1291-B-MERGE")],
    "workflow": [("FLOW-PROOF", "M1291-T-ASSEMBLE", "workflow_depends_on", "M1291-T-INTEGRAL"), ("FLOW-PROV", "M1291-X-PROVENANCE", "workflow_depends_on", "M1291-T-ASSEMBLE")],
}


def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}


graphs = {"proof": graph(proof), **{name: graph(edges) for name, edges in OTHER.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1291-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1291-ROOT", "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1291-T-INTEGRAL"], "composition_certificates": [], "reason": "The corrected-remainder integral convergence package and every downstream composition body remain unproved."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "argv": ["python3", "Stage1_Instances/THM-M-1291/check_obligation_tree.py"], "network_policy": "denied", "expected": "structural registry and graph validation passes; this does not close the node"} for oid, *_ in SPECS]}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
(HERE / "validation-specs.json").write_text(json.dumps(recipes, indent=2) + "\n")
print(f"generated {len(obligations)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
