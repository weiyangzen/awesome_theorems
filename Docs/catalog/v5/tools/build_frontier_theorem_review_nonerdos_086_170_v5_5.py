#!/usr/bin/env python3
"""Build the human-evidence review ledger for frontier ranks 86--170.

The output is review eligibility only.  It does not edit release 5.4, allocate
claim IDs, grant release credit, or grant new-theorem credit.
"""

from __future__ import annotations

import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
RELEASE = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
SOURCE = ROOT / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
OUT_DIR = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"
LEDGER = OUT_DIR / "nonerdos_086_170.jsonl"
SUMMARY = OUT_DIR / "nonerdos_086_170.summary.json"
CHECKER = ROOT / "Docs/catalog/v5/tools/check_frontier_theorem_review_nonerdos_086_170_v5_5.py"
FIRST = 86
LAST = 170
AS_OF = "2026-08-10"

QUEUE_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
QUEUE_AUTHORITY = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
RELEASE_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
SOURCE_SHA = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


def cb(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def spec(kind: str, identifier: str, title: str, year: str, url: str | None = None,
         version: str | None = None) -> tuple[str, str, str, str, str | None, str | None]:
    return kind, identifier, title, year, url, version


def make_ref(value: tuple[str, str, str, str, str | None, str | None], note: str) -> dict:
    kind, identifier, title, year, url, version = value
    if url is None:
        if kind == "doi":
            url = "https://doi.org/" + identifier
        elif kind == "arxiv":
            url = "https://arxiv.org/abs/" + identifier.removeprefix("arXiv:")
        else:
            raise AssertionError((kind, identifier))
    return {
        "kind": kind,
        "identifier": identifier,
        "url": url,
        "title": title,
        "version": version,
        "published_at": year,
        "updated_at": None,
        "artifact_path": None,
        "artifact_sha256": None,
        "verification": note,
    }


# Primary proof/resolution locators.  A reference on a pending/rejected row is
# useful provenance; it does not by itself make that row eligible.
REF_SPECS = {
    87: [spec("doi", "10.1017/FMP.2024.27", "Partition regularity of Pythagorean pairs", "2025")],
    88: [spec("doi", "10.1007/S00605-003-0199-Y", "Problemes diophantiens simultanes", "2004")],
    89: [spec("doi", "10.1007/BF01389798", "Invariant rational functions and a problem of Steenrod", "1969")],
    90: [spec("git_commit", "google-deepmind/formal-conjectures@9c7f21e7d4445637538bc1817b058b9b3f31bd2b", "Formal proof of the A357513 supercongruence", "2026", "https://github.com/google-deepmind/formal-conjectures/blob/9c7f21e7d4445637538bc1817b058b9b3f31bd2b/FormalConjectures/OEIS/357513.lean#L228-L258", "9c7f21e7d4445637538bc1817b058b9b3f31bd2b")],
    91: [spec("doi", "10.1016/J.EJC.2013.05.027", "Roth-type theorems in finite groups", "2013")],
    92: [spec("doi", "10.1216/RMJ-1984-14-4-983", "On the Pierce-Birkhoff conjecture", "1984")],
    93: [spec("doi", "10.1216/RMJ-1984-14-4-983", "On the Pierce-Birkhoff conjecture", "1984")],
    94: [spec("arxiv", "arXiv:2307.08725", "Real exponential sums over primes and prime gaps", "2023", version="v4")],
    95: [spec("doi", "10.1090/S0025-5718-1988-0930224-9", "On A^4+B^4+C^4=D^4", "1988")],
    96: [spec("doi", "10.1090/S0025-5718-1967-0220669-3", "A counterexample to Euler's sum of powers conjecture", "1967")],
    97: [spec("arxiv", "arXiv:2307.08725", "Real exponential sums over primes and prime gaps", "2023", version="v4")],
    98: [spec("arxiv", "arXiv:2307.08725", "Real exponential sums over primes and prime gaps", "2023", version="v4")],
    99: [
        spec("arxiv", "arXiv:2102.11818", "A counterexample to the unit conjecture for group rings", "2021"),
        spec("arxiv", "arXiv:2106.02147", "Counterexamples to the unit conjecture for group rings", "2021"),
        spec("arxiv", "arXiv:2312.05240", "The Kaplansky unit conjecture in arbitrary characteristic", "2023"),
    ],
    100: [spec("arxiv", "arXiv:2307.08725", "Real exponential sums over primes and prime gaps", "2023", version="v4")],
    101: [spec("arxiv", "arXiv:2302.05537", "Strong Bounds for 3-Progressions", "2023", version="v6")],
    102: [spec("arxiv", "arXiv:2510.01300", "The Permanent Rank of a Matrix (Part Three): Note on the Additive Basis Conjecture", "2025", version="v2")],
    103: [spec("doi", "10.1016/S0021-9800(69)80024-4", "A remark on B4-Sequences", "1969")],
    104: [spec("doi", "10.4007/ANNALS.2003.157.689", "New upper bounds on sphere packings I", "2003")],
    105: [spec("doi", "10.1002/(SICI)1098-2418(199807)12:4<351::AID-RSA3>3.0.CO;2-S", "Balancing vectors and Gaussian measures of n-dimensional convex bodies", "1998")],
    106: [spec("doi", "10.1016/0166-218X(81)90022-6", "Integer-making theorems", "1981")],
    108: [spec("arxiv", "arXiv:math/0104012", "Perfect numbers and groups", "2001")],
    109: [spec("arxiv", "arXiv:2607.09558", "Solving the Reachability Problem for Branching Vector Addition Systems via Semilinear Inductive Invariants", "2026", version="v1")],
    111: [spec("arxiv", "arXiv:1901.06542", "An improved upper bound for the length of the shortest reset words", "2019")],
    113: [spec("doi", "10.1090/S0002-9947-1985-0784009-0", "Six standard deviations suffice", "1985")],
    114: [spec("doi", "10.1016/S0764-4442(00)01624-4", "La fonction zeta de Riemann prend une infinite de valeurs irrationnelles aux entiers impairs", "2000")],
    115: [
        spec("doi", "10.1090/S0025-5718-2012-02563-4", "Odd perfect numbers are greater than 10^1500", "2012"),
        spec("doi", "10.1090/S0025-5718-2013-02776-7", "On the number of prime factors of an odd perfect number", "2013"),
    ],
    116: [spec("doi", "10.1090/S0002-9904-1974-13434-8", "On the incompatibility of two conjectures concerning primes", "1974")],
    117: [spec("doi", "10.1070/RM2001V056N04ABEH000427", "One of the numbers zeta(5), zeta(7), zeta(9), zeta(11) is irrational", "2001")],
    118: [spec("arxiv", "arXiv:math/0104012", "Perfect numbers and groups", "2001")],
    120: [spec("doi", "10.1103/PHYSREVA.69.052330", "Multipartite entanglement, quantum-error-correcting codes, and entangling power of quantum evolutions", "2004")],
    121: [spec("doi", "10.1103/PHYSREVA.69.052330", "Multipartite entanglement, quantum-error-correcting codes, and entangling power of quantum evolutions", "2004")],
    122: [spec("journal_article", "JIS-8-A101", "Determining Mills' Constant and a Note on Honaker's Problem", "2005", "https://cs.uwaterloo.ca/journals/JIS/VOL8/Caldwell/caldwell78.html")],
    123: [spec("doi", "10.2307/1969795", "Groups Without Small Subgroups", "1952")],
    124: [spec("doi", "10.1090/SURV/019", "Contributions to the Theory of Transcendental Numbers", "1984")],
    125: [spec("doi", "10.1090/SURV/019", "Contributions to the Theory of Transcendental Numbers", "1984")],
    126: [spec("doi", "10.1090/S0002-9904-1947-08849-2", "A prime-representing function", "1947")],
    128: [spec("arxiv", "arXiv:2001.02665", "A proof of Ringel's Conjecture", "2020", version="v2")],
    129: [spec("source_paper", "SA22-Conjecture-3.4", "Source paper containing Conjecture 3.4 for A358684", "2022", "https://oeis.org/A358684")],
    130: [spec("arxiv", "arXiv:2001.02665", "A proof of Ringel's Conjecture", "2020", version="v2")],
    132: [spec("arxiv", "arXiv:2504.17644", "Bounded diagonal orbits in homogeneous spaces over function fields", "2025", version="v3")],
    133: [spec("doi", "10.4310/ACTA.2022.V229.N2.A3", "Sendov's conjecture for sufficiently-high-degree polynomials", "2022")],
    134: [spec("doi", "10.1006/JMAA.1999.6267", "On Sendov's conjecture for polynomials of degree at most eight", "1999")],
    135: [spec("mathoverflow", "MathOverflow:486451", "Unique left and right maximal ideals in a semiring", "2025", "https://mathoverflow.net/questions/486451")],
    136: [spec("doi", "10.1137/20M1335030", "A Large Gap in a Dilate of a Set", "2020")],
    137: [spec("doi", "10.4007/ANNALS.2017.185.3.10", "Monochromatic sums and products in N", "2017")],
    138: [spec("doi", "10.1007/978-3-642-61324-1_4", "On a Conjecture of Roth and Some Related Problems I", "1989")],
    139: [spec("doi", "10.1016/J.JSC.2025.102421", "Wilf-Zeilberger seeds and non-trivial hypergeometric identities", "2025")],
    140: [
        spec("doi", "10.1215/IJM/1256047933", "On the density of sequence n_k xi", "1979"),
        spec("doi", "10.1007/BF01898138", "Numbers contravening a condition in density modulo 1", "1980"),
    ],
    142: [spec("arxiv", "arXiv:1312.7748", "The ternary Goldbach conjecture is true", "2013")],
    143: [spec("doi", "10.1006/JCTA.1997.2715", "Large Product-Free Subsets of Finite Groups", "1997")],
    145: [spec("doi", "10.1112/BLMS/27.6.513", "On the Equations z^m=F(x,y) and Ax^p+By^q=Cz^r", "1995")],
    146: [spec("doi", "10.1006/JABR.2000.8451", "Polynomial rings over nil rings need not be nil", "2000")],
    147: [
        spec("arxiv", "arXiv:2602.20143", "An isoperimetric inequality for word overlap", "2026", version="v1"),
        spec("git_commit", "google-deepmind/formal-conjectures@102e47fee802d461946e3a4e0b47fdbe7db4c1ed", "Formal proof of the weaker suffix-prefix avoidance bound", "2026", "https://github.com/google-deepmind/formal-conjectures/blob/102e47fee802d461946e3a4e0b47fdbe7db4c1ed/FormalConjectures/Other/SuffixPrefixAvoidance.lean#L157", "102e47fee802d461946e3a4e0b47fdbe7db4c1ed")],
    148: [spec("doi", "10.1007/978-3-642-61324-1_4", "On a Conjecture of Roth and Some Related Problems I", "1989")],
    149: [spec("arxiv", "arXiv:2303.01089", "Around Furstenberg's times p, times q conjecture", "2023")],
    151: [spec("doi", "10.1006/AIMA.1994.1068", "Density modulo 1 of Dilations of Sublacunary Sequences", "1994")],
    152: [spec("arxiv", "arXiv:2607.05349", "The microscopic weighting on a metric space", "2026", version="v1")],
    153: [spec("doi", "10.1307/MMJ/1028999653", "A complete determination of the complex quadratic fields of class-number one", "1967")],
    155: [spec("doi", "10.1112/S0025579300005313", "On the large sieve", "1965")],
    156: [spec("arxiv", "arXiv:2602.05192", "First Proof", "2026", version="v2")],
    158: [
        spec("doi", "10.1090/S0002-9939-05-07874-3", "Fuglede's conjecture fails in dimension 4", "2005"),
        spec("doi", "10.1007/S00041-005-5069-7", "On Fuglede's Conjecture and the Existence of Universal Spectra", "2006"),
    ],
    159: [spec("arxiv", "arXiv:2602.05192", "First Proof", "2026", version="v2")],
    160: [spec("doi", "10.1007/BF01389798", "Invariant rational functions and a problem of Steenrod", "1969")],
    161: [spec("doi", "10.1017/S0963548307008474", "Thresholds and Expectation Thresholds", "2007")],
    162: [spec("doi", "10.1007/BF01443605", "Ueber die Darstellung definiter Formen als Summe von Formenquadraten", "1888")],
    163: [spec("survey", "Wanless-2011-Theorem-7.2", "Transversals in Latin Squares: A Survey", "2011", "https://users.monash.edu.au/~iwanless/papers/transurveyBCC.pdf")],
    164: [spec("arxiv", "arXiv:2510.17744", "Quantitative pyjama", "2025", version="v1")],
    165: [spec("doi", "10.1515/CRLL.2004.048", "Primary cyclotomic units and a proof of Catalan's conjecture", "2004")],
    166: [spec("doi", "10.1109/TIT.1979.1055985", "On the Shannon capacity of a graph", "1979")],
    167: [spec("doi", "10.1017/S0963548307008826", "Quasirandom Groups", "2008")],
}


ELIGIBLE = {
    87: "The primary paper proves the finite-colouring Pythagorean-pair statement with the same positive-integer and same-colour scope.",
    88: "de Mathan and Teulie prove the p-adic Littlewood conjecture for real quadratic irrationals, matching this fixed quadratic specialization.",
    90: "The source annotation points to an immutable later commit whose theorem has a complete proof body and no sorry, axiom, or admit; it proves the exact A357513 congruence.",
    91: "The cited primary finite-group Roth theorem gives the BMZ-corner density lower bound with the same asymptotic quantifiers.",
    92: "Mahe's primary paper establishes the one-dimensional Pierce-Birkhoff representation; the catalog hypothesis is a restricted semialgebraic piecewise-polynomial scope.",
    93: "Mahe's primary paper proves the Pierce-Birkhoff conjecture in two variables with the same finite max-min representation.",
    95: "Elkies supplies an explicit three-fourth-powers counterexample, exactly negating Euler's k=4 lower-number-of-summands assertion.",
    96: "Lander and Parkin supply the four-fifth-powers counterexample, exactly negating Euler's k=5 assertion.",
    99: "The fixed sequence of primary counterexample papers covers characteristic zero and every prime characteristic, matching the candidate's characteristic split.",
    101: "Kelley and Meka's stronger subexponential-density bound implies r_3(N)=O(N(log N)^-10), so the stale Bloom-Sisask citation does not limit the proved scope.",
    102: "Yu proves that the union of any four bases over F_3 is an additive basis, which is exactly the sum-of-four-cubes formulation. This stronger rank is the canonical representative; rank 191's 100-cube consequence must not receive a second integrated credit.",
    103: "Lindstrom's primary B4-sequence construction gives the stated square-root plus fourth-root asymptotic upper bound.",
    104: "The Cohn-Elkies primary theorem includes the exact one-dimensional optimality statement and normalization used here.",
    106: "The Beck-Fiala paper proves discrepancy at most 2t-1 for degree-t set systems, matching all hypotheses and constants.",
    108: "Leinster's theorem gives the exact dihedral-group equivalence with odd perfect numbers.",
    111: "Shitov's primary result gives the displayed uniform cubic leading constant and lower-order term for synchronizing automata.",
    113: "Spencer's primary theorem is exactly the six-standard-deviations discrepancy bound for n sets on n points.",
    114: "Rivoal proves that infinitely many odd positive-integer zeta values are irrational, matching the infinite-set claim.",
    115: "The two primary papers independently supply the 10^1500 size bound and the at-least-101 prime-factors-with-multiplicity bound combined by this row.",
    116: "Richards proves the incompatibility implication between the first and second Hardy-Littlewood conjectures represented here.",
    117: "Zudilin proves that at least one of zeta(5), zeta(7), zeta(9), and zeta(11) is irrational.",
    118: "Leinster's Theorem 2.1 gives the exact classification of finite abelian Leinster groups as cyclic groups of perfect order.",
    120: "Scott's primary construction/classification records existence of an AME(5,2) state with the same subsystem condition encoded by ExistsAME.",
    121: "Scott's primary construction/classification records existence of an AME(6,2) state with the same subsystem condition encoded by ExistsAME.",
    122: "Caldwell and Cheng rigorously enclose the minimal Mills constant under RH inside the exact decimal interval used by the candidate.",
    123: "Gleason's no-small-subgroups theorem is a primary component of the Gleason-Montgomery-Zippin solution and matches the locally Euclidean topological-group conclusion.",
    124: "Chudnovsky's primary monograph proves transcendence of Gamma(1/4).",
    125: "Chudnovsky's primary monograph proves transcendence of Gamma(1/6).",
    126: "Mills proves existence of A>1 whose floor(A^(3^n)) is prime for every nonnegative n.",
    128: "Montgomery-Pokrovskiy-Sudakov Theorem 2.1 proves the cyclic Kotzig decomposition for every sufficiently large tree size.",
    130: "The same primary paper states Ringel's sufficiently-large theorem as Theorem 1.2; it is a distinct non-cyclic consequence of the stronger Kotzig result.",
    132: "Huang and Shi's Theorem 1.2 has the same four characteristics, SL4 function-field quotient, compact orbit closure, and nonclosed orbit.",
    133: "Tao proves Sendov's conjecture for all sufficiently large degrees, exactly the eventual statement in this row.",
    137: "Moreira's Corollary 1.5 supplies infinitely many monochromatic triples x, xy, x+y under every finite colouring.",
    138: "Erdos-Sarkozy-Sos construct counterexamples at order N/log N; the Theta formulation excludes the unrelated singleton degeneracy and matches that result.",
    139: "Au's published Wilf-Zeilberger proof evaluates exactly the displayed Gourevitch-Guillera series as 32/pi^3.",
    140: "Pollington and de Mathan prove that the nondense exceptional set for every positive lacunary sequence has full Hausdorff dimension.",
    142: "Helfgott's complete primary proof establishes the weak ternary Goldbach theorem for every odd integer greater than five.",
    143: "Kedlaya proves the n^(11/14) product-free lower bound for every finite nontrivial group.",
    145: "Darmon and Granville prove finiteness for each fixed generalized Fermat signature with reciprocal sum below one, matching the pairwise-coprime positive triples.",
    147: "Zakharov's primary inequality implies this weaker 1/n bound, and the immutable linked Lean commit contains a complete proof of the exact candidate statement.",
    148: "The Erdos-Sarkozy-Sos lower regime yields the little-o(log log N) formulation with the catalog's valid-partition guard.",
    149: "The primary paper constructs a counterexample to Conjecture 1.4, exactly negating the universal weak-star convergence proposition.",
    151: "Boshernitzan proves Hausdorff dimension zero for nondense dilations of positive unbounded sublacunary sequences.",
    153: "Stark's complete class-number-one determination gives exactly the nine negative squarefree radicands in the candidate set equality.",
    155: "Bombieri's large-sieve theorem yields every fixed exponent theta<1/2 and arbitrary logarithmic saving in the candidate's prime-progressions error normalization.",
    158: "The primary counterexample papers disprove the universal Fuglede equivalence in dimension at least three; product lifting preserves the negative general answer.",
    161: "Kahn and Kalai prove the n^epsilon expectation-threshold comparison represented by this weak threshold statement.",
    162: "Hilbert's 1888 classification is exactly the one-variable, binary-form, quadratic-form, and ternary-quartic list encoded by n and half-degree d.",
    164: "Kravitz and Leng provide the first quantitative triple-exponential pyjama bound with the same small-epsilon quantifiers.",
    165: "Mihailescu's primary proof of Catalan's conjecture leaves exactly 3^2-2^3=1 under the candidate's positive-base and exponent hypotheses.",
    166: "Lovasz's Corollary 5 gives the exact theta-function constant 7 cos(pi/7)/(1+cos(pi/7)) and hence the eventual epsilon upper bound.",
    167: "Gowers proves the n^(8/9) product-free upper bound for SL_2(F_p) represented by the candidate.",
}


PENDING = {
    94: "Ferreira arXiv:2307.08725v4 asserts the required exceptionally short prime intervals, but this simultaneous Oppermann-scale consequence has not passed an independent proof/status check.",
    97: "The claimed eventual Andrica theorem depends on the same unusually strong Ferreira preprint and remains uncorroborated by an independent accepted source.",
    98: "The claimed eventual Brocard theorem depends on the same unusually strong Ferreira preprint and remains uncorroborated by an independent accepted source.",
    100: "The claimed eventual Legendre theorem depends on the same unusually strong Ferreira preprint and remains uncorroborated by an independent accepted source.",
    107: "The jump from the published size-46 verification and the 12-element computation to every family of size at most 50 was not bound to one exact primary proof or certificate.",
    109: "The 2026 BVAS preprint states the general decidability result, but its proof and exact encoding have not yet received an independent verification sufficient for this gate.",
    112: "The source provides a journal locator but no fixed exhaustive certificate or primary text confirming the exact universe-cardinality-at-most-12 formulation.",
    135: "The MathOverflow construction is stable, but the available experimental/formal link is not immutable and was not matched to this exact unique-left/unique-right-maximal proposition.",
    141: "Giuga's historical paper was not fixed and translated far enough to verify the exact strong-Giuga, Carmichael, and rational-sum equivalence.",
    152: "The very recent microscopic-weighting preprint states this implication, but a fixed theorem-level proof artifact and independent scope check are still missing.",
    156: "The First Proof paper publishes only the question; the claimed Lean answer is a mutable main-branch link, not a fixed independently replayed resolution artifact.",
    163: "Wanless is a survey source; the exact upper constant, lower construction, and definition of T(n) were not traced to and matched against their primary proofs.",
}


REJECT = {
    86: ("scope_missing_constant_factor", "The natural theorem has an additional factor 1/sqrt(1+sqrt(3)); the formal inequality omits it and is strictly stronger than the cited result."),
    89: ("scope_definition_mismatch", "Swan's C_47 counterexample concerns a specified permutation action and invariant field; the catalog's HasNoetherProperty quantifies over every finite automorphism subgroup and leaves G unused."),
    105: ("scope_parameter_mismatch", "Banaszczyk's cube/Gaussian argument has logarithmic dependence on the ambient coordinate dimension; the formal row uses the number n of vectors instead of dimension m without a verified reduction."),
    110: ("insufficient_frontier_provenance", "The classical Schur statement is supported here only by secondary MathOverflow/StackExchange pages; no fixed primary 1924 theorem was bound, and it is not a resolution event of the surrounding open problem."),
    119: ("not_frontier_result", "Eisenstein's bounded-denominator implication is classical context for the still-open Lam-Litt conjecture, not its resolution or a separately documented frontier result in this queue."),
    127: ("not_frontier_result", "The random-colouring Chernoff estimate is an elementary benchmark explicitly included only for comparison with Spencer's frontier theorem."),
    129: ("source_still_conjectural", "The cited source explicitly labels this exact inequality Conjecture 3.4 and supplies no proof or resolution."),
    131: ("source_still_conjectural", "Green's survey says the answer is probably no; a guess is not a proof of the formal negative answer."),
    134: ("scope_degree_overreach", "Brown-Xiang prove Sendov through degree eight, while the formal interval includes degree nine; the cited source does not prove the full row."),
    136: ("semantic_duplicate_direct_corollary", "This floor(sqrt(p))-size row is a direct specialization of Shakan's general gap theorem at supplemental candidate rank 329; the stronger general statement is the canonical resolution representative."),
    144: ("not_frontier_result", "For squares and -1 the density-zero half is the elementary obstruction side of Artin's formulation, not a resolution of the open nonsquare case."),
    146: ("polarity_contradiction", "The natural text correctly says Amitsur's nil-polynomial-ring conjecture is false, while the formal proposition asserts it positively for every nil ideal."),
    150: ("unsupported_source_assertion", "The row says only 'Tom Sanders finite field variant' and gives neither a primary proof paper nor a verifiable proof artifact for the exact constant 100."),
    154: ("not_frontier_result", "The classical alpha=1 Voronovskaja formula is background for the source's unresolved alpha-not-equal-one problem, not its resolution."),
    157: ("not_frontier_result", "The exact floor-series identity is a classical counting formula and is not documented as a frontier or open-problem resolution."),
    159: ("semantic_duplicate", "The degree-two FourProp row is a direct specialization of the already represented general First Proof theorem at candidate rank 11 and cannot receive separate frontier credit."),
    160: ("scope_definition_mismatch", "The universal HasNoetherProperty proposition is not the classical Noether problem for a specified finite group permutation action; G is unused and the negative wrapper does not repair that mismatch."),
    168: ("scope_missing_additive_term", "The natural upper-bound denominator contains a final -7 term, which is absent from the formal statement; the constants therefore do not match."),
    169: ("not_frontier_result", "The source itself calls this loose rectangle-area bound an easy Cauchy-Schwarz observation; it is context for Green problem 85, not its frontier resolution."),
    170: ("scope_base_field_overreach", "Riemann existence directly realizes finite groups over an algebraically closed complex function field; the formal row asserts realizability over RatFunc K for every characteristic-zero field K."),
}


PENDING_OVERRIDES = {
    94: {"primary_reference": True, "scope_match": True},
    97: {"primary_reference": True, "scope_match": True},
    98: {"primary_reference": True, "scope_match": True},
    100: {"primary_reference": True, "scope_match": True},
    109: {"primary_reference": True, "scope_match": True},
    152: {"primary_reference": True, "scope_match": True},
}


REJECT_OVERRIDES = {
    86: {"complete_proved_statement": False, "scope_match": False, "current_proved_status": False},
    89: {"scope_match": False, "current_proved_status": False},
    105: {"scope_match": False, "current_proved_status": False},
    129: {"current_proved_status": False},
    131: {"current_proved_status": False},
    134: {"scope_match": False, "current_proved_status": False},
    136: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    146: {"scope_match": False, "current_proved_status": False},
    150: {"current_proved_status": False},
    159: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    160: {"scope_match": False, "current_proved_status": False},
    168: {"complete_proved_statement": False, "scope_match": False, "current_proved_status": False},
    170: {"scope_match": False, "current_proved_status": False},
}


def decision(rank: int) -> tuple[str, list[str], str]:
    if rank in ELIGIBLE:
        reasons = ["all_review_gates_pass"]
        if rank == 102:
            reasons.append("canonical_stronger_representative_over_candidate_rank_191")
        return "eligible_existing_frontier_credit", reasons, ELIGIBLE[rank]
    if rank in PENDING:
        return "pending", ["independent_primary_or_status_verification_pending"], PENDING[rank]
    code, note = REJECT[rank]
    return "reject", [code], note


def gate(value: bool, *evidence: str) -> dict:
    return {"pass": value, "evidence": list(evidence)}


def build_gates(candidate: dict, result: str, refs: list[dict], note: str,
                uniqueness: str) -> dict:
    rank = candidate["candidate_rank"]
    if result == "eligible_existing_frontier_credit":
        values = {name: True for name in (
            "complete_proved_statement", "primary_reference", "scope_match",
            "current_proved_status", "frontier_or_documented_resolution", "rights",
            "semantic_dedupe",
        )}
    elif result == "pending":
        values = {
            "complete_proved_statement": True,
            "primary_reference": False,
            "scope_match": False,
            "current_proved_status": False,
            "frontier_or_documented_resolution": False,
            "rights": True,
            "semantic_dedupe": True,
        }
        values.update(PENDING_OVERRIDES.get(rank, {}))
    else:
        values = {
            "complete_proved_statement": True,
            "primary_reference": bool(refs),
            "scope_match": True,
            "current_proved_status": True,
            "frontier_or_documented_resolution": False,
            "rights": True,
            "semantic_dedupe": True,
        }
        values.update(REJECT_OVERRIDES.get(rank, {}))
    ref_evidence = [f"{item['identifier']}: {item['verification']}" for item in refs]
    if not ref_evidence:
        ref_evidence = ["No exact independently verified primary resolution locator passed this review."]
    return {
        "complete_proved_statement": gate(
            values["complete_proved_statement"],
            f"Inspected frozen source block {candidate['source_member_path']}:{candidate['source_locator']['line_start']}-{candidate['source_locator']['line_end']} and formal_type_sha256={candidate['formal_type_sha256']}.",
            note,
        ),
        "primary_reference": gate(values["primary_reference"], *ref_evidence),
        "scope_match": gate(
            values["scope_match"],
            "Hypotheses, quantifiers, definitions, constants, and conclusion match the bound primary result." if values["scope_match"] else "An exact hypotheses/quantifiers/definitions/constants match was not established.",
            note,
        ),
        "current_proved_status": gate(
            values["current_proved_status"],
            f"Current proved status was independently supported as of {AS_OF}." if values["current_proved_status"] else f"Current proved status for the exact formal scope was not independently established as of {AS_OF}.",
        ),
        "frontier_or_documented_resolution": gate(
            values["frontier_or_documented_resolution"], note,
            "The pinned Formal Conjectures 'research solved' category was used only for discovery and never as independent frontier evidence.",
        ),
        "rights": gate(
            values["rights"],
            f"Pinned source archive sha256={SOURCE_SHA}; root LICENSE sha256={LICENSE_SHA}; the reviewed source file carries the Apache-2.0 header.",
            "This is a metadata-only eligibility review: attribution and locators are preserved, external paper prose is not redistributed, and no material is relicensed.",
        ),
        "semantic_dedupe": gate(values["semantic_dedupe"], uniqueness, note),
    }


def main() -> None:
    assert file_sha(QUEUE) == QUEUE_SHA
    assert file_sha(RELEASE) == RELEASE_SHA
    assert file_sha(SOURCE) == SOURCE_SHA
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert queue["authority_sha256"] == QUEUE_AUTHORITY
    selected = [row for row in queue["records"] if FIRST <= row["candidate_rank"] <= LAST]
    expected = set(range(FIRST, LAST + 1))
    assert [row["candidate_rank"] for row in selected] == list(range(FIRST, LAST + 1))
    assert set(ELIGIBLE) | set(PENDING) | set(REJECT) == expected
    assert not (set(ELIGIBLE) & set(PENDING) or set(ELIGIBLE) & set(REJECT) or set(PENDING) & set(REJECT))
    assert set(ELIGIBLE) <= set(REF_SPECS)

    normalized_counts = Counter(
        row.get("dedupe", {}).get("normalized_statement_sha256")
        for row in release["records"] if row.get("dedupe", {}).get("normalized_statement_sha256")
    )
    formal_counts = Counter(
        row.get("formal_type_sha256") for row in release["records"] if row.get("formal_type_sha256")
    )
    release_by_stage = {row["stage_claim_id"]: row for row in release["records"]}

    archive_prefix = "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669/"
    with tarfile.open(SOURCE, "r:gz") as tf:
        license_data = tf.extractfile(archive_prefix + "LICENSE").read()
        assert sha(license_data) == LICENSE_SHA
        for candidate in selected:
            member_data = tf.extractfile(archive_prefix + candidate["source_member_path"]).read()
            assert sha(member_data) == candidate["source_locator"]["file_sha256"]
            assert b"Licensed under the Apache License, Version 2.0" in member_data[:800]

    rows = []
    for candidate in selected:
        rank = candidate["candidate_rank"]
        queue_payload = {key: value for key, value in candidate.items() if key != "row_sha256"}
        assert sha(cb(queue_payload)) == candidate["row_sha256"]
        parent = release_by_stage[candidate["stage_claim_id"]]
        semantic_hash = candidate["semantic_key"].split("/", 1)[1]
        assert parent["dedupe"]["normalized_statement_sha256"] == semantic_hash
        assert parent["formal_type_sha256"] == candidate["formal_type_sha256"]
        assert normalized_counts[semantic_hash] == 1
        assert formal_counts[candidate["formal_type_sha256"]] == 1
        uniqueness = (
            f"Full release 5.4 scan (Claim_Catalog sha256={RELEASE_SHA}) found exactly one exact normalized-statement hash and one exact formal-type hash, both at {candidate['stage_claim_id']}; manual logical-subsumption review was also applied."
        )
        result, reason_codes, note = decision(rank)
        refs = [make_ref(value, note) for value in REF_SPECS.get(rank, [])]
        gates = build_gates(candidate, result, refs, note, uniqueness)
        all_pass = all(item["pass"] for item in gates.values())
        assert all_pass == (result == "eligible_existing_frontier_credit")
        credit_key = None
        if all_pass:
            payload = [sorted(item["identifier"] for item in refs), candidate["formal_type_sha256"], candidate["semantic_key"]]
            credit_key = "frontier-resolution-sha256/" + sha(cb(payload))
        row = {
            "schema_version": "awesome-theorems/frontier-theorem-human-review/5.5",
            "reviewed_as_of": AS_OF,
            "candidate_rank": rank,
            "stage_claim_id": candidate["stage_claim_id"],
            "variant_id": candidate["variant_id"],
            "family_id": candidate["family_id"],
            "display_name": candidate["display_name"],
            "queue_row_sha256": candidate["row_sha256"],
            "semantic_key": candidate["semantic_key"],
            "decision": result,
            "gates": gates,
            "primary_references": refs,
            "frontier_credit_key": credit_key,
            "reason_codes": reason_codes,
            "reviewer_notes": note,
            "grants_frontier_credit": all_pass,
            "grants_new_theorem_credit": False,
        }
        row["row_sha256"] = sha(cb(row))
        rows.append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ledger_data = b"".join(cb(row) + b"\n" for row in rows)
    LEDGER.write_bytes(ledger_data)
    counts = Counter(row["decision"] for row in rows)
    keys = [row["frontier_credit_key"] for row in rows if row["frontier_credit_key"]]
    assert len(keys) == len(set(keys))
    builder = Path(__file__).resolve()
    summary = {
        "schema_version": "awesome-theorems/frontier-theorem-human-review-summary/5.5",
        "reviewed_as_of": AS_OF,
        "scope": "non-Erdos frontier theorem candidates, inclusive ranks 86--170; human review eligibility only",
        "rank_range": {"first": FIRST, "last": LAST, "inclusive": True, "expected_rows": LAST - FIRST + 1},
        "inputs": {
            "queue_path": QUEUE.relative_to(ROOT).as_posix(),
            "queue_sha256": QUEUE_SHA,
            "queue_authority_sha256": QUEUE_AUTHORITY,
            "release_5_4_claim_catalog_path": RELEASE.relative_to(ROOT).as_posix(),
            "release_5_4_claim_catalog_sha256": RELEASE_SHA,
            "source_archive_path": SOURCE.relative_to(ROOT).as_posix(),
            "source_archive_sha256": SOURCE_SHA,
            "source_license_sha256": LICENSE_SHA,
        },
        "output": {
            "ledger_path": LEDGER.relative_to(ROOT).as_posix(),
            "ledger_sha256": sha(ledger_data),
            "ledger_bytes": len(ledger_data),
            "ledger_rows": len(rows),
        },
        "counts": {
            "eligible_existing_frontier_credit": counts["eligible_existing_frontier_credit"],
            "pending": counts["pending"],
            "reject": counts["reject"],
            "review_rows": len(rows),
            "review_eligible_frontier_keys": len(keys),
            "formal_release_frontier_credits_granted": 0,
            "new_theorem_credits_granted": 0,
        },
        "set_digests": {
            "ordered_queue_row_sha256_chain": sha(cb([row["queue_row_sha256"] for row in rows])),
            "ordered_review_row_sha256_chain": sha(cb([row["row_sha256"] for row in rows])),
            "semantic_key_set_sha256": sha(cb(sorted({row["semantic_key"] for row in rows}))),
            "frontier_credit_key_set_sha256": sha(cb(sorted(keys))),
            "eligible_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "eligible_existing_frontier_credit"))),
            "pending_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "pending"))),
            "reject_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "reject"))),
        },
        "invariants": {
            "all_seven_gates_required_for_eligibility": True,
            "source_category_signal_is_not_independent_evidence": True,
            "manual_logical_subsumption_dedupe_applied": True,
            "metadata_only_rights_review": True,
            "formal_release_modified": False,
            "review_alone_grants_release_credit": False,
            "eligible_rows_grant_new_theorem_credit": False,
        },
        "cross_batch_findings": {
            "canonical_stronger_rank": 102,
            "subsumed_candidate_rank": 191,
            "integration_requirement": "Rank 191 is the 100-cube consequence of rank 102's proved four-cube theorem and must not receive a second integrated resolution credit.",
            "shakan_canonical_general_rank": 329,
            "shakan_subsumed_primary_rank": 136,
            "shakan_integration_requirement": "Supplemental rank 329 states Shakan's general gap theorem and strictly subsumes primary rank 136's floor(sqrt(p))-size corollary; rank 136 receives no separate credit.",
        },
        "validation": {
            "builder_path": builder.relative_to(ROOT).as_posix(),
            "builder_sha256": file_sha(builder),
            "checker_path": CHECKER.relative_to(ROOT).as_posix(),
            "checker_sha256": file_sha(CHECKER),
            "status": "checker_bound; independent read-only checker required and run after generation",
        },
    }
    summary["authority_sha256"] = sha(cb(summary))
    SUMMARY.write_bytes(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")
    print(json.dumps({"rows": len(rows), "counts": summary["counts"], "ledger_sha256": summary["output"]["ledger_sha256"], "authority_sha256": summary["authority_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
