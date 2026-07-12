#!/usr/bin/env python3
"""Build the frozen THM-M-0452 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0452-OBLIGATION_TREE"
THEOREM = "THM-M-0452"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M0452-ROOT", "root", "critical", "Construct the exact normalized Neron-Tate pairing package for every elliptic curve over every number field.", "Stage1Instances.THM_M_0452.NeronTatePairingTarget", "The exact canonical proposition."),
    ("M0452-S-POINTS", "definition", "high", "Retain mathlib's elliptic affine point group, identity x-coordinate, scalar actions, torsion subgroup, and torsion quotient.", "Stage1Instances.THM_M_0452.{xHeight,NeronTatePairingTarget}", "The exact point and quotient substrate."),
    ("M0452-S-NORMALIZATION", "normalization", "critical", "Fix xHeight, the factor one half, the 4^(-n) doubling limit, and bounded comparison with xHeight/2.", "Stage1Instances.THM_M_0452.NeronTatePairingPackage", "The frozen height and polarization conventions."),
    ("M0452-S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotients, real topology, imports, axioms, TCB, and the no-oracle computation policy.", "planned transitive foundation and trust report", "An accepted trust boundary."),
    ("M0452-H-NAIVE", "construction", "critical", "Develop the logarithmic naive x-height estimates needed under point addition and duplication.", "planned pinned-mathlib height estimate package", "Uniform local/global estimates for xHeight."),
    ("M0452-H-DUPLICATION", "core_lemma", "critical", "Prove the duplication recurrence with a curve-dependent uniformly bounded error.", "planned |xHeight (2 • P) - 4*xHeight P| bound", "A summable error sequence for iterated doubling."),
    ("M0452-H-CAUCHY", "core_lemma", "critical", "Show the normalized doubling-height sequence is Cauchy and converges in Real.", "planned canonical-height convergence theorem", "Existence of the normalized height limit."),
    ("M0452-H-LIMIT", "construction", "critical", "Define canonicalHeight from the limit and prove the exact limit_formula and bounded_difference fields.", "Stage1Instances.THM_M_0452.CanonicalHeightCoreTarget", "A canonical-height core for each curve."),
    ("M0452-Q-QUADRATIC", "core_lemma", "critical", "Derive h(nP)=n^2 h(P), evenness, and the exact parallelogram law from the limiting construction.", "planned canonical-height quadraticity package", "The quadratic identities used by polarization."),
    ("M0452-P-POLARIZATION", "construction", "high", "Define the one-half polarization and prove symmetry and self-pairing with the frozen normalization.", "planned polarization construction", "The pairing formula, symmetry, and diagonal identity."),
    ("M0452-P-ADDITIVITY", "core_lemma", "critical", "Use the parallelogram law to prove additivity in both arguments without assuming bilinearity.", "planned polarization additivity theorem", "Additive pairing laws in both arguments."),
    ("M0452-P-ZSMUL", "transport", "high", "Extend additivity through zero, positive, and negative multiples to both integer scalar laws.", "planned zsmul transport theorem", "The exact Z-bilinearity fields."),
    ("M0452-P-ASSEMBLE", "terminal", "high", "Assemble polarization, symmetry, additivity, integer scalar laws, and diagonal identity.", "Stage1Instances.THM_M_0452.PolarizationCoreTarget", "A polarization core over every canonical-height core."),
    ("M0452-K-NONNEG", "core_lemma", "critical", "Prove nonnegativity of canonical height over number fields.", "planned canonical-height nonnegativity theorem", "Nonnegative self-pairings."),
    ("M0452-K-TORSION-FWD", "core_lemma", "high", "Show every finite-additive-order point has zero canonical height using quadraticity.", "planned torsion_implies_height_zero", "The forward diagonal-kernel implication."),
    ("M0452-K-BOUNDED-HEIGHT", "core_lemma", "critical", "Prove Northcott finiteness for bounded degree and bounded logarithmic projective height in the needed encoding.", "planned number-field Northcott theorem", "Finiteness of points of bounded naive height."),
    ("M0452-K-ZERO-TORSION", "core_lemma", "critical", "Combine zero canonical height, bounded comparison, and Northcott with the multiples nP to prove finite additive order.", "planned height_zero_implies_torsion", "The reverse diagonal-kernel implication."),
    ("M0452-K-KERNEL", "terminal", "critical", "Combine positivity and both kernel directions into the exact diagonal fields.", "planned diagonal positivity/kernel package", "diagonal_nonnegative and diagonal_kernel."),
    ("M0452-D-WELLDEFINED", "construction", "critical", "Prove the pairing vanishes on torsion in either argument and descends through the quotient.", "planned QuotientAddGroup lift", "A representative-independent quotient pairing."),
    ("M0452-D-POSITIVE", "terminal", "critical", "Transfer diagonal nonnegativity and the torsion-kernel iff to positive definiteness on the quotient.", "Stage1Instances.THM_M_0452.QuotientPairingCoreTarget", "The exact quotient lift and positive-definite fields."),
    ("M0452-T-ASSEMBLE", "transport", "high", "Compose the height, polarization, and quotient packages into the exact canonical statement.", "Stage1Instances.THM_M_0452.root_of_height_polarization_quotient", "The exact root conditional on three explicit packages."),
    ("M0452-X-SOURCE", "terminal", "high", "Map every material limit, quadraticity, positivity, Northcott, and quotient transition to fixed reviewed primary-source passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without proof credit."),
    ("M0452-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, anchors, axioms, TCB, placeholders, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0452-S-POINTS", "M0452-S-NORMALIZATION", "M0452-T-ASSEMBLE"}
source_na = {"M0452-S-POINTS", "M0452-S-NORMALIZATION", "M0452-S-FOUNDATION", "M0452-X-PROVENANCE"}
machine_special = {"M0452-X-SOURCE": "not_applicable", "M0452-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
statement_expression = json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_sha256"]

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-expression-sha256:" + statement_expression if oid == "M0452-ROOT"
                   else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    body = ("local:Stage1_Instances/THM-M-0452/ObligationTree.lean#root_of_height_polarization_quotient"
            if oid == "M0452-T-ASSEMBLE" else None)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0452-" + oid.removeprefix("M0452-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0452-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if body else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no experiment, native_decide, oracle, or solver may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires outputs and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0452/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0452-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0452/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0452 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor inventory", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit; height-limit, quadratic-polarization, torsion-kernel/Northcott, and quotient-descent routes expanded before closure status was observed.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0452-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0452-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no canonical-height construction, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0452-ROOT": ["M0452-T-ASSEMBLE"],
    "M0452-T-ASSEMBLE": ["M0452-H-LIMIT", "M0452-P-ASSEMBLE", "M0452-D-POSITIVE"],
    "M0452-H-LIMIT": ["M0452-H-NAIVE", "M0452-H-DUPLICATION", "M0452-H-CAUCHY"],
    "M0452-P-ASSEMBLE": ["M0452-Q-QUADRATIC", "M0452-P-POLARIZATION", "M0452-P-ADDITIVITY", "M0452-P-ZSMUL", "M0452-K-KERNEL"],
    "M0452-K-KERNEL": ["M0452-K-NONNEG", "M0452-K-TORSION-FWD", "M0452-K-ZERO-TORSION"],
    "M0452-K-ZERO-TORSION": ["M0452-K-BOUNDED-HEIGHT"],
    "M0452-D-POSITIVE": ["M0452-D-WELLDEFINED", "M0452-K-KERNEL"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-POINTS", "M0452-ROOT", "logical_decomposition", "M0452-S-POINTS"), edge("REF-ROOT-NORM", "M0452-ROOT", "logical_decomposition", "M0452-S-NORMALIZATION"), edge("REF-ROOT-FOUND", "M0452-ROOT", "logical_decomposition", "M0452-S-FOUNDATION")],
    "provenance": [edge("SRC-HEIGHT", "M0452-H-LIMIT", "source_map", "M0452-X-SOURCE"), edge("SRC-KERNEL", "M0452-K-KERNEL", "source_map", "M0452-X-SOURCE"), edge("PROV-ROOT", "M0452-X-PROVENANCE", "provenance_of", "M0452-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0452-ROOT", "trusts", "M0452-S-FOUNDATION"), edge("TRUST-PROV", "M0452-ROOT", "trusts", "M0452-X-PROVENANCE")],
    "documentation": [edge("DOC-NORM", "M0452-S-NORMALIZATION", "documents", "M0452-ROOT"), edge("DOC-SOURCE-HEIGHT", "M0452-X-SOURCE", "documents", "M0452-H-LIMIT"), edge("DOC-SOURCE-KERNEL", "M0452-X-SOURCE", "documents", "M0452-K-KERNEL")],
    "workflow": [edge("FLOW-ASSEMBLE-HEIGHT", "M0452-T-ASSEMBLE", "workflow_depends_on", "M0452-H-LIMIT"), edge("FLOW-ASSEMBLE-POLAR", "M0452-T-ASSEMBLE", "workflow_depends_on", "M0452-P-ASSEMBLE"), edge("FLOW-ASSEMBLE-QUOT", "M0452-T-ASSEMBLE", "workflow_depends_on", "M0452-D-POSITIVE"), edge("FLOW-PROV-ASSEMBLE", "M0452-X-PROVENANCE", "workflow_depends_on", "M0452-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0452-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0452-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0452-H-LIMIT", "M0452-P-ASSEMBLE", "M0452-D-POSITIVE"], "composition_certificates": ["Stage1Instances.THM_M_0452.root_of_height_polarization_quotient"], "reason": "The final composition is conditional; all three semantic input packages remain open."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0452/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
