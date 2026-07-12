#!/usr/bin/env python3
"""Build the frozen THM-M-1085 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = "M1085"

# The route is the standard covariance-interpolation proof.  The registry is selected from the
# mathematics and the frozen statement, independently of whether any proof body is available.
SPECS = [
    ("ROOT", "root", "The exact finite-dimensional SlepianTarget.",
     "Stage1Instances.THM_M_1085.SlepianTarget", "The canonical lower-orthant comparison.", "critical", "H1"),
    ("S-DEFINITIONS", "definition", "Freeze BelowAll, coordinate means, covariances, and lower-orthant probabilities.",
     "Definitions and binders of Statement.lean", "The exact objects used by all later nodes.", "high", "not_applicable"),
    ("S-DOMAINS", "normalization", "Audit finite nonempty indexing, two sample spaces, measurability, integrability, and extended-real measure values.",
     "Domain package for SlepianTarget", "No common-space, density, or positive-definiteness premise is introduced.", "critical", "H1"),
    ("S-BOUNDARY", "branch", "Cover singleton indices and singular or repeated-coordinate Gaussian laws.",
     "Boundary package including singleton_boundary", "The proof route includes every degenerate case admitted by the target.", "critical", "H1"),
    ("S-FOUNDATION", "certificate", "Freeze classical choice, integration, measure, and trust assumptions.",
     "Foundation and TCB certificate", "An auditable foundation profile for eventual proof bodies.", "critical", "not_applicable"),
    ("N-LAWS", "normalization", "Push both random vectors to their finite coordinate laws and recover means and covariance entries.",
     "HasGaussianLaw pushforward reduction on a finite coordinate type", "Two centered finite Gaussian laws with the frozen covariance data.", "critical", "H1"),
    ("N-MATRIX", "normalization", "Encode covariance as symmetric positive-semidefinite matrices with equal diagonals and ordered off-diagonals.",
     "Finite covariance-matrix interface", "Matrix data equivalent in the required direction to the target hypotheses.", "critical", "H1"),
    ("C-INTERPOLATION", "construction", "Construct C(s) = (1-s) C_X + s C_Y and its centered Gaussian law for s in [0,1].",
     "Interpolated centered Gaussian law with covariance C(s)", "A Gaussian path joining the endpoint laws, including singular matrices.", "critical", "H1"),
    ("C-SMOOTHER", "construction", "Construct bounded smooth decreasing coordinate cutoffs converging to 1_{x <= t}.",
     "Smooth lower-orthant approximants F_epsilon,t", "Integrable C2 test functions with controlled mixed derivatives.", "high", "H1"),
    ("L-INTERPOLATION-ID", "core_lemma", "Prove the Gaussian covariance interpolation derivative identity for bounded C2 tests.",
     "d/ds E[F(Z_s)] = (1/2) sum_ij (C_Y-C_X)_ij E[partial_ij F(Z_s)]", "An exact derivative formula valid at singular endpoints by approximation.", "critical", "H1"),
    ("L-MIXED-SIGN", "core_lemma", "Show every off-diagonal mixed derivative of the product cutoff is nonnegative.",
     "i != j -> 0 <= partial_i partial_j F_epsilon,t", "The covariance-order terms have the comparison sign.", "critical", "H1"),
    ("L-MONOTONE", "core_lemma", "Use equal diagonals and ordered off-diagonals in the derivative identity and integrate over s.",
     "E[F_epsilon,t(X)] <= E[F_epsilon,t(Y)]", "The smoothed lower-orthant comparison for every epsilon > 0.", "critical", "H1"),
    ("L-LIMIT", "core_lemma", "Pass the smooth inequality to lower-orthant indicators using bounded convergence and endpoint-law transport.",
     "P(forall i, X_i <= t) <= P(forall i, Y_i <= t)", "The exact event-probability inequality for every threshold.", "critical", "H1"),
    ("T-COMPARISON", "terminal", "Package the comparison uniformly over every binder and hypothesis of SlepianTarget.",
     "Stage1Instances.THM_M_1085.ObligationTree.PointwiseComparison", "A proposition definitionally equal to the canonical target.", "critical", "H1"),
    ("T-COMPOSE", "terminal", "Transport the terminal comparison to the exact canonical declaration without changing binders.",
     "Stage1Instances.THM_M_1085.ObligationTree.slepianTarget_of_pointwise", "Stage1Instances.THM_M_1085.SlepianTarget.", "critical", "not_applicable"),
    ("X-SOURCE", "terminal", "Map mathematical nodes to exact primary-source proof locations and errata review.",
     "Human-source overlay", "Source classification only; no machine proof credit.", "high", "H1"),
    ("X-PROVENANCE", "terminal", "Record wrapper, terminal-body, dependency, axiom, and unsafe/oracle provenance.",
     "Formal provenance overlay", "Provenance classification only; no proof credit.", "critical", "not_applicable"),
]

specs = [(f"{PREFIX}-{suffix}", *rest) for suffix, *rest in SPECS]
ids = [s[0] for s in specs]
machine = ids[:-2]
human = [s[0] for s in specs if s[6] != "not_applicable"]
denominators = {
    "inventory": ids,
    "required_machine": machine,
    "required_human_source": human,
    "required_readable": ids,
    "informational_overlays": ids[-2:],
}

def fingerprint(oid, formal):
    if oid == f"{PREFIX}-ROOT":
        return "lean-expression-sha256:2af285ae0bb208a80c325d1b8ba89cd273b83d01b2fef018b13e2feca9d43315"
    payload = f"THM-M-1085/registry-v1/{oid}/{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(payload).hexdigest()

obligations, nodes = [], []
for oid, kind, statement, formal, output, risk, human_debt in specs:
    required = oid in machine
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, formal), "kind": kind,
        "root_relevant": True, "machine_eligibility": "required" if required else "informational",
        "human_source_eligibility": "required" if oid in human else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None if required else "overlay-no-proof-credit", "terminal_proof_body_id": None,
    })
    ledger = (["Consume every incoming proof premise at its exact planned signature.",
               f"Derive: {output}", "Use the registered composition edge without an undeclared premise."]
              if kind in {"root", "terminal"} else
              ["Fix the exact context and named premises from the frozen target.", f"Establish: {statement}",
               f"Derive: {output}", "Pass the output through its typed edge without changing the target."])
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": statement,
        "formal_target": formal, "output": output, "human_debt": human_debt,
        "machine_debt": "M3" if kind == "definition" else "M4", "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "pending-node-pinpoint-review" if human_debt != "not_applicable" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending", "computation_record": "none",
        "step_budget": len(ledger), "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1085/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture only; no accepted proof body or root closure is claimed.",
        "task_ids": ["S56-M-1085-OBLIGATION_TREE", "S56-M-1085-PROOF"], "owned_sources": [],
        "owner": "THM-M-1085 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1085-OBLIGATION_TREE",
    "theorem_id": "THM-M-1085", "registry_version": 1,
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; covariance-interpolation architecture selected without observing proof closure.",
    "root_obligation_id": f"{PREFIX}-ROOT", "frozen_denominators": denominators,
    "eligibility_policy": "Every semantic node needed by covariance interpolation is required regardless of library availability; overlays earn no proof credit.",
    "exclusions": [
        "Expected-maximum-only and strict-threshold-only Slepian variants are not substitutes for the frozen lower-orthant target.",
        "Positive-definite covariance, positive variance, density, and common-sample-space assumptions may not be added.",
        "Aliases, wrappers, source rows, and transports do not duplicate semantic or terminal-body credit."
    ], "obligations": obligations,
}

P = PREFIX + "-"
proof_pairs = [
    (P+"S-DEFINITIONS", P+"N-LAWS", "proof_requires"), (P+"S-DOMAINS", P+"N-LAWS", "proof_requires"),
    (P+"S-BOUNDARY", P+"C-INTERPOLATION", "proof_requires"), (P+"N-LAWS", P+"N-MATRIX", "proof_requires"),
    (P+"N-MATRIX", P+"C-INTERPOLATION", "proof_requires"), (P+"C-INTERPOLATION", P+"L-INTERPOLATION-ID", "proof_requires"),
    (P+"C-SMOOTHER", P+"L-INTERPOLATION-ID", "proof_requires"), (P+"C-SMOOTHER", P+"L-MIXED-SIGN", "proof_requires"),
    (P+"L-INTERPOLATION-ID", P+"L-MONOTONE", "proof_requires"), (P+"L-MIXED-SIGN", P+"L-MONOTONE", "proof_requires"),
    (P+"N-MATRIX", P+"L-MONOTONE", "proof_requires"), (P+"L-MONOTONE", P+"L-LIMIT", "proof_requires"),
    (P+"N-LAWS", P+"L-LIMIT", "proof_requires"), (P+"S-DOMAINS", P+"L-LIMIT", "proof_requires"),
    (P+"S-FOUNDATION", P+"T-COMPARISON", "proof_requires"), (P+"L-LIMIT", P+"T-COMPARISON", "composes"),
    (P+"T-COMPARISON", P+"T-COMPOSE", "composes"), (P+"T-COMPOSE", P+"ROOT", "composes"),
]
refinement_pairs = [(P+"N-LAWS", P+"ROOT", "logical_decomposition"),
                    (P+"L-MONOTONE", P+"L-LIMIT", "logical_decomposition"),
                    (P+"T-COMPARISON", P+"ROOT", "logical_decomposition")]

def graph(name, pairs):
    edges, outgoing, incoming = [], {}, {}
    for n, (src, dst, role) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{n:03d}"
        edges.append({"edge_id": eid, "from": src, "to": dst, "type": role})
        outgoing.setdefault(src, []).append(eid); incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}

graphs = {
    "proof": graph("proof", proof_pairs), "refinement": graph("refinement", refinement_pairs),
    "provenance": graph("provenance", [(P+"X-PROVENANCE", x, "provenance_of") for x in machine]),
    "evidence": graph("evidence", []),
    "trust": graph("trust", [(P+"S-FOUNDATION", x, "trusts") for x in machine if x != P+"S-FOUNDATION"]),
    "documentation": graph("documentation", [(P+"X-SOURCE", x, "documents") for x in human if x != P+"X-SOURCE"]),
    "workflow": graph("workflow", [(P+"X-SOURCE", P+"X-PROVENANCE", "workflow_depends_on"),
                                         (P+"X-PROVENANCE", P+"T-COMPARISON", "workflow_depends_on"),
                                         (P+"T-COMPARISON", P+"ROOT", "workflow_depends_on")]),
}
digest = hashlib.sha256(json.dumps(denominators, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"],
    "registry_id": "THM-M-1085/registry-v1", "registry_denominator_sha256": digest,
    "statement_source_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "root_node_id": P+"ROOT", "edge_direction": "prerequisite_or_child -> consumer_or_parent", "nodes": nodes,
    "graphs": graphs, "composition_certificates": [{
        "certificate_id": "COMP-M1085-ROOT-V1", "parent": P+"ROOT", "required_children": [P+"T-COMPARISON", P+"T-COMPOSE"],
        "checked_declaration": "Stage1Instances.THM_M_1085.ObligationTree.slepianTarget_of_pointwise",
        "status": "exact-interface-composition-kernel-checked; mathematical child open"
    }],
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": [P+"N-LAWS", P+"C-INTERPOLATION", P+"L-INTERPOLATION-ID", P+"L-MIXED-SIGN", P+"L-LIMIT"]},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
lines = ["# THM-M-1085 obligation tree", "", "This freezes the covariance-interpolation route before proof closure is observed. Every semantic node is open.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "",
              f"Output: {node['output']}", "", "Semantic ledger:"]
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
    lines += ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(ids)} obligations; denominator sha256 {digest}")
