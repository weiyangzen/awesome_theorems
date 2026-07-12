#!/usr/bin/env python3
"""Generate the frozen THM-M-0510 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0510-OBLIGATION_TREE"
THEOREM = "THM-M-0510"

# IDs and eligibility are frozen independently of whether a proof is available.
ROWS = [
    ("M0510-ROOT", "root", "The ordinary partition count is equivalent to the full Hardy-Ramanujan main term along Nat.atTop.", "Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget", "critical", "required"),
    ("M0510-S-ENCODING", "definition", "Fix Nat.Partition cardinality, real coercions, atTop, IsEquivalent, and the full constant-factor main term.", "Stage1Instances.THM_M_0510.{partitionCount,hardyRamanujanMainTerm}", "high", "required"),
    ("M0510-S-BOUNDARY", "transport", "Preserve the exact named target under direct expansion and retain the totalized n = 0 boundary.", "Stage1Instances.THM_M_0510.{target_iff_expandedTarget,mainTerm_at_zero}", "high", "required"),
    ("M0510-N-EULER-PRODUCT", "normalization", "Identify the ordinary partition generating function with the reciprocal Euler product, including coefficient conventions.", "planned exact ordinary-partition Euler-product signature", "critical", "required"),
    ("M0510-N-COEFFICIENT", "reduction", "Recover partitionCount n as the nth coefficient and express it by a coefficient-extraction contour integral.", "planned coefficient extraction signature", "critical", "required"),
    ("M0510-C-CONTOUR", "construction", "Choose the n-dependent contour and prove it is admissible, avoids singularities, and has the required orientation.", "planned admissible contour construction", "critical", "required"),
    ("M0510-B-ARC-SPLIT", "branch", "Split the contour into major and minor arcs and prove exhaustive, disjoint recomposition of the coefficient integral.", "planned major/minor arc decomposition", "critical", "required"),
    ("M0510-L-MODULAR", "bridge", "Derive the near-cusp transformation of the Euler product with the exact square-root factor and exponential constant.", "planned eta/modular transformation bridge", "critical", "required"),
    ("M0510-L-MAJOR-LOCAL", "core_lemma", "Uniformly approximate the generating function on the major arc with a quantified error usable under integration.", "planned major-arc local approximation", "critical", "required"),
    ("M0510-L-MAJOR-INTEGRAL", "reduction", "Transform the major-arc integral to its saddle-point or Bessel model without losing normalization constants.", "planned major-arc model-integral reduction", "critical", "required"),
    ("M0510-L-MAJOR-ASYMPTOTIC", "terminal", "Evaluate the model integral as exp(pi*sqrt(2*n/3))/(4*n*sqrt(3)) with relative error tending to zero.", "planned exact major-arc asymptotic", "critical", "required"),
    ("M0510-L-MINOR-BOUND", "terminal", "Bound every minor-arc contribution as little-o of the full Hardy-Ramanujan main term, uniformly over the arc cover.", "planned minor-arc negligible estimate", "critical", "required"),
    ("M0510-T-RECOMBINE", "transport", "Recombine major and minor arcs into the exact partition coefficient, consuming both estimates and the contour identity.", "planned checked arc recomposition theorem", "critical", "required"),
    ("M0510-T-ASYMPTOTIC", "transport", "Convert relative-error convergence into the canonical Asymptotics.IsEquivalent target with the exact Nat filter.", "Stage1Instances.THM_M_0510.root_of_finalAsymptotic", "critical", "required"),
    ("M0510-X-SOURCE", "source_boundary", "Map every analytic step and normalization to an inspected primary proof and errata record.", "primary source node map pending", "critical", "not_applicable"),
    ("M0510-X-FOUNDATION", "certificate", "Audit complex analysis, choice, quotients, imported theorem closure, axioms, and the Lean TCB.", "planned foundation and axiom report", "critical", "required"),
    ("M0510-X-PROVENANCE", "certificate", "Record terminal proof bodies, immutable revisions, licenses, evidence receipts, and revocation inputs.", "planned provenance ledger", "critical", "informational"),
]

PROOF_REQUIRES = [
    ("M0510-ROOT", "M0510-T-ASYMPTOTIC"),
    ("M0510-T-ASYMPTOTIC", "M0510-S-ENCODING"),
    ("M0510-T-ASYMPTOTIC", "M0510-S-BOUNDARY"),
    ("M0510-T-ASYMPTOTIC", "M0510-T-RECOMBINE"),
    ("M0510-T-RECOMBINE", "M0510-N-EULER-PRODUCT"),
    ("M0510-T-RECOMBINE", "M0510-N-COEFFICIENT"),
    ("M0510-T-RECOMBINE", "M0510-C-CONTOUR"),
    ("M0510-T-RECOMBINE", "M0510-B-ARC-SPLIT"),
    ("M0510-B-ARC-SPLIT", "M0510-L-MAJOR-LOCAL"),
    ("M0510-L-MAJOR-LOCAL", "M0510-L-MODULAR"),
    ("M0510-L-MAJOR-LOCAL", "M0510-L-MAJOR-INTEGRAL"),
    ("M0510-L-MAJOR-INTEGRAL", "M0510-L-MAJOR-ASYMPTOTIC"),
    ("M0510-B-ARC-SPLIT", "M0510-L-MINOR-BOUND"),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, risk, machine in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-source-sha256:" + statement_sha) if oid in {"M0510-ROOT", "M0510-S-ENCODING"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in {"M0510-S-ENCODING", "M0510-S-BOUNDARY", "M0510-X-FOUNDATION", "M0510-X-PROVENANCE"} else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0510-X-SOURCE" else ("release_overlay_no_proof_credit" if oid == "M0510-X-PROVENANCE" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0510/ObligationTree.lean#root_of_finalAsymptotic" if oid == "M0510-T-ASYMPTOTIC" else None,
    })

ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit; circle-method major/minor-arc architecture selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0510-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0510-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

node_kind = {"normalization", "reduction", "branch", "construction", "bridge", "core_lemma", "terminal", "transport", "root", "definition", "certificate", "source_boundary"}
nodes = []
for oid, kind, human, formal, risk, machine in ROWS:
    assert kind in node_kind
    checked = oid in {"M0510-S-ENCODING", "M0510-S-BOUNDARY", "M0510-T-ASYMPTOTIC"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0510-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in {"M0510-S-BOUNDARY", "M0510-T-ASYMPTOTIC"} else ("M3" if oid in {"M0510-ROOT", "M0510-S-ENCODING"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib/classical-and-complex-analysis-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment or unchecked certificate may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only the exact formal context and declared proof-requires children.",
            "inference": human, "output": human,
            "outgoing_use": "Consumed only through declared typed parent edges; source and workflow links carry no proof credit.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0510/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface only; no unlisted premise, analytic proof, or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0510-PROOF"], "owned_sources": [],
        "owner": "THM-M-0510 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"},
    })

def graph(edge_rows):
    out = {i: [] for i in ids}; incoming = {i: [] for i in ids}
    for edge in edge_rows:
        out[edge["from"]].append(edge["edge_id"]); incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edge_rows, "out": out, "in": incoming}

proof_edges = []
for i, (parent, child) in enumerate(PROOF_REQUIRES, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [
        {"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req},
    ]

def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M0510-ROOT", "M0510-S-ENCODING"), ("M0510-B-ARC-SPLIT", "M0510-L-MAJOR-ASYMPTOTIC"), ("M0510-B-ARC-SPLIT", "M0510-L-MINOR-BOUND")])),
    "provenance": graph(edges("V", "provenance_of", [("M0510-X-PROVENANCE", x) for x in ids if x != "M0510-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0510-X-SOURCE", x) for x in ["M0510-N-EULER-PRODUCT", "M0510-C-CONTOUR", "M0510-L-MODULAR", "M0510-L-MAJOR-ASYMPTOTIC", "M0510-L-MINOR-BOUND"]])),
    "trust": graph(edges("T", "trusts", [(x, "M0510-X-FOUNDATION") for x in ["M0510-ROOT", "M0510-N-EULER-PRODUCT", "M0510-L-MODULAR", "M0510-T-ASYMPTOTIC"]])),
    "documentation": graph(edges("D", "documents", [("M0510-X-SOURCE", "M0510-ROOT"), ("M0510-X-PROVENANCE", "M0510-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0510-ROOT", "M0510-X-SOURCE"), ("M0510-ROOT", "M0510-X-FOUNDATION"), ("M0510-ROOT", "M0510-X-PROVENANCE")])),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0510-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0510-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False,
        "first_open_cut": ["M0510-N-EULER-PRODUCT", "M0510-N-COEFFICIENT", "M0510-C-CONTOUR", "M0510-L-MODULAR", "M0510-L-MINOR-BOUND", "M0510-X-SOURCE", "M0510-X-FOUNDATION"]},
}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in {"M0510-S-ENCODING", "M0510-S-BOUNDARY", "M0510-T-ASYMPTOTIC"} else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
