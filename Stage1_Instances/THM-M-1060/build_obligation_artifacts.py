#!/usr/bin/env python3
"""Build the frozen THM-M-1060 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# IDs and architecture are selected from the mathematics, not observed closure.
SPECS = [
    ("M1060-ROOT", "root", "SchilderTarget for every Wiener measure on BasedPath.",
     "Stage1Instances.THM_M_1060.SchilderTarget", "The exact canonical target.", "critical", "H2"),
    ("M1060-S-DEFINITIONS", "definition", "Fix BasedPath, scaling, Wiener finite-dimensional laws, the small-noise LDP, and the Cameron-Martin rate.",
     "Statement.lean definitions used by SchilderTarget", "Exact objects and binder order used by every later node.", "high", "not_applicable"),
    ("M1060-S-BOUNDARY", "normalization", "Retain the horizon [0,1], epsilon tending to zero from above, empty sets, and extended-real conventions.",
     "Boundary package for SchilderTarget", "No finite-dimensional, one-sided, or assumed-LDP substitution enters the proof.", "high", "H2"),
    ("M1060-S-FOUNDATION", "certificate", "Freeze classical noncomputable measure theory, choice, and kernel trust policy.",
     "Foundation and trust certificate", "An audited foundation profile for every eventual proof body.", "critical", "not_applicable"),
    ("M1060-N-WIENER", "normalization", "Derive the increment, covariance, and path-law facts needed from IsWienerMeasure.",
     "IsWienerMeasure W -> Wiener increment and covariance interface", "A usable Wiener-law interface without assuming any LDP conclusion.", "critical", "H2"),
    ("M1060-N-LDP", "transport", "Translate the epsilon-log filter convention to the finite-dimensional and exponential-equivalence formulations used below.",
     "Equivalence of SmallNoiseLDP bounds with the selected auxiliary normalizations", "Correct signs, speed, filters, and empty-set behavior in both directions.", "critical", "H2"),
    ("M1060-C-PROJECTION", "construction", "Construct dyadic polygonal interpolation and its finite evaluation map on BasedPath.",
     "Dyadic projection P_n : BasedPath -> BasedPath with measurable/continuous evaluation maps", "A based piecewise-linear approximation with all measurability and compatibility invariants.", "high", "H2"),
    ("M1060-L-GAUSSIAN", "core_lemma", "Prove the small-noise LDP for each finite Gaussian increment vector.",
     "Finite-dimensional centered Gaussian LDP with quadratic covariance rate", "Open and closed finite-dimensional bounds at speed 1/epsilon.", "critical", "H2"),
    ("M1060-L-PROJECTED", "core_lemma", "Transport the finite Gaussian LDP through dyadic polygonal interpolation.",
     "Small-noise LDP for Measure.map P_n (Measure.map (scale (sqrt epsilon)) W)", "An LDP for every fixed polygonal approximation with its discrete energy.", "critical", "H2"),
    ("M1060-L-MODULUS", "core_lemma", "Establish the Brownian modulus-of-continuity exponential tail bound uniformly at small noise.",
     "lim n -> infinity, limsup epsilon -> 0+, epsilon * log P(||sqrt epsilon W-P_n(sqrt epsilon W)||>=delta)=-infinity", "Exponential approximation of scaled paths by dyadic interpolants.", "critical", "H2"),
    ("M1060-L-EXP-EQUIV", "bridge", "Apply a proved exponential-approximation transfer theorem to the projected laws.",
     "Exponential approximation transfer for open/closed LDP bounds", "Path-space lower and upper bounds with the limiting candidate rate.", "critical", "H2"),
    ("M1060-L-RATE-ID", "core_lemma", "Identify the supremum of dyadic discrete energies with cameronMartinRate.",
     "sup_n discreteEnergy n f = cameronMartinRate f", "The transferred LDP uses exactly the frozen Cameron-Martin rate.", "critical", "H2"),
    ("M1060-T-LOWER", "terminal", "Derive the open-set lower bound for every Wiener measure.",
     "forall W, IsWienerMeasure W -> forall G, IsOpen G -> -(sInf (rate '' G)) <= liminf ...", "The first conjunct of SmallNoiseLDP.", "critical", "H2"),
    ("M1060-T-UPPER", "terminal", "Derive the closed-set upper bound for every Wiener measure.",
     "forall W, IsWienerMeasure W -> forall F, IsClosed F -> limsup ... <= -(sInf (rate '' F))", "The second conjunct of SmallNoiseLDP.", "critical", "H2"),
    ("M1060-C-CM-WITNESS", "construction", "Relate integral-representation witnesses to absolutely continuous based paths and their a.e. derivatives.",
     "Cameron-Martin witness equivalence and energy uniqueness", "A representation-independent energy characterization.", "high", "H2"),
    ("M1060-L-RATE-LSC", "core_lemma", "Prove lower semicontinuity of cameronMartinRate in the uniform path topology.",
     "LowerSemicontinuous cameronMartinRate", "Closed real sublevel sets.", "critical", "H2"),
    ("M1060-L-SUBLEVEL-BOUND", "core_lemma", "Prove uniform boundedness and equicontinuity of every finite-energy sublevel using Cauchy-Schwarz.",
     "Equicontinuity and uniform boundedness of {f | cameronMartinRate f <= a}", "Relative compactness of each real sublevel.", "critical", "H2"),
    ("M1060-T-GOOD", "terminal", "Combine closedness and relative compactness to prove compactness of every real rate sublevel.",
     "forall a : Real, IsCompact {f | cameronMartinRate f <= a}", "The third conjunct of SmallNoiseLDP.", "critical", "H2"),
    ("M1060-T-COMPOSE", "terminal", "Conjoin the exact open lower, closed upper, and goodness conclusions for each Wiener measure.",
     "SchilderTarget from the three exact conjunct packages", "The complete SmallNoiseLDP conclusion with no undeclared premise.", "critical", "H2"),
    ("M1060-X-SOURCE", "terminal", "Map every root-relevant proof node to exact primary and modern source pinpoints and errata review.",
     "Human-source crosswalk overlay", "Source-boundary classification only; no machine proof credit.", "high", "H2"),
    ("M1060-X-PROVENANCE", "terminal", "Record terminal proof-body, wrapper, dependency, axiom, and unsafe/oracle provenance.",
     "Formal provenance overlay", "Provenance classification only; no proof credit without checked bodies.", "critical", "not_applicable"),
]

ids = [x[0] for x in SPECS]
machine = ids[:-2]
human = [x[0] for x in SPECS if x[6] != "not_applicable"]
denominators = {
    "inventory": ids,
    "required_machine": machine,
    "required_human_source": human,
    "required_readable": ids,
    "informational_overlays": ids[-2:],
}

def fingerprint(oid, formal):
    if oid == "M1060-ROOT":
        # SHA-256 of the exact `lake env lean Statement.lean` printed declaration output.
        return "lean-expression-sha256:a5d3c4e6d9c19f45a79240a26c72c098a43adf164171b3167ee8bee67c1ab7f8"
    data = f"THM-M-1060/registry-v1/{oid}/{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(data).hexdigest()

obligations = []
nodes = []
for oid, kind, human_statement, formal, output, risk, human_debt in SPECS:
    machine_required = oid in machine
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(oid, formal),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if machine_required else "informational",
        "human_source_eligibility": "required" if oid in human else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None if machine_required else "overlay-no-proof-credit",
        "terminal_proof_body_id": None,
    })
    ledger = (["Consume every incoming proof premise at its exact planned signature.",
               f"Derive: {output}",
               "Discharge the registered parent composition edge without an undeclared premise."]
              if kind in {"root", "terminal"} else
              ["Freeze the exact hypotheses and named interfaces.",
               f"Establish: {human_statement}",
               f"Derive: {output}",
               "Pass the output through the registered typed edge without changing the target."])
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": human_statement, "formal_target": formal, "output": output,
        "human_debt": human_debt, "machine_debt": "M3" if kind == "definition" else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "pending-node-pinpoint-review" if oid != "M1060-X-PROVENANCE" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": len(ledger), "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1060/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture only; this node has no accepted proof body and does not close the root.",
        "task_ids": ["S56-M-1060-OBLIGATION_TREE", "S56-M-1060-PROOF"],
        "owned_sources": [], "owner": "THM-M-1060 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1060-OBLIGATION_TREE",
    "theorem_id": "THM-M-1060", "registry_version": 1,
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; architecture and eligibility selected without observing proof closure.",
    "root_obligation_id": "M1060-ROOT", "frozen_denominators": denominators,
    "eligibility_policy": "All semantic nodes needed by the selected polygonal-approximation proof are required regardless of current library availability. Overlays cannot earn proof credit.",
    "exclusions": [
        "Finite-dimensional Gaussian LDPs, one-sided bounds, compact-set upper bounds, or an assumed abstract LDP are not the root.",
        "The interval is [0,1]; time-rescaling transports do not add obligations or proof-body credit.",
        "Aliases, wrappers, source rows, and presentation splits do not add semantic or terminal-body credit."
    ], "obligations": obligations,
}

# Child/prerequisite -> consumer/parent. Proof and refinement stay distinct.
proof_pairs = [
    ("M1060-S-DEFINITIONS", "M1060-T-COMPOSE", "proof_requires"),
    ("M1060-S-BOUNDARY", "M1060-T-COMPOSE", "proof_requires"),
    ("M1060-S-FOUNDATION", "M1060-T-COMPOSE", "proof_requires"),
    ("M1060-N-WIENER", "M1060-C-PROJECTION", "proof_requires"),
    ("M1060-N-WIENER", "M1060-L-MODULUS", "proof_requires"),
    ("M1060-N-LDP", "M1060-L-PROJECTED", "proof_requires"),
    ("M1060-C-PROJECTION", "M1060-L-PROJECTED", "proof_requires"),
    ("M1060-L-GAUSSIAN", "M1060-L-PROJECTED", "proof_requires"),
    ("M1060-L-PROJECTED", "M1060-L-EXP-EQUIV", "proof_requires"),
    ("M1060-L-MODULUS", "M1060-L-EXP-EQUIV", "proof_requires"),
    ("M1060-L-RATE-ID", "M1060-L-EXP-EQUIV", "proof_requires"),
    ("M1060-L-EXP-EQUIV", "M1060-T-LOWER", "composes"),
    ("M1060-L-EXP-EQUIV", "M1060-T-UPPER", "composes"),
    ("M1060-C-CM-WITNESS", "M1060-L-RATE-ID", "proof_requires"),
    ("M1060-C-CM-WITNESS", "M1060-L-RATE-LSC", "proof_requires"),
    ("M1060-C-CM-WITNESS", "M1060-L-SUBLEVEL-BOUND", "proof_requires"),
    ("M1060-L-RATE-LSC", "M1060-T-GOOD", "proof_requires"),
    ("M1060-L-SUBLEVEL-BOUND", "M1060-T-GOOD", "proof_requires"),
    ("M1060-T-LOWER", "M1060-T-COMPOSE", "composes"),
    ("M1060-T-UPPER", "M1060-T-COMPOSE", "composes"),
    ("M1060-T-GOOD", "M1060-T-COMPOSE", "composes"),
    ("M1060-T-COMPOSE", "M1060-ROOT", "composes"),
]
refinement_pairs = [
    ("M1060-T-LOWER", "M1060-L-EXP-EQUIV", "logical_decomposition"),
    ("M1060-T-UPPER", "M1060-L-EXP-EQUIV", "logical_decomposition"),
    ("M1060-L-RATE-LSC", "M1060-T-GOOD", "logical_decomposition"),
    ("M1060-L-SUBLEVEL-BOUND", "M1060-T-GOOD", "logical_decomposition"),
]

def graph(name, pairs):
    edges, outgoing, incoming = [], {}, {}
    for i, (src, dst, role) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{i:03d}"
        edge = {"edge_id": eid, "from": src, "to": dst, "type": role}
        edges.append(edge); outgoing.setdefault(src, []).append(eid); incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}

graphs = {
    "proof": graph("proof", proof_pairs),
    "refinement": graph("refinement", refinement_pairs),
    "provenance": graph("provenance", [("M1060-X-PROVENANCE", x, "provenance_of") for x in machine]),
    "evidence": graph("evidence", []),
    "trust": graph("trust", [("M1060-S-FOUNDATION", x, "trusts") for x in machine if x != "M1060-S-FOUNDATION"]),
    "documentation": graph("documentation", [("M1060-X-SOURCE", x, "documents") for x in human]),
    "workflow": graph("workflow", [("M1060-X-SOURCE", "M1060-X-PROVENANCE", "workflow_depends_on"),
                                            ("M1060-X-PROVENANCE", "M1060-ROOT", "workflow_depends_on")]),
}

digest = hashlib.sha256(json.dumps(denominators, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"],
    "registry_id": "THM-M-1060/registry-v1", "registry_denominator_sha256": digest,
    "statement_source_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "root_node_id": "M1060-ROOT", "edge_direction": "prerequisite_or_child -> consumer_or_parent",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{
        "certificate_id": "COMP-M1060-SMALL-NOISE-LDP-V1", "parent": "M1060-T-COMPOSE",
        "required_children": ["M1060-T-LOWER", "M1060-T-UPPER", "M1060-T-GOOD"],
        "checked_declaration": "Stage1Instances.THM_M_1060.ObligationTree.smallNoiseLDP_of_bounds_and_good",
        "status": "interface-composition-kernel-checked; children-open"
    }, {
        "certificate_id": "COMP-M1060-ROOT-V1", "parent": "M1060-ROOT",
        "required_children": ["M1060-T-COMPOSE"],
        "checked_declaration": "Stage1Instances.THM_M_1060.ObligationTree.schilderTarget_of_components",
        "status": "interface-composition-kernel-checked; child-open"
    }],
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M1060-L-GAUSSIAN", "M1060-L-MODULUS", "M1060-L-EXP-EQUIV", "M1060-L-RATE-ID", "M1060-L-RATE-LSC", "M1060-L-SUBLEVEL-BOUND"]}
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1060 obligation tree", "", "This registry freezes a polygonal-approximation proof route before proof closure is observed. All nodes are open architecture obligations.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
    lines += ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(ids)} obligations; denominator sha256 {digest}")
