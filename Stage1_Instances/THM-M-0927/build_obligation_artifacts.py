#!/usr/bin/env python3
"""Build the frozen THM-M-0927 obligation registry and typed graphs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0927-OBLIGATION_TREE"
THEOREM = "THM-M-0927"
PREFIX = "M0927-"
REGISTRY_ID = "THM-M-0927-OBLIGATIONS-v1"
ROOT_EXPRESSION = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GOLDEN_BLOB = "9e9a9f050354f828a54fb235846405987daa4971"
LINEAR_RECURRENCE_BLOB = "e644c74090240f527cc982d19d1e5f7cf342a387"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def spec(
    short: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    budget: int,
    inference: str,
    locator: str,
    *,
    machine: str = "required",
    human: str = "required",
    readable: str = "required",
    body: str | None = None,
    root_relevant: bool = True,
) -> dict:
    return {
        "short": short,
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "budget": budget,
        "inference": inference,
        "locator": locator,
        "machine": machine,
        "human": human,
        "readable": readable,
        "body": body,
        "root_relevant": root_relevant,
    }


ROWS = [
    spec(
        "ROOT", "root", "critical",
        "For every natural n, the zero-based Fibonacci number equals the frozen DLMF radical expression.",
        "Stage1Instances.THM_M_0927.BinetFormulaTarget",
        "The complete frozen BinetFormulaTarget.", 10,
        "Consume the exact root composition, function Binet package, and both one-directional transports without changing the natural binder or radical expression.",
        "Stage1_Instances/THM-M-0927/Statement.lean:17-22",
    ),
    spec(
        "S-INTERFACE", "definition", "critical",
        "Preserve the universal Nat binder, zero-based Nat.fib, Real codomain, ordinary powers, positive square root, and source radical denominator.",
        "Stage1Instances.THM_M_0927.BinetFormulaTarget",
        "The exact canonical binder, domain, coercion, roots, denominator, and equality interface.", 18,
        "Read the elaborated expression and preserve every binder, coercion, exponent, subtraction, multiplication, and division node.",
        "Stage1_Instances/THM-M-0927/statement.json",
        machine="informational", human="not_applicable",
    ),
    spec(
        "S-BOUNDARY", "branch", "high",
        "Include n=0 and n=1, exclude no natural index, and reject deletion of the conjugate term or changes to domain and binder scope.",
        "Statement mutation failures and zero_index_formula/one_index_formula",
        "The exact boundary and mutation policy for the canonical statement.", 24,
        "Use four rejected structural mutations plus the checked zero and one witnesses to keep the canonical source boundary distinct.",
        "Stage1_Instances/THM-M-0927/Statement.lean:68-145",
        machine="informational",
    ),
    spec(
        "S-FUNCTION-TRANSPORT", "transport", "high",
        "Convert equality of the Fibonacci and named-root functions into pointwise equality at every natural index.",
        "Stage1Instances.THM_M_0927.ObligationTree.FunctionToPointwiseTransport",
        "FunctionNamedRootPackage implies PointwiseNamedRootPackage.", 6,
        "Apply congrFun to the exact function equality at an arbitrary natural index.",
        "Stage1_Instances/THM-M-0927/ObligationTree.lean#functionToPointwiseTransport_checked",
        human="not_applicable",
    ),
    spec(
        "S-RADICAL-TRANSPORT", "transport", "critical",
        "Normalize the named characteristic roots into the source's explicit powers of (1 plus or minus sqrt 5) divided by 2^n.",
        "Stage1Instances.THM_M_0927.ObligationTree.NamedRootToRadicalTransport",
        "PointwiseNamedRootPackage implies BinetFormulaTarget.", 18,
        "Reuse the checked statement iff and unfold only the named-root abbreviations, preserving the binder and result direction.",
        "Stage1_Instances/THM-M-0927/ObligationTree.lean#namedRootToRadicalTransport_checked",
        human="not_applicable",
    ),
    spec(
        "S-FOUNDATION", "certificate", "critical",
        "Audit Lean dependent type theory, propext, Classical.choice, Quot.sound, compiled artifacts, and the no-oracle computation policy.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation, computation, and TCB boundary.", 42,
        "Compare machine-derived declaration axioms and executable inputs with the selected foundation and trust profiles.",
        "Stage1_Instances/THM-M-0927/anchor-audit.json",
        machine="informational", human="not_applicable",
    ),
    spec(
        "N-ROOT-SPELLING", "normalization", "high",
        "Identify Real.goldenRatio and Real.goldenConj with the two explicit roots and normalize powers of quotients to the source denominator.",
        "Real.goldenRatio; Real.goldenConj; div_pow; ring normalization",
        "The checked named-root-to-radical equality used by the final transport.", 15,
        "Unfold both root abbreviations, distribute natural powers over division, and prove the resulting field identity by ring normalization.",
        "Stage1_Instances/THM-M-0927/Statement.lean:51-64",
        human="not_applicable",
    ),
    spec(
        "N-FUNCTION-POINTWISE", "normalization", "normal",
        "Relate a function equality on Nat to its pointwise dependent-equality form without duplicating the substantive proof body.",
        "Function.funext_iff; congrFun",
        "A reversible representation bridge between function and pointwise forms.", 6,
        "Use function extensionality in one direction and congruence at an arbitrary argument in the other.",
        "Stage1_Instances/THM-M-0927/Statement.lean:44-49",
        machine="informational", human="not_applicable", root_relevant=False,
    ),
    spec(
        "L-RECURRENCE-DEFINITION", "definition", "high",
        "Define the order-two Fibonacci recurrence with coefficient vector [1,1] and expose its characteristic polynomial.",
        "Real.fibRec; Real.fibRec_charPoly_eq",
        "The exact recurrence and characteristic polynomial used by all solution packages.", 20,
        "Unfold LinearRecurrence.charPoly for order two and simplify the finite coefficient sum to X^2-(X+1).",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:143-156",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.fibRec_charPoly_eq",
    ),
    spec(
        "L-FIB-SOLUTION", "core_lemma", "critical",
        "The real coercion of Nat.fib satisfies the order-two Fibonacci recurrence.",
        "Real.fib_isSol_fibRec",
        "A recurrence-solution witness for n maps to Nat.fib n in Real.", 18,
        "Unfold fibRec, rewrite Nat.fib_add_two, commute the two summands, and simplify the Fin 2 sum.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:160-166",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.fib_isSol_fibRec",
    ),
    spec(
        "L-PHI-SOLUTION", "core_lemma", "critical",
        "The geometric sequence n maps to goldenRatio^n satisfies the Fibonacci recurrence.",
        "Real.geom_goldenRatio_isSol_fibRec",
        "A recurrence-solution witness for the positive characteristic root.", 14,
        "Apply the geometric-solution/characteristic-root equivalence, rewrite the characteristic polynomial, and verify the root equation.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:168-171",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.geom_goldenRatio_isSol_fibRec",
    ),
    spec(
        "L-PSI-SOLUTION", "core_lemma", "critical",
        "The geometric sequence n maps to goldenConj^n satisfies the Fibonacci recurrence.",
        "Real.geom_goldenConj_isSol_fibRec",
        "A recurrence-solution witness for the conjugate characteristic root.", 14,
        "Apply the geometric-solution/characteristic-root equivalence, rewrite the characteristic polynomial, and verify the conjugate root equation.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:173-176",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.geom_goldenConj_isSol_fibRec",
    ),
    spec(
        "C-RHS-SOLUTION", "construction", "critical",
        "Construct the scaled difference of the two geometric recurrence solutions and identify it with the named-root Binet function.",
        "Real.fibRec.solSpace.sub_mem; Submodule.smul_mem; Pi.sub_apply",
        "The named-root right-hand side is a solution of the Fibonacci recurrence.", 25,
        "Scale each geometric solution by inverse sqrt 5, subtract them in the solution submodule, then use pointwise algebra to recover division by sqrt 5.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:188-195",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.coe_fib_eq'",
    ),
    spec(
        "B-INITIAL-CASES", "branch", "critical",
        "The Fibonacci sequence and named-root expression agree exhaustively at every index below recurrence order two.",
        "Real.coe_fib_eq' initial-value fin_cases branch",
        "Set.EqOn equality on Finset.range Real.fibRec.order.", 12,
        "Normalize membership in range two, split exhaustively into indices zero and one, and recompose both exact equalities.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:183-186",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.coe_fib_eq'",
    ),
    spec(
        "B-INITIAL-ZERO", "branch", "normal",
        "At initial index zero, both the zero-based Fibonacci sequence and the named-root expression equal zero.",
        "Real.coe_fib_eq' index-zero branch",
        "Equality of the two recurrence solutions at index zero.", 7,
        "Simplify Nat.fib 0, both zeroth powers, their difference, and division by sqrt 5.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:184-186",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.coe_fib_eq'",
    ),
    spec(
        "B-INITIAL-ONE", "branch", "normal",
        "At initial index one, both the zero-based Fibonacci sequence and the named-root expression equal one.",
        "Real.coe_fib_eq' index-one branch",
        "Equality of the two recurrence solutions at index one.", 9,
        "Simplify Nat.fib 1 and first powers, then use the exact difference of the two named roots over sqrt 5.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:184-186",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.coe_fib_eq'",
    ),
    spec(
        "X-RECURRENCE-UNIQUENESS", "bridge", "critical",
        "Two solutions of one linear recurrence are equal when they agree at every index below the recurrence order.",
        "LinearRecurrence.sol_eq_of_eq_init",
        "Function equality from two solution witnesses and equality on the initial range.", 32,
        "Embed both sequences in the solution submodule, compare their initial-value images through the linear equivalence, and reflect equality back to functions.",
        "Mathlib/Algebra/LinearRecurrence.lean:127-152",
        body=f"mathlib:{MATHLIB_REVISION}:{LINEAR_RECURRENCE_BLOB}#LinearRecurrence.sol_eq_of_eq_init",
    ),
    spec(
        "T-FUNCTION-BINET", "terminal", "critical",
        "Compose recurrence uniqueness, both recurrence-solution witnesses, solution-space closure, and initial values into Binet's formula as a function equality.",
        "Real.coe_fib_eq'",
        "FunctionNamedRootPackage.", 24,
        "Invoke recurrence-solution uniqueness, discharge the two initial cases, and supply the Fibonacci and scaled-difference solution witnesses.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:180-195",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.coe_fib_eq'",
    ),
    spec(
        "T-POINTWISE-BINET", "terminal", "high",
        "Turn the substantive function-equality theorem into the pointwise named-root theorem without assigning a second terminal body.",
        "Real.coe_fib_eq",
        "PointwiseNamedRootPackage.", 6,
        "Rewrite the dependent equality goal through funext_iff and consume Real.coe_fib_eq'.",
        "Mathlib/NumberTheory/Real/GoldenRatio.lean:197-199",
        machine="informational",
        body=f"mathlib:{MATHLIB_REVISION}:{GOLDEN_BLOB}#Real.coe_fib_eq'",
        root_relevant=False,
    ),
    spec(
        "T-ROOT-COMPOSE", "terminal", "critical",
        "Compose the substantive named-root function theorem with function-to-pointwise and radical-spelling transports into the exact root.",
        "Stage1Instances.THM_M_0927.ObligationTree.root_of_terminal_packages",
        "The exact frozen BinetFormulaTarget from all declared terminal children.", 12,
        "Consume FunctionNamedRootPackage, FunctionToPointwiseTransport, and NamedRootToRadicalTransport through the exact RootComposition harness.",
        "Stage1_Instances/THM-M-0927/ObligationTree.lean#root_of_terminal_packages",
        human="not_applicable",
    ),
    spec(
        "X-SOURCE", "terminal", "high",
        "Pinpoint and independently review a complete primary proof, exact conventions, historical attribution, assumptions, corrections, and errata.",
        "primary-source proof packet and independent review pending",
        "Human-source coverage without machine-proof credit.", 45,
        "Admit exact source editions, map every material recurrence step and boundary, audit Binet attribution and errata, and obtain independent review.",
        "Stage1_Instances/THM-M-0927/source-statement-crosswalk.md",
        machine="not_applicable",
    ),
    spec(
        "X-PROVENANCE", "certificate", "critical",
        "Bind the pointwise wrapper, unique function body, source blobs, revisions, imports, aliases, candidate records, and licenses without duplicate credit.",
        "anchor-audit.json plus transitive declaration provenance",
        "Conclusion-to-body provenance without mathematical proof credit.", 40,
        "Trace the exact root through local transports to Real.coe_fib_eq' and deduplicate Real.coe_fib_eq, Real.coe_intFib_eq, downstream wrappers, and historical variants.",
        "Stage1_Instances/THM-M-0927/anchor-audit.json",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-EVIDENCE", "certificate", "critical",
        "Bind exact recipes, outputs, statement fingerprints, axiom reports, placeholder checks, freshness, and invalidation inputs for every obligation.",
        "content-addressed node evidence bundle pending",
        "Replayable evidence without mathematical proof credit.", 40,
        "Execute each structured recipe against its exact declaration and registry version and reject stale or scope-mismatched results.",
        "Docs/Stage1_Blueprint_rev-5.6.md, Sections 9-10",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-TRUST", "certificate", "critical",
        "Close the Lean executable, compiled artifacts, axiom, unsafe, oracle, supply-chain, SBOM, and offline replay trust boundary.",
        "release foundation and TCB closure pending",
        "Accepted transitive trust evidence without mathematical proof credit.", 45,
        "Recompute terminal declaration closure in a clean network-denied environment and compare it with the selected profiles.",
        "Docs/Stage1_Blueprint_rev-5.6.md, Sections 7.4 and 10.6",
        machine="informational", human="not_applicable",
    ),
    spec(
        "X-READABLE", "terminal", "high",
        "Write and independently review a complete recurrence proof mapped to every substantive obligation and source boundary.",
        "node-specific readable reconstruction and review pending",
        "Readable coverage without machine-proof credit.", 45,
        "Explain definitions, recurrence solutions, solution-space closure, initial values, uniqueness, and both transports with stable node anchors.",
        "Stage1_Instances/THM-M-0927/obligation-tree.md",
        machine="not_applicable", human="not_applicable",
    ),
    spec(
        "X-WORKFLOW", "certificate", "high",
        "Enforce dependency-legal proof, validation, release, freshness, revocation, and independent-verification acceptance.",
        "Stage1 rev-5.6 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.", 24,
        "Require accepted predecessors before proof adoption and accepted proof, validation, and release receipts before terminal decisions.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        machine="informational", human="not_applicable",
    ),
]


# Only the exact root harness is represented as a certified proof graph. The
# pinned terminal body's source-shaped expansion remains an explicitly
# unverified logical plan until proof-phase exact child interfaces consume it.
REQUIRES = {
    oid("ROOT"): [
        oid("T-ROOT-COMPOSE"), oid("T-FUNCTION-BINET"),
        oid("S-FUNCTION-TRANSPORT"), oid("S-RADICAL-TRANSPORT"),
    ],
}

CERTIFICATES = {
    oid("ROOT"): "Stage1Instances.THM_M_0927.ObligationTree.root_of_terminal_packages",
}

LOGICAL_PLANS = {
    oid("T-FUNCTION-BINET"): [
        oid("X-RECURRENCE-UNIQUENESS"), oid("L-FIB-SOLUTION"),
        oid("C-RHS-SOLUTION"), oid("B-INITIAL-CASES"),
    ],
    oid("B-INITIAL-CASES"): [oid("B-INITIAL-ZERO"), oid("B-INITIAL-ONE")],
    oid("C-RHS-SOLUTION"): [oid("L-PHI-SOLUTION"), oid("L-PSI-SOLUTION")],
    oid("L-PHI-SOLUTION"): [oid("L-RECURRENCE-DEFINITION")],
    oid("L-PSI-SOLUTION"): [oid("L-RECURRENCE-DEFINITION")],
    oid("L-FIB-SOLUTION"): [oid("L-RECURRENCE-DEFINITION")],
    oid("T-POINTWISE-BINET"): [oid("T-FUNCTION-BINET"), oid("N-FUNCTION-POINTWISE")],
    oid("S-RADICAL-TRANSPORT"): [oid("N-ROOT-SPELLING")],
}


def edge(
    edge_id: str,
    source: str,
    edge_type: str,
    target: str,
    reciprocal: str | None = None,
) -> dict:
    result = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


def graph(edges: list[dict]) -> dict:
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict, str]:
    statement_hash = file_digest("Statement.lean")
    anchor_hash = file_digest("anchor-audit.json")
    tree_hash = file_digest("ObligationTree.lean")
    all_ids = [oid(row["short"]) for row in ROWS]
    checked_local = {
        oid("S-FUNCTION-TRANSPORT"), oid("S-RADICAL-TRANSPORT"),
        oid("N-ROOT-SPELLING"), oid("N-FUNCTION-POINTWISE"),
        oid("T-ROOT-COMPOSE"),
    }
    candidate_nodes = {
        oid("L-RECURRENCE-DEFINITION"), oid("L-FIB-SOLUTION"),
        oid("L-PHI-SOLUTION"), oid("L-PSI-SOLUTION"), oid("C-RHS-SOLUTION"),
        oid("B-INITIAL-CASES"), oid("B-INITIAL-ZERO"), oid("B-INITIAL-ONE"),
        oid("X-RECURRENCE-UNIQUENESS"),
        oid("T-FUNCTION-BINET"), oid("T-POINTWISE-BINET"),
    }
    source_only = {oid("X-SOURCE")}
    exclusions = {
        oid("S-INTERFACE"): "formal_interface_overlay_no_duplicate_machine_or_source_credit_pending_review",
        oid("S-BOUNDARY"): "formal_boundary_overlay_no_duplicate_machine_proof_credit_pending_review",
        oid("S-FUNCTION-TRANSPORT"): "formal_transport_has_no_separate_human_source_eligibility_pending_review",
        oid("S-RADICAL-TRANSPORT"): "formal_transport_has_no_separate_human_source_eligibility_pending_review",
        oid("S-FOUNDATION"): "foundation_overlay_no_mathematical_proof_credit_pending_review",
        oid("N-ROOT-SPELLING"): "formal_normalization_source_coverage_inherited_from_root_pending_review",
        oid("N-FUNCTION-POINTWISE"): "formal_representation_normalization_no_duplicate_source_credit_pending_review",
        oid("T-POINTWISE-BINET"): "pointwise_wrapper_overlay_no_duplicate_terminal_body_or_root_credit_pending_review",
        oid("T-ROOT-COMPOSE"): "formal_composition_has_no_separate_human_source_eligibility_pending_review",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-EVIDENCE"): "evidence_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-TRUST"): "trust_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_mathematical_proof_credit_pending_review",
    }
    obligations: list[dict] = []
    nodes: list[dict] = []
    for row in ROWS:
        identifier = oid(row["short"])
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")}
            else "planned:v1:sha256:" + digest([
                identifier, row["kind"], row["claim"], row["formal"], row["output"],
            ])
        )
        body = row["body"]
        local_declarations = {
            oid("S-FUNCTION-TRANSPORT"): "functionToPointwiseTransport_checked",
            oid("S-RADICAL-TRANSPORT"): "namedRootToRadicalTransport_checked",
            oid("T-ROOT-COMPOSE"): "rootComposition_checked",
        }
        if identifier in local_declarations:
            body = f"local-source-sha256:{tree_hash}#{local_declarations[identifier]}"
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": row["kind"],
            "root_relevant": row["root_relevant"],
            "machine_eligibility": row["machine"],
            "human_source_eligibility": row["human"],
            "readable_eligibility": row["readable"],
            "risk_class": row["risk"],
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })
        if identifier == oid("ROOT"):
            machine_debt = "M3"
            provenance = "none"
        elif identifier in checked_local:
            machine_debt = "M3"
            provenance = "local-provisional-interface"
        elif identifier in candidate_nodes:
            machine_debt = "M3"
            provenance = "anchor-audit:exact-pinned-mathlib-route-candidate"
        elif identifier in {oid("S-INTERFACE"), oid("S-BOUNDARY")}:
            machine_debt = "M3"
            provenance = "statement-phase-provisional"
        else:
            machine_debt = "M4"
            provenance = "pending"
        if identifier in REQUIRES:
            premise_ids = REQUIRES[identifier]
        elif identifier in LOGICAL_PLANS:
            premise_ids = LOGICAL_PLANS[identifier]
        elif identifier in source_only:
            premise_ids = ["frozen-source-context"]
        else:
            premise_ids = ["frozen-formal-context"]
        ledger = [{
            "step_id": f"STEP-{identifier}-01",
            "premise_ids": premise_ids,
            "inference": row["inference"],
            "source_locator": row["locator"],
            "output": row["output"],
            "outgoing_use": "Only a declared proof parent or typed non-proof edge may consume this exact output.",
        }]
        owned_sources: list[str] = []
        if identifier in {oid("S-FUNCTION-TRANSPORT"), oid("S-RADICAL-TRANSPORT"), oid("T-ROOT-COMPOSE")}:
            owned_sources = ["Stage1_Instances/THM-M-0927/ObligationTree.lean"]
        elif identifier in {oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("N-ROOT-SPELLING"), oid("N-FUNCTION-POINTWISE")}:
            owned_sources = ["Stage1_Instances/THM-M-0927/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{row['short']}",
            "obligation_id": identifier,
            "kind": row["kind"],
            "human_statement": row["claim"],
            "formal_target": row["formal"],
            "output": row["output"],
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review"
                if row["human"] == "not_applicable"
                else "DLMF-26.11-and-primary-proof-node-map-pending-independent-review"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; propext/Classical.choice/Quot.sound policy review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": row["budget"],
            "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-0927/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof, H0/R0 closure, audit completion, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0927-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0927 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-15" if identifier in checked_local else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "statement.json", "anchor-audit.json",
                    "obligation-registry.json", "typed-graphs.json",
                    "source-node map", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in checked_local else "open",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_version": 1,
        "frozen_at": "2026-07-15T16:30:00+08:00",
        "freeze_basis": "The exact elaborated DLMF radical statement, bounded immutable candidate audit, and source-shaped pinned recurrence proof body. Eligibility and denominators are frozen independently of proof acceptance; all observed candidate status is recorded only after the freeze.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "architecture_source_sha256": tree_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": all_ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "mandatory_layers": {
            "S": [oid(short) for short in ("S-INTERFACE", "S-BOUNDARY", "S-FUNCTION-TRANSPORT", "S-RADICAL-TRANSPORT", "S-FOUNDATION")],
            "N": [oid("N-ROOT-SPELLING"), oid("N-FUNCTION-POINTWISE")],
            "B": [oid("S-BOUNDARY"), oid("B-INITIAL-CASES"), oid("B-INITIAL-ZERO"), oid("B-INITIAL-ONE")],
            "C": [oid("C-RHS-SOLUTION")],
            "L": [oid(short) for short in ("L-RECURRENCE-DEFINITION", "L-FIB-SOLUTION", "L-PHI-SOLUTION", "L-PSI-SOLUTION")],
            "X": [oid(short) for short in ("X-RECURRENCE-UNIQUENESS", "X-SOURCE", "X-PROVENANCE", "X-EVIDENCE", "X-TRUST", "X-READABLE", "X-WORKFLOW")],
            "T": [oid("T-FUNCTION-BINET"), oid("T-POINTWISE-BINET"), oid("T-ROOT-COMPOSE")],
        },
        "layer_exclusions": {
            "additional_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The selected recurrence-uniqueness route has only the separately modeled two-case initial-value check. It contains no parity, prime, local/global, primitive/nonprimitive, or other mathematical branch.",
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, numerical approximation, native evaluator, solver, oracle, experiment, finite search, or external certificate proves the universal identity.",
            },
        },
        "proof_body_aliases": {
            "Real.coe_fib_eq": "pointwise wrapper over Real.coe_fib_eq'; no second terminal-body credit",
            "Real.coe_intFib_eq": "broader Int-index extension downstream of the natural theorem; no root or body credit",
            "Omega.Entropy.binet_formula": "external downstream wrapper over Real.coe_fib_eq; no independent body credit",
            "mathlib3.real.coe_fib_eq'": "historical wrong-backend predecessor; provenance only",
            "LeanCourse23.coe_fib_eq": "different Fibonacci definition and denominator, incompatible pins, and no checked exact transport",
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility/risk change, or proof-route/body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": sorted(checked_local),
            "audited_candidate_obligations": sorted(candidate_nodes),
            "audited_candidate_classification": "exact pinned mathlib M0-W route candidate pending proof-phase adoption and master acceptance",
            "accepted_root_machine_debt": "M3",
        },
        "status_boundary": "Architecture only. The exact pinned route is not installed or accepted; no obligation is accepted closed and both terminal decisions remain false.",
    }

    proof_edges: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            request = f"REQ-{parent}-{child}"
            compose = f"CMP-{child}-{parent}"
            proof_edges.append(edge(request, parent, "proof_requires", child, compose))
            proof_edges.append(edge(compose, child, "composes", parent, request))
    refinement_edges = [
        edge("REF-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
        edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
        edge("REF-POINTWISE-RADICAL", oid("T-POINTWISE-BINET"), "transports", oid("S-RADICAL-TRANSPORT")),
    ]
    for parent, children in LOGICAL_PLANS.items():
        for child in children:
            refinement_edges.append(edge(f"LOG-{parent}-{child}", parent, "logical_decomposition", child))
    provenance_edges = [
        edge("PROV-ROOT", oid("X-PROVENANCE"), "provenance_of", oid("ROOT")),
        edge("PROV-FUNCTION-BODY", oid("X-PROVENANCE"), "provenance_of", oid("T-FUNCTION-BINET")),
        edge("PROV-POINTWISE-WRAPPER", oid("X-PROVENANCE"), "provenance_of", oid("T-POINTWISE-BINET")),
        edge("PROV-UNIQUENESS", oid("X-PROVENANCE"), "provenance_of", oid("X-RECURRENCE-UNIQUENESS")),
        edge("SRC-ROOT", oid("ROOT"), "source_map", oid("X-SOURCE")),
        edge("SRC-FUNCTION", oid("T-FUNCTION-BINET"), "source_map", oid("X-SOURCE")),
    ]
    evidence_edges = [
        edge("EVIDENCE-STATEMENT", oid("X-EVIDENCE"), "evidence_for", oid("S-INTERFACE")),
        edge("EVIDENCE-ANCHOR", oid("X-EVIDENCE"), "evidence_for", oid("T-FUNCTION-BINET")),
        edge("EVIDENCE-COMPOSITION", oid("X-EVIDENCE"), "evidence_for", oid("T-ROOT-COMPOSE")),
    ]
    trust_edges = [
        edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TRUST-ROOT-RELEASE", oid("ROOT"), "trusts", oid("X-TRUST")),
        edge("TRUST-FUNCTION-BODY", oid("T-FUNCTION-BINET"), "trusts", oid("X-TRUST")),
        edge("TRUST-UNIQUENESS", oid("X-RECURRENCE-UNIQUENESS"), "trusts", oid("X-TRUST")),
    ]
    documentation_edges = [
        edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
        edge("DOC-RECURRENCE", oid("X-READABLE"), "documents", oid("T-FUNCTION-BINET")),
        edge("DOC-TRANSPORT", oid("X-READABLE"), "documents", oid("S-RADICAL-TRANSPORT")),
        edge("DOC-SOURCE", oid("X-SOURCE"), "documents", oid("ROOT")),
    ]
    workflow_nodes = [
        "S56-M-0927-STATEMENT", "S56-M-0927-ANCHOR_AUDIT", ITEM,
        "S56-M-0927-PROOF", "S56-M-0927-VALIDATION", "S56-M-0927-RELEASE",
    ]
    workflow_edges = [
        edge(f"FLOW-{index}", workflow_nodes[index], "workflow_depends_on", workflow_nodes[index - 1])
        for index in range(1, len(workflow_nodes))
    ]
    graphs = {
        "proof": graph(proof_edges),
        "refinement": graph(refinement_edges),
        "provenance": graph(provenance_edges),
        "evidence": graph(evidence_edges),
        "trust": graph(trust_edges),
        "documentation": graph(documentation_edges),
        "workflow": graph(workflow_edges),
    }
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}
    certificates = [{
        "certificate_id": f"CERT-{parent}",
        "parent_obligation_id": parent,
        "parent_statement_fingerprint": fingerprints[parent],
        "required_child_ids": children,
        "required_child_statement_fingerprints": {child: fingerprints[child] for child in children},
        "declaration": CERTIFICATES[parent],
        "certificate_kind": "lean_abstract_child_harness",
        "introduces_undeclared_premises": False,
        "status": "provisionally_elaborated_not_accepted",
    } for parent, children in REQUIRES.items()]
    unverified = [{
        "plan_id": f"DECOMP-{parent}",
        "parent_obligation_id": parent,
        "planned_child_ids": children,
        "source_locator": next(row["locator"] for row in ROWS if oid(row["short"]) == parent),
        "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
        "required_future_certificate": "An exact Lean abstract-child harness must bind these fingerprints and consume every child before parent closure.",
    } for parent, children in LOGICAL_PLANS.items()]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_direction": "proof_requires runs parent to child and reciprocal composes runs child to parent; logical plans run parent to child.",
        "nodes": nodes,
        "graphs": graphs,
        "workflow_task_nodes": workflow_nodes,
        "composition_certificates": certificates,
        "unverified_decomposition_plans": unverified,
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "minimal_open_machine_proof_cut_sets": [[oid("T-FUNCTION-BINET")]],
            "remaining_root_cut_set": [
                oid("T-FUNCTION-BINET"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "The exact pinned function theorem remains an audited candidate rather than an installed proof-phase child. Source, trust, evidence, readability, validation, release, and master acceptance remain open.",
        },
    }
    declaration_map = {
        oid("ROOT"): ["Stage1Instances.THM_M_0927.BinetFormulaTarget"],
        oid("S-FUNCTION-TRANSPORT"): ["Stage1Instances.THM_M_0927.ObligationTree.functionToPointwiseTransport_checked"],
        oid("S-RADICAL-TRANSPORT"): ["Stage1Instances.THM_M_0927.ObligationTree.namedRootToRadicalTransport_checked"],
        oid("T-FUNCTION-BINET"): ["Real.coe_fib_eq'"],
        oid("T-POINTWISE-BINET"): ["Real.coe_fib_eq"],
        oid("T-ROOT-COMPOSE"): [
            "Stage1Instances.THM_M_0927.ObligationTree.rootComposition_checked",
            "Stage1Instances.THM_M_0927.ObligationTree.root_of_terminal_packages",
        ],
    }
    recipes = [{
        "recipe_id": f"VAL-{identifier}",
        "cwd": ".",
        "argv": ["python3", "-B", "Stage1_Instances/THM-M-0927/check_obligation_tree.py"],
        "env_allowlist": {"LC_ALL": "C", "TZ": "UTC"},
        "timeout_seconds": 300,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{
            "path_or_stream": "stdout",
            "semantic_hash_policy": "contains PASS THM-M-0927 obligation tree and accepted obligations 0",
        }],
        "covered_obligation_ids": [identifier],
        "covered_declarations": declaration_map.get(identifier, []),
        "closure_credit": False,
    } for identifier in all_ids]
    validation = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": recipes,
    }
    lines = [
        "# THM-M-0927 frozen obligation architecture", "", "## Freeze boundary", "",
        f"Registry version 1 freezes {len(obligations)} canonical obligations before proof adoption.",
        "The denominator binds the exact radical statement and immutable anchor-audit snapshot.",
        "The architecture expands the pinned recurrence proof through recurrence definition,",
        "three solution witnesses, solution-space closure, initial values, uniqueness, wrappers,",
        "and exact source-spelling transport. No obligation is accepted closed.", "",
        "## Proof route", "", "```text",
        "M0927-ROOT exact radical BinetFormulaTarget",
        "|-- M0927-T-FUNCTION-BINET named-root function equality [open candidate cut]",
        "|   |-- M0927-X-RECURRENCE-UNIQUENESS",
        "|   |-- M0927-L-FIB-SOLUTION",
        "|   |-- M0927-C-RHS-SOLUTION",
        "|   |   |-- M0927-L-PHI-SOLUTION",
        "|   |   `-- M0927-L-PSI-SOLUTION",
        "|   `-- M0927-B-INITIAL-CASES",
        "|       |-- M0927-B-INITIAL-ZERO",
        "|       `-- M0927-B-INITIAL-ONE",
        "|-- M0927-S-FUNCTION-TRANSPORT",
        "`-- M0927-S-RADICAL-TRANSPORT",
        "```", "",
        "Only the exact abstract-child root harness belongs to the proof graph. Internal pinned",
        "body relations are typed logical-decomposition plans pending proof-phase child signatures",
        "and consuming composition certificates. Support graphs cannot close proof premises.", "",
        "## Node ledger", "",
    ]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        node = node_by_id[identifier]
        lines.extend([
            f"### {identifier.lower()}", "",
            f"Kind: `{node['kind']}`. Risk: `{obligation['risk_class']}`. Step budget: `{node['step_budget']}`.", "",
            f"Claim: {node['human_statement']}", "",
            f"Formal target: `{node['formal_target']}`", "",
            f"Output: {node['output']}", "", "Semantic ledger:", "",
        ])
        for index, step in enumerate(node["semantic_step_ledger"], 1):
            lines.append(f"{index}. `{step['step_id']}`: {step['inference']} Output: {step['output']}")
        lines.extend(["", f"Boundary: {node['status_boundary']}", ""])
    lines.extend([
        "## Closure boundary", "",
        "The minimal open machine-proof cut is `M0927-T-FUNCTION-BINET`. It has an exact pinned",
        "candidate but no proof-phase adoption or master acceptance. Primary-source H0, readable",
        "R0, provenance/evidence/TCB closure, hermetic replay, independent verification, validation,",
        "release, AUDIT-Z, and THEOREM-Z remain open. The root stays `[H1, M3, R4]`.", "",
    ])
    return registry, bundle, validation, "\n".join(lines)


def serialized(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, bundle, validation, readable = build()
    outputs = {
        "obligation-registry.json": serialized(registry),
        "typed-graphs.json": serialized(bundle),
        "validation-specs.json": serialized(validation),
        "obligation-tree.md": readable.encode(),
    }
    for name, data in outputs.items():
        path = HERE / name
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f"stale generated artifact: {name}")
        else:
            path.write_bytes(data)
    action = "checked" if args.check else "wrote"
    edge_count = sum(len(value["edges"]) for value in bundle["graphs"].values())
    print(f"{action} {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
