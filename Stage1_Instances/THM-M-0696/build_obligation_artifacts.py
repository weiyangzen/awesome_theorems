#!/usr/bin/env python3
"""Build the deterministic THM-M-0696 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0696-OBLIGATION_TREE"
THEOREM = "THM-M-0696"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def planned(text: str) -> str:
    return "planned:v1:sha256:" + sha(text.encode())


# id, kind, claim, formal target, risk, machine eligibility, source eligibility, M debt, budget
SPECS = [
    ("M0696-ROOT", "root", "The frozen arbitrary-context classical propositional completeness theorem.", "Stage1Instances.THM_M_0696.PropositionalCompletenessTarget", "critical", "required", "required", "M3", 20),
    ("M0696-S-ENCODING", "definition", "The false/implication syntax, Boolean semantics, Set contexts, and K/S/DNE/MP derivability have the frozen meanings.", "Stage1Instances.THM_M_0696.{Formula,Satisfies,SemanticallyEntails,Derives}", "critical", "required", "required", "M3", 35),
    ("M0696-S-BOUNDARY", "branch", "Empty, inconsistent, infinite-context, and empty-atom boundary behavior agrees with the canonical statement.", "Stage1Instances.THM_M_0696.{empty_context_atom_boundary,falsum_context_boundary,assumption_boundary}", "high", "required", "required", "M3", 30),
    ("M0696-S-FOUNDATION", "certificate", "All classical choice, propositional extensionality, and kernel axioms used by the eventual proof are explicitly inventoried and accepted.", "planned axiom and foundation closure report", "critical", "required", "not_applicable", "M4", 25),
    ("M0696-N-SEED", "reduction", "If Gamma does not derive phi, adjoining not-phi produces a consistent seed theory.", "Stage1Instances.THM_M_0696.SeedConsistencyTarget", "critical", "required", "required", "M4", 70),
    ("M0696-L-DEDUCTION", "core_lemma", "Derivability from Gamma with phi adjoined is equivalent to deriving phi implies psi from Gamma.", "Stage1Instances.THM_M_0696.DeductionTheoremTarget", "critical", "required", "required", "M4", 100),
    ("M0696-C-MAXIMAL", "construction", "A consistent seed extends to a deductively closed, syntactically complete consistent theory without countability assumptions.", "Stage1Instances.THM_M_0696.LindenbaumTarget", "critical", "required", "required", "M4", 100),
    ("M0696-L-CHAIN", "core_lemma", "The union of a chain of consistent theory extensions is consistent, using finitary derivation support.", "planned exact chain-union consistency signature", "critical", "required", "required", "M4", 90),
    ("M0696-C-VALUATION", "construction", "The maximal theory determines the canonical Boolean valuation on atoms.", "Stage1Instances.THM_M_0696.canonicalValuation", "high", "required", "required", "M3", 35),
    ("M0696-B-TRUTH", "branch", "Formula induction proves the truth lemma in the atom, falsum, and implication cases.", "Stage1Instances.THM_M_0696.TruthLemmaTarget", "critical", "required", "required", "M4", 100),
    ("M0696-L-IMP", "core_lemma", "Maximal-consistent membership for implication matches Boolean implication of membership of its operands.", "planned exact implication-membership signature", "critical", "required", "required", "M4", 90),
    ("M0696-T-COUNTERMODEL", "terminal", "Every failure of derivability has a Boolean valuation satisfying Gamma and falsifying phi.", "Stage1Instances.THM_M_0696.CountermodelTarget", "critical", "required", "required", "M4", 80),
    ("M0696-T-ASSEMBLE", "transport", "The exact countermodel conclusion yields the canonical semantic-consequence completeness target.", "Stage1Instances.THM_M_0696.completeness_of_countermodel", "critical", "required", "required", "M3", 20),
    ("M0696-X-SOURCE", "bridge", "Primary human sources are mapped node by node to the chosen Hilbert and maximal-consistency route.", "not-applicable: human-source boundary", "critical", "not_applicable", "required", "M4", 45),
    ("M0696-X-EXTERNAL", "bridge", "The Foundation tautology endpoint is recorded only as a mismatched provenance boundary, with no proof credit.", "LO.Propositional.Hilbert.Cl.provable_of_tautology (external, not imported)", "high", "informational", "not_applicable", "M3", 30),
    ("M0696-X-PROVENANCE", "certificate", "Terminal body origins, dependency closures, placeholder scans, and trust reports are classified before machine credit.", "planned provenance and trust receipt bundle", "critical", "informational", "not_applicable", "M4", 35),
    ("M0696-X-COMPUTATION", "certificate", "No computation, reflection, solver, or oracle is required by this architecture; any later introduction reopens the registry.", "not-applicable pending independent reviewer acceptance", "normal", "not_applicable", "not_applicable", "M4", 15),
]

statement_hash = sha((HERE / "Statement.lean").read_bytes())
anchor_hash = sha((HERE / "anchor-audit.json").read_bytes())
rows = []
for oid, kind, claim, formal, risk, machine, source, _, _ in SPECS:
    rows.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-expression-sha256:2bb204606e13f5d322f577f7537b370a834d8079d500ce6a3e0e65670cd2e14f" if oid == "M0696-ROOT" else planned(claim + "\n" + formal)),
        "kind": kind,
        "root_relevant": oid not in {"M0696-X-EXTERNAL", "M0696-X-COMPUTATION"},
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"M0696-X-SOURCE": "human_source_boundary_only", "M0696-X-EXTERNAL": "mismatched_external_anchor_no_proof_credit", "M0696-X-PROVENANCE": "release_overlay_no_proof_credit", "M0696-X-COMPUTATION": "architecture_has_no_computation_pending_reviewer"}.get(oid)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0696/ObligationTree.lean#completeness_of_countermodel" if oid == "M0696-T-ASSEMBLE" else None),
    })

ids = [r["obligation_id"] for r in rows]
denominator = sha(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and completed anchor inventory; maximal-consistent countermodel architecture selected without crediting closure.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0696-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for oid, kind, claim, formal, _, _, source, mdebt, budget in SPECS:
    nodes.append({
        "node_id": "THM-M-0696-" + oid.removeprefix("M0696-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": formal,
        "output": claim,
        "human_debt": "H1" if source == "required" else "H1",
        "machine_debt": mdebt,
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit:M0696-C02" if oid == "M0696-X-EXTERNAL" else ("source-node-map-pending" if source == "required" else "not-applicable"),
        "provenance_id": "anchor-audit:M0696-C02" if oid == "M0696-X-EXTERNAL" else "none",
        "foundation_profile": "lean4-object-classical-v1; meta-level choice/extensionality audit open",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure open",
        "computation_record": "none; computation is not credited by this architecture",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Exact typed proof children listed in the proof graph.", "inference": claim, "output": claim, "outgoing_use": "Only the listed typed edges may consume or describe this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0696/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen obligation only; open children, source review, and kernel evidence remain uncredited.",
        "task_ids": [ITEM, "S56-M-0696-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0696/ObligationTree.lean"] if formal.startswith("Stage1Instances") else [],
        "owner": "THM-M-0696 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if mdebt == "M3" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if mdebt == "M3" else "open"},
    })

graphs = {name: {"edges": [], "out": {x: [] for x in ids}, "in": {x: [] for x in ids}} for name in ("proof", "refinement", "provenance", "trust", "documentation", "workflow")}

def edge(graph, eid, typ, src, dst, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal:
        e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e)
    graphs[graph]["out"][src].append(eid)
    graphs[graph]["in"][dst].append(eid)

requirements = [
    ("M0696-ROOT", "M0696-T-ASSEMBLE"),
    ("M0696-T-ASSEMBLE", "M0696-T-COUNTERMODEL"),
    ("M0696-T-COUNTERMODEL", "M0696-N-SEED"),
    ("M0696-T-COUNTERMODEL", "M0696-C-MAXIMAL"),
    ("M0696-T-COUNTERMODEL", "M0696-B-TRUTH"),
    ("M0696-N-SEED", "M0696-L-DEDUCTION"),
    ("M0696-C-MAXIMAL", "M0696-L-CHAIN"),
    ("M0696-B-TRUTH", "M0696-C-VALUATION"),
    ("M0696-B-TRUTH", "M0696-L-IMP"),
    ("M0696-B-TRUTH", "M0696-S-ENCODING"),
]
for i, (parent, child) in enumerate(requirements, 1):
    fwd, rev = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    edge("proof", fwd, "proof_requires", parent, child, rev)
    edge("proof", rev, "composes", child, parent, fwd)

for i, child in enumerate(("M0696-S-ENCODING", "M0696-S-BOUNDARY", "M0696-S-FOUNDATION", "M0696-N-SEED", "M0696-C-MAXIMAL", "M0696-B-TRUTH", "M0696-T-COUNTERMODEL"), 1):
    edge("refinement", f"R{i:02d}", "logical_decomposition", "M0696-ROOT", child)
edge("provenance", "V01", "source_map", "M0696-X-SOURCE", "M0696-ROOT")
edge("provenance", "V02", "provenance_of", "M0696-X-EXTERNAL", "M0696-T-COUNTERMODEL")
edge("provenance", "V03", "provenance_of", "M0696-X-PROVENANCE", "M0696-ROOT")
edge("trust", "T01", "trusts", "M0696-ROOT", "M0696-S-FOUNDATION")
edge("trust", "T02", "trusts", "M0696-ROOT", "M0696-X-PROVENANCE")
edge("trust", "T03", "trusts", "M0696-ROOT", "M0696-X-COMPUTATION")
for i, oid in enumerate(ids, 1):
    edge("documentation", f"D{i:02d}", "documents", "M0696-X-PROVENANCE", oid)
for i, (parent, child) in enumerate(requirements, 1):
    edge("workflow", f"W{i:02d}", "workflow_depends_on", parent, child)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0696-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "THM-M-0696-ROOT", "edge_direction": "proof_requires runs parent to child; composes is reciprocal child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "theorem_complete": False, "root_vector": ["H1", "M3", "R3"], "first_open_cut_set": ["M0696-T-COUNTERMODEL"], "checked_composition": "completeness_of_countermodel", "status": "interfaces_frozen_no_proof_credit"},
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0696/check_obligation_tree.py", "expected": "structural registry and graph acceptance; no closure inference"} for oid in ids]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(obj, indent=2) + "\n")
print(denominator)
