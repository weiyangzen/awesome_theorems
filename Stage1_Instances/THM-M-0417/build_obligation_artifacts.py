#!/usr/bin/env python3
"""Build the frozen THM-M-0417 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0417-OBLIGATION_TREE"
THEOREM = "THM-M-0417"
STATEMENT = json.loads((HERE / "statement.json").read_text())
ROOT_HASH = STATEMENT["canonical_formal_target"]["elaborated_expression_sha256"]


def obligation(oid, fingerprint, kind, risk, body=None):
    return {
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required",
        "human_source_eligibility": "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": body,
    }


obligations = [
    obligation("M0417-ROOT", f"lean:Stage1Instances.THM_M_0417.Statement@{ROOT_HASH}", "root", "critical"),
    obligation("M0417-S-CONTEXT", "lean:Stage1Instances.THM_M_0417.ObligationTree.Root@rfl-to-frozen-statement-v1", "definition", "high"),
    obligation("M0417-N-HALF-VOLUME", "lean:Stage1Instances.THM_M_0417.ObligationTree.HalfBodyVolume@v1", "normalization", "high"),
    obligation("M0417-L-BLICHFELDT", "lean:Stage1Instances.THM_M_0417.ObligationTree.BlichfeldtBridge@v1", "bridge", "critical", "mathlib:MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd@8a178386"),
    obligation("M0417-C-COLLISION", "lean:Stage1Instances.THM_M_0417.ObligationTree.Collision@v1", "construction", "high"),
    obligation("M0417-T-DIFFERENCE", "lean:Stage1Instances.THM_M_0417.ObligationTree.DifferenceExtraction@v1", "transport", "high"),
    obligation("M0417-T-COMPOSE", "lean:Stage1Instances.THM_M_0417.ObligationTree.root_compose@v1", "terminal", "critical", "mathlib:MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure@8a178386"),
    obligation("M0417-X-SOURCE", "policy:v1:primary-source-theorem-page-assumptions-errata-crosswalk", "source_boundary", "high"),
    obligation("M0417-X-TRUST", "policy:v1:terminal-body-import-axiom-tcb-independent-replay", "trust_boundary", "critical"),
]

ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "theorem_id": THEOREM,
    "item_id": ITEM,
    "registry_version": 1,
    "freeze_policy": "append-only new version for any target, split, merge, exclusion, eligibility, or weight change",
    "canonical_root": "M0417-ROOT",
    "status_observed_at_freeze": False,
    "eligibility_denominator": {
        "root_relevant_machine": 9,
        "root_relevant_human_source": 9,
        "root_relevant_readable": 9,
        "excluded": 0,
    },
    "obligations": obligations,
    "aliases_and_non_denominator_surfaces": [
        {"name": "Stage1Instances.THM_M_0417.ObligationTree.Root", "canonical_obligation_id": "M0417-ROOT", "reason": "definitionally equal composition-harness root"},
        {"name": "Stage1Instances.THM_M_0417.AnchorAudit.mathlibCandidateClosesFrozenTarget", "canonical_obligation_id": "M0417-T-COMPOSE", "reason": "one-step wrapper around the unique pinned terminal body"},
        {"name": "AwesomeTheorems.Stage1.S1_M_072.minkowski_convex_body_strict", "canonical_obligation_id": "M0417-T-COMPOSE", "reason": "legacy duplicate wrapper with no distinct proof body"},
        {"name": "GeometryOfNumbers.minkowski_lattice_point", "canonical_obligation_id": "M0417-T-COMPOSE", "reason": "external duplicate wrapper with no distinct proof body"},
    ],
    "audit_complete": False,
    "theorem_complete": False,
    "status_boundary": "Nine obligations and zero exclusions are frozen. This inventory does not close proof, source, readability, trust, validation, or release gates.",
}

node_specs = {
    "M0417-ROOT": ("Exact strict Minkowski convex-body statement.", "Stage1Instances.THM_M_0417.Statement", "A nonzero member of L lying in s.", 3),
    "M0417-S-CONTEXT": ("The frozen binders, instances, covolume model, strict threshold, and witness coercions agree with the root.", "Stage1Instances.THM_M_0417.ObligationTree.root_exact_type", "Checked definitional equality to the frozen statement.", 2),
    "M0417-N-HALF-VOLUME": ("The strict 2^finrank bound implies that the half-scaled body has measure greater than the fundamental domain.", "Stage1Instances.THM_M_0417.ObligationTree.HalfBodyVolume", "mu F < mu ((2^-1) • s).", 4),
    "M0417-L-BLICHFELDT": ("Blichfeldt applied to the measurable half-body yields distinct lattice translates that overlap.", "Stage1Instances.THM_M_0417.ObligationTree.BlichfeldtBridge", "Collision E L s.", 3),
    "M0417-C-COLLISION": ("Unpack translate non-disjointness into half-body points with equal translated images.", "Stage1Instances.THM_M_0417.ObligationTree.Collision", "Distinct x,y in L and an overlap relation for their half-body translates.", 3),
    "M0417-T-DIFFERENCE": ("Use the overlap equation, central symmetry, and convexity to put x-y in s and prove x-y is nonzero.", "Stage1Instances.THM_M_0417.ObligationTree.DifferenceExtraction", "A nonzero lattice point in s.", 5),
    "M0417-T-COMPOSE": ("Compose half-body volume, Blichfeldt collision, and difference extraction without adding premises.", "Stage1Instances.THM_M_0417.ObligationTree.root_compose", "The exact root proposition.", 3),
    "M0417-X-SOURCE": ("Map every mathematical obligation to a primary source theorem, assumptions, page, and errata record.", "policy obligation; no Lean declaration", "Human-source boundary record.", 2),
    "M0417-X-TRUST": ("Classify the terminal body, transitive declarations, axioms, imports, TCB, and replay boundary.", "policy obligation; terminal declaration MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure", "Trust and provenance boundary record.", 3),
}

ledgers = {
    "M0417-ROOT": [
        (["M0417-S-CONTEXT", "M0417-N-HALF-VOLUME"], "instantiate the frozen context and normalize the volume premise", "strict half-body volume bound", "M0417-L-BLICHFELDT"),
        (["M0417-L-BLICHFELDT", "M0417-C-COLLISION"], "apply and unpack the Blichfeldt collision", "distinct overlapping lattice translates", "M0417-T-DIFFERENCE"),
        (["M0417-T-DIFFERENCE", "M0417-T-COMPOSE"], "extract and compose the lattice difference witness", "exact frozen root conclusion", "root acceptance gate"),
    ],
    "M0417-S-CONTEXT": [
        (["statement-expression-" + ROOT_HASH], "compare universes, ordered binders, instances, coercions, hypotheses, and conclusion", "composition Root has the frozen expression", "root_exact_type"),
        (["root_exact_type"], "kernel-check definitional equality", "exact statement identity", "M0417-ROOT"),
    ],
    "M0417-N-HALF-VOLUME": [
        (["root strict measure premise"], "apply addHaar_smul_of_nonneg to scalar 2^-1", "measure of half-body as scalar factor times mu s", "ENNReal normalization"),
        (["finite-dimensionality", "two_ne_zero"], "rewrite the scalar factor as (2^-1)^finrank", "explicit dimension-dependent scale", "inequality cancellation"),
        (["mu F * 2^finrank < mu s"], "cancel the finite nonzero 2^finrank factor in ENNReal", "mu F below the rescaled measure expression", "final arithmetic"),
        (["inverse multiplication identities"], "normalize inverse powers and multiplication order", "mu F < mu ((2^-1) • s)", "M0417-L-BLICHFELDT"),
    ],
    "M0417-L-BLICHFELDT": [
        (["Convex Real s"], "scale convexity by 2^-1 and derive null measurability", "NullMeasurableSet ((2^-1) • s) mu", "Blichfeldt premise"),
        (["fundamental domain", "half-body volume bound", "half-body null measurability"], "apply exists_pair_mem_lattice_not_disjoint_vadd", "distinct x,y with nondisjoint translates", "M0417-C-COLLISION"),
        (["Blichfeldt witnesses"], "package the witness and overlap relation", "Collision E L s", "M0417-T-DIFFERENCE"),
    ],
    "M0417-C-COLLISION": [
        (["not Disjoint translated half-bodies"], "use Set.not_disjoint_iff", "a common ambient point in both translates", "witness unpacking"),
        (["common-point memberships"], "unpack vadd-set membership", "half-body points v,w and translate equality", "difference rewriting"),
        (["x != y"], "retain distinct subgroup witnesses alongside the equality", "structured collision data", "M0417-T-DIFFERENCE"),
    ],
    "M0417-T-DIFFERENCE": [
        (["collision x != y"], "apply sub_ne_zero.mpr", "x-y != 0", "root witness nonzeroness"),
        (["half-body memberships"], "rewrite inverse scalar membership", "v,w belong to the original body after doubling", "convexity inputs"),
        (["translate overlap equality"], "rewrite vadd as addition and isolate the subgroup difference", "x-y equals the half-scaled point difference", "body membership calculation"),
        (["central symmetry", "membership of v"], "replace subtraction by addition of a body point and its negative", "two points of s at equal weights", "convexity"),
        (["Convex Real s", "weights 1/2 and 1/2"], "apply convexity and normalize the scalar expression", "the nonzero lattice difference lies in s", "M0417-T-COMPOSE"),
    ],
    "M0417-T-COMPOSE": [
        (["M0417-N-HALF-VOLUME"], "specialize HalfBodyVolume to the root inputs", "half-body strict measure bound", "BlichfeldtBridge"),
        (["M0417-L-BLICHFELDT", "half-body bound"], "specialize BlichfeldtBridge", "Collision E L s", "DifferenceExtraction"),
        (["M0417-T-DIFFERENCE", "collision"], "specialize DifferenceExtraction", "exact Root conclusion", "M0417-ROOT"),
    ],
    "M0417-X-SOURCE": [
        (["Minkowski 1896 discovery anchor", "mathlib Clark reference"], "locate exact theorem, edition, page, and assumptions", "pinpoint source crosswalk", "independent source review"),
        (["pinpoint crosswalk", "errata search"], "independently review every root-relevant obligation", "H0-eligible source packet or explicit debt", "release source gate"),
    ],
    "M0417-X-TRUST": [
        (["pinned terminal declaration"], "resolve terminal body and transitive declaration/import provenance", "complete formal provenance graph", "foundation comparison"),
        (["transitive provenance", "axiom output"], "compare exact principles with the versioned foundation profile", "accepted or rejected foundation closure", "TCB audit"),
        (["Lean executable", "compiled artifacts", "package tools", "replay recipes"], "inventory, hash, and independently replay the full trusted boundary", "release-grade trust packet or explicit debt", "release trust gate"),
    ],
}

nodes = []
for row in obligations:
    oid = row["obligation_id"]
    statement, formal, output, budget = node_specs[oid]
    assert len(ledgers[oid]) == budget
    steps = []
    for index, (premises, inference, step_output, outgoing_use) in enumerate(ledgers[oid], 1):
        steps.append({
            "step_id": f"{oid}-STEP-{index}",
            "premises": premises,
            "inference": inference,
            "output": step_output,
            "outgoing_use": outgoing_use,
        })
    nodes.append({
        "node_id": "THM-M-0417-" + oid.removeprefix("M0417-"),
        "obligation_id": oid,
        "kind": row["kind"],
        "human_statement": statement,
        "formal_target": formal,
        "output": output,
        "human_debt": "H1",
        "machine_debt": "M0-W-candidate" if oid == "M0417-T-COMPOSE" else "M2",
        "readability_debt": "R3",
        "evidence_ids": ["evidence:statement-expression-" + ROOT_HASH[:12]] if oid in {"M0417-ROOT", "M0417-S-CONTEXT"} else [],
        "source_crosswalk_id": "source_statement_crosswalk.md" if oid != "M0417-X-TRUST" else "not-applicable",
        "provenance_id": row["terminal_proof_body_id"] or "none",
        "foundation_profile": "lean4-mathlib-classical-v1-pending-validation",
        "tcb_profile": "lean4-4.29.0-mathlib-8a178386-pending-transitive-audit",
        "computation_record": "none",
        "step_budget": budget,
        "semantic_step_ledger": steps,
        "public_readable_target": f"Stage1_Instances/THM-M-0417/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "recipe:M0417-obligation-tree-lean" if oid not in {"M0417-X-SOURCE", "M0417-X-TRUST"} else "recipe:M0417-obligation-tree-structure",
        "status_boundary": "Architecture and decomposition only; no H0, M0, R0, or theorem-completion credit.",
        "task_ids": [ITEM, "S56-M-0417-PROOF", "S56-M-0417-VALIDATION"],
        "owned_sources": ["Stage1_Instances/THM-M-0417/ObligationTree.lean", "Stage1_Instances/THM-M-0417/obligation-tree.md"],
        "owner": "Stage1 rev-5.6 THM-M-0417 execution lane",
        "reviewer": "independent integration-lane reviewer required",
        "validity": {"validated_at": "2026-07-12", "review_due": "on any invalidation input", "invalidation_inputs": ["statement", "registry", "Lean source", "mathlib pin", "standard"], "revocation_state": "active-provisional"},
    })

nodes_doc = {
    "schema_version": "stage1-obligation-nodes/1.0",
    "theorem_id": THEOREM,
    "item_id": ITEM,
    "registry_version": 1,
    "nodes": nodes,
    "status_boundary": "Node records freeze the architecture and budgets; their debt values remain open projections.",
}

proof_children = ids[1:]
graphs = {
    "schema_version": "stage1-typed-graphs/1.0",
    "theorem_id": THEOREM,
    "item_id": ITEM,
    "registry_version": 1,
    "nodes": ids,
    "graphs": {
        "proof": ([{"from": "M0417-ROOT", "type": "proof_requires", "to": child} for child in proof_children] + [
            {"from": "M0417-N-HALF-VOLUME", "type": "composes", "to": "M0417-T-COMPOSE", "certificate": "Stage1Instances.THM_M_0417.ObligationTree.root_compose", "status": "conditional-kernel-checked"},
            {"from": "M0417-L-BLICHFELDT", "type": "composes", "to": "M0417-T-COMPOSE", "certificate": "Stage1Instances.THM_M_0417.ObligationTree.root_compose", "status": "conditional-kernel-checked"},
            {"from": "M0417-T-DIFFERENCE", "type": "composes", "to": "M0417-T-COMPOSE", "certificate": "Stage1Instances.THM_M_0417.ObligationTree.root_compose", "status": "conditional-kernel-checked"},
            {"from": "M0417-T-COMPOSE", "type": "composes", "to": "M0417-ROOT", "certificate": "Stage1Instances.THM_M_0417.ObligationTree.root_exact_type", "status": "conditional-kernel-checked"},
        ]),
        "refinement": [
            {"from": "M0417-S-CONTEXT", "type": "logical_decomposition", "to": "M0417-N-HALF-VOLUME"},
            {"from": "M0417-N-HALF-VOLUME", "type": "logical_decomposition", "to": "M0417-L-BLICHFELDT"},
            {"from": "M0417-L-BLICHFELDT", "type": "logical_decomposition", "to": "M0417-C-COLLISION"},
            {"from": "M0417-C-COLLISION", "type": "logical_decomposition", "to": "M0417-T-DIFFERENCE"},
            {"from": "M0417-T-DIFFERENCE", "type": "logical_decomposition", "to": "M0417-T-COMPOSE"},
        ],
        "provenance": [
            {"from": "source:mathlib-GeometryOfNumbers-lines-65-84@8a178386", "type": "provenance_of", "to": "M0417-T-COMPOSE"},
            {"from": "source:mathlib-GeometryOfNumbers-lines-52-60@8a178386", "type": "provenance_of", "to": "M0417-L-BLICHFELDT"},
            {"from": "source:Minkowski-Geometrie-der-Zahlen-1896-review-open", "type": "source_map", "to": "M0417-X-SOURCE"},
        ],
        "evidence": [
            {"from": "evidence:statement-expression-" + ROOT_HASH[:12], "type": "evidence_for", "to": "M0417-ROOT"},
            {"from": "evidence:anchor-audit-C01", "type": "evidence_for", "to": "M0417-T-COMPOSE"},
            {"from": "evidence:conditional-composition-selftest", "type": "evidence_for", "to": "M0417-T-COMPOSE"},
        ],
        "trust": [
            {"from": "M0417-ROOT", "type": "trusts", "to": "M0417-X-TRUST"},
            {"from": "M0417-T-COMPOSE", "type": "trusts", "to": "trust:mathlib-terminal-transitive-closure-pending-validation"},
            {"from": "M0417-L-BLICHFELDT", "type": "trusts", "to": "trust:mathlib-Blichfeldt-transitive-closure-pending-validation"},
        ],
        "documentation": [{"from": f"doc:obligation-tree.md#{oid.lower()}", "type": "documents", "to": oid} for oid in ids],
        "workflow": [
            {"from": "task:S56-M-0417-OBLIGATION_TREE", "type": "workflow_depends_on", "to": "task:S56-M-0417-ANCHOR_AUDIT"},
            {"from": "task:S56-M-0417-PROOF", "type": "workflow_depends_on", "to": "task:S56-M-0417-OBLIGATION_TREE"},
            {"from": "task:S56-M-0417-VALIDATION", "type": "workflow_depends_on", "to": "task:S56-M-0417-PROOF"},
            {"from": "task:S56-M-0417-RELEASE", "type": "workflow_depends_on", "to": "task:S56-M-0417-VALIDATION"},
        ],
    },
    "graph_invariants": {"proof_acyclic": True, "proof_root_reaches": 9, "unknown_semantic_endpoints": 0, "semantic_and_workflow_edges_separated": True},
    "status_boundary": "Typed edges freeze proof, refinement, provenance, evidence, trust, documentation, and workflow relations; no open obligation is thereby closed.",
}

recipes = {
    "schema_version": "stage1-validation-recipes/1.0",
    "theorem_id": THEOREM,
    "item_id": ITEM,
    "recipes": [
        {"recipe_id": "recipe:M0417-obligation-tree-lean", "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0417/ObligationTree.lean"], "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains root_compose and axiom report"}], "covered_obligation_ids": ids[:7], "covered_declarations": ["Stage1Instances.THM_M_0417.ObligationTree.root_compose", "Stage1Instances.THM_M_0417.ObligationTree.root_exact_type"]},
        {"recipe_id": "recipe:M0417-obligation-tree-structure", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0417/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 60, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact structural success marker"}], "covered_obligation_ids": ids, "covered_declarations": []},
    ],
}

for name, value in (("obligation-registry.json", registry), ("obligation-nodes.json", nodes_doc), ("typed-graphs.json", graphs), ("validation-recipes.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=False) + "\n")

for name in ("obligation-registry.json", "obligation-nodes.json", "typed-graphs.json", "validation-recipes.json"):
    digest = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    print(f"{digest}  {name}")
