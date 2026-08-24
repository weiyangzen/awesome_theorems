#!/usr/bin/env python3
"""Build the rights-safe 1962--1969 half of the PutnamGAP one-hop review shard."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[6]
OUT_DIR = Path(__file__).resolve().parent
DATASET = Path("/tmp/putnamgap-audit.uYDPao/dataset")
MANIFEST = Path("/tmp/putnamgap-audit.pfFCTE/grid_1962_1977_192_source_manifest.jsonl")
COMMIT = "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
TREE = "0f55aee4f4b911e767785a7c5977fbe36f58dbbe"
PARENT_ROOT = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"
REVIEW_DATE = "2026-08-10"
REVIEWER = "codex-putnam-onehop-1962-1977"
SHARD_SCHEMA = "awesome-theorems/putnam-onehop-review-candidate-shard/5.6"


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def primary(problem: str, label: str, statement: str, selector: str, *, relation: str = "standard_solution_uses", anomalies: tuple[str, ...] = ()) -> dict:
    return {
        "problem": problem,
        "label": label,
        "statement": statement,
        "selector": selector,
        "relation": relation,
        "anomalies": list(anomalies),
    }


# Each statement below is independently written. Selectors are used only while
# computing a source span and are never emitted into a repository artifact.
PRIMARY = [
    primary("1962-A-1", "interior-pair convex-position lemma", "Let D and E lie inside triangle ABC. If the line DE crosses sides AB and AC, then B, C, D, and E occur in convex position.", "Then \\( B, C, D"),
    primary("1962-A-2", "integral-average differential reduction", "For F(x)=integral_0^x f(t)dt and a=f(0)>0, the averaging condition a f(x)=(F(x)/x)^2 implies a F'(x)=F(x)^2/x^2 for x>0.", "Then (2) becomes"),
    primary("1962-A-3", "barycentric area determinant formula", "If the barycentric-coordinate rows of three points relative to triangle ABC are assembled into a matrix M, their oriented area ratio to ABC is det(M).", "area} P Q R"),
    primary("1962-A-4", "Taylor theorem with second-order remainder", "For a twice differentiable function, expansion from an interior point x to either endpoint has a second-order Lagrange remainder evaluated at an intermediate point.", "Using Taylor's formula"),
    primary("1962-A-5", "weighted binomial first-moment identity", "For every positive integer n, sum_{k=1}^n binom(n,k) k x^k = n x (1+x)^(n-1).", "obtain the identity"),
    primary("1962-A-6", "positive-cone square lemma", "Under the stated trichotomy and multiplicative closure on a subset S of the rationals, the square of every nonzero rational belongs to S.", "Since \\( r^{2}"),
    primary("1962-B-1", "uniqueness of convergent power-series coefficients", "Two power series that agree on an interval around zero have equal coefficients term by term.", "power series representations are unique"),
    primary("1962-B-2", "density of the rationals", "Between any two distinct real numbers there is a rational number.", "there is a rational number between"),
    primary("1962-B-3", "Heine-Borel finite-subcover theorem", "Every open cover of a compact real interval has a finite subcover.", "Heine-Borel theorem"),
    primary("1962-B-4", "circle-boundary parity toggle", "Crossing a boundary arc belonging to exactly one circle changes by one the number of circle interiors containing the region, so the containment parity flips.", "one of these regions is interior"),
    primary("1962-B-5", "trapezoidal bound for convex functions", "For a convex function on an interval, the trapezoidal approximation on any partition is at least the integral.", "trapezoidal rule"),
    primary("1962-B-6", "zero bound for trigonometric polynomials", "A nonzero trigonometric polynomial of degree at most n has no more than 2n zeros in one period when multiplicities are counted.", "no more than \\( 2 n \\) zeros"),

    primary("1963-A-1", "inscribed-angle theorem", "An angle subtended by a circular arc at a point on the circle equals half the corresponding central angle.", "half the central angle"),
    primary("1963-A-2", "growth of strictly increasing integer sequences", "If f is strictly increasing and integer-valued, then f(n+p) is at least f(n)+p for positive integers n and p.", "strictly increasing and integer-valued"),
    primary("1963-A-3", "Euler-operator falling-factorial identity", "For delta=x d/dx, the operator delta(delta-1)...(delta-n+1) applied to y equals x^n y^(n).", "We first show that"),
    primary("1963-A-4", "divergence of the harmonic series", "For every starting index k, the partial sums sum_{j=k+1}^{k+p} 1/j are unbounded as p grows.", "harmonic series diverges"),
    primary("1963-A-5", "single-sign-change sine test", "If a continuous function changes sign only once at alpha in (0,pi), then its integral against sin(theta-alpha) is nonzero.", "only zero of \\( f \\)"),
    primary("1963-A-6", "harmonic chord-polar relation", "For a conic, a chord's endpoints are harmonically separated by a point on the chord and the intersection of that chord with the point's polar.", "divided harmonically"),
    primary("1963-B-1", "integer divisor reduction", "If a positive integer a divides both 90 and 92, then a divides 2 and hence a is 1 or 2.", "last two equations"),
    primary("1963-B-2", "classification of additive subgroups of the real line", "An additive subgroup of the real numbers is either trivial, a cyclic discrete subgroup, or dense in the real line.", "Theorem 2"),
    primary("1963-B-3", "separated second-derivative identity", "Every twice differentiable solution of the functional equation satisfies f''(u)f(v)=f(u)f''(v) for all real u and v.", "for any \\( u \\) and \\( v"),
    primary("1963-B-4", "support-line lemma for a perimeter maximizer", "At each vertex of a maximum-perimeter triangle chosen from a planar set, the set has a support line perpendicular to that vertex's internal angle bisector.", "Theorem. If \\( C"),
    primary("1963-B-5", "block-sum domination inequality", "With S_k=sum_{k/2<=n<=k} a_n under the stated comparison hypothesis, one has k a_k/2 <= 100 S_k.", "Adding these inequalities"),
    primary("1963-B-6", "Caratheodory theorem in finite dimension", "Every point in the convex hull of a subset of an n-dimensional real vector space is a convex combination of at most n+1 points of that subset.", "The essence of the problem"),

    primary("1964-A-1", "large-angle side-ratio lemma", "In a triangle whose angle A is at least 120 degrees, if c is no longer than the adjacent side b, then the opposite side a satisfies a >= sqrt(3)c.", "By the law of cosines"),
    primary("1964-A-2", "strict positivity of a weighted square integral", "If f is continuous and strictly positive on [0,1], then integral_0^1 f(x)(x-alpha)^2 dx is strictly positive for every real alpha.", "this integral is clearly positive"),
    primary("1964-A-3", "cubic decrement under interval splitting", "Splitting an interval of length a+b into pieces a and b decreases the sum of cubed lengths by exactly 3ab(a+b).", "S_{n \cdot 1}-S_{n}"),
    primary("1964-A-4", "finite-state recurrence periodicity theorem", "Every bounded integer sequence generated deterministically from a fixed finite window of its preceding terms is eventually periodic.", "much more general theorem", relation="generalization"),
    primary("1964-A-5", "finite Knopp-type inequality", "For positive a_1,...,a_k and A_n=sum_{j<=n}a_j, one has sum_{n=1}^k n/A_n <= 4 sum_{n=1}^k 1/a_n.", "We shall prove"),
    primary("1964-A-6", "span theorem for repeated differences", "For a finite subset of a rational vector space, the span of differences that occur only once equals the span of all pairwise differences.", "The linear span of the non-repeated", relation="generalization"),
    primary("1964-B-1", "reciprocal-tail counting bound", "If u_1<=u_2<=... are positive and V_n counts terms at most n, then (V_n-p)/n <= sum_{k=p+1}^{V_n}1/u_k for V_n>p.", "for a fixed \\( p"),
    primary("1964-B-2", "complementary-pair bound for intersecting families", "An intersecting family of subsets of an n-element set contains at most one member from each complementary pair, and therefore has size at most 2^(n-1).", "complementary pairs"),
    primary("1964-B-3", "eventual coverage by dilated intervals", "For 0<a<b and any positive integer k, the union of [na,nb] over n>=k contains a ray [c,infinity).", "Lemma. If \\( 0<a<b"),
    primary("1964-B-4", "Euler formula on the sphere", "For a connected cellular graph embedded on a sphere, the numbers of vertices, edges, and faces satisfy V-E+F=2.", "By Euler's formula"),
    primary("1964-B-5", "divisor-count square-root bound", "Every positive integer N has at most 2 sqrt(N) positive divisors.", "at least \\( n \\) positive divisors"),
    primary("1964-B-6", "center-fixing lemma for a two-piece disk congruence", "An isometry between two putative disjoint congruent pieces covering a unit disk would have to send the disk center to itself.", "Thus \\( p^{*}=p"),

    primary("1965-A-1", "isosceles-triangle angle transfer", "In a triangle, equality of two side lengths forces equality of the opposite angles; applying this to the two exterior-bisector triangles gives the angle relations used in the solution.", "triangle \\( A B Y"),
    primary("1965-A-2", "Vandermonde convolution", "For nonnegative integers m,n,k, sum_r binom(m,k-r)binom(n,r)=binom(m+n,k).", "well-known identities"),
    primary("1965-A-3", "square-index interpolation bound for Cesaro means", "If m=n^2+k with 0<=k<=2n and |c_r|=1, then the difference between S(m)/m and S(n^2)/n^2 tends uniformly to zero as n grows.", "write \\( m=n^{2}+k"),
    primary("1965-A-4", "maximal-neighborhood witness lemma", "In a finite bipartite graph, if a vertex b has maximum degree and a nonneighbor g' has a neighbor b', then b has a neighbor not adjacent to b'.", "maximal number of girls"),
    primary("1965-A-5", "endpoint-reflection bijection for admissible arrangements", "The map a_i -> n+1-a_i is a fixed-point-free pairing of admissible arrangements ending in 1 with those ending in n.", "there is another \\( n \\)-arrangement"),
    primary("1965-A-6", "tangent equation for an l^m unit curve", "At a nonnegative point (x_0,y_0) of x^m+y^m=1, the tangent line is x_0^(m-1)x+y_0^(m-1)y=1.", "The tangent to this curve"),
    primary("1965-B-1", "measure-preserving reflection of the unit cube", "The substitution x_k -> 1-x_k preserves the unit cube and interchanges the cosine-squared and sine-squared integrands in the stated integral.", "change of variables"),
    primary("1965-B-2", "tournament win-loss square identity", "If each player has w_r+l_r=n-1 and the total wins equal the total losses, then sum_r w_r^2=sum_r l_r^2.", "omega_{r}+l_{r}"),
    primary("1965-B-3", "Euclid parametrization of Pythagorean triples", "Every integer right triangle has sides lambda(p^2-q^2), 2lambda pq, and lambda(p^2+q^2) after interchanging the legs, with the usual coprimality and parity conditions.", "All Pythagorean triples"),
    primary("1965-B-4", "even-odd binomial quotient formula", "The quotient of the even and odd binomial parts can be written using (1+sqrt(x))^n and (1-sqrt(x))^n, yielding a geometric-ratio convergence test.", "we first note that"),
    primary("1965-B-5", "balanced complete bipartite graph bound", "A complete bipartite graph on V vertices is triangle-free and, with balanced parts, has floor(V^2/4) edges.", "Divide the objects into two subsets"),
    primary("1965-B-6", "separating-circle lemma for two point pairs", "If two point pairs are neither concyclic nor collinear, their perpendicular bisectors are distinct and one can choose a circle through each pair so that the two circles are disjoint.", "neither concyclic nor collinear"),

    primary("1966-A-1", "closed form for the repeated-integer partial sums", "For the sequence 0,1,1,2,2,..., the sum of its first n terms is n^2/4 for even n and (n^2-1)/4 for odd n.", "verified by induction"),
    primary("1966-A-2", "Heron-inradius identity", "For a triangle with semiperimeter p and inradius r, p r^2=(p-a)(p-b)(p-c).", "Squaring and equating"),
    primary("1966-A-3", "recurrence comparison bound", "If 0<x_1<1 and x_(n+1)=x_n(1-x_n), then (n+1)x_n<=1 for every n>=2.", "So by induction"),
    primary("1966-A-4", "nearest-square transition criterion", "The nearest integer to sqrt(n) increases exactly at those n for which the corresponding square-deleted index skips a perfect square.", "perfect square if and only if"),
    primary("1966-A-5", "pointwise form of a local linear operator", "If T is local and linear on continuous real functions and f=T1, then Tpsi(x_0)=psi(x_0)f(x_0) for every psi and x_0.", "By continuity of"),
    primary("1966-A-6", "finite nested-radical identity", "The identity (n+2)^2=1+(n+1)(n+3) permits the finite radical tail sqrt((n+2)^2) to collapse recursively to the value 3.", "Proceedirg by induction"),
    primary("1966-B-1", "orthogonal-projection square decomposition", "For every polygon edge, its squared length is the sum of the squared lengths of its two orthogonal projections.", "using the Pythagorean theorem"),
    primary("1966-B-2", "small-prime divisor lemma for a ten-term interval", "A common divisor greater than one of two distinct integers in a block of ten must have a prime divisor among 2, 3, 5, and 7.", "common factor of two"),
    primary("1966-B-3", "weighted Cauchy-Schwarz estimate", "For positive p_n and q_n=sum_{j<=n}p_j, (sum_{n=2}^N n/q_n)^2 <= (sum_{n=2}^N n^2 p_n/q_n^2)(sum_{n>=1}1/p_n).", "Schwarz's inequality"),
    primary("1966-B-4", "rank-pigeonhole lemma for divisibility chains", "If every divisibility chain among mn+1 ordered integers has length at most n, then at least m+1 integers share the same maximum-chain rank and form an antichain.", "there are at least \\( m+1"),
    primary("1966-B-5", "uncrossing shortens a polygonal tour", "If two nonadjacent edges of a polygonal tour cross and no three vertices are collinear, reconnecting the four endpoints without the crossing strictly shortens the tour.", "would have shorter length"),
    primary("1966-B-6", "weighted energy identity for the differential equation", "A solution of y''+e^x y=0 satisfies an identity bounding y(T)^2 by y(0)^2+y'(0)^2 for every T>=0.", "We then obtain"),

    primary("1967-A-1", "sine quotient limit", "The limit of sin(x)/x as x tends to zero is 1.", "sin x}{x}"),
    primary("1967-A-2", "involution recurrence", "The number S_n of involutions on n labeled elements satisfies S_n=S_(n-1)+(n-1)S_(n-2).", "Consequently"),
    primary("1967-A-3", "quadratic midpoint bound", "For 0<r<1, r(1-r)<=1/4, with equality exactly at r=1/2.", "graph of \\( r(r-1)"),
    primary("1967-A-4", "triangular convolution integral identity", "If alpha=integral_0^1 u, then integral_0^1 u(y) integral_0^y u(z)dz dy=alpha^2/2.", "Set \\( f(y)"),
    primary("1967-A-5", "diameter-section bound for a convex region", "If a convex planar region has diameter below 1 and vertical boundary functions f and -g over [-d,d], then f(x)+g(-x)<sqrt(1-4x^2); integrating gives area below pi/4.", "Calculating the distance", anomalies=("source_ocr_sign_and_integral_value_error",)),
    primary("1967-A-6", "central-line arrangement region count", "Four distinct lines through the origin divide the plane into exactly eight open sectors.", "four lines through the origin"),
    primary("1967-B-1", "sixty-degree complex rotation criterion", "For omega=e^(i pi/3), if Q+omega(R-Q)=P, then triangle PQR is equilateral.", "rotated through \\( \\pi / 3"),
    primary("1967-B-2", "transformed mixed-coefficient obstruction", "With p'=p-1/2 and r'=r-1/2, the mixed coefficient beta equals 1/2-2p'r'; the three coefficient bounds below 4/9 are mutually incompatible.", "setting \\( p^{\\prime}"),
    primary("1967-B-3", "periodic block-integral identity", "If g has period one, then integral_{m/n}^{(m+1)/n} g(nx)dx=(1/n)integral_0^1 g(t)dt.", "The first term equals"),
    primary("1967-B-4", "odd-divisor characterization of squares", "A positive integer has an odd number of positive divisors if and only if it is a perfect square.", "odd if and only if"),
    primary("1967-B-5", "constant recurrence for truncated negative-binomial sums", "The truncated sums A_n in the solution satisfy A_n=A_(n-1), and A_1=1/2.", "Thus \\( A_{n}=A_{n-1}"),
    primary("1967-B-6", "Fermat stationary-point theorem", "At an interior local minimum of a differentiable function of two real variables, both first partial derivatives vanish.", "has a minimum"),

    primary("1968-A-1", "polynomial-division identity for the pi integral", "For 0<=x<=1, x^4(1-x)^4/(1+x^2)=x^6-4x^5+5x^4-4x^2+4-4/(1+x^2).", "By division"),
    primary("1968-A-2", "density of rational perturbations", "For every epsilon>0 there is a rational rho satisfying 0<rho<epsilon.", "selecting a rational number"),
    primary("1968-A-3", "Gray-code and hypercube equivalence", "A cyclic listing of all subsets in which consecutive subsets differ in one element is equivalent to a Hamiltonian circuit of the Boolean n-cube through the zero vertex.", "equivalent to finding", relation="equivalence"),
    primary("1968-A-4", "pairwise-distance variance identity", "For vectors v_1,...,v_n, sum_{i<j}|v_i-v_j|^2=n sum_i|v_i|^2-|sum_i v_i|^2.", "general identities"),
    primary("1968-A-5", "quadratic endpoint interpolation identity", "Every quadratic polynomial P satisfies P'(0)=4P(1/2)-3P(0)-P(1).", "f^{\\prime}(0)=b"),
    primary("1968-A-6", "AM-GM bound for squared real roots", "For real roots z_1,...,z_n, their mean square is at least the nth root of the product z_1^2...z_n^2.", "arithmetic-geometric mean inequality"),
    primary("1968-B-1", "two-event probability valuation identity", "If events A,B,C,D have A union B=C union D and A intersection B=C intersection D, then P(A)+P(B)=P(C)+P(D).", "A \\cup B=C \\cup D"),
    primary("1968-B-2", "more-than-half intersection lemma", "Any two subsets of a finite set, each containing more than half its elements, must intersect.", "If these two sets are disjoint"),
    primary("1968-B-3", "tower law for finite field extensions", "For finite extensions K subset L subset M, [M:K]=[M:L][L:K].", "If \\( K, L, M"),
    primary("1968-B-4", "two-branch change-of-variables identity", "The two inverse branches of y=x-1/x have Jacobian contributions whose sum is one, so their transformed integrals recombine into the integral of f(y).", "After the changes of variable"),
    primary("1968-B-5", "product-count lemma over a prime field", "Over F_p, bc=0 has 2p-1 ordered solutions, while bc=t for nonzero t has p-1 ordered solutions.", "There are \\( 2 p-1"),
    primary("1968-B-6", "closed-set density obstruction", "A closed subset of the real line that contains every rational in a nondegenerate interval also contains the entire interval, including irrational points.", "since \\( K_{n} \\) is closed"),

    primary("1969-A-1", "connected-image theorem", "The continuous image of a connected topological space in the real line is an interval.", "continuity of \\( f(x, y)"),
    primary("1969-A-2", "triangular determinant product rule", "The determinant of a triangular matrix is the product of its diagonal entries.", "product of its diagonal elements"),
    primary("1969-A-3", "Euler planar formula", "For a connected planar cell decomposition, V-E+F=2.", "Euler's formula"),
    primary("1969-A-4", "termwise integration under uniform convergence", "A uniformly convergent series of continuous functions on a compact interval may be integrated term by term.", "uniform convergence can be applied"),
    primary("1969-A-5", "difference equation invariant", "Every solution of the system satisfies x(t)-y(t)=(x_0-y_0)e^(2t), independently of the control u(t).", "Subtracting the two equations"),
    primary("1969-A-6", "iterated affine-contraction bound", "If e_n<=epsilon/4+e_(n-1)/2 eventually, then e_(n+m)<epsilon/2+2^(-(m+1))e_(n-1).", "can be iterated"),
    primary("1969-B-1", "divisor-pair congruence lemma", "When n is congruent to -1 modulo 24, every divisor pair d and n/d has sum divisible by both 3 and 8, hence by 24.", "In every case"),
    primary("1969-B-2", "Lagrange subgroup-order theorem", "The order of a subgroup of a finite group divides the order of the group.", "number of elements in a subgroup"),
    primary("1969-B-3", "Wallis product", "The Wallis product gives pi/2 as the limit of alternating ratios of even and odd double factorials.", "Wallis product"),
    primary("1969-B-4", "bounding-rectangle length constraint", "For the minimal axis-parallel rectangle of width a and height b covering a unit-length curve, the broken-line projection argument gives a^2+4b^2<=1.", "a^{2}+4 b^{2}"),
    primary("1969-B-5", "counting-function tail bound", "For increasing positive a_n and k(x)=#{n:a_n<=x}, one has sum_{n=N}^{infinity}1/a_n >= (k(x)-N)/x whenever k(x)>=N.", "for any positive integer \\( N"),
    primary("1969-B-6", "one-sided inverses from full rank", "A full-column-rank matrix has a left inverse and a full-row-rank matrix has a right inverse.", "Hence there exist matrices"),
]


def extra(problem: str, slug: str, label: str, statement: str | None, selector: str, relation: str | None, disposition: str, reason: str, *, kind: str = "claim", status: str | None = "proved", citation: str | None = None, anomalies: tuple[str, ...] = ()) -> dict:
    return {
        "problem": problem, "slug": slug, "label": label, "statement": statement,
        "selector": selector, "relation": relation, "disposition": disposition,
        "reason": reason, "kind": kind, "status": status, "citation": citation,
        "anomalies": list(anomalies),
    }


EXTRAS = [
    extra("1962-A-1", "convex-pentagon-generalization", "nine-point convex-pentagon theorem", "Every set of nine planar points with no three collinear contains five points in convex position.", "every set of nine points", "generalization", "accepted_edge", "explicit proposition-level generalization in a cited remark", citation="W. E. Bonnice, American Mathematical Monthly 81 (1974), 749-752"),
    extra("1962-A-4", "extremal-classification", "equality-case classification for the Landau derivative bound", "Under the solution's hypotheses, equality |f'(x)|=2 occurs only at an endpoint, and the extremizers are the four reflected quadratic examples described there.", "only extremal functions", "strengthening", "accepted_edge", "remark adds equality locations and a complete extremizer classification"),
    extra("1962-A-4", "landau-citation", "Landau derivative inequality citation", None, "first established by Landau", None, "rejected_duplicate_candidate", "citation concerns the seed theorem itself rather than a distinct endpoint", kind="historical_event", status=None, citation="E. Landau, Proceedings of the London Mathematical Society (2) 13 (1914), 43-49"),
    extra("1962-A-4", "related-inequalities", "Schoenberg related inequalities", None, "several similar inequalities", None, "rejected_relation_not_established", "bibliographic related-work wording gives no exact proposition-level relation", kind="topic", status=None, citation="I. J. Schoenberg, American Mathematical Monthly 80 (1973), 121-158"),
    extra("1962-A-6", "ordered-field-generalization", "positive-cone characterization in ordered fields", "A subset P of a field is a positive cone precisely when it is closed under addition and multiplication and exactly one of x, -x, or 0 lies in P for every x.", "abstract ordered field", "generalization", "accepted_edge", "remark explicitly places the argument in the general positive-cone characterization"),
    extra("1962-A-6", "drop-product-property", "additive-trichotomy weakening over the rationals", "If multiplicative closure is omitted but additive closure and trichotomy are retained on Q, the set is either the positive rationals or the negative rationals.", "product property is dropped", "weakening", "accepted_edge", "remark states a theorem under weaker assumptions and a correspondingly weaker conclusion"),
    extra("1962-B-2", "dense-range-generalization", "dense-range embedding generalization", "The construction remains strictly inclusion-preserving when the enumerating map from N to R merely has dense range; bijectivity onto Q is unnecessary.", "sufficient that", "generalization", "accepted_edge", "remark explicitly weakens the construction hypothesis"),
    extra("1962-B-3", "bolzano-weierstrass", "Bolzano-Weierstrass theorem", "Every bounded sequence in R has a convergent subsequence.", "Bolzano-Weierstrass theorem", "standard_solution_uses", "accepted_edge", "named theorem is applied in the closed-set branch"),
    extra("1962-B-4", "coloring-reading", "general coloring references", None, "four-color problem", None, "rejected_topic_only", "the remark supplies a topic and reading reference, not a proposition relation", kind="topic", status=None, citation="E. B. Dynkin and V. A. Uspenskii, Multicolor Problems (1963)"),
    extra("1962-B-5", "exponential-tangent-inequality", "exponential tangent inequality", "For every real x, 1-x<=e^(-x).", "1-x \\leq e^{-x}", "standard_solution_uses", "accepted_edge", "explicit inequality drives the geometric-series upper bound"),
    extra("1963-A-3", "taylor-integral-remainder", "Taylor theorem with integral remainder", "If y^(n) is continuous, then y(x) equals its degree-(n-1) Taylor polynomial at a plus integral_a^x (x-t)^(n-1)y^(n)(t)/(n-1)! dt.", "standard forms of Taylor's theorem", "standard_solution_uses", "accepted_edge", "named theorem collapses the repeated integration"),
    extra("1963-A-4", "log-tangent-bound", "logarithm tangent-line inequality", "For every x>-1, log(1+x)<=x.", "log (1+x) \\leq x", "standard_solution_uses", "accepted_edge", "explicit inequality proves sharpness of the constant"),
    extra("1963-A-6", "butterfly-generalization", "projective butterfly generalization", "The midpoint conclusion persists for an arbitrary nondegenerate conic, and the two opposite joining lines may be replaced by a conic through the four auxiliary chord points as described in the remark.", "ellipse can be any conic", "generalization", "accepted_edge", "remark explicitly broadens both the base conic and an incidence component"),
    extra("1963-A-6", "butterfly-name", "butterfly theorem", None, "butterfly theorem", None, "rejected_duplicate_candidate", "the named theorem is the seed claim, not a distinct one-hop endpoint", kind="claim", status="proved", citation="H. Eves, A Survey of Geometry (1972)"),
    extra("1963-B-2", "unique-factorization", "unique factorization for positive integers", "If 2^p=3^q for nonnegative integers p and q, then p=q=0.", "unique factorization theorem", "standard_solution_uses", "accepted_edge", "named theorem excludes a rational dependence between log 2 and log 3"),
    extra("1963-B-4", "circle-specialization", "maximum-perimeter inscribed triangle in a circle", "Every maximum-perimeter triangle inscribed in a circle is equilateral.", "If \\( C \\) is a circle", "specialization", "accepted_edge", "solution derives the circle case as a specialization of the support-line theorem"),
    extra("1964-A-1", "sharp-six-point-bound", "sharp six-point planar distance-ratio bound", "Among six planar points, the ratio of the greatest pairwise distance to the least is at least 2 sin(72 degrees), with equality for a regular pentagon together with its center.", "not the best possible", "strengthening", "accepted_edge", "remark gives a strictly sharper constant and an equality configuration", anomalies=("source_ocr_approximation_separator",)),
    extra("1964-A-5", "knopp-sharp-constant", "sharp Knopp constant", "The least universal K in the infinite inequality is 2.", "least constant", "strengthening", "accepted_edge", "remark sharpens the demonstrated constant from 4 to 2", citation="K. Knopp, Journal of the London Mathematical Society 3 (1928), 205-211"),
    extra("1964-A-5", "redheffer-stronger", "Redheffer strengthened inequality", "For every positive sequence, 3/a_1+5/A_2+7/A_3+... is at most 4 sum_n 1/a_n, with A_n=a_1+...+a_n.", "inequality that is stronger", "strengthening", "accepted_edge", "remark explicitly states a proposition stronger than the displayed Knopp inequality", citation="R. M. Redheffer, Proceedings of the London Mathematical Society 17 (1967), 683-699"),
    extra("1964-A-5", "redheffer-local-lemma", "Redheffer rational inequality lemma", "For lambda>0 and x>0, (lambda+2)^2/(1+x)<=4/x+lambda^2, with equality exactly when x=2/lambda.", "Lemma. Suppose \\( \\lambda>0", "standard_solution_uses", "accepted_edge", "local lemma is applied in the induction proving the stronger finite inequality"),
    extra("1964-A-6", "straus-general-theorem", "rational-span theorem for finite differences", "For every finite subset of a rational vector space, all pairwise differences are spanned by those differences that occur only once.", "Theorem. The linear span", "generalization", "accepted_edge", "the source labels and proves this exact generalization", citation="E. G. Straus, Acta Arithmetica 11 (1965), 203-204"),
    extra("1964-B-3", "baire-category", "Baire category theorem for the real line", "If countably many closed subsets of R cover a nondegenerate interval, at least one of them contains a nondegenerate interval.", "By the Baire category theorem", "standard_solution_uses", "accepted_edge", "named theorem supplies the interval on which the estimates are uniform"),
    extra("1964-B-3", "complete-metric-baire", "Baire category theorem for complete metric spaces", "If a countable union of closed subsets of a complete metric space contains a nonempty open set, one closed subset has nonempty relative interior there.", "more general context", "generalization", "accepted_edge", "note explicitly states the complete-metric-space generalization"),
    extra("1965-A-5", "proved-enumeration-conjecture", "admissible-arrangement count", "The number of admissible arrangements of 1,...,n in the problem is 2^(n-1).", "we conjecture the answer", "standard_solution_uses", "accepted_edge", "the provisional conjecture is proved immediately by induction and is not open"),
    extra("1965-B-4", "complex-domain-extension", "complex extension of the binomial-quotient limit", "For every complex x off the negative real axis, the quotient converges to the square root of x in the right half-plane.", "all other complex numbers", "generalization", "accepted_edge", "solution explicitly extends the real-domain limit to a complex domain"),
    extra("1966-A-5", "weakened-linearity-hypothesis", "local homogeneous-operator strengthening", "The multiplication-operator conclusion needs only scalar homogeneity of T together with locality and continuity of every image; additivity is not used.", "needed only in the case", "strengthening", "accepted_edge", "comment explicitly weakens the hypotheses while retaining the conclusion"),
    extra("1966-A-6", "finite-radical-proved", "finite radical formula initially conjectured in the solution", "For every n>=1, the finite radical with terminal value sqrt((n+2)^2) described in the solution evaluates to 3.", "leads us to conjecture", "standard_solution_uses", "accepted_edge", "the source's word conjecture is provisional; the following induction proves the formula", anomalies=("provisional_conjecture_wording_but_proved",)),
    extra("1967-A-2", "involution-equivalence", "symmetric permutation matrices and involutions", "Symmetric n-by-n permutation matrices are in bijection with involutions of n labeled symbols.", "number of permutations", "equivalence", "accepted_edge", "comment gives an exact bijective reformulation"),
    extra("1967-A-5", "boundary-hypothesis-removed", "convex-region diameter conclusion without boundary regularity", "The unit-distance conclusion remains valid for every convex planar region of area greater than pi/4; no finiteness condition on straight boundary segments is required.", "requirement that the boundary", "strengthening", "accepted_edge", "comment explicitly removes an extraneous hypothesis", anomalies=("source_ocr_sign_and_integral_value_error",)),
    extra("1967-B-5", "random-walk-equivalence", "negative-binomial truncation as a boundary-hitting probability", "The truncated binomial sum equals the probability that a symmetric northeast lattice walk first reaches the boundary of the n-by-n square on its right side rather than its top side.", "Alternate solution: Consider a random walk", "equivalence", "accepted_edge", "alternate solution gives an exact probabilistic interpretation of the sum"),
    extra("1968-B-4", "dirichlet-corollary", "Dirichlet-test corollary for improper integrals", "The improper integrals arising from the two inverse substitutions converge under the stated continuity and convergence assumptions on f.", "corollary of the Dirichlet Test", "standard_solution_uses", "accepted_edge", "named corollary justifies recombining the transformed improper integrals", citation="R. C. Buck, Advanced Calculus, p. 143"),
    extra("1969-A-3", "angle-count-proof", "triangulation angle-count identity", "In a triangulation with m interior and n boundary vertices, the total triangle-angle sum is both pi times the number of triangles and 2pi m+(n-2)pi.", "sum of all the angles", "standard_solution_uses", "accepted_edge", "independent first proof uses this exact identity"),
    extra("1962-A-2", "solution-family-duplicate", "explicit solution family for the seed", "The positive solutions of the original averaging problem have the rational-square form derived in the standard solution, on the maximal interval where they remain integrable.", "We can integrate this differential equation", None, "rejected_duplicate_candidate", "the formula is the solved seed conclusion rather than a distinct one-hop endpoint"),
    extra("1962-A-2", "corrupt-remark-variant", "OCR-corrupted differential-equation remark", None, "Remark. If", None, "rejected_relation_not_established", "the frozen remark has a corrupted parameter and does not support a safely reconstructible proposition relation", kind="claim", status=None, anomalies=("source_ocr_corrupt_parameter",)),
    extra("1963-B-2", "rank-two-density-theorem", "density criterion for two generated real subgroups", "For real alpha and beta, the subgroup Z alpha+Z beta is dense in R unless alpha and beta satisfy a nontrivial integer linear relation.", "Theorem 1.", "standard_solution_uses", "accepted_edge", "the named theorem is the direct density criterion applied to log 2 and log 3"),
    extra("1963-B-2", "theorem-two-proof-reference", "proof reference to additive-subgroup classification", "An additive subgroup of R with a least positive element x is exactly xZ.", "Proof of Theorem 2", None, "rejected_duplicate_candidate", "this occurrence proves a component of the already accepted subgroup-classification candidate"),
    extra("1963-B-2", "theorem-one-proof-reference", "proof reference to the two-generator density theorem", "A nondense subgroup generated by alpha and beta is cyclic and therefore yields a nontrivial integer relation between alpha and beta.", "Proof of Theorem 1", None, "rejected_duplicate_candidate", "this occurrence proves the already accepted two-generator density candidate"),
    extra("1963-B-6", "caratheodory-proof-reference", "proof reference to Caratheodory reduction", "An affine dependence among more than n+1 points lets one adjust convex coefficients until one coefficient vanishes without making another negative.", "choose \\( \\sigma \\) so that", None, "rejected_duplicate_candidate", "this is the reduction step inside the already accepted Caratheodory theorem"),
    extra("1963-B-6", "caratheodory-application-reference", "application reference to the dimension-three Caratheodory theorem", "In dimension at most three, every convex-hull point is a convex combination of at most four source points.", "By the theorem we can write", None, "rejected_duplicate_candidate", "this is an application occurrence of the already accepted theorem"),
    extra("1964-B-1", "positive-real-sequence-extension", "positive-real extension of the reciprocal counting theorem", "The integer assumption on the positive sequence u_k is unnecessary; the same density conclusion holds for any positive real sequence.", "need not assume the \\( u \\) 's are integers", "strengthening", "accepted_edge", "the remark explicitly removes the integrality hypothesis"),
    extra("1964-B-1", "mixed-sign-warning", "mixed-sign analogue warning", None, "mixed sign", None, "rejected_relation_not_established", "the remark gives a failure mode for a different counting definition but no accepted relation type to a distinct theorem endpoint", kind="topic", status=None),
    extra("1964-B-2", "fixed-element-family", "fixed-element extremal intersecting family", "All subsets of an n-element set that contain one fixed element form an intersecting family of size 2^(n-1) satisfying the stated maximality condition.", "collection of all subsets", "specialization", "accepted_edge", "remark supplies an exact extremal construction"),
    extra("1964-B-4", "euler-cellularity-note", "cellularity hypotheses for Euler's sphere formula", "Euler's relation on the sphere applies when graph edges are topological arcs and complementary regions are disks; the unmodified zero- and one-circle decompositions violate these hypotheses.", "Euler's formula for networks", "specialization", "accepted_edge", "note states the exact applicability conditions and exceptional small cases"),
    extra("1966-A-2", "symmetric-square-inequality", "three-variable symmetric square inequality", "For real x,y,z, x^2+y^2+z^2 is at least xy+xz+yz.", "trivial inequalities", "standard_solution_uses", "accepted_edge", "the displayed pairwise square bounds sum to the required inequality"),
    extra("1966-A-6", "nested-radical-comparison", "nested-radical comparison inequality", "For alpha>1 and n>=1, sqrt(1+n alpha)<=sqrt(alpha)sqrt(1+n).", "To set an inequality in the other direction", "standard_solution_uses", "accepted_edge", "the explicit inequality supplies the lower comparison for the finite radicals"),
    extra("1966-B-3", "quadratic-bound-step", "quadratic estimate for partial sums", "If S,T,c are nonnegative and S<=c+2sqrt(ST)+T, then sqrt(S)<=sqrt(T)+sqrt(2T+c).", "This quadratic inequality implies", "standard_solution_uses", "accepted_edge", "the algebraic estimate turns the Cauchy-Schwarz inequality into a uniform partial-sum bound"),
    extra("1967-A-6", "linear-system-parametrization", "two-equation solution-space parametrization", "When the leading 2-by-2 minor is nonzero, the two homogeneous equations are equivalent to expressing x_1 and x_2 as linear forms in the free variables x_3 and x_4.", "leads to the equivalent system", "equivalence", "accepted_edge", "the solution explicitly gives an equivalent two-parameter system"),
    extra("1967-A-6", "minor-nondegeneracy-equivalence", "minor criterion for eight sign sectors", "The four sign-boundary lines are distinct exactly when every 2-by-2 minor a_i b_j-a_j b_i is nonzero.", "This is equivalent to the conditions", "equivalence", "accepted_edge", "the final paragraph states necessary and sufficient algebraic conditions"),
    extra("1968-A-2", "seed-conclusion-reference", "rational linear-system conclusion", "The nonsingular rational 2-by-2 system used in the solution has a unique rational solution.", "solution for \\( r \\) and \\( s \\) exist", None, "rejected_duplicate_candidate", "this occurrence closes the seed proof and does not introduce a distinct candidate beyond the rational-perturbation prerequisite"),
    extra("1969-A-4", "log-moment-integration-formula", "logarithmic moment integral", "For integers m,k>=0, integral_0^1 x^m(log x)^k dx=(-1)^k k!/(m+1)^(k+1).", "Let \\( F(m, k)", "standard_solution_uses", "accepted_edge", "integration by parts establishes the displayed recurrence and closed form"),
    extra("1969-B-1", "modular-reformulation", "modular reformulation of divisibility by 24", "For an integer n, 24 divides n+1 exactly when n is -1 modulo both 3 and 8.", "condition \\( 24 \\mid n+1 \\) is equivalent", "equivalence", "accepted_edge", "the solution begins with this exact Chinese-remainder reformulation"),
    extra("1969-B-2", "identity-nonclaim", "group identity element", None, "have the identity in common", None, "rejected_nonclaim_endpoint", "the identity element is a defined object, not a truth-apt proposition endpoint", kind="definition", status=None),
    extra("1964-A-5", "finite-to-infinite-reference", "finite Knopp inequality implication", "The uniform finite inequality with constant 4 implies the corresponding infinite-series inequality by passage to increasing partial sums.", "From this inequality", None, "rejected_duplicate_candidate", "this is the implication from the already accepted finite prerequisite to the seed conclusion"),
    extra("1964-A-5", "infinite-conclusion-reference", "infinite Knopp inequality conclusion", "If sum_n 1/a_n converges, the finite bounds pass to sum_n n/A_n<=4 sum_n 1/a_n.", "If the series \\( \\sum_{n=1}^{\\infty}", None, "rejected_duplicate_candidate", "this paragraph is the seed conclusion obtained from the accepted finite inequality"),
    extra("1964-A-5", "local-lemma-proof-reference", "proof reference for the rational inequality lemma", "The auxiliary function used for the local rational inequality reaches its maximum at x=2/lambda.", "This critical point", None, "rejected_duplicate_candidate", "this is a proof occurrence for the already accepted local lemma"),
    extra("1964-A-5", "local-lemma-application-reference", "application reference for the rational inequality lemma", "Substituting x=a_(p+1)/A_p and lambda=p into the local lemma supplies the induction-step estimate.", "applying the lemma", None, "rejected_duplicate_candidate", "this is the application occurrence of the already accepted local lemma"),
    extra("1964-A-5", "strong-finite-induction-reference", "strong finite inequality induction step", "Adding the local-lemma estimate to the p-case proves the displayed stronger finite inequality for p+1.", "Adding this inequality", None, "rejected_duplicate_candidate", "this is a proof step within the already accepted Redheffer strengthening"),
    extra("1964-A-5", "strictness-strengthening", "strictness of the convergent Knopp bound", "When sum_n 1/a_n converges, the constant-4 inequality obtained in the solution is strict.", "it follows that the inequality is strict", "strengthening", "accepted_edge", "the final sentence adds a strictness conclusion to the non-strict seed bound"),
    extra("1964-A-6", "span-theorem-proof-reference", "proof reference for the repeated-difference span theorem", "A separating rational linear functional would contradict the extremal gap after an injective perturbation.", "Suppose this theorem is false", None, "rejected_duplicate_candidate", "this paragraph proves the already accepted generalized span theorem"),
    extra("1964-A-6", "span-theorem-application-reference", "application reference for the repeated-difference span theorem", "When the only nonrepeated oriented differences are 1 and -1, the span theorem forces every difference to be rational.", "This contradiction proves the theorem", None, "rejected_duplicate_candidate", "this paragraph applies the already accepted generalized span theorem"),
    extra("1964-A-6", "span-theorem-bibliographic-reference", "bibliographic occurrence for the repeated-difference theorem", "The source attributes the finite-difference result and its rational-vector-space generalization to the cited papers.", "Remarks. The result was first published", None, "rejected_duplicate_candidate", "the bibliographic occurrence refers to already accepted seed/generalization endpoints", citation="Mikusinski and Schinzel, Acta Arithmetica 9 (1964), 91-95; E. G. Straus, Acta Arithmetica 11 (1965), 203-204"),
    extra("1964-B-3", "baire-theorem-declaration", "declaration occurrence of the real-line Baire theorem", "If countably many closed subsets of R cover an interval, one of the closed subsets contains an interval.", "Baire Category Theorem. Suppose", None, "rejected_duplicate_candidate", "the declaration supplies the statement of the already accepted named-theorem use"),
    extra("1964-B-3", "baire-proof-reference", "proof occurrence for the real-line Baire theorem", "A nested-interval construction contradicts a countable closed cover in which every member has empty interior.", "Assuming that the conclusion of the theorem", None, "rejected_duplicate_candidate", "this paragraph is part of the proof of the already accepted Baire theorem"),
    extra("1966-A-6", "comparison-repetition-reference", "repeated nested-radical comparison", "Iterating the accepted comparison inequality through the nested radical yields the lower bound used for convergence.", "A repetition of this inequality", None, "rejected_duplicate_candidate", "this is an application reference to the already accepted comparison inequality"),
    extra("1969-B-2", "klein-four-counterexample", "Klein-four three-subgroup counterexample", "The Klein four-group is the union of its three distinct order-two proper subgroups.", "An example for the second part", None, "rejected_duplicate_candidate", "the counterexample is the seed's requested three-subgroup conclusion rather than a distinct one-hop endpoint"),
]


def paragraphs(solution: str) -> list[tuple[int, int]]:
    result = []
    for match in re.finditer(r"(?:^|\n\n)(.*?)(?=\n\n|$)", solution, flags=re.S):
        start, end = match.span(1)
        if solution[start:end].strip():
            result.append((start, end))
    return result


def locate(solution: str, selector: str) -> tuple[int, int]:
    lowered = solution.lower()
    needle = selector.lower()
    pos = lowered.find(needle)
    if pos < 0:
        # Treat selectors containing TeX spacing as forgiving regexes.
        pattern = re.escape(selector).replace(r"\\ ", r"\\s*").replace(r"\ ", r"\\s+")
        match = re.search(pattern, solution, flags=re.I)
        if match is None:
            raise RuntimeError(f"selector not found: {selector!r}")
        pos = match.start()
    for start, end in paragraphs(solution):
        if start <= pos < end:
            return start, end
    raise RuntimeError(f"selector outside paragraph: {selector!r}")


def problem_key(index: str) -> str:
    year, side, number = index.split("-")
    return f"putnam_{year}_{side.lower()}{number}"


def build_row(spec: dict, sequence: int, source: dict, manifest: dict, *, is_primary: bool) -> dict:
    index = spec["problem"]
    solution = source["solution"]
    start, end = locate(solution, spec["selector"])
    span = solution[start:end]
    raw_path = DATASET / f"{index}.json"
    raw = raw_path.read_bytes()
    source_path = f"dataset/{index}.json"
    if manifest["source_path"] != source_path:
        raise RuntimeError(f"manifest path mismatch for {index}")
    if manifest["source_size_bytes"] != len(raw) or manifest["source_blob_sha1"] != git_blob(raw):
        raise RuntimeError(f"manifest blob mismatch for {index}")

    statement = spec.get("statement")
    accepted = is_primary or spec["disposition"] == "accepted_edge"
    disposition = "accepted_edge" if is_primary else spec["disposition"]
    relation = spec.get("relation")
    if accepted and (not statement or not relation):
        raise RuntimeError(f"accepted candidate lacks proposition/relation: {index}")
    slug = "primary-key-proposition" if is_primary else spec["slug"]
    candidate_key = f"putnamgap-onehop/{problem_key(index)}/{sequence:02d}-{slug}"
    target_kind = "claim" if is_primary else spec.get("kind", "claim")
    target_status = "proved" if is_primary else spec.get("status")

    if accepted and relation in {"standard_solution_uses", "direct_prerequisite"}:
        independent_summary = f"The standard solution uses the proposition labeled '{spec['label']}' at the bound proof-step span to derive the seed result."
    elif accepted:
        independent_summary = f"The bound source span explicitly supports a proposition-level {relation} relation from the seed to the independently stated target labeled '{spec['label']}'."
    else:
        independent_summary = f"The bound occurrence labeled '{spec['label']}' was reviewed but does not establish a distinct proposition-level edge."

    row = {
        "schema_version": SHARD_SCHEMA,
        "review_shard": "1962-1977",
        "candidate_key": candidate_key,
        "problem_key": problem_key(index),
        "source_problem_id": index,
        "source_binding": {
            "repository": "https://github.com/YurenHao0426/PutnamGAP",
            "commit": COMMIT,
            "tree": TREE,
            "path": source_path,
            "git_blob_sha1": manifest["source_blob_sha1"],
            "file_sha256": sha(raw),
            "file_size_bytes": len(raw),
            "solution_locator": {
                "json_pointer": "/solution",
                "solution_text_sha256": sha(solution.encode("utf-8")),
                "decoded_char_start": start,
                "decoded_char_end_exclusive": end,
                "proof_step_span_sha256": sha(span.encode("utf-8")),
            },
            "rights_id": "putnamgap-canonical-solution-maa-reference-only",
        },
        "discovery": {
            "method": "mandatory_key_proposition_selection" if is_primary else "explicit_relation_signal_review",
            "signal_class": "reviewer_selected_key_lemma_identity_or_inequality" if is_primary else slug,
            "candidate_occurrence_index": sequence,
        },
        "proposed_relation_type": relation,
        "target": {
            "kind": target_kind,
            "normalized_label": spec["label"],
            "independently_written_statement": statement,
            "statement_sha256": sha(statement.encode("utf-8")) if statement else None,
            "claim_kind": "theorem" if target_kind == "claim" and target_status == "proved" else ("open_problem" if target_status in {"open", "partial"} else None),
            "material_status": target_status,
            "citation": spec.get("citation") if not is_primary else None,
            "parent_5_5_exact_join": {
                "status": "no_exact_match_established",
                "stage_claim_id": None,
                "variant_id": None,
                "basis": "No exact independently written statement-text or exact formal-type equality was established; names and topics were not treated as identity evidence.",
            },
        },
        "evidence": {
            "independently_written_summary": independent_summary,
            "relation_assertion_origin": "independently_written_reviewed_summary",
            "source_wording_redistributed": False,
            "verbatim_source_text_stored": False,
            "proof_step_use_verified": bool(accepted and relation in {"standard_solution_uses", "direct_prerequisite"}),
            "proposition_level": bool(accepted),
        },
        "disposition": disposition,
        "reason_code": "reviewed_direct_proposition_relation" if accepted else spec["reason"],
        "review_anomaly_codes": sorted(set(spec.get("anomalies", []))),
        "review": {
            "reviewer_id": REVIEWER,
            "reviewed_as_of": REVIEW_DATE,
            "manual_statement_review": True,
            "manual_relation_review": True,
            "notes": "The relation summary and target statement are independently written; the copyrighted solution wording is represented only by locators and hashes.",
        },
    }
    row["row_sha256"] = sha(canonical(row))
    return row


def load_manifest() -> dict[str, dict]:
    rows = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        rows[row["index"]] = row
    return rows


def main() -> None:
    manifests = load_manifest()
    specs_by_problem = {spec["problem"]: spec for spec in PRIMARY}
    expected = {f"{year}-{side}-{n}" for year in range(1962, 1970) for side in "AB" for n in range(1, 7)}
    if set(specs_by_problem) != expected or len(PRIMARY) != 96:
        raise RuntimeError(f"primary coverage mismatch: missing={sorted(expected-set(specs_by_problem))} extra={sorted(set(specs_by_problem)-expected)}")

    extras_by_problem: dict[str, list[dict]] = {}
    for item in EXTRAS:
        extras_by_problem.setdefault(item["problem"], []).append(item)

    rows = []
    for index in sorted(expected):
        path = DATASET / f"{index}.json"
        source = json.loads(path.read_text(encoding="utf-8"))
        if source.get("index") != index or not source.get("solution"):
            raise RuntimeError(f"source row malformed: {index}")
        sequence = 1
        rows.append(build_row(specs_by_problem[index], sequence, source, manifests[index], is_primary=True))
        for item in extras_by_problem.get(index, []):
            sequence += 1
            rows.append(build_row(item, sequence, source, manifests[index], is_primary=False))

    accepted = [row for row in rows if row["disposition"] == "accepted_edge"]
    covered = {row["problem_key"] for row in accepted}
    if covered != {problem_key(item) for item in expected}:
        raise RuntimeError("accepted edge seed coverage is incomplete")
    if any(row["evidence"]["source_wording_redistributed"] or row["evidence"]["verbatim_source_text_stored"] for row in rows):
        raise RuntimeError("rights boundary violated")

    half_path = OUT_DIR / "_1962-1969.partial.jsonl"
    half_payload = b"".join(canonical(row) + b"\n" for row in rows)
    half_path.write_bytes(half_payload)
    summary = {
        "schema_version": "awesome-theorems/putnam-onehop-review-shard-summary/5.6",
        "review_shard": "1962-1969-partial",
        "source_commit": COMMIT,
        "source_tree": TREE,
        "parent_release_root_sha256": PARENT_ROOT,
        "counts": {
            "seed_problem_keys": len(expected),
            "candidate_occurrences": len(rows),
            "accepted_edges": len(accepted),
            "rejected_candidates": len(rows) - len(accepted),
            "accepted_edge_seed_coverage": len(covered),
            "missing_accepted_edge_seed_keys": 0,
            "by_relation_type": dict(sorted(Counter(row["proposed_relation_type"] for row in accepted).items())),
            "by_disposition": dict(sorted(Counter(row["disposition"] for row in rows).items())),
            "anomaly_occurrences": sum(bool(row["review_anomaly_codes"]) for row in rows),
        },
        "rights": {
            "solution_text_redistributed": False,
            "verbatim_trigger_stored": False,
            "repository_rows_contain_only_locators_hashes_and_independent_summaries": True,
        },
        "output": {"path": str(half_path.relative_to(REPO)), "row_count": len(rows), "sha256": sha(half_payload)},
        "findings": [],
    }
    summary["authority_sha256"] = sha(canonical(summary))
    (OUT_DIR / "_1962-1969.partial.summary.json").write_bytes(canonical(summary) + b"\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
