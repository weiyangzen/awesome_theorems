#!/usr/bin/env python3
"""Build the frozen THM-M-0931 obligation registry and typed graph bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0931-OBLIGATION_TREE"
THEOREM = "THM-M-0931"
PREFIX = "M0931-"
REGISTRY_ID = "THM-M-0931-OBLIGATIONS-v1"
ROOT_EXPRESSION = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EGZ_BLOB = "dbe223c73d6c612461bc900d3d7dd70be3c1d747"
CHEVALLEY_BLOB = "144087d302ebc67510cc3cf6903ab84706326b41"
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


EGZ_BODY = f"mathlib4@{MATHLIB_REVISION}:{EGZ_BLOB}"
CW_BODY = f"mathlib4@{MATHLIB_REVISION}:{CHEVALLEY_BLOB}"

# short id, kind, risk, claim, formal target, output, machine eligibility,
# human-source eligibility, readable eligibility, terminal body, budget,
# substantive inference, source locator
ROWS = (
    (
        "ROOT", "root", "critical",
        "For positive n, exactly 2n-1 integer occurrences contain exactly n occurrences whose sum is divisible by n.",
        "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget",
        "The exact frozen positive exact-count multiset proposition.",
        "required", "required", "required", None, 12,
        "Consume the exact terminal package, the at-least-count anchor, and the exact-count transport without changing any canonical binder.",
        "Stage1_Instances/THM-M-0931/Statement.lean",
    ),
    (
        "S-INTERFACE", "definition", "critical",
        "Freeze n : Nat with 0 < n, Multiset Int occurrence semantics, exact input and witness cardinalities, submultiset selection, and integer divisibility.",
        "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget",
        "The canonical binders, hypotheses, witness, and conclusion.",
        "informational", "not_applicable", "required", None, 16,
        "Read the fully elaborated target and preserve occurrence multiplicity, binder order, casts, and divisibility exactly.",
        "Stage1_Instances/THM-M-0931/statement.json",
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Exclude n=0 but retain n=1, repeated and all-equal values, negative integers, and the exact natural subtraction boundary.",
        "Statement mutations and checked boundary fixtures",
        "The full canonical boundary policy and no broadened theorem.",
        "informational", "required", "required", None, 24,
        "Use positivity and exact-cardinality mutations to distinguish the source-shaped root from the all-natural stronger candidate.",
        "Stage1_Instances/THM-M-0931/statement.json",
    ),
    (
        "S-COUNT-TRANSPORT", "transport", "high",
        "Specialize the all-natural at-least-count multiset proposition to the positive exact-count source proposition.",
        "Stage1Instances.THM_M_0931.ObligationTree.ExactCountTransport",
        "AtLeastCountAnchor implies the exact canonical root.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0931/ObligationTree.lean#exactCountTransport_checked", 16,
        "Turn input-cardinality equality into the required lower bound and leave positivity, witness cardinality, and divisibility unchanged.",
        "Stage1_Instances/THM-M-0931/ObligationTree.lean",
    ),
    (
        "S-RESIDUE-TRANSPORT", "transport", "high",
        "Relate divisibility of the selected integer sum by n to equality of its cast with zero in ZMod n.",
        "Stage1Instances.THM_M_0931.erdosGinzburgZivTarget_iff_residueTarget",
        "A checked bidirectional statement transport with the same integer occurrences.",
        "informational", "required", "required",
        "local:Stage1_Instances/THM-M-0931/Statement.lean#erdosGinzburgZivTarget_iff_residueTarget", 14,
        "Apply ZMod.intCast_zmod_eq_zero_iff_dvd without changing the input carrier or selected submultiset.",
        "Stage1_Instances/THM-M-0931/Statement.lean",
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit Lean dependent type theory, propext, Classical.choice, Quot.sound, compiled artifacts, and the no-oracle computation policy.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation, TCB, and computation boundary.",
        "informational", "not_applicable", "required", None, 42,
        "Compare exact machine-derived axioms and executables with the selected foundation and TCB profiles.",
        "Stage1_Instances/THM-M-0931/anchor-audit.json",
    ),
    (
        "T-ROOT-COMPOSE", "terminal", "critical",
        "Compose the at-least-count anchor and exact-count transport into the exact canonical root.",
        "Stage1Instances.THM_M_0931.ObligationTree.root_of_terminal_packages",
        "ErdosGinzburgZivTarget from every explicit terminal child.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0931/ObligationTree.lean#root_of_terminal_packages", 18,
        "Consume RootComposition, AtLeastCountAnchor, and ExactCountTransport, yielding the full frozen target.",
        "Stage1_Instances/THM-M-0931/ObligationTree.lean",
    ),
    (
        "A-MULTISET-EGZ", "bridge", "critical",
        "Every integer multiset with at least 2n-1 occurrences has an n-occurrence submultiset whose sum is divisible by n.",
        "Stage1Instances.THM_M_0931.ObligationTree.AtLeastCountAnchor",
        "The exact at-least-count anchor consumed by source specialization.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv_multiset", 18,
        "Use the indexed integer theorem on occurrence enumeration and map selected indices back to a submultiset.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:192-195",
    ),
    (
        "N-ENUMERATE", "normalization", "critical",
        "Enumerate duplicate-preserving multiset occurrences by value-index pairs and transport an indexed selection back to a submultiset.",
        "Stage1Instances.THM_M_0931.ObligationTree.MultisetEnumerationTransport",
        "IndexedIntegerEGZ implies AtLeastCountAnchor.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0931/ObligationTree.lean#multisetEnumerationTransport_checked", 28,
        "Apply the indexed package to toEnumFinset, then use map_fst_le_of_subset_toEnumFinset and the enumeration sum/cardinality identities.",
        "Stage1_Instances/THM-M-0931/ObligationTree.lean",
    ),
    (
        "L-INDEXED-EGZ", "core_lemma", "critical",
        "For an indexed finite set of at least 2n-1 integers, select n indices whose indexed sum is divisible by n.",
        "Stage1Instances.THM_M_0931.ObligationTree.IndexedIntegerEGZ",
        "The indexed theorem consumed by occurrence enumeration.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv", 22,
        "Perform prime-composite induction on n, with explicit zero, one, prime, and composite branches.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:110-178",
    ),
    (
        "B-INDUCTION", "branch", "critical",
        "Nat.prime_composite_induction exhaustively separates n into zero, one, prime, or a product of two factors at least two.",
        "Nat.prime_composite_induction specialized to IndexedIntegerEGZ",
        "Exhaustive branch recomposition for the indexed theorem.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv", 28,
        "Generalize the index type and recompose the four induction constructors into the indexed conclusion.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:113-129",
    ),
    (
        "B-ZERO", "branch", "normal",
        "At n=0, the all-natural stronger indexed theorem selects the empty subset.",
        "Int.erdos_ginzburg_ziv zero branch",
        "The indexed EGZ conclusion at n=0, without source-root credit.",
        "required", "not_applicable", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv", 8,
        "Choose the empty finset and discharge subset, cardinality, and zero-divisibility goals.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:116-117",
    ),
    (
        "B-ONE", "branch", "normal",
        "At n=1, select a one-element subset from the cardinality lower bound.",
        "Int.erdos_ginzburg_ziv one branch",
        "The indexed EGZ conclusion at n=1.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv", 10,
        "Apply exists_subset_card_eq and simplify divisibility by one.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:118-119",
    ),
    (
        "B-PRIME", "branch", "critical",
        "For prime p, trim to exactly 2p-1 indices and invoke the integer prime case.",
        "Int.erdos_ginzburg_ziv prime branch",
        "The indexed EGZ conclusion for prime modulus.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv", 20,
        "Install Fact p.Prime, choose an exact-cardinality subset, apply the prime theorem, and compose subset inclusion.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:120-125",
    ),
    (
        "T-PRIME-CAST", "transport", "critical",
        "Transport the ZMod p zero-sum prime theorem back to integer divisibility by p.",
        "Int.erdos_ginzburg_ziv_prime",
        "The integer prime indexed EGZ conclusion.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv_prime", 18,
        "Cast integer summands into ZMod p, commute cast with the finite sum, and apply the cast-zero iff divisibility equivalence.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:92-99",
    ),
    (
        "L-ZMOD-PRIME", "core_lemma", "critical",
        "For prime p and exactly 2p-1 ZMod p entries, select p indices whose sum is zero.",
        "ZMod.erdos_ginzburg_ziv_prime",
        "The prime zero-sum selection used by the integer cast transport.",
        "required", "required", "required",
        f"{EGZ_BODY}#ZMod.erdos_ginzburg_ziv_prime", 24,
        "Construct two polynomials, count common roots via Chevalley-Warning, choose a nonzero common root, and extract its support.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:52-90",
    ),
    (
        "C-POLYNOMIALS", "construction", "critical",
        "Construct f1 as the sum of X_i^(p-1) and f2 as the coefficient-weighted sum over the input residues.",
        "private f1 and f2 in the pinned EGZ module",
        "Two well-typed multivariate polynomials whose common roots encode cardinality and sum.",
        "required", "required", "required", None, 22,
        "Form both finite polynomial sums over the exact index set and preserve coefficients in ZMod p.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:34-41",
    ),
    (
        "L-DEGREE-BOUND", "core_lemma", "critical",
        "The total degrees of f1 and f2 sum to less than 2p-1 variables.",
        "totalDegree_f1_add_totalDegree_f2",
        "The strict degree inequality required by binary Chevalley-Warning.",
        "required", "required", "required", None, 28,
        "Bound each finite-sum degree by p-1, add the bounds, and use primality to prove strictness.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:43-50",
    ),
    (
        "X-CHEVALLEY-WARNING", "bridge", "critical",
        "When two multivariate polynomials over a finite field have total-degree sum below the number of variables, the characteristic divides their common-root count.",
        "char_dvd_card_solutions_of_add_lt",
        "Divisibility by p of the common-root count for f1 and f2.",
        "required", "required", "required",
        f"{CW_BODY}#char_dvd_card_solutions_of_add_lt", 34,
        "Encode the binary family by Bool and invoke the finite-family Chevalley-Warning theorem after normalizing the degree sum.",
        "Mathlib/FieldTheory/ChevalleyWarning.lean:184-194",
    ),
    (
        "L-NONZERO-SOLUTION", "core_lemma", "critical",
        "The zero assignment is a common root, and p-divisibility with p at least two forces a distinct nonzero common root.",
        "zero_sol, hN0, hpN and Fintype.exists_ne_of_one_lt_card",
        "A common root distinct from the zero assignment.",
        "required", "required", "required", None, 30,
        "Show the common-root subtype is inhabited by zero, combine positive cardinality with p divisibility, then select a second element.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:60-73",
    ),
    (
        "L-PRIME-CARD", "core_lemma", "critical",
        "The support of a nonzero common root has positive cardinality divisible by p and less than 2p, hence exactly p.",
        "support cardinality extraction in ZMod.erdos_ginzburg_ziv_prime",
        "A selected support with cardinality p.",
        "required", "required", "required", None, 36,
        "Use the f1 equation for divisibility, nonzeroness for positivity, and the ambient 2p-1 bound for strictness.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:74-88",
    ),
    (
        "L-PRIME-SUM", "core_lemma", "critical",
        "The f2 common-root equation makes the input residues sum to zero over the selected support.",
        "support sum extraction in ZMod.erdos_ginzburg_ziv_prime",
        "Zero sum of the p selected residues.",
        "required", "required", "required", None, 18,
        "Rewrite the weighted polynomial evaluation using the ZMod power identity and Finset.sum_filter.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:89-90",
    ),
    (
        "B-COMPOSITE", "branch", "critical",
        "For n=m*k with both factors at least two, build 2m-1 disjoint k-blocks and select m blocks by the outer induction hypothesis.",
        "Int.erdos_ginzburg_ziv composite branch",
        "The indexed EGZ conclusion for composite modulus.",
        "required", "required", "required",
        f"{EGZ_BODY}#Int.erdos_ginzburg_ziv", 30,
        "Apply the inner induction to form disjoint blocks, apply the outer induction to normalized block sums, and union the chosen blocks.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:126-178",
    ),
    (
        "C-DISJOINT-BLOCKS", "construction", "critical",
        "Maintain a family of k disjoint input subsets, each of size n and each having sum divisible by n.",
        "the family A invariant in the composite branch",
        "A disjoint block family parameterized by k <= 2m-1.",
        "required", "required", "required", None, 30,
        "Package family cardinality, pairwise disjointness, input containment, block size, and divisibility as one invariant.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:130-135",
    ),
    (
        "L-INNER-INDUCTION", "core_lemma", "critical",
        "Extend the disjoint block family from k to k+1 by applying the n-induction hypothesis to unused indices.",
        "the induction k construction in the composite branch",
        "The disjoint-block invariant for every k <= 2m-1.",
        "required", "required", "required", None, 45,
        "Prove enough unused indices remain, select a new n-block, prove it is new and disjoint, and preserve all invariants.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:146-178",
    ),
    (
        "L-OUTER-INDUCTION", "core_lemma", "critical",
        "Apply the m-induction hypothesis to the quotients of the 2m-1 block sums by n and choose m blocks.",
        "the ihm invocation in the composite branch",
        "A subfamily of m blocks whose normalized sums are divisible by m.",
        "required", "required", "required", None, 24,
        "Define each block value as its integer sum divided by n and apply indexed EGZ at modulus m.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:135-139",
    ),
    (
        "T-COMPOSITE-ASSEMBLE", "terminal", "critical",
        "Union the chosen disjoint blocks, obtaining mn indices and a total sum divisible by mn.",
        "the biUnion terminal assembly in the composite branch",
        "The complete composite indexed EGZ conclusion.",
        "required", "required", "required", None, 32,
        "Use disjoint biUnion cardinality, sum_biUnion, exact block divisibility, integer division, and the outer divisibility result.",
        "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean:139-145",
    ),
    (
        "X-SOURCE", "terminal", "high",
        "Pinpoint and independently review the 1961 prime and multiplicative-composite proof against every material obligation.",
        "primary-source node map and independent review pending",
        "Human-source coverage without machine proof credit.",
        "not_applicable", "required", "required", None, 70,
        "Map the source's indexed prime argument, multiplicative closure, positivity convention, and occurrence semantics to stable node IDs.",
        "Stage1_Instances/THM-M-0931/source-statement-crosswalk.md",
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Bind the local wrappers, private and public terminal bodies, source blobs, revisions, imports, aliases, and license without duplicate credit.",
        "content-addressed transitive declaration provenance closure",
        "Release-grade body provenance without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 55,
        "Trace the root candidate through the multiset wrapper, indexed induction, prime private bodies, and Chevalley-Warning source boundary.",
        "Stage1_Instances/THM-M-0931/anchor-audit.json",
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit toolchain, compiled artifacts, axioms, unsafe and oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0 and pinned mathlib transitive trust closure",
        "Release trust evidence without proof credit.",
        "informational", "not_applicable", "required", None, 55,
        "Recompute the declaration, executable, artifact, axiom, and no-oracle closure in a hermetic verifier.",
        "Stage1_Instances/THM-M-0931/anchor-audit.json",
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide and independently review a complete readable reconstruction of the prime and composite routes.",
        "node-specific readable reconstruction and review pending",
        "Readable proof coverage without machine proof credit.",
        "not_applicable", "not_applicable", "required", None, 90,
        "Expand every high-risk bridge into premise-to-inference-to-output steps and obtain an independent mathematical reading decision.",
        "Stage1_Instances/THM-M-0931/obligation-tree.md",
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind dependency-legal proof, validation, release, freshness, revocation, and independent-verification acceptance.",
        "Stage1 rev-5.6 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 30,
        "Require accepted predecessors before proof adoption and accepted proof, validation, and release receipts before terminal decisions.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    ),
)


# Only exact abstract-child harnesses belong in the machine proof graph. The
# visible source-body expansion remains a typed logical plan until exact child
# interfaces and parent compositions are checked in later proof work.
REQUIRES = {
    oid("ROOT"): [oid("T-ROOT-COMPOSE"), oid("A-MULTISET-EGZ"), oid("S-COUNT-TRANSPORT")],
    oid("A-MULTISET-EGZ"): [oid("L-INDEXED-EGZ"), oid("N-ENUMERATE")],
}

CERTIFICATES = {
    oid("ROOT"): "Stage1Instances.THM_M_0931.ObligationTree.root_of_terminal_packages",
    oid("A-MULTISET-EGZ"): "Stage1Instances.THM_M_0931.ObligationTree.atLeastCountAnchor_of_indexed_and_enumeration",
}

LOGICAL_PLANS = {
    oid("L-INDEXED-EGZ"): [oid("B-INDUCTION")],
    oid("B-INDUCTION"): [oid("B-ZERO"), oid("B-ONE"), oid("B-PRIME"), oid("B-COMPOSITE")],
    oid("B-PRIME"): [oid("T-PRIME-CAST")],
    oid("T-PRIME-CAST"): [oid("L-ZMOD-PRIME")],
    oid("L-ZMOD-PRIME"): [
        oid("C-POLYNOMIALS"), oid("L-DEGREE-BOUND"),
        oid("X-CHEVALLEY-WARNING"), oid("L-NONZERO-SOLUTION"),
        oid("L-PRIME-CARD"), oid("L-PRIME-SUM"),
    ],
    oid("B-COMPOSITE"): [oid("C-DISJOINT-BLOCKS"), oid("L-INNER-INDUCTION"), oid("L-OUTER-INDUCTION"), oid("T-COMPOSITE-ASSEMBLE")],
}


def edge(edge_id: str, source: str, edge_type: str, target: str,
         reciprocal: str | None = None) -> dict:
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


def build() -> tuple[dict, dict, dict]:
    statement_hash = file_digest("Statement.lean")
    anchor_hash = file_digest("anchor-audit.json")
    obligations: list[dict] = []
    nodes: list[dict] = []

    exclusions = {
        oid("S-INTERFACE"): "formal_statement_overlay_no_duplicate_machine_or_source_credit_pending_review",
        oid("S-BOUNDARY"): "formal_boundary_overlay_no_duplicate_machine_proof_credit_pending_review",
        oid("S-RESIDUE-TRANSPORT"): "alternate_encoding_overlay_no_duplicate_root_machine_credit_pending_review",
        oid("S-FOUNDATION"): "trust_governance_overlay_no_mathematical_proof_credit_pending_review",
        oid("B-ZERO"): "stronger_candidate_boundary_outside_positive_human_source_root_pending_review",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-TRUST"): "trust_overlay_no_mathematical_proof_credit_pending_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_mathematical_proof_credit_pending_review",
    }
    checked_local = {
        oid("S-COUNT-TRANSPORT"), oid("S-RESIDUE-TRANSPORT"),
        oid("T-ROOT-COMPOSE"), oid("N-ENUMERATE"),
    }

    for short, kind, risk, claim, formal, output, machine, human, readable, body, budget, inference, locator in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")}
            else "planned:v1:sha256:" + digest([identifier, kind, claim, formal, output])
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": identifier not in {
                oid("S-RESIDUE-TRANSPORT"), oid("X-PROVENANCE"),
                oid("X-TRUST"), oid("X-WORKFLOW"),
            },
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })
        if identifier in checked_local:
            machine_debt = "M0-L"
            provenance = "local-conditional-composition"
        elif identifier in {oid("A-MULTISET-EGZ"), oid("L-INDEXED-EGZ")}:
            machine_debt = "M0-W"
            provenance = "anchor-audit:M0931-C01-MATHLIB-INT-MULTISET"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
            provenance = "none"
        else:
            machine_debt = "M4"
            provenance = "pinned-visible-source-route" if identifier not in {
                oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-FOUNDATION"),
                oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            } else "pending"
        premise_ids = ["frozen-formal-context"]
        if identifier in REQUIRES:
            premise_ids = REQUIRES[identifier]
        elif identifier in LOGICAL_PLANS:
            premise_ids = LOGICAL_PLANS[identifier]
        elif identifier in {oid("A-MULTISET-EGZ"), oid("L-INDEXED-EGZ"), oid("X-CHEVALLEY-WARNING")}:
            premise_ids = ["pinned-mathlib-source"]
        step = {
            "step_id": f"STEP-{identifier}-01",
            "premise_ids": premise_ids,
            "inference": inference,
            "source_locator": locator,
            "output": output,
            "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
        }
        owned_sources: list[str] = []
        if identifier in checked_local or identifier == oid("T-ROOT-COMPOSE"):
            owned_sources = ["Stage1_Instances/THM-M-0931/ObligationTree.lean"]
        if identifier == oid("S-RESIDUE-TRANSPORT"):
            owned_sources = ["Stage1_Instances/THM-M-0931/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if human == "not_applicable"
                else "primary-source-node-map-pending"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; propext/Classical.choice/Quot.sound policy review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": [step],
            "public_readable_target": f"Stage1_Instances/THM-M-0931/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": "VAL-M0931-OBLIGATION-BUNDLE",
            "status_boundary": "Frozen architecture, candidate, or conditional interface only; no accepted M0 root, source/readable closure, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0931-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0931 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in checked_local else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in checked_local else "open",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{key: row[key] for key in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact elaborated positive exact-count statement, bounded immutable anchor audit, and visible pinned proof architecture. Eligibility and denominators are frozen without accepting candidate closure.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "additional_symmetry_sign_order_or_representative_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The occurrence enumeration is explicit; the target and visible route use no symmetry, sign, order, representative, finite/infinite, or local/global normalization beyond it.",
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, numerical approximation, native evaluator, oracle, experiment, or external certificate participates in the visible proof route.",
            },
        },
        "delta_policy": "Any target change, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
        "obligations": obligations,
        "append_only_delta": [],
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "accepted_root_machine_debt": "M3",
            "candidate_route": "Pinned mathlib M0-W candidate remains unaccepted and below release evidence E1.",
        },
        "status_boundary": "Architecture only; no obligation is accepted closed and both terminal decisions remain false.",
    }

    proof_edges: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            request = f"REQ-{parent}-{child}"
            compose = f"CMP-{child}-{parent}"
            proof_edges.append(edge(request, parent, "proof_requires", child, compose))
            proof_edges.append(edge(compose, child, "composes", parent, request))

    refinement_edges: list[dict] = [
        edge("REF-ROOT-INTERFACE", oid("ROOT"), "expository_decomposition", oid("S-INTERFACE")),
        edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
        edge("REF-ROOT-RESIDUE", oid("ROOT"), "equivalent_to", oid("S-RESIDUE-TRANSPORT")),
    ]
    for parent, children in LOGICAL_PLANS.items():
        for child in children:
            refinement_edges.append(edge(f"LOG-{parent}-{child}", parent, "logical_decomposition", child))

    provenance_edges = [
        edge("PROV-MULTISET", oid("X-PROVENANCE"), "provenance_of", oid("A-MULTISET-EGZ")),
        edge("PROV-INDEXED", oid("X-PROVENANCE"), "provenance_of", oid("L-INDEXED-EGZ")),
        edge("PROV-CW", oid("X-PROVENANCE"), "provenance_of", oid("X-CHEVALLEY-WARNING")),
        edge("SRC-PRIME", oid("B-PRIME"), "source_map", oid("X-SOURCE")),
        edge("SRC-COMPOSITE", oid("B-COMPOSITE"), "source_map", oid("X-SOURCE")),
    ]
    evidence_edges: list[dict] = []
    trust_edges = [
        edge("TRUST-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TRUST-RELEASE", oid("ROOT"), "trusts", oid("X-TRUST")),
    ]
    documentation_edges = [
        edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
        edge("DOC-PRIME", oid("X-READABLE"), "documents", oid("B-PRIME")),
        edge("DOC-COMPOSITE", oid("X-READABLE"), "documents", oid("B-COMPOSITE")),
        edge("DOC-SOURCE", oid("X-SOURCE"), "documents", oid("ROOT")),
    ]
    workflow_nodes = [
        "S56-M-0931-STATEMENT", "S56-M-0931-ANCHOR_AUDIT", ITEM,
        "S56-M-0931-PROOF", "S56-M-0931-VALIDATION", "S56-M-0931-RELEASE",
    ]
    workflow_edges = [
        edge(f"FLOW-{index}", workflow_nodes[index], "workflow_depends_on", workflow_nodes[index - 1])
        for index in range(1, len(workflow_nodes))
    ]

    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}
    certificates = []
    for parent, children in REQUIRES.items():
        certificates.append({
            "certificate_id": f"CERT-{parent}",
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": fingerprints[parent],
            "required_child_ids": children,
            "required_child_statement_fingerprints": {child: fingerprints[child] for child in children},
            "declaration": CERTIFICATES[parent],
            "certificate_kind": "lean_abstract_child_harness",
            "introduces_undeclared_premises": False,
            "status": "provisionally_elaborated_not_accepted",
        })
    unverified = [{
        "plan_id": f"DECOMP-{parent}",
        "parent_obligation_id": parent,
        "planned_child_ids": children,
        "source_declaration": nodes[ids.index(parent)]["formal_target"],
        "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
        "required_future_certificate": "An exact abstract-child harness must bind these fingerprints and consume every child before parent closure.",
    } for parent, children in LOGICAL_PLANS.items()]
    graphs = {
        "proof": graph(proof_edges),
        "refinement": graph(refinement_edges),
        "provenance": graph(provenance_edges),
        "evidence": graph(evidence_edges),
        "trust": graph(trust_edges),
        "documentation": graph(documentation_edges),
        "workflow": graph(workflow_edges),
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
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
            "proof_leaf_cut_set": [oid("L-INDEXED-EGZ"), oid("N-ENUMERATE"), oid("S-COUNT-TRANSPORT")],
            "remaining_root_cut_set": [
                oid("A-MULTISET-EGZ"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"),
                oid("X-WORKFLOW"),
            ],
        },
    }
    recipe = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [{
            "recipe_id": "VAL-M0931-OBLIGATION-BUNDLE",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0931/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 240,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains PASS THM-M-0931 obligation tree and accepted obligations 0",
            }],
            "covered_obligation_ids": ids,
            "covered_declarations": [
                "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget",
                "Stage1Instances.THM_M_0931.ObligationTree.multisetEnumerationTransport_checked",
                "Stage1Instances.THM_M_0931.ObligationTree.atLeastCountAnchor_of_indexed_and_enumeration",
                "Stage1Instances.THM_M_0931.ObligationTree.exactCountTransport_checked",
                "Stage1Instances.THM_M_0931.ObligationTree.rootComposition_checked",
                "Stage1Instances.THM_M_0931.ObligationTree.root_of_terminal_packages",
                "Int.erdos_ginzburg_ziv_multiset", "Int.erdos_ginzburg_ziv",
                "char_dvd_card_solutions_of_add_lt",
            ],
            "closure_credit": False,
        }],
    }
    return registry, bundle, recipe


def serialized(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, bundle, recipes = build()
    outputs = {
        "obligation-registry.json": registry,
        "typed-graphs.json": bundle,
        "validation-specs.json": recipes,
    }
    check_only = args.check
    for name, value in outputs.items():
        data = serialized(value)
        path = HERE / name
        if check_only:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f"stale generated artifact: {name}")
        else:
            path.write_bytes(data)
    action = "checked" if check_only else "wrote"
    edge_count = sum(len(graph_value["edges"]) for graph_value in bundle["graphs"].values())
    print(f"{action} {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
