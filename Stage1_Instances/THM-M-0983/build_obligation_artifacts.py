#!/usr/bin/env python3
"""Build the frozen THM-M-0983 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()

def fingerprint(text):
    return hashlib.sha256(text.encode()).hexdigest()

raw = [
    ("M0983-ROOT", "root", "The exact frozen Bernoulli strong-law target", "Stage1Instances.THM_M_0983.BernoulliStrongLawTarget", "critical", "M3", 6, "M0983-T-ASSEMBLE"),
    ("M0983-S-DEFINITIONS", "definition", "The empirical frequency and exact target binders have the frozen meanings", "Stage1Instances.THM_M_0983.empiricalFrequency; BernoulliStrongLawTarget", "high", "M0-L", 5, None),
    ("M0983-S-BOUNDARY", "terminal", "The empty empirical average is zero and endpoint probabilities remain in scope", "Stage1Instances.THM_M_0983.empiricalFrequency_zero", "normal", "M0-L", 3, "statement-boundary-body"),
    ("M0983-S-FOUNDATION", "terminal", "The proof route stays within the declared Lean/mathlib foundation and trust policy", "planned foundation, axiom, and TCB inventory", "high", "M3", 7, None),
    ("M0983-R-PAIRWISE", "reduction", "Joint independence projects to the pairwise independence required by the strong law", "PairwiseProjectionPackage", "high", "M3", 4, "ProbabilityTheory.iIndepFun.indepFun"),
    ("M0983-B-STRONG-LAW", "bridge", "The pinned real IID strong law yields almost-sure convergence to the reference expectation", "StrongLawPackage", "critical", "M3", 8, "ProbabilityTheory.strong_law_ae_real"),
    ("M0983-T-EXPECTATION", "transport", "The equality mu[X 0] = p transports the limit from the expectation to p", "ExpectationTransportPackage", "high", "M3", 3, None),
    ("M0983-T-ASSEMBLE", "transport", "The pairwise, strong-law, and expectation packages compose into the exact root", "Stage1Instances.THM_M_0983_Obligations.root_of_packages", "critical", "M0-L", 5, "root-of-packages-body"),
    ("M0983-X-SOURCE", "terminal", "Every material premise and transition receives a pinpoint primary-source crosswalk", "planned source ledger", "high", "M4", 8, None),
    ("M0983-X-PROVENANCE", "terminal", "Wrapper, terminal body, imports, axioms, TCB, and replay boundaries are classified", "planned provenance and trust receipt bundle", "critical", "M3", 9, None),
]

obligations = []
nodes = []
for oid, kind, claim, formal, risk, machine, budget, body in raw:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(claim + "\n" + formal),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if not oid.startswith("M0983-X-") else "informational",
        "human_source_eligibility": "required" if oid not in {"M0983-S-FOUNDATION", "M0983-X-PROVENANCE"} else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None if not oid.startswith("M0983-X-") else "governance node; classified outside the logical proof denominator",
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": oid + "-N1", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": formal, "output": claim,
        "human_debt": "H3", "machine_debt": machine, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-accepted",
        "provenance_id": "anchor-audit:S56-M-0983-C01" if oid in {"M0983-B-STRONG-LAW", "M0983-X-PROVENANCE"} else "none",
        "foundation_profile": "lean4-mathlib-pinned/provisional", "tcb_profile": "rev56-tcb/open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": [], "inference": claim, "output": claim, "outgoing_use": "typed graph edges"},
        "public_readable_target": f"Stage1_Instances/THM-M-0983/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture status only; no downstream proof or acceptance receipt is claimed.",
        "task_ids": ["S56-M-0983-OBLIGATION_TREE"],
        "owned_sources": ["Stage1_Instances/THM-M-0983/ObligationTree.lean"] if oid == "M0983-T-ASSEMBLE" else [],
        "owner": "Stage1 rev-5.6 execution lane", "reviewer": "independent integration-lane reviewer required",
        "validity": {"validated_at": "2026-07-12", "review_due": "on any frozen-input change", "invalidation_inputs": ["statement", "anchor audit", "toolchain", "registry"], "revocation_state": "active"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0983-OBLIGATION_TREE", "theorem_id": "THM-M-0983",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded immutable anchor audit; eligibility assigned from the pairwise-projection, strong-law, expectation-transport architecture rather than observed proof closure.",
    "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M0983-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r[0] for r in raw],
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": [r[0] for r in raw],
    },
    "obligations": obligations,
    "change_policy": "Any semantic split, merge, exclusion, or eligibility change requires a new version and append-only delta.",
}

graphs = {name: {"edges": [], "out": {r[0]: [] for r in raw}, "in": {r[0]: [] for r in raw}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def edge(graph, eid, typ, src, dst, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e); graphs[graph]["out"][src].append(eid); graphs[graph]["in"][dst].append(eid)
def proof_pair(n, parent, child):
    edge("proof", f"P{n}A", "proof_requires", parent, child, f"P{n}B")
    edge("proof", f"P{n}B", "composes", child, parent, f"P{n}A")
proof_pair(1, "M0983-ROOT", "M0983-T-ASSEMBLE")
proof_pair(2, "M0983-T-ASSEMBLE", "M0983-R-PAIRWISE")
proof_pair(3, "M0983-T-ASSEMBLE", "M0983-B-STRONG-LAW")
proof_pair(4, "M0983-T-ASSEMBLE", "M0983-T-EXPECTATION")
for n, child in enumerate(("M0983-S-DEFINITIONS", "M0983-S-BOUNDARY", "M0983-S-FOUNDATION"), 1): edge("refinement", f"R{n}", "logical_decomposition", "M0983-ROOT", child)
edge("provenance", "PV1", "provenance_of", "M0983-X-PROVENANCE", "M0983-B-STRONG-LAW")
edge("provenance", "PV2", "source_map", "M0983-X-SOURCE", "M0983-ROOT")
edge("evidence", "E1", "evidence_for", "M0983-X-PROVENANCE", "M0983-T-ASSEMBLE")
edge("trust", "TR1", "trusts", "M0983-ROOT", "M0983-S-FOUNDATION")
for n, oid in enumerate((r[0] for r in raw if not r[0].startswith("M0983-X-")), 1): edge("documentation", f"D{n}", "documents", "M0983-X-SOURCE", oid)
for n, oid in enumerate((r[0] for r in raw if r[0] != "M0983-ROOT"), 1): edge("workflow", f"W{n}", "workflow_depends_on", "M0983-ROOT", oid)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0983-OBLIGATION_TREE", "theorem_id": "THM-M-0983",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "minimal_open_root_cut": ["M0983-R-PAIRWISE", "M0983-B-STRONG-LAW", "M0983-T-EXPECTATION"], "theorem_complete": False, "accepted_receipts": []},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": "S56-M-0983-OBLIGATION_TREE", "theorem_id": "THM-M-0983", "recipes": [{"recipe_id": "VAL-" + r[0], "scope": r[0], "command": "python3 Stage1_Instances/THM-M-0983/check_obligation_tree.py", "expected_exit": 0} for r in raw]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
intake = json.loads((HERE / "intake.json").read_text())
assert intake["obligation_registry_hash"] == "sha256:" + denominator
print(denominator)
