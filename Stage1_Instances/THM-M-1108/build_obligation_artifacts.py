#!/usr/bin/env python3
"""Build the frozen THM-M-1108 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1108-OBLIGATION_TREE"
THEOREM = "THM-M-1108"

specs = [
    ("M1108-ROOT", "root", "Exact canonical BDJ pointwise CDF limit.", "Stage1Instances.THM_M_1108.CanonicalStatement", "CanonicalStatement.", "critical", "required", "required", 5),
    ("M1108-S-DEFS", "definition", "Freeze uniform permutations, strict LIS, the normalized CDF, and the source Tracy-Widom predicate.", "Stage1Instances.THM_M_1108.{lisLength,normalizedLISCDF,IsTracyWidomCDF}", "Exact statement objects and binder order.", "high", "required", "not_applicable", 20),
    ("M1108-S-BOUNDARY", "normalization", "Preserve N = 0, every real threshold, strict subsequences, and the exact 2 sqrt(N), N^(1/6) normalization.", "boundary package for CanonicalStatement", "No shifted-index or altered-scaling theorem enters the route.", "high", "required", "required", 30),
    ("M1108-S-FOUNDATION", "certificate", "Audit classical choice, quotients, improper integrals, derivatives, infinite sums, imports, and TCB.", "planned transitive axiom/trust report", "Accepted foundation profile for eventual bodies.", "critical", "required", "not_applicable", 40),
    ("M1108-N-POISSON", "normalization", "Poissonize permutation size with parameter n and translate the LIS threshold without changing centering or scale.", "Stage1Instances.THM_M_1108.poissonizedLISCDF", "Exact Poissonized finite-permutation CDF.", "critical", "required", "required", 60),
    ("M1108-C-RSK", "construction", "Construct Robinson-Schensted and identify LIS length with the first row of the associated Young diagram.", "planned Lean RSK bijection and first-row identity", "Permutation counts become Plancherel/Young-diagram counts.", "critical", "required", "required", 100),
    ("M1108-L-TOEPLITZ", "bridge", "Convert the Poissonized first-row distribution to the source Toeplitz determinant/orthogonal-polynomial representation.", "planned exact determinant representation", "Analytic representation of poissonizedLISCDF.", "critical", "required", "required", 100),
    ("M1108-C-RHP", "construction", "Set up the source Riemann-Hilbert problem and its steepest-descent transformations with all contour and solvability invariants.", "planned Lean RHP deformation package", "Normalized local/global parametrices and error problem.", "critical", "required", "required", 100),
    ("M1108-L-PAINLEVE", "core_lemma", "Identify the edge parametrix and limiting determinant with the Hastings-McLeod Painleve II formula defining F.", "planned RHP-to-IsTracyWidomCDF identification", "The exact source-specified Tracy-Widom limit.", "critical", "required", "required", 100),
    ("M1108-L-UNIFORM-ERROR", "core_lemma", "Prove uniform error estimates in the edge-scaling window sufficient for convergence at every fixed t.", "planned uniform steepest-descent estimates", "Uniform analytic control of the Poissonized CDF.", "critical", "required", "required", 100),
    ("M1108-T-POISSONIZED", "terminal", "Compose RSK, determinant, RHP, Painleve, and error estimates into pointwise Poissonized convergence.", "Stage1Instances.THM_M_1108.PoissonizedAsymptotics", "PoissonizedAsymptotics.", "critical", "required", "required", 40),
    ("M1108-L-MONOTONE", "lemma", "Establish the monotonic comparison between fixed-size LIS events at nearby sizes.", "planned fixed-size monotonicity/coupling lemma", "Two-sided comparison needed for de-Poissonization.", "critical", "required", "required", 80),
    ("M1108-L-POISSON-TAIL", "lemma", "Control Poisson size tails in an edge-compatible window with errors vanishing after normalization.", "planned Poisson concentration estimates", "Negligible out-of-window probability.", "critical", "required", "required", 80),
    ("M1108-T-DEPOISSONIZE", "terminal", "Use monotonicity, tail control, and uniform analytic estimates to transfer the Poissonized limit to fixed N.", "Stage1Instances.THM_M_1108.DePoissonizationTransfer", "DePoissonizationTransfer.", "critical", "required", "required", 80),
    ("M1108-T-ASSEMBLE", "transport", "Consume both terminal packages and yield the exact canonical root.", "Stage1Instances.THM_M_1108.canonicalStatement_of_poissonized_depoissonized", "CanonicalStatement conditional on both packages.", "high", "required", "required", 8),
    ("M1108-X-SOURCE", "terminal", "Map every material source transition to reviewed theorem/page/assumption/errata records.", "human source boundary; no Lean proposition", "Node-level H evidence without machine credit.", "high", "not_applicable", "required", 60),
    ("M1108-X-PROVENANCE", "certificate", "Inventory terminal bodies, wrappers, imports, generated artifacts, axioms, and replay evidence.", "planned provenance closure", "Content-addressed provenance without proof credit.", "critical", "informational", "not_applicable", 50),
    ("M1108-X-TRUST", "certificate", "Record kernel, executable, automation, computation, dependency, and independent-runner boundaries.", "planned release trust record", "Replayable trust boundary without proof credit.", "critical", "informational", "not_applicable", 50),
]

def planned_fp(oid, target):
    if oid == "M1108-ROOT":
        return "lean-expression-sha256:77a8060cec0d52904b4e490aba897941da35e272082be2de219d588100ce15c5"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

closed = {"M1108-T-ASSEMBLE"}
obligations, nodes = [], []
for oid, kind, claim, target, output, risk, machine, human, budget in specs:
    body = "local:Stage1_Instances/THM-M-1108/ObligationTree.lean#canonicalStatement_of_poissonized_depoissonized" if oid in closed else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": planned_fp(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": ("support_overlay_no_machine_proof_credit" if machine == "informational" else "human_source_boundary_only" if machine == "not_applicable" else None),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-1108-" + oid.removeprefix("M1108-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in closed else ("M3" if oid == "M1108-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-dependent-type-theory/classical-analysis-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; numerical RHP/Painleve evaluation receives no proof credit",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared reciprocal composition or non-proof support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1108/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-1108-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1108/ObligationTree.lean"] if oid in closed else [],
        "owner": "THM-M-1108 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in closed else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated source statement and immutable anchor audit; Poissonization/RSK/RHP/de-Poissonization route selected before proof closure was inspected.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1108-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(closed), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; both terminal mathematical packages, root closure, source acceptance, and theorem completion remain open.",
}

proof_pairs = [
    ("M1108-ROOT", "M1108-T-ASSEMBLE"), ("M1108-T-ASSEMBLE", "M1108-T-POISSONIZED"), ("M1108-T-ASSEMBLE", "M1108-T-DEPOISSONIZE"),
    ("M1108-T-POISSONIZED", "M1108-N-POISSON"), ("M1108-T-POISSONIZED", "M1108-C-RSK"), ("M1108-T-POISSONIZED", "M1108-L-TOEPLITZ"), ("M1108-T-POISSONIZED", "M1108-C-RHP"), ("M1108-T-POISSONIZED", "M1108-L-PAINLEVE"), ("M1108-T-POISSONIZED", "M1108-L-UNIFORM-ERROR"),
    ("M1108-T-DEPOISSONIZE", "M1108-L-MONOTONE"), ("M1108-T-DEPOISSONIZE", "M1108-L-POISSON-TAIL"), ("M1108-T-DEPOISSONIZE", "M1108-L-UNIFORM-ERROR"),
]
proof = []
for parent, child in proof_pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

other = {
    "refinement": [("REF-ROOT-DEFS", "M1108-ROOT", "logical_decomposition", "M1108-S-DEFS"), ("REF-ROOT-BOUNDARY", "M1108-ROOT", "logical_decomposition", "M1108-S-BOUNDARY")],
    "provenance": [("SRC-RHP", "M1108-C-RHP", "source_map", "M1108-X-SOURCE"), ("SRC-DEPOISSON", "M1108-T-DEPOISSONIZE", "source_map", "M1108-X-SOURCE"), ("PROV-ROOT", "M1108-X-PROVENANCE", "provenance_of", "M1108-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUND", "M1108-ROOT", "trusts", "M1108-S-FOUNDATION"), ("TRUST-RELEASE", "M1108-ROOT", "trusts", "M1108-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1108-X-SOURCE", "documents", "M1108-ROOT"), ("DOC-BOUNDARY", "M1108-S-BOUNDARY", "documents", "M1108-T-DEPOISSONIZE")],
    "workflow": [("FLOW-POISSON", "M1108-T-POISSONIZED", "workflow_depends_on", "M1108-C-RSK"), ("FLOW-DEPOISSON", "M1108-T-DEPOISSONIZE", "workflow_depends_on", "M1108-T-POISSONIZED"), ("FLOW-PROV", "M1108-X-PROVENANCE", "workflow_depends_on", "M1108-T-ASSEMBLE")],
}

def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for e in cooked:
        outgoing.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}

graphs = {"proof": graph(proof), **{name: graph(edges) for name, edges in other.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1108-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M1108-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(closed), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1108-T-POISSONIZED", "M1108-T-DEPOISSONIZE"], "composition_certificates": ["Stage1Instances.THM_M_1108.canonicalStatement_of_poissonized_depoissonized"], "reason": "The composition term is checked, but both mathematical package premises remain open."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"generated {len(ids)} obligations; denominator {digest}")
