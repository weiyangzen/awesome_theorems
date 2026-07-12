#!/usr/bin/env python3
"""Generate the frozen THM-M-1129 registry, typed graphs, and readable projection."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

specs = [
    ("M1129-ROOT", "root", "The exact canonical PoissonFormulaTarget.", "Stage1.THM_M_1129.PoissonFormulaTarget", "The canonical proposition.", "critical", "H2", "M3", 12),
    ("M1129-S-DEFS", "definition", "Freeze Plane, poissonDiskTerm, and IsClassicalWaveSolution without changing their definitions.", "Stage1.THM_M_1129.{Plane,poissonDiskTerm,IsClassicalWaveSolution}", "The exact definitions used below.", "high", "H2", "M0-L", 15),
    ("M1129-S-DOMAIN", "definition", "Preserve dimension two, c > 0, C3/C2 compactly supported data, the classical compact-support solution class, and t > 0.", "quantified context of Stage1.THM_M_1129.PoissonFormulaTarget", "The exact root context.", "critical", "H2", "M0-L", 18),
    ("M1129-S-BOUNDARY", "branch", "Separate positive-time representation from recovery of displacement and velocity at t = 0.", "planned exact boundary signatures over poissonDiskTerm", "A complete boundary policy with no singular substitution at zero.", "critical", "H2", "M4", 55),
    ("M1129-S-TRANSPORT", "transport", "Relate the fixed unit-disk term to the physical disk of radius c*t with the exact Jacobian and normalization.", "planned checked equivalence for the two disk encodings", "A directional checked transport into the canonical unit-disk statement.", "critical", "H2", "M4", 85),
    ("M1129-S-FOUNDATION", "certificate", "Audit imports, axioms, classical principles, and the Lean/mathlib trust boundary.", "planned transitive axiom and trust report", "An accepted foundation and TCB profile.", "critical", "H2", "M4", 40),
    ("M1129-C-KERNEL", "construction", "Construct both weighted disk integrals as finite real Bochner integrals for positive time.", "planned Lean integrability and construction theorem for poissonDiskTerm", "Well-defined displacement and velocity integral terms.", "critical", "H2", "M4", 80),
    ("M1129-L-WEIGHT", "core_lemma", "Prove integrability of z |-> (1-||z||^2)^(-1/2) on the closed unit disk, including the boundary singularity.", "planned IntegrableOn theorem on closedBall (0 : Plane) 1", "The singular kernel is integrable and boundary values are harmless a.e.", "critical", "H2", "M4", 95),
    ("M1129-L-DATA", "core_lemma", "Derive measurability, boundedness on the moving compact image, and local dominating functions from the data hypotheses.", "planned measurable/bounded/domination lemmas for f and g", "Domination hypotheses required by the parametric integral API.", "high", "H2", "M4", 85),
    ("M1129-L-DIFF", "bridge", "Differentiate the parameterized displacement integral and justify every interchange with the integral.", "planned HasDerivAt theorem for fun s => poissonDiskTerm c s f x", "A checked expression for the outer time derivative.", "critical", "H2", "M4", 90),
    ("M1129-L-SPATIAL", "core_lemma", "Compute the spatial Laplacian of the disk representation using the Euclidean basis expansion.", "planned Laplacian identity for the represented solution", "The spatial side of the wave equation.", "critical", "H2", "M4", 90),
    ("M1129-L-TIME", "core_lemma", "Compute two time derivatives of the represented solution under the singular integral.", "planned second-time-derivative identity", "The time side of the wave equation.", "critical", "H2", "M4", 95),
    ("M1129-L-PDE", "bridge", "Combine the spatial and time derivative identities to show the Poisson expression satisfies u_tt = c^2 Delta u.", "planned wave-equation theorem for the represented expression", "The constructed expression solves the PDE at positive time.", "critical", "H2", "M4", 45),
    ("M1129-L-INITIAL-F", "terminal", "Recover f as the t -> 0+ displacement limit, including the displacement term's outer derivative.", "planned zero-time value theorem for the represented expression", "Initial displacement equals f.", "critical", "H2", "M4", 90),
    ("M1129-L-INITIAL-G", "terminal", "Recover g as the t -> 0+ time derivative of the representation.", "planned zero-time derivative theorem for the represented expression", "Initial velocity equals g.", "critical", "H2", "M4", 90),
    ("M1129-L-UNIQUENESS", "core_lemma", "Prove uniqueness in the exact classical compact-support solution class frozen by the statement.", "planned uniqueness theorem for IsClassicalWaveSolution", "Any two solutions with the same data agree for positive time.", "critical", "H2", "M4", 95),
    ("M1129-T-CONSTRUCT", "terminal", "Assemble well-definedness, PDE, and both initial conditions into a classical solution supplied by the Poisson expression.", "planned construction theorem for the Poisson expression", "A represented classical solution with data f and g.", "critical", "H2", "M4", 60),
    ("M1129-T-REPRESENT", "terminal", "Apply uniqueness to identify the arbitrary input solution u with the constructed Poisson solution.", "Stage1.THM_M_1129.PoissonAnalyticPackage", "The complete analytic package, definitionally the canonical target.", "critical", "H2", "M4", 35),
    ("M1129-T-ASSEMBLE", "transport", "Consume the exact analytic package and return PoissonFormulaTarget without additional premises.", "Stage1.THM_M_1129.poissonFormulaTarget_of_analyticPackage", "The exact canonical proposition, conditionally on the open package.", "high", "H2", "M0-L", 3),
    ("M1129-X-SOURCE", "terminal", "Pin and independently review a primary source for every analytic and uniqueness step.", "human-source boundary; no Lean proof target", "An H0-eligible source crosswalk.", "high", "H2", "not_applicable", 60),
    ("M1129-X-PROVENANCE", "certificate", "Trace every wrapper to its terminal proof body and deduplicate shared bodies.", "planned declaration/proof-body provenance report", "A complete terminal-body provenance map.", "high", "H2", "informational", 40),
    ("M1129-X-TRUST", "certificate", "Recompute exact types, axioms, placeholders, unsafe/oracle boundaries, and dependency closure.", "planned kernel and trust evidence bundle", "Release-gate trust evidence.", "critical", "H2", "informational", 45),
]

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

obligations = []
for oid, kind, human, formal, output, risk, hd, md, budget in specs:
    fp = "lean-expression-sha256:0cb797156a05d1c76475f474799fc7993b09556fa4254dbcf2f61bdb48298b69" if oid == "M1129-ROOT" else "planned:v1:sha256:" + sha(oid + "\n" + formal + "\n" + output)
    machine = "required" if md not in ("not_applicable", "informational") else md
    human_eligible = "not_applicable" if oid in ("M1129-S-DEFS", "M1129-S-FOUNDATION", "M1129-X-PROVENANCE", "M1129-X-TRUST") else "required"
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True,
        "machine_eligibility": machine, "human_source_eligibility": human_eligible,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if md == "not_applicable" else ("release_overlay_not_proof_premise" if md == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1129/ObligationTree.lean#poissonFormulaTarget_of_analyticPackage" if oid == "M1129-T-ASSEMBLE" else None})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [o["obligation_id"] for o in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1129-OBLIGATION_TREE", "theorem_id": "THM-M-1129",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; construction-plus-uniqueness route selected before proof closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": "M1129-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids,
      "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
      "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
      "required_readable": ids,
      "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for (oid, kind, human, formal, output, risk, hd, md, budget), obligation in zip(specs, obligations):
    nodes.append({"node_id": "THM-M-1129-" + oid.removeprefix("M1129-"), "obligation_id": oid, "kind": kind,
      "human_statement": human, "formal_target": formal, "output": output, "human_debt": hd, "machine_debt": md,
      "readability_debt": "R3", "evidence_ids": ["lean:conditional-composition"] if oid == "M1129-T-ASSEMBLE" else [],
      "source_crosswalk_id": "not-applicable" if obligation["human_source_eligibility"] == "not_applicable" else "source-pinpoint-pending",
      "provenance_id": "local-poisson-composition-body" if oid == "M1129-T-ASSEMBLE" else "none",
      "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
      "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
      "computation_record": "none; no oracle or numerical experiment is credited", "step_budget": budget,
      "semantic_step_ledger": {"premises": "The exact formal context plus children named by incoming proof composition.",
        "inference": human, "output": output, "outgoing_use": "Used only by the declared parent composition or a non-proof support edge."},
      "public_readable_target": "Stage1_Instances/THM-M-1129/obligation-tree.md#" + oid.lower(),
      "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or conditional interface only; no unresolved analytic claim is asserted.",
      "task_ids": ["S56-M-1129-OBLIGATION_TREE", "S56-M-1129-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1129/ObligationTree.lean"] if oid == "M1129-T-ASSEMBLE" else [],
      "owner": "THM-M-1129 proof lane", "reviewer": "independent Stage1 integration lane",
      "validity": {"validated_at": "2026-07-12" if oid == "M1129-T-ASSEMBLE" else None, "review_due": "before proof acceptance",
        "invalidation_inputs": ["Statement.lean", "obligation-registry.json", "anchor_audit.md", "toolchain"], "revocation_state": "open"}})

# Parent -> child proof requirements. Every required-machine obligation is reachable from ROOT.
requirements = {
 "M1129-ROOT": ["M1129-S-DEFS", "M1129-S-DOMAIN", "M1129-S-BOUNDARY", "M1129-S-TRANSPORT", "M1129-T-ASSEMBLE"],
 "M1129-T-ASSEMBLE": ["M1129-T-REPRESENT"],
 "M1129-T-REPRESENT": ["M1129-T-CONSTRUCT", "M1129-L-UNIQUENESS"],
 "M1129-T-CONSTRUCT": ["M1129-C-KERNEL", "M1129-L-DIFF", "M1129-L-PDE", "M1129-L-INITIAL-F", "M1129-L-INITIAL-G"],
 "M1129-C-KERNEL": ["M1129-L-WEIGHT", "M1129-L-DATA"],
 "M1129-L-DIFF": ["M1129-L-WEIGHT", "M1129-L-DATA"],
 "M1129-L-PDE": ["M1129-L-SPATIAL", "M1129-L-TIME"],
}

def graph(edges):
    outgoing = {i: [] for i in ids}; incoming = {i: [] for i in ids}
    for e in edges: outgoing[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_edges = []
for parent, children in requirements.items():
    for child in children:
        stem = "P-" + parent.removeprefix("M1129-") + "-" + child.removeprefix("M1129-")
        req, comp = stem + "-REQ", stem + "-COMP"
        proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp},
                        {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]

refine_edges = [{"edge_id": "R-BOUNDARY-F", "type": "logical_decomposition", "from": "M1129-S-BOUNDARY", "to": "M1129-L-INITIAL-F"},
                {"edge_id": "R-BOUNDARY-G", "type": "logical_decomposition", "from": "M1129-S-BOUNDARY", "to": "M1129-L-INITIAL-G"}]
provenance_edges = [{"edge_id": "PV-ASSEMBLE", "type": "provenance_of", "from": "M1129-X-PROVENANCE", "to": "M1129-T-ASSEMBLE"}]
evidence_edges = [{"edge_id": "EV-COMPOSE", "type": "evidence_for", "from": "M1129-X-TRUST", "to": "M1129-T-ASSEMBLE"}]
trust_edges = [{"edge_id": "TR-ROOT", "type": "trusts", "from": "M1129-ROOT", "to": "M1129-S-FOUNDATION"},
               {"edge_id": "TR-FOUNDATION", "type": "trusts", "from": "M1129-S-FOUNDATION", "to": "M1129-X-TRUST"}]
documentation_edges = [{"edge_id": "D-SOURCE-" + oid, "type": "source_map", "from": oid, "to": "M1129-X-SOURCE"} for oid in ("M1129-ROOT", "M1129-S-BOUNDARY", "M1129-S-TRANSPORT", "M1129-L-WEIGHT", "M1129-L-DIFF", "M1129-L-PDE", "M1129-L-UNIQUENESS")]
documentation_edges += [{"edge_id": "D-DOC-" + oid, "type": "documents", "from": oid, "to": oid} for oid in ids]
workflow_edges = [{"edge_id": "W-" + oid, "type": "workflow_depends_on", "from": oid, "to": "M1129-X-PROVENANCE"} for oid in ("M1129-T-ASSEMBLE", "M1129-T-REPRESENT")]

bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1129-OBLIGATION_TREE", "theorem_id": "THM-M-1129",
 "registry_id": "THM-M-1129-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M1129-ROOT",
 "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes,
 "graphs": {"proof": graph(proof_edges), "refinement": graph(refine_edges), "provenance": graph(provenance_edges),
   "evidence": graph(evidence_edges), "trust": graph(trust_edges), "documentation": graph(documentation_edges), "workflow": graph(workflow_edges)},
 "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False,
   "conditionally_checked_nodes": ["M1129-T-ASSEMBLE"], "remaining_root_cut_set": ["M1129-T-REPRESENT"],
   "reason": "The exact root composition checks only when the complete analytic package is supplied; that package remains M4."}}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

lines = ["# Frozen obligation tree", "", "Registry version 1 freezes 22 semantic obligations before proof execution. The selected route constructs the Poisson expression, proves its PDE and initial-data properties, and uses uniqueness in the exact solution class. All analytic leaves remain open unless explicitly marked below.", "", "| Obligation | Kind | Exact output | H/M/R | Budget |", "|---|---|---|---|---:|"]
for node in nodes:
    lines += [f"<a id=\"{node['obligation_id'].lower()}\"></a>", f"| `{node['obligation_id']}` | {node['kind']} | {node['output']} | {node['human_debt']}/{node['machine_debt']}/{node['readability_debt']} | {node['step_budget']} |"]
lines += ["", "## Proof architecture", "", "`ROOT -> T-ASSEMBLE -> T-REPRESENT -> {T-CONSTRUCT, L-UNIQUENESS}`. Construction expands into kernel well-definedness, differentiation, the wave identity, and both zero-time data obligations. The kernel and differentiation nodes share, without double credit, the singular-weight and data-domination leaves. `L-PDE` expands into separate spatial-Laplacian and second-time-derivative calculations.", "", "`S-BOUNDARY` has logical-decomposition edges to both initial-data leaves. Source, provenance, evidence, trust, documentation, and workflow edges are separate from proof edges and cannot close the root.", "", "## Composition boundary", "", "`poissonFormulaTarget_of_analyticPackage` is kernel checked and consumes an explicit `PoissonAnalyticPackage`, definitionally the exact root. It proves only the child-to-parent interface. It does not prove the analytic package. The first remaining root cut is `M1129-T-REPRESENT`; root debt remains M3 and theorem completion is false.", "", "No node is excluded merely because it is difficult. The source-only and release overlays are root-relevant but are not proof premises. Every planned leaf has a provisional budget at most 100; these budgets freeze granularity and are not R0 evidence."]
(HERE / "obligation-tree.md").write_text("\n".join(lines) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
