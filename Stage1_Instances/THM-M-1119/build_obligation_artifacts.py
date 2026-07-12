#!/usr/bin/env python3
"""Deterministically build the THM-M-1119 typed graph and readable tree."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = json.loads((HERE / "obligation-registry.json").read_text())
IDS = REGISTRY["frozen_denominators"]["inventory"]

specs = {
    "M1119-ROOT": ("root", "The exact square-lattice bond critical probability equals one half.", "Stage1Instances.THM_M_1119.KestenTarget", "The canonical proposition.", "H2", "M4", 3),
    "M1119-S-DEFINITIONS": ("definition", "Freeze the square lattice, bond configurations, Bernoulli product measure, open graph, infinite-cluster event, and critical infimum.", "Statement.lean definitions used by KestenTarget", "The exact object interface.", "not_applicable", "M3", 8),
    "M1119-S-BOUNDARY": ("normalization", "Preserve p in [0,1], the infimum convention, rooted unbounded reachability, and the fact that endpoint nonpercolation is outside the root.", "Boundary package for KestenTarget", "No stronger endpoint or different percolation model enters the proof.", "not_applicable", "M4", 8),
    "M1119-S-FOUNDATION": ("certificate", "Audit classical noncomputable measure theory, choice, imports, axioms, and the no-oracle policy.", "Planned foundation and transitive trust certificate", "An accepted trust boundary for all terminal bodies.", "not_applicable", "M4", 8),
    "M1119-N-MONOTONE": ("normalization", "Construct the monotone coupling in p and reduce the infimum equality to exact lower and upper threshold bounds.", "Planned monotone-coupling and sInf reduction signature", "A threshold interface connecting finite events to criticalProbability.", "H2", "M4", 30),
    "M1119-C-RECTANGLES": ("construction", "Define finite rectangular crossings, pivotal bonds, and primal/dual circuits with measurable finite-coordinate events.", "Planned finite-box event construction signature", "Well-defined measurable finite events used by duality, RSW, and Russo.", "H2", "M4", 45),
    "M1119-L-DUALITY": ("core_lemma", "Prove the planar primal/dual crossing complement and the self-dual p = 1/2 probability identity.", "Planned exact planar-duality signature", "Critical crossing identities on finite rectangles.", "H2", "M4", 70),
    "M1119-L-RSW": ("core_lemma", "Derive uniform bounded-aspect-ratio crossing estimates from square crossings using gluing and symmetry.", "Planned exact RSW signature", "Scale-uniform crossing and dual-circuit bounds.", "H2", "M4", 95),
    "M1119-L-RUSSO": ("core_lemma", "Relate derivatives of increasing finite crossing events to sums of pivotal probabilities.", "Planned exact Russo-formula signature", "A finite-volume derivative identity with all measurability and finiteness premises.", "H2", "M4", 75),
    "M1119-L-SHARP": ("core_lemma", "Combine pivotal estimates and RSW to obtain the finite-size sharp-threshold bounds on both sides of one half.", "Planned exact sharp-threshold signature", "Quantitative decay/growth sufficient for infinite-volume limits.", "H2", "M4", 100),
    "M1119-T-SUBCRITICAL": ("terminal", "Show one half is at most the critical probability.", "Stage1Instances.THM_M_1119.SubcriticalThresholdBound", "(1/2 : NNReal) <= criticalProbability.", "H2", "M4", 35),
    "M1119-T-SUPERCRITICAL": ("terminal", "Show the critical probability is at most one half.", "Stage1Instances.THM_M_1119.SupercriticalThresholdBound", "criticalProbability <= (1/2 : NNReal).", "H2", "M4", 35),
    "M1119-T-COMPOSE": ("transport", "Combine the two exact threshold inequalities by antisymmetry.", "Stage1Instances.THM_M_1119.kestenTarget_of_threshold_bounds", "KestenTarget, conditionally on both open bounds.", "H2", "M0-L", 3),
    "M1119-X-SOURCE": ("terminal", "Map every material proof transition to Kesten's primary source and independently review assumptions and errata.", "Human-source crosswalk; no Lean proof target", "Pinpoint source fidelity for eligible nodes.", "H2", "not_applicable", 20),
    "M1119-X-PROVENANCE": ("certificate", "Classify every eventual wrapper, terminal body, dependency, axiom, placeholder, and trust boundary.", "Planned provenance and trust closure", "Content-addressed proof-body identities and trust reports.", "not_applicable", "M4", 20),
}

proof = [
    ("M1119-S-DEFINITIONS", "M1119-N-MONOTONE"), ("M1119-S-BOUNDARY", "M1119-N-MONOTONE"),
    ("M1119-C-RECTANGLES", "M1119-L-DUALITY"), ("M1119-C-RECTANGLES", "M1119-L-RSW"),
    ("M1119-C-RECTANGLES", "M1119-L-RUSSO"), ("M1119-L-DUALITY", "M1119-L-RSW"),
    ("M1119-L-RSW", "M1119-L-SHARP"), ("M1119-L-RUSSO", "M1119-L-SHARP"),
    ("M1119-N-MONOTONE", "M1119-T-SUBCRITICAL"), ("M1119-L-SHARP", "M1119-T-SUBCRITICAL"),
    ("M1119-N-MONOTONE", "M1119-T-SUPERCRITICAL"), ("M1119-L-SHARP", "M1119-T-SUPERCRITICAL"),
    ("M1119-T-SUBCRITICAL", "M1119-T-COMPOSE"), ("M1119-T-SUPERCRITICAL", "M1119-T-COMPOSE"),
    ("M1119-T-COMPOSE", "M1119-ROOT"),
]

def edge(kind, source, target, affects):
    return {"edge_type": kind, "source": source, "target": target, "affects_machine_closure": affects}

nodes = []
for oid in IDS:
    kind, claim, formal, output, h, m, budget = specs[oid]
    nodes.append({
        "node_id": f"THM-M-1119-{oid.removeprefix('M1119-')}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": formal, "output": output,
        "human_debt": h, "machine_debt": m, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if h == "not_applicable" else "pending-node-pinpoint-review",
        "provenance_id": "none", "foundation_profile": "lean4-classical-measure-theory/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; experiment and numerical evidence receive no proof credit",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only incoming proof_requires outputs and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed consumers may use this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1119/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING", "status_boundary": "Architecture or conditional interface only; no unregistered premise and no substantive root closure is supplied.",
        "task_ids": ["S56-M-1119-OBLIGATION_TREE", "S56-M-1119-PROOF"], "owned_sources": [],
        "owner": "THM-M-1119 proof lane", "reviewer": "independent Stage1 integration reviewer",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "open"}
    })

edges = [edge("proof_requires", a, b, True) for a, b in proof]
edges += [edge("composes", "M1119-T-SUBCRITICAL", "M1119-T-COMPOSE", True), edge("composes", "M1119-T-SUPERCRITICAL", "M1119-T-COMPOSE", True), edge("composes", "M1119-T-COMPOSE", "M1119-ROOT", True)]
edges += [edge("source_map", "M1119-X-SOURCE", oid, False) for oid in REGISTRY["frozen_denominators"]["required_human_source"] if oid != "M1119-X-SOURCE"]
edges += [edge("provenance_of", "M1119-X-PROVENANCE", oid, False) for oid in REGISTRY["frozen_denominators"]["required_machine"]]
edges += [edge("trusts", "M1119-S-FOUNDATION", oid, False) for oid in REGISTRY["frozen_denominators"]["required_machine"] if oid != "M1119-S-FOUNDATION"]
workflow = [edge("workflow_depends_on", "S56-M-1119-ANCHOR_AUDIT", "S56-M-1119-OBLIGATION_TREE", False), edge("workflow_depends_on", "S56-M-1119-OBLIGATION_TREE", "S56-M-1119-PROOF", False), edge("workflow_depends_on", "S56-M-1119-PROOF", "S56-M-1119-VALIDATION", False), edge("workflow_depends_on", "S56-M-1119-VALIDATION", "S56-M-1119-RELEASE", False)]

denominator = hashlib.sha256("\n".join(IDS).encode()).hexdigest()
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1119-OBLIGATION_TREE", "theorem_id": "THM-M-1119", "registry_id": "THM-M-1119/registry-v1", "registry_denominator_sha256": denominator, "root_node_id": "M1119-ROOT", "edge_direction": "prerequisite or support source -> consumer", "nodes": nodes, "graphs": {"proof": [e for e in edges if e["edge_type"] in {"proof_requires", "composes"}], "provenance": [e for e in edges if e["edge_type"] == "provenance_of"], "trust": [e for e in edges if e["edge_type"] == "trusts"], "documentation": [e for e in edges if e["edge_type"] == "source_map"], "workflow": workflow}, "status_boundary": "Typed architecture only; only the conditional two-bound composition elaborates, and all mathematical proof leaves remain open."}
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

lines = ["# THM-M-1119 frozen obligation tree", "", "The exact root is `KestenTarget`. This is a reader map of open obligations, not a proof. The checked composition consumes both threshold inequalities, but neither inequality has a proof body.", ""]
for node in nodes:
    oid = node["obligation_id"]
    lines += [f"## {oid}", "", f"**Claim:** {node['human_statement']}", f"**Role:** Supplies `{node['output']}` along the declared typed edges.", "**Inputs:** Only the frozen formal context and incoming `proof_requires` nodes.", f"**Proof route:** Open; implement the exact planned signature within the {node['step_budget']}-step leaf budget, splitting first if the substantive ledger would exceed 100 steps.", "**Branch logic:** No hidden branch may be introduced; any case split requires a registry revision or explicit child nodes.", f"**Formal map:** `{node['formal_target']}`.", f"**Trust boundary:** {node['tcb_profile']}; {node['computation_record']}.", f"**Step ledger:** premise: incoming typed outputs; inference: {node['human_statement']}; output: {node['output']}; outgoing use: declared graph edges only.", f"**Boundary:** {node['status_boundary']}", f"**Status vector:** `[{node['human_debt']}, {node['machine_debt']}, {node['readability_debt']}]`; no accepted evidence receipt.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
