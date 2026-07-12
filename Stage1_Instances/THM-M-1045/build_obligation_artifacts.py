#!/usr/bin/env python3
"""Build the deterministic THM-M-1045 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

rows = [
    ("M1045-ROOT", "root", "Exact CameronMartinTarget for every WienerData and direction", "Stage1Instances.THM_M_1045.CameronMartinTarget", "critical", "M3"),
    ("M1045-S-DEFINITIONS", "definition", "Freeze paths, measures, translation, directions, energy and density", "Statement.lean definitions", "high", "M0-L"),
    ("M1045-S-BOUNDARY", "branch", "Include zero direction and full nonnegative-time boundary", "zero_isCameronMartinDirection", "normal", "M0-L"),
    ("M1045-S-FOUNDATION", "definition", "Audit classical measure, integration and RN foundations", "planned transitive axiom report", "high", "M3"),
    ("M1045-N-TRANSLATION", "normalization", "Fix x+h push-forward and positive pairing sign", "translatedMeasure; density", "high", "M3"),
    ("M1045-B-EQUIVALENCE", "branch", "Prove equivalence exactly for Cameron-Martin directions", "EquivalenceBranch", "critical", "M4"),
    ("M1045-B-DENSITY", "branch", "Identify the RN derivative with the exponential density", "DensityBranch", "critical", "M4"),
    ("M1045-B-SINGULARITY", "branch", "Prove singularity for every non-Cameron-Martin direction", "SingularityBranch", "critical", "M4"),
    ("M1045-L-CYLINDER-SHIFT", "core_lemma", "Establish compatible finite-dimensional translated cylinder laws", "planned cylinder-shift signature", "high", "M4"),
    ("M1045-L-PALEY-WIENER", "construction", "Construct and characterize the Paley-Wiener pairing needed by the density", "planned pairing-law signature", "critical", "M4"),
    ("M1045-L-EXTENSION", "bridge", "Extend cylinder identities to the path sigma-algebra and identify RN density", "planned monotone-class/RN signature", "critical", "M4"),
    ("M1045-L-SEPARATION", "core_lemma", "Separate a non-admissible direction to obtain singularity", "planned Gaussian separation signature", "critical", "M4"),
    ("M1045-T-ASSEMBLE", "terminal", "Compose the three exact branch packages into the root", "root_of_branch_packages", "high", "M0-L"),
    ("M1045-X-SOURCE", "terminal", "Map mathematical leaves to pinpoint primary sources", "source_statement_crosswalk.md", "high", "M3"),
    ("M1045-X-PROVENANCE", "terminal", "Audit terminal bodies, imports and trust closure", "planned provenance record", "critical", "M3"),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
ids = [r[0] for r in rows]

def fingerprint(oid, target):
    return "sha256:" + hashlib.sha256((statement_hash + "\0" + oid + "\0" + target).encode()).hexdigest()

obligations = []
nodes = []
for oid, kind, human, target, risk, machine in rows:
    informational = oid == "M1045-X-PROVENANCE"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
        "root_relevant": not informational, "machine_eligibility": "informational" if informational else "required",
        "human_source_eligibility": "required" if oid not in {"M1045-S-BOUNDARY", "M1045-X-PROVENANCE"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "informational provenance overlay; release-gating but not a proof premise" if informational else None,
        "terminal_proof_body_id": "Stage1Instances.THM_M_1045.root_of_branch_packages" if oid == "M1045-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": oid + "-N", "obligation_id": oid, "kind": kind, "human_statement": human,
        "formal_target": target, "output": human, "human_debt": "H1", "machine_debt": machine,
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "M1045-SOURCE-OPEN" if oid != "M1045-S-BOUNDARY" else "not-applicable",
        "provenance_id": "M1045-PROV-OPEN", "foundation_profile": "lean4-classical-measure-v1",
        "tcb_profile": "lean4-4.29.0-mathlib-8a178386", "computation_record": "none",
        "step_budget": 12 if risk == "critical" else 8,
        "semantic_step_ledger": {"premises": [], "inference": "Open semantic package; no closure inferred", "output": human, "outgoing_use": "typed graph edges"},
        "public_readable_target": "Stage1_Instances/THM-M-1045/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "M1045-V-STRUCTURE", "status_boundary": "Architecture only; machine debt is unchanged unless named kernel evidence exists.",
        "task_ids": ["S56-M-1045-OBLIGATION_TREE"], "owned_sources": ["Stage1_Instances/THM-M-1045"],
        "owner": "Stage1 rev-5.6 execution lane", "reviewer": "independent integration-lane reviewer",
        "validity": {"validated_at": "2026-07-12", "review_due": "on any invalidation input", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "rev-5.6 schema"], "revocation_state": "active"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1045-OBLIGATION_TREE", "theorem_id": "THM-M-1045",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Frozen exact statement, bounded anchor audit, and classical cylinder/extension/separation architecture; eligibility chosen independently of closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1045-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1045-X-PROVENANCE"]},
    "delta_policy": "Any target correction, split, merge or eligibility change creates registry version 2 with an append-only semantic delta.",
    "obligations": obligations, "root_vector": {"human": "H1", "machine": "M3", "readability": "R3"},
    "theorem_complete": False,
}

proof_pairs = [
    ("M1045-ROOT", "M1045-T-ASSEMBLE"),
    ("M1045-T-ASSEMBLE", "M1045-B-EQUIVALENCE"), ("M1045-T-ASSEMBLE", "M1045-B-DENSITY"), ("M1045-T-ASSEMBLE", "M1045-B-SINGULARITY"),
    ("M1045-B-EQUIVALENCE", "M1045-L-CYLINDER-SHIFT"), ("M1045-B-EQUIVALENCE", "M1045-L-EXTENSION"),
    ("M1045-B-DENSITY", "M1045-L-PALEY-WIENER"), ("M1045-B-DENSITY", "M1045-L-EXTENSION"),
    ("M1045-B-SINGULARITY", "M1045-L-SEPARATION"),
]

def graph(edges):
    out, inc = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"]); inc.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inc}

proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "from": a, "type": typ, "to": b} for i, (a,b) in enumerate(pairs,1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M1045-ROOT", "M1045-S-DEFINITIONS"), ("M1045-ROOT", "M1045-S-BOUNDARY"), ("M1045-ROOT", "M1045-N-TRANSLATION")])),
    "provenance": graph(edges("PR", "provenance_of", [("M1045-X-PROVENANCE", "M1045-T-ASSEMBLE")])),
    "evidence": graph([]),
    "trust": graph(edges("TR", "trusts", [("M1045-ROOT", "M1045-S-FOUNDATION"), ("M1045-ROOT", "M1045-X-PROVENANCE")])),
    "documentation": graph(edges("D", "documents", [("M1045-X-SOURCE", "M1045-ROOT"), ("M1045-S-DEFINITIONS", "M1045-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M1045-T-ASSEMBLE", "M1045-B-EQUIVALENCE"), ("M1045-T-ASSEMBLE", "M1045-B-DENSITY"), ("M1045-T-ASSEMBLE", "M1045-B-SINGULARITY"), ("M1045-X-PROVENANCE", "M1045-T-ASSEMBLE")])),
}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"], "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
          "closure_boundary": {"closed_obligations": ["M1045-S-DEFINITIONS", "M1045-S-BOUNDARY", "M1045-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1045-B-EQUIVALENCE", "M1045-B-DENSITY", "M1045-B-SINGULARITY"], "composition_certificates": ["Stage1Instances.THM_M_1045.root_of_branch_packages"], "reason": "Composition is conditional and all three mathematical branches lack proof bodies."}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"], "recipes": [{"recipe_id": "M1045-V-STRUCTURE", "covers": ids, "command": "python3 Stage1_Instances/THM-M-1045/check_obligation_tree.py", "expected_exit": 0}, {"recipe_id": "M1045-V-LEAN-COMPOSITION", "covers": ["M1045-T-ASSEMBLE"], "command": "elaborate Statement.lean then ObligationTree.lean with pinned lake env", "expected_exit": 0}]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
print(denominator)
