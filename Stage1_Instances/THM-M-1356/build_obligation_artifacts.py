#!/usr/bin/env python3
"""Build the frozen THM-M-1356 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1356-OBLIGATION_TREE"
THEOREM = "THM-M-1356"
PREFIX = "M1356-"
EXPRESSION_HASH = "7901eb74686f457348ec06812b8584c69eb09649779637cbb28b2e7bd84b98bf"
SOURCE_HASH = "da0e65cd8b8f0fe68622e2814a2714ab30eb0e2b97577ae9407f8270d26d02c6"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def spec(
    oid: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    source: str,
    budget: int,
) -> dict:
    return {
        "id": oid,
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "source": source,
        "budget": budget,
    }


SPECS = [
    spec(
        "M1356-ROOT", "root", "critical",
        "For every frozen positive-degree coefficient vector, strict left-half-plane stability is equivalent to positivity of every finite leading Hurwitz minor.",
        "Stage1Instances.THM_M_1356.RouthHurwitzTarget",
        "The exact canonical proposition.",
        "Statement.lean; elaborated expression sha256 " + EXPRESSION_HASH, 10,
    ),
    spec(
        "M1356-S-STATEMENT", "definition", "critical",
        "Preserve the exact degree, coefficient, root, matrix, minor, quantifier, implication, and strict-inequality interfaces.",
        "Stage1Instances.THM_M_1356.{RouthHurwitzTarget,IsStrictlyStable,hurwitzMinor}",
        "The exact input and output interfaces used by every composition edge.",
        "Statement.lean: sourceCoefficient through RouthHurwitzTarget; Barkovsky pp. 6, 18-19", 16,
    ),
    spec(
        "M1356-S-COEFFICIENT", "transport", "high",
        "Relate descending source coefficients to Polynomial.ofFn, prove coefficient n is a_0, prevent degree drop, and map the real polynomial to Complex.",
        "Stage1Instances.THM_M_1356.{realPolynomial_coeff_degree,realPolynomial_natDegree_eq,complexPolynomial}",
        "A degree-exact real-to-complex polynomial matching a_0 z^n + ... + a_n.",
        "Statement.lean: sourceCoefficient and realPolynomial adapters; Barkovsky p. 19 eq. (38)", 28,
    ),
    spec(
        "M1356-S-BOUNDARIES", "normalization", "critical",
        "Retain n > 0, a_0 > 0, exact degree n, strict open half-plane, all n strict minors, and the imaginary-axis/nonregular cases needed by the reverse direction.",
        "Boundary package for Stage1Instances.THM_M_1356.RouthHurwitzTarget",
        "No zero-degree, degree-drop, non-strict, selected-minor, or regular-only substitute enters the proof.",
        "Statement.lean binders and mutations; Barkovsky pp. 16-20, Theorems 34 and 40", 24,
    ),
    spec(
        "M1356-S-FOUNDATION", "certificate", "critical",
        "Account for classical finite-root arguments, real-to-complex algebra, determinant reasoning, extensionality, the kernel, and the no-oracle policy.",
        "Future axiom, dependency, and TCB report for every terminal declaration",
        "An accepted foundation and trust boundary for all proof bodies.",
        "Statement receipt profiles; anchor-audit immutable environment", 24,
    ),
    spec(
        "M1356-C-EVEN-ODD", "construction", "high",
        "Split the normalized imaginary-axis evaluation into the alternating real polynomials f_0 and f_1 and prove their coefficient, degree, and common-root identities.",
        "Planned signature: exists_evenOddPair_for_imaginaryAxis",
        "Real polynomials f_0,f_1 with i^(-n)p(i*w)=f_0(w)-i*f_1(w) and an exact imaginary-axis common-root criterion.",
        "Barkovsky p. 10 eqs. (9)-(12)", 46,
    ),
    spec(
        "M1356-C-EVEN-ODD-DEFS", "construction", "high",
        "Define the alternating real polynomials f_0,f_1 and prove the normalized imaginary-axis evaluation, displayed coefficient formulas, and degree inequality.",
        "Planned signature: alternatingPair_evaluation_and_degree",
        "i^(-n)p(i*w)=f_0(w)-i*f_1(w), the source coefficient rows (11), and deg f_1 < deg f_0.",
        "Barkovsky p. 10, eqs. (9)-(11)", 34,
    ),
    spec(
        "M1356-L-IMAG-COMMON-ROOT", "core_lemma", "critical",
        "Identify imaginary-axis roots of p with common real roots of f_0,f_1 and hence real roots of their gcd.",
        "Planned signature: imaginaryRoot_iff_evenOddGcdRoot",
        "p(i*w)=0 iff f_0(w)=f_1(w)=0 iff gcd(f_0,f_1)(w)=0.",
        "Barkovsky p. 10, eq. (12)", 24,
    ),
    spec(
        "M1356-C-STURM", "construction", "critical",
        "Construct the signed Euclidean Sturm/Routh sequence from f_0,f_1, including degree decrease, termination, sign-change invariants, and the possible final zero cases.",
        "Planned signature: exists_routhSturmSequence",
        "A finite Routh sequence with leading coefficients h_0,...,h_n and a complete regular/nonregular terminal classification.",
        "Barkovsky pp. 13-17, eqs. (19)-(33)", 72,
    ),
    spec(
        "M1356-C-SIGNED-REMAINDER", "construction", "high",
        "Define one signed Euclidean step f_(k-1) = d_k f_k - f_(k+1) and prove the new remainder has strictly smaller degree when nonzero.",
        "Planned signature: signedRemainder_step",
        "A next polynomial with the required sign convention and strict degree descent.",
        "Barkovsky p. 14, eq. (25)", 44,
    ),
    spec(
        "M1356-C-STURM-TERMINATION", "construction", "critical",
        "Iterate signed remainders until the first zero remainder and prove termination, finite indexing, and the greatest-common-divisor terminal invariant.",
        "Planned signature: signedRemainder_terminates_with_gcd",
        "A finite sequence ending at a nonzero gcd, with every earlier degree strictly descending.",
        "Barkovsky pp. 14, 16-17, eq. (25) and Theorem 34 proof", 62,
    ),
    spec(
        "M1356-C-STURM-INVARIANTS", "construction", "critical",
        "Prove the signed-remainder sequence satisfies the Sturm non-simultaneous-zero and opposite-neighbor-sign conditions.",
        "Planned signature: signedRemainder_isSturmSequence",
        "The exact Sturm conditions needed by Theorem 26 for every nonterminal prefix.",
        "Barkovsky pp. 12-14, conditions (19)-(21) and eq. (25)", 58,
    ),
    spec(
        "M1356-C-ROUTH-RECURRENCE", "construction", "critical",
        "Specialize the signed remainder step to alternating coefficients and prove the array update records the next leading coefficient and preserves the alternating row shape.",
        "Planned signature: routhArray_step_matches_signedRemainder",
        "A Routh array whose stored h_k are exactly the Sturm-polynomial leading coefficients.",
        "Barkovsky pp. 15-16, eqs. (26)-(28) and Routh routine", 66,
    ),
    spec(
        "M1356-L-HERMITE", "bridge", "critical",
        "Relate the argument increment of the imaginary-axis hodograph to the difference between left- and right-half-plane root counts.",
        "Planned signature: hermite_hodograph_root_count",
        "Delta_p = pi * (n_minus - n_plus) when there is no imaginary-axis root.",
        "Barkovsky pp. 8-9, Theorem 6 and Lemma 5", 58,
    ),
    spec(
        "M1356-L-LINEAR-HODOGRAPH", "core_lemma", "high",
        "Compute the argument increment of the normalized imaginary-axis hodograph for one linear factor z-lambda with nonzero real part.",
        "Planned signature: linearFactor_hodographIncrement",
        "Delta_(z-lambda) = -pi * sign(re lambda).",
        "Barkovsky p. 8, Lemma 5", 32,
    ),
    spec(
        "M1356-L-HODOGRAPH-PRODUCT", "core_lemma", "high",
        "Prove argument increments add under multiplication and account for the positive leading scalar and all complex roots with multiplicity.",
        "Planned signature: hodographIncrement_factorization",
        "The increment of p is the sum of the increments of its linear factors.",
        "Barkovsky pp. 8-9, Theorem 6 proof", 42,
    ),
    spec(
        "M1356-L-CAUCHY-INDEX", "bridge", "critical",
        "Convert half-plane root counts into the Cauchy index of f_1/f_0, without assuming the desired stability criterion.",
        "Planned signature: halfPlaneRootCount_eq_cauchyIndex",
        "n_minus - n_plus = Ind_{-infinity}^{+infinity}(f_1/f_0).",
        "Barkovsky pp. 10-12, Lemmas 15-17 and Theorem 18", 68,
    ),
    spec(
        "M1356-L-CROSSING-INTERIOR", "core_lemma", "high",
        "Compute the hodograph argument increment between consecutive imaginary-axis crossings from their oriented crossing indices.",
        "Planned signature: argumentIncrement_between_crossings",
        "Each interior increment is pi/2 times the sum of its two crossing indices.",
        "Barkovsky p. 11, Lemma 15", 38,
    ),
    spec(
        "M1356-L-CROSSING-ENDS", "core_lemma", "high",
        "Compute the two unbounded-end argument increments from degree f_1 < degree f_0 and the first and last crossing indices.",
        "Planned signature: argumentIncrement_at_infinite_ends",
        "The two end increments are pi/2 times the first and last crossing indices.",
        "Barkovsky pp. 11-12, Lemma 16", 42,
    ),
    spec(
        "M1356-L-CROSSING-SUM", "core_lemma", "high",
        "Sum the disjoint interior and end intervals, including the no-crossing case, and identify the sum of crossing indices with the Cauchy index.",
        "Planned signature: hodographIncrement_eq_cauchyIndex",
        "Delta_p = pi * Ind(f_1/f_0).",
        "Barkovsky p. 12, Lemma 17 and definitions (15)-(17)", 50,
    ),
    spec(
        "M1356-L-STURM-INDEX", "core_lemma", "critical",
        "Compute the Cauchy index from a signed Sturm sequence, including discontinuity jumps and limiting sign variations.",
        "Planned signature: cauchyIndex_eq_sturmVariation",
        "The Cauchy index is V(-infinity)-V(+infinity), with the regular leading-coefficient formula as a corollary.",
        "Barkovsky pp. 12-14, Lemmas 24-25 and Theorems 26 and 28", 78,
    ),
    spec(
        "M1356-L-STURM-NOJUMP", "core_lemma", "high",
        "Show the sign-variation count has no jump at a point that is not an odd-multiplicity zero of f_0.",
        "Planned signature: sturmVariation_noJump",
        "Equal left and right limits of V at every non-pole discontinuity candidate.",
        "Barkovsky p. 13, Lemma 24", 44,
    ),
    spec(
        "M1356-L-STURM-POLE-JUMP", "core_lemma", "high",
        "At every odd-multiplicity zero of f_0, identify the jump of sign variation with minus the local Cauchy index.",
        "Planned signature: sturmVariation_jump_eq_neg_index",
        "V(c+)-V(c-) = -Ind_c(f_1/f_0).",
        "Barkovsky p. 13, Lemma 25", 42,
    ),
    spec(
        "M1356-L-STURM-GLOBAL", "core_lemma", "critical",
        "Sum every jump of the finite sign-variation step function to obtain Sturm's global Cauchy-index formula.",
        "Planned signature: cauchyIndex_eq_variationDifference",
        "Ind_a^b(f_1/f_0) = V(a+)-V(b-).",
        "Barkovsky pp. 13-14, Theorem 26", 46,
    ),
    spec(
        "M1356-L-STURM-INFINITY", "core_lemma", "high",
        "For a regular degree-descending sequence, compute both infinite-end sign variations from the leading coefficients.",
        "Planned signature: regularSturm_index_eq_leadingSignChanges",
        "Ind = n - 2*v(h_0,...,h_n).",
        "Barkovsky p. 14, Theorem 28", 40,
    ),
    spec(
        "M1356-L-ROUTH-REGULAR", "core_lemma", "critical",
        "In the regular case, prove stability iff the Routh procedure terminates and all nonzero leading coefficients h_0,...,h_n have one sign.",
        "Planned signature: stable_iff_routh_regular_sameSign",
        "The regular Routh sign criterion in both directions.",
        "Barkovsky p. 16, Theorem 33", 52,
    ),
    spec(
        "M1356-B-ROUTH-NECESSITY", "branch", "critical",
        "From stability derive extreme sign variations at both infinities, maximal Sturm-sequence length, regularity, and one common nonzero sign for all h_k.",
        "Planned signature: stable_implies_routhRegular_sameSign",
        "The necessity direction of Barkovsky Theorem 33.",
        "Barkovsky p. 16, Theorem 33 proof using Theorems 18 and 26", 32,
    ),
    spec(
        "M1356-B-ROUTH-SUFFICIENCY", "branch", "critical",
        "From regularity and one common nonzero sign for all h_k derive zero sign variation, exact root counts, and strict stability.",
        "Planned signature: routhRegular_sameSign_implies_stable",
        "The sufficiency direction of Barkovsky Theorem 33.",
        "Barkovsky p. 16, Theorem 33 proof using Theorems 28 and 18", 28,
    ),
    spec(
        "M1356-B-NONREGULAR", "branch", "critical",
        "Classify all terminal h_(n-1),h_n zero/sign cases, remove the gcd representing imaginary-axis roots where required, and recompose an exhaustive boundary result.",
        "Planned signature: routh_terminal_cases",
        "Exact root counts and imaginary-axis-root status for every Routh terminal case.",
        "Barkovsky pp. 16-17, Theorem 34 cases (a)-(e)", 82,
    ),
    spec(
        "M1356-B-TERMINAL-SPLIT", "branch", "critical",
        "Split exhaustively on h_(n-1), h_n, and the sign of h_(n-2)*h_n, with disjoint cases matching Theorem 34.",
        "Planned signature: routhTerminal_exhaustiveCases",
        "Exactly one of terminal cases A through E.",
        "Barkovsky pp. 16-17, Theorem 34 cases (a)-(e)", 28,
    ),
    spec(
        "M1356-B-TERMINAL-A", "branch", "high",
        "When h_(n-1) and h_n are nonzero, prove regularity, absence of imaginary-axis roots, and the two sign-variation root counts.",
        "Planned signature: routhTerminal_caseA",
        "Theorem 34(a), including formula (29).",
        "Barkovsky pp. 16-17, Theorem 34(a)", 42,
    ),
    spec(
        "M1356-B-TERMINAL-B", "branch", "high",
        "When h_(n-1) is nonzero and h_n is zero, identify the gcd as omega and remove the one simple root at zero before recounting.",
        "Planned signature: routhTerminal_caseB",
        "Theorem 34(b), including formula (30).",
        "Barkovsky pp. 16-17, Theorem 34(b)", 48,
    ),
    spec(
        "M1356-B-TERMINAL-C", "branch", "high",
        "When h_(n-1)=0 and h_(n-2)*h_n<0, prove the quadratic terminal gcd has no real zero and compute root counts by Sturm's general formula.",
        "Planned signature: routhTerminal_caseC",
        "Theorem 34(c), including formula (31).",
        "Barkovsky pp. 16-17, Theorem 34(c)", 48,
    ),
    spec(
        "M1356-B-TERMINAL-D", "branch", "high",
        "When h_(n-1)=0 and h_(n-2)*h_n>0, remove the two simple nonzero imaginary-axis roots encoded by the quadratic gcd and recount.",
        "Planned signature: routhTerminal_caseD",
        "Theorem 34(d), including formula (32).",
        "Barkovsky pp. 16-17, Theorem 34(d)", 52,
    ),
    spec(
        "M1356-B-TERMINAL-E", "branch", "high",
        "When h_(n-1)=h_n=0, remove the double zero root encoded by the quadratic gcd and recount.",
        "Planned signature: routhTerminal_caseE",
        "Theorem 34(e), including formula (33).",
        "Barkovsky pp. 16-17, Theorem 34(e)", 48,
    ),
    spec(
        "M1356-T-GCD-CORRECTION", "transport", "critical",
        "Divide p by the polynomial corresponding to the normalized gcd of f_0,f_1, prove the exact root-multiset removal, and transport half-plane counts back to p.",
        "Planned signature: removeImaginaryAxisGcd_and_transport_counts",
        "A checked bridge used by terminal cases B, D, and E, with no lost multiplicity or changed half-plane convention.",
        "Barkovsky p. 17, Theorem 34 proof after formulas (29)-(33)", 70,
    ),
    spec(
        "M1356-L-ROUTH-CRITERION", "core_lemma", "critical",
        "Combine Hermite root counting, Cauchy indices, Sturm variation, the regular sign theorem, and the nonregular terminal cases into the complete Routh criterion.",
        "Planned signature: stable_iff_routhLeadingCoefficientsPositive",
        "For a_0 > 0, stability iff the full Routh leading-coefficient package is positive, with nonregular cases excluded for the correct reason.",
        "Barkovsky pp. 8-17, Theorems 6, 18, 26, 28, 33, and 34", 34,
    ),
    spec(
        "M1356-L-GAUSS", "core_lemma", "critical",
        "Perform no-pivot Gaussian elimination on every leading Hurwitz block and show each row operation preserves every relevant leading principal determinant.",
        "Planned signature: hurwitzLeadingBlocks_eliminate_to_routh",
        "The first k Hurwitz block reduces to an upper triangular block with diagonal h_1,...,h_k without changing its determinant.",
        "Barkovsky pp. 18-19, Lemma 39 proof and eqs. (26)-(28)", 74,
    ),
    spec(
        "M1356-L-GAUSS-STEP", "core_lemma", "high",
        "Show one no-pivot row subtraction eliminates the lower leading entry, preserves the determinant of every enclosing leading block, and produces coefficients of the next Routh polynomial.",
        "Planned signature: hurwitzBlock_oneEliminationStep",
        "One determinant-preserving reduction from the (f_(k-1),f_k) block to the (f_k,f_(k+1)) block.",
        "Barkovsky pp. 15, 18, eqs. (26)-(28) and Lemma 39 proof", 52,
    ),
    spec(
        "M1356-L-GAUSS-SHAPE", "core_lemma", "critical",
        "Inductively preserve the shifted Hurwitz block shape after crossing out the completed row and column.",
        "Planned signature: hurwitzBlock_recursiveShape",
        "After k steps, the remaining block is the Hurwitz-shaped block of f_k,f_(k+1).",
        "Barkovsky p. 18, Lemma 39 proof", 58,
    ),
    spec(
        "M1356-L-TRIANGULAR-DET", "core_lemma", "high",
        "Compute every leading determinant of the resulting upper triangular matrix as the product of its first k diagonal Routh coefficients.",
        "Planned signature: leadingDet_upperTriangular_eq_diagonalProduct",
        "eta_k = product_{1<=j<=k} h_j after the determinant-preserving elimination sequence.",
        "Barkovsky p. 19, Lemma 39 and eq. (37)", 38,
    ),
    spec(
        "M1356-L-MINOR-PRODUCT", "core_lemma", "critical",
        "Deduce eta_k = h_1*...*h_k for every regular prefix and handle the last-minor identity and zero cases without dividing by an unproved nonzero minor.",
        "Planned signature: hurwitzMinor_eq_routhLeadingProduct",
        "An exact indexed product identity connecting finite Hurwitz minors to Routh leading coefficients.",
        "Barkovsky pp. 18-19, eqs. (35)-(37) and Lemma 39", 48,
    ),
    spec(
        "M1356-B-STABLE-TO-MINORS", "branch", "critical",
        "Use the complete Routh criterion and the determinant product identity to derive strict positivity of every leading Hurwitz minor from strict stability.",
        "Stage1Instances.THM_M_1356.ObligationTree.StableToPositiveMinorsTarget",
        "The exact forward implication at every frozen binder.",
        "Barkovsky p. 19, Theorem 40 necessity via Lemma 39 and Theorems 33-34", 30,
    ),
    spec(
        "M1356-B-MINORS-TO-STABLE", "branch", "critical",
        "Use positive leading minors to derive positive nonzero Routh coefficients, rule out every nonregular/imaginary-axis case, and conclude strict stability.",
        "Stage1Instances.THM_M_1356.ObligationTree.PositiveMinorsToStableTarget",
        "The exact reverse implication at every frozen binder.",
        "Barkovsky p. 19, Theorem 40 sufficiency via Lemma 39 and Theorems 33-34", 36,
    ),
    spec(
        "M1356-T-ASSEMBLE", "transport", "critical",
        "Assemble the exact forward and reverse implication packages at the unchanged canonical binders.",
        "Stage1Instances.THM_M_1356.ObligationTree.root_of_directions",
        "Stage1Instances.THM_M_1356.RouthHurwitzTarget.",
        "ObligationTree.lean conditional composition harness", 12,
    ),
    spec(
        "M1356-X-SOURCE", "terminal", "critical",
        "Map every material proof node to reviewed primary and modern sources, assumptions, proof steps, translation choices, corrections, and errata.",
        "Node-specific human-source crosswalk",
        "Human-source evidence without machine-proof credit.",
        "Hurwitz 1895 pp. 273-284; Barkovsky arXiv:0802.1805v1 pp. 6-19", 40,
    ),
    spec(
        "M1356-X-PROVENANCE", "certificate", "critical",
        "Resolve every future local or imported terminal declaration, body, revision, license, dependency, wrapper, placeholder scan, and receipt without duplicate credit.",
        "Future transitive proof-body provenance report",
        "Proof provenance and evidence coverage without mathematical proof credit.",
        "anchor-audit.json exact negative candidate inventory", 36,
    ),
    spec(
        "M1356-X-TRUST", "certificate", "critical",
        "Audit the Lean/mathlib declaration closure, axioms, compiled artifacts, executables, unsafe/oracle boundaries, hermetic replay, and independent verification.",
        "Future release-grade foundation and TCB closure",
        "A release trust decision without mathematical proof credit.",
        "Lean 4.29.0; mathlib 8a178386; anchor-audit immutable environment", 40,
    ),
    spec(
        "M1356-X-READABLE", "certificate", "high",
        "Produce a fingerprint-linked, independently reviewed readable reconstruction for every required obligation, explicitly labeling every machine-open node.",
        "Future node-specific R0 records",
        "Readable coverage without machine-proof or human-source credit.",
        "Docs/Stage1_Blueprint_rev-5.6.md sections 8 and 9", 32,
    ),
    spec(
        "M1356-X-WORKFLOW", "certificate", "critical",
        "Bind dependency-ordered task acceptance, structured recipes, receipts, reconciliation, freshness, and revocation without treating workflow success as proof.",
        "Future Stage1 receipt and reconciliation closure",
        "A workflow acceptance decision without mathematical proof credit.",
        "Docs/Stage1_Blueprint_rev-5.6.md sections 9 and 10", 34,
    ),
]


REQUIRES = {
    "M1356-ROOT": ["M1356-T-ASSEMBLE"],
    "M1356-T-ASSEMBLE": ["M1356-B-STABLE-TO-MINORS", "M1356-B-MINORS-TO-STABLE"],
    "M1356-B-STABLE-TO-MINORS": ["M1356-L-ROUTH-CRITERION", "M1356-L-MINOR-PRODUCT"],
    "M1356-B-MINORS-TO-STABLE": ["M1356-L-ROUTH-CRITERION", "M1356-L-MINOR-PRODUCT"],
    "M1356-L-ROUTH-CRITERION": ["M1356-L-HERMITE", "M1356-L-CAUCHY-INDEX", "M1356-L-STURM-INDEX", "M1356-L-ROUTH-REGULAR", "M1356-B-NONREGULAR", "M1356-C-STURM"],
    "M1356-L-HERMITE": ["M1356-L-LINEAR-HODOGRAPH", "M1356-L-HODOGRAPH-PRODUCT"],
    "M1356-L-HODOGRAPH-PRODUCT": ["M1356-L-LINEAR-HODOGRAPH"],
    "M1356-L-CAUCHY-INDEX": ["M1356-C-EVEN-ODD", "M1356-L-HERMITE", "M1356-L-CROSSING-SUM"],
    "M1356-L-CROSSING-SUM": ["M1356-L-CROSSING-INTERIOR", "M1356-L-CROSSING-ENDS"],
    "M1356-L-STURM-INDEX": ["M1356-C-STURM", "M1356-L-STURM-GLOBAL", "M1356-L-STURM-INFINITY"],
    "M1356-L-STURM-GLOBAL": ["M1356-L-STURM-NOJUMP", "M1356-L-STURM-POLE-JUMP"],
    "M1356-L-STURM-INFINITY": ["M1356-L-STURM-GLOBAL", "M1356-C-STURM-INVARIANTS"],
    "M1356-L-ROUTH-REGULAR": ["M1356-B-ROUTH-NECESSITY", "M1356-B-ROUTH-SUFFICIENCY"],
    "M1356-B-ROUTH-NECESSITY": ["M1356-L-CAUCHY-INDEX", "M1356-L-STURM-GLOBAL", "M1356-C-STURM"],
    "M1356-B-ROUTH-SUFFICIENCY": ["M1356-L-CAUCHY-INDEX", "M1356-L-STURM-INFINITY", "M1356-C-STURM"],
    "M1356-B-NONREGULAR": ["M1356-B-TERMINAL-SPLIT", "M1356-B-TERMINAL-A", "M1356-B-TERMINAL-B", "M1356-B-TERMINAL-C", "M1356-B-TERMINAL-D", "M1356-B-TERMINAL-E", "M1356-T-GCD-CORRECTION", "M1356-L-STURM-INDEX"],
    "M1356-B-TERMINAL-A": ["M1356-L-STURM-INFINITY"],
    "M1356-B-TERMINAL-B": ["M1356-T-GCD-CORRECTION"],
    "M1356-B-TERMINAL-C": ["M1356-L-STURM-GLOBAL"],
    "M1356-B-TERMINAL-D": ["M1356-T-GCD-CORRECTION"],
    "M1356-B-TERMINAL-E": ["M1356-T-GCD-CORRECTION"],
    "M1356-T-GCD-CORRECTION": ["M1356-C-EVEN-ODD", "M1356-C-STURM-TERMINATION"],
    "M1356-C-EVEN-ODD": ["M1356-C-EVEN-ODD-DEFS", "M1356-L-IMAG-COMMON-ROOT"],
    "M1356-L-IMAG-COMMON-ROOT": ["M1356-C-EVEN-ODD-DEFS"],
    "M1356-C-STURM": ["M1356-C-EVEN-ODD", "M1356-C-SIGNED-REMAINDER", "M1356-C-STURM-TERMINATION", "M1356-C-STURM-INVARIANTS", "M1356-C-ROUTH-RECURRENCE"],
    "M1356-C-STURM-TERMINATION": ["M1356-C-SIGNED-REMAINDER"],
    "M1356-C-STURM-INVARIANTS": ["M1356-C-SIGNED-REMAINDER"],
    "M1356-C-ROUTH-RECURRENCE": ["M1356-C-SIGNED-REMAINDER", "M1356-C-EVEN-ODD-DEFS"],
    "M1356-L-MINOR-PRODUCT": ["M1356-L-GAUSS", "M1356-C-STURM"],
    "M1356-L-GAUSS": ["M1356-C-STURM", "M1356-L-GAUSS-STEP", "M1356-L-GAUSS-SHAPE", "M1356-L-TRIANGULAR-DET"],
    "M1356-L-GAUSS-STEP": ["M1356-C-ROUTH-RECURRENCE"],
    "M1356-L-GAUSS-SHAPE": ["M1356-L-GAUSS-STEP"],
    "M1356-L-TRIANGULAR-DET": ["M1356-L-GAUSS-SHAPE"],
}

SOURCE_NA = {
    "M1356-S-STATEMENT", "M1356-S-COEFFICIENT", "M1356-S-FOUNDATION",
    "M1356-X-PROVENANCE", "M1356-X-TRUST", "M1356-X-READABLE", "M1356-X-WORKFLOW",
}
MACHINE_SPECIAL = {
    "M1356-X-SOURCE": "not_applicable",
    "M1356-X-PROVENANCE": "informational",
    "M1356-X-TRUST": "informational",
    "M1356-X-READABLE": "informational",
    "M1356-X-WORKFLOW": "informational",
}
INTERFACE_TYPES = {
    "M1356-B-STABLE-TO-MINORS": "Stage1Instances.THM_M_1356.ObligationTree.StableToPositiveMinorsTarget",
    "M1356-B-MINORS-TO-STABLE": "Stage1Instances.THM_M_1356.ObligationTree.PositiveMinorsToStableTarget",
    "M1356-T-ASSEMBLE": "Stage1Instances.THM_M_1356.ObligationTree.DirectionPackage -> Stage1Instances.THM_M_1356.RouthHurwitzTarget",
}

spec_by_id = {row["id"]: row for row in SPECS}
assert len(spec_by_id) == len(SPECS)


def make_obligations() -> list[dict]:
    result = []
    for row in SPECS:
        oid = row["id"]
        if oid in {"M1356-ROOT", "M1356-S-STATEMENT"}:
            fingerprint = "lean-expression-sha256:" + EXPRESSION_HASH
        elif oid in INTERFACE_TYPES:
            fingerprint = "lean-interface:v1:sha256:" + digest(INTERFACE_TYPES[oid])
        else:
            fingerprint = "planned:v1:sha256:" + digest([
                oid, row["kind"], row["claim"], row["formal"], row["output"], row["source"]
            ])
        machine = MACHINE_SPECIAL.get(oid, "required")
        exclusion = None
        if oid == "M1356-X-SOURCE":
            exclusion = "human_source_boundary_only_pending_independent_approval"
        elif oid in {"M1356-X-PROVENANCE", "M1356-X-TRUST", "M1356-X-READABLE", "M1356-X-WORKFLOW"}:
            exclusion = "release_overlay_no_proof_credit_pending_independent_approval"
        result.append({
            "obligation_id": oid,
            "statement_fingerprint": fingerprint,
            "kind": row["kind"],
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": "not_applicable" if oid in SOURCE_NA else "required",
            "readable_eligibility": "required",
            "risk_class": row["risk"],
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": None,
        })
    return result


DENOMINATOR_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def semantic_ledger(row: dict) -> list[dict]:
    oid = row["id"]
    children = REQUIRES.get(oid, [])
    steps = []
    for index, child in enumerate(children, 1):
        child_row = spec_by_id[child]
        steps.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": [child],
            "inference": "Consume the exact typed child output; no source citation or workflow edge substitutes for it.",
            "source_locator": child_row["source"],
            "output": child_row["output"],
            "outgoing_use": f"Exact future composition of {oid}",
        })
    steps.append({
        "step_id": f"{oid}-STEP-{len(steps) + 1:02d}",
        "premise_ids": children if children else ["frozen-formal-context"],
        "inference": row["claim"],
        "source_locator": row["source"],
        "output": row["output"],
        "outgoing_use": "Only the declared proof parent or non-proof typed support edge may consume this output.",
    })
    return steps


def edge(eid: str, source: str, typ: str, target: str, reciprocal: str | None = None) -> dict:
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def indexed_graph(edges: list[dict]) -> dict:
    outgoing: dict[str, list[str]] = {}
    incoming: dict[str, list[str]] = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict, str]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = make_obligations()
    ids = [row["obligation_id"] for row in obligations]
    denominator = digest([{key: row[key] for key in DENOMINATOR_FIELDS} for row in obligations])

    denominators = {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
        "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
    }
    mandatory = {
        "S": ["M1356-S-STATEMENT", "M1356-S-COEFFICIENT", "M1356-S-BOUNDARIES", "M1356-S-FOUNDATION"],
        "N": ["M1356-S-COEFFICIENT", "M1356-S-BOUNDARIES"],
        "B": [row["id"] for row in SPECS if row["id"].startswith("M1356-B-")],
        "C": [row["id"] for row in SPECS if row["id"].startswith("M1356-C-")],
        "L": [row["id"] for row in SPECS if row["id"].startswith("M1356-L-")],
        "X": [row["id"] for row in SPECS if row["id"].startswith("M1356-X-")],
        "T": [row["id"] for row in SPECS if row["id"].startswith("M1356-T-")],
        "not_applicable_layers": [],
    }
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "registry_id": "THM-M-1356-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-15T00:00:00+08:00",
        "freeze_basis": "The exact source-selected statement and bounded immutable anchor inventory determine a Barkovsky Theorem 40 route through Hermite root counting, Cauchy indices, Sturm/Routh construction, regular and nonregular cases, no-pivot Hurwitz elimination, both implications, and exact root assembly. Eligibility is assigned before proof-phase closure credit.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": "M1356-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": denominators,
        "mandatory_layer_analysis": mandatory,
        "delta_policy": "Any semantic correction, split, merge, exclusion, eligibility, risk, or proof-body identity change requires registry version 2 and an append-only old/new ID delta; version 1 denominators remain reportable.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R4"},
            "known_terminal_proof_body_ids": [],
            "reason": "The exact proposition elaborates, but the anchor audit found no local, pinned-mathlib, or external Lean 4 proof body.",
        },
        "status_boundary": "Frozen architecture only. No obligation receives proof, H0, or R0 closure credit, and audit completion and theorem completion remain false.",
    }

    nodes = []
    obligation_by_id = {row["obligation_id"]: row for row in obligations}
    checked_interfaces = {
        "M1356-S-STATEMENT", "M1356-S-COEFFICIENT", "M1356-B-STABLE-TO-MINORS",
        "M1356-B-MINORS-TO-STABLE", "M1356-T-ASSEMBLE",
    }
    for row in SPECS:
        oid = row["id"]
        obligation = obligation_by_id[oid]
        nodes.append({
            "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
            "obligation_id": oid,
            "kind": row["kind"],
            "human_statement": row["claim"],
            "formal_target": row["formal"],
            "output": row["output"],
            "human_debt": "H1" if obligation["human_source_eligibility"] == "required" else "H2",
            "machine_debt": "M3" if oid in checked_interfaces or oid == "M1356-ROOT" else ("M5" if obligation["machine_eligibility"] == "not_applicable" else "M4"),
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "SRC-M1356-BARKOVSKY-V1-UNREVIEWED" if obligation["human_source_eligibility"] == "required" else "not-applicable",
            "provenance_id": "none",
            "foundation_profile": "Lean4-mathlib-classical/provisional; terminal axiom comparison and independent acceptance remain open",
            "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive compiled-artifact and release closure pending",
            "computation_record": "none; no numerical root finder, floating-point test, CAS, native evaluation, certificate, or oracle receives proof credit",
            "step_budget": row["budget"],
            "semantic_step_ledger": semantic_ledger(row),
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": "VAL-" + oid,
            "status_boundary": "Frozen plan or checked conditional interface only; the stated mathematical output and root closure remain open.",
            "task_ids": [ITEM, "S56-M-1356-PROOF"],
            "owned_sources": [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"] if oid in checked_interfaces else [],
            "owner": "THM-M-1356 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-15" if oid in checked_interfaces else None,
                "review_due": "before proof acceptance and after every invalidation input change",
                "invalidation_inputs": ["canonical statement", "registry", "source map", "toolchain", "dependency", "composition harness"],
                "revocation_state": "provisional" if oid in checked_interfaces else "open",
            },
        })

    proof_edges = []
    composition_certificates = []
    decomposition_plans = []
    checked_parents = {"M1356-ROOT", "M1356-T-ASSEMBLE"}
    for parent, children in REQUIRES.items():
        for child in children:
            req = "REQ-" + parent + "-" + child
            reverse = "REV-" + child + "-" + parent
            reverse_type = "composes" if parent in checked_parents else "logical_decomposition"
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, reverse),
                edge(reverse, child, reverse_type, parent, req),
            ])
        if parent in checked_parents:
            declaration = (
                "Stage1Instances.THM_M_1356.ObligationTree.root_of_directionPackage"
                if parent == "M1356-ROOT"
                else "Stage1Instances.THM_M_1356.ObligationTree.directionPackage_of_directions"
            )
            composition_certificates.append({
                "certificate_id": "COMP-" + parent,
                "parent_obligation_id": parent,
                "parent_statement_fingerprint": obligation_by_id[parent]["statement_fingerprint"],
                "required_child_ids": children,
                "required_child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in children},
                "checked_declaration": declaration,
                "certificate_kind": "lean_abstract_child_harness",
                "status": "provisionally_elaborated_not_accepted",
                "introduces_undeclared_premises": False,
                "proof_boundary": "Every substantive mathematical child is an explicit premise; no child closure is asserted.",
            })
        else:
            decomposition_plans.append({
                "plan_id": "DECOMP-" + parent,
                "parent_obligation_id": parent,
                "planned_child_ids": children,
                "source_locator": spec_by_id[parent]["source"],
                "status": "source_route_decomposition_unverified_as_child_to_parent_composition",
                "required_future_certificate": "An exact abstract-child Lean harness must bind these fingerprints and consume every child before parent closure.",
            })

    refinement_edges = [
        edge("REF-ROOT-STATEMENT", "M1356-ROOT", "logical_decomposition", "M1356-S-STATEMENT"),
        edge("REF-ROOT-COEFFICIENT", "M1356-ROOT", "logical_decomposition", "M1356-S-COEFFICIENT"),
        edge("REF-ROOT-BOUNDARIES", "M1356-ROOT", "logical_decomposition", "M1356-S-BOUNDARIES"),
    ]
    provenance_edges = []
    evidence_edges = []
    documentation_edges = []
    for oid in ids:
        if oid != "M1356-X-SOURCE" and obligation_by_id[oid]["human_source_eligibility"] == "required":
            provenance_edges.append(edge("SOURCE-MAP-" + oid, oid, "source_map", "M1356-X-SOURCE"))
        if oid not in {"M1356-X-PROVENANCE", "M1356-X-SOURCE", "M1356-X-TRUST", "M1356-X-READABLE", "M1356-X-WORKFLOW"}:
            provenance_edges.append(edge("PROVENANCE-" + oid, "M1356-X-PROVENANCE", "provenance_of", oid))
            evidence_edges.append(edge("EVIDENCE-" + oid, "M1356-X-PROVENANCE", "evidence_for", oid))
        if oid not in {"M1356-X-SOURCE", "M1356-X-READABLE"}:
            documentation_edges.append(edge("DOCUMENT-" + oid, "M1356-X-READABLE", "documents", oid))
    trust_edges = [
        edge("TRUST-FOUNDATION", "M1356-ROOT", "trusts", "M1356-S-FOUNDATION"),
        edge("TRUST-ROOT", "M1356-ROOT", "trusts", "M1356-X-TRUST"),
        edge("TRUST-PROVENANCE", "M1356-X-TRUST", "trusts", "M1356-X-PROVENANCE"),
        edge("TRUST-WORKFLOW", "M1356-X-WORKFLOW", "trusts", "M1356-X-TRUST"),
    ]
    workflow_tasks = [
        "S56-M-1356-ANCHOR_AUDIT", ITEM, "S56-M-1356-PROOF",
        "S56-M-1356-VALIDATION", "S56-M-1356-RELEASE",
    ]
    workflow_edges = [
        edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-1356-ANCHOR_AUDIT"),
        edge("FLOW-PROOF-TREE", "S56-M-1356-PROOF", "workflow_depends_on", ITEM),
        edge("FLOW-VALIDATION-PROOF", "S56-M-1356-VALIDATION", "workflow_depends_on", "S56-M-1356-PROOF"),
        edge("FLOW-RELEASE-VALIDATION", "S56-M-1356-RELEASE", "workflow_depends_on", "S56-M-1356-VALIDATION"),
    ]
    graphs = {
        "proof": indexed_graph(proof_edges),
        "refinement": indexed_graph(refinement_edges),
        "provenance": indexed_graph(provenance_edges),
        "evidence": indexed_graph(evidence_edges),
        "trust": indexed_graph(trust_edges),
        "documentation": indexed_graph(documentation_edges),
        "workflow": indexed_graph(workflow_edges),
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": "M1356-ROOT",
        "edge_direction": "Proof requirements run parent to child; reciprocal composes or logical_decomposition edges run child to parent. Workflow dependencies run task to prerequisite.",
        "workflow_task_nodes": workflow_tasks,
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": composition_certificates,
        "unverified_decomposition_plans": decomposition_plans,
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R4"},
            "minimal_open_proof_cut_set": ["M1356-B-STABLE-TO-MINORS", "M1356-B-MINORS-TO-STABLE"],
            "implementation_leaf_frontier": ["M1356-C-EVEN-ODD-DEFS", "M1356-C-SIGNED-REMAINDER", "M1356-L-LINEAR-HODOGRAPH", "M1356-L-CROSSING-INTERIOR", "M1356-L-CROSSING-ENDS", "M1356-L-STURM-NOJUMP", "M1356-L-STURM-POLE-JUMP", "M1356-B-TERMINAL-SPLIT", "M1356-L-GAUSS-STEP", "M1356-L-TRIANGULAR-DET"],
            "provisionally_checked_interfaces": ["M1356-S-STATEMENT", "M1356-S-COEFFICIENT", "M1356-B-STABLE-TO-MINORS", "M1356-B-MINORS-TO-STABLE", "M1356-T-ASSEMBLE"],
            "remaining_release_cut_set": ["M1356-X-SOURCE", "M1356-S-FOUNDATION", "M1356-X-PROVENANCE", "M1356-X-TRUST", "M1356-X-READABLE", "M1356-X-WORKFLOW", "hermetic replay", "independent verification", "master acceptance"],
            "known_terminal_proof_body_ids": [],
            "reason": "Only the exact final conditional composition interfaces elaborate. Every substantive Routh-Hurwitz proof node, source review, provenance/trust gate, and release gate remains open.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "recipes": [],
    }
    for oid in ids:
        recipes["recipes"].append({
            "recipe_id": "VAL-" + oid,
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {
                "PATH": "runner-provided tool path",
                "HOME": "runner-provided toolchain home",
                "TMPDIR": "runner-provided temporary directory",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains structural PASS, the frozen denominator, exact conditional Lean composition, and open H1/M3/R4 root",
            }],
            "covered_obligation_ids": [oid],
            "covered_declarations": [
                "Stage1Instances.THM_M_1356.RouthHurwitzTarget",
                "Stage1Instances.THM_M_1356.ObligationTree.root_of_directions",
            ] if oid in {"M1356-S-STATEMENT", "M1356-T-ASSEMBLE"} else [],
        })

    markdown = [
        "# THM-M-1356 frozen obligation architecture",
        "",
        f"Item: `{ITEM}`.",
        "",
        f"Registry version 1 freezes {len(ids)} canonical obligations before proof-phase closure credit.",
        "The route expands Barkovsky's one-line proof of Theorem 40 through the Hermite root-count",
        "bridge, Cauchy-index and Sturm theorems, the regular and nonregular Routh cases, no-pivot",
        "Gaussian elimination of the finite Hurwitz matrix, both logical directions, and exact root",
        "assembly. Provenance, evidence, trust, documentation, and workflow edges remain separate",
        "from mathematical proof requirements.",
        "",
        "## Proof route",
        "",
        "```text",
        "ROOT -> exact direction assembly",
        "  stable -> positive minors",
        "    complete Routh criterion -> Hermite -> Cauchy index -> Sturm variations",
        "                             -> regular signs + nonregular terminal cases",
        "    Hurwitz minors -> no-pivot elimination -> products of Routh coefficients",
        "  positive minors -> stable (same two engines, reverse implication)",
        "```",
        "",
        "Only the two final abstract-child composition declarations are checked here. Every internal",
        "source route is an explicitly unverified decomposition until a future Lean harness consumes",
        "the exact child fingerprints. No source, provenance, trust, or documentation edge can close",
        "a proof obligation.",
        "",
        "## Node ledger",
        "",
    ]
    for row in SPECS:
        oid = row["id"]
        markdown.extend([
            f'<a id="{oid.lower()}"></a>',
            f"### {oid}",
            "",
            row["claim"],
            "",
            f"Formal target: `{row['formal']}`",
            "",
            f"Output: {row['output']}",
            "",
            f"Source boundary: {row['source']}",
            "",
            f"Step budget: `{row['budget']}`; structured ledger entries: `{len(semantic_ledger(row))}`.",
            "",
            "Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.",
            "",
        ])
    markdown.extend([
        "## Freeze boundary",
        "",
        "No obligation is accepted closed. The root remains `[H1, M3, R4]`: the exact proposition",
        "elaborates, but no Lean proof body for either direction was discovered. Pinpoint proof/errata",
        "review, every substantive machine node, readable `R0`, transitive provenance and trust,",
        "hermetic replay, independent verification, audit completion, theorem completion, and master",
        "acceptance remain open. An architecture or eligibility change requires a new registry version",
        "and an append-only delta; it must not rewrite version 1 denominators.",
        "",
    ])
    return registry, bundle, recipes, "\n".join(markdown)


def write() -> None:
    registry, bundle, recipes, markdown = build()
    outputs = {
        "obligation-registry.json": json.dumps(registry, indent=2, ensure_ascii=True) + "\n",
        "typed-graphs.json": json.dumps(bundle, indent=2, ensure_ascii=True) + "\n",
        "validation-specs.json": json.dumps(recipes, indent=2, ensure_ascii=True) + "\n",
        "obligation-tree.md": markdown,
    }
    for name, content in outputs.items():
        (HERE / name).write_text(content, encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    step_count = sum(len(node["semantic_step_ledger"]) for node in bundle["nodes"])
    print(f"wrote {len(registry['obligations'])} obligations, {edge_count} typed edges, and {step_count} ledger steps")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    write()
