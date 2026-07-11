#!/usr/bin/env python3
"""Build the frozen THM-M-0415 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0415-OBLIGATION_TREE"
THEOREM = "THM-M-0415"
REGISTRY = "THM-M-0415-OBLIGATIONS-v1"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


ROWS = [
    ("M0415-ROOT", "root", "critical", "The ideal class group of the ring of integers of every number field is finite.", "Stage1Instances.THM_M_0415.IdealClassGroupFiniteTarget", "The exact frozen root.", 8, "required", "required"),
    ("M0415-S-DEFINITIONS", "definition", "high", "Fix number fields, rings of integers, ideal class groups, and propositional finiteness with the frozen universe and typeclass binders.", "Stage1Instances.THM_M_0415.IdealClassGroupFiniteTarget", "The exact statement interface.", 25, "not_applicable", "required"),
    ("M0415-S-BOUNDARY", "terminal", "normal", "Retain the rational field, class-number-one fields, all finite degrees, and all signatures without an extra nontriviality hypothesis.", "Stage1Instances.THM_M_0415.rational_boundary plus statement mutation record", "Checked boundary and exclusion policy.", 20, "not_applicable", "required"),
    ("M0415-S-TRANSPORT", "transport", "high", "Transport exactly between Finite class-group propositions and inhabited Fintype data.", "Stage1Instances.THM_M_0415.idealClassGroupFiniteTarget_iff_fintypePresentation", "The checked Finite/Fintype equivalence.", 12, "not_applicable", "required"),
    ("M0415-S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotients, propositional extensionality, the transitive declaration closure, and the pinned Lean TCB.", "planned exact axiom and TCB report", "An accepted foundation and trust boundary.", 35, "not_applicable", "required"),
    ("M0415-X-NUMBERFIELD-INSTANCE", "bridge", "critical", "Specialize the general admissible-absolute-value class-number construction to Q and an arbitrary number field K.", "NumberField.RingOfIntegers.instFintypeClassGroup", "Fintype (ClassGroup (RingOfIntegers K)).", 18, "required", "required"),
    ("M0415-N-FINITE-EXTENSION", "reduction", "critical", "Build the integral-closure, Dedekind-domain, fraction-ring, finite-basis, and algebraicity data needed to invoke the algebraic-extension construction.", "ClassGroup.fintypeOfAdmissibleOfFinite", "The hypotheses and call to the algebraic-extension finiteness construction.", 90, "required", "required"),
    ("M0415-C-FINITE-APPROX", "construction", "critical", "Construct the finite approximation supplied by an admissible absolute value and prove its approximation property.", "ClassGroup.finsetApprox and ClassGroup.exists_mem_finsetApprox", "A finite set of approximants with the required norm inequality.", 100, "required", "required"),
    ("M0415-C-IDEAL-REPRESENTATIVES", "construction", "critical", "Show every ideal class has a representative ideal containing the product of the finite approximation.", "ClassGroup.exists_mk0_eq_mk0", "A bounded finite family containing a representative of every class.", 100, "required", "required"),
    ("M0415-L-SURJECTION", "core_lemma", "critical", "Construct the map from the finite subtype of representative ideals to the class group and prove it surjective.", "ClassGroup.mkMMem_surjective", "A surjection from a finite type onto the class group.", 35, "required", "required"),
    ("M0415-T-ALGEBRAIC-FINTYPE", "terminal", "critical", "Use the finite representative subtype and its surjection to construct a Fintype instance for the class group in an algebraic extension.", "ClassGroup.fintypeOfAdmissibleOfAlgebraic", "Fintype (ClassGroup S).", 30, "required", "required"),
    ("M0415-T-FINTYPE-PRESENTATION", "terminal", "high", "Package the pinned number-field Fintype instance into the exact data-bearing child proposition.", "Stage1Instances.THM_M_0415.ObligationTree.fintypePresentation_mathlib", "Stage1Instances.THM_M_0415.FintypePresentation.", 8, "required", "required"),
    ("M0415-T-FINITE-WRAPPER", "terminal", "high", "Consume the exact data-bearing child and the checked transport to yield the canonical Finite root.", "Stage1Instances.THM_M_0415.ObligationTree.finiteTarget_of_fintypePresentation", "Stage1Instances.THM_M_0415.IdealClassGroupFiniteTarget.", 6, "not_applicable", "required"),
    ("M0415-X-SOURCE", "terminal", "high", "Map the admissible-value, approximation, representative, and surjection nodes to pinpoint reviewed primary mathematical sources.", "non-machine node-specific primary-source crosswalk", "Human-source coverage only.", 50, "required", "required"),
    ("M0415-X-PROVENANCE", "certificate", "critical", "Resolve unique terminal bodies, source blobs, imports, transitive dependencies, axioms, TCB, licenses, and replay receipts.", "planned machine-derived provenance closure", "Release provenance without duplicate proof credit.", 45, "not_applicable", "required"),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

machine_special = {"M0415-X-SOURCE": "not_applicable", "M0415-X-PROVENANCE": "informational"}
checked_local = {"M0415-S-BOUNDARY", "M0415-S-TRANSPORT", "M0415-T-FINTYPE-PRESENTATION", "M0415-T-FINITE-WRAPPER"}
candidate_mathlib = {"M0415-X-NUMBERFIELD-INSTANCE", "M0415-N-FINITE-EXTENSION", "M0415-C-FINITE-APPROX", "M0415-C-IDEAL-REPRESENTATIVES", "M0415-L-SURJECTION", "M0415-T-ALGEBRAIC-FINTYPE"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, budget, human_source, readable in ROWS:
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-expression-sha256:" + statement_fp if oid == "M0415-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human_source, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0415-X-SOURCE" else ("release_provenance_overlay_no_proof_credit" if oid == "M0415-X-PROVENANCE" else None),
        "terminal_proof_body_id": "mathlib-8a178386:ClassGroup.fintypeOfAdmissibleOfAlgebraic" if oid in candidate_mathlib else ("local:ObligationTree.lean#" + ("fintypePresentation_mathlib" if oid == "M0415-T-FINTYPE-PRESENTATION" else "finiteTarget_of_fintypePresentation") if oid in {"M0415-T-FINTYPE-PRESENTATION", "M0415-T-FINITE-WRAPPER"} else None),
    })
    if oid in checked_local:
        mdebt = "M0-L"
    elif oid in candidate_mathlib:
        # Anchor discovery found these declarations, but this phase cannot
        # promote them to M0-W before accepted provenance/trust receipts.
        mdebt = "M3"
    elif oid == "M0415-ROOT":
        mdebt = "M3"
    else:
        mdebt = "M4"
    nodes.append({
        "node_id": "THM-M-0415-" + oid.removeprefix("M0415-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": mdebt, "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if human_source == "not_applicable" else "primary-source-node-map-pending",
        "provenance_id": "anchor-candidate-M0415-C01" if oid in candidate_mathlib else ("local-checked-interface" if oid in checked_local else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation is credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the frozen context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0415/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Provisional architecture/candidate classification only; no master receipt, H0/R0, audit completion, or theorem completion is supplied.",
        "task_ids": [ITEM, "S56-M-0415-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0415/ObligationTree.lean"] if oid in checked_local else [],
        "owner": "THM-M-0415 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked_local | candidate_mathlib else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "mathlib revision", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked_local | candidate_mathlib else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "registry_id": REGISTRY,
    "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus the pre-status architecture of the admissible-absolute-value proof; eligibility does not depend on candidate closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0415-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0415-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"checked_local_interfaces": sorted(checked_local), "provisional_mathlib_candidates": sorted(candidate_mathlib), "root_machine_debt": "M3"},
    "status_boundary": "The denominator is frozen and the exact wrapper elaborates, but all classifications await master acceptance and release provenance; root completion is not claimed.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    "M0415-ROOT": ["M0415-T-FINITE-WRAPPER"],
    "M0415-T-FINITE-WRAPPER": ["M0415-S-TRANSPORT", "M0415-T-FINTYPE-PRESENTATION"],
    "M0415-T-FINTYPE-PRESENTATION": ["M0415-X-NUMBERFIELD-INSTANCE"],
    "M0415-X-NUMBERFIELD-INSTANCE": ["M0415-N-FINITE-EXTENSION"],
    "M0415-N-FINITE-EXTENSION": ["M0415-T-ALGEBRAIC-FINTYPE"],
    "M0415-T-ALGEBRAIC-FINTYPE": ["M0415-C-FINITE-APPROX", "M0415-C-IDEAL-REPRESENTATIVES", "M0415-L-SURJECTION"],
    "M0415-C-IDEAL-REPRESENTATIVES": ["M0415-C-FINITE-APPROX"],
    "M0415-L-SURJECTION": ["M0415-C-IDEAL-REPRESENTATIVES"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0415-ROOT", "logical_decomposition", "M0415-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", "M0415-ROOT", "logical_decomposition", "M0415-S-BOUNDARY")],
    "provenance": [edge("SRC-APPROX", "M0415-C-FINITE-APPROX", "source_map", "M0415-X-SOURCE"), edge("SRC-SURJ", "M0415-L-SURJECTION", "source_map", "M0415-X-SOURCE"), edge("PROV-ROOT", "M0415-X-PROVENANCE", "provenance_of", "M0415-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0415-ROOT", "trusts", "M0415-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0415-ROOT", "trusts", "M0415-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M0415-X-SOURCE", "documents", "M0415-ROOT"), edge("DOC-BOUNDARY", "M0415-S-BOUNDARY", "documents", "M0415-ROOT")],
    "workflow": [edge("FLOW-PROOF", "M0415-T-FINITE-WRAPPER", "workflow_depends_on", "M0415-T-FINTYPE-PRESENTATION"), edge("FLOW-PROV", "M0415-X-PROVENANCE", "workflow_depends_on", "M0415-X-NUMBERFIELD-INSTANCE")],
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
    "registry_id": REGISTRY, "registry_denominator_sha256": denominator,
    "root_node_id": "M0415-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_machine_debt": "M3", "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0415-X-PROVENANCE", "M0415-X-SOURCE"],
        "checked_composition_certificates": ["Stage1Instances.THM_M_0415.ObligationTree.finiteTarget_of_fintypePresentation", "Stage1Instances.THM_M_0415.ObligationTree.idealClassGroupFinite_mathlib"],
        "reason": "The exact pinned wrapper checks, but full proof-body provenance/trust, H0/R0, receipts, and master acceptance remain open."},
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0415/check_obligation_tree.py"], "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": []} for oid, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
