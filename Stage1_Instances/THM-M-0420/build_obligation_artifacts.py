#!/usr/bin/env python3
"""Deterministically build the THM-M-0420 frozen obligation architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0420-OBLIGATION_TREE"
THEOREM = "THM-M-0420"


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def fp(target):
    return "sha256:" + hashlib.sha256(target.encode()).hexdigest()


# IDs and eligibility are frozen before any later proof phase observes closure.
raw = [
    ("M0420-ROOT", "root", "Exact Hilbert class field target for every number field.",
     "Stage1Instances.THM_M_0420.HilbertClassFieldTarget", "The exact canonical proposition.", "split-required", "critical", "M3"),
    ("M0420-S", "definition", "Freeze finite-prime unramifiedness, abelian Galoisness, reciprocity, and comparison-universe maximality.",
     "IsEverywhereUnramifiedAtFinitePrimes / IsAbelianGaloisExtension / HilbertClassFieldProperty", "The exact statement interface.", "split-required", "high", "M3"),
    ("M0420-S1", "transport", "Identify the canonical target with the directly expanded historical source shape.",
     "Stage1Instances.THM_M_0420.hilbertClassFieldTarget_iff_pinnedCandidateSourceShape", "A checked exact-statement equivalence.", 1, "low", "M0-L"),
    ("M0420-S2", "transport", "Reverse the reciprocity group-isomorphism orientation without changing content.",
     "Stage1Instances.THM_M_0420.reciprocity_orientation_transport", "A checked symmetry transport.", 3, "low", "M0-L"),
    ("M0420-N1", "normalization", "Relate the prime-ideal predicate to the standard finite-place notion used by global class field theory.",
     "planned: finite_prime_unramifiedness_equivalence", "A convention-preserving unramifiedness normalization.", "split-required", "critical", "M4"),
    ("M0420-N2", "normalization", "Normalize automorphisms, Artin maps, and class-group conventions to the frozen group isomorphism.",
     "planned: artin_reciprocity_convention_transport", "The frozen reciprocity orientation and modulus.", "split-required", "critical", "M4"),
    ("M0420-B", "branch", "Exhaust all finite unramified abelian comparison extensions in universe uM and preserve their embeddings.",
     "planned: comparison_extension_exhaustion", "The universally quantified maximality family.", "split-required", "critical", "M4"),
    ("M0420-C", "construction", "Construct a finite number-field extension candidate H/K with coherent instances.",
     "Stage1Instances.THM_M_0420.ObligationTree.ConstructionObligation", "A candidate shared by every property obligation.", "split-required", "critical", "M4"),
    ("M0420-C1", "construction", "Construct the global class field attached to the trivial modulus and identify its finite degree.",
     "planned: trivial_modulus_class_field_construction", "The mathematical construction underlying the candidate.", "split-required", "critical", "M4"),
    ("M0420-L1", "core_lemma", "Prove the shared candidate is an abelian Galois extension.",
     "Stage1Instances.THM_M_0420.ObligationTree.AbelianGaloisObligation", "Abelian Galoisness of H/K.", "split-required", "critical", "M4"),
    ("M0420-L2", "core_lemma", "Prove the shared candidate is unramified at every nonzero finite prime.",
     "Stage1Instances.THM_M_0420.ObligationTree.UnramifiedObligation", "Finite-prime unramifiedness of H/K.", "split-required", "critical", "M4"),
    ("M0420-L3", "core_lemma", "Global Artin reciprocity identifies the candidate automorphism group with the ideal class group.",
     "Stage1Instances.THM_M_0420.ObligationTree.ReciprocityObligation", "The frozen group isomorphism.", "split-required", "critical", "M4"),
    ("M0420-L4", "core_lemma", "Every finite everywhere-unramified abelian comparison extension embeds into the shared candidate over K.",
     "Stage1Instances.THM_M_0420.ObligationTree.MaximalityObligation", "Maximality in comparison universe uM.", "split-required", "critical", "M4"),
    ("M0420-X1", "bridge", "Supply the global existence and Artin reciprocity theorem at the exact trivial-modulus boundary.",
     "planned: global_class_field_theory_terminal_bridge", "The currently unavailable global class-field-theory engine.", "split-required", "critical", "M4"),
    ("M0420-T", "terminal", "Compose one shared candidate and its four properties into the exact existential root.",
     "Stage1Instances.THM_M_0420.ObligationTree.root_composition", "The exact root conditional on all substantive children.", 14, "critical", "M0-L"),
    ("M0420-X2", "terminal", "Audit terminal bodies, axioms, imports, provenance, and reproducibility.",
     "planned: terminal trust and provenance certificate", "A release report, not a mathematical premise.", 12, "critical", "M4"),
]

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
obligations = []
nodes = []
for oid, kind, human, formal, output, budget, risk, machine in raw:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(formal), "kind": kind,
        "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": "local:ObligationTree.lean:root_composition" if oid == "M0420-T" else None,
    })
    is_statement = oid in {"M0420-S", "M0420-S1", "M0420-S2"}
    is_harness = oid in {"M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4", "M0420-T"}
    owned = (["Stage1_Instances/THM-M-0420/Statement.lean"] if is_statement else [])
    if is_harness:
        owned.append("Stage1_Instances/THM-M-0420/ObligationTree.lean")
    nodes.append({
        "node_id": "THM-M-0420-" + oid.removeprefix("M0420-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": machine, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source_statement_crosswalk.md:pinpoint-review-pending",
        "provenance_id": "local:Statement.lean" if is_statement else ("local:ObligationTree.lean" if is_harness else "none"),
        "foundation_profile": "lean4-mathlib/rev-5.6-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": f"Premises are exactly the incoming typed proof edges for {oid}. Inference target: `{formal}`. Output: {output} Outgoing use is limited to the recorded typed edges.",
        "public_readable_target": f"Stage1_Instances/THM-M-0420/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-M0420-COMPOSITION-LEAN" if oid == "M0420-T" else "VAL-M0420-ARCH-STRUCTURE",
        "status_boundary": "Architecture record only; M3/M4 targets have no credited proof body and conditional composition proves no premise.",
        "task_ids": [ITEM, "S56-M-0420-PROOF"], "owned_sources": owned,
        "owner": "THM-M-0420 execution lane", "reviewer": "independent master integration lane",
        "validity": {"frozen_on": "2026-07-12", "review_due": "before proof acceptance",
                     "invalidate_on": ["canonical statement", "registry", "anchor audit", "source map", "toolchain"],
                     "revocation_state": "none"},
    })

projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in raw]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_against_statement_sha256": sha("Statement.lean"),
    "frozen_against_statement_record_sha256": sha("statement.json"),
    "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "freeze_basis": "Exact elaborated statement plus bounded immutable anchor audit; eligibility was assigned without proof-status discovery.",
    "root_obligation_id": "M0420-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {key: ids for key in ("inventory", "required_machine", "required_human_source", "required_readable")},
    "append_only_deltas": [], "obligations": obligations,
    "status_boundary": "Sixteen semantic obligations are frozen; this grants no substantive proof credit."
}


def indexed(edges):
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_pairs = [
    ("M0420-ROOT", "M0420-T"), ("M0420-T", "M0420-C"), ("M0420-T", "M0420-L1"),
    ("M0420-T", "M0420-L2"), ("M0420-T", "M0420-L3"), ("M0420-T", "M0420-L4"),
    ("M0420-C", "M0420-C1"), ("M0420-C1", "M0420-X1"), ("M0420-L1", "M0420-X1"),
    ("M0420-L2", "M0420-N1"), ("M0420-L2", "M0420-X1"), ("M0420-L3", "M0420-N2"),
    ("M0420-L3", "M0420-X1"), ("M0420-L4", "M0420-B"), ("M0420-L4", "M0420-X1"),
]
proof = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    proof += [
        {"edge_id": f"P{i:02d}R", "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": f"P{i:02d}C"},
        {"edge_id": f"P{i:02d}C", "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": f"P{i:02d}R"},
    ]
refinement = [{"edge_id": f"R{i:02d}", "type": "logical_decomposition", "from": a, "to": b}
              for i, (a, b) in enumerate([("M0420-ROOT", "M0420-S"), ("M0420-S", "M0420-S1"), ("M0420-S", "M0420-S2")], 1)]
provenance = [
    {"edge_id": "PR01", "type": "provenance_of", "from": "M0420-X1", "to": "M0420-C1"},
    {"edge_id": "PR02", "type": "provenance_of", "from": "M0420-X1", "to": "M0420-L3"},
    {"edge_id": "PR03", "type": "provenance_of", "from": "M0420-T", "to": "M0420-ROOT"},
]
trust = [{"edge_id": "TR01", "type": "trusts", "from": "M0420-ROOT", "to": "M0420-X2"}]
docs = [{"edge_id": f"D{i:02d}", "type": "documents", "from": "M0420-S", "to": oid}
        for i, oid in enumerate(ids, 1) if oid != "M0420-S"]
workflow = [
    {"edge_id": "W01", "type": "workflow_depends_on", "from": "M0420-T", "to": "M0420-ROOT"},
    {"edge_id": "W02", "type": "workflow_depends_on", "from": "M0420-X2", "to": "M0420-T"},
]
graphs = {"proof": indexed(proof), "refinement": indexed(refinement), "provenance": indexed(provenance),
          "evidence": indexed([]), "trust": indexed(trust), "documentation": indexed(docs), "workflow": indexed(workflow)}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "root_obligation_id": "M0420-ROOT", "registry_denominator_sha256": denominator,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0420-S1", "M0420-S2", "M0420-T"],
                         "root_closed": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4"],
                         "reason": "The terminal theorem is conditional; construction and all four substantive properties remain M4."}
}
specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [
        {"recipe_id": "VAL-M0420-ARCH-STRUCTURE", "cwd": ".",
         "argv": ["python3", "Stage1_Instances/THM-M-0420/check_obligation_tree.py"],
         "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0420 obligation tree"}],
         "covered_obligation_ids": [oid for oid in ids if oid != "M0420-T"], "covered_declarations": []},
        {"recipe_id": "VAL-M0420-COMPOSITION-LEAN", "cwd": "Formalizations/Lean",
         "argv": ["bash", "../../Stage1_Instances/THM-M-0420/check_composition.sh"],
         "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains root_composition"}],
         "covered_obligation_ids": ["M0420-T"],
         "covered_declarations": ["Stage1Instances.THM_M_0420.ObligationTree.root_composition"]},
    ],
    "status_boundary": "Lean checks conditional child-to-root composition only; it asserts none of the five inputs."
}

for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2) + "\n")
