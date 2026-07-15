#!/usr/bin/env python3
"""Deterministically build the THM-M-0673 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0673-OBLIGATION_TREE"
THEOREM = "THM-M-0673"
PREFIX = "M0673-"
ROOT_EXPRESSION = "3b541698da0e2b40d0cef5ea0f03ebd62538d330293e4e393ce053e000906cba"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(payload).hexdigest()


def row(short: str, reg_kind: str, node_kind: str, risk: str, claim: str,
        formal: str, output: str, locator: str, budget: int,
        machine: str = "required", human: str = "required",
        body: str | None = None) -> dict:
    return {
        "short": short, "id": oid(short), "reg_kind": reg_kind,
        "node_kind": node_kind, "risk": risk, "claim": claim,
        "formal": formal, "output": output, "locator": locator,
        "budget": budget, "machine": machine, "human": human, "body": body,
    }


# Architecture and eligibility are fixed here independently of observed closure.
ROWS = [
    row("ROOT", "root", "root", "critical",
        "Every sentence is true in an ultraproduct exactly when it is true in almost every factor.",
        "Stage1Instances.THM_M_0673.LosSentenceTarget",
        "The exact polymorphic sentence biconditional frozen by Statement.lean.",
        "Statement.lean; expression sha256 " + ROOT_EXPRESSION, 8),
    row("S-INTERFACE", "definition", "definition", "critical",
        "Fix the language, index and carrier universes, ultrafilter, factor structures and nonempty instances, and sentence binder.",
        "Stage1Instances.THM_M_0673.LosSentenceTarget",
        "The exact binder order and product-satisfaction conclusion.",
        "Statement.lean:16-22; statement.json ordered_binders", 18,
        machine="informational", human="not_applicable"),
    row("S-BOUNDARY", "branch", "branch", "high",
        "Retain principal and nonprincipal ultrafilters, arbitrary index types, empty languages, nullary symbols, and quantified sentences without adding a nonempty-index premise.",
        "Statement.lean mutation suite and principal_boundary",
        "The complete degenerate-case policy for the root.",
        "scope-map.md; Statement.lean:40-75", 20,
        machine="informational", human="not_applicable"),
    row("S-FOUNDATION", "terminal", "certificate", "critical",
        "Fix quotient soundness, propositional extensionality, classical choice, kernel, and no-oracle policies for the route.",
        "Lean 4.29.0 foundation and transitive TCB packet",
        "An accepted foundation, trust, and computation boundary.",
        "anchor-audit.json candidate_result; AnchorAudit.lean axiom reports", 36,
        machine="informational", human="not_applicable"),
    row("T-ADAPTER", "transport", "transport", "high",
        "Consume the exact sentence terminal package and yield the canonical LosSentenceTarget without a broadened statement.",
        "Stage1Instances.THM_M_0673_Obligations.terminal_of_sentence; root_of_terminal",
        "The exact canonical root, conditionally on the sentence package.",
        "ObligationTree.lean", 8,
        body="repo:Stage1Instances.THM_M_0673_Obligations.root_of_terminal"),
    row("A-SENTENCE", "terminal", "bridge", "critical",
        "Specialize formula satisfaction to the empty free-variable type and eliminate the unique assignment.",
        "FirstOrder.Language.Ultraproduct.sentence_realize / SentenceRealizePackage",
        "Sentence satisfaction in the product iff factor satisfaction is ultrafilter-eventual.",
        "Mathlib/ModelTheory/Ultraproducts.lean:152-158", 14,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.Ultraproduct.sentence_realize"),
    row("A-FORMULA", "terminal", "bridge", "critical",
        "Specialize bounded-formula transfer to formulas with no in-scope bound variables.",
        "FirstOrder.Language.Ultraproduct.realize_formula_cast / FormulaRealizePackage",
        "Formula satisfaction transfer for arbitrary free-variable assignments.",
        "Mathlib/ModelTheory/Ultraproducts.lean:146-150", 14,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.Ultraproduct.realize_formula_cast"),
    row("A-BOUNDED", "lemma", "bridge", "critical",
        "Prove satisfaction transfer for every bounded formula by structural induction.",
        "FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast / BoundedFormulaRealizePackage",
        "The substantive all-formulas transfer package.",
        "Mathlib/ModelTheory/Ultraproducts.lean:94-144", 72,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast"),
    row("B-FALSUM", "branch", "branch", "normal",
        "Transfer falsum using the proper-filter eventually-constant law.",
        "BoundedFormula.falsum branch; Filter.eventually_const",
        "The falsum induction case.",
        "Ultraproducts.lean:101", 6),
    row("B-EQUALITY", "branch", "branch", "high",
        "Transfer equality formulas through term evaluation and quotient equality.",
        "BoundedFormula.equal branch",
        "The equality induction case.",
        "Ultraproducts.lean:102-108", 16),
    row("B-RELATION", "branch", "branch", "high",
        "Transfer relation atoms through term evaluation and quotient relation semantics.",
        "BoundedFormula.rel branch",
        "The relation induction case.",
        "Ultraproducts.lean:109-115", 16),
    row("B-IMPLICATION", "branch", "branch", "critical",
        "Transfer implication using both induction hypotheses and maximality of the ultrafilter.",
        "BoundedFormula.imp branch; Ultrafilter.eventually_imp",
        "The implication induction case.",
        "Ultraproducts.lean:116-118", 10),
    row("B-UNIVERSAL", "branch", "branch", "critical",
        "Transfer universal quantification by quotient representatives and factorwise counterexample choice.",
        "BoundedFormula.all branch",
        "The universal-quantifier induction case.",
        "Ultraproducts.lean:119-144", 46),
    row("T-TERM", "transport", "bridge", "high",
        "Show term evaluation commutes with the quotient injection of factorwise assignments.",
        "FirstOrder.Language.Ultraproduct.term_realize_cast",
        "Term values in the product are represented by factorwise term values.",
        "Ultraproducts.lean:82-90", 20,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.Ultraproduct.term_realize_cast"),
    row("C-PRESTRUCTURE", "construction", "construction", "critical",
        "Construct the filter-product prestructure and prove function and relation interpretations respect the product setoid.",
        "FirstOrder.Language.Ultraproduct.setoidPrestructure and structure",
        "A well-defined language structure on the quotient product.",
        "Ultraproducts.lean:49-75", 44,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.Ultraproduct.setoidPrestructure"),
    row("L-FUNMAP", "lemma", "core_lemma", "high",
        "Identify quotient function interpretation with the class of factorwise function interpretation.",
        "FirstOrder.Language.Ultraproduct.funMap_cast",
        "The function-symbol compatibility used by term induction.",
        "Ultraproducts.lean:77-80", 10,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.Ultraproduct.funMap_cast"),
    row("L-QUOT-EQ", "lemma", "core_lemma", "high",
        "Characterize equality of product quotient classes by equality on an ultrafilter-large set.",
        "Quotient.eq''",
        "The quotient equality biconditional used by equality atoms.",
        "Ultraproducts.lean:102-108", 12,
        body=f"mathlib:{MATHLIB_REVISION}:Quotient.eq''"),
    row("L-QUOT-REL", "lemma", "core_lemma", "high",
        "Relate quotient relation interpretation to the ultrafilter-eventual factor relation.",
        "FirstOrder.Language.relMap_quotient_mk'",
        "The relation-symbol compatibility used by relation atoms.",
        "Ultraproducts.lean:109-115", 12,
        body=f"mathlib:{MATHLIB_REVISION}:FirstOrder.Language.relMap_quotient_mk'"),
    row("L-ULTRAFILTER-IMP", "lemma", "core_lemma", "critical",
        "Use ultrafilter maximality to commute eventual implication with implication of eventual propositions.",
        "Ultrafilter.eventually_imp",
        "The implication semantic bridge.",
        "Ultraproducts.lean:116-118", 12,
        body=f"mathlib:{MATHLIB_REVISION}:Ultrafilter.eventually_imp"),
    row("L-QUOT-FORALL", "lemma", "core_lemma", "critical",
        "Replace universal quantification over quotient classes by universal quantification over representatives.",
        "Quotient.forall",
        "Representative-level quantification for the universal branch.",
        "Ultraproducts.lean:121-125", 12,
        body=f"mathlib:{MATHLIB_REVISION}:Quotient.forall"),
    row("T-SNOC", "transport", "transport", "high",
        "Commute factorwise evaluation with extension of the bound-variable assignment by Fin.snoc.",
        "the h' assignment equality and Fin.comp_snoc",
        "The assignment identity required by the quantifier induction hypothesis.",
        "Ultraproducts.lean:126-134", 20),
    row("C-EPSILON", "construction", "construction", "critical",
        "Choose one counterexample witness in every factor when eventual universal satisfaction fails.",
        "Classical.epsilon and Classical.epsilon_spec",
        "A factorwise representative contradicting quotient-level universal satisfaction.",
        "Ultraproducts.lean:135-142", 18,
        body=f"mathlib:{MATHLIB_REVISION}:Classical.epsilon"),
    row("L-EVENTUAL-SET", "lemma", "core_lemma", "high",
        "Use eventual-set membership and monotonicity to pass between the chosen representative and every representative.",
        "Filter.eventually_iff and Filter.mem_of_superset",
        "The reverse direction of the universal branch.",
        "Ultraproducts.lean:142-144", 14),
    row("X-SOURCE", "terminal", "terminal", "critical",
        "Pinpoint and independently review the primary Los proof, exact assumptions, definitions, edition, and errata for every mathematical node.",
        "primary-source packet and independent review pending",
        "Human-source coverage without machine proof credit.",
        "source-statement-crosswalk.md", 70,
        machine="not_applicable"),
    row("X-PROVENANCE", "terminal", "certificate", "critical",
        "Bind the wrapper, three terminal bodies, supporting declarations, immutable source blobs, imports, revisions, and aliases without duplicate credit.",
        "future content-addressed terminal-body provenance closure",
        "Complete formal provenance without semantic proof credit.",
        "anchor-audit.json exact candidate route", 50,
        machine="informational", human="not_applicable"),
    row("X-TRUST", "terminal", "certificate", "critical",
        "Audit transitive declarations, compiled artifacts, axioms, unsafe and oracle boundaries, licenses, replay, and supply-chain trust.",
        "Lean 4.29.0 and mathlib 8a178386 release-grade trust packet",
        "Release-grade trust coverage without semantic proof credit.",
        "anchor-audit-receipt.json nonrelease closure", 50,
        machine="informational", human="not_applicable"),
    row("X-READABLE", "terminal", "terminal", "high",
        "Produce and independently review a complete node-anchored reconstruction of the bounded-formula induction.",
        "future proof outline, long reconstruction, and reader receipt",
        "Readable coverage without machine proof credit.",
        "obligation-tree.md is architecture only", 80,
        machine="not_applicable"),
    row("X-WORKFLOW", "terminal", "certificate", "critical",
        "Bind dependency-legal proof, validation, source, readability, freshness, revocation, independent verification, and release tasks.",
        "Stage1 execution and receipt closure pending",
        "Workflow acceptance without mathematical proof credit.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json", 30,
        machine="informational", human="not_applicable"),
]


REQUIRES = {
    oid("ROOT"): [oid("T-ADAPTER")],
    oid("T-ADAPTER"): [oid("A-SENTENCE")],
    oid("A-SENTENCE"): [oid("A-FORMULA")],
    oid("A-FORMULA"): [oid("A-BOUNDED")],
    oid("A-BOUNDED"): [oid("B-FALSUM"), oid("B-EQUALITY"), oid("B-RELATION"),
                       oid("B-IMPLICATION"), oid("B-UNIVERSAL")],
    oid("B-EQUALITY"): [oid("T-TERM"), oid("L-QUOT-EQ")],
    oid("B-RELATION"): [oid("T-TERM"), oid("L-QUOT-REL")],
    oid("B-IMPLICATION"): [oid("L-ULTRAFILTER-IMP")],
    oid("B-UNIVERSAL"): [oid("L-QUOT-FORALL"), oid("T-SNOC"), oid("C-EPSILON"),
                         oid("L-EVENTUAL-SET")],
    oid("T-TERM"): [oid("L-FUNMAP")],
    oid("L-FUNMAP"): [oid("C-PRESTRUCTURE")],
}

CHECKED_COMPOSITIONS = {
    oid("ROOT"): "Stage1Instances.THM_M_0673_Obligations.root_of_terminal",
    oid("T-ADAPTER"): "Stage1Instances.THM_M_0673_Obligations.terminal_of_sentence",
    oid("A-SENTENCE"): "Stage1Instances.THM_M_0673_Obligations.sentence_of_formula",
    oid("A-FORMULA"): "Stage1Instances.THM_M_0673_Obligations.formula_of_bounded",
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    nodes = []
    for spec in ROWS:
        identifier = spec["id"]
        if identifier in {oid("ROOT"), oid("S-INTERFACE")}:
            fingerprint = "lean-expression-sha256:" + ROOT_EXPRESSION
        else:
            fingerprint = "planned:v1:sha256:" + digest([
                identifier, spec["reg_kind"], spec["claim"], spec["formal"], spec["output"],
            ])
        excluded = spec["machine"] != "required" or spec["human"] != "required"
        exclusion = None
        if excluded:
            exclusion = {
                "code": (
                    "human_source_boundary_only" if spec["machine"] == "not_applicable"
                    else "assurance_or_formal_overlay_no_independent_proof_credit"
                ),
                "justification": "This node's typed role excludes the inapplicable metric; its other required roles remain in the frozen denominator.",
                "approval": "pending independent Stage1 integration review",
            }
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": spec["reg_kind"],
            "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")},
            "machine_eligibility": spec["machine"],
            "human_source_eligibility": spec["human"],
            "readable_eligibility": "required",
            "risk_class": spec["risk"],
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": spec["body"],
        })
        if identifier in CHECKED_COMPOSITIONS:
            validity_state = "provisional_interface_check"
            validated_at = "2026-07-15"
        else:
            validity_state = "structurally_validated_not_proof_accepted"
            validated_at = "2026-07-15"
        if identifier == oid("ROOT"):
            provenance = "anchor-audit:M0673-C01-MATHLIB-EXACT"
        elif identifier in {oid("A-SENTENCE"), oid("A-FORMULA"), oid("A-BOUNDED")}:
            provenance = "anchor-audit:pinned-visible-terminal-chain"
        else:
            provenance = "none"
        owned = []
        if identifier in CHECKED_COMPOSITIONS:
            owned = ["Stage1_Instances/THM-M-0673/ObligationTree.lean"]
        elif identifier == oid("S-BOUNDARY"):
            owned = ["Stage1_Instances/THM-M-0673/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{spec['short']}",
            "obligation_id": identifier,
            "kind": spec["node_kind"],
            "human_statement": spec["claim"],
            "formal_target": spec["formal"],
            "output": spec["output"],
            "human_debt": "H1",
            "machine_debt": "M3" if spec["machine"] == "required" else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "primary-source-node-map-pending" if spec["human"] == "required"
                else "not-applicable-pending-independent-review"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; propext, Classical.choice, Quot.sound candidate policy acceptance pending",
            "tcb_profile": "Lean-4.29.0+mathlib-8a178386; release-grade transitive and independent review pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": "split-required" if identifier in REQUIRES else spec["budget"],
            "semantic_step_ledger": [{
                "step_id": f"STEP-{identifier}-01",
                "premise_ids": REQUIRES.get(identifier, ["FROZEN-FORMAL-CONTEXT"]),
                "inference": spec["formal"],
                "source_locator": spec["locator"],
                "output": spec["output"],
                "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
                "status": (
                    "checked_interface" if identifier in CHECKED_COMPOSITIONS
                    else "planned_substantive_not_proof_accepted"
                ),
            }],
            "public_readable_target": f"Stage1_Instances/THM-M-0673/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditional interface only; no proof-phase M0, accepted root closure, audit completion, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0673-PROOF"],
            "owned_sources": owned,
            "owner": "THM-M-0673 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": validated_at,
                "review_due": "before proof acceptance and on every invalidation input change",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "typed-graphs.json", "ObligationTree.lean", "toolchain and dependency pins"],
                "revocation_state": validity_state,
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{field: value[field] for field in fields} for value in obligations])
    identifiers = [value["obligation_id"] for value in obligations]
    registry_scope = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "lifecycle_mode": "executing",
        "registry_id": "THM-M-0673-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-15T00:00:00+08:00",
        "freeze_basis": "Exact elaborated statement plus immutable bounded anchor inventory. Eligibility is fixed from the source-visible semantic architecture independently of candidate closure credit.",
        "freeze_order_boundary": "The ROWS and eligibility table are declared before build() reads or records candidate status.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_statement_expression_sha256": ROOT_EXPRESSION,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "canonical_projection_fields": list(fields),
        "frozen_denominators": {
            "inventory": identifiers,
            "required_machine": [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"],
            "required_human_source": [value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"],
            "required_readable": identifiers,
            "informational_overlays": [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "normalization": {"status": "not_applicable_pending_independent_approval", "reason": "The statement already uses mathlib's canonical filter-product quotient; no representative, symmetry, order, finite/infinite, or local/global normalization precedes the proof."},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "No solver, reflection, enumeration, native code, oracle, experiment, or certificate participates in the route."},
        },
        "mandatory_layer_analysis": {
            "S": [oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-FOUNDATION")],
            "N": [],
            "B": [oid("B-FALSUM"), oid("B-EQUALITY"), oid("B-RELATION"), oid("B-IMPLICATION"), oid("B-UNIVERSAL")],
            "C": [oid("C-PRESTRUCTURE"), oid("C-EPSILON")],
            "L": [oid("A-BOUNDED"), oid("L-FUNMAP"), oid("L-QUOT-EQ"), oid("L-QUOT-REL"), oid("L-ULTRAFILTER-IMP"), oid("L-QUOT-FORALL"), oid("L-EVENTUAL-SET")],
            "X": [oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "T": [oid("T-ADAPTER"), oid("A-SENTENCE"), oid("A-FORMULA"), oid("T-TERM"), oid("T-SNOC")],
            "not_applicable_layers": ["N: no normalization route; pending independent approval", "X/computation: no computation; pending independent approval"],
        },
        "proof_body_aliases": {
            "sentence_realize": "terminal wrapper over realize_formula_cast; no independent semantic root credit",
            "realize_formula_cast": "terminal wrapper over boundedFormula_realize_cast; no independent duplicate coverage",
            "exactTarget_mathlib_candidate": "local audit wrapper; no relocated or duplicate proof-body credit",
        },
        "delta_policy": "Any correction, split, merge, exclusion, eligibility/risk change, or terminal-body identity change requires registry version 2 and an append-only old/new semantic-ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
    }
    registry_sha256 = digest(registry_scope)
    registry = {
        **registry_scope,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_COMPOSITIONS),
            "audited_candidate_obligations": [oid("A-SENTENCE"), oid("A-FORMULA"), oid("A-BOUNDED")],
            "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact mathlib candidate is not installed or accepted; H0, R0, audit completion, validation, release, and theorem completion remain open.",
        "registry_sha256": registry_sha256,
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str,
             reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    proof = []
    decomposition = []
    for parent, children in REQUIRES.items():
        for child in children:
            if parent in CHECKED_COMPOSITIONS:
                request = f"REQ-{parent}-{child}"
                compose = f"CMP-{child}-{parent}"
                proof.extend([
                    edge(request, parent, "proof_requires", child, compose),
                    edge(compose, child, "composes", parent, request),
                ])
            else:
                logical = f"DEC-{parent}-{child}"
                refinement = f"REF-{child}-{parent}"
                decomposition.extend([
                    edge(logical, parent, "logical_decomposition", child, refinement),
                    edge(refinement, child, "refines", parent, logical),
                ])
    math_ids = [
        value for value in identifiers
        if value not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
    ]
    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("EQ-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE"), "EQ-INTERFACE-ROOT"),
            edge("EQ-INTERFACE-ROOT", oid("S-INTERFACE"), "equivalent_to", oid("ROOT"), "EQ-ROOT-INTERFACE"),
            edge("EXP-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
            *decomposition,
        ],
        "provenance": [
            *[edge(f"PROV-{target}", oid("X-PROVENANCE"), "provenance_of", target) for target in math_ids],
            *[edge(f"SRC-{target}", oid("X-SOURCE"), "source_map", target)
              for target in identifiers
              if target != oid("X-SOURCE")
              and next(value for value in obligations if value["obligation_id"] == target)["human_source_eligibility"] == "required"],
        ],
        "evidence": [
            edge("EVID-PROVENANCE-BOUNDED", oid("X-PROVENANCE"), "evidence_for", oid("A-BOUNDED")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-BOUNDED-CLOSURE", oid("A-BOUNDED"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            *[edge(f"DOC-{target}", oid("X-READABLE"), "documents", target)
              for target in identifiers if target != oid("X-READABLE")],
        ],
        "workflow": [
            edge("FLOW-PROOF", oid("X-WORKFLOW"), "workflow_depends_on", oid("A-BOUNDED")),
            edge("FLOW-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
            edge("FLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
        ],
    }
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in identifiers}
        incoming = {identifier: [] for identifier in identifiers}
        for value in graph_edges[name]:
            outgoing[value["from"]].append(value["edge_id"])
            incoming[value["to"]].append(value["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "lifecycle_mode": "executing",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_version": 1,
        "registry_denominator_sha256": denominator,
        "registry_sha256": registry_sha256,
        "root_node_id": f"{THEOREM}-ROOT",
        "root_obligation_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "reciprocal_edge_type_contract": {
            "proof_requires": "composes", "composes": "proof_requires",
            "logical_decomposition": "refines", "refines": "logical_decomposition",
            "equivalent_to": "equivalent_to"
        },
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [
            {"parent_obligation_id": parent, "declaration": declaration,
             "required_child_ids": REQUIRES[parent], "status": "checked_conditional_no_child_closure_credit"}
            for parent, declaration in CHECKED_COMPOSITIONS.items()
        ],
        "unverified_decomposition_plans": [
            {"parent_obligation_id": parent, "required_child_ids": children,
             "status": "typed_plan_requires_proof_phase_composition_certificate"}
            for parent, children in REQUIRES.items() if parent not in CHECKED_COMPOSITIONS
        ],
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_COMPOSITIONS),
            "candidate_only_obligations": [oid("A-SENTENCE"), oid("A-FORMULA"), oid("A-BOUNDED")],
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("A-BOUNDED"), oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "reason": "All local composition checks are conditional; the pinned candidate remains uninstalled and unaccepted until proof-phase and master validation.",
        },
    }

    declarations = {
        oid("ROOT"): ["Stage1Instances.THM_M_0673.LosSentenceTarget", CHECKED_COMPOSITIONS[oid("ROOT")]],
        oid("T-ADAPTER"): [CHECKED_COMPOSITIONS[oid("T-ADAPTER")]],
        oid("A-SENTENCE"): ["FirstOrder.Language.Ultraproduct.sentence_realize", CHECKED_COMPOSITIONS[oid("A-SENTENCE")]],
        oid("A-FORMULA"): ["FirstOrder.Language.Ultraproduct.realize_formula_cast", CHECKED_COMPOSITIONS[oid("A-FORMULA")]],
        oid("A-BOUNDED"): ["FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast"],
        oid("T-TERM"): ["FirstOrder.Language.Ultraproduct.term_realize_cast"],
        oid("C-PRESTRUCTURE"): ["FirstOrder.Language.Ultraproduct.setoidPrestructure"],
        oid("L-FUNMAP"): ["FirstOrder.Language.Ultraproduct.funMap_cast"],
    }
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "lifecycle_mode": "executing",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "registry_sha256": registry_sha256,
        "recipes": [],
        "status_boundary": "Node-scoped structural and conditional-interface recipes only; proof, release, and theorem completion are not covered.",
    }
    for identifier in identifiers:
        recipes["recipes"].append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0673/check_obligation_tree.py"],
            "env_allowlist": {"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0673 obligation tree"}],
            "covered_obligation_ids": [identifier] if identifier in CHECKED_COMPOSITIONS else [],
            "covered_declarations": declarations.get(identifier, []),
            "coverage_boundary": (
                "exact conditional interface coverage without child or root closure credit"
                if identifier in CHECKED_COMPOSITIONS else
                "structural architecture and declaration-presence coverage only; no M0 or proof-closure credit"
            ),
        })
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values,
    ):
        (HERE / name).write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")
    print(f"registry scope sha256: {values[0]['registry_sha256']}")


if __name__ == "__main__":
    main()
