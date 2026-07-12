#!/usr/bin/env python3
"""Build the frozen THM-M-1063 Donsker obligation architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1063-OBLIGATION_TREE"
THEOREM = "THM-M-1063"

# This is a proof plan selected from the exact target and the audited classical
# truncation/tightness route. It deliberately does not encode observed closure.
SPECS = [
    ("M1063-ROOT", "root", "The normalized polygonal partial-sum processes converge in distribution in C([0,1], Real) to the specified standard Brownian path variable.", "AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple", "The exact frozen Donsker target.", "critical", "required"),
    ("M1063-S-DEFS", "definition", "Freeze UnitInterval, polygonalValue, IsPolygonalWalk, IsStandardBrownian, and TendstoInDistribution with the exact binder order.", "Definitions in DonskerTarget.lean", "The exact objects and conclusion used by every proof node.", "critical", "not_applicable"),
    ("M1063-S-DOMAINS", "definition", "Fix both probability spaces, the Borel uniform topology on continuous paths, and all measurable structures and instances.", "Measurable-space and BorelSpace context of DonskerInvariancePrinciple", "No silent change of path topology, law, or probability space.", "high", "not_applicable"),
    ("M1063-S-BOUNDARY", "normalization", "Account for n=0 totalization, t=0, t=1, positive sigma, and the clipped final interpolation segment.", "Boundary package for polygonalValue", "The total definition agrees with n normalized increments at t=1 and has the intended asymptotic domain.", "high", "required"),
    ("M1063-S-FOUNDATION", "certificate", "Freeze classical noncomputable measure theory, accepted Lean foundations, and the no-placeholder/no-oracle policy.", "Foundation and trust certificate", "An audited foundation profile for every admitted body.", "critical", "not_applicable"),
    ("M1063-N-STANDARDIZE", "normalization", "Reduce the increments to centered variance-one variables by division by positive sigma.", "X i / sigma with mean 0 and variance 1", "A standardized iid sequence without changing the polygonal target.", "high", "required"),
    ("M1063-N-FIDI", "normalization", "Rewrite every finite linear combination of path evaluations as a triangular weighted sum of standardized increments plus a vanishing interpolation remainder.", "Finite evaluation linear-combination identity", "A scalar triangular-array expression suitable for Cramer-Wold.", "critical", "required"),
    ("M1063-B-FIDI", "branch", "Prove convergence of every finite vector of polygonal evaluations to the Brownian evaluation vector.", "Finite-dimensional distribution convergence for W n", "All finite-dimensional marginals converge with covariance min(s,t).", "critical", "required"),
    ("M1063-B-TIGHT", "branch", "Prove tightness of the complete sequence of polygonal path laws in the uniform topology.", "Tight (fun n => Measure.map (W n) P)", "Uniform path-space tightness under only a finite second moment.", "critical", "required"),
    ("M1063-B-RECOMPOSE", "terminal", "Combine tightness and finite-dimensional convergence, identify all subsequential limits, and recover convergence of the whole sequence.", "TendstoInDistribution W atTop B (fun _ => P) PB", "The exact path-space convergence conclusion.", "critical", "required"),
    ("M1063-C-PATH", "construction", "Construct the polygonal interpolation as a continuous map and prove equality with polygonalValue.", "forall n omega, C(UnitInterval, Real)", "Continuous based polygonal paths with the frozen pointwise formula.", "high", "required"),
    ("M1063-C-MEAS", "construction", "Prove measurability of every polygonal path random variable into the Borel uniform path space.", "forall n, AEMeasurable (W n) P", "Well-defined pushforward laws and applicability of convergence-in-distribution APIs.", "critical", "required"),
    ("M1063-C-TRUNC", "construction", "Choose a deterministic truncation scale and split increments into bounded centered parts and a rare large-jump remainder.", "Triangular truncation and recentering package", "A bounded array plus a remainder controlled by finite second moments.", "critical", "required"),
    ("M1063-L-TAIL", "core_lemma", "Use finite second moment to show the accumulated large-jump contribution is negligible at diffusive scale.", "Large-jump maximum tends to zero in probability", "Removal of the truncation remainder uniformly over time.", "critical", "required"),
    ("M1063-L-MAX", "core_lemma", "Establish the required maximal inequality for centered independent bounded block sums.", "Maximal partial-sum probability estimate", "Control of oscillations inside time blocks.", "critical", "required"),
    ("M1063-L-MODULUS", "core_lemma", "Combine truncation and maximal estimates to control the uniform modulus of continuity of polygonal paths.", "lim delta->0, limsup n, P(modulus(W n,delta)>eta)=0", "The equicontinuity-in-probability criterion for tightness.", "critical", "required"),
    ("M1063-L-ORIGIN", "core_lemma", "Control W n at the origin and uniform path magnitude using the same maximal estimates.", "Tightness at one time and uniform boundedness in probability", "The pointwise component of the path compactness criterion.", "high", "required"),
    ("M1063-L-ASCOLI", "bridge", "Apply Arzela-Ascoli to turn uniform bounds and modulus control into compact subsets of continuous path space.", "Compact containment from bounded equicontinuous path sets", "Compact sets capturing arbitrarily large path-law mass.", "critical", "required"),
    ("M1063-L-TIGHT", "terminal", "Derive tightness of polygonal laws from compact containment.", "Tight (fun n => Measure.map (W n) P)", "The complete tightness branch.", "critical", "required"),
    ("M1063-L-CLT", "bridge", "Prove the scalar triangular-array central limit theorem needed for finite linear combinations, preserving the variance calculation.", "Weighted triangular-array CLT", "Gaussian limits for the Cramer-Wold scalar projections.", "critical", "required"),
    ("M1063-L-COV", "core_lemma", "Compute limiting covariances of polygonal evaluations as min(s,t).", "lim n, Cov(W n s,W n t)=min s t", "The covariance matrix of every limiting finite Gaussian vector.", "critical", "required"),
    ("M1063-L-CRAMER", "bridge", "Apply Cramer-Wold to the scalar projection limits.", "Finite-vector convergence in distribution", "Joint Gaussian finite-dimensional limits with the Brownian covariance.", "critical", "required"),
    ("M1063-L-BROWNIAN-FIDI", "terminal", "Use the specified Brownian process predicate to match the limiting Gaussian vectors, including their zero means and covariance.", "FDD(W n) -> FDD(B)", "The complete finite-dimensional convergence branch.", "critical", "required"),
    ("M1063-L-PROKHOROV", "bridge", "Extract weakly convergent subsequences of path laws from tightness.", "Every subsequence has a weakly convergent subsubsequence", "Candidate probability laws on continuous path space.", "critical", "required"),
    ("M1063-L-EVAL", "bridge", "Transport subsequential weak convergence through every finite continuous evaluation map.", "Candidate-law finite-dimensional marginals equal Brownian marginals", "Every subsequential limit has the target finite-dimensional laws.", "critical", "required"),
    ("M1063-L-LAW-UNIQUE", "core_lemma", "Prove that probability laws on continuous paths are determined by finite evaluations on a countable dense time set.", "Equality of path laws from finite-dimensional marginals", "Every subsequential limit equals the law of B.", "critical", "required"),
    ("M1063-T-SEQUENCE", "terminal", "Use uniqueness of all subsequential limits to prove convergence of the full sequence of laws.", "Tendsto (law(W n)) atTop (law B)", "Full weak convergence, not merely subsequential convergence.", "critical", "required"),
    ("M1063-T-API", "transport", "Translate weak convergence of pushforward laws into the frozen TendstoInDistribution declaration with its varying source measures.", "TendstoInDistribution W atTop B (fun _ => P) PB", "The exact target API with no assumed convergence premise.", "critical", "required"),
    ("M1063-X-SCALAR-CLT", "bridge", "Audit and use the pinned mathlib scalar CLT only at the exact scalar leaf it supports.", "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum[_sub]", "A checked scalar anchor; never path-space closure.", "high", "required"),
    ("M1063-X-SOURCE", "terminal", "Map root-relevant mathematical nodes to pinpoint human sources and errata review.", "Human-source crosswalk overlay", "Source classification only; no machine proof credit.", "high", "informational"),
    ("M1063-X-PROVENANCE", "terminal", "Record proof-body, dependency, axiom, unsafe, automation, and external-project provenance.", "Formal provenance overlay", "Provenance classification only; no proof credit.", "critical", "informational"),
]

ids = [x[0] for x in SPECS]
machine = [x[0] for x in SPECS if x[6] != "informational"]
human = [x[0] for x in SPECS if x[6] == "required"]
denominators = {"inventory": ids, "required_machine": machine,
                "required_human_source": human, "required_readable": ids,
                "informational_overlays": ["M1063-X-SOURCE", "M1063-X-PROVENANCE"]}

root_fp = "lean-expression-sha256:a5bb2e2443661e20f8342ed0dba6b7f7ef5f5ce445bc2d5bbdf19ef5ce842c81"
def fingerprint(oid, formal):
    if oid == "M1063-ROOT":
        return root_fp
    raw = f"THM-M-1063/registry-v1/{oid}/{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(raw).hexdigest()

obligations, nodes = [], []
for oid, kind, statement, formal, output, risk, human_elig in SPECS:
    machine_required = oid in machine
    obligations.append({"obligation_id": oid, "statement_fingerprint": fingerprint(oid, formal),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": "required" if machine_required else "informational",
        "human_source_eligibility": "required" if human_elig == "required" else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None if machine_required else "overlay-no-proof-credit",
        "terminal_proof_body_id": None})
    ledger = ["Consume each registered incoming premise at its exact planned signature.",
              f"Establish the named transition: {statement}", f"Derive: {output}",
              "Pass that output through the typed parent edge without strengthening assumptions."]
    nodes.append({"node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": "H2" if human_elig == "required" else "H5",
        "machine_debt": "M3" if kind == "definition" else "M4", "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "pending-node-pinpoint-review" if human_elig == "required" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending", "computation_record": "none",
        "step_budget": len(ledger), "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1063/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture only; no proof body or closure credit is assigned by this node.",
        "task_ids": [ITEM, "S56-M-1063-PROOF"], "owned_sources": [],
        "owner": "THM-M-1063 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none"})

registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "freeze_basis": "Exact elaborated Donsker statement and immutable anchor audit; classical truncation, finite-dimensional convergence, and tightness architecture selected before observing closure.",
    "root_obligation_id": "M1063-ROOT", "frozen_denominators": denominators,
    "eligibility_policy": "Every semantic node needed by the selected finite-second-moment Donsker route is required irrespective of current library availability; overlays never earn proof credit.",
    "exclusions": ["Scalar or finite-dimensional CLT alone is not path-space convergence.",
      "An assumed tightness, Brownian-law uniqueness, or abstract Donsker theorem is not a discharged leaf.",
      "Step processes, Skorokhod topology, stronger moments, bounded increments, and one probability space are not substitutions for the frozen target.",
      "Aliases, wrappers, presentation rows, and source overlays add no semantic or terminal-body credit."],
    "obligations": obligations}

proof_pairs = [
 ("M1063-S-DEFS","M1063-C-PATH","proof_requires"),("M1063-S-DOMAINS","M1063-C-MEAS","proof_requires"),
 ("M1063-S-BOUNDARY","M1063-N-STANDARDIZE","proof_requires"),("M1063-S-FOUNDATION","M1063-B-RECOMPOSE","proof_requires"),
 ("M1063-N-STANDARDIZE","M1063-N-FIDI","proof_requires"),("M1063-C-PATH","M1063-C-MEAS","proof_requires"),
 ("M1063-C-PATH","M1063-N-FIDI","proof_requires"),("M1063-N-FIDI","M1063-L-CLT","proof_requires"),
 ("M1063-X-SCALAR-CLT","M1063-L-CLT","proof_requires"),("M1063-L-CLT","M1063-L-CRAMER","proof_requires"),
 ("M1063-L-COV","M1063-L-CRAMER","proof_requires"),("M1063-L-CRAMER","M1063-L-BROWNIAN-FIDI","proof_requires"),
 ("M1063-L-BROWNIAN-FIDI","M1063-B-FIDI","composes"),("M1063-N-STANDARDIZE","M1063-C-TRUNC","proof_requires"),
 ("M1063-C-TRUNC","M1063-L-TAIL","proof_requires"),("M1063-C-TRUNC","M1063-L-MAX","proof_requires"),
 ("M1063-L-TAIL","M1063-L-MODULUS","proof_requires"),("M1063-L-MAX","M1063-L-MODULUS","proof_requires"),
 ("M1063-L-MAX","M1063-L-ORIGIN","proof_requires"),("M1063-L-MODULUS","M1063-L-ASCOLI","proof_requires"),
 ("M1063-L-ORIGIN","M1063-L-ASCOLI","proof_requires"),("M1063-L-ASCOLI","M1063-L-TIGHT","proof_requires"),
 ("M1063-C-MEAS","M1063-L-TIGHT","proof_requires"),("M1063-L-TIGHT","M1063-B-TIGHT","composes"),
 ("M1063-B-TIGHT","M1063-L-PROKHOROV","proof_requires"),("M1063-L-PROKHOROV","M1063-L-EVAL","proof_requires"),
 ("M1063-B-FIDI","M1063-L-EVAL","proof_requires"),("M1063-L-EVAL","M1063-L-LAW-UNIQUE","proof_requires"),
 ("M1063-L-LAW-UNIQUE","M1063-T-SEQUENCE","proof_requires"),("M1063-L-PROKHOROV","M1063-T-SEQUENCE","proof_requires"),
 ("M1063-T-SEQUENCE","M1063-T-API","proof_requires"),("M1063-T-API","M1063-B-RECOMPOSE","composes"),
 ("M1063-B-FIDI","M1063-B-RECOMPOSE","proof_requires"),("M1063-B-TIGHT","M1063-B-RECOMPOSE","proof_requires"),
 ("M1063-B-RECOMPOSE","M1063-ROOT","composes")]
refinement_pairs = [("M1063-B-FIDI","M1063-ROOT","logical_decomposition"),
 ("M1063-B-TIGHT","M1063-ROOT","logical_decomposition"),
 ("M1063-L-TAIL","M1063-B-TIGHT","logical_decomposition"),
 ("M1063-L-MODULUS","M1063-B-TIGHT","logical_decomposition"),
 ("M1063-L-LAW-UNIQUE","M1063-B-RECOMPOSE","logical_decomposition")]

def graph(name, pairs):
    edges, outgoing, incoming = [], {}, {}
    for i, (src, dst, role) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{i:03d}"
        edges.append({"edge_id": eid, "from": src, "to": dst, "type": role})
        outgoing.setdefault(src, []).append(eid); incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}

graphs = {"proof": graph("proof", proof_pairs), "refinement": graph("refinement", refinement_pairs),
 "provenance": graph("provenance", [("M1063-X-PROVENANCE", x, "provenance_of") for x in machine]),
 "evidence": graph("evidence", []),
 "trust": graph("trust", [("M1063-S-FOUNDATION", x, "trusts") for x in machine if x != "M1063-S-FOUNDATION"]),
 "documentation": graph("documentation", [("M1063-X-SOURCE", x, "documents") for x in human]),
 "workflow": graph("workflow", [("M1063-X-SOURCE","M1063-X-PROVENANCE","workflow_depends_on"),
                                    ("M1063-X-PROVENANCE","M1063-ROOT","workflow_depends_on")])}
digest = hashlib.sha256(json.dumps(denominators, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
 "registry_id": "THM-M-1063/registry-v1", "registry_denominator_sha256": digest,
 "statement_source_sha256": hashlib.sha256((HERE / "DonskerTarget.lean").read_bytes()).hexdigest(),
 "root_node_id": "M1063-ROOT", "edge_direction": "prerequisite_or_child -> consumer_or_parent",
 "nodes": nodes, "graphs": graphs,
 "composition_certificates": [{"certificate_id":"COMP-M1063-ROOT-IDENTITY-V1","parent":"M1063-ROOT",
   "required_children":["M1063-B-RECOMPOSE"],
   "checked_declaration":"AwesomeTheorems.Stage1.THM_M_1063.ObligationTree.exactRoot_of_exactRoot",
   "status":"exact-root identity interface kernel-checked; substantive child composition remains open"}],
 "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt":"M4",
   "audit_complete":False,"theorem_complete":False,
   "remaining_root_cut_set":["M1063-L-CLT","M1063-L-MODULUS","M1063-L-ASCOLI","M1063-L-PROKHOROV","M1063-L-LAW-UNIQUE","M1063-T-API"]}}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
lines = ["# THM-M-1063 obligation tree", "", "This registry freezes the classical finite-second-moment Donsker route before proof closure is observed. Every mathematical node is open.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
    lines += ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(ids)} obligations; denominator sha256 {digest}")
