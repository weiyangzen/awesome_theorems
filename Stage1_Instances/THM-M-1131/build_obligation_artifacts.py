#!/usr/bin/env python3
"""Build the frozen THM-M-1131 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1131-OBLIGATION_TREE"
THEOREM = "THM-M-1131"
PREFIX = "M1131"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# id, kind, risk, machine eligibility, source eligibility, claim, target, output, budget
SPECS = [
    ("ROOT", "root", "critical", "required", "required", "The frozen homogeneous isotropic Fourier heat-conduction implication.", "Stage1Instances.THM_M_1131.Statement", "The exact canonical proposition.", 20),
    ("S-DEFS", "definition", "high", "required", "not_applicable", "Fix coordinate space, gradient, divergence, Laplacian, and time derivative exactly as elaborated.", "Stage1Instances.THM_M_1131.{Space,gradient,divergence,laplacian,timeDerivative}", "The operator interface used by every proof node.", 30),
    ("S-DOMAIN", "definition", "high", "required", "required", "Preserve positive dimension, material regimes, arbitrary fields, source, point, and time without adding regularity assumptions.", "Stage1Instances.THM_M_1131.Statement", "The complete quantified context.", 25),
    ("S-FOUNDATION", "certificate", "critical", "required", "not_applicable", "Audit the actual axioms, imported declarations, compiled artifacts, and Lean/mathlib trust boundary.", "planned transitive axiom and trust report", "An accepted foundation and TCB profile.", 40),
    ("N-FLUX", "normalization", "critical", "required", "required", "Rewrite the heat-flux field pointwise using the Fourier constitutive hypothesis.", "planned theorem rewriting heatFlux t to -conductivity * gradient (temperature t)", "A divergence expression whose field is the negative constant multiple of the gradient.", 35),
    ("L-COORD", "core_lemma", "critical", "required", "required", "For each coordinate, move constant scalar multiplication and negation through the Frechet derivative evaluation.", "planned coordinate fderiv theorem using fderiv_fun_const_smul and fderiv_fun_neg", "Each diagonal derivative equals -conductivity times the corresponding second derivative.", 70),
    ("L-FINSUM", "lemma", "high", "required", "required", "Move negation and constant multiplication through the finite coordinate sum.", "planned Finset sum normalization theorem", "Divergence of the Fourier field equals -conductivity times the Laplacian.", 35),
    ("B-ZERO", "branch", "high", "required", "required", "Cover zero conductivity without cancellation or invertibility assumptions.", "planned exact zero-conductivity branch", "The flux-divergence identity when conductivity = 0.", 25),
    ("B-NONZERO", "branch", "high", "required", "required", "Cover nonzero conductivity using only derivative identities justified by invertibility over Real.", "planned exact nonzero-conductivity branch", "The flux-divergence identity when conductivity != 0.", 50),
    ("T-FLUXDIV", "terminal", "critical", "required", "required", "Assemble the constitutive rewrite and derivative algebra into the universal flux-divergence package.", "Stage1Instances.THM_M_1131.FluxDivergencePackage (planned body)", "FluxDivergencePackage.", 30),
    ("L-BALANCE", "lemma", "normal", "required", "required", "Substitute the flux-divergence equality into local energy balance at a fixed point.", "Stage1Instances.THM_M_1131.heatEquation_of_balance_of_fluxDivergence", "The fixed-point heat-equation conclusion.", 10),
    ("T-ASSEMBLE", "transport", "high", "required", "required", "Instantiate the universal flux package and compose it with balance into the exact root.", "Stage1Instances.THM_M_1131.statement_of_fluxDivergencePackage", "Statement conditional on FluxDivergencePackage.", 15),
    ("X-SOURCE", "terminal", "high", "not_applicable", "required", "Map the constitutive law, energy balance, material regime, and algebraic derivation to pinpoint primary sources.", "human source boundary; no Lean proposition", "Reviewed node-level source crosswalk.", 60),
    ("X-PROVENANCE", "certificate", "critical", "informational", "not_applicable", "Classify terminal bodies, supporting mathlib declarations, wrappers, imports, and their origins.", "planned content-addressed provenance closure", "Release provenance coverage without mathematical proof credit.", 50),
]


def oid(short):
    return f"{PREFIX}-{short}"


statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {oid("S-DEFS"), oid("S-DOMAIN"), oid("L-BALANCE"), oid("T-ASSEMBLE")}
obligations = []
nodes = []
for short, kind, risk, machine, human, claim, target, output, budget in SPECS:
    obligation = oid(short)
    fingerprint = (
        "lean-expression-sha256:01b3e91bb9da602483ca5af9d00787c8b264c6afb530c8b4b268c4c49c60ee99"
        if short in {"ROOT", "S-DOMAIN"}
        else "planned:v1:sha256:" + digest([obligation, kind, claim, target, output])
    )
    terminal = None
    if short == "L-BALANCE":
        terminal = "local:Stage1_Instances/THM-M-1131/ObligationTree.lean#heatEquation_of_balance_of_fluxDivergence"
    elif short == "T-ASSEMBLE":
        terminal = "local:Stage1_Instances/THM-M-1131/ObligationTree.lean#statement_of_fluxDivergencePackage"
    obligations.append({
        "obligation_id": obligation, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_provenance_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": terminal,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{short}", "obligation_id": obligation, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if obligation in checked else ("M3" if short == "ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": "local-conditional-composition" if terminal else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, numerical solver, or empirical result receives proof credit",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the exact formal context and incoming proof-required children.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1131/obligation-tree.md#{obligation.lower()}",
        "validation_spec_id": f"VAL-{obligation}",
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-1131-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1131/ObligationTree.lean"] if terminal else [],
        "owner": "THM-M-1131 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if obligation in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if obligation in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; status-independent pointwise derivative architecture with explicit zero/nonzero conductivity branches.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"], "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [oid("X-PROVENANCE")]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the flux-divergence package, H0 source review, root proof, and theorem completion remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": oid(source), "type": kind, "to": oid(target)}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "ROOT": ["T-ASSEMBLE"], "T-ASSEMBLE": ["T-FLUXDIV", "L-BALANCE"],
    "T-FLUXDIV": ["N-FLUX", "L-FINSUM", "B-ZERO", "B-NONZERO"],
    "N-FLUX": ["L-COORD"], "B-NONZERO": ["L-COORD"], "B-ZERO": ["L-FINSUM"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{PREFIX}-{parent}-{child}"
        comp = f"CMP-{PREFIX}-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "ROOT", "logical_decomposition", "S-DEFS"), edge("REF-ROOT-DOMAIN", "ROOT", "logical_decomposition", "S-DOMAIN")],
    "provenance": [edge("SRC-FLUX", "N-FLUX", "source_map", "X-SOURCE"), edge("SRC-BALANCE", "L-BALANCE", "source_map", "X-SOURCE"), edge("PROV-ROOT", "X-PROVENANCE", "provenance_of", "ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "ROOT", "trusts", "S-FOUNDATION"), edge("TRUST-PROV", "ROOT", "trusts", "X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "S-DEFS", "documents", "ROOT"), edge("DOC-SOURCE", "X-SOURCE", "documents", "T-FLUXDIV")],
    "workflow": [edge("FLOW-ASSEMBLE-FLUX", "T-ASSEMBLE", "workflow_depends_on", "T-FLUXDIV"), edge("FLOW-ASSEMBLE-BALANCE", "T-ASSEMBLE", "workflow_depends_on", "L-BALANCE"), edge("FLOW-PROV-ASSEMBLE", "X-PROVENANCE", "workflow_depends_on", "T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1131-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": oid("ROOT"), "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-FLUXDIV")], "composition_certificates": ["Stage1Instances.THM_M_1131.heatEquation_of_balance_of_fluxDivergence", "Stage1Instances.THM_M_1131.statement_of_fluxDivergencePackage"], "reason": "Both checked declarations are conditional; FluxDivergencePackage has no proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid(short)}", "obligation_id": oid(short), "command": "python3 Stage1_Instances/THM-M-1131/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for short, *_ in SPECS]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
