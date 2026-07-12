#!/usr/bin/env python3
"""Build the frozen THM-M-0509 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0509-OBLIGATION_TREE"
THEOREM = "THM-M-0509"
PREFIX = "M0509"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


rows = [
    ("ROOT", "root", "critical", "Prove the exact frozen uniform natural-number P + P2 target.", "Stage1Instances.THM_M_0509.ChenTheoremTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Preserve the explicit P2 convention: a prime or a product of two primes, with repetition allowed.", "Stage1Instances.THM_M_0509.{IsP2,ChenTheoremTarget}", "The exact elaborated statement interface."),
    ("S-BOUNDARY", "terminal", "high", "Preserve prime and prime-square inclusion and the exclusion of zero and one.", "Stage1Instances.THM_M_0509.{prime_boundary,prime_square_boundary,zero_not_p2,one_not_p2}", "Checked encoding boundary facts."),
    ("S-FOUNDATION", "certificate", "critical", "Freeze classical logic, choice, analytic estimates, imports, axioms, TCB, and the no-oracle policy.", "planned transitive trust and axiom certificate", "An accepted trust boundary."),
    ("C-REPRESENTATION", "construction", "critical", "Define the representation sequence for even N and the sifted candidates N - p with every range, parity, and coprimality invariant explicit.", "planned Lean representation/sifting construction", "A finite sieve problem whose survivors yield representations."),
    ("S-SIEVE-SETUP", "reduction", "critical", "Select sieve level, weights, exceptional moduli, and local densities uniformly in N and prove all admissibility and positivity side conditions.", "planned weighted-sieve parameter package", "A valid weighted sieve instance for each sufficiently large even N."),
    ("N-DISTRIBUTION", "analytic_lemma", "critical", "Establish the required averaged distribution estimate for primes in arithmetic progressions over the exact modulus and error ranges used by the sieve.", "planned exact distribution estimate", "A uniform bound for the main sieve remainder terms."),
    ("L-WEIGHTED-SIEVE", "core_lemma", "critical", "Apply the weighted lower-bound sieve to the representation sequence, with constants and uniform error terms stated explicitly.", "planned exact weighted lower-bound sieve theorem", "A lower bound for the weighted count of admissible representations."),
    ("L-SWITCHING", "core_lemma", "critical", "Control candidates with three or more prime factors by the switching argument, including all decompositions, cutoffs, and exceptional ranges.", "planned exact switching-principle estimate", "An upper bound for the unwanted weighted contribution."),
    ("L-REMAINDER", "analytic_lemma", "critical", "Combine distribution and auxiliary bilinear remainder estimates and show that their total is smaller than the main term uniformly above one threshold.", "planned exact remainder aggregation theorem", "A quantitatively dominated total error."),
    ("T-POSITIVITY", "terminal", "critical", "Combine the weighted main term, switching bound, and remainder control to obtain a positive admissible representation count for every sufficiently large even N.", "planned exact positivity theorem", "Existence of a surviving representation for each N."),
    ("T-P2-EXTRACTION", "transport", "critical", "Convert a surviving weighted-sieve candidate to the frozen IsP2 predicate, ruling out every residual factor-count and boundary case.", "planned survivor-to-IsP2 theorem", "Prime p and IsP2 a with N = p + a."),
    ("T-ASSEMBLE", "transport", "high", "Choose one uniform threshold and compose the analytic package with P2 extraction into the exact canonical target.", "Stage1Instances.THM_M_0509.root_of_sieve_package", "The exact root, conditional on the still-open sieve package."),
    ("X-SOURCE", "source_boundary", "high", "Map every analytic estimate, constant range, and transition to pinpoint primary-source passages, assumptions, corrections, and an independent review.", "node-specific primary-source crosswalk pending", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory every terminal body, wrapper, import, axiom, TCB component, replay recipe, and evidence receipt.", "planned machine-derived provenance closure", "Release provenance coverage without mathematical proof credit."),
]

checked = {"S-DEFINITIONS", "S-BOUNDARY", "T-ASSEMBLE"}
source_na = {"S-DEFINITIONS", "S-BOUNDARY", "S-FOUNDATION", "X-PROVENANCE"}
obligations = []
nodes = []
for short, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{short}"
    machine = "not_applicable" if short == "X-SOURCE" else ("informational" if short == "X-PROVENANCE" else "required")
    fp = "lean-expression-sha256:e2c8d3782d80648aa229dab05f90a84506ed5b6f213fa3083e312674aa6c64f7" if short in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if short in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if short == "X-SOURCE" else ("release_provenance_overlay_no_proof_credit" if short == "X-PROVENANCE" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0509/ObligationTree.lean#root_of_sieve_package" if short == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{short}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if short in checked else ("M4" if short == "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if short in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-handoff" if short == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib/classical-policy-and-analytic-imports-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no experiment, oracle, or numerical sample may close this node",
        "step_budget": 100 if short in {"N-DISTRIBUTION", "L-WEIGHTED-SIEVE", "L-SWITCHING", "L-REMAINDER"} else 40,
        "semantic_step_ledger": {
            "premises": "Only the declared proof-requirement children and the exact formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only a declared typed parent edge may consume this output as proof input."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0509/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or checked conditional handoff only; no unlisted premise and no root closure.",
        "task_ids": [ITEM, "S56-M-0509-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0509/ObligationTree.lean"] if short == "T-ASSEMBLE" else [],
        "owner": "THM-M-0509 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if short in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if short in checked else "open"}
    })

denominator = digest(obligations)
ids = [o["obligation_id"] for o in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact frozen P + P2 statement and bounded formal-anchor audit; classical weighted-sieve architecture is provisional pending pinpoint primary-source review; eligibility was assigned before closure inspection.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked), "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; no analytic sieve package, primary-source acceptance, audit completion, or Chen-theorem proof."
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "ROOT": ["T-ASSEMBLE"],
    "T-ASSEMBLE": ["T-P2-EXTRACTION"],
    "T-P2-EXTRACTION": ["T-POSITIVITY"],
    "T-POSITIVITY": ["L-WEIGHTED-SIEVE", "L-SWITCHING", "L-REMAINDER"],
    "L-WEIGHTED-SIEVE": ["C-REPRESENTATION", "S-SIEVE-SETUP", "N-DISTRIBUTION"],
    "L-SWITCHING": ["C-REPRESENTATION", "S-SIEVE-SETUP", "N-DISTRIBUTION"],
    "L-REMAINDER": ["N-DISTRIBUTION", "S-SIEVE-SETUP"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        p, c = f"{PREFIX}-{parent}", f"{PREFIX}-{child}"
        req, comp = f"REQ-{p}-{c}", f"CMP-{c}-{p}"
        proof.extend([edge(req, p, "proof_requires", c, comp), edge(comp, c, "composes", p, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-ANALYTIC", f"{PREFIX}-N-DISTRIBUTION", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-SWITCH", f"{PREFIX}-L-SWITCHING", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-N-DISTRIBUTION")],
    "workflow": [edge("FLOW-ASSEMBLE", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-P2-EXTRACTION"), edge("FLOW-POS", f"{PREFIX}-T-P2-EXTRACTION", "workflow_depends_on", f"{PREFIX}-T-POSITIVITY"), edge("FLOW-PROV", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-P2-EXTRACTION"], "composition_certificates": ["Stage1Instances.THM_M_0509.root_of_sieve_package"], "reason": "The exact-root handoff is conditional; the complete analytic sieve package and its child obligations remain open."}
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{PREFIX}-{short}", "obligation_id": f"{PREFIX}-{short}", "command": "python3 Stage1_Instances/THM-M-0509/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for short, *_ in rows]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
