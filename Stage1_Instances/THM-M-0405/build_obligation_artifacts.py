#!/usr/bin/env python3
"""Build the frozen THM-M-0405 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATEMENT_HASH = "db2edf61040b73d00d4d3ab2b7dc227b6ec418793400bf79ac86edc79aa18da1"
REGISTRY_ID = "THM-M-0405-OBLIGATIONS-v1"


def obligation(oid, kind, risk="critical", source=True):
    return {
        "obligation_id": oid,
        "statement_fingerprint": (
            f"lean-sha256:{STATEMENT_HASH}" if oid == "M0405-ROOT"
            else f"planned-id:{oid}:v1"
        ),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required",
        "human_source_eligibility": "required" if source else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": None,
    }


OBLIGATIONS = [
    obligation("M0405-ROOT", "root"),
    obligation("M0405-S-DEFINITIONS", "definition", "high", False),
    obligation("M0405-S-FOUNDATION", "terminal", source=False),
    obligation("M0405-B-LUCAS", "branch"),
    obligation("M0405-B-LEHMER", "branch"),
    obligation("M0405-N-PAIR-NORMALIZATION", "normalization"),
    obligation("M0405-C-CYCLOTOMIC-FACTOR", "construction"),
    obligation("M0405-L-NONPRIMITIVE-BOUND", "lemma"),
    obligation("M0405-L-LARGE-INDEX-EXCLUSION", "lemma"),
    obligation("M0405-B-DEFECTIVE-CLASSIFICATION", "branch"),
    obligation("M0405-X-BHV-BRIDGE", "terminal"),
    obligation("M0405-T-LUCAS-ADAPTER", "transport", "high"),
    obligation("M0405-T-LEHMER-ADAPTER", "transport", "high"),
    obligation("M0405-C-ROOT-COMPOSITION", "terminal", "high", False),
    obligation("M0405-X-PROVENANCE", "terminal", source=False),
]

DENOMINATOR_KEYS = [
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason",
]
projection = [{k: o[k] for k in DENOMINATOR_KEYS} for o in OBLIGATIONS]
denominator_hash = hashlib.sha256(
    json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "registry_id": REGISTRY_ID,
    "theorem_id": "THM-M-0405",
    "item_id": "S56-M-0405-OBLIGATION_TREE",
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": {
        "canonical_declaration": "Stage1.THM_M_0405.Statement",
        "statement_source_sha256": STATEMENT_HASH,
        "source_inventory": "anchor-audit.json",
        "architecture_rule": "The two exact conjunction branches and the BHV primitive-divisor argument are required independently of candidate availability.",
    },
    "denominator_projection": "Registry-order objects restricted to the nine eligibility keys and serialized with sorted keys and compact separators.",
    "denominator_sha256": denominator_hash,
    "obligations": OBLIGATIONS,
    "eligibility_counts": {
        "total": len(OBLIGATIONS), "root_relevant": len(OBLIGATIONS),
        "machine_required": len(OBLIGATIONS),
        "human_source_required": sum(o["human_source_eligibility"] == "required" for o in OBLIGATIONS),
        "readable_required": len(OBLIGATIONS), "informational": 0,
    },
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M4"},
    "append_only_delta": [],
    "status_boundary": "The registry freezes scope and denominators only; it supplies no BHV proof or theorem-completion evidence.",
}

DETAILS = {
    "M0405-ROOT": ("root", "The exact frozen conjunction: both Lucas and Lehmer terms have a primitive divisor for every index above 30.", "Stage1.THM_M_0405.Statement", "The canonical proposition.", 8, ["Obtain the exact Lucas branch.", "Obtain the exact Lehmer branch.", "Apply the checked conjunction constructor."], "SRC-BHV-2001-MAIN"),
    "M0405-S-DEFINITIONS": ("definition", "The pair structures, sequences, discriminants, and primitive-divisor predicates encode the selected claim.", "Stage1.THM_M_0405.{LucasPair,LehmerPair,LucasPair.IsPrimitiveDivisor,LehmerPair.IsPrimitiveDivisor}", "Well-scoped canonical definitions.", 35, ["Audit pair invariants and coprimality.", "Audit quotient identities for odd/even indices.", "Audit prime, term, discriminant, and earlier-term exclusions."], "not-applicable"),
    "M0405-S-FOUNDATION": ("terminal", "The eventual proof has an accepted transitive axiom and trusted-computing-base closure.", "planned root axiom/dependency report", "Accepted trust closure.", 25, ["Resolve terminal declarations.", "Extract transitive constants and axioms.", "Compare them with the pinned foundation profile."], "not-applicable"),
    "M0405-B-LUCAS": ("branch", "Every canonical Lucas pair and n > 30 admits a prime satisfying the exact Lucas primitive-divisor predicate.", "Stage1.THM_M_0405.LucasBranch", "The left conjunct of Statement.", 30, ["Instantiate the common BHV result for a Lucas pair.", "Translate its primitive-divisor conclusion.", "Return the existential prime."], "SRC-BHV-2001-LUCAS"),
    "M0405-B-LEHMER": ("branch", "Every canonical Lehmer pair and n > 30 admits a prime satisfying the exact Lehmer primitive-divisor predicate.", "Stage1.THM_M_0405.LehmerBranch", "The right conjunct of Statement.", 35, ["Instantiate the common BHV result for a Lehmer pair.", "Select the parity-specific sequence identity.", "Translate its primitive-divisor conclusion."], "SRC-BHV-2001-LEHMER"),
    "M0405-N-PAIR-NORMALIZATION": ("normalization", "Convert each canonical pair into the normalized Lucas-or-Lehmer pair data used by BHV without losing coprimality or nontorsion.", "planned Lean normalized-pair constructor", "Normalized source hypotheses for either branch.", 85, ["Package integral invariants.", "Preserve nonzero and coprime conditions.", "Transport the quotient nontorsion hypothesis.", "Identify the stored integer sequence with the source quotient."], "SRC-BHV-2001-DEFS"),
    "M0405-C-CYCLOTOMIC-FACTOR": ("construction", "Construct the homogeneous cyclotomic factor of the nth term and relate its prime factors to primitive divisors.", "planned Lean cyclotomic-factor construction", "An integral factor controlling primitive primes.", 95, ["Define the homogeneous cyclotomic value.", "Derive its product/Mobius relation to sequence terms.", "Control primes shared with the discriminant and earlier terms."], "SRC-BHV-2001-CYCLOTOMIC"),
    "M0405-L-NONPRIMITIVE-BOUND": ("core_lemma", "If the nth term has no primitive divisor, its cyclotomic factor satisfies the explicit upper bounds used in the BHV reduction.", "planned Lean nonprimitive upper-bound theorem", "An explicit numerical inequality under defectiveness.", 100, ["Assume absence of primitive primes.", "Classify valuations of the cyclotomic factor.", "Bound exceptional prime contributions.", "Assemble the logarithmic upper bound."], "SRC-BHV-2001-BOUND"),
    "M0405-L-LARGE-INDEX-EXCLUSION": ("core_lemma", "Cyclotomic lower estimates contradict the nonprimitive upper bound outside the finite exceptional index range.", "planned Lean analytic inequality theorem", "Defectiveness implies membership in a finite index range.", 100, ["Apply lower bounds for cyclotomic values.", "Combine them with the nonprimitive upper bound.", "Verify the explicit inequalities by certified arithmetic.", "Deduce the finite remaining range."], "SRC-BHV-2001-LARGE-N"),
    "M0405-B-DEFECTIVE-CLASSIFICATION": ("branch", "The finite remaining defective Lucas and Lehmer pairs are exhaustively classified, and none has index greater than 30.", "planned Lean finite classification certificate", "No defective normalized pair exists for n > 30.", 100, ["Enumerate the bounded index cases.", "Reduce parameters using the source classification.", "Check each certified exceptional family.", "Prove the list exhaustive and its indices at most 30."], "SRC-BHV-2001-CLASSIFICATION"),
    "M0405-X-BHV-BRIDGE": ("bridge", "Compose normalization, cyclotomic bounds, large-index exclusion, and finite classification into the common BHV theorem.", "planned exact Lean BHV theorem", "Primitive-divisor existence for every normalized Lucas or Lehmer pair at n > 30.", 45, ["Suppose the nth term is defective.", "Apply the upper/lower-bound reduction.", "Enter the exhaustive finite classification.", "Contradict n > 30."], "SRC-BHV-2001-MAIN"),
    "M0405-T-LUCAS-ADAPTER": ("transport", "Translate the common BHV conclusion to the exact LucasPair.IsPrimitiveDivisor predicate.", "planned exact Lucas adapter", "M0405-B-LUCAS.", 55, ["Rewrite the normalized term as L.term n.", "Rewrite the discriminant.", "Translate all earlier positive-term exclusions."], "SRC-BHV-2001-LUCAS"),
    "M0405-T-LEHMER-ADAPTER": ("transport", "Translate the common BHV conclusion to the parity-sensitive LehmerPair.IsPrimitiveDivisor predicate.", "planned exact Lehmer adapter", "M0405-B-LEHMER.", 65, ["Split on index parity only for the sequence identity.", "Rewrite the squared even denominator.", "Translate all earlier positive-term exclusions."], "SRC-BHV-2001-LEHMER"),
    "M0405-C-ROOT-COMPOSITION": ("terminal", "Combine the exact Lucas and Lehmer branches into the canonical conjunction.", "Stage1.THM_M_0405.statement_of_branches", "Stage1.THM_M_0405.Statement.", 6, ["Apply And.intro to the two exact branch premises."], "not-applicable"),
    "M0405-X-PROVENANCE": ("terminal", "Every eventual proof body, imported theorem, computation certificate, and source boundary has content-addressed provenance.", "planned machine-derived provenance closure", "Complete body/origin/TCB inventory.", 40, ["Resolve terminal proof bodies.", "Hash origins and dependencies.", "Bind validation receipts to this registry."], "not-applicable"),
}


def node(oid):
    kind, human, formal, output, budget, steps, source = DETAILS[oid]
    return {
        "node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": "M4", "readability_debt": "R3" if budget < 60 else "R4",
        "evidence_ids": [], "source_crosswalk_id": source,
        "provenance_id": "PROV-LOCAL-CHECKED-COMPOSITION" if oid == "M0405-C-ROOT-COMPOSITION" else "none",
        "foundation_profile": "LEAN4-MATHLIB-CLASSICAL-v1", "tcb_profile": "LEAN4-PINNED-v1",
        "computation_record": "none", "step_budget": budget, "semantic_step_ledger": steps,
        "public_readable_target": f"Stage1_Instances/THM-M-0405/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-M0405-OBLIGATION-TREE",
        "status_boundary": "Open architecture node; no proof-body closure is credited." if oid != "M0405-C-ROOT-COMPOSITION" else "The composition term is checked, but its two mathematical premises remain open.",
        "task_ids": ["S56-M-0405-OBLIGATION_TREE", "S56-M-0405-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0405/ObligationTree.lean" if oid in {"M0405-B-LUCAS", "M0405-B-LEHMER", "M0405-C-ROOT-COMPOSITION"} else "Stage1_Instances/THM-M-0405/obligation-graphs.json"],
        "owner": "S56-M-0405 execution lane", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M0405-C-ROOT-COMPOSITION" else None, "review_due": "on invalidation", "invalidation_inputs": ["statement hash", "registry hash", "proof implementation"], "revocation_state": "provisional" if oid == "M0405-C-ROOT-COMPOSITION" else "open"},
    }


def graph(name, edge_type, pairs):
    edges, outgoing, incoming = [], {}, {}
    for i, (src, dst) in enumerate(pairs, 1):
        prefixes = {"proof": "P", "refinement": "R", "provenance": "PV", "evidence": "E", "trust": "TR", "documentation": "D", "workflow": "W"}
        eid = f"{prefixes[name]}{i:02d}"
        edges.append({"edge_id": eid, "type": edge_type, "from": src, "to": dst})
        outgoing.setdefault(src, []).append(eid)
        incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_pairs = [
    ("M0405-ROOT", "M0405-C-ROOT-COMPOSITION"),
    ("M0405-C-ROOT-COMPOSITION", "M0405-B-LUCAS"),
    ("M0405-C-ROOT-COMPOSITION", "M0405-B-LEHMER"),
    ("M0405-B-LUCAS", "M0405-T-LUCAS-ADAPTER"),
    ("M0405-B-LEHMER", "M0405-T-LEHMER-ADAPTER"),
    ("M0405-T-LUCAS-ADAPTER", "M0405-X-BHV-BRIDGE"),
    ("M0405-T-LEHMER-ADAPTER", "M0405-X-BHV-BRIDGE"),
    ("M0405-X-BHV-BRIDGE", "M0405-N-PAIR-NORMALIZATION"),
    ("M0405-X-BHV-BRIDGE", "M0405-C-CYCLOTOMIC-FACTOR"),
    ("M0405-X-BHV-BRIDGE", "M0405-L-NONPRIMITIVE-BOUND"),
    ("M0405-X-BHV-BRIDGE", "M0405-L-LARGE-INDEX-EXCLUSION"),
    ("M0405-X-BHV-BRIDGE", "M0405-B-DEFECTIVE-CLASSIFICATION"),
]
graphs = {
    "proof": graph("proof", "proof_requires", proof_pairs),
    "refinement": graph("refinement", "logical_decomposition", [("M0405-ROOT", "M0405-S-DEFINITIONS")]),
    "provenance": graph("provenance", "provenance_of", [("M0405-X-PROVENANCE", "M0405-ROOT")]),
    "evidence": graph("evidence", "evidence_for", []),
    "trust": graph("trust", "trusts", [("M0405-ROOT", "M0405-S-FOUNDATION"), ("M0405-ROOT", "M0405-X-PROVENANCE")]),
    "documentation": graph("documentation", "documents", [("M0405-ROOT", "M0405-S-DEFINITIONS"), ("M0405-ROOT", "M0405-X-BHV-BRIDGE")]),
    "workflow": graph("workflow", "workflow_depends_on", proof_pairs),
}

typed = {
    "schema_version": "stage1-typed-graphs/1.0", "theorem_id": "THM-M-0405",
    "registry_id": REGISTRY_ID,
    "edge_direction": "Edges run from consumer/parent to required child/support; reciprocal adjacency is explicit.",
    "nodes": [node(o["obligation_id"]) for o in OBLIGATIONS], "graphs": graphs,
    "closure_boundary": {
        "root_machine_debt": "M4", "closed_obligations": [],
        "minimal_open_root_cut_set": ["M0405-X-BHV-BRIDGE"],
        "checked_interfaces_not_closed": ["M0405-C-ROOT-COMPOSITION"],
        "composition_certificates": ["Stage1.THM_M_0405.statement_of_branches"],
        "audit_complete": False, "theorem_complete": False,
    },
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", typed)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

print(f"wrote 15 obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {denominator_hash}")
