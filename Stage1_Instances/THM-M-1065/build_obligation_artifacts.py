#!/usr/bin/env python3
"""Build the frozen THM-M-1065 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1065-OBLIGATION_TREE"
THEOREM = "THM-M-1065"
ROOT = "M1065-ROOT"

# These are semantic obligations, not claims that the corresponding lemmas exist.
SPECS = [
    (ROOT, "root", "Prove the exact normalized KMT strong-approximation target.",
     "Stage1Instances.THM_M_1065.KMTStrongApproximationTarget", "the exact canonical target", "critical", "H2"),
    ("M1065-S-LAW", "definition", "Preserve the probability, integrability, centering, variance-one, and two-sided exponential-moment assumptions.",
     "AdmissibleLaw mu", "the unchanged input-law package", "high", "H2"),
    ("M1065-S-EVENT", "definition", "Preserve the running maximum over every 1 <= k <= n and the strict C log n + x threshold.",
     "DiscrepancyEvent X Y C x n", "the exact measurable-event target", "high", "H2"),
    ("M1065-S-BOUNDARY", "normalization", "Handle n >= 1, x >= 0, positive constants, and ENNReal probability comparison without changing inequalities.",
     "KMT boundary and coercion package", "the exact boundary conventions", "high", "H2"),
    ("M1065-S-FOUNDATION", "certificate", "Audit classical choice, noncomputable measure constructions, measurability, and the transitive trust closure.",
     "foundation/trust certificate", "an admissible trust profile", "critical", "not_applicable"),
    ("M1065-C-SPACE", "construction", "Construct one probability space carrying both infinite sequences.",
     "exists Omega, MeasurableSpace Omega, P, X, Y", "a common-space coupling carrier", "critical", "H2"),
    ("M1065-L-X-LAWS", "core_lemma", "Prove every X increment has law mu on the constructed probability space.",
     "forall i, HasLaw (X i) mu P", "the prescribed marginal laws", "critical", "H2"),
    ("M1065-L-X-INDEP", "core_lemma", "Prove the X increments are mutually independent.",
     "ProbabilityTheory.iIndepFun X P", "iid independence for X", "critical", "H2"),
    ("M1065-L-Y-LAWS", "core_lemma", "Prove every Y increment has the standard real Gaussian law.",
     "forall i, HasLaw (Y i) (gaussianReal 0 1) P", "the Gaussian marginal laws", "critical", "H2"),
    ("M1065-L-Y-INDEP", "core_lemma", "Prove the Y increments are mutually independent.",
     "ProbabilityTheory.iIndepFun Y P", "iid independence for Y", "critical", "H2"),
    ("M1065-L-EVENT-MEAS", "core_lemma", "Establish measurability of every finite-horizon discrepancy event used by the measure bound.",
     "MeasurableSet (DiscrepancyEvent X Y C x n)", "well-formed probability events", "high", "H2"),
    ("M1065-C-CONSTANTS", "construction", "Construct law-dependent C, K, lambda that are strictly positive and uniform in n and x.",
     "exists C K lambda, 0 < C and 0 < K and 0 < lambda", "uniform positive constants", "critical", "H2"),
    ("M1065-L-BLOCK-COUPLING", "bridge", "Establish the quantitative finite-block coupling estimate from the exponential-moment law assumptions.",
     "finite-block KMT coupling interface", "the quantitative coupling input", "critical", "H2"),
    ("M1065-L-MAXIMAL-TAIL", "core_lemma", "Upgrade the coupling estimate to the maximum of all partial-sum discrepancies through n.",
     "P (DiscrepancyEvent X Y C x n) <= ofReal (K * exp (-lambda*x))", "the uniform exponential maximal tail", "critical", "H2"),
    ("M1065-T-WITNESS", "terminal", "Assemble the probability-space, law, independence, constant, and tail fields into one exact witness package.",
     "CouplingData mu with TailGuarantee", "an exact root witness for each admissible mu", "critical", "H2"),
    ("M1065-T-COMPOSE", "terminal", "Eliminate the witness package into the ordered existential and conjunction shape of the canonical target.",
     "kmtTarget_of_couplingData", "KMTStrongApproximationTarget", "critical", "H2"),
    ("M1065-X-SOURCE", "source", "Pinpoint primary theorem, assumptions, constants, and errata for every human-required node.",
     "node source crosswalk", "human provenance only", "critical", "H2"),
    ("M1065-X-PROVENANCE", "provenance", "Record terminal proof bodies, imports, axioms, and duplicate-body identities.",
     "proof provenance ledger", "machine provenance only", "critical", "not_applicable"),
]

ids = [row[0] for row in SPECS]
overlays = ["M1065-X-SOURCE", "M1065-X-PROVENANCE"]
machine = [oid for oid in ids if oid not in overlays]
human = [oid for oid, _, _, _, _, _, debt in SPECS if debt == "H2"]
denominators = {
    "inventory": ids,
    "required_machine": machine,
    "required_human_source": human,
    "required_readable": ids,
    "informational_overlays": overlays,
}

def planned_fingerprint(oid, formal):
    if oid == ROOT:
        return "lean-expression-sha256:b257ceb188a0b84aab11fd389b5df322129c283dbc38f5c226900a4fec5cebd0"
    payload = f"{THEOREM}/registry-v1/{oid}/{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(payload).hexdigest()

obligations = []
nodes = []
for oid, kind, human_statement, formal, output, risk, human_debt in SPECS:
    required = oid in machine
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": planned_fingerprint(oid, formal),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if required else "informational",
        "human_source_eligibility": "required" if oid in human else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None if required else "overlay-no-proof-credit",
        "terminal_proof_body_id": None,
    })
    ledger = [
        "Consume only the registered incoming premises at their frozen interfaces.",
        f"Establish: {human_statement}",
        f"Produce: {output}.",
        "Pass the result through the registered typed edge without weakening the target.",
    ]
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": human_statement, "formal_target": formal, "output": output,
        "human_debt": human_debt, "machine_debt": "M3" if kind == "definition" else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "open-node-pinpoint-review" if oid in human else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": len(ledger), "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1065/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture only; no accepted proof body or closure evidence is attached.",
        "task_ids": [ITEM, "S56-M-1065-PROOF"], "owned_sources": [],
        "owner": "THM-M-1065 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1,
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; architecture frozen without observing proof closure.",
    "root_obligation_id": ROOT, "frozen_denominators": denominators,
    "eligibility_policy": "Every semantic node on the selected common-space coupling route is required regardless of current library availability; overlays earn no proof credit.",
    "exclusions": [
        "An asymptotic invariance principle, terminal-time estimate, or empirical-process KMT theorem is not the root.",
        "A Brownian-motion formulation requires a checked integer-increment bridge and is not silently substituted.",
        "Aliases, wrappers, source rows, and presentation splits do not add semantic or terminal-body credit."
    ],
    "obligations": obligations,
}

proof_pairs = [
    ("M1065-S-LAW", "M1065-L-BLOCK-COUPLING", "proof_requires"),
    ("M1065-S-EVENT", "M1065-L-EVENT-MEAS", "proof_requires"),
    ("M1065-S-BOUNDARY", "M1065-L-MAXIMAL-TAIL", "proof_requires"),
    ("M1065-S-FOUNDATION", "M1065-T-WITNESS", "proof_requires"),
    ("M1065-C-SPACE", "M1065-L-X-LAWS", "proof_requires"),
    ("M1065-C-SPACE", "M1065-L-X-INDEP", "proof_requires"),
    ("M1065-C-SPACE", "M1065-L-Y-LAWS", "proof_requires"),
    ("M1065-C-SPACE", "M1065-L-Y-INDEP", "proof_requires"),
    ("M1065-C-SPACE", "M1065-L-EVENT-MEAS", "proof_requires"),
    ("M1065-C-SPACE", "M1065-L-BLOCK-COUPLING", "proof_requires"),
    ("M1065-C-CONSTANTS", "M1065-L-BLOCK-COUPLING", "proof_requires"),
    ("M1065-L-BLOCK-COUPLING", "M1065-L-MAXIMAL-TAIL", "proof_requires"),
    ("M1065-L-EVENT-MEAS", "M1065-L-MAXIMAL-TAIL", "proof_requires"),
    ("M1065-L-X-LAWS", "M1065-T-WITNESS", "composes"),
    ("M1065-L-X-INDEP", "M1065-T-WITNESS", "composes"),
    ("M1065-L-Y-LAWS", "M1065-T-WITNESS", "composes"),
    ("M1065-L-Y-INDEP", "M1065-T-WITNESS", "composes"),
    ("M1065-C-CONSTANTS", "M1065-T-WITNESS", "composes"),
    ("M1065-L-MAXIMAL-TAIL", "M1065-T-WITNESS", "composes"),
    ("M1065-T-WITNESS", "M1065-T-COMPOSE", "composes"),
    ("M1065-T-COMPOSE", ROOT, "composes"),
]
refinement_pairs = [
    (ROOT, "M1065-T-COMPOSE", "logical_decomposition"),
    ("M1065-T-WITNESS", "M1065-L-X-LAWS", "logical_decomposition"),
    ("M1065-T-WITNESS", "M1065-L-X-INDEP", "logical_decomposition"),
    ("M1065-T-WITNESS", "M1065-L-Y-LAWS", "logical_decomposition"),
    ("M1065-T-WITNESS", "M1065-L-Y-INDEP", "logical_decomposition"),
    ("M1065-T-WITNESS", "M1065-L-MAXIMAL-TAIL", "logical_decomposition"),
]

def graph(name, pairs):
    edges, outgoing, incoming = [], {}, {}
    for number, (src, dst, edge_type) in enumerate(pairs, 1):
        edge_id = f"{name.upper()}-{number:03d}"
        edges.append({"edge_id": edge_id, "from": src, "to": dst, "type": edge_type})
        outgoing.setdefault(src, []).append(edge_id)
        incoming.setdefault(dst, []).append(edge_id)
    return {"edges": edges, "out": outgoing, "in": incoming}

graphs = {
    "proof": graph("proof", proof_pairs),
    "refinement": graph("refinement", refinement_pairs),
    "provenance": graph("provenance", [("M1065-X-PROVENANCE", oid, "provenance_of") for oid in machine]),
    "evidence": graph("evidence", []),
    "trust": graph("trust", [("M1065-S-FOUNDATION", oid, "trusts") for oid in machine if oid != "M1065-S-FOUNDATION"]),
    "documentation": graph("documentation", [("M1065-X-SOURCE", oid, "documents") for oid in human if oid != "M1065-X-SOURCE"]),
    "workflow": graph("workflow", [("M1065-X-SOURCE", "M1065-X-PROVENANCE", "workflow_depends_on"),
                                         ("M1065-X-PROVENANCE", ROOT, "workflow_depends_on")]),
}

digest = hashlib.sha256(json.dumps(denominators, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1065/registry-v1", "registry_denominator_sha256": digest,
    "statement_source_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "root_node_id": ROOT, "edge_direction": "prerequisite_or_child -> consumer_or_parent",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{
        "certificate_id": "COMP-M1065-WITNESS-ROOT-V1", "parent": ROOT,
        "required_children": ["M1065-T-WITNESS", "M1065-T-COMPOSE"],
        "checked_declaration": "Stage1Instances.THM_M_1065.ObligationTree.kmtTarget_iff_couplingData",
        "status": "exact interface composition kernel-checked; substantive children open"
    }],
    "closure_boundary": {
        "closed_obligations": [], "root_closed": False, "root_machine_debt": "M4",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M1065-C-SPACE", "M1065-L-BLOCK-COUPLING", "M1065-L-MAXIMAL-TAIL"]
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

lines = ["# THM-M-1065 obligation tree", "", f"Registry version 1 freezes {len(ids)} obligations before proof work. Every node below is open architecture unless explicitly described as a kernel-checked composition interface.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", "Semantic ledger:"]
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
    lines += ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(ids)} obligations; denominator sha256 {digest}")
