#!/usr/bin/env python3
"""Build the human evidence ledger for non-Erdos frontier ranks 171--254.

This script is deliberately range-local.  It reads the frozen 5.4 release and
the 5.5 candidate queue, and writes only this range's review ledger/summary.
It never allocates an ID and never edits a release artifact.
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
SOURCE_ARCHIVE = ROOT / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
OUT_DIR = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"
LEDGER = OUT_DIR / "nonerdos_171_254.jsonl"
SUMMARY = OUT_DIR / "nonerdos_171_254_summary.json"
CHECKER = ROOT / "Docs/catalog/v5/tools/check_frontier_theorem_review_nonerdos_171_254_v5_5.py"
TEST = ROOT / "Docs/catalog/v5/tests/test_frontier_theorem_review_nonerdos_171_254_v5_5.py"
FIRST_RANK = 171
LAST_RANK = 254
AS_OF = "2026-08-10"

QUEUE_SHA256 = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
RELEASE_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
SOURCE_ARCHIVE_SHA256 = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def ref(
    kind: str,
    identifier: str,
    url: str,
    title: str,
    *,
    version: str | None = None,
    published_at: str | None = None,
    updated_at: str | None = None,
    artifact_path: str | None = None,
    artifact_sha256: str | None = None,
    verification: str,
) -> dict:
    return {
        "kind": kind,
        "identifier": identifier,
        "url": url,
        "title": title,
        "version": version,
        "published_at": published_at,
        "updated_at": updated_at,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "verification": verification,
    }


R = {
    "gromov1981": ref("doi", "10.1007/BF02698687", "https://doi.org/10.1007/BF02698687", "Groups of polynomial growth and expanding maps (with an appendix by Jacques Tits)", published_at="1981", verification="Crossref metadata and the primary paper title were independently matched to the iff statement."),
    "exoo1989": ref("doi", "10.1002/JGT.3190130113", "https://doi.org/10.1002/jgt.3190130113", "A lower bound for R(5,5)", published_at="1989", verification="Crossref metadata matches Exoo's 42-vertex construction and the lower bound 43."),
    "microscopic2026": ref("arxiv", "arXiv:2607.05349", "https://arxiv.org/abs/2607.05349", "The microscopic weighting on a metric space", version="v1", published_at="2026-07-06", updated_at="2026-07-06", verification="The arXiv API metadata and source Theorem 3.8 were checked; the source theorem contains an additional uniqueness clause."),
    "degree1991": ref("doi", "10.1016/0012-365X(91)90269-8", "https://doi.org/10.1016/0012-365X(91)90269-8", "Degree sequences in triangle-free graphs", published_at="1991", verification="Crossref metadata matches the source authors, journal, pages, and theorem provenance."),
    "green94proof": ref("git_commit", "google-deepmind/formal-conjectures@153d79d6c82c76fe1bee860742af800840c974d9", "https://github.com/google-deepmind/formal-conjectures/blob/153d79d6c82c76fe1bee860742af800840c974d9/FormalConjectures/GreensOpenProblems/94.lean#L174", "Formal proof of the negative outer-measure answer to Green problem 94", version="153d79d6c82c76fe1bee860742af800840c974d9", published_at="2026", verification="The immutable raw GitHub file was fetched and the cited theorem block has a proof body rather than sorry."),
    "moreira2017": ref("doi", "10.4007/ANNALS.2017.185.3.10", "https://doi.org/10.4007/annals.2017.185.3.10", "Monochromatic sums and products in N", published_at="2017", verification="Crossref metadata verifies the source used only to establish well-definedness; the candidate's bound nine is elementary."),
    "gowerslong2021": ref("arxiv", "arXiv:1609.08688", "https://arxiv.org/abs/1609.08688", "The length of an s-increasing sequence of r-tuples", version="v2", published_at="2016-11-02", verification="arXiv metadata and the candidate source were checked; the natural and formal quantifiers do not agree."),
    "foxkleitman2006": ref("doi", "10.1016/J.JCTA.2005.07.004", "https://doi.org/10.1016/j.jcta.2005.07.004", "On Rado's Boundedness Conjecture", published_at="2006", verification="Crossref metadata and the primary result match the k=3 bound c<=24."),
    "polak2020": ref("arxiv", "arXiv:2005.02945", "https://arxiv.org/abs/2005.02945", "New methods in coding theory: Error-correcting codes and the Shannon capacity", published_at="2020", verification="The frozen source cites Section 9.1 of this primary thesis for the constant 367^(1/5)."),
    "knuth2026": ref("primary_manuscript", "Knuth-Claude-Cycles-2026", "https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf", "Claude's Cycles", published_at="2026", verification="The author-hosted primary manuscript and the independent Lean proof link in the source were checked for the odd-m theorem."),
    "bhargavashankar2013": ref("arxiv", "arXiv:1312.7859", "https://arxiv.org/abs/1312.7859", "The average size of the 5-Selmer group of elliptic curves is 6, and the average rank is less than 1", published_at="2013-12-30", verification="The primary preprint's numbered Theorems 4 and 5 match the two density claims."),
    "ramsey46": ref("doi", "10.1002/JGT.70029", "https://doi.org/10.1002/jgt.70029", "R(5,5) <= 46", published_at="2026", verification="Crossref and arXiv:2409.15709v2 metadata independently state the exact upper bound and duplicate computations."),
    "boxdot2016": ref("doi", "10.1002/MALQ.201600036", "https://doi.org/10.1002/malq.201600036", "Cluster expansion and the boxdot conjecture", published_at="2016", verification="The arXiv abstract explicitly says the named conjecture is confirmed; Crossref supplies the journal DOI."),
    "aubert1982": ref("doi", "10.1016/0095-8956(82)90010-7", "https://doi.org/10.1016/0095-8956(82)90010-7", "Graphes orientes indecomposables en circuits hamiltoniens", published_at="1982", verification="Crossref metadata matches the exact Aubert-Schneider reference cited for the m=2 obstruction."),
    "modularity2001": ref("doi", "10.1090/S0894-0347-01-00370-8", "https://doi.org/10.1090/S0894-0347-01-00370-8", "On the modularity of elliptic curves over Q: Wild 3-adic exercises", published_at="2001", verification="This primary completion of the modularity theorem matches the all-elliptic-curves-over-Q scope."),
    "ruzsa1991": ref("doi", "10.4064/AA-60-2-191-202", "https://doi.org/10.4064/aa-60-2-191-202", "Arithmetic progressions in sumsets", published_at="1991", verification="Crossref metadata matches the primary extremal construction cited in the source."),
    "terasoma2002": ref("doi", "10.1007/S002220200218", "https://doi.org/10.1007/s002220200218", "Mixed Tate motives and multiple zeta values", published_at="2002", verification="Crossref metadata matches one of the two independent primary proofs of the MZV dimension upper bound."),
    "delignegoncharov2005": ref("doi", "10.1016/J.ANSENS.2004.11.001", "https://doi.org/10.1016/j.ansens.2004.11.001", "Groupes fondamentaux motiviques de Tate mixte", published_at="2005", verification="Crossref metadata matches the second primary source for the MZV dimension bound."),
    "yu2025": ref("arxiv", "arXiv:2510.01300", "https://arxiv.org/abs/2510.01300", "The Permanent Rank of a Matrix (Part Three): Note on the Additive Basis Conjecture", version="v2", published_at="2025-10-01", updated_at="2026-06-10", verification="The arXiv v2 abstract proves the stronger four-basis Z_3 statement, hence the 100-cube statement."),
    "fg1989": ref("doi", "10.2307/1971450", "https://doi.org/10.2307/1971450", "Limitations to the Equi-Distribution of Primes I", published_at="1989", verification="Crossref metadata matches the primary endpoint counterexample cited by the source."),
    "banachsurvey": ref("arxiv", "arXiv:math/0110202", "https://arxiv.org/abs/math/0110202", "The Banach-Mazur rotation problem", published_at="2001", verification="The source is a survey of the still-open infinite-dimensional problem; the finite-dimensional case is not a frontier resolution."),
    "bfr2023": ref("doi", "10.1080/00029890.2023.2176667", "https://doi.org/10.1080/00029890.2023.2176667", "An Upper Bound on the Size of Sidon Sets", published_at="2023", verification="Crossref metadata and the source formula match the historical 0.998 result; the ledger does not call it the current best bound."),
    "green2002": ref("doi", "10.1007/S00039-002-8258-4", "https://doi.org/10.1007/s00039-002-8258-4", "Arithmetic progressions in sumsets", published_at="2002", verification="Crossref metadata matches the primary lower-bound paper cited by the source."),
    "artin1927": ref("doi", "10.1007/BF02952513", "https://doi.org/10.1007/bf02952513", "Uber die Zerlegung definiter Funktionen in Quadrate", published_at="1927", verification="Crossref metadata matches Artin's primary solution of Hilbert's seventeenth problem."),
    "fernandes2026": ref("arxiv", "arXiv:2605.12342", "https://arxiv.org/abs/2605.12342", "Groups of permutations that are even on maximal proper subsets, and related monoids", version="v1", published_at="2026-05-12", verification="The primary preprint/source records these low-rank exceptions, but they are boundary data rather than resolutions of Conjecture 1."),
    "bedert2023": ref("doi", "10.1007/S00493-023-00069-W", "https://doi.org/10.1007/s00493-023-00069-w", "On Unique Sums in Abelian Groups", published_at="2023", verification="Crossref metadata matches the source's Theorem 3 lower bound and historical upper bound."),
    "shapirov2012": ref("arxiv", "arXiv:1108.5348", "https://arxiv.org/abs/1108.5348", "Perfect cuboids and irreducible polynomials", published_at="2011", verification="The cited observation is conditional on three unproved cuboid conjectures and is not a resolution."),
    "green2001": ref("doi", "10.4064/AA100-4-6", "https://doi.org/10.4064/aa100-4-6", "The number of squares and B_h[g] sets", published_at="2001", verification="Crossref metadata matches the primary source for the c(2) lower bound."),
    "gk2025": ref("arxiv", "arXiv:2510.17743", "https://arxiv.org/abs/2510.17743", "No-(k+1)-in-line problem for large constant k", version="v1", published_at="2025-10-20", verification="The arXiv abstract gives the exact n>=k>=10^37 theorem; the source's strict inequality is a safe sub-scope."),
    "rupert2025": ref("arxiv", "arXiv:2508.18475", "https://arxiv.org/abs/2508.18475", "A convex polyhedron without Rupert's property", version="v2", published_at="2025-08-25", updated_at="2026-01-28", verification="The arXiv abstract explicitly constructs a non-Rupert polyhedron and disproves the 2017 conjecture."),
    "ek2007": ref("doi", "10.1112/S0010437X07002801", "https://doi.org/10.1112/s0010437x07002801", "Measure rigidity and p-adic Littlewood-type problems", published_at="2007", verification="Crossref metadata and the primary theorem match the Hausdorff-dimension-zero exceptional-set statement."),
    "gupta2014": ref("doi", "10.1016/J.AIM.2014.07.012", "https://doi.org/10.1016/j.aim.2014.07.012", "On Zariski's Cancellation Problem in positive characteristic", published_at="2014", verification="Crossref metadata matches Gupta's primary dimension-three positive-characteristic counterexample."),
    "greene_lobb2021": ref("doi", "10.4007/ANNALS.2021.194.2.4", "https://doi.org/10.4007/annals.2021.194.2.4", "The rectangular peg problem", published_at="2021", verification="The primary paper/arXiv:2005.09193 states every smooth Jordan curve realizes every rectangle similarity class."),
    "sanders2019": ref("doi", "10.4153/S0008414X1900049X", "https://doi.org/10.4153/s0008414x1900049x", "The Erdos-Moser Sum-free Set Problem", published_at="2019", verification="Crossref metadata matches the primary super-logarithmic lower-bound paper."),
    "oddmahler2004": ref("doi", "10.1112/S002460930300287X", "https://doi.org/10.1112/s002460930300287x", "The Mahler measure of polynomials with odd coefficients", published_at="2004", verification="Crossref metadata and title directly match the restricted Mahler-measure theorem."),
    "rankin1938": ref("doi", "10.1112/JLMS/S1-13.4.242", "https://doi.org/10.1112/jlms/s1-13.4.242", "The Difference between Consecutive Prime Numbers", published_at="1938", verification="Crossref metadata matches Rankin's primary covering construction underlying the stated lower bound."),
    "fgkmt2018": ref("doi", "10.1090/JAMS/876", "https://doi.org/10.1090/jams/876", "Long gaps between primes", published_at="2018", verification="The primary modern covering construction gives the one-power log-log denominator in the candidate; the source's [Ra38] label is bibliographically stale."),
    "baek2024": ref("arxiv", "arXiv:2411.19826", "https://arxiv.org/abs/2411.19826", "Optimality of Gerver's Sofa", version="v1", published_at="2024-11-29", verification="The arXiv abstract explicitly says the moving-sofa problem is resolved and Gerver's sofa is optimal."),
    "flp1995": ref("doi", "10.4064/AA-70-2-125-147", "https://doi.org/10.4064/aa-70-2-125-147", "On the range of fractional parts {xi(p/q)^n}", published_at="1995", verification="Crossref metadata matches Flatto-Lagarias-Pollington and the rational p/q Mahler 3/2 bound."),
    "cs2017": ref("doi", "10.1090/PROC/13690", "https://doi.org/10.1090/proc/13690", "On suprema of autoconvolutions with an application to Sidon sets", published_at="2017", verification="Crossref and arXiv:1403.7988 metadata match the c(infinity) lower-bound provenance."),
    "aaronson2019": ref("doi", "10.1112/BLMS.12253", "https://doi.org/10.1112/blms.12253", "Maximising the number of solutions to a linear equation in a set of integers", published_at="2019", verification="Crossref metadata and equation (1.2) in the source bind the distinct upper and lower gamma bounds."),
    "aeh1972": ref("doi", "10.1016/0021-8693(72)90134-2", "https://doi.org/10.1016/0021-8693(72)90134-2", "On the uniqueness of the coefficient ring in a polynomial ring", published_at="1972", verification="Crossref metadata matches the primary one-variable cancellation theorem."),
    "tunnell1983": ref("doi", "10.1007/BF01389327", "https://doi.org/10.1007/bf01389327", "A classical Diophantine problem and modular forms of weight 3/2", published_at="1983", verification="Crossref metadata matches Tunnell's parity-split necessary conditions for congruent numbers."),
    "deligne1974": ref("doi", "10.1007/BF02684373", "https://doi.org/10.1007/bf02684373", "La conjecture de Weil I", published_at="1974", verification="Deligne's primary Weil-conjecture proof yields the Ramanujan-Petersson bound for tau."),
    "degiorgi2011": ref("doi", "10.4007/ANNALS.2011.174.3.3", "https://doi.org/10.4007/annals.2011.174.3.3", "On De Giorgi's conjecture in dimensions 9 and higher", published_at="2011", verification="The primary paper title and theorem match failure in every dimension n>=9."),
    "eq677": ref("project_result", "equational-theories:255-not-implies-677:finite-order-3", "https://teorth.github.io/equational_theories/implications/?677&finite", "Finite three-element countermodel: Equation 255 does not imply Equation 677", published_at="2025", artifact_path="Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz", artifact_sha256=SOURCE_ARCHIVE_SHA256, verification="The frozen Lean source contains an explicit Fin 3 multiplication table and a sorry-free decidable proof; the project page supplies the stable problem identity."),
    "ruzsa2005": ref("doi", "10.1007/S11139-005-0826-4", "https://doi.org/10.1007/s11139-005-0826-4", "Sum-Avoiding Subsets", published_at="2005", verification="Crossref metadata matches the primary extremal construction for the upper bound."),
    "smyth1971": ref("doi", "10.1112/BLMS/3.2.169", "https://doi.org/10.1112/blms/3.2.169", "On the Product of the Conjugates outside the unit circle of an Algebraic Integer", published_at="1971", verification="Crossref metadata matches Smyth's sharp nonreciprocal Mahler-measure theorem."),
    "green2022": ref("doi", "10.1017/FMP.2022.12", "https://doi.org/10.1017/fmp.2022.12", "New lower bounds for van der Waerden numbers", published_at="2022", verification="Crossref metadata and the primary result establish superpolynomial growth, stronger than the quadratic negation."),
    "ttt2026": ref("arxiv", "arXiv:2601.16175", "https://arxiv.org/abs/2601.16175", "Learning to Discover at Test Time", version="v2", published_at="2026-01-23", updated_at="2026-02-05", verification="The primary manuscript explicitly certifies C1<=1.50286, which implies the catalog's rounded 1.5029 bound."),
    "mv2010": ref("arxiv", "arXiv:0907.1379", "https://arxiv.org/abs/0907.1379", "Improved bounds on the supremum of autoconvolutions", version="v2", published_at="2009-07-08", updated_at="2009-09-04", verification="The primary manuscript explicitly states 1.2748<=S and supplies the proof data."),
    "bb5coq": ref("formal_proof", "ccz181078/Coq-BB5@9142e219229baf2245d3f70851947230ea28a318", "https://github.com/ccz181078/Coq-BB5/commit/9142e219229baf2245d3f70851947230ea28a318", "Coq proof that BB(5)=47,176,870", version="9142e219229baf2245d3f70851947230ea28a318", updated_at="2025-09-20", verification="The Busy Beaver Challenge page links this fixed Coq proof repository; the exact commit and value were checked."),
    "mo75792": ref("formal_counterexample", "MathOverflow:75792;formal-conjectures@2270d31e", "https://mathoverflow.net/questions/75792", "Counterexample to complexity(5^n)=5n", published_at="2011", artifact_path="Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz", artifact_sha256=SOURCE_ARCHIVE_SHA256, verification="The archived source gives the explicit n=6 expression using 29 ones and a sorry-free Lean proof, while 5n=30."),
    "bjp2014": ref("journal_article", "Integers-14-A43", "https://math.colgate.edu/~integers/vol14.html", "On double 3-term arithmetic progressions", published_at="2014", verification="The stable journal volume/article number and source citation match the four-term-progression construction."),
    "sphere24": ref("doi", "10.4007/ANNALS.2017.185.3.8", "https://doi.org/10.4007/annals.2017.185.3.8", "The sphere packing problem in dimension 24", published_at="2017", verification="Crossref metadata matches the primary optimality proof in dimension 24."),
    "iwaniec1978": ref("doi", "10.1515/DEMA-1978-0121", "https://doi.org/10.1515/dema-1978-0121", "On the problem of Jacobsthal", published_at="1978", verification="Crossref metadata matches the primary x^2 upper-bound result."),
    "jensen1915": ref("jstor", "JSTOR:24532219", "https://www.jstor.org/stable/24532219", "Om talteoretiske Egenskaber ved de Bernoulliske Tal", published_at="1915", verification="The stable primary-paper identifier records Jensen's stronger infinitude result for irregular primes congruent to 3 mod 4."),
}


ELIGIBLE = {
    171: (["gromov1981"], "Gromov's equivalence is the named 1981 solution of the polynomial-growth classification problem."),
    172: (["exoo1989"], "Exoo's explicit construction established the frontier lower bound R(5,5)>=43."),
    177: (["green94proof"], "A fixed, independently inspected formal proof gives the negative answer to Green's outer-measure variant."),
    179: (["foxkleitman2006"], "Fox-Kleitman resolved the k=3 case of Rado's boundedness conjecture with the exact constant 24."),
    180: (["polak2020"], "The primary thesis records the then-frontier Shannon-capacity construction with constant 367^(1/5)."),
    182: (["knuth2026"], "The primary manuscript resolves the odd-m Hamiltonian arc-decomposition family and has an independent Lean implementation."),
    183: (["bhargavashankar2013"], "Theorem 4 is a major quantitative average-rank result and exactly gives the 83.75 percent density claim."),
    184: (["ramsey46"], "The primary paper proves R(5,5)<=46 and reports independent implementations of the computation."),
    185: (["boxdot2016"], "The primary paper explicitly confirms the named Boxdot Conjecture."),
    186: (["aubert1982"], "The primary paper supplies the exact m=2 obstruction complementary to the odd-m decomposition theorem."),
    187: (["modularity2001"], "The cited completion proves the full Modularity Theorem for every elliptic curve over Q."),
    188: (["ruzsa1991"], "Ruzsa's construction is the primary frontier upper example for arithmetic progressions in dense sumsets."),
    190: (["terasoma2002", "delignegoncharov2005"], "Two primary motivic proofs establish the Zagier-dimension upper bound for MZVs."),
    191: (["yu2025"], "Yu proves the stronger four-cube additive-basis theorem over F_3, resolving the catalog's 100-cube statement."),
    192: (["fg1989"], "Friedlander-Granville's primary limitation theorem disproves the endpoint theta=1 form."),
    193: (["bhargavashankar2013"], "Theorem 5 of the primary paper exactly gives the 20.62 percent rank-zero density claim."),
    195: (["bfr2023"], "This is a documented historical frontier improvement; the review does not repeat the obsolete 'current best' label."),
    197: (["green2002"], "Green's primary paper proves the stated exp(c sqrt(log N)) lower guarantee."),
    198: (["artin1927"], "Artin's 1927 paper is the primary solution to Hilbert's seventeenth problem with the same rational-function sum-of-squares scope."),
    201: (["bedert2023"], "Bedert's Theorem 3 gives the super-logarithmic lower bound with a diverging factor."),
    202: (["degree1991"], "The primary paper provides the explicit extremal graph construction establishing F(4)<=19."),
    204: (["green2001"], "Green's primary research paper establishes the exact sqrt(4/7) lower bound for c(2)."),
    205: (["gk2025"], "The primary paper resolves the no-k-in-line conjecture throughout the stated large-k range."),
    206: (["rupert2025"], "The primary counterexample disproves the 2017 universal Rupert-property conjecture."),
    207: (["ek2007"], "The primary measure-rigidity paper proves Hausdorff dimension zero for the exceptional set."),
    214: (["gupta2014"], "Gupta's primary counterexample resolves Zariski cancellation negatively in positive characteristic and dimension three."),
    215: (["greene_lobb2021"], "Greene-Lobb solve the smooth rectangular peg problem for every prescribed aspect ratio."),
    216: (["sanders2019"], "Sanders' primary paper gives the stated super-logarithmic Erdos-Moser sum-free lower bound."),
    217: (["oddmahler2004"], "The primary restricted-Mahler paper establishes the sharp golden-ratio lower bound for odd coefficients."),
    218: (["fgkmt2018"], "The Ford-Green-Konyagin-Maynard-Tao construction supplies the candidate's modern one-power log-log-denominator bound; the frozen [Ra38] label is stale."),
    220: (["baek2024"], "Baek's primary manuscript explicitly resolves the moving-sofa problem by proving Gerver's sofa optimal."),
    221: (["flp1995"], "The primary paper gives the exact rational p/q lower bound for the Mahler 3/2 orbit diameter."),
    222: (["cs2017"], "The primary autoconvolution paper establishes the stated 0.64 lower bound and documents its Sidon-set significance."),
    224: (["aaronson2019"], "The candidate is the lower half of the primary paper's explicit asymptotic gamma bounds."),
    225: (["aaronson2019"], "The candidate is the upper half of the primary paper's explicit asymptotic gamma bounds."),
    227: (["aeh1972"], "The foundational cancellation paper proves the one-variable polynomial-ring case in arbitrary characteristic."),
    228: (["tunnell1983"], "This is the even-squarefree necessary half of Tunnell's major congruent-number theorem."),
    229: (["deligne1974"], "Deligne's Weil-conjecture proof establishes the Ramanujan-Petersson bound for tau."),
    231: (["degiorgi2011"], "The primary construction gives counterexamples to De Giorgi's conclusion in every dimension n>=9."),
    232: (["tunnell1983"], "This is the odd-squarefree necessary half of Tunnell's major congruent-number theorem."),
    234: (["eq677"], "The explicit finite three-element model is a machine-checkable frontier result of the Equational Theories implication project."),
    236: (["ruzsa2005"], "Ruzsa's primary extremal construction gives the stated exponential square-root-log upper example."),
    238: (["green2022"], "Green's primary theorem proves superpolynomial growth of W(3,r), resolving every fixed-polynomial upper proposal."),
    241: (["bedert2023"], "This is the documented historical frontier upper estimate in the same primary unique-sums paper."),
    242: (["bb5coq"], "The finite five-state Busy Beaver classification is backed by a fixed machine-checked Coq proof artifact."),
    247: (["mo75792"], "The explicit n=6 construction gives complexity(5^6)<=29<30 and the archived theorem proof is sorry-free."),
    249: (["bjp2014"], "The primary article establishes the four-term-progression-free Lipschitz graph construction."),
    250: (["sphere24"], "The Annals paper resolves the sphere-packing problem in dimension 24."),
    251: (["iwaniec1978"], "Iwaniec's primary Jacobsthal paper establishes the stated quadratic upper bound."),
    253: (["jensen1915"], "Jensen's primary theorem proves the stronger infinitude of irregular primes congruent to 3 mod 4."),
}


PENDING = {
    175: "The dimensions 0--8 list is a composite of separate computational classifications; the source gives only Wikipedia and no per-dimension primary proof/certificate.",
    181: "The claim combines classical dimensions with Wang's special dimensions; no primary-source bundle was verified for the exact set-valued formulation.",
    196: "Only an OEIS page is cited; no primary proof or explicit certificate for the primitive-times-squarefree classification was located.",
    208: "A stable scan of Yakovlev's Russian paper is cited, but the exact CH, compact-Hausdorff, weak-first-countability scope was not independently translated and matched.",
    210: "The MathOverflow page is stable, but the fixed formal-proof link in the file is for a different unique-left-and-right-maximal statement, not this more-than-one-right-maximal claim.",
    211: "Only a secondary Wikipedia reference is supplied; no exact primary Riemann-existence/Galois realization statement was bound to this formal scope.",
    212: "The large-sieve special case is asserted only in Green's problem survey; an exact theorem and constants were not traced to a primary source.",
    219: "The finite verification through k=166 has no construction table, certificate, or primary computational paper in the source.",
    226: "Three sources are cited for related approximate-group results, but no single theorem was matched to the exact |S| and S^8 subset A^4 formulation.",
    233: "The available primary rectangular-peg paper treats smooth curves and prescribed ratios; a primary source for this exact arbitrary-Jordan-curve statement was not verified.",
    243: "The source gives no primary reference, witness, or proof artifact for the assertion that the 2K version is false.",
    244: "The OEIS entry asserts an existential counterexample but the catalog row carries no explicit n, proof certificate, or primary paper.",
    246: "The 1.4238 value is cited only to a secondary covering-codes book; its exact primary theorem and normalization were not verified.",
    248: "The N<=60 computation has no cited program, exhaustive certificate, or primary paper in the frozen source.",
}


REJECT = {
    173: ("scope_underformalized", "The source's Theorem 3.8 also says the microscopic weighting is the unique gauging, but the formal candidate states only an existence equivalence."),
    174: ("scope_extra_hypothesis", "The paper/docstring theorem is stated for triangle-free graphs with f=2, while the Lean candidate silently adds connectedness; exact primary scope is not represented."),
    176: ("not_frontier_result", "The lower bound nine is the immediate x,y>=3 observation; Moreira is used only for existence of N_0, so this is not a frontier resolution theorem."),
    178: ("quantifier_scope_mismatch", "The natural statement says arbitrarily large m, whereas the Lean type uses forall-eventually (all sufficiently large m), a strictly stronger quantifier."),
    189: ("not_frontier_result", "The dimension-six bounds combine a general lower construction with the universal d+1 upper bound and do not resolve the dimension-six MUB problem."),
    194: ("not_frontier_result", "The finite-dimensional invariant-inner-product argument is elementary and does not resolve the still-open infinite-dimensional Banach-Mazur rotation problem."),
    199: ("semantic_duplicate", "This no-quadratic-bound consequence is subsumed by rank 238's no-polynomial-growth theorem from the same Green paper."),
    200: ("not_frontier_result", "The cyclic rank of Gamma_(2+2) is elementary boundary data excluded from the paper's open conjecture, not a resolution of it."),
    203: ("conditional_nonresolution", "The conclusion assumes all three unproved Cuboid conjectures and therefore does not resolve existence of a perfect cuboid."),
    209: ("not_frontier_result", "The f(1)=1 Hamming-code sanity value is elementary and not a frontier/open-problem resolution."),
    213: ("not_frontier_result", "The source itself calls this O(X^(1/4)) estimate almost trivial; it is context for an open problem, not a frontier resolution."),
    223: ("not_frontier_result", "The d=2 maximum-three MUB fact is the elementary prime-power construction plus d+1 bound, not a frontier resolution."),
    230: ("not_frontier_result", "The rank-three Gamma_(3+3) exception is boundary data explicitly excluded from Conjecture 1, not a resolution of the conjecture."),
    235: ("not_frontier_result", "The accumulation-point fact has only textbook/secondary provenance and is not documented as a frontier problem resolution."),
    237: ("scope_missing_normalization", "Smyth's theorem is for the normalized irreducible nonreciprocal algebraic-integer setting; the Lean row quantifies over every integer polynomial and even admits multiplying a reciprocal polynomial by X without changing Mahler measure."),
    239: ("scope_definition_mismatch", "The primary C1 theorem assumes a supported/integrable nonnegative function and the full convolution supremum; the catalog's C1a definition omits support/integrability and changes the supremum domain."),
    240: ("scope_definition_mismatch", "The primary lower bound is for the standard supported autoconvolution constant; the catalog's C1a definition omits support/integrability and changes the supremum domain."),
    245: ("not_frontier_result", "The one-dimensional De Giorgi case is explicitly trivial and cannot receive independent frontier credit."),
    252: ("semantic_duplicate", "The same explicit Fin 3 countermodel proves rank 234's stronger finite statement; this weaker row is the identical resolution event."),
    254: ("semantic_duplicate_and_question", "The natural language remains a question and the formal answer wrapper denotes the same Gerver-sofa equality already represented by rank 220."),
}


EXTRA_REFS = {
    173: ["microscopic2026"],
    174: ["degree1991"],
    176: ["moreira2017"],
    178: ["gowerslong2021"],
    194: ["banachsurvey"],
    199: ["green2022"],
    200: ["fernandes2026"],
    203: ["shapirov2012"],
    208: [],
    230: ["fernandes2026"],
    237: ["smyth1971"],
    239: ["ttt2026"],
    240: ["mv2010"],
    252: ["eq677"],
    254: ["baek2024"],
}


GATE_SPECIAL = {
    173: {"complete_proved_statement": False, "scope_match": False, "frontier_or_documented_resolution": True},
    174: {"scope_match": False, "current_proved_status": False, "frontier_or_documented_resolution": True},
    178: {"complete_proved_statement": False, "scope_match": False, "current_proved_status": False, "frontier_or_documented_resolution": True},
    199: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    203: {"frontier_or_documented_resolution": False},
    237: {"scope_match": False, "current_proved_status": False, "frontier_or_documented_resolution": True},
    239: {"scope_match": False, "current_proved_status": False, "frontier_or_documented_resolution": True},
    240: {"scope_match": False, "current_proved_status": False, "frontier_or_documented_resolution": True},
    252: {"frontier_or_documented_resolution": True, "semantic_dedupe": False},
    254: {"complete_proved_statement": False, "scope_match": False, "frontier_or_documented_resolution": True, "semantic_dedupe": False},
}


def primary_refs_for(rank: int) -> list[dict]:
    if rank in ELIGIBLE:
        keys = ELIGIBLE[rank][0]
    else:
        keys = EXTRA_REFS.get(rank, [])
    return [R[key] for key in keys]


def decision_for(rank: int) -> tuple[str, list[str], str]:
    if rank in ELIGIBLE:
        return "eligible_existing_frontier_credit", ["all_review_gates_pass"], ELIGIBLE[rank][1]
    if rank in PENDING:
        return "pending", ["insufficient_independent_primary_evidence"], PENDING[rank]
    code, note = REJECT[rank]
    return "reject", [code], note


def gate(pass_value: bool, *evidence: str) -> dict:
    return {"pass": pass_value, "evidence": list(evidence)}


def build_gates(row: dict, decision: str, refs: list[dict], note: str, release_uniqueness: str) -> dict:
    rank = row["candidate_rank"]
    if decision == "eligible_existing_frontier_credit":
        values = {
            "complete_proved_statement": True,
            "primary_reference": True,
            "scope_match": True,
            "current_proved_status": True,
            "frontier_or_documented_resolution": True,
            "rights": True,
            "semantic_dedupe": True,
        }
    elif decision == "pending":
        values = {
            "complete_proved_statement": True,
            "primary_reference": False,
            "scope_match": False,
            "current_proved_status": False,
            "frontier_or_documented_resolution": False,
            "rights": True,
            "semantic_dedupe": True,
        }
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
    values.update(GATE_SPECIAL.get(rank, {}))
    primary_evidence = [f"{x['identifier']}: {x['verification']}" for x in refs]
    if not primary_evidence:
        primary_evidence = ["No exact primary resolution artifact with a stable identifier passed this review."]
    return {
        "complete_proved_statement": gate(
            values["complete_proved_statement"],
            f"Frozen source block {row['source_member_path']}:{row['source_locator']['line_start']}-{row['source_locator']['line_end']} and formal_type_sha256={row['formal_type_sha256']} were inspected.",
            note,
        ),
        "primary_reference": gate(values["primary_reference"], *primary_evidence),
        "scope_match": gate(
            values["scope_match"],
            ("The hypotheses, quantifiers, constants, and conclusion were matched to the primary result." if values["scope_match"] else "An exact hypotheses/quantifiers/conclusion match was not established."),
            note,
        ),
        "current_proved_status": gate(
            values["current_proved_status"],
            (f"Stable primary evidence was checked as of {AS_OF}; the claim remains a proved theorem (a superseded bound remains mathematically valid)." if values["current_proved_status"] else f"The stronger formal/current proved status was not independently established as of {AS_OF}."),
        ),
        "frontier_or_documented_resolution": gate(
            values["frontier_or_documented_resolution"],
            note,
            "The Formal Conjectures 'research solved' category was treated only as discovery evidence, never as this gate's proof.",
        ),
        "rights": gate(
            values["rights"],
            f"Pinned source archive sha256={SOURCE_ARCHIVE_SHA256}; root LICENSE sha256={LICENSE_SHA256}; the candidate file has an Apache-2.0 header.",
            "This review grants metadata-only eligibility, preserves attribution/locator, copies no external paper text, performs no relicensing, and grants no new-theorem credit.",
        ),
        "semantic_dedupe": gate(values["semantic_dedupe"], release_uniqueness, note),
    }


def main() -> None:
    assert file_sha256(QUEUE) == QUEUE_SHA256
    assert file_sha256(RELEASE) == RELEASE_SHA256
    assert file_sha256(SOURCE_ARCHIVE) == SOURCE_ARCHIVE_SHA256
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert queue["authority_sha256"] == "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
    selected = [r for r in queue["records"] if FIRST_RANK <= r["candidate_rank"] <= LAST_RANK]
    assert [r["candidate_rank"] for r in selected] == list(range(FIRST_RANK, LAST_RANK + 1))
    assert set(ELIGIBLE) | set(PENDING) | set(REJECT) == set(range(FIRST_RANK, LAST_RANK + 1))
    assert not (set(ELIGIBLE) & set(PENDING) or set(ELIGIBLE) & set(REJECT) or set(PENDING) & set(REJECT))

    norm_counts = Counter(
        r.get("dedupe", {}).get("normalized_statement_sha256")
        for r in release["records"]
        if r.get("dedupe", {}).get("normalized_statement_sha256")
    )
    formal_counts = Counter(
        r.get("formal_type_sha256")
        for r in release["records"]
        if r.get("formal_type_sha256")
    )
    release_by_stage = {r["stage_claim_id"]: r for r in release["records"]}

    archive_prefix = "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669/"
    with tarfile.open(SOURCE_ARCHIVE, "r:gz") as tf:
        license_bytes = tf.extractfile(archive_prefix + "LICENSE").read()
        assert sha256_bytes(license_bytes) == LICENSE_SHA256
        source_bytes = {}
        for candidate in selected:
            member = archive_prefix + candidate["source_member_path"]
            data = tf.extractfile(member).read()
            assert sha256_bytes(data) == candidate["source_locator"]["file_sha256"]
            head = data[:800].decode("utf-8", errors="strict")
            assert "Licensed under the Apache License, Version 2.0" in head
            source_bytes[candidate["candidate_rank"]] = data

    rows = []
    for candidate in selected:
        rank = candidate["candidate_rank"]
        payload = dict(candidate)
        queue_row_hash = payload.pop("row_sha256")
        assert sha256_bytes(canonical_bytes(payload)) == queue_row_hash
        parent = release_by_stage[candidate["stage_claim_id"]]
        sem_hash = candidate["semantic_key"].split("/", 1)[1]
        assert parent["dedupe"]["normalized_statement_sha256"] == sem_hash
        assert parent["formal_type_sha256"] == candidate["formal_type_sha256"]
        assert norm_counts[sem_hash] == 1
        assert formal_counts[candidate["formal_type_sha256"]] == 1
        uniqueness = (
            f"Full release 5.4 scan (Claim_Catalog sha256={RELEASE_SHA256}) found exactly one exact normalized-statement hash and one exact formal-type hash, both at {candidate['stage_claim_id']}; manual logical-subsumption review was then applied."
        )
        decision, reason_codes, note = decision_for(rank)
        refs = primary_refs_for(rank)
        gates = build_gates(candidate, decision, refs, note, uniqueness)
        all_pass = all(g["pass"] is True for g in gates.values())
        assert all_pass == (decision == "eligible_existing_frontier_credit")
        credit_key = None
        if all_pass:
            credit_payload = [refs[0]["identifier"], candidate["formal_type_sha256"], candidate["semantic_key"]]
            credit_key = "frontier-resolution-sha256/" + sha256_bytes(canonical_bytes(credit_payload))
        row = {
            "schema_version": "awesome-theorems/frontier-theorem-human-review/5.5",
            "reviewed_as_of": AS_OF,
            "candidate_rank": rank,
            "stage_claim_id": candidate["stage_claim_id"],
            "variant_id": candidate["variant_id"],
            "family_id": candidate["family_id"],
            "display_name": candidate["display_name"],
            "queue_row_sha256": queue_row_hash,
            "semantic_key": candidate["semantic_key"],
            "decision": decision,
            "gates": gates,
            "primary_references": refs,
            "frontier_credit_key": credit_key,
            "reason_codes": reason_codes,
            "reviewer_notes": note,
            "grants_frontier_credit": all_pass,
            "grants_new_theorem_credit": False,
        }
        row["row_sha256"] = sha256_bytes(canonical_bytes(row))
        rows.append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ledger_bytes = b"".join(canonical_bytes(row) + b"\n" for row in rows)
    LEDGER.write_bytes(ledger_bytes)
    decisions = Counter(row["decision"] for row in rows)
    eligible_keys = [row["frontier_credit_key"] for row in rows if row["frontier_credit_key"]]
    assert len(eligible_keys) == len(set(eligible_keys))
    builder_path = Path(__file__).resolve()
    summary = {
        "schema_version": "awesome-theorems/frontier-theorem-human-review-summary/5.5",
        "reviewed_as_of": AS_OF,
        "scope": "non-Erdos frontier theorem candidates, inclusive ranks 171--254; review eligibility only",
        "rank_range": {"first": FIRST_RANK, "last": LAST_RANK, "inclusive": True, "expected_rows": LAST_RANK - FIRST_RANK + 1},
        "inputs": {
            "queue_path": QUEUE.relative_to(ROOT).as_posix(),
            "queue_sha256": QUEUE_SHA256,
            "queue_authority_sha256": queue["authority_sha256"],
            "release_5_4_claim_catalog_path": RELEASE.relative_to(ROOT).as_posix(),
            "release_5_4_claim_catalog_sha256": RELEASE_SHA256,
            "source_archive_path": SOURCE_ARCHIVE.relative_to(ROOT).as_posix(),
            "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
            "source_license_sha256": LICENSE_SHA256,
        },
        "output": {
            "ledger_path": LEDGER.relative_to(ROOT).as_posix(),
            "ledger_sha256": sha256_bytes(ledger_bytes),
            "ledger_bytes": len(ledger_bytes),
            "ledger_rows": len(rows),
        },
        "counts": {
            "eligible_existing_frontier_credit": decisions["eligible_existing_frontier_credit"],
            "pending": decisions["pending"],
            "reject": decisions["reject"],
            "review_rows": len(rows),
            "review_eligible_frontier_keys": len(eligible_keys),
            "formal_release_frontier_credits_granted": 0,
            "new_theorem_credits_granted": 0,
        },
        "set_digests": {
            "ordered_queue_row_sha256_chain": sha256_bytes(canonical_bytes([row["queue_row_sha256"] for row in rows])),
            "ordered_review_row_sha256_chain": sha256_bytes(canonical_bytes([row["row_sha256"] for row in rows])),
            "semantic_key_set_sha256": sha256_bytes(canonical_bytes(sorted({row["semantic_key"] for row in rows}))),
            "frontier_credit_key_set_sha256": sha256_bytes(canonical_bytes(sorted(eligible_keys))),
            "eligible_rank_set_sha256": sha256_bytes(canonical_bytes(sorted(row["candidate_rank"] for row in rows if row["decision"] == "eligible_existing_frontier_credit"))),
            "pending_rank_set_sha256": sha256_bytes(canonical_bytes(sorted(row["candidate_rank"] for row in rows if row["decision"] == "pending"))),
            "reject_rank_set_sha256": sha256_bytes(canonical_bytes(sorted(row["candidate_rank"] for row in rows if row["decision"] == "reject"))),
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
        "validation": {
            "builder_path": builder_path.relative_to(ROOT).as_posix(),
            "builder_sha256": file_sha256(builder_path),
            "checker_path": CHECKER.relative_to(ROOT).as_posix(),
            "checker_sha256": file_sha256(CHECKER),
            "test_path": TEST.relative_to(ROOT).as_posix(),
            "test_sha256": file_sha256(TEST),
            "status": "checker_bound; independent read-only checker required and run after generation",
        },
    }
    summary["authority_sha256"] = sha256_bytes(canonical_bytes(summary))
    SUMMARY.write_bytes(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")
    print(json.dumps({"rows": len(rows), "counts": summary["counts"], "ledger_sha256": summary["output"]["ledger_sha256"], "authority_sha256": summary["authority_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
