#!/usr/bin/env python3
"""Build the frozen THM-M-0487 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0487-OBLIGATION_TREE"
THEOREM = "THM-M-0487"
PREFIX = "M0487-"
ROOT_EXPRESSION = "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"
ANALYTIC_CUTOFF = "1000000000000000000000000000"
FINITE_UPPER = "8875694145621773516800000000000"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# short id, kind, risk, claim, formal target, output, machine eligibility,
# human-source eligibility, proof-body identity, substantive-step split budget
ROWS = (
    (
        "ROOT", "root", "critical",
        "Every odd natural n with 5 < n is a sum of three natural primes, with repetition permitted.",
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget",
        "The exact frozen weak Goldbach proposition.",
        "required", "required", None, 12,
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Preserve n : Nat, 5 < n, Odd n, three independent Nat.Prime witnesses, and n = p + q + r in the frozen order.",
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget",
        "The exact canonical binder and witness interface.",
        "required", "not_applicable", None, 16,
    ),
    (
        "S-DOMAIN", "transport", "high",
        "Transport exactly between the positive integer source domain and the canonical natural domain.",
        "Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_integerWeakGoldbachTarget",
        "The checked Nat/Int source-domain equivalence.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_integerWeakGoldbachTarget", 18,
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Exclude five and even inputs, include seven as 2 + 2 + 3, and retain repetition and the even prime two.",
        "five_excluded; seven_included; seven_repeated_prime_representation; eight_not_odd",
        "The exhaustive threshold, parity, and prime-witness boundary policy.",
        "required", "not_applicable", None, 20,
    ),
    (
        "S-TRANSPORT", "transport", "high",
        "Transport equality orientation without changing domains, hypotheses, association, witness order, or prime requirements.",
        "Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget",
        "The checked equality-orientation equivalence.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget", 12,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Fix the Lean kernel, logic, choice, analytic foundations, computation policy, and no-oracle boundary.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation and computation policy.",
        "required", "not_applicable", None, 40,
    ),
    (
        "N-REPRESENTATION", "normalization", "high",
        "Normalize both source branches to the canonical three-natural-prime existential predicate.",
        "Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff",
        "ThreePrimeRepresentation n iff the exact canonical existential conclusion.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff", 12,
    ),
    (
        "N-CUTOFF", "normalization", "critical",
        f"Freeze the exact cutoff {ANALYTIC_CUTOFF}, with finite inputs below it and analytic inputs at or above it.",
        "Stage1Instances.THM_M_0487.ObligationTree.analyticCutoff",
        "The fixed Nat cutoff and endpoint conventions.",
        "required", "required", None, 12,
    ),
    (
        "B-RANGE-SPLIT", "branch", "critical",
        "Prove every input is in exactly n < analyticCutoff or analyticCutoff <= n and preserve the cutoff endpoint on the analytic side.",
        "Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases",
        "An exhaustive disjoint finite/analytic case split.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases", 16,
    ),
    (
        "C-ANALYTIC-PARAMETERS", "construction", "critical",
        "Construct one compatible parameter record for x, r0, smoothing scale, character ranges, and explicit error constants at n >= 10^27.",
        "planned AnalyticParameterPackage",
        "Well-formed parameters shared by both arc branches.",
        "required", "required", None, 70,
    ),
    (
        "C-WEIGHTS", "construction", "critical",
        "Construct the eta-plus and eta-star smoothing functions with support, sign, norm, transform, and compatibility invariants.",
        "planned GoldbachSmoothingPackage",
        "The exact nonnegative weights and invariants used by the weighted count.",
        "required", "required", None, 70,
    ),
    (
        "N-WEIGHTED-FOURIER", "normalization", "critical",
        "Express the weighted von-Mangoldt representation sum as the exact circle integral for the common parameters and weights.",
        "planned WeightedTernaryFourierIdentity",
        "An equality between the weighted arithmetic sum and the full circle integral.",
        "required", "required", None, 85,
    ),
    (
        "C-MAJOR-ARCS", "construction", "high",
        "Construct the disjoint major arcs around reduced rationals with the frozen common parameters.",
        "planned MajorArcConstruction",
        "A measurable major-arc set with well-definedness and disjointness invariants.",
        "required", "required", None, 55,
    ),
    (
        "C-MINOR-ARCS", "construction", "high",
        "Construct the minor arcs as the exact measurable complement of the common major arcs.",
        "planned MinorArcConstruction",
        "The complementary measurable minor-arc set.",
        "required", "required", None, 30,
    ),
    (
        "B-ARCS", "branch", "critical",
        "Prove the common major and minor arcs are disjoint, exhaustive, and recompose the full circle integral.",
        "planned MajorMinorArcPartition",
        "Exact integral decomposition into the two arc branches.",
        "required", "required", None, 45,
    ),
    (
        "B-MAJOR-CHARACTERS", "branch", "critical",
        "Split the major-arc exponential sums into principal and nonprincipal Dirichlet-character contributions and prove exhaustive recomposition.",
        "planned MajorArcCharacterDecomposition",
        "All character terms and their common reconstruction.",
        "required", "required", None, 70,
    ),
    (
        "L-MAJOR-CHARACTERS", "bridge", "critical",
        "Supply the explicit character-sum estimates, including the bounded L-function verification boundary, uniformly on every major arc.",
        "Helfgott major-arcs Main Theorem package, formalization planned",
        "Uniform estimates for every character term.",
        "required", "required", None, 95,
    ),
    (
        "L-MAJOR-MAIN", "core_lemma", "critical",
        "Extract the major-arc main term and prove positivity of its singular and archimedean factors for odd inputs.",
        "planned MajorArcMainTermPositive",
        "A uniform positive main-term lower bound.",
        "required", "required", None, 85,
    ),
    (
        "L-MAJOR-ERROR", "core_lemma", "critical",
        "Bound every truncation, smoothing, transform, character, and completion error in the major-arc evaluation.",
        "planned MajorArcErrorBound",
        "A uniform error bound compatible with the main term.",
        "required", "required", None, 90,
    ),
    (
        "T-MAJOR", "terminal", "critical",
        "Combine the character decomposition, positive main term, and all errors into the explicit major-arc lower bound.",
        "planned MajorArcLowerBound",
        "The source-compatible major-arc lower bound.",
        "required", "required", None, 45,
    ),
    (
        "L-MINOR-EXP-SUM", "bridge", "critical",
        "Supply the explicit pointwise exponential-sum estimates over the nested minor-arc ranges.",
        "Helfgott minor-arcs section 1.1 package, formalization planned",
        "Uniform pointwise minor-arc exponential-sum bounds.",
        "required", "required", None, 95,
    ),
    (
        "L-LARGE-SIEVE", "core_lemma", "critical",
        "Prove the explicit prime-supported large-sieve and L2 estimates used to integrate the pointwise minor-arc bounds.",
        "planned ExplicitPrimeLargeSievePackage",
        "Uniform L2 control over the arc ranges.",
        "required", "required", None, 95,
    ),
    (
        "L-MINOR-TOTAL", "core_lemma", "critical",
        "Combine the pointwise and L2 estimates by the source's partial-summation argument into the total minor-arc bound.",
        "planned MinorArcIntegralBound",
        "The absolute minor-arc contribution upper bound.",
        "required", "required", None, 85,
    ),
    (
        "T-MINOR", "terminal", "critical",
        "Package the common-parameter minor-arc integral upper bound consumed by analytic positivity.",
        "planned MinorArcUpperBound",
        "The source-compatible minor-arc upper bound.",
        "required", "required", None, 35,
    ),
    (
        "L-ANALYTIC-DOMINANCE", "core_lemma", "critical",
        "Verify the explicit numerical constants and prove the major lower bound strictly exceeds all minor and error contributions for n >= 10^27.",
        "planned AnalyticDominanceAtCutoff",
        "Strict positivity of the full weighted representation sum.",
        "required", "required", None, 80,
    ),
    (
        "T-ANALYTIC-POSITIVE", "terminal", "critical",
        "Use the Fourier identity, exact arc partition, compatible estimates, and dominance to prove weighted-sum positivity.",
        "planned WeightedRepresentationPositive",
        "A positive weighted von-Mangoldt representation sum for every odd n at or above the cutoff.",
        "required", "required", None, 45,
    ),
    (
        "L-PRIME-POWER-ERROR", "core_lemma", "critical",
        "Bound the contribution of powers of primes, the even term, and all non-prime-supported von-Mangoldt terms below the positive margin.",
        "planned PrimePowerContributionBound",
        "A strict positive contribution remains from three actual odd primes.",
        "required", "required", None, 75,
    ),
    (
        "L-PRIME-EXTRACT", "core_lemma", "critical",
        "Extract three actual prime witnesses from positive weighted prime support and transport the source equality to ThreePrimeRepresentation.",
        "planned PrimeWitnessExtraction",
        "ThreePrimeRepresentation n on the analytic range.",
        "required", "required", None, 55,
    ),
    (
        "T-ANALYTIC", "terminal", "critical",
        "Compose analytic positivity, prime-power removal, and witness extraction into the exact inclusive analytic range package.",
        "Stage1Instances.THM_M_0487.ObligationTree.AnalyticRangePackage",
        "Every odd n >= 10^27 has the canonical three-prime representation.",
        "required", "required", None, 35,
    ),
    (
        "N-FINITE-COVERAGE", "normalization", "high",
        f"Restrict the exact finite upper interval ending at {FINITE_UPPER} to every canonical input below {ANALYTIC_CUTOFF}.",
        "Stage1Instances.THM_M_0487.ObligationTree.finiteCoverage_of_publishedUpper",
        "Every n below analyticCutoff lies in the exact published inclusive interval.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0487.ObligationTree.finiteCoverage_of_publishedUpper", 18,
    ),
    (
        "B-FINITE-REDUCTION", "branch", "critical",
        "Split finite odd inputs into the base binary-Goldbach interval and the prime-ladder extension, with endpoint and parity exhaustiveness.",
        "planned FiniteRangeReductionCases",
        "Every finite input is assigned to a complete reduction branch.",
        "required", "required", None, 55,
    ),
    (
        "L-FINITE-REDUCTION", "core_lemma", "critical",
        "Reduce an odd n to n - p in the verified even binary range using a certified nearby prime p, preserving positivity and parity.",
        "planned PrimeLadderToTernaryReduction",
        "A nearby prime plus an even two-prime representation yields a canonical three-prime representation.",
        "required", "required", None, 65,
    ),
    (
        "C-FINITE-FORMAT", "construction", "critical",
        "Specify the complete finite input domain, ladder rows, Proth witnesses, general-prime certificates, exact endpoints, serialization, and ordering invariants.",
        "planned FiniteCertificateFormat",
        "A canonical certificate format with no omitted range.",
        "required", "required", None, 70,
    ),
    (
        "C-PRIME-LADDER", "construction", "critical",
        "Construct the prime ladder from admitted rows and prove monotonicity, primality labels, first/last coverage, and maximum-gap invariants.",
        "planned PrimeLadderCertificate",
        "A fully covered, tightly spaced certified prime sequence.",
        "required", "required", None, 80,
    ),
    (
        "L-PROTH-CERTIFICATES", "certificate", "critical",
        "Kernel-check every Proth-form primality witness through Proth's theorem with exact modular and Jacobi computations.",
        "planned ProthCertificateSoundness",
        "Primality of every Proth ladder rung.",
        "required", "required", None, 85,
    ),
    (
        "L-GENERAL-PRIME-CERTIFICATES", "certificate", "critical",
        "Kernel-check every general-form ladder prime through a complete primality certificate rather than a probable-prime oracle.",
        "planned GeneralPrimeCertificateSoundness",
        "Primality of every general-form ladder rung.",
        "required", "required", None, 85,
    ),
    (
        "L-PRIME-GAP-COVERAGE", "computation", "critical",
        "Replay every row, reject tampering or omissions, and prove consecutive gaps and boundary gaps meet the exact finite-domain bound.",
        "planned PrimeLadderCoverageCheckerSound",
        "Exhaustive nearby-prime coverage through the exact upper endpoint.",
        "required", "required", None, 85,
    ),
    (
        "L-BINARY-GOLDBACH-FINITE", "bridge", "critical",
        "Admit and replay the complete verification that every even m from 4 through 4 * 10^18 is a sum of two primes.",
        "planned BinaryGoldbachFiniteCertificateSound",
        "Two prime witnesses for every even remainder produced by the ladder reduction.",
        "required", "required", None, 90,
    ),
    (
        "L-FINITE-CHECKER-SOUND", "certificate", "critical",
        "Prove the finite checker accepts only complete, well-formed, primality-valid, gap-valid, endpoint-bound certificate bundles.",
        "planned FiniteGoldbachCheckerSoundness",
        "Checker acceptance implies every claimed certificate invariant.",
        "required", "required", None, 90,
    ),
    (
        "T-FINITE-UPPER", "terminal", "critical",
        "Compose the finite cases, certificate soundness, prime ladder, binary verification, and ternary reduction into the exact upper-interval theorem.",
        "Stage1Instances.THM_M_0487.ObligationTree.FiniteUpperBoundPackage",
        f"Every odd n with 5 < n <= {FINITE_UPPER} has ThreePrimeRepresentation n.",
        "required", "required", None, 55,
    ),
    (
        "T-FINITE", "terminal", "critical",
        "Restrict the exact upper-interval theorem through the checked endpoint inequality to the finite side of the root cutoff.",
        "Stage1Instances.THM_M_0487.ObligationTree.FiniteRangePackage",
        "Every odd 5 < n < 10^27 has the canonical representation.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0487.ObligationTree.finiteRange_of_publishedFiniteUpper", 20,
    ),
    (
        "T-ASSEMBLE", "terminal", "critical",
        "Consume both exact range packages and the exhaustive cutoff split to yield the exact frozen root with no extra premise.",
        "Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite",
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite", 18,
    ),
    (
        "X-SOURCE-MAIN", "source_boundary", "critical",
        "Pin and independently review the exact main theorem, source-domain conventions, final analytic/finite merge, corrections, and errata.",
        "Helfgott arXiv:1312.7748v2 main source packet pending",
        "Main-paper human-source coverage without machine proof credit.",
        "not_applicable", "required", None, 45,
    ),
    (
        "X-SOURCE-MAJOR", "source_boundary", "critical",
        "Pin and crosswalk the upstream major-arcs Main Theorem and bounded L-function computation used by the main paper.",
        "Helfgott major-arcs source packet pending",
        "Major-arc source coverage without machine proof credit.",
        "not_applicable", "required", None, 60,
    ),
    (
        "X-SOURCE-MINOR", "source_boundary", "critical",
        "Pin and crosswalk the upstream minor-arcs section 1.1 estimates used by the main paper.",
        "Helfgott minor-arcs source packet pending",
        "Minor-arc source coverage without machine proof credit.",
        "not_applicable", "required", None, 60,
    ),
    (
        "X-SOURCE-PRIME-BOUNDS", "source_boundary", "high",
        "Pin and crosswalk every explicit prime, theta, von-Mangoldt, and prime-power estimate used at the analytic endpoint.",
        "explicit prime-bound source packets pending",
        "Explicit-estimate source coverage without machine proof credit.",
        "not_applicable", "required", None, 55,
    ),
    (
        "X-SOURCE-FINITE", "source_boundary", "critical",
        "Pin and independently review Helfgott-Platt, binary Goldbach verification, Proth/ECPP dependencies, exact interval, and computation claims.",
        "Helfgott-Platt arXiv:1305.3062v2 and finite dependencies pending admission",
        "Finite-route human-source coverage without machine proof credit.",
        "not_applicable", "required", None, 60,
    ),
    (
        "X-COMPUTATION", "certificate", "critical",
        "Inventory producer, complete inputs and hashes, seeds, environments, output digests, certificate format, checker identity, determinism, resources, replay, tamper, and incomplete-domain fixtures.",
        "release computation record pending",
        "Computation provenance and replay assurance without replacing proof-relevant soundness nodes.",
        "informational", "not_applicable", None, 70,
    ),
    (
        "X-EVIDENCE", "certificate", "critical",
        "Bind every node validation recipe to immutable raw results, statement fingerprints, source inputs, and receipt identities.",
        "content-addressed evidence bundle pending",
        "Node evidence without independent proof credit.",
        "informational", "not_applicable", None, 50,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Resolve every local wrapper, imported theorem, analytic boundary, certificate, checker, source hash, license, and terminal proof body.",
        "transitive proof and computation provenance closure pending",
        "Body-level provenance without duplicate proof credit.",
        "informational", "not_applicable", None, 65,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit Lean, mathlib, compiled artifacts, analytic foundations, certificate checkers, external code, unsafe/oracle boundaries, and supply chain transitively.",
        "release trust and TCB closure pending",
        "Release-grade trust inventory without mathematical proof credit.",
        "informational", "not_applicable", None, 65,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide and independently review a node-complete readable reconstruction of both the analytic and finite routes.",
        "node-specific readable reconstruction pending",
        "Readable coverage and review without machine proof credit.",
        "not_applicable", "not_applicable", None, 80,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, hermetic replay, independent verification, release, freshness, revocation, and incident task acceptance.",
        "Stage1 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 30,
    ),
    (
        "X-REJECTED-CANDIDATES", "certificate", "normal",
        "Preserve the exact-placeholder, bounded-placeholder-ancestry, binary, and conditional-scaffold dispositions without proof edges or coverage credit.",
        "anchor-audit rejected candidate inventory",
        "Deduplicated negative provenance only.",
        "informational", "not_applicable", None, 25,
    ),
)


CHECKED_INTERFACES = {
    oid("S-INTERFACE"),
    oid("S-DOMAIN"),
    oid("S-BOUNDARY"),
    oid("S-TRANSPORT"),
    oid("N-REPRESENTATION"),
    oid("N-CUTOFF"),
    oid("B-RANGE-SPLIT"),
    oid("N-FINITE-COVERAGE"),
    oid("T-FINITE"),
    oid("T-ASSEMBLE"),
}


LEAN_TARGET_FINGERPRINTS = {
    oid("S-DOMAIN"): digest([
        "Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_integerWeakGoldbachTarget",
        "WeakGoldbachTarget <-> IntegerWeakGoldbachTarget",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("S-BOUNDARY"): digest([
        "five_excluded", "five_not_three_prime_sum",
        "mutationIncludedFiveBoundary_is_false",
        "mutationChangedDomainToFinEight_is_true", "seven_included",
        "seven_repeated_prime_representation", "eight_not_odd",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("S-TRANSPORT"): digest([
        "Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget",
        "WeakGoldbachTarget <-> ReversedEqualityWeakGoldbachTarget",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("N-REPRESENTATION"): digest([
        "Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff",
        "forall n, ThreePrimeRepresentation n <-> exists p q r, Nat.Prime p and Nat.Prime q and Nat.Prime r and n = p + q + r",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("N-CUTOFF"): digest([
        "analyticCutoff=10^27", "publishedFiniteUpper=8875694145621773516800000000000",
        "five_lt_analyticCutoff", "analyticCutoff_le_publishedFiniteUpper",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("B-RANGE-SPLIT"): digest([
        "Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases",
        "forall n, n < analyticCutoff or analyticCutoff <= n",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("N-FINITE-COVERAGE"): digest([
        "Stage1Instances.THM_M_0487.ObligationTree.finiteCoverage_of_publishedUpper",
        "forall n, n < analyticCutoff -> n <= publishedFiniteUpper",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("T-FINITE"): digest([
        "Stage1Instances.THM_M_0487.ObligationTree.finiteRange_of_publishedFiniteUpper",
        "FiniteUpperBoundPackage -> FiniteRangePackage",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
    oid("T-ASSEMBLE"): digest([
        "Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite",
        "CutoffPartitionPackage -> AnalyticRangePackage -> FiniteRangePackage -> WeakGoldbachTarget",
        "autoImplicit=false;lean=4.29.0;mathlib=8a178386ffc0",
    ]),
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    exclusions = {
        oid("S-INTERFACE"): "formal_statement_interface_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-DOMAIN"): "formal_domain_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-BOUNDARY"): "formal_boundary_fixtures_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-TRANSPORT"): "formal_encoding_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
        oid("X-SOURCE-MAIN"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-SOURCE-MAJOR"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-SOURCE-MINOR"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-SOURCE-PRIME-BOUNDS"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-SOURCE-FINITE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-COMPUTATION"): "release_computation_overlay_no_proof_credit_pending_integration_review",
        oid("X-EVIDENCE"): "release_evidence_overlay_no_proof_credit_pending_integration_review",
        oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
        oid("X-REJECTED-CANDIDATES"): "negative_provenance_overlay_no_proof_credit_pending_integration_review",
    }

    source_na = {
        identifier for identifier, reason in exclusions.items()
        if "source_coverage_inherited" in reason
        or "formal_trust" in reason
        or "overlay_no_proof_credit" in reason
    }
    local_computation_ids = {
        oid("C-FINITE-FORMAT"), oid("C-PRIME-LADDER"),
        oid("L-PROTH-CERTIFICATES"), oid("L-GENERAL-PRIME-CERTIFICATES"),
        oid("L-PRIME-GAP-COVERAGE"), oid("L-BINARY-GOLDBACH-FINITE"),
        oid("L-FINITE-CHECKER-SOUND"), oid("T-FINITE-UPPER"), oid("T-FINITE"),
    }

    row_ids = [oid(row[0]) for row in ROWS]
    proof_children = {
        oid("ROOT"): [oid("T-ASSEMBLE")],
        oid("T-ASSEMBLE"): [oid("B-RANGE-SPLIT"), oid("T-ANALYTIC"), oid("T-FINITE")],
        oid("B-RANGE-SPLIT"): [oid("N-CUTOFF")],
        oid("T-ANALYTIC"): [oid("L-PRIME-EXTRACT"), oid("N-REPRESENTATION")],
        oid("T-ANALYTIC-POSITIVE"): [oid("N-WEIGHTED-FOURIER"), oid("B-ARCS"), oid("L-ANALYTIC-DOMINANCE")],
        oid("N-WEIGHTED-FOURIER"): [oid("C-ANALYTIC-PARAMETERS"), oid("C-WEIGHTS")],
        oid("B-ARCS"): [oid("C-MAJOR-ARCS"), oid("C-MINOR-ARCS"), oid("C-ANALYTIC-PARAMETERS")],
        oid("T-MAJOR"): [oid("B-MAJOR-CHARACTERS"), oid("L-MAJOR-MAIN"), oid("L-MAJOR-ERROR")],
        oid("B-MAJOR-CHARACTERS"): [oid("L-MAJOR-CHARACTERS"), oid("C-MAJOR-ARCS"), oid("C-ANALYTIC-PARAMETERS")],
        oid("L-MAJOR-MAIN"): [oid("C-WEIGHTS"), oid("C-ANALYTIC-PARAMETERS")],
        oid("L-MAJOR-ERROR"): [oid("L-MAJOR-CHARACTERS"), oid("C-WEIGHTS"), oid("C-ANALYTIC-PARAMETERS")],
        oid("T-MINOR"): [oid("L-MINOR-TOTAL")],
        oid("L-MINOR-TOTAL"): [oid("L-MINOR-EXP-SUM"), oid("L-LARGE-SIEVE"), oid("C-MINOR-ARCS"), oid("C-WEIGHTS"), oid("C-ANALYTIC-PARAMETERS")],
        oid("L-ANALYTIC-DOMINANCE"): [oid("T-MAJOR"), oid("T-MINOR"), oid("N-CUTOFF")],
        oid("L-PRIME-POWER-ERROR"): [oid("C-WEIGHTS"), oid("N-CUTOFF")],
        oid("L-PRIME-EXTRACT"): [oid("T-ANALYTIC-POSITIVE"), oid("L-PRIME-POWER-ERROR")],
        oid("T-FINITE"): [oid("N-FINITE-COVERAGE"), oid("T-FINITE-UPPER")],
        oid("N-FINITE-COVERAGE"): [oid("N-CUTOFF")],
        oid("T-FINITE-UPPER"): [oid("L-FINITE-REDUCTION"), oid("N-REPRESENTATION")],
        oid("B-FINITE-REDUCTION"): [oid("C-FINITE-FORMAT")],
        oid("C-PRIME-LADDER"): [oid("C-FINITE-FORMAT"), oid("L-PROTH-CERTIFICATES"), oid("L-GENERAL-PRIME-CERTIFICATES"), oid("L-PRIME-GAP-COVERAGE")],
        oid("L-PRIME-GAP-COVERAGE"): [oid("C-FINITE-FORMAT"), oid("L-FINITE-CHECKER-SOUND")],
        oid("L-FINITE-CHECKER-SOUND"): [oid("C-FINITE-FORMAT"), oid("L-PROTH-CERTIFICATES"), oid("L-GENERAL-PRIME-CERTIFICATES")],
        oid("L-FINITE-REDUCTION"): [oid("B-FINITE-REDUCTION"), oid("C-PRIME-LADDER"), oid("L-BINARY-GOLDBACH-FINITE")],
    }
    proof_parents = {
        identifier: [parent for parent, children in proof_children.items() if identifier in children]
        for identifier in row_ids
    }

    for short, kind, risk, claim, target, output, machine, human_source, body, budget in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")}
            else f"lean-target-context-sha256:{LEAN_TARGET_FINGERPRINTS[identifier]}"
            if identifier in LEAN_TARGET_FINGERPRINTS
            else "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": not short.startswith("X-"),
                "machine_eligibility": machine,
                "human_source_eligibility": human_source,
                "readable_eligibility": "required",
                "risk_class": risk,
                "exclusion_reason": exclusions.get(identifier),
                "terminal_proof_body_id": body,
            }
        )

        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
        elif identifier == oid("X-REJECTED-CANDIDATES"):
            machine_debt = "M5"
        else:
            machine_debt = "M4"
        if identifier in CHECKED_INTERFACES:
            provenance = "local-checked-interface"
        elif identifier == oid("X-REJECTED-CANDIDATES"):
            provenance = "anchor-audit:seven-member-candidate-inventory"
        elif identifier in local_computation_ids:
            provenance = "finite-source-lead-only-no-admitted-certificate"
        elif short.startswith(("L-MAJOR", "L-MINOR")):
            provenance = "analytic-source-boundary-unformalized"
        else:
            provenance = "none"
        owned_sources = [
            "Stage1_Instances/THM-M-0487/obligation-registry.json",
            "Stage1_Instances/THM-M-0487/typed-graphs.json",
            f"Stage1_Instances/THM-M-0487/obligation-tree.md#{identifier.lower()}",
        ]
        if identifier in CHECKED_INTERFACES:
            owned_sources.append(
                "Stage1_Instances/THM-M-0487/Statement.lean"
                if identifier in {oid("S-INTERFACE"), oid("S-DOMAIN"), oid("S-BOUNDARY"), oid("S-TRANSPORT")}
                else "Stage1_Instances/THM-M-0487/ObligationTree.lean"
            )
        computation_record = (
            "open certificate_replayed_by_kernel route: complete domain/input digests, producer and version, seed/environment, output digest, certificate format, checker identity/theorem, determinism, resource bounds, replay, tamper, and incomplete-domain fixtures are all pending; no computation credit"
            if identifier in local_computation_ids or identifier == oid("X-COMPUTATION")
            else "none; no computation, oracle, experiment, native shortcut, or unchecked certificate is credited"
        )
        nodes.append(
            {
                "node_id": f"{THEOREM}-{short}",
                "obligation_id": identifier,
                "kind": kind,
                "human_statement": claim,
                "formal_target": target,
                "output": output,
                "human_debt": "H1",
                "machine_debt": machine_debt,
                "readability_debt": "R3",
                "evidence_ids": [],
                "source_crosswalk_id": (
                    "not-applicable-pending-review"
                    if identifier in source_na else "primary-source-node-map-pending"
                ),
                "provenance_id": provenance,
                "foundation_profile": "lean4-dependent-type-theory; analytic foundations, accepted axiom policy, and transitive review pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; analytic libraries, computation checkers, transitive closure, and independent replay pending",
                "computation_record": computation_record,
                "step_budget": budget,
                "semantic_step_ledger": {
                    "premises": proof_children.get(identifier, []),
                    "inference": (
                        f"kernel-checked declaration {target}"
                        if identifier in CHECKED_INTERFACES
                        else f"planned {kind} inference/source boundary: {target}"
                    ),
                    "output": output,
                    "outgoing_use": proof_parents[identifier],
                },
                "public_readable_target": f"Stage1_Instances/THM-M-0487/obligation-tree.md#{identifier.lower()}",
                "validation_spec_id": f"VAL-{identifier}",
                "status_boundary": (
                    "Checked conditional interface only; this does not close either deep branch or the root."
                    if identifier in CHECKED_INTERFACES
                    else "Non-proof overlay with no semantic proof credit."
                    if short.startswith("X-")
                    else "Open package: the budget is a split threshold, not a leaf-adequacy or proof-closure claim; substantive ledgers and any further required split remain proof-phase work."
                ),
                "task_ids": [ITEM, "S56-M-0487-PROOF"],
                "owned_sources": owned_sources,
                "owner": "THM-M-0487 proof lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                    "review_due": "before proof acceptance",
                    "invalidation_inputs": [
                        "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                        "typed-graphs.json", "analytic or finite source", "toolchain and dependency pins",
                    ],
                    "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
                },
            }
        )

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0487-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T22:30:00+08:00",
        "freeze_basis": "The exact statement, inspected Helfgott analytic route, the Helfgott-Platt finite route plus a selected fail-closed formal certificate refinement, and the prerequisite candidate audit. The certificate format and kernel replay nodes are planned formalization architecture, not historical artifacts claimed by the finite paper. Eligibility, risks, and denominators are fixed before observing per-obligation closure metrics.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "source_architecture_inputs": {
            "helfgott_main_arxiv": "1312.7748v2",
            "helfgott_main_source_url": "https://arxiv.org/src/1312.7748v2",
            "helfgott_main_tex_sha256": "86ea555015d974174c744dbf7b78d777015e959f2986c0b9b6873634f44e0fed",
            "helfgott_main_locators": "Main Theorem lines 123-127; architecture lines 298-548; final composition lines 5313-5391 of ternvin.tex",
            "helfgott_platt_arxiv": "1305.3062v2",
            "helfgott_platt_source_url": "https://arxiv.org/src/1305.3062v2",
            "helfgott_platt_compressed_source_sha256": "376ec723223d4f014e55f80263137b88800c3a71d6c021cdab0a476b171bf408",
            "helfgott_platt_decompressed_tex_sha256": "5a9026c9850de02d7e5e78e8da734afadde0104a4be76d2cfabc74b1aae50dac",
            "helfgott_platt_locators": "abstract lines 94-96; exact interval theorem lines 206-211 of decompressed arXiv source",
            "helfgott_platt_exact_upper_endpoint": FINITE_UPPER,
            "helfgott_platt_lean_nat_literal": "8875694145621773516800000000000",
            "finite_formalization_refinement": "Selected future certificate-replayed-by-kernel architecture. The paper reports a C++/CLN computation and independent checks; deleted/unavailable historical data and lack of an admitted certificate bundle remain reproduction blockers.",
            "admission_boundary": "content-hashed source leads inspected during worker audit; neither source bundle nor computation is accepted H0/M0 evidence",
        },
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "symmetry_and_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "Summand order and equality orientation are presentation transports in S-TRANSPORT; the proof needs no quotient by permutations or canonical ordering.",
            },
            "local_global_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No local-global principle is used; the only global split is the exact numeric cutoff represented by N-CUTOFF and B-RANGE-SPLIT.",
            },
            "additional_root_branches": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "Parity and lower-bound exclusions are frozen in S-BOUNDARY; all root-admissible inputs are exhausted by the finite/analytic split.",
            },
        },
        "candidate_dispositions": {
            "M0487-C01-LOCAL-STATEMENT": "exact_statement_only_M3_no_terminal_proof_no_proof_edge",
            "M0487-C02-MATHLIB-SUPPORT": "support_only_no_target_conclusion_no_proof_edge",
            "M0487-C03-FORMAL-CONJECTURES-EXACT-PLACEHOLDER": "M5_rejected_no_proof_edge",
            "M0487-C04-PRIME-NUMBER-THEOREM-AND-FINITE": "M5_bounded_placeholder_ancestry_no_proof_edge",
            "M0487-C05-GOLDBACH-TM-BINARY": "statement_mismatch_no_proof_edge",
            "M0487-C06-FOOLISHAIR-EXACT-SCAFFOLD": "conditional_architecture_only_no_proof_credit",
            "M0487-C07-OPENCODE-MIRROR": "duplicate_placeholder_surface_no_proof_edge",
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "analytic_package_status": "M4_open_no_Lean_proof_body",
            "finite_package_status": "M4_open_no_admitted_data_certificate_or_checker",
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. Both deep proof branches, source admission, certificate replay, H0, R0, accepted proof state, validation, release, and theorem completion remain open.",
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    requires = proof_children
    proof: list[dict] = []
    for parent, children in requires.items():
        for child in children:
            requirement = f"REQ-{parent}-{child}"
            composition = f"CMP-{child}-{parent}"
            proof.extend(
                [
                    edge(requirement, parent, "proof_requires", child, composition),
                    edge(composition, child, "composes", parent, requirement),
                ]
            )

    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
            edge("REF-ROOT-DOMAIN", oid("ROOT"), "transports", oid("S-DOMAIN")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-EQUALITY", oid("ROOT"), "transports", oid("S-TRANSPORT")),
            edge("REF-ROOT-CUTOFF", oid("ROOT"), "logical_decomposition", oid("B-RANGE-SPLIT")),
            edge("REF-ANALYTIC-REP", oid("T-ANALYTIC"), "transports", oid("N-REPRESENTATION")),
            edge("REF-FINITE-REP", oid("T-FINITE-UPPER"), "transports", oid("N-REPRESENTATION")),
        ],
        "provenance": [
            edge("SRC-MAIN-ROOT", oid("X-SOURCE-MAIN"), "source_map", oid("ROOT")),
            edge("SRC-MAIN-ANALYTIC", oid("X-SOURCE-MAIN"), "source_map", oid("T-ANALYTIC")),
            edge("SRC-MAIN-FOURIER", oid("X-SOURCE-MAIN"), "source_map", oid("N-WEIGHTED-FOURIER")),
            edge("SRC-MAIN-DOMINANCE", oid("X-SOURCE-MAIN"), "source_map", oid("L-ANALYTIC-DOMINANCE")),
            edge("SRC-MAJOR-CHARACTERS", oid("X-SOURCE-MAJOR"), "source_map", oid("L-MAJOR-CHARACTERS")),
            edge("SRC-MAJOR-MAIN", oid("X-SOURCE-MAJOR"), "source_map", oid("L-MAJOR-MAIN")),
            edge("SRC-MAJOR-ERROR", oid("X-SOURCE-MAJOR"), "source_map", oid("L-MAJOR-ERROR")),
            edge("SRC-MINOR-EXP", oid("X-SOURCE-MINOR"), "source_map", oid("L-MINOR-EXP-SUM")),
            edge("SRC-MINOR-SIEVE", oid("X-SOURCE-MINOR"), "source_map", oid("L-LARGE-SIEVE")),
            edge("SRC-MINOR-TOTAL", oid("X-SOURCE-MINOR"), "source_map", oid("L-MINOR-TOTAL")),
            edge("SRC-PRIME-BOUNDS", oid("X-SOURCE-PRIME-BOUNDS"), "source_map", oid("L-PRIME-POWER-ERROR")),
            edge("SRC-FINITE", oid("X-SOURCE-FINITE"), "source_map", oid("T-FINITE-UPPER")),
            edge("SRC-FINITE-REDUCTION", oid("X-SOURCE-FINITE"), "source_map", oid("L-FINITE-REDUCTION")),
            edge("SRC-FINITE-BINARY", oid("X-SOURCE-FINITE"), "source_map", oid("L-BINARY-GOLDBACH-FINITE")),
            edge("PROV-ANALYTIC", oid("X-PROVENANCE"), "provenance_of", oid("T-ANALYTIC")),
            edge("PROV-FINITE", oid("X-PROVENANCE"), "provenance_of", oid("T-FINITE-UPPER")),
            edge("PROV-REJECTED", oid("X-PROVENANCE"), "provenance_of", oid("X-REJECTED-CANDIDATES")),
        ],
        "evidence": [
            edge("EVID-ROOT", oid("X-EVIDENCE"), "evidence_for", oid("ROOT")),
            edge("EVID-ANALYTIC", oid("X-EVIDENCE"), "evidence_for", oid("T-ANALYTIC")),
            edge("EVID-FINITE", oid("X-EVIDENCE"), "evidence_for", oid("T-FINITE-UPPER")),
            edge("EVID-COMPUTATION", oid("X-COMPUTATION"), "evidence_for", oid("L-FINITE-CHECKER-SOUND")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-ANALYTIC", oid("T-ANALYTIC"), "trusts", oid("X-TRUST")),
            edge("TRUST-FINITE", oid("T-FINITE-UPPER"), "trusts", oid("X-TRUST")),
            edge("TRUST-COMPUTATION", oid("T-FINITE-UPPER"), "trusts", oid("X-COMPUTATION")),
        ],
        "documentation": [
            edge(f"DOC-{identifier}", oid("X-READABLE"), "documents", identifier)
            for identifier in ids if identifier != oid("X-READABLE")
        ],
        "workflow": [
            edge("FLOW-PROOF", oid("X-WORKFLOW"), "workflow_depends_on", oid("T-ASSEMBLE")),
            edge("FLOW-SOURCE-MAIN", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE-MAIN")),
            edge("FLOW-SOURCE-MAJOR", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE-MAJOR")),
            edge("FLOW-SOURCE-MINOR", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE-MINOR")),
            edge("FLOW-SOURCE-PRIME", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE-PRIME-BOUNDS")),
            edge("FLOW-SOURCE-FINITE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE-FINITE")),
            edge("FLOW-COMPUTATION", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-COMPUTATION")),
            edge("FLOW-EVIDENCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-EVIDENCE")),
            edge("FLOW-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
        ],
    }
    for identifier in ids:
        if identifier != oid("X-EVIDENCE") and not any(
            row["to"] == identifier for row in graph_edges["evidence"]
        ):
            graph_edges["evidence"].append(
                edge(f"EVID-{identifier}", oid("X-EVIDENCE"), "evidence_for", identifier)
            )
        if identifier not in {oid("X-PROVENANCE"), oid("X-EVIDENCE")} and not any(
            row["to"] == identifier for row in graph_edges["provenance"]
        ):
            graph_edges["provenance"].append(
                edge(f"PROV-{identifier}", oid("X-PROVENANCE"), "provenance_of", identifier)
            )
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for row in graph_edges[name]:
            outgoing[row["from"]].append(row["edge_id"])
            incoming[row["to"]].append(row["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    reachable = set()
    stack = [oid("ROOT")]
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        stack.extend(requires.get(current, []))

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0487-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": f"{THEOREM}-ROOT",
        "root_obligation_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "proof_reachable_obligations": sorted(reachable),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "minimal_open_proof_cut_sets": [
                [oid("T-ANALYTIC"), oid("T-FINITE-UPPER")],
            ],
            "open_release_gates": [
                oid("X-SOURCE-MAIN"), oid("X-SOURCE-MAJOR"), oid("X-SOURCE-MINOR"),
                oid("X-SOURCE-PRIME-BOUNDS"), oid("X-SOURCE-FINITE"),
                oid("S-FOUNDATION"), oid("X-COMPUTATION"), oid("X-EVIDENCE"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff",
                "Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases",
                "Stage1Instances.THM_M_0487.ObligationTree.finiteRange_of_publishedFiniteUpper",
                "Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite",
                "Stage1Instances.THM_M_0487.ObligationTree.root_iff_analytic_and_finite",
            ],
            "reason": "Only statement transports, exact arithmetic endpoints, and conditional compositions elaborate. Both deep mathematical branches and all release overlays remain open and unaccepted.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [],
    }
    declaration_map = {
        oid("S-DOMAIN"): ["Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_integerWeakGoldbachTarget"],
        oid("S-TRANSPORT"): ["Stage1Instances.THM_M_0487.weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget"],
        oid("N-REPRESENTATION"): ["Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff"],
        oid("B-RANGE-SPLIT"): ["Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases"],
        oid("S-INTERFACE"): ["Stage1Instances.THM_M_0487.WeakGoldbachTarget"],
        oid("S-BOUNDARY"): [
            "Stage1Instances.THM_M_0487.five_excluded",
            "Stage1Instances.THM_M_0487.five_not_three_prime_sum",
            "Stage1Instances.THM_M_0487.mutationIncludedFiveBoundary_is_false",
            "Stage1Instances.THM_M_0487.mutationChangedDomainToFinEight_is_true",
            "Stage1Instances.THM_M_0487.seven_included",
            "Stage1Instances.THM_M_0487.seven_repeated_prime_representation",
            "Stage1Instances.THM_M_0487.eight_not_odd",
        ],
        oid("N-CUTOFF"): [
            "Stage1Instances.THM_M_0487.ObligationTree.analyticCutoff",
            "Stage1Instances.THM_M_0487.ObligationTree.publishedFiniteUpper",
            "Stage1Instances.THM_M_0487.ObligationTree.five_lt_analyticCutoff",
            "Stage1Instances.THM_M_0487.ObligationTree.analyticCutoff_le_publishedFiniteUpper",
        ],
        oid("N-FINITE-COVERAGE"): [
            "Stage1Instances.THM_M_0487.ObligationTree.finiteCoverage_of_publishedUpper"
        ],
        oid("T-FINITE"): ["Stage1Instances.THM_M_0487.ObligationTree.finiteRange_of_publishedFiniteUpper"],
        oid("T-ASSEMBLE"): ["Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite"],
    }
    for identifier in ids:
        recipes["recipes"].append(
            {
                "recipe_id": f"VAL-{identifier}",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0487/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0487 obligation tree",
                    },
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": (
                            "structural registry/graph presence only; no M/H/R closure credit"
                            if identifier not in CHECKED_INTERFACES
                            else "checker replays pinned Lean declarations listed in covered_declarations; provisional M0-L interface only"
                        ),
                    },
                ],
                "covered_obligation_ids": [identifier],
                "covered_declarations": declaration_map.get(identifier, []),
            }
        )
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
