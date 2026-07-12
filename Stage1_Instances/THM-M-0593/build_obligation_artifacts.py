#!/usr/bin/env python3
"""Build the frozen THM-M-0593 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0593-OBLIGATION_TREE"
THEOREM = "THM-M-0593"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def planned(text: str) -> str:
    return "planned:v1:sha256:" + sha(text.encode())


rows = [
    # id, kind, risk, H-source, statement, output, step budget
    ("M0593-ROOT", "root", "critical", True, "The exact SardTarget proposition.", "Codomain volume-nullity of all critical values.", 20),
    ("M0593-S-DEFINITIONS", "definition", "high", False, "Freeze criticalPointsOn, fderiv nonsurjectivity, image, and Euclidean volume.", "The canonical predicates with no representation drift.", 30),
    ("M0593-S-DOMAINS", "normalization", "high", False, "Freeze natural dimensions, total maps, open regions, and smoothness only on the region.", "The exact binder and typeclass context.", 30),
    ("M0593-S-BOUNDARY", "branch", "high", True, "Account for empty regions and zero-dimensional domain or codomain.", "All degenerate cases are assigned to an exhaustive branch.", 50),
    ("M0593-S-FOUNDATION", "certificate", "critical", False, "Audit classical choice, quotients, measure completion, and terminal axiom closure.", "An accepted foundation and TCB report.", 100),
    ("M0593-N-LOCAL", "reduction", "critical", True, "Reduce an arbitrary open region to a countable family of bounded local cubes whose interiors cover it.", "A countable local-to-global nullity reduction.", 80),
    ("M0593-B-ZERO", "branch", "normal", True, "If n = 0, show every derivative is surjective and the critical locus is empty.", "The zero-codomain Sard branch.", 30),
    ("M0593-B-LOWDIM", "branch", "critical", True, "If m < n, prove the whole smooth image, hence the critical-value image, has n-volume zero.", "The dimension-increasing Sard branch.", 80),
    ("M0593-B-HARD", "branch", "critical", True, "If 0 < n and n <= m, prove nullity of the critical values by the Morse-Sard local argument.", "The positive-codomain hard branch.", 100),
    ("M0593-B-MERGE", "terminal", "high", True, "Prove n = 0 or m < n or (0 < n and n <= m), then merge the three exact branches.", "The complete canonical target from exhaustive branches.", 25),
    ("M0593-L-DIMENSION-IMAGE", "bridge", "critical", True, "Establish n-volume nullity of a C1 image from an m-dimensional domain when m < n, locally without a convexity gap.", "The analytic engine for M0593-B-LOWDIM.", 100),
    ("M0593-C-RANK-STRATA", "construction", "critical", True, "Partition the hard critical locus into rank/derivative-vanishing strata suited to induction and Taylor estimates.", "A countable measurable cover of every hard critical point.", 80),
    ("M0593-L-RANK-REDUCTION", "core_lemma", "critical", True, "Near a point with a nonzero derivative minor, straighten selected coordinates and reduce the remaining critical-value claim by slicing and induction.", "Nullity for all non-flat rank strata.", 100),
    ("M0593-L-HIGHER-STRATA", "core_lemma", "critical", True, "Separate points where successive derivatives vanish and identify the finite Taylor order needed for each residual stratum.", "An exhaustive finite-order flatness decomposition.", 80),
    ("M0593-L-TAYLOR", "core_lemma", "critical", True, "Bound image diameters on sufficiently small cubes using Taylor remainder estimates at flat critical points.", "Quantitative image-size bounds for each flat stratum.", 100),
    ("M0593-L-CUBE-COVER", "core_lemma", "critical", True, "Cover each flat stratum by cubes and sum codomain-volume bounds with the correct dimension exponent.", "Arbitrarily small outer volume of every flat stratum image.", 100),
    ("M0593-L-NULL-LIMIT", "core_lemma", "high", True, "Pass from arbitrary outer-volume bounds and countable unions to volume zero.", "Nullity of all local hard-branch critical values.", 60),
    ("M0593-T-HARD-LOCAL", "terminal", "critical", True, "Compose rank reduction and flat-stratum estimates on one bounded local cube.", "The local hard-branch Sard lemma.", 70),
    ("M0593-T-LOCAL-GLOBAL", "terminal", "critical", True, "Map the countable local cube cover through f and use countable union nullity.", "The hard branch on the arbitrary open region R.", 60),
    ("M0593-X-EQUAL-DIM", "bridge", "high", False, "Audit the pinned determinant-zero equal-dimensional mathlib theorem and any checked transport into a local subcase.", "A provenance-bounded partial formal anchor only.", 50),
    ("M0593-X-SOURCE", "terminal", "high", True, "Pinpoint Sard 1942 Theorems 4.1 and 7.2 against every mathematical engine.", "A human-source crosswalk, without machine proof credit.", 100),
    ("M0593-X-PROVENANCE", "terminal", "critical", False, "Record terminal proof bodies, imports, revisions, axioms, and wrapper deduplication.", "A complete proof-body and trust provenance ledger.", 100),
]

statement_hash = sha((HERE / "Statement.lean").read_bytes())
anchor_hash = sha((HERE / "anchor-audit.md").read_bytes())
obligations = []
for oid, kind, risk, hsource, statement, output, budget in rows:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0593-ROOT", "M0593-S-DEFINITIONS"} else planned(statement),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if not oid.startswith("M0593-X-") else "informational",
        "human_source_eligibility": "required" if hsource else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "formal-anchor/source/provenance overlay; excluded from machine denominator" if oid.startswith("M0593-X-") else None,
        "terminal_proof_body_id": None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact Euclidean smooth SardTarget and bounded AA-0593-v1 audit; the classical dimension split and Morse-Sard rank/Taylor route were expanded before proof execution.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0593-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta; version 1 denominators remain reportable.",
    "obligations": obligations,
}

nodes = []
for oid, kind, risk, hsource, statement, output, budget in rows:
    checked = oid in {"M0593-S-DEFINITIONS", "M0593-B-MERGE"}
    nodes.append({
        "node_id": "THM-M-0593-" + oid.removeprefix("M0593-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": "Stage1Instances.THMM0593.SardTarget" if oid == "M0593-ROOT" else ("checked in ObligationTree.lean" if checked else "planned exact signature; must elaborate before proof credit"),
        "output": output,
        "human_debt": "H1" if hsource else "H2",
        "machine_debt": "M3" if checked else "M4",
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "SARD-1942-4.1/7.2-node-map-pending" if hsource else "not-applicable",
        "provenance_id": "AA-0593-v1" if oid.startswith("M0593-X-") else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical computation or oracle may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the frozen formal context.", "inference": statement, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0593/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no unlisted premise and no proof of SardTarget is supplied.",
        "task_ids": [ITEM, "S56-M-0593-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0593/ObligationTree.lean"] if checked else [],
        "owner": "THM-M-0593 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.md", "registry", "toolchain"], "revocation_state": "provisional" if checked else "open"},
    })

proof_pairs = [
    ("M0593-ROOT", "M0593-B-MERGE"),
    ("M0593-B-MERGE", "M0593-B-ZERO"), ("M0593-B-MERGE", "M0593-B-LOWDIM"), ("M0593-B-MERGE", "M0593-B-HARD"),
    ("M0593-B-LOWDIM", "M0593-L-DIMENSION-IMAGE"),
    ("M0593-B-HARD", "M0593-T-LOCAL-GLOBAL"),
    ("M0593-T-LOCAL-GLOBAL", "M0593-N-LOCAL"), ("M0593-T-LOCAL-GLOBAL", "M0593-T-HARD-LOCAL"),
    ("M0593-T-HARD-LOCAL", "M0593-C-RANK-STRATA"), ("M0593-T-HARD-LOCAL", "M0593-L-RANK-REDUCTION"), ("M0593-T-HARD-LOCAL", "M0593-L-NULL-LIMIT"),
    ("M0593-C-RANK-STRATA", "M0593-L-HIGHER-STRATA"),
    ("M0593-L-NULL-LIMIT", "M0593-L-CUBE-COVER"),
    ("M0593-L-CUBE-COVER", "M0593-L-TAYLOR"),
]


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


proof_edges = []
for parent, child in proof_pairs:
    req = f"REQ-{parent}-{child}"
    comp = f"CMP-{child}-{parent}"
    proof_edges += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

other = {
    "refinement": [
        edge("REF-ROOT-DEFS", "M0593-ROOT", "logical_decomposition", "M0593-S-DEFINITIONS"),
        edge("REF-ROOT-DOMAINS", "M0593-ROOT", "logical_decomposition", "M0593-S-DOMAINS"),
        edge("REF-ROOT-BOUNDARY", "M0593-ROOT", "logical_decomposition", "M0593-S-BOUNDARY"),
    ],
    "provenance": [
        edge("SRC-DIMENSION", "M0593-L-DIMENSION-IMAGE", "source_map", "M0593-X-SOURCE"),
        edge("SRC-HARD", "M0593-T-HARD-LOCAL", "source_map", "M0593-X-SOURCE"),
        edge("PROV-EQUAL-DIM", "M0593-X-EQUAL-DIM", "provenance_of", "M0593-L-RANK-REDUCTION"),
        edge("PROV-ROOT", "M0593-X-PROVENANCE", "provenance_of", "M0593-ROOT"),
    ],
    "evidence": [edge("EVID-ANCHOR", "M0593-X-PROVENANCE", "evidence_for", "M0593-X-EQUAL-DIM")],
    "trust": [edge("TRUST-FOUNDATION", "M0593-ROOT", "trusts", "M0593-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0593-ROOT", "trusts", "M0593-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0593-S-DEFINITIONS", "documents", "M0593-ROOT"), edge("DOC-SOURCE", "M0593-X-SOURCE", "documents", "M0593-T-HARD-LOCAL")],
    "workflow": [edge("FLOW-MERGE-BRANCHES", "M0593-B-MERGE", "workflow_depends_on", "M0593-B-HARD"), edge("FLOW-HARD-LOCAL", "M0593-T-LOCAL-GLOBAL", "workflow_depends_on", "M0593-T-HARD-LOCAL"), edge("FLOW-PROVENANCE", "M0593-X-PROVENANCE", "workflow_depends_on", "M0593-B-MERGE")],
}


def graph(edges):
    outgoing = {oid: [] for oid in ids}
    incoming = {oid: [] for oid in ids}
    for e in edges:
        outgoing[e["from"]].append(e["edge_id"])
        incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


graphs = {"proof": graph(proof_edges)}
graphs.update({name: graph(edges) for name, edges in other.items()})
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0593/v1", "registry_denominator_sha256": denominator,
    "root_node_id": "THM-M-0593-ROOT", "edge_direction": "proof_requires points parent-to-required-child; composes is its reciprocal",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0593-S-DEFINITIONS"], "root_closed": False, "root_machine_debt": "M4", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0593-L-DIMENSION-IMAGE", "M0593-L-RANK-REDUCTION", "M0593-L-TAYLOR"], "composition_certificates": ["Stage1Instances.THMM0593.root_of_sard_branches"], "reason": "The branch merger is conditional; no audited candidate closes either analytic engine or the exact root."},
}

recipes = []
for oid in ids:
    recipes.append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0593/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0593 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THMM0593.root_of_sard_branches"] if oid == "M0593-B-MERGE" else []})
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / filename).write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
print(f"built {len(ids)} obligations; denominator sha256: {denominator}")
