#!/usr/bin/env python3
"""Deterministically build the THM-M-0819 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
THEOREM = "THM-M-0819"
ITEM = "S56-M-0819-OBLIGATION_TREE"
PREFIX = "M0819-"
ROOT_EXPRESSION = "bdf0aa8f8adac4be9bf2080951be62eac168872b8c589a804ac8587c1878bb19"
ROOT_BUNDLE = "df437e79e306cbbdca0f9344a6a953a7f27886a197db7c614b995c846f8a2195"
GRAPH_NAMES = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
WORKFLOW_TASKS = (
    "S56-M-0819-INTAKE", "S56-M-0819-STATEMENT", "S56-M-0819-ANCHOR_AUDIT",
    ITEM, "S56-M-0819-PROOF", "S56-M-0819-VALIDATION", "S56-M-0819-RELEASE",
)
CHECKED_PARENT_DECLARATIONS = {
    PREFIX + "ROOT": "Stage1Instances.THM_M_0819_Obligations.root_of_terminal",
    PREFIX + "T-ROOT-ASSEMBLE": "Stage1Instances.THM_M_0819_Obligations.root_of_widthBranches",
    PREFIX + "T-WIDTH-BRANCHES": "Stage1Instances.THM_M_0819_Obligations.widthBranches_of_positive_and_zero",
}
INTERFACE_DECLARATIONS = {
    PREFIX + "ROOT": "Stage1Instances.THM_M_0819.DilworthPrimaryTarget",
    PREFIX + "S-TRANSPORT": "Stage1Instances.THM_M_0819_Obligations.RootTransportPackage",
    PREFIX + "B-WIDTH-ZERO": "Stage1Instances.THM_M_0819_Obligations.ZeroWidthPackage",
    PREFIX + "B-WIDTH-POSITIVE": "Stage1Instances.THM_M_0819_Obligations.PositiveWidthPackage",
    PREFIX + "T-WIDTH-BRANCHES": "Stage1Instances.THM_M_0819_Obligations.WidthBranchPackage",
    PREFIX + "T-ROOT-ASSEMBLE": "Stage1Instances.THM_M_0819_Obligations.TerminalRootPackage",
}
INTERFACE_EXPRESSION_FINGERPRINTS = {
    PREFIX + "ROOT": "lean-expression-sha256:" + ROOT_EXPRESSION,
    PREFIX + "S-TRANSPORT": "lean-expression-sha256:4d12a1039553ad6b5ebf5073265dbfb7796c8edef6b34662d6bec004b0e05761",
    PREFIX + "B-WIDTH-ZERO": "lean-expression-sha256:66084fe9adf3ca4e1de99c675afa46e28385f8a8ce38e14efeca4b2beabcaeff",
    PREFIX + "B-WIDTH-POSITIVE": "lean-expression-sha256:79fea9f6dbd89960ea2a381dd4c2faa783e2f1b2e3f41f3a1f54c01e2a8fc1d5",
    PREFIX + "T-WIDTH-BRANCHES": "lean-expression-sha256:f96b3dbfe2c7f0c4fceb18b389033f8b0aceb58022a2372a7e3bec7219b55824",
    PREFIX + "T-ROOT-ASSEMBLE": "lean-expression-sha256:8821dff5dca854aaab50210150eac4a66f27f11b9c843361b2f16f1bd6ac30d9",
}


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


ROWS = [
    row("ROOT", "root", "root", "critical",
        "For every partially ordered set and natural k, no (k+1)-element antichain plus an attained k-element antichain yields a disjoint Fin k-indexed chain decomposition.",
        "Stage1Instances.THM_M_0819.DilworthPrimaryTarget",
        "The exact arbitrary-poset target frozen by Statement.lean.",
        "Statement.lean:36-43; expression sha256 " + ROOT_EXPRESSION, 10),
    row("S-DEFINITIONS", "definition", "definition", "high",
        "Freeze exact finite cardinality, dependence, antichain, chain, and disjoint set-sum meanings.",
        "Stage1Instances.THM_M_0819.{HasExactly,IsDependent,IsDisjointChainDecomposition}",
        "The support definitions included in the statement-bundle identity.",
        "Statement.lean:16-31; bundle sha256 " + ROOT_BUNDLE, 20,
        machine="informational", human="not_applicable"),
    row("S-DOMAIN", "definition", "definition", "critical",
        "Retain an arbitrary possibly infinite carrier and natural finite width; do not substitute a finite-poset equality.",
        "forall (alpha : Type u) [PartialOrder alpha] (k : Nat), ...",
        "No Finite alpha assumption and no ENat minimum/maximum substitution.",
        "Statement.lean:38; statement.json domain_and_universes", 12,
        machine="informational", human="not_applicable"),
    row("S-TRANSPORT", "transport", "transport", "high",
        "Relate the support-predicate target to its direct expanded chain-family spelling only.",
        "Stage1Instances.THM_M_0819_Obligations.RootTransportPackage",
        "The checked Iff without a modern finite-equality transport.",
        "Statement.lean:45-61; dilworthPrimaryTarget_iff_expanded", 8,
        human="not_applicable"),
    row("S-FOUNDATION", "terminal", "certificate", "critical",
        "Audit classical choice, compactness, imported artifacts, the Lean kernel, and the no-oracle computation boundary.",
        "future transitive foundation and TCB packet for all exact terminal declarations",
        "An accepted foundation, trust, and computation profile.",
        "statement.json profiles; anchor-audit.json immutable_environment", 36,
        machine="informational", human="not_applicable"),
    row("N-FINITE-RESTRICTION", "reduction", "normalization", "critical",
        "Fix the global exact-k antichain A and enlarge each requested finite set s to the finite induced carrier s union A; restrict order and hdep while retaining A as an exact-k antichain.",
        "planned finite witness-closure package over s union A for DilworthPrimaryTarget",
        "A finite induced poset of exact width k containing s and the original witness A.",
        "finite-to-global architecture; exact Lean signature pending", 34),
    row("N-COLORING", "reduction", "normalization", "high",
        "Normalize a Fin k-indexed chain partition to a coloring whose equal-color fibers contain only comparable elements, and back.",
        "planned equivalence between IsDisjointChainDecomposition k and a proper Fin k coloring of incomparability",
        "A representation suitable for compactness and exact reconstruction of chain fibers.",
        "Statement.lean unique-membership representation; transport pending", 40),
    row("B-WIDTH-ZERO", "branch", "branch", "high",
        "Use dependence of every singleton to make the carrier empty and provide the unique zero-indexed decomposition.",
        "Stage1Instances.THM_M_0819_Obligations.ZeroWidthPackage",
        "The exact k=0 instance of the expanded target.",
        "Statement.lean:89-120; ObligationTree.lean zeroWidth_of_statement", 14,
        body="Stage1Instances.THM_M_0819_Obligations.zeroWidth_of_statement"),
    row("B-WIDTH-POSITIVE", "branch", "branch", "critical",
        "Prove the printed positive-width theorem without using the zero-width extension.",
        "Stage1Instances.THM_M_0819_Obligations.PositiveWidthPackage",
        "The exact expanded target for every 0<k.",
        "ObligationTree.lean PositiveWidthPackage; Dilworth 1950 Theorem 1.1", 14),
    row("C-LOCAL-COLORINGS", "construction", "construction", "critical",
        "For each finite s, apply exact finite Dilworth to the witness closure s union A and restrict its Fin k chain coloring back to s.",
        "planned (s : Finset alpha) -> (x : s) -> Fin k with local incomparability separation",
        "A total local-coloring family for Rado selection without falsely asserting that s itself contains an exact-k witness.",
        "finite-to-global plan; choice and nonempty Fin k boundary explicit", 42),
    row("L-FINITE-DILWORTH", "lemma", "bridge", "critical",
        "Prove exact finite Dilworth for a finite poset carrying the inherited k-antichain A and no (k+1)-antichain.",
        "planned finite-carrier exact-k chain-decomposition theorem",
        "A Fin k chain coloring on each finite witness closure s union A.",
        "Dilworth 1950 finite proof, pp.161-163; full tail not yet inspected", 70),
    row("B-FINITE-INDUCTION", "branch", "branch", "critical",
        "Use strong induction on width for smaller residual widths, nested with induction on finite carrier size by adjoining one element at fixed positive width k.",
        "planned nested width-and-cardinality induction package",
        "The exact finite theorem once both induction measures and successor construction close.",
        "Dilworth 1950 pp.161-162 inspected opening", 30),
    row("C-ADJOIN-ELEMENT", "construction", "construction", "critical",
        "Starting from the k singleton chains of the attained antichain, extend an already decomposed finite induced union by one outside element a and classify each existing chain into elements above, below, or incomparable with a.",
        "planned finite decomposition plus U_i/L_i/N_i construction",
        "The source's successor-step data and its chain invariants.",
        "Dilworth 1950 p.162", 44),
    row("L-LOW-WIDTH-INDEX", "lemma", "core_lemma", "critical",
        "Find an index m for which the source's upper/incomparable residual set has width below k, by the minimal-element contradiction argument.",
        "planned exact upper residual width lemma",
        "The first smaller-width subproblem used by induction.",
        "Dilworth 1950 p.162 inspected argument", 56),
    row("L-DUAL-INDEX", "lemma", "core_lemma", "critical",
        "Apply the order-dual argument to find the matching lower residual index.",
        "planned exact lower residual width lemma over OrderDual",
        "The second smaller-width subproblem used by induction.",
        "Dilworth 1950 p.162 inspected dual invocation", 30),
    row("X-FINITE-TAIL", "terminal", "bridge", "critical",
        "Recover and audit the uninspected remainder of the finite proof, including the exact recombination after the two residual-width reductions.",
        "planned finite-tail proof package; no statement is credited until the complete source is admitted",
        "The missing child-to-parent route from residual decompositions to finite Dilworth.",
        "Dilworth 1950 pp.162-163; lawful preview currently cuts off", 80),
    row("L-FINITE-EXACTNESS", "lemma", "core_lemma", "high",
        "Transport the global exact-k antichain into every finite witness closure s union A and show it also forces every final one-of-k global chain fiber nonempty, although nonemptiness is not required by the formal conclusion.",
        "planned witness-closure transport plus global pigeonhole/intersection compatibility lemma",
        "A lawful local exact-k premise and final source-width compatibility.",
        "Dilworth 1950 p.161 necessity argument; Statement.lean exact witness", 28),
    row("L-RADO-SELECTION", "lemma", "bridge", "critical",
        "Apply finite compactness/Rado selection to stitch local Fin k colorings into one global coloring.",
        "Finset.rado_selection_subtype specialized to beta := fun _ => Fin k",
        "A global color function locally agreeing with a coloring on a larger finite restriction.",
        "Mathlib.Combinatorics.Compactness:88; not in anchor inventory v1", 32,
        human="not_applicable"),
    row("C-GLOBAL-COLORING", "construction", "construction", "critical",
        "Construct the global Fin k coloring selected from all finite local colorings.",
        "planned chi : alpha -> Fin k returned by Finset.rado_selection_subtype",
        "A total color assignment on the arbitrary carrier.",
        "finite compactness architecture; exact Lean construction pending", 28),
    row("L-GLOBAL-PROPER", "lemma", "core_lemma", "critical",
        "For any two elements of the same global color, use agreement on a finite set containing both to prove they are comparable.",
        "planned forall x y, chi x = chi y -> x <= y or y <= x",
        "Every global color fiber is a chain.",
        "Rado finite-agreement consequence; pair finite set", 32),
    row("C-COLOR-CLASSES", "construction", "construction", "high",
        "Define C i as the fiber of the global coloring at i.",
        "planned C : Fin k -> Set alpha := fun i => {x | chi x = i}",
        "The Fin k-indexed family delivered to the canonical conclusion.",
        "Statement.lean IsDisjointChainDecomposition", 12),
    row("L-FIBERS-CHAIN", "lemma", "core_lemma", "critical",
        "Turn global same-color comparability into IsChain for every fiber.",
        "planned forall i, IsChain (fun x y : alpha => x <= y) (C i)",
        "The chain conjunct of IsDisjointChainDecomposition.",
        "IsChain definition plus L-GLOBAL-PROPER", 20),
    row("L-UNIQUE-MEMBERSHIP", "lemma", "core_lemma", "high",
        "Show every element belongs to exactly its color fiber.",
        "planned forall x : alpha, exists! i, x in C i",
        "Cover and pairwise disjointness in the exact unique-membership representation.",
        "fiber definition; equality in Fin k", 14),
    row("T-POSITIVE-ASSEMBLE", "terminal", "terminal", "critical",
        "Assemble finite restriction, finite Dilworth, compactness, global properness, and fiber invariants into PositiveWidthPackage.",
        "planned inhabitant of Stage1Instances.THM_M_0819_Obligations.PositiveWidthPackage",
        "The complete 0<k branch consumed by the checked root harness.",
        "ObligationTree.lean PositiveWidthPackage; composition pending", 24),
    row("T-WIDTH-BRANCHES", "terminal", "terminal", "critical",
        "Bundle the open positive-width theorem with the checked zero-width boundary theorem.",
        "Stage1Instances.THM_M_0819_Obligations.WidthBranchPackage",
        "Both exhaustive width branches.",
        "ObligationTree.lean widthBranches_of_positive_and_zero", 8,
        body="Stage1Instances.THM_M_0819_Obligations.widthBranches_of_positive_and_zero"),
    row("T-ROOT-ASSEMBLE", "terminal", "terminal", "critical",
        "Recompose the width split, expand the exact decomposition predicate, and transport to the canonical root.",
        "Stage1Instances.THM_M_0819_Obligations.TerminalRootPackage",
        "Stage1Instances.THM_M_0819.DilworthPrimaryTarget",
        "ObligationTree.lean expanded_of_widthBranches; root_of_widthBranches; root_of_terminal", 12,
        body="Stage1Instances.THM_M_0819_Obligations.root_of_widthBranches"),
    row("X-PRIMARY-SOURCE", "terminal", "terminal", "critical",
        "Map every mathematical node to a complete primary edition, corrections, assumptions, and independent review.",
        "future node-specific Dilworth 1950 source packet",
        "Human-source coverage without machine proof credit.",
        "source-statement-crosswalk.md; anchor-audit.json C09", 80,
        machine="not_applicable"),
    row("X-FINITE-CANDIDATE", "terminal", "bridge", "high",
        "Keep the immutable finite ENat equality candidate as nonexact research provenance and require explicit representation and finite-to-general transports before any use.",
        "vlad902/misc-lean-proofs@f82f920:minChainPartition_eq_antichainWidth",
        "No root proof credit; a successor integration task only.",
        "anchor-audit.json C06; current-pin failures at 397,404,597", 45,
        machine="informational", human="not_applicable"),
    row("X-RADO-PROVENANCE", "terminal", "certificate", "critical",
        "Create an append-only successor anchor inventory for the newly identified Rado bridge and audit its exact body, imports, license, axioms, and role.",
        "Finset.rado_selection_subtype provenance packet pending",
        "Reviewed bridge provenance without silently extending anchor inventory v1.",
        "Mathlib.Combinatorics.Compactness at pinned revision", 42,
        machine="informational", human="not_applicable"),
    row("X-PROVENANCE", "terminal", "certificate", "critical",
        "Bind every wrapper, terminal body, source slice, revision, dependency, and alias without duplicate proof-body credit.",
        "future content-addressed provenance closure",
        "Complete formal provenance without semantic proof credit.",
        "anchor-audit.json and future proof receipts", 50,
        machine="informational", human="not_applicable"),
    row("X-TRUST", "terminal", "certificate", "critical",
        "Audit transitive declarations, compiled artifacts, axioms, unsafe/oracle boundaries, compactness principles, and independent replay.",
        "Lean 4.29.0 and mathlib 8a178386 transitive closure pending",
        "Release-grade trust coverage without semantic proof credit.",
        "anchor-audit.json immutable_environment; ObligationTree.lean axiom probes", 50,
        machine="informational", human="not_applicable"),
    row("X-READABLE", "terminal", "terminal", "high",
        "Produce and independently review a complete node-anchored reconstruction, including the uninspected finite tail and compactness bridge.",
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
    oid("ROOT"): [oid("T-ROOT-ASSEMBLE")],
    oid("T-ROOT-ASSEMBLE"): [oid("S-TRANSPORT"), oid("T-WIDTH-BRANCHES")],
    oid("T-WIDTH-BRANCHES"): [oid("B-WIDTH-ZERO"), oid("B-WIDTH-POSITIVE")],
    oid("B-WIDTH-POSITIVE"): [oid("T-POSITIVE-ASSEMBLE")],
    oid("T-POSITIVE-ASSEMBLE"): [
        oid("N-FINITE-RESTRICTION"), oid("N-COLORING"), oid("C-LOCAL-COLORINGS"),
        oid("L-FINITE-DILWORTH"), oid("L-RADO-SELECTION"),
        oid("C-GLOBAL-COLORING"), oid("L-GLOBAL-PROPER"), oid("C-COLOR-CLASSES"),
        oid("L-FIBERS-CHAIN"), oid("L-UNIQUE-MEMBERSHIP"), oid("L-FINITE-EXACTNESS"),
    ],
    oid("C-LOCAL-COLORINGS"): [
        oid("N-FINITE-RESTRICTION"), oid("N-COLORING"),
        oid("L-FINITE-DILWORTH"), oid("L-FINITE-EXACTNESS"),
    ],
    oid("L-FINITE-DILWORTH"): [oid("B-FINITE-INDUCTION")],
    oid("B-FINITE-INDUCTION"): [
        oid("C-ADJOIN-ELEMENT"), oid("L-LOW-WIDTH-INDEX"),
        oid("L-DUAL-INDEX"), oid("X-FINITE-TAIL"),
    ],
    oid("L-LOW-WIDTH-INDEX"): [oid("C-ADJOIN-ELEMENT")],
    oid("L-DUAL-INDEX"): [oid("C-ADJOIN-ELEMENT")],
    oid("C-GLOBAL-COLORING"): [oid("C-LOCAL-COLORINGS"), oid("L-RADO-SELECTION")],
    oid("L-GLOBAL-PROPER"): [oid("C-GLOBAL-COLORING"), oid("C-LOCAL-COLORINGS")],
    oid("C-COLOR-CLASSES"): [oid("C-GLOBAL-COLORING")],
    oid("L-FIBERS-CHAIN"): [oid("L-GLOBAL-PROPER"), oid("C-COLOR-CLASSES")],
    oid("L-UNIQUE-MEMBERSHIP"): [oid("C-COLOR-CLASSES")],
}


CHECKED_INTERFACES = {
    oid("S-TRANSPORT"),
    oid("B-WIDTH-ZERO"), oid("T-WIDTH-BRANCHES"), oid("T-ROOT-ASSEMBLE"),
}

SUBSTANTIVE_LEDGERS = {
    "N-FINITE-RESTRICTION": [
        ("Choose the exact global antichain witness A and an equivalence A equiv Fin k.", "Statement.lean exact-k witness"),
        ("For each requested finite s, choose a finite representative a : Finset alpha for A and define t := s union a.", "Set.Finite/Finset conversion at the planned Lean boundary"),
        ("Equip the subtype t with the inherited partial order and embed A into t.", "Subtype order and Set.inclusion"),
        ("Restrict the no-(k+1)-antichain hypothesis to subsets of t without changing exact cardinality.", "DilworthPrimaryTarget hdep"),
        ("Transport the equivalence A equiv Fin k into t, retaining the exact-k antichain premise.", "DilworthPrimaryTarget hindependent"),
    ],
    "N-COLORING": [
        ("Map unique membership in a Fin k-indexed chain family to the unique color of each element.", "Statement.lean IsDisjointChainDecomposition"),
        ("Show equal colors place two elements in one chain and hence make them comparable.", "IsChain comparability"),
        ("Conversely, define each chain as a color fiber.", "Set fiber construction"),
        ("Prove every element belongs to its color fiber and uniqueness follows from equality in Fin k.", "fiber membership"),
    ],
    "C-LOCAL-COLORINGS": [
        ("Build the witness closure t := s union A using the finite-restriction package.", "M0819-N-FINITE-RESTRICTION"),
        ("Apply exact finite Dilworth to t and its inherited exact width-k data.", "M0819-L-FINITE-DILWORTH"),
        ("Convert the resulting Fin k chain family on t to a coloring.", "M0819-N-COLORING"),
        ("Restrict that coloring along s subset t and retain same-color comparability on s.", "Finset subtype inclusion"),
    ],
    "L-FINITE-DILWORTH": [
        ("Induct on k and, at fixed positive k, on the number of elements beyond the attained antichain.", "M0819-B-FINITE-INDUCTION"),
        ("Use the source successor construction and both smaller-width residual packages.", "M0819-C-ADJOIN-ELEMENT; M0819-L-LOW-WIDTH-INDEX; M0819-L-DUAL-INDEX"),
        ("Require the uninspected recombination tail as an explicit child rather than inventing it.", "M0819-X-FINITE-TAIL"),
        ("Assemble k chains and convert them to the exact local coloring output.", "M0819-N-COLORING"),
    ],
    "B-FINITE-INDUCTION": [
        ("Base on the attained k-antichain represented by k singleton chains.", "Dilworth 1950 p.162 opening"),
        ("Choose an element a outside the already decomposed induced carrier.", "finite carrier induction"),
        ("Form the U_i, L_i, and N_i pieces relative to a.", "M0819-C-ADJOIN-ELEMENT"),
        ("Obtain upper and order-dual lower residual widths strictly below k.", "M0819-L-LOW-WIDTH-INDEX; M0819-L-DUAL-INDEX"),
        ("Invoke the width induction hypotheses on both residuals.", "strong induction on k"),
        ("Defer exact recombination to the explicitly uninspected finite-tail child.", "M0819-X-FINITE-TAIL"),
    ],
    "C-ADJOIN-ELEMENT": [
        ("Fix a decomposition C_i of the induced carrier before adjoining a.", "Dilworth 1950 p.162"),
        ("Define U_i as elements of C_i above a and L_i as elements below a.", "Dilworth 1950 p.162"),
        ("Define N_i as the remaining elements incomparable with a.", "Dilworth 1950 p.162"),
        ("Prove each piece lies in C_i and inherits chain comparability.", "chain restriction"),
        ("Record union/disjointness and upper/lower closure invariants required by recombination.", "source successor invariants; exact tail open"),
    ],
    "L-LOW-WIDTH-INDEX": [
        ("Assume every candidate upper/incomparable residual has width k.", "Dilworth 1950 p.162 contradiction setup"),
        ("Choose minimal elements witnessing the assumed widths.", "finite minimality"),
        ("Combine the witnesses with a to construct a forbidden (k+1)-antichain.", "hdep contradiction"),
        ("Conclude one residual has width strictly below k.", "negation elimination"),
    ],
    "L-DUAL-INDEX": [
        ("Pass the finite successor data to OrderDual.", "OrderDual transport"),
        ("Apply the upper residual lemma in the dual order.", "M0819-L-LOW-WIDTH-INDEX"),
        ("Transport the selected index and strict width bound back to the original order.", "OrderDual involution"),
    ],
    "X-FINITE-TAIL": [
        ("Acquire original pages 162-163 from a lawful stable source and hash the admitted text.", "source admission task"),
        ("Crosswalk every residual decomposition and recombination premise.", "primary-source node mapping"),
        ("Freeze an exact planned Lean signature for the recombination theorem.", "future registry version if semantics change"),
        ("Obtain independent source review before H0 or composition credit.", "Blueprint section 8.1"),
    ],
    "L-FINITE-EXACTNESS": [
        ("Embed the fixed global exact-k antichain A into every witness closure s union A.", "M0819-N-FINITE-RESTRICTION"),
        ("Preserve cardinality and antichain relations under subtype inclusion.", "equivalence and induced order"),
        ("Use the k distinct witness elements to force distinct local colors.", "chain coloring comparability"),
        ("After global assembly, infer each of the k fibers is hit; retain this as source compatibility only.", "finite pigeonhole; not required by root conclusion"),
    ],
    "L-RADO-SELECTION": [
        ("Instantiate beta a := Fin k and the local family g s from C-LOCAL-COLORINGS.", "Finset.rado_selection_subtype"),
        ("Discharge the finite codomain instance and the k>0 nonempty boundary supplied by the positive branch.", "Finite (Fin k); 0 < k"),
        ("Obtain chi and, for each finite s, a larger t on which chi agrees with g t over s.", "Compactness.lean:88-95"),
        ("Keep the theorem body/provenance/trust audit in X-RADO-PROVENANCE before proof credit.", "new successor anchor boundary"),
    ],
    "C-GLOBAL-COLORING": [
        ("Apply the specialized Rado package to all finite local colorings.", "M0819-L-RADO-SELECTION"),
        ("Project the selected total dependent function to chi : alpha -> Fin k.", "Rado existential output"),
        ("Retain the finite-agreement witness for every requested finset.", "Rado locality conclusion"),
    ],
    "L-GLOBAL-PROPER": [
        ("Fix x and y with chi x = chi y.", "same-color premise"),
        ("Request Rado agreement on the finset {x,y}.", "M0819-C-GLOBAL-COLORING"),
        ("Transport the color equality to one local coloring on a common larger t.", "finite-agreement equalities"),
        ("Apply local same-color comparability and project it to alpha.", "M0819-C-LOCAL-COLORINGS"),
    ],
    "C-COLOR-CLASSES": [
        ("Define C i := {x | chi x = i} for i : Fin k.", "Set fiber"),
        ("Record x in C i iff chi x = i.", "definition unfolding"),
    ],
    "L-FIBERS-CHAIN": [
        ("Fix i and two distinct members x,y of C i.", "IsChain goal"),
        ("Unfold fiber membership to get chi x = chi y.", "M0819-C-COLOR-CLASSES"),
        ("Apply global properness to obtain x <= y or y <= x.", "M0819-L-GLOBAL-PROPER"),
        ("Package pairwise comparability as IsChain for C i.", "IsChain definition"),
    ],
    "L-UNIQUE-MEMBERSHIP": [
        ("For each x choose i := chi x.", "M0819-C-COLOR-CLASSES"),
        ("Show x lies in C i by reflexivity.", "fiber membership"),
        ("For any j with x in C j, unfold both memberships and conclude j = i.", "equality transitivity"),
        ("Package existence and uniqueness in exists! form.", "ExistsUnique.intro"),
    ],
    "T-POSITIVE-ASSEMBLE": [
        ("Introduce alpha, its order, k, positivity, the dependence hypothesis, and exact antichain witness.", "PositiveWidthPackage signature"),
        ("Build all finite local colorings from witness closures and finite Dilworth.", "M0819-C-LOCAL-COLORINGS"),
        ("Select a global coloring by Rado compactness.", "M0819-C-GLOBAL-COLORING"),
        ("Define color fibers and prove the chain invariant.", "M0819-C-COLOR-CLASSES; M0819-L-FIBERS-CHAIN"),
        ("Prove unique membership and construct IsDisjointChainDecomposition.", "M0819-L-UNIQUE-MEMBERSHIP"),
    ],
}


def edge(edge_id: str, source: str, edge_type: str, target: str,
         reciprocal: str | None = None) -> dict:
    value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def graph(endpoints: list[str], values: list[dict]) -> dict:
    outgoing = {identifier: [] for identifier in endpoints}
    incoming = {identifier: [] for identifier in endpoints}
    for value in values:
        outgoing[value["from"]].append(value["edge_id"])
        incoming[value["to"]].append(value["edge_id"])
    return {"edges": values, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    for spec in ROWS:
        fingerprint = (
            INTERFACE_EXPRESSION_FINGERPRINTS[spec["id"]]
            if spec["id"] in INTERFACE_EXPRESSION_FINGERPRINTS
            else "planned:v1:sha256:" + digest([
                spec["id"], spec["reg_kind"], spec["claim"], spec["formal"], spec["output"]
            ])
        )
        reasons = []
        if spec["machine"] != "required":
            reasons.append("no_machine_proof_credit")
        if spec["human"] != "required":
            reasons.append("not_a_distinct_human_claim")
        obligations.append({
            "obligation_id": spec["id"],
            "statement_fingerprint": fingerprint,
            "kind": spec["reg_kind"],
            "root_relevant": spec["short"] not in {"X-FINITE-CANDIDATE"},
            "machine_eligibility": spec["machine"],
            "human_source_eligibility": spec["human"],
            "readable_eligibility": "required" if spec["short"] not in {
                "X-PROVENANCE", "X-RADO-PROVENANCE", "X-TRUST", "X-WORKFLOW"
            } else "not_applicable",
            "risk_class": spec["risk"],
            "exclusion_reason": ({
                "code": "_and_".join(reasons),
                "justification": "This assurance or formal-interface node does not receive the excluded coverage credit.",
                "approval": "pending independent Stage1 integration review",
            } if reasons else None),
            "terminal_proof_body_id": spec["body"],
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{key: value[key] for key in fields} for value in obligations])
    ids = [value["obligation_id"] for value in obligations]
    by_id = {value["obligation_id"]: value for value in obligations}
    parents = {identifier: [] for identifier in ids}
    for parent, children in REQUIRES.items():
        for child in children:
            parents[child].append(parent)

    interface_shorts = {
        "ROOT", "S-DEFINITIONS", "S-DOMAIN",
        "S-TRANSPORT", "B-WIDTH-ZERO", "B-WIDTH-POSITIVE",
        "T-WIDTH-BRANCHES", "T-ROOT-ASSEMBLE",
    }
    nodes = []
    for spec in ROWS:
        identifier = spec["id"]
        children = REQUIRES.get(identifier, [])
        machine_debt = "M3" if spec["short"] in interface_shorts else "M4"
        if spec["short"] in {"X-FINITE-CANDIDATE"}:
            machine_debt = "M5"
        architecture_shorts = {
            "N-FINITE-RESTRICTION", "N-COLORING", "C-LOCAL-COLORINGS",
            "L-RADO-SELECTION", "C-GLOBAL-COLORING", "L-GLOBAL-PROPER",
            "C-COLOR-CLASSES", "L-FIBERS-CHAIN", "L-UNIQUE-MEMBERSHIP",
            "T-POSITIVE-ASSEMBLE", "T-WIDTH-BRANCHES", "T-ROOT-ASSEMBLE",
        }
        source_id = (
            "not-applicable-pending-independent-review"
            if spec["human"] != "required"
            else "architecture-derived-no-primary-node-map-pending-review"
            if spec["short"] in architecture_shorts
            else "Dilworth-1950-node-map-pending-complete-source-and-independent-review"
        )
        provenance_id = "none"
        if identifier in CHECKED_INTERFACES:
            provenance_id = "repo-local-conditional-interface"
        elif spec["short"] == "L-RADO-SELECTION":
            provenance_id = "successor-anchor-required:Finset.rado_selection_subtype"
        elif spec["short"] == "X-FINITE-CANDIDATE":
            provenance_id = "anchor-audit:M0819-C06-nonexact-blocked"
        ledger_rows = SUBSTANTIVE_LEDGERS.get(spec["short"])
        if ledger_rows is None:
            ledger_rows = [(spec["formal"], spec["locator"])]
        ledger = []
        for index, (inference, locator) in enumerate(ledger_rows, 1):
            if index == 1:
                premises = children if children else ["FROZEN-FORMAL-CONTEXT"]
            else:
                premises = [f"{identifier}-STEP-{index - 1:02d}"]
            ledger.append({
                "step_id": f"{identifier}-STEP-{index:02d}",
                "premise_ids": premises,
                "inference": inference,
                "source_locator": locator,
                "output": spec["output"] if index == len(ledger_rows)
                else f"Intermediate output for {identifier} step {index:02d}.",
                "outgoing_use": parents[identifier] if index == len(ledger_rows) and parents[identifier]
                else [f"{identifier}-STEP-{index + 1:02d}"] if index < len(ledger_rows)
                else ["typed-non-proof-edge-or-canonical-root-boundary"],
                "status": "checked_interface" if identifier in CHECKED_INTERFACES
                else "planned_substantive_not_proof_accepted",
            })
        nodes.append({
            "node_id": f"{THEOREM}-{spec['short']}",
            "obligation_id": identifier,
            "kind": spec["node_kind"],
            "human_statement": spec["claim"],
            "formal_target": spec["formal"],
            "output": spec["output"],
            "human_debt": "H1" if spec["human"] == "required" else "H2",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": source_id,
            "provenance_id": provenance_id,
            "foundation_profile": "Lean4 dependent type theory; classical choice/compactness expected; exact accepted axiom profile pending",
            "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive declarations, oleans, executables, and independent replay pending",
            "computation_record": "none; no solver, native evaluator, oracle, experiment, or unchecked certificate is credited",
            "step_budget": "split-required" if children else spec["budget"],
            "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or checked conditional interface only; no open mathematical child, H0, M0, R0, AUDIT-Z, or theorem completion is discharged.",
            "task_ids": [ITEM]
            + (["S56-M-0819-PROOF"] if spec["machine"] == "required" else [])
            + ["S56-M-0819-VALIDATION", "S56-M-0819-RELEASE"],
            "owned_sources": ([f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
                              if identifier in CHECKED_INTERFACES else []),
            "owner": "THM-M-0819 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-14",
                "review_due": "before proof or master acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "primary source", "toolchain", "dependency pin",
                ],
                "revocation_state": "provisional_interface_check" if identifier in CHECKED_INTERFACES
                else "structurally_validated_not_proof_accepted",
            },
        })

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "lifecycle_mode": "executing",
        "registry_id": "THM-M-0819-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:45:00+08:00",
        "freeze_basis": "The exact arbitrary-poset finite-width statement, the inspected primary-proof opening, and an explicit finite-to-global compactness architecture. Roles and eligibility were selected before closure status; the uninspected source tail and newly identified Rado bridge remain explicit open boundaries.",
        "freeze_order_boundary": "The canonical ten-field projection is hashed independently of status_observed_after_freeze. Candidate availability did not determine obligation eligibility.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_statement_bundle_sha256": ROOT_BUNDLE,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "canonical_projection_fields": list(fields),
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"],
            "required_human_source": [value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"],
            "required_readable": [value["obligation_id"] for value in obligations if value["readable_eligibility"] == "required"],
            "informational_overlays": [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The architecture uses mathematical finite compactness, not an external solver, experiment, oracle, native evaluation, or unchecked certificate.",
                "reviewer": "independent Stage1 integration lane",
            }
        },
        "mandatory_layer_analysis": {
            "S": [value["id"] for value in ROWS if value["short"].startswith("S-")],
            "N": [value["id"] for value in ROWS if value["short"].startswith("N-")],
            "B": [value["id"] for value in ROWS if value["short"].startswith("B-")],
            "C": [value["id"] for value in ROWS if value["reg_kind"] == "construction"],
            "L": [value["id"] for value in ROWS if value["reg_kind"] == "lemma"],
            "X": [value["id"] for value in ROWS if value["short"].startswith("X-")],
            "T": [value["id"] for value in ROWS if value["short"].startswith("T-")] + [oid("ROOT")],
            "not_applicable_layers": [],
        },
        "delta_policy": "Any target correction, new anchor, split, merge, exclusion, eligibility, risk, edge role, or proof-body identity change requires version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
            "exact_root_candidate": "none located",
            "nonexact_candidate": "M5 scope mismatch and current-pin failure",
        },
        "status_boundary": "The registry freezes scope and denominators only. Substantive planned ledgers are architecture, not accepted proof leaves. The checked zero-width and conditional composition interfaces do not close the positive-width theorem or any accepted root obligation.",
    }
    registry_scope = {
        key: value for key, value in registry.items()
        if key not in {"status_observed_after_freeze", "status_boundary", "registry_sha256"}
    }
    registry["registry_sha256"] = digest(registry_scope)

    proof_edges = []
    sequence = 0
    checked_pairs = {
        (oid("ROOT"), oid("T-ROOT-ASSEMBLE")),
        (oid("T-ROOT-ASSEMBLE"), oid("S-TRANSPORT")),
        (oid("T-ROOT-ASSEMBLE"), oid("T-WIDTH-BRANCHES")),
        (oid("T-WIDTH-BRANCHES"), oid("B-WIDTH-ZERO")),
        (oid("T-WIDTH-BRANCHES"), oid("B-WIDTH-POSITIVE")),
    }
    for parent, children in REQUIRES.items():
        for child in children:
            sequence += 1
            req = f"P{sequence:03d}-REQ"
            reverse = f"P{sequence:03d}-REV"
            checked = (parent, child) in checked_pairs
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, reverse),
                edge(reverse, child, "composes" if checked else "refines", parent, req),
            ])
            if checked:
                proof_edges[-1]["composition_certificate_id"] = (
                    "COMP-M0819-ROOT" if parent == oid("ROOT")
                    else "COMP-M0819-T-ROOT-ASSEMBLE" if parent == oid("T-ROOT-ASSEMBLE")
                    else "COMP-M0819-T-WIDTH-BRANCHES"
                )
    unverified = [{
        "plan_id": "DECOMP-" + parent,
        "parent_obligation_id": parent,
        "parent_statement_fingerprint": by_id[parent]["statement_fingerprint"],
        "planned_child_ids": children,
        "planned_child_statement_fingerprints": {
            child: by_id[child]["statement_fingerprint"] for child in children
        },
        "status": "planned_semantic_decomposition_not_proof_accepted",
        "required_future_certificate": "A proof-phase exact abstract-child harness must consume every listed child and introduce no undeclared premise before parent closure.",
    } for parent, children in REQUIRES.items() if parent not in CHECKED_PARENT_DECLARATIONS]

    def simple_edges(prefix: str, edge_type: str, pairs: list[tuple[str, str]]) -> list[dict]:
        return [edge(f"{prefix}{index:03d}", source, edge_type, target)
                for index, (source, target) in enumerate(pairs, 1)]

    def reciprocal_edges(prefix: str, forward_type: str, reverse_type: str,
                         pairs: list[tuple[str, str]]) -> list[dict]:
        values = []
        for index, (source, target) in enumerate(pairs, 1):
            forward = f"{prefix}{index:03d}-FWD"
            reverse = f"{prefix}{index:03d}-REV"
            values.extend([
                edge(forward, source, forward_type, target, reverse),
                edge(reverse, target, reverse_type, source, forward),
            ])
        return values

    overlay_ids = {
        oid("S-FOUNDATION"), oid("X-PRIMARY-SOURCE"), oid("X-FINITE-CANDIDATE"),
        oid("X-RADO-PROVENANCE"), oid("X-PROVENANCE"), oid("X-TRUST"),
        oid("X-READABLE"), oid("X-WORKFLOW"),
    }
    proof_overlay_ids = overlay_ids | {oid("S-DEFINITIONS"), oid("S-DOMAIN")}
    graph_edges = {
        "proof": proof_edges,
        "refinement": reciprocal_edges("R", "logical_decomposition", "refines", [
            (oid("ROOT"), oid("S-DEFINITIONS")), (oid("ROOT"), oid("S-DOMAIN")),
            (oid("B-WIDTH-POSITIVE"), oid("N-FINITE-RESTRICTION")),
            (oid("B-WIDTH-POSITIVE"), oid("N-COLORING")),
        ]) + reciprocal_edges("Q", "equivalent_to", "equivalent_to", [
            (oid("ROOT"), oid("S-TRANSPORT")),
        ]),
        "provenance": simple_edges("S", "source_map", [
            (identifier, oid("X-PRIMARY-SOURCE")) for identifier in ids
            if identifier != oid("X-PRIMARY-SOURCE")
            and by_id[identifier]["human_source_eligibility"] == "required"
        ]) + simple_edges("V", "provenance_of", [
            (oid("X-FINITE-CANDIDATE"), oid("L-FINITE-DILWORTH")),
            (oid("X-RADO-PROVENANCE"), oid("L-RADO-SELECTION")),
            (oid("X-PROVENANCE"), oid("S-DEFINITIONS")),
            (oid("X-PROVENANCE"), oid("T-ROOT-ASSEMBLE")),
        ]),
        "evidence": [],
        "trust": reciprocal_edges("T", "trusts", "trusted_by", [
            (oid("ROOT"), oid("S-FOUNDATION")), (oid("ROOT"), oid("X-TRUST")),
            (oid("L-RADO-SELECTION"), oid("X-TRUST")),
            (oid("T-ROOT-ASSEMBLE"), oid("X-TRUST")),
        ]),
        "documentation": simple_edges("D", "documents", [
            (oid("X-READABLE"), identifier) for identifier in ids if identifier != oid("X-READABLE")
        ]),
        "workflow": simple_edges("W", "workflow_depends_on", [
            ("S56-M-0819-STATEMENT", "S56-M-0819-INTAKE"),
            ("S56-M-0819-ANCHOR_AUDIT", "S56-M-0819-STATEMENT"),
            (ITEM, "S56-M-0819-ANCHOR_AUDIT"),
            ("S56-M-0819-PROOF", ITEM),
            ("S56-M-0819-VALIDATION", "S56-M-0819-PROOF"),
            ("S56-M-0819-RELEASE", "S56-M-0819-VALIDATION"),
        ]),
    }
    workflow_tasks = list(WORKFLOW_TASKS)
    graphs = {}
    for name, values in graph_edges.items():
        endpoints = workflow_tasks if name == "workflow" else ids
        graphs[name] = graph(endpoints, values)

    interface_fingerprints = INTERFACE_EXPRESSION_FINGERPRINTS
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "lifecycle_mode": "executing",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_version": 1,
        "registry_denominator_sha256": denominator,
        "registry_sha256": registry["registry_sha256"],
        "root_node_id": f"{THEOREM}-ROOT",
        "root_obligation_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id except workflow task IDs",
        "edge_direction": "Proof requirements run parent to child. Reverse composes edges are certificate-bound checked child contributions; unchecked reverse refines edges are navigational only. Refinement logical_decomposition runs parent to child. Workflow runs task to prerequisite.",
        "workflow_task_nodes": workflow_tasks,
        "task_to_obligation_ids": {
            ITEM: ids,
            "S56-M-0819-PROOF": [
                value["obligation_id"] for value in obligations
                if value["machine_eligibility"] == "required"
            ],
            "S56-M-0819-VALIDATION": ids,
            "S56-M-0819-RELEASE": ids,
        },
        "reciprocal_edge_type_contract": {
            "proof": {
                "proof_requires": ["composes", "refines"],
                "composes": ["proof_requires"],
                "refines": ["proof_requires"],
            },
            "refinement": {
                "logical_decomposition": ["refines"],
                "refines": ["logical_decomposition"],
                "equivalent_to": ["equivalent_to"],
            },
            "trust": {"trusts": ["trusted_by"], "trusted_by": ["trusts"]},
        },
        "interface_expression_fingerprints": interface_fingerprints,
        "graph_reachability_contract": {
            "proof": {
                "roots": [oid("ROOT")],
                "required_reachable": [
                    identifier for identifier in ids if identifier not in proof_overlay_ids
                ],
            },
            "refinement": {
                "roots": [oid("ROOT"), oid("B-WIDTH-POSITIVE")],
                "required_reachable": sorted({
                    oid("ROOT"), oid("S-DEFINITIONS"), oid("S-DOMAIN"), oid("S-TRANSPORT"),
                    oid("B-WIDTH-POSITIVE"), oid("N-FINITE-RESTRICTION"), oid("N-COLORING"),
                }),
            },
            "provenance": {
                "roots": sorted(
                    identifier for identifier in ids
                    if identifier != oid("X-PRIMARY-SOURCE")
                    and by_id[identifier]["human_source_eligibility"] == "required"
                ),
                "required_reachable": sorted(
                    {oid("X-PRIMARY-SOURCE")} | {
                        identifier for identifier in ids
                        if identifier != oid("X-PRIMARY-SOURCE")
                        and by_id[identifier]["human_source_eligibility"] == "required"
                    }
                ),
            },
            "evidence": {"roots": [], "required_reachable": []},
            "trust": {
                "roots": [oid("ROOT"), oid("L-RADO-SELECTION"), oid("T-ROOT-ASSEMBLE")],
                "required_reachable": sorted({
                    oid("ROOT"), oid("L-RADO-SELECTION"), oid("T-ROOT-ASSEMBLE"),
                    oid("S-FOUNDATION"), oid("X-TRUST"),
                }),
            },
            "documentation": {
                "roots": [oid("X-READABLE")],
                "required_reachable": ids,
            },
            "workflow": {
                "roots": ["S56-M-0819-RELEASE"],
                "required_reachable": workflow_tasks,
            },
        },
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [{
            "certificate_id": "COMP-M0819-T-WIDTH-BRANCHES",
            "parent_obligation_id": oid("T-WIDTH-BRANCHES"),
            "parent_statement_fingerprint": by_id[oid("T-WIDTH-BRANCHES")]["statement_fingerprint"],
            "required_child_ids": [oid("B-WIDTH-ZERO"), oid("B-WIDTH-POSITIVE")],
            "required_child_statement_fingerprints": {
                child: by_id[child]["statement_fingerprint"]
                for child in [oid("B-WIDTH-ZERO"), oid("B-WIDTH-POSITIVE")]
            },
            "parent_interface_expression_fingerprint": interface_fingerprints[oid("T-WIDTH-BRANCHES")],
            "required_child_interface_expression_fingerprints": {
                child: interface_fingerprints[child]
                for child in [oid("B-WIDTH-ZERO"), oid("B-WIDTH-POSITIVE")]
            },
            "consumed_child_ids": [oid("B-WIDTH-ZERO"), oid("B-WIDTH-POSITIVE")],
            "unused_child_ids": [],
            "undeclared_premises": [],
            "declarations": [
                "Stage1Instances.THM_M_0819_Obligations.widthBranches_of_positive_and_zero",
            ],
            "kind": "Lean abstract-child harness",
            "status": "provisional conditional composition; the positive-width child remains open",
        }, {
            "certificate_id": "COMP-M0819-T-ROOT-ASSEMBLE",
            "parent_obligation_id": oid("T-ROOT-ASSEMBLE"),
            "parent_statement_fingerprint": by_id[oid("T-ROOT-ASSEMBLE")]["statement_fingerprint"],
            "required_child_ids": [oid("S-TRANSPORT"), oid("T-WIDTH-BRANCHES")],
            "required_child_statement_fingerprints": {
                child: by_id[child]["statement_fingerprint"]
                for child in [oid("S-TRANSPORT"), oid("T-WIDTH-BRANCHES")]
            },
            "parent_interface_expression_fingerprint": interface_fingerprints[oid("T-ROOT-ASSEMBLE")],
            "required_child_interface_expression_fingerprints": {
                child: interface_fingerprints[child]
                for child in [oid("S-TRANSPORT"), oid("T-WIDTH-BRANCHES")]
            },
            "consumed_child_ids": [oid("S-TRANSPORT"), oid("T-WIDTH-BRANCHES")],
            "unused_child_ids": [],
            "undeclared_premises": [],
            "declarations": [
                "Stage1Instances.THM_M_0819_Obligations.expanded_of_widthBranches",
                "Stage1Instances.THM_M_0819_Obligations.checked_root_transport",
                "Stage1Instances.THM_M_0819_Obligations.root_of_widthBranches",
            ],
            "kind": "Lean abstract-child harness",
            "status": "provisional conditional composition; no positive-width proof is supplied",
        }, {
            "certificate_id": "COMP-M0819-ROOT",
            "parent_obligation_id": oid("ROOT"),
            "parent_statement_fingerprint": by_id[oid("ROOT")]["statement_fingerprint"],
            "required_child_ids": [oid("T-ROOT-ASSEMBLE")],
            "required_child_statement_fingerprints": {
                oid("T-ROOT-ASSEMBLE"): by_id[oid("T-ROOT-ASSEMBLE")]["statement_fingerprint"]
            },
            "parent_interface_expression_fingerprint": interface_fingerprints[oid("ROOT")],
            "required_child_interface_expression_fingerprints": {
                oid("T-ROOT-ASSEMBLE"): interface_fingerprints[oid("T-ROOT-ASSEMBLE")]
            },
            "consumed_child_ids": [oid("T-ROOT-ASSEMBLE")],
            "unused_child_ids": [],
            "undeclared_premises": [],
            "declarations": [
                "Stage1Instances.THM_M_0819_Obligations.root_of_terminal",
            ],
            "kind": "Lean exact terminal identity harness",
            "status": "provisional conditional composition; the terminal child remains open",
        }],
        "unverified_decomposition_plans": unverified,
        "closure_boundary": {
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R3"},
            "audit_complete": False,
            "theorem_complete": False,
            "minimal_open_proof_cut_set": [oid("B-WIDTH-POSITIVE")],
            "coarse_interface_cut_set": [oid("B-WIDTH-POSITIVE")],
            "open_proof_leaf_frontier": sorted({
                oid("N-FINITE-RESTRICTION"), oid("N-COLORING"),
                oid("C-ADJOIN-ELEMENT"), oid("X-FINITE-TAIL"),
                oid("L-FINITE-EXACTNESS"), oid("L-RADO-SELECTION"),
            }),
            "remaining_release_cut_set": [
                oid("B-WIDTH-POSITIVE"), oid("X-PRIMARY-SOURCE"), oid("S-FOUNDATION"),
                oid("X-RADO-PROVENANCE"), oid("X-PROVENANCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "The k=0 boundary and abstract branch/root composition are checked, but no exact positive-width proof body was located or supplied. All proof, source, provenance, trust, readability, validation, and release acceptance remains open.",
        },
    }

    bundle_recipe_id = "VAL-M0819-OBLIGATION-STRUCTURE-AND-LEAN"
    for node in nodes:
        node["validation_spec_id"] = bundle_recipe_id
    recipes = [{
        "recipe_id": bundle_recipe_id,
        "cwd": ".",
        "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
        "env_allowlist": {
            "LC_ALL": "C",
            "LANG": "C",
            "NO_COLOR": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        "timeout_seconds": 240,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{
            "path_or_stream": "stdout",
            "semantic_hash_policy": "report exact obligation, edge, ledger, open-composition, denominator, Lean-output, and false-completion values",
        }],
        "covered_obligation_ids": ids,
        "covered_declarations": [
            "Stage1Instances.THM_M_0819.DilworthPrimaryTarget",
            "Stage1Instances.THM_M_0819_Obligations.zeroWidth_of_statement",
            "Stage1Instances.THM_M_0819_Obligations.widthBranches_of_positive_and_zero",
            "Stage1Instances.THM_M_0819_Obligations.expanded_of_widthBranches",
            "Stage1Instances.THM_M_0819_Obligations.checked_root_transport",
            "Stage1Instances.THM_M_0819_Obligations.root_of_widthBranches",
            "Stage1Instances.THM_M_0819_Obligations.root_of_terminal",
        ],
        "coverage_boundary": "The recipe structurally covers every frozen obligation. Kernel coverage is limited to the named exact target, zero-width theorem, and conditional composition declarations; it supplies no positive-width inhabitant or accepted closure.",
    }]
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "lifecycle_mode": "executing",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "registry_sha256": registry["registry_sha256"],
        "recipes": recipes,
        "status_boundary": "This bundle recipe validates the frozen registry, graph structure, substrate anchor, and conditional Lean interfaces only. Structural coverage of an obligation supplies no kernel or semantic proof closure for it.",
    }
    return registry, bundle, specs


def main() -> None:
    registry, bundle, specs = build()
    for filename, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", specs),
    ):
        (HERE / filename).write_text(
            json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
    edge_count = sum(len(value["edges"]) for value in bundle["graphs"].values())
    print(
        f"built {len(registry['obligations'])} obligations and {edge_count} typed edges; "
        f"denominator {registry['denominator_sha256']}"
    )


if __name__ == "__main__":
    main()
