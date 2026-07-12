#!/usr/bin/env python3
"""Deterministically build the THM-M-1133 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1133-OBLIGATION_TREE"
THEOREM = "THM-M-1133"
PREFIX = "M1133"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def planned(text: str) -> str:
    return "planned:v1:sha256:" + sha(text.encode())


# id, kind, claim, formal target, output, H, M, risk, source eligibility, budget
ROWS = [
    ("M1133-ROOT", "root", "The exact classical weak heat-equation maximum principle frozen in Statement.lean.", "Stage1Instances.THM_M_1133.HeatEquationWeakMaximumPrinciple", "A boundary maximizer for every classical caloric function on the closed cylinder.", "H2", "M3", "critical", "required", 40),
    ("M1133-S-INTERFACE", "definition", "Preserve the closed cylinder, parabolic boundary, coordinate Laplacian, regularity, and forward heat sign convention.", "Stage1Instances.THM_M_1133.{ClosedCylinder,ParabolicBoundary,spatialLaplacian,IsClassicalCaloricOn}", "The exact elaborated vocabulary of the root.", "H2", "M0-L", "critical", "required", 40),
    ("M1133-S-BOUNDARY", "terminal", "Prove compactness and nonemptiness of the closed cylinder and characterize points outside the parabolic boundary, including the terminal-time interior case.", "planned cylinder compactness/nonemptiness and boundary-membership declarations", "A compact nonempty domain and an exhaustive boundary/interior split.", "H2", "M4", "high", "required", 80),
    ("M1133-S-FOUNDATION", "certificate", "Audit classical extrema, choice, imports, transitive axioms, TCB, and the no-oracle boundary.", "planned transitive axiom and TCB certificate", "An accepted trust boundary for every terminal body.", "H2", "M4", "critical", "not_applicable", 40),
    ("M1133-N-SUBSOLUTION", "normalization", "Generalize the equality-form heat equation to the forward subsolution inequality without changing domain, regularity, or boundary.", "Stage1Instances.THM_M_1133.{IsClassicalSubcaloricOn,WeakSubsolutionMaximumPrinciple}", "The exact subsolution proposition used by the analytic proof.", "H2", "M0-L", "high", "required", 40),
    ("M1133-N-PERTURB", "construction", "For epsilon > 0 form v(x,t)=u(x,t)-epsilon*t and prove strict forward subcaloricity, continuity, and unchanged spatial regularity.", "planned strict perturbation construction and invariant package", "A strict subsolution converging uniformly back to u.", "H2", "M4", "critical", "required", 100),
    ("M1133-L-EXTREMUM", "core_lemma", "Use compactness and continuity to obtain a global maximizer of the perturbed function on the closed cylinder.", "planned IsCompact.exists_isMaxOn bridge", "A selected cylinder maximizer with global comparison.", "H2", "M4", "high", "required", 60),
    ("M1133-B-LOCATION", "branch", "Split the selected maximizer into parabolic-boundary membership or a spatial-interior point at positive time, and prove exhaustiveness.", "planned parabolic-boundary/interior dichotomy", "Either the desired boundary witness or the forbidden interior branch.", "H2", "M4", "critical", "required", 80),
    ("M1133-L-SPATIAL", "core_lemma", "At a spatial interior maximum prove vanishing first spatial derivative and nonpositive coordinate second derivatives, hence nonpositive Laplacian.", "planned local-maximum Hessian/Laplacian sign package", "Delta_x v is nonpositive at the selected interior point.", "H2", "M4", "critical", "required", 100),
    ("M1133-B-TIME", "branch", "Split positive time into t<T and t=T, preserving the one-sided cylinder maximum information in both cases.", "planned time endpoint dichotomy", "An exhaustive interior-time or terminal-time branch.", "H2", "M4", "high", "required", 60),
    ("M1133-L-TIME", "core_lemma", "At the cylinder maximizer prove the time derivative is zero for 0<t<T and nonnegative for t=T using the left-hand maximum inequality.", "planned temporal derivative sign package", "partial_t v is nonnegative at every nonboundary maximizer.", "H2", "M4", "critical", "required", 100),
    ("M1133-T-STRICT", "terminal", "Combine the temporal and spatial derivative signs to contradict the strict subsolution inequality at a nonboundary maximizer.", "planned strict-subsolution maximum-on-boundary theorem", "Every perturbed strict subsolution has a boundary maximizer.", "H2", "M4", "critical", "required", 80),
    ("M1133-T-LIMIT", "terminal", "Let epsilon decrease to zero and transfer the perturbed boundary estimate to the original subsolution without assuming a convergent choice of maximizers.", "planned epsilon inequality limit theorem", "The full weak subsolution maximum principle.", "H2", "M4", "critical", "required", 100),
    ("M1133-T-ASSEMBLE", "transport", "Specialize the subsolution principle to heat-operator equality and compose it into the exact root.", "Stage1Instances.THM_M_1133.root_of_subsolutionMaximumPrinciple", "The exact canonical target, conditional only on the open subsolution package.", "H2", "M0-L", "high", "required", 30),
    ("M1133-X-SOURCE", "terminal", "Pinpoint every proof transition in a primary PDE source, map assumptions, check errata, and obtain independent source review.", "human-source ledger and independent review", "Accepted human-source coverage.", "H2", "M5", "high", "required", 100),
    ("M1133-X-PROVENANCE", "certificate", "Inventory terminal proof bodies, wrappers, imports, axioms, automation, and replay boundaries.", "planned proof-body provenance and trust closure", "Release provenance coverage without proof credit.", "H2", "M4", "critical", "not_applicable", 60),
]

statement_hash = sha((HERE / "Statement.lean").read_bytes())
audit_hash = sha((HERE / "anchor-audit.json").read_bytes())
root_expression = json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_sha256"]
obligations = []
for oid, kind, claim, target, output, h, m, risk, source, budget in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-expression-sha256:" + root_expression if oid == "M1133-ROOT" else planned(target + "\n" + claim),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": "not_applicable" if oid == "M1133-X-SOURCE" else ("informational" if oid == "M1133-X-PROVENANCE" else "required"),
        "human_source_eligibility": source, "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"M1133-X-SOURCE": "human_source_boundary_only", "M1133-X-PROVENANCE": "release_overlay_no_proof_credit"}.get(oid),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1133/ObligationTree.lean#root_of_subsolutionMaximumPrinciple" if oid == "M1133-T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [row[0] for row in ROWS]
closed = ["M1133-S-INTERFACE", "M1133-N-SUBSOLUTION", "M1133-T-ASSEMBLE"]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated classical cylinder statement and bounded anchor audit; the architecture freezes the standard strict-perturbation proof before closure metrics are observed.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": audit_hash,
    "root_obligation_id": "M1133-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1133-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": closed, "root_machine_debt": "M3"},
    "status_boundary": "The frozen registry and conditional bridge do not prove the subsolution maximum principle or close the root.",
}

nodes = []
for oid, kind, claim, target, output, h, m, risk, source, budget in ROWS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX + "-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": h, "machine_debt": m, "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "evans-section-2.3-pinpoint-review-pending" if source == "required" else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1133-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical-analysis/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no solver, numerical PDE computation, or oracle may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the exact proof children declared in the proof graph and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared reciprocal composition edge or a typed non-proof edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1133/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.",
        "task_ids": [ITEM, "S56-M-1133-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1133/ObligationTree.lean"] if oid in closed else [],
        "owner": "THM-M-1133 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if m == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if m == "M0-L" else "open"},
    })

requirements = [
    ("M1133-ROOT", "M1133-T-ASSEMBLE"), ("M1133-T-ASSEMBLE", "M1133-T-LIMIT"),
    ("M1133-T-LIMIT", "M1133-T-STRICT"), ("M1133-T-LIMIT", "M1133-N-PERTURB"),
    ("M1133-T-STRICT", "M1133-L-EXTREMUM"), ("M1133-T-STRICT", "M1133-B-LOCATION"),
    ("M1133-T-STRICT", "M1133-L-SPATIAL"), ("M1133-T-STRICT", "M1133-B-TIME"),
    ("M1133-T-STRICT", "M1133-L-TIME"), ("M1133-L-EXTREMUM", "M1133-S-BOUNDARY"),
]
proof_edges = []
for parent, child in requirements:
    req, cmp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": cmp}, {"edge_id": cmp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

edge_sets = {
    "proof": proof_edges,
    "refinement": [
        {"edge_id": "REF-ROOT-INTERFACE", "from": "M1133-ROOT", "type": "logical_decomposition", "to": "M1133-S-INTERFACE"},
        {"edge_id": "REF-ROOT-SUBSOLUTION", "from": "M1133-ROOT", "type": "logical_decomposition", "to": "M1133-N-SUBSOLUTION"},
    ],
    "provenance": [
        {"edge_id": "SRC-ROOT", "from": "M1133-ROOT", "type": "source_map", "to": "M1133-X-SOURCE"},
        {"edge_id": "PROV-ROOT", "from": "M1133-X-PROVENANCE", "type": "provenance_of", "to": "M1133-ROOT"},
    ],
    "evidence": [],
    "trust": [{"edge_id": "TRUST-FOUND", "from": "M1133-ROOT", "type": "trusts", "to": "M1133-S-FOUNDATION"}, {"edge_id": "TRUST-PROV", "from": "M1133-ROOT", "type": "trusts", "to": "M1133-X-PROVENANCE"}],
    "documentation": [{"edge_id": "DOC-SOURCE", "from": "M1133-X-SOURCE", "type": "documents", "to": "M1133-ROOT"}],
    "workflow": [{"edge_id": f"FLOW-{parent}-{child}", "from": parent, "type": "workflow_depends_on", "to": child} for parent, child in requirements],
}
graphs = {}
for name, edges in edge_sets.items():
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    graphs[name] = {"edges": edges, "out": out, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1133-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1133-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": closed, "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1133-T-LIMIT"], "composition_certificates": ["Stage1Instances.THM_M_1133.caloric_isSubcaloric", "Stage1Instances.THM_M_1133.root_of_subsolutionMaximumPrinciple"], "reason": "The exact equality-to-subsolution transport is checked, but the root-critical weak subsolution maximum package remains M4."},
}

recipes = [{
    "recipe_id": node["validation_spec_id"], "cwd": "repository root",
    "argv": ["python3", "Stage1_Instances/THM-M-1133/check_obligation_tree.py"],
    "env_allowlist": {"LANG": "C.UTF-8", "TZ": "Asia/Shanghai"}, "timeout_seconds": 120,
    "network_policy": "denied", "expected_exit": 0,
    "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "capture exact output; release receipt pending"}],
    "covered_obligation_ids": [node["obligation_id"]],
    "covered_declarations": [node["formal_target"]] if node["machine_debt"] == "M0-L" else [],
} for node in nodes]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "These recipes are structured warm local checks, not release receipts or independent validation."}

for filename, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / filename).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")

intake = json.loads((HERE / "intake.json").read_text())
intake["obligation_registry_hash"] = "sha256:" + denominator
(HERE / "intake.json").write_text(json.dumps(intake, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1133 frozen obligation tree", "", "Registry v1 freezes the standard strict-perturbation architecture. Open debt is intentional; this is not a proof-completion claim.", ""]
for row, node in zip(ROWS, nodes):
    oid = row[0]
    lines += [f"## {oid}", "", f"**Claim:** {node['human_statement']}", "", f"**Role:** supplies `{node['output']}` through the typed graph.", "", f"**Formal target:** `{node['formal_target']}`", "", f"**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `{node['output']}`; budget `{node['step_budget']}` substantive steps.", "", f"**Boundary and status:** `[{node['human_debt']}, {node['machine_debt']}, {node['readability_debt']}]`. {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"wrote {len(ids)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {denominator}")
