#!/usr/bin/env python3
"""Generate the frozen THM-M-1255 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1255-OBLIGATION_TREE"
THEOREM = "THM-M-1255"


def sha(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


raw = [
    ("M1255-ROOT", "root", "The exact frozen Malgrange-Ehrenpreis target.", "Stage1Instances.THM_M_1255.MalgrangeEhrenpreisTarget", "M3", "critical", "required"),
    ("M1255-S-DEFINITIONS", "definition", "Preserve Euclidean space, tempered distributions, delta, coordinate derivatives, and polynomial-action definitions.", "Stage1Instances.THM_M_1255.{Space,TemperedDist,deltaZero,coordinateDerivative,PolynomialDifferentialAction}", "M0-L", "high", "not_applicable"),
    ("M1255-L-COMMUTE", "core_lemma", "Prove that distributional coordinate derivatives commute with one another.", "planned exact pairwise commutation theorem for coordinateDerivative", "M4", "critical", "required"),
    ("M1255-C-ACTION", "construction", "Construct, in every finite coordinate dimension, the polynomial algebra action sending X i to coordinate differentiation.", "Stage1Instances.THM_M_1255.PolynomialActionPackage", "M4", "critical", "required"),
    ("M1255-N-FOURIER", "reduction", "Relate the constructed P(D) action to multiplication by the polynomial Fourier symbol with all constants and signs explicit.", "planned exact Fourier intertwining theorem for the constructed polynomial action", "M4", "critical", "required"),
    ("M1255-L-DIVISION", "core_lemma", "For every nonzero multivariate polynomial symbol, construct a tempered distribution whose symbol product is the Fourier transform of delta zero.", "planned tempered-distribution division theorem for arbitrary nonzero MvPolynomial", "M4", "critical", "required"),
    ("M1255-C-FUNDSOL", "construction", "Transport the Fourier-side division witness back to a tempered fundamental solution for the chosen action.", "Stage1Instances.THM_M_1255.FundamentalSolutionsFor", "M4", "critical", "required"),
    ("M1255-T-ASSEMBLE", "transport", "Compose the action package and its fundamental solutions into the exact canonical root.", "Stage1Instances.THM_M_1255.root_of_action_and_fundamental_packages", "M0-L", "high", "required"),
    ("M1255-S-BOUNDARY", "boundary", "Check dimension zero, nonzero constants, exclusion of the zero symbol, and scalar/Fourier convention boundaries.", "planned exact boundary lemmas and convention checks", "M4", "high", "required"),
    ("M1255-S-FOUNDATION", "certificate", "Freeze classical choice, axioms, imports, TCB, and no-oracle policy for every terminal body.", "planned transitive axiom and trust report", "M4", "critical", "not_applicable"),
    ("M1255-X-SOURCE", "source", "Map every analytic leaf to primary-source theorem, page, assumptions, and errata, including the tempered strengthening.", "human source boundary only", "M4", "high", "required"),
    ("M1255-X-PROVENANCE", "certificate", "Inventory terminal proof bodies, imports, revisions, licenses, axioms, and replay evidence.", "release provenance overlay", "M4", "critical", "not_applicable"),
    ("M1255-X-READABLE", "documentation", "Provide a reader-checkable reconstruction aligned one-to-one with the semantic proof leaves.", "public readable reconstruction", "M4", "high", "required"),
]

obligations = []
for oid, kind, human, formal, machine, risk, human_eligibility in raw:
    fingerprint = "lean-expression-sha256:" + sha(formal) if machine == "M0-L" or kind == "root" else "planned:v1:sha256:" + sha(human + "|" + formal)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "not_applicable" if oid == "M1255-X-SOURCE" else ("informational" if oid in {"M1255-X-PROVENANCE", "M1255-X-READABLE"} else "required"),
        "human_source_eligibility": human_eligibility,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"M1255-X-SOURCE": "human_source_boundary_only", "M1255-X-PROVENANCE": "release_overlay_no_proof_credit", "M1255-X-READABLE": "documentation_overlay_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1255/ObligationTree.lean#root_of_action_and_fundamental_packages" if oid == "M1255-T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; Fourier/division architecture selected before observing closure metrics.",
    "frozen_against_statement_sha256": sha((HERE / "Statement.lean").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": "M1255-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1255-X-PROVENANCE", "M1255-X-READABLE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for (oid, kind, human, formal, machine, risk, _), reg in zip(raw, obligations):
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M1255-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal,
        "output": "The typed result described by this obligation, usable only through declared graph edges.",
        "human_debt": "H1" if oid == "M1255-X-SOURCE" else "H3", "machine_debt": machine, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if reg["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M1255-L-DIVISION", "M1255-C-FUNDSOL"} else 40,
        "semantic_step_ledger": {"premises": "Only incoming proof_requires children and the stated formal context.", "inference": human, "output": "The node's declared typed result.", "outgoing_use": "Only declared composes or non-proof support edges may consume the result."},
        "public_readable_target": "Stage1_Instances/THM-M-1255/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-1255-PROOF"], "owned_sources": [], "owner": "THM-M-1255 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if machine == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if machine == "M0-L" else "open"},
    })

proof_requires = [
    ("ROOT-ASSEMBLE", "M1255-ROOT", "M1255-T-ASSEMBLE"),
    ("ASSEMBLE-ACTION", "M1255-T-ASSEMBLE", "M1255-C-ACTION"),
    ("ASSEMBLE-SOLUTION", "M1255-T-ASSEMBLE", "M1255-C-FUNDSOL"),
    ("ACTION-COMMUTE", "M1255-C-ACTION", "M1255-L-COMMUTE"),
    ("SOLUTION-FOURIER", "M1255-C-FUNDSOL", "M1255-N-FOURIER"),
    ("SOLUTION-DIVISION", "M1255-C-FUNDSOL", "M1255-L-DIVISION"),
]

def indexed(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_edges = []
for label, parent, child in proof_requires:
    req, comp = "PROOF-REQ-" + label, "PROOF-COMP-" + label
    proof_edges += [
        {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req},
    ]

def edges(prefix, typ, pairs):
    return indexed([{"edge_id": f"{prefix}-{i}", "from": a, "type": typ, "to": b} for i, (a, b) in enumerate(pairs, 1)])

graphs = {
    "proof": indexed(proof_edges),
    "refinement": edges("REF", "logical_decomposition", [("M1255-S-DEFINITIONS", "M1255-ROOT"), ("M1255-S-BOUNDARY", "M1255-C-FUNDSOL")]),
    "provenance": edges("PROV", "provenance_of", [("M1255-X-PROVENANCE", "M1255-T-ASSEMBLE"), ("M1255-X-PROVENANCE", "M1255-L-DIVISION")]),
    "evidence": edges("EVID", "provenance_of", [("M1255-T-ASSEMBLE", "M1255-ROOT")]),
    "trust": edges("TRUST", "trusts", [("M1255-S-FOUNDATION", "M1255-ROOT"), ("M1255-S-FOUNDATION", "M1255-L-DIVISION")]),
    "documentation": edges("DOC", "documents", [("M1255-X-READABLE", "M1255-ROOT"), ("M1255-X-SOURCE", "M1255-L-DIVISION")]),
    "workflow": edges("FLOW", "workflow_depends_on", [("M1255-T-ASSEMBLE", "M1255-C-ACTION"), ("M1255-T-ASSEMBLE", "M1255-C-FUNDSOL"), ("M1255-X-PROVENANCE", "M1255-T-ASSEMBLE"), ("M1255-X-READABLE", "M1255-C-FUNDSOL")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1255-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1255-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M1255-S-DEFINITIONS", "M1255-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1255-C-ACTION", "M1255-C-FUNDSOL"], "composition_certificates": ["Stage1Instances.THM_M_1255.root_of_action_and_fundamental_packages"], "reason": "The final composition is conditional; neither required package has a proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1255/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
dump("obligation-registry.json", registry)
dump("typed-graphs.json", bundle)
dump("validation-specs.json", specs)
print(f"generated {len(ids)} obligations; denominator sha256: {denominator}")
