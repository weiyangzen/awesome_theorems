#!/usr/bin/env python3
"""Build or verify the candidate-only Putnam seed review for 1988--1992.

The 60 review rows are evidence-bound benchmark seeds.  They do not allocate
catalog IDs, mutate a release, or grant theorem/conjecture credit.  Original
MAA problem and solution prose is read only from the pinned PutnamGAP checkout
and is never emitted.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata
from typing import Any, Mapping, Sequence


REPO = Path(__file__).resolve().parents[4]
RAW_REPO = Path(os.environ.get(
    "PUTNAM_SEED_REVIEW_SOURCE_1988_1992", "/tmp/putnamgap-audit.uYDPao"))
PB_ROOT = REPO / "Docs/catalog/v5/curation/putnambench_v5_6"
OUT_ROOT = PB_ROOT / "seed-reviews"
OUTPUT = OUT_ROOT / "1988-1992.jsonl"
SUMMARY = OUT_ROOT / "1988-1992-summary.json"
RECEIPT = OUT_ROOT / "1988-1992-receipt.json"

FULL_INVENTORY = PB_ROOT / "Full_Putnam_Source_Inventory_v5_6.json"
FULL_CANDIDATES = PB_ROOT / "Full_Putnam_Source_Candidates_v5_6.jsonl"
FULL_SEEDS = PB_ROOT / "Full_Putnam_Seed_Problems_v5_6.jsonl"
LOCATORS = PB_ROOT / "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl"
PB_INVENTORY = PB_ROOT / "PutnamBench_Source_Inventory_v5_6.json"
PB_PROBLEMS = PB_ROOT / "PutnamBench_Source_Problems_v5_6.jsonl"
PB_HEADERS = PB_ROOT / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
PARENT = REPO / "Docs/catalog/v5/releases/5.5/Claim_Catalog.json"

PUTNAM_REPOSITORY = "https://github.com/YurenHao0426/PutnamGAP"
PUTNAM_COMMIT = "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
PUTNAM_TREE = "0f55aee4f4b911e767785a7c5977fbe36f58dbbe"
REVIEW_AS_OF = "2026-08-10"
SCHEMA_ROW = "awesome-theorems/putnam-seed-claim-review/5.6"
SCHEMA_SUMMARY = "awesome-theorems/putnam-seed-claim-review-summary/5.6"
SCHEMA_RECEIPT = "awesome-theorems/putnam-seed-claim-review-receipt/5.6"


class BuildError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def encoded(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop(field, None)
    result[field] = digest(canonical(result))
    return result


def verify_seal(value: Mapping[str, Any], field: str, label: str) -> None:
    observed = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    require(observed == digest(canonical(payload)), f"{label} self-seal drifted")


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def file_binding(path: Path, rows: int) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": relative(path), "rows": rows,
        "sha256": digest(payload), "size_bytes": len(payload),
    }


def payload_binding(path: Path, payload: bytes, rows: int) -> dict[str, Any]:
    return {
        "path": relative(path), "rows": rows,
        "sha256": digest(payload), "size_bytes": len(payload),
    }


def read_document(path: Path, label: str) -> tuple[bytes, dict[str, Any]]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n") and payload.count(b"\n") == 1,
            f"{label} is not one JSON line")
    value = json.loads(payload)
    require(isinstance(value, dict), f"{label} is not an object")
    require(payload == encoded(value), f"{label} is not canonical JSON")
    return payload, value


def read_rows(path: Path, label: str) -> tuple[bytes, list[tuple[int, bytes, dict[str, Any]]]]:
    payload = path.read_bytes()
    rows: list[tuple[int, bytes, dict[str, Any]]] = []
    for number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{label} line {number} is empty")
        row = json.loads(raw)
        require(isinstance(row, dict), f"{label} line {number} is not an object")
        require(raw == canonical(row), f"{label} line {number} is not canonical JSON")
        if "row_sha256" in row:
            check = dict(row)
            observed = check.pop("row_sha256")
            require(observed == digest(canonical(check)),
                    f"{label} line {number} row seal drifted")
        rows.append((number, raw, row))
    return payload, rows


def semantic_key(statement: str) -> str:
    text = unicodedata.normalize("NFKC", statement).casefold()
    text = re.sub(r"\s+", " ", text).strip()
    return "putnam-seed-semantic-v1/" + digest(text.encode("utf-8"))


def set_digest(values: Sequence[str]) -> str:
    return digest(canonical(sorted(values)))


def expected_keys() -> list[str]:
    return [
        f"putnam_{year}_{section}{number}"
        for year in range(1988, 1993)
        for section in ("a", "b")
        for number in range(1, 7)
    ]


def problem_key(index: str) -> str:
    year, section, number = index.split("-")
    return f"putnam_{year}_{section.lower()}{number}"


FRAGMENTS: dict[str, dict[str, Any]] = {}


def add(
    index: str,
    statement: str,
    method: str,
    *,
    visibility: str = "proof_claim_no_separate_answer",
    validity: str = "valid_as_scoped",
    anomalies: tuple[str, ...] = (),
    defect: str | None = None,
    shape: str = "single",
    multipart: bool = False,
    multipart_detail: str | None = None,
) -> None:
    key = problem_key(index)
    require(key not in FRAGMENTS, f"duplicate fragment {key}")
    if validity == "valid_as_scoped":
        rationale = (
            "The pinned mathematical prompt is truth-apt as scoped, and its pinned "
            "solution supports this independently written statement and method summary."
        )
    else:
        rationale = (
            "The independently written statement makes the recorded source repair explicit; "
            "the pinned solution and frozen source cross-check support the repaired claim."
        )
    FRAGMENTS[key] = {
        "source_index": index,
        "problem_key": key,
        "anomaly_codes": list(anomalies),
        "proof_method_summary": method,
        "claim_review": {
            "alias_target_problem_key": None,
            "answer_visibility": visibility,
            "children": [],
            "claim_disposition": "theorem",
            "claim_shape": shape,
            "independent_english_statement": statement,
            "multipart_handling": {
                "all_parts_accounted_for": True,
                "detail": multipart_detail or (
                    "The source's related deliverables are represented together in one compound claim."
                    if multipart else
                    "The source poses one claim or computation, represented in full."
                ),
                "handling": "single_compound_claim" if multipart else "single_complete_claim",
                "source_has_multiple_parts": multipart,
            },
            "review_as_of": REVIEW_AS_OF,
            "review_rationale": rationale,
            "semantic_key": None,
            "source_claim_validity": validity,
            "source_defect_detail": defect,
            "statement_representation": "independently_written_review_statement",
            "truth_apt": True,
        },
    }


def split(
    index: str,
    children: tuple[tuple[str, str, str, str], ...],
    method: str,
    *,
    validity: str = "valid_as_scoped",
    anomalies: tuple[str, ...] = (),
    defect: str | None = None,
) -> None:
    key = problem_key(index)
    require(key not in FRAGMENTS, f"duplicate fragment {key}")
    child_rows = []
    for label, statement, visibility, distinction in children:
        child_rows.append({
            "child_id": f"putnamgap/{PUTNAM_COMMIT}/{index}/part-{label}",
            "part_label": label,
            "independent_english_statement": statement,
            "semantic_key": None,
            "answer_visibility": visibility,
            "distinction_basis": distinction,
        })
    FRAGMENTS[key] = {
        "source_index": index,
        "problem_key": key,
        "anomaly_codes": list(anomalies),
        "proof_method_summary": method,
        "claim_review": {
            "alias_target_problem_key": None,
            "answer_visibility": "not_applicable_split_parent",
            "children": child_rows,
            "claim_disposition": "split",
            "claim_shape": "split",
            "independent_english_statement": None,
            "multipart_handling": {
                "all_parts_accounted_for": True,
                "detail": f"All {len(children)} labeled source parts are represented by distinct child claims.",
                "handling": "split_into_exhaustive_children",
                "source_has_multiple_parts": True,
            },
            "review_as_of": REVIEW_AS_OF,
            "review_rationale": (
                "The source contains independently truth-apt labeled deliverables, so the review "
                "preserves them as exhaustive non-credit child identities."
            ),
            "semantic_key": None,
            "source_claim_validity": validity,
            "source_defect_detail": defect,
            "statement_representation": "independently_written_review_statement",
            "truth_apt": True,
        },
    }


# 1988
add("1988-A-1",
    "The planar set satisfying |x|-|y|<=1 and |y|<=1 consists of four reflected trapezoidal pieces and has area 6.",
    "In the first quadrant the inequalities describe a unit square together with a right triangle of area one half. Reflection in both axes multiplies that area by four.",
    visibility="explicit_answer_in_statement", shape="source_named_compound", multipart=True,
    multipart_detail="The geometric description requested for the sketch and the numerical area are retained together.")
add("1988-A-2",
    "For f(x)=exp(x^2), the false product-rule equation (fg)'=f'g' nevertheless has a nonzero differentiable solution on an open interval: on any interval avoiding 1/2, g(x)=C exp(x)|2x-1|^(1/2) works for every nonzero constant C.",
    "Expanding the derivative reduces the equation to (2x-1)g'=2xg. Separation away from the singular point and integration give the displayed family, which verifies the requested existence.",
    visibility="explicit_answer_in_statement")
add("1988-A-3",
    "The series sum over n>=1 of ((csc(1/n))/n-1)^x converges exactly for real x>1/2.",
    "The Taylor expansion of sine makes the positive base asymptotic to 1/(6n^2). Limit comparison reduces convergence to that of the p-series with exponent 2x.",
    visibility="classification_complete")
split("1988-A-4", (
    ("a", "Every three-coloring of the Euclidean plane has two equally colored points exactly one unit apart.", "explicit_answer_in_statement", "This child records the affirmative three-color conclusion."),
    ("b", "There is a nine-coloring of the Euclidean plane with no equally colored pair at distance one.", "explicit_answer_in_statement", "This child records the negative nine-color conclusion and its construction."),
),
    "For three colors, linked equilateral triangles force a same-colored pair at a second prescribed distance and then a unit-distance contradiction. For nine colors, use a sufficiently fine square grid and color cells periodically by both coordinates modulo three; cells of one color are either too close internally or too far apart to realize distance one.")
add("1988-A-5",
    "The unique function f from the positive reals to themselves satisfying f(f(x))=6x-f(x) for every x>0 is f(x)=2x.",
    "Iterates of an arbitrary x obey a second-order recurrence with characteristic roots 2 and -3. Positivity of every iterate eliminates the alternating -3 component, forcing f(x)=2x; substitution proves existence.",
    visibility="classification_complete")
add("1988-A-6",
    "An endomorphism of an n-dimensional vector space that has n+1 eigenvectors with every n linearly independent must be a scalar multiple of the identity.",
    "Omitting each eigenvector in turn gives n+1 eigenbases. The invariant trace equals the sum of eigenvalues in each omitted basis, so all n+1 eigenvalues coincide; any one eigenbasis then makes the operator scalar.",
    visibility="explicit_answer_in_statement")
add("1988-B-1",
    "Every composite positive integer is xy+xz+yz+1 for some positive integers x,y,z.",
    "Given a factorization N=ab with a,b>=2, take x=a-1, y=b-1, and z=1; the expression becomes (x+1)(y+1)=ab.")
add("1988-B-2",
    "For real x and y>=0, y(y+1)<=(x+1)^2 always implies y(y-1)<=x^2.",
    "The conclusion is immediate for y<=1. For y>1, separate the ranges of x around y-1/2; one range follows by subtracting 2y from the hypothesis, and the other by direct comparison with (y-1/2)^2.",
    visibility="explicit_answer_in_statement")
add("1988-B-3",
    "If r_n=min{|c-d sqrt(3)|: c,d are nonnegative integers and c+d=n}, then the smallest g>0 satisfying r_n<=g for every n is (1+sqrt(3))/2.",
    "For fixed n the signed quantities form an arithmetic progression of step 1+sqrt(3) crossing zero, so the nearest term is at most half a step away. Density of irrational rotations makes these nearest distances approach the half-step bound, proving sharpness.",
    visibility="explicit_answer_in_statement")
add("1988-B-4",
    "Whenever a series of positive terms sum a_n converges, the series sum a_n^(n/(n+1)) also converges.",
    "Split indices according as a_n is at least 2^(-(n+1)). In the first case the transformed term is at most 2a_n, and in the second it is at most 2^(-n), giving a summable majorant.")
add("1988-B-5",
    "The (2n+1)-square skew-symmetric matrix whose first n subdiagonals are 1 and whose other lower-triangular entries are -1 has rank 2n for every positive n.",
    "Gaussian elimination splits off a nonsingular 2-by-2 block and leaves the negative of the matrix for n-1, proving the rank recursively. Odd-dimensional skew-symmetry supplies the matching upper bound.",
    visibility="explicit_answer_in_statement")
add("1988-B-6",
    "Infinitely many integer pairs preserve triangular numbers in both directions: for each k>=1, a=9^k and b=(9^k-1)/8 satisfy that at+b is triangular exactly when the positive integer t is triangular.",
    "The identity T_(3n+1)=9T_n+1 and the possible triangular residues modulo nine show that t is triangular exactly when 9t+1 is. Iterating this affine equivalence gives the stated family.",
    visibility="explicit_answer_in_statement",
    defect="The mathematical prompt is intact but is followed by stray TeX document terminators in the pinned question field.")

# 1989
add("1989-A-1",
    "Among decimal integers whose digits alternate 1 and 0 and whose first and last digits are 1, exactly one is prime: 101.",
    "If the numeral has k ones, multiplication by 99 gives 10^(2k)-1=(10^k-1)(10^k+1). For k>2 this forces compositeness, while the remaining nontrivial case is 101.",
    visibility="explicit_answer_in_statement")
add("1989-A-2",
    "For positive a,b, the integral of exp(max{b^2x^2,a^2y^2}) over 0<=x<=a and 0<=y<=b equals (exp(a^2b^2)-1)/(ab).",
    "Split the rectangle along ay=bx. On the two triangular parts the maximum is a single square term, and elementary substitutions reduce their sum to one exponential antiderivative.",
    visibility="explicit_answer_in_statement")
add("1989-A-3",
    "Every complex zero of 11z^10+10iz^9+10iz-11 lies on the unit circle.",
    "Rearrange to z^9=(11-10iz)/(11z+10i). A comparison of squared moduli contradicts either |z|>1 or |z|<1, so equality is forced.")
add("1989-A-4",
    "For each irrational alpha in (0,1), an almost-surely finite fair-coin game can give one player winning probability alpha.",
    "Interpret successive tosses as binary digits of a uniform point of [0,1]. Stop when its current dyadic interval lies wholly on one side of alpha; equality has probability zero, and the outcome below alpha has probability alpha.",
    visibility="explicit_answer_in_statement")
add("1989-A-5",
    "There is a constant A>0 independent of m such that, from every interior point of a regular (2m+1)-gon in the unit circle, two distinct vertices have distances differing by less than 1/m-A/m^3.",
    "Order all vertex distances. Their range is at most the longest vertex chord, 2cos(pi/(4m+2)), so one of the 2m successive gaps is at most that range divided by 2m. A uniform cosine estimate yields the fixed cubic improvement.")
add("1989-A-6",
    "Over the field with two elements, let alpha=sum_(n>=0) a_n x^n, where a_n=1 exactly when every run of zeroes in the binary expansion of n has even length. Then alpha^3+x alpha+1=0.",
    "Multiply by alpha and use characteristic-two squaring. Recurrences obtained by appending a binary one, one zero, or two zeroes make every coefficient of alpha^4+x alpha^2+alpha vanish.")
add("1989-B-1",
    "A uniformly thrown dart in a square is nearer the center than every edge with probability (4sqrt(2)-5)/3.",
    "Normalize the square to [-1,1]^2. Center-versus-edge comparisons give parabolic boundaries; symmetry reduces the favorable area to eight copies of a region integrated between a diagonal and one parabola.",
    visibility="explicit_answer_in_statement")
add("1989-B-2",
    "Every nonempty left- and right-cancellative semigroup in which {a^n:n>=1} is finite for each a is a group.",
    "Repeated powers of an element produce an idempotent power. Cancellation shows that idempotent is a global two-sided identity, and a preceding power supplies a two-sided inverse for each element.",
    visibility="explicit_answer_in_statement")
split("1989-B-3", (
    ("a", "If f'(x)=-3f(x)+6f(2x), |f(x)|<=exp(-sqrt(x)), and mu_n=integral_0^infinity x^n f(x) dx, then mu_n=(n!/3^n)(product_(j=1)^n(1-2^(-j)))^(-1)mu_0.", "explicit_answer_in_statement", "This child is the requested exact moment formula."),
    ("b", "Under the same hypotheses, mu_n 3^n/n! converges to mu_0/product_(j=1)^infinity(1-2^(-j)), and this limit is zero only when mu_0=0.", "explicit_answer_in_statement", "This child is the separate convergence and nonvanishing conclusion."),
),
    "Multiply the differential-functional equation by x^n and integrate by parts; the decay bound removes boundary terms, and rescaling the f(2x) integral gives a first-order recurrence for the moments. Iteration yields a finite product whose infinite limit is positive.")
add("1989-B-4",
    "A countably infinite set can have uncountably many nonempty subsets whose pairwise intersections are finite.",
    "For every real alpha choose a sequence of distinct rationals converging to alpha. Two sequences having infinitely many common terms would share a convergent subsequence and hence the same limit.",
    visibility="explicit_answer_in_statement")
add("1989-B-5",
    "For a cyclic trapezoid in the unit circle with parallel-side lengths s_1,s_2 and diagonal intersection at nonzero distance d from the center, the supremum of (s_1-s_2)/d is 2; it is attained exactly when the diagonals are perpendicular and s_1>s_2.",
    "Place the parallel chords horizontally and write one diagonal as y=mx+e. Vieta's formula expresses the ratio as 4m sign(e)/(m^2+1); the inequality m^2+1>=2m gives the bound and its exact equality conditions.",
    visibility="classification_complete", shape="source_named_compound", multipart=True,
    multipart_detail="The sharp supremum and all equality cases form one complete extremal classification.")
add("1989-B-6",
    "For ordered uniform points 0<x_1<...<x_n<1, with x_0=0 and x_(n+1)=1, the expected sum of (x_(i+1)-x_i)f(x_(i+1)) equals integral_0^1 f(t)(1-(1-t)^n)dt for every continuous f with f(1)=0; thus P(t)=1-(1-t)^n, a degree-n polynomial taking values in [0,1] on [0,1].",
    "Integrate the gap terms over the order-statistics simplex. Fixing a right endpoint t produces binomial weights, whose sum over the possible preceding counts is 1-(1-t)^n.",
    visibility="explicit_answer_in_statement",
    defect="The mathematical prompt is intact but is followed by stray TeX document terminators in the pinned question field.")

# 1990
add("1990-A-1",
    "The recurrence T_0=2, T_1=3, T_2=6 and T_n=(n+4)T_(n-1)-4nT_(n-2)+(4n-8)T_(n-3) has the closed form T_n=n!+2^n.",
    "Substitute n!+2^n into the recurrence and verify the three initial values; uniqueness for a third-order recurrence proves the formula.",
    visibility="explicit_answer_in_statement")
add("1990-A-2",
    "There are sequences of nonnegative integers n_k,m_k for which cube_root(n_k)-cube_root(m_k) tends to sqrt(2).",
    "Successive cube roots have gaps tending to zero. For a large base m, the increasing mesh cube_root(m+j)-cube_root(m) crosses any fixed positive target, so suitable mesh points approach sqrt(2).",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question retains only its final expression; the review restores the yes/no request asking whether sqrt(2) is a sequential limit of such differences.")
add("1990-A-3",
    "Every convex pentagon with integer-coordinate vertices and no three collinear has area at least 5/2.",
    "Assume a smaller lattice pentagon of least area. Two of its five vertices have the same coordinate parity, so their midpoint is a lattice point; convex replacement arguments then contradict minimality, while lattice polygon areas occur in half-integer units.",
    validity="ocr_repair_explicit", anomalies=("question_opening_truncated",),
    defect="The pinned question begins inside a parenthetical clause; the review restores the convex lattice-pentagon hypotheses.")
add("1990-A-4",
    "A punch that removes exactly those plane points at irrational distance from its center needs exactly three placements to remove the entire plane.",
    "Two centers always leave points having rational distances to both. Their full survivor set is a countable union of finite circle intersections; choose a third center at irrational distance from every survivor.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the opening definition of the movable paper punch; the review restores that setup.")
add("1990-A-5",
    "For equally sized square matrices, ABAB=0 does not in general imply BABA=0.",
    "An explicit 3-by-3 pair supplied by the pinned solution is multiplied in both orders: one alternating fourth product vanishes and the reverse product does not.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question drops the introduction of the two same-size square matrices and the start of the implication question.")
add("1990-A-6",
    "There are 17711 ordered pairs (S,T) of subsets of {1,...,10} for which every s in S exceeds |T| and every t in T exceeds |S|.",
    "Count the analogous objects on variable finite initial segments. Removing the largest available element gives Pascal-type recurrences and identifies the diagonal count with F_22=17711.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question starts with an orphaned fragment from a missing cardinality definition; the review restores the complete admissible-pair problem directly.")
add("1990-B-1",
    "The continuously differentiable real functions satisfying f(x)^2=integral_0^x(f(t)^2+f'(t)^2)dt+1990 for every real x are exactly f(x)=sqrt(1990)exp(x) and f(x)=-sqrt(1990)exp(x).",
    "Differentiate to obtain (f-f')^2=0, hence f=C exp(x). Evaluation at zero gives C^2=1990, and both signs satisfy the original identity.",
    visibility="classification_complete", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the request and the regularity and domain hypotheses; the review restores the full classification problem.")
add("1990-B-2",
    "For real x,z with |x|<1 and |z|>1, if P_j=product_(k=0)^(j-1)(1-zx^k)/product_(k=1)^j(z-x^k), then 1+sum_(j>=1)(1+x^j)P_j=0.",
    "Induction factors the nth partial sum as product_(k=1)^n(1-zx^k)/(z-x^k). Its successive factors approach 1/z in modulus below one, so the product tends to zero.",
    validity="ocr_repair_explicit", anomalies=("question_opening_truncated",),
    defect="The pinned question loses the domain assumptions and proof directive; the review restores |x|<1 and |z|>1.")
add("1990-B-3",
    "Any set of more than 50387 two-by-two integer matrices whose entries are integer squares not exceeding 200 contains two commuting matrices.",
    "There are 15 choices per entry. A pairwise noncommuting set contains at most one diagonal matrix and at most one scalar multiple of the all-ones matrix; moreover a fixed commuting pair lies outside those two families, forcing one additional omission. Inclusion-exclusion leaves at most 50387 matrices.",
    validity="ocr_repair_explicit", anomalies=("question_opening_truncated",),
    defect="The pinned question omits the introduction of the set and the 2-by-2 matrix size; the review restores both.")
add("1990-B-4",
    "If a finite group G of order n is generated by a and b, there is a cyclic sequence g_1,...,g_(2n) in which each group element occurs twice and each next term is obtained by right multiplication by a or b.",
    "Use the directed Cayley multigraph having arcs g->ga and g->gb. Generation gives connectivity and every vertex has equal indegree and outdegree two, so an Euler circuit lists the required starting vertices.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question loses the finite-group introduction and begins with the final generator name; the review restores it.")
add("1990-B-5",
    "There is an infinite sequence of nonzero real numbers a_0,a_1,... such that each polynomial sum_(j=0)^n a_jx^j has exactly n distinct real roots.",
    "Inductively add a sufficiently small nonzero leading term to a real-rooted polynomial. Alternating signs at interlacing test points preserve the old roots, while the leading sign forces one new outer root.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the existential opening and begins inside the coefficient description; the review restores it.")
add("1990-B-6",
    "For each direction K and nonempty compact convex plane set S, take the two support lines parallel to K and the central band whose half-width is t/2 times their separation. The smallest universal t for which S meets all these bands simultaneously is 1/3.",
    "A triangle proves that no smaller value works. For t=1/3, the centroid of a convex body lies in the middle third of its width in every direction, so it belongs to every band.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated", "support_line_direction_subscript_ocr"),
    defect="The pinned question omits the definition of S and prints K_1 where the fixed direction K is required; the review restores a nonempty compact convex S and the consistent direction.")

# 1991
add("1991-A-1",
    "Start with the rectangle having corners (0,0), (2,0), (0,3), and (2,3), and rotate it clockwise by a quarter-turn successively about (2,0), (5,0), (7,0), and (10,0). The trajectory of the point initially at (1,1) forms the upper boundary of a region over the x-axis having area 6+7pi/2.",
    "Track the point after each rotation, then partition the region under its circular arcs into elementary right triangles and quarter-disks of radii sqrt(2) and sqrt(5). Their areas sum to the stated value.",
    visibility="explicit_answer_in_statement")
add("1991-A-2",
    "If distinct real n-by-n matrices A and B satisfy A^3=B^3 and A^2B=B^2A, then A^2+B^2 is not invertible.",
    "Direct expansion gives (A^2+B^2)(A-B)=A^3-B^3-A^2B+B^2A=0. Since A-B is nonzero, the left factor has a nontrivial kernel.",
    visibility="explicit_answer_in_statement")
add("1991-A-3",
    "A real polynomial of degree n>=2 has n distinct ordered real zeros r_i and derivative zero at every midpoint (r_i+r_(i+1))/2 exactly when n=2; equivalently, the solutions are all nonzero scalar multiples of (x-r_1)(x-r_2) with r_1<r_2.",
    "Quadratics are symmetric about the midpoint of their two zeros. For n>2, evaluate the logarithmic derivative p'/p at the midpoint of the final two roots: their reciprocal terms cancel, while all earlier-root terms have the same positive sign, so p' cannot vanish there.",
    visibility="classification_complete")
add("1991-A-4",
    "There is a sequence of closed disks whose centers have no finite accumulation point, whose total area is finite, and whose union meets every line in the plane.",
    "Choose radii a_i with divergent sum but convergent sum of squares, and place disks of radius a_i cumulatively along all four coordinate rays. They cover both coordinate axes, hence meet every line, while their centers escape and their total area converges.",
    visibility="explicit_answer_in_statement")
add("1991-A-5",
    "For 0<=y<=1, the maximum of integral_0^y sqrt(x^4+(y-y^2)^2) dx is 1/3.",
    "Use sqrt(u^2+v^2)<=u+v with u=x^2 and v=y-y^2. The resulting bound y^2-(2/3)y^3 increases to 1/3, and equality holds at y=1.",
    visibility="explicit_answer_in_statement")
add("1991-A-6",
    "Let A(n) count compositions a_1+...+a_r=n satisfying a_i>a_(i+1)+a_(i+2) for 1<=i<=r-2 and, when r>=2, a_(r-1)>a_r. Define g_1=1, g_2=2, and g_j=g_(j-1)+g_(j-2)+1. Let B(n) count nonincreasing partitions into the g_j that contain every allowed part through their largest part. Then A(n)=B(n) for all n>=1.",
    "Apply an upper-triangular unimodular change of variables taking the strict composition gaps to positive multiplicities. The identity relating its columns to the g_j converts the total sum condition into a partition with positive multiplicity for every part up to the largest, giving a bijection.")
add("1991-B-1",
    "For S(n)=n-floor(sqrt(n))^2 and a_(k+1)=a_k+S(a_k), the sequence starting at a positive integer A is eventually constant exactly when A is a perfect square.",
    "A square is immediately fixed. Between consecutive squares, the next term is larger, remains nonsquare by a parity argument, and lies before the square after next; hence a nonsquare orbit can never become constant.",
    visibility="classification_complete")
add("1991-B-2",
    "Let f and g be differentiable nonconstant real functions on the real line, and put h(x)=f(x)+i g(x). If h converts addition into multiplication, h(x+y)=h(x)h(y), and f'(0)=0, then f(x)^2+g(x)^2=1 for every real x.",
    "Combine the functions as h=f+ig, so h(x+y)=h(x)h(y). Differentiation at zero gives h'=ic h for a real c; nonconstancy rules out h=0, and h(0)^2=h(0) forces h(0)=1, so |h|=1.")
add("1991-B-3",
    "There is a real L such that every integer-sided m-by-n rectangle with m,n>L can be tiled by 4-by-6 and 5-by-7 rectangles, allowing quarter-turn rotations and without overlapping interiors.",
    "First combine tiles into strips of heights 20, 35, and 42 with all sufficiently large widths, using the numerical semigroup theorem. Choose a constructible height coprime to 42, then apply the same theorem in the vertical direction.",
    visibility="explicit_answer_in_statement")
add("1991-B-4",
    "For every odd prime p, sum_(j=0)^p binom(p,j)binom(p+j,j) is congruent modulo p^2 to 2^p+1.",
    "Interpret the sum as the coefficient of x^p in (2+x)^p(1+x)^p. All interior coefficient products contain p^2, leaving only the two endpoint contributions modulo p^2.")
add("1991-B-5",
    "For an odd prime p, the intersection of the square residues in Z_p with the residues y^2+1 has exactly ceil(p/4) elements.",
    "Count solutions of x^2-y^2=1 by the invertible substitution (u,v)=(x+y,x-y), which gives p-1 pairs with uv=1. Quotient by the sign fibers, treating x=0 or y=0 separately according as -1 is a square.",
    visibility="explicit_answer_in_statement")
add("1991-B-6",
    "For positive a,b, the largest c>=0 such that a^x b^(1-x)<=a sinh(ux)/sinh(u)+b sinh(u(1-x))/sinh(u) for every 0<x<1 and 0<|u|<=c is |log(a/b)|.",
    "The right side is even in u, and sinh(alpha u)/sinh(u) decreases for positive u when 0<alpha<1. Equality occurs at u=|log(a/b)|; monotonicity gives the inequality below this threshold and failure above it.",
    visibility="explicit_answer_in_statement",
    defect="The mathematical prompt is intact but is followed by stray TeX itemize and document terminators in the pinned question field.")

# 1992: every pinned question lost its opening clause; each repair is explicit.
add("1992-A-1",
    "The only integer-valued function on the integers satisfying f(f(n))=n, f(f(n+2)+2)=n for every n, and f(0)=1 is f(n)=1-n.",
    "The displayed function verifies all conditions. Conversely, involutivity applied to the second identity yields f(n+2)=f(n)-2; the initial values f(0)=1 and f(1)=0 determine both parity classes.",
    visibility="classification_complete", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question begins after the requested formula and the subject 'integer-valued function'; the review restores both from the solution and frozen formal headers.")
add("1992-A-2",
    "Let C(alpha) be the coefficient of x^1992 in the power series of (1+x)^alpha at zero. Then integral_0^1 C(-y-1) sum_(k=1)^1992 1/(y+k) dy equals 1992.",
    "Write C(-y-1) as product_(k=1)^1992(y+k)/1992!. Multiplication by the reciprocal sum is the derivative of that product, so the integral is its endpoint difference.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the definition of C(alpha); the review restores the coefficient-of-x^1992 definition.")
add("1992-A-3",
    "For a fixed positive integer m, positive triples (n,x,y) with gcd(n,m)=1 and (x^2+y^2)^m=(xy)^n exist exactly when m=2k is even; then the unique triple is (n,x,y)=(2k+1,2^k,2^k).",
    "Remove gcd(x,y) and use coprimality to force the reduced factors to be one. The equation becomes a pure power of two; valuation and gcd(n,m)=1 force m=2k, n=2k+1, and the common value x=y=2^k.",
    visibility="classification_complete", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the fixed positive integer m and the request to find all triples; the review restores that scope.")
add("1992-A-4",
    "If f is infinitely differentiable on the reals and f(1/n)=n^2/(n^2+1) for every positive n, then f^(k)(0)=0 for odd k and f^(k)(0)=(-1)^(k/2)k! for even positive k.",
    "Subtract 1/(1+x^2). The difference vanishes along 1/n tending to zero; iterated Rolle arguments force every derivative of the difference at zero to vanish. Read the remaining derivatives from the geometric power series.",
    visibility="classification_complete", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the smoothness and real-domain introduction for f; the review restores it.")
add("1992-A-5",
    "Let a_n be zero or one according as the binary expansion of positive n has an even or odd number of ones. No three consecutive blocks of equal positive length in this sequence are identical.",
    "Use a_(2n)=a_n and a_(2n+1)=1-a_n. A minimal repeated triple cannot have odd block length by forced alternation; if the length is even, extracting even-indexed terms produces a smaller repeated triple.",
    validity="ocr_repair_explicit", anomalies=("question_opening_truncated",),
    defect="The pinned question omits the quantifier over positive n and the definition's opening clause; the review restores the binary-parity sequence.")
add("1992-A-6",
    "Four independent uniform points on a sphere form a tetrahedron containing the sphere's center with probability 1/8.",
    "Condition on four unoriented lines through the center and choose independent endpoint signs. In general position the unique linear dependence contains the origin in the convex hull exactly when its four signed coefficients share a sign, which occurs for 2 of 16 sign choices.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the opening sentence choosing four random surface points; the review restores it.")
add("1992-B-1",
    "For n>=2 distinct real numbers S, let A_S contain the averages of every two distinct elements of S. The minimum possible size of A_S is 2n-3.",
    "Ordering S gives a strictly increasing chain of 2n-3 averages formed from the least and greatest elements. An arithmetic progression realizes exactly that many averages.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the definitions of S and A_S; the review restores them.")
add("1992-B-2",
    "For nonnegative n,k, if Q(n,k) is the coefficient of x^k in (1+x+x^2+x^3)^n, then Q(n,k)=sum_(j=0)^k binom(n,j)binom(n,k-2j), with out-of-range binomial coefficients zero.",
    "Factor the generating polynomial as (1+x^2)^n(1+x)^n and convolve the coefficient of x^(2j) in the first factor with that of x^(k-2j) in the second.",
    validity="ocr_repair_explicit", anomalies=("question_opening_truncated",),
    defect="The pinned question omits the nonnegative parameter range and the definition of Q(n,k); the review restores both.")
add("1992-B-3",
    "For a_0(x,y)=x and a_(n+1)(x,y)=(a_n(x,y)^2+y^2)/2, the set of real pairs for which the sequence converges has area 4+pi.",
    "By sign symmetry restrict to x,y>=0. Fixed-point analysis of w->(w^2+y^2)/2 shows convergence exactly when 0<=y<=1 and 0<=x<=1+sqrt(1-y^2); reflecting this region gives a 2-by-2 square plus two unit semicircles.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the introduction quantifying real pairs (x,y) before the recurrence; the review restores it.")
add("1992-B-4",
    "Let p be a nonzero polynomial of degree below 1992 and coprime to x^3-x. If the 1992nd derivative of p(x)/(x^3-x) is written as f(x)/g(x) with polynomials f,g, the smallest possible degree of f is 3984.",
    "Reduce p modulo x^3-x and use partial fractions at -1,0,1. After differentiation the numerator has three leading coefficients controlled by three nonzero residues; two can vanish simultaneously, giving degree 3984, but vanishing the third would force all residues to zero.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the definition and degree/coprimality hypotheses for p(x); the review restores them.")
add("1992-B-5",
    "Let D_n be the determinant of the (n-1)-by-(n-1) matrix with diagonal 3,4,...,n+1 and every off-diagonal entry one. Then D_n/n!=sum_(k=1)^n 1/k, so the set of these ratios for n>=2 is unbounded.",
    "Subtract the first row from all later rows and clear the first column with elementary column operations. The resulting upper-triangular determinant is n! times the nth harmonic sum, which diverges.",
    visibility="explicit_answer_in_statement", validity="ocr_repair_explicit",
    anomalies=("question_opening_truncated",),
    defect="The pinned question omits the sentence defining D_n and the determinant size; the review restores both.")
add("1992-B-6",
    "Let M be a set of real n-by-n matrices containing I, closed up to exactly one sign under products, pairwise commuting or anticommuting, and such that every A!=I anticommutes with some member. Then M has at most n^2 elements.",
    "First show A^2 is plus or minus I for every member. If more than n^2 matrices existed, choose a linear dependence with minimal support; translate it so I occurs, then use an anticommuting witness and add left- and right-multiplied relations to remove some but not all terms, contradicting minimality.",
    validity="ocr_repair_explicit", anomalies=("question_opening_truncated",),
    defect="The pinned question omits the introduction defining M as a set of real n-by-n matrices and ends with stray TeX document terminators; the review restores the missing scope.")


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(RAW_REPO), *args], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return result.stdout.strip()


def ngram_overlap(left: str, right: str, width: int = 14) -> bool:
    token = re.compile(r"[A-Za-z]+")
    a = [word.casefold() for word in token.findall(left)]
    b = [word.casefold() for word in token.findall(right)]
    if len(a) < width or len(b) < width:
        return False
    windows = {tuple(a[i:i + width]) for i in range(len(a) - width + 1)}
    return any(tuple(b[i:i + width]) in windows for i in range(len(b) - width + 1))


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def emit(path: Path, payload: bytes, check: bool) -> None:
    if check:
        require(path.is_file(), f"missing output {relative(path)}")
        require(path.read_bytes() == payload, f"byte drift in {relative(path)}")
    else:
        atomic_write(path, payload)


def build() -> tuple[bytes, bytes, bytes, dict[str, Any], dict[str, Any]]:
    require(set(FRAGMENTS) == set(expected_keys()),
            f"fragment grid mismatch missing={sorted(set(expected_keys())-set(FRAGMENTS))} extra={sorted(set(FRAGMENTS)-set(expected_keys()))}")
    require(run_git("rev-parse", "HEAD^{commit}") == PUTNAM_COMMIT,
            "PutnamGAP checkout commit drifted")
    require(run_git("rev-parse", "HEAD^{tree}") == PUTNAM_TREE,
            "PutnamGAP checkout tree drifted")
    require(run_git("status", "--porcelain") == "", "PutnamGAP checkout is dirty")

    _, full_inventory = read_document(FULL_INVENTORY, "full Putnam inventory")
    _, pb_inventory = read_document(PB_INVENTORY, "PutnamBench inventory")
    verify_seal(full_inventory, "authority_sha256", "full Putnam inventory")
    verify_seal(pb_inventory, "authority_sha256", "PutnamBench inventory")
    _, candidate_rows = read_rows(FULL_CANDIDATES, "full Putnam candidates")
    _, seed_rows = read_rows(FULL_SEEDS, "full Putnam seeds")
    _, locator_rows = read_rows(LOCATORS, "PutnamGAP locators")
    _, pb_problem_rows = read_rows(PB_PROBLEMS, "PutnamBench source problems")
    _, pb_header_rows = read_rows(PB_HEADERS, "PutnamBench formal headers")
    require(len(candidate_rows) == 1063, "full candidate row count drifted")
    require(len(seed_rows) == 768, "full seed row count drifted")
    require(len(locator_rows) == 1051, "PutnamGAP locator row count drifted")
    require(len(pb_problem_rows) == 675, "PutnamBench problem row count drifted")
    require(len(pb_header_rows) == 1724, "PutnamBench header row count drifted")

    candidates = {row["source_candidate_id"]: (number, raw, row)
                  for number, raw, row in candidate_rows}
    seeds = {row["problem_key"]: (number, raw, row)
             for number, raw, row in seed_rows}
    locators = {row["source_candidate_id"]: (number, raw, row)
                for number, raw, row in locator_rows}
    pb_problems = {row["problem_key"]: (number, raw, row)
                   for number, raw, row in pb_problem_rows}
    headers: dict[str, list[tuple[int, bytes, dict[str, Any]]]] = {}
    for number, raw, row in pb_header_rows:
        headers.setdefault(row["problem_key"], []).append((number, raw, row))

    output_rows: list[dict[str, Any]] = []
    for key in expected_keys():
        fragment = copy.deepcopy(FRAGMENTS[key])
        index = fragment.pop("source_index")
        require(fragment.pop("problem_key") == key, f"fragment key drift {key}")
        source_id = f"putnamgap/{PUTNAM_COMMIT}/{index}"
        raw_path = RAW_REPO / "dataset" / f"{index}.json"
        raw_bytes = raw_path.read_bytes()
        raw_record = json.loads(raw_bytes)
        require(raw_record["index"] == index, f"raw index drift {key}")

        _, _, locator = locators[source_id]
        _, _, candidate = candidates[source_id]
        _, _, full_seed = seeds[key]
        source_file = locator["source_file_binding"]
        record_locator = locator["record_locator"]
        require(source_file["file_sha256"] == digest(raw_bytes), f"source file hash drift {key}")
        require(source_file["byte_length"] == len(raw_bytes), f"source byte length drift {key}")
        git_blob = hashlib.sha1(b"blob " + str(len(raw_bytes)).encode() + b"\0" + raw_bytes).hexdigest()
        require(source_file["git_blob_sha1"] == git_blob, f"source git blob drift {key}")
        require(record_locator["record_raw_sha256"] == digest(raw_bytes), f"raw locator hash drift {key}")
        require(record_locator["record_canonical_sha256"] == digest(canonical(raw_record)),
                f"canonical locator hash drift {key}")
        question_sha = digest(raw_record["question"].encode("utf-8"))
        solution_sha = digest(raw_record["solution"].encode("utf-8"))
        require(record_locator["statement_value_sha256"] == question_sha,
                f"question value hash drift {key}")
        require(record_locator["solution_value_sha256"] == solution_sha,
                f"solution value hash drift {key}")
        require(candidate["target_problem_key"] == key and candidate["disposition"] == "mapped_in_scope_coordinate",
                f"candidate mapping drift {key}")
        require(candidate["source_statement_sha256"] == question_sha and candidate["source_solution_sha256"] == solution_sha,
                f"candidate value hash drift {key}")
        require(full_seed["source_candidate_ids"] == [source_id], f"seed source identity drift {key}")
        require(full_seed["source_statement_sha256"] == question_sha and full_seed["source_solution_sha256"] == solution_sha,
                f"seed value hash drift {key}")

        claim = fragment["claim_review"]
        children = claim["children"]
        if claim["claim_disposition"] == "split":
            require(children and claim["independent_english_statement"] is None,
                    f"invalid split {key}")
            for child in children:
                child["semantic_key"] = semantic_key(child["independent_english_statement"])
                require(not ngram_overlap(child["independent_english_statement"], raw_record["question"]),
                        f"possible verbatim question prose in {key}/{child['part_label']}")
            claim["semantic_key"] = None
        else:
            statement = claim["independent_english_statement"]
            require(isinstance(statement, str) and statement.strip(), f"missing review statement {key}")
            claim["semantic_key"] = semantic_key(statement)
            require(not ngram_overlap(statement, raw_record["question"]),
                    f"possible verbatim question prose in {key}")
        method = fragment.pop("proof_method_summary")
        require(isinstance(method, str) and method.strip(), f"missing proof summary {key}")
        require(not ngram_overlap(method, raw_record["solution"]),
                f"possible verbatim solution prose in {key}")

        pb_problem = pb_problems.get(key)
        if pb_problem:
            pb_number, _, pb_row = pb_problem
            pb_binding = {
                "path": relative(PB_PROBLEMS),
                "file_sha256": digest(PB_PROBLEMS.read_bytes()),
                "line_number": pb_number,
                "row_sha256": pb_row["row_sha256"],
            }
            require(full_seed["putnambench_problem_row_sha256"] == pb_row["row_sha256"],
                    f"full seed PB row binding drift {key}")
        else:
            pb_binding = None
            require(full_seed["putnambench_problem_row_sha256"] is None,
                    f"unexpected full seed PB binding {key}")

        formal_headers = []
        for header_number, _, header in sorted(
                headers.get(key, []),
                key=lambda item: {"lean4": 0, "isabelle": 1, "coq": 2}[item[2]["language"]]):
            formal_headers.append({
                "variant_id": header["variant_id"],
                "language": header["language"],
                "header_sha256": header["declaration_header"]["sha256"],
                "asset_path": relative(PB_HEADERS),
                "asset_file_sha256": digest(PB_HEADERS.read_bytes()),
                "asset_line_number": header_number,
                "asset_row_sha256": header["row_sha256"],
                "rights_id": header["rights"]["rights_id"],
                "license_expression": header["rights"]["license_expression"],
                "external_source_path": header["external_source_binding"]["upstream_relative_path"],
                "external_file_sha256": header["external_source_binding"]["file_sha256"],
                "source_proof_state": "placeholder_with_proof_hole",
            })
        require(full_seed["formal_variant_ids"] == [row["variant_id"] for row in formal_headers],
                f"formal variant crosswalk drift {key}")

        inherited_anomalies = (
            list(locator.get("anomaly_codes", []))
            + list(full_seed.get("anomaly_codes", []))
            + (list(pb_problem[2].get("anomaly_codes", [])) if pb_problem else [])
        )
        anomaly_codes = sorted(set(fragment.pop("anomaly_codes") + inherited_anomalies))
        match = re.fullmatch(r"putnam_(\d{4})_([ab])([1-6])", key)
        require(match is not None, f"bad problem key {key}")
        languages = [header["language"] for header in formal_headers]
        licenses = sorted({header["license_expression"] for header in formal_headers})
        row = {
            "schema_version": SCHEMA_ROW,
            "source_candidate_id": source_id,
            "problem_key": key,
            "coordinate": {
                "year": int(match.group(1)),
                "section": match.group(2).upper(),
                "problem_number": int(match.group(3)),
            },
            "source_index": index,
            "source_problem_type": raw_record["problem_type"],
            "anomaly_codes": anomaly_codes,
            "source_binding": {
                "source_kind": "putnamgap",
                "repository": PUTNAM_REPOSITORY,
                "commit": PUTNAM_COMMIT,
                "tree": PUTNAM_TREE,
                "archive_member_path": f"dataset/{index}.json",
                "file_sha256": digest(raw_bytes),
                "git_blob_sha1": git_blob,
                "byte_length": len(raw_bytes),
                "row_canonical_sha256": digest(canonical(raw_record)),
                "question_json_pointer": "/question",
                "question_value_sha256_utf8": question_sha,
                "solution_json_pointer": "/solution",
                "solution_value_sha256_utf8": solution_sha,
                "evidence_only": True,
            },
            "putnambench_binding": {
                "present": pb_problem is not None,
                "source_problem_row_binding": pb_binding,
                "formal_headers": formal_headers,
            },
            "claim_review": claim,
            "proof_status": {
                "human_status": "solved_competition_problem",
                "status_as_of": REVIEW_AS_OF,
                "solution_evidence": "pinned_solution_locator_and_hash",
                "proof_method_summary": method,
                "solution_text_redistributed": False,
                "formal_statement_available": bool(formal_headers),
                "formal_proof_state": (
                    "placeholder_only_not_proof" if formal_headers else "no_pb_formal_variant"),
            },
            "rights": {
                "question_and_solution_usage": "evidence_only_no_redistribution",
                "question_solution_license": "NOASSERTION_MAA_COPYRIGHT",
                "independent_statement_origin": "reviewer_authored",
                "formal_header_licenses": licenses,
            },
            "existing_5_5_exact_match_candidates": [],
            "variant_handling": {
                "formal_variant_count": len(formal_headers),
                "formal_languages": languages,
                "one_seed_identity_credit_max": True,
                "formal_variants_grant_no_duplicate_credit": True,
            },
            "candidate_only": True,
            "verbatim_source_text_included": False,
            "grants_theorem_credit": False,
            "grants_catalog_entry": False,
            "release_mutation_authorized_or_performed": False,
        }
        output_rows.append(seal(row, "row_sha256"))

    require([row["problem_key"] for row in output_rows] == expected_keys(),
            "output coordinate order drifted")
    require(len({row["source_candidate_id"] for row in output_rows}) == 60,
            "source candidate IDs are not unique")
    semantic_keys = [
        key
        for row in output_rows
        for key in (([row["claim_review"]["semantic_key"]]
                     if row["claim_review"]["semantic_key"] else [])
                    + [child["semantic_key"] for child in row["claim_review"]["children"]])
    ]
    require(len(semantic_keys) == len(set(semantic_keys)),
            "semantic keys collide within shard")
    require(all(row["candidate_only"] and not row["grants_theorem_credit"]
                and not row["grants_catalog_entry"]
                and not row["release_mutation_authorized_or_performed"]
                for row in output_rows), "zero-credit boundary drifted")

    output_payload = b"".join(encoded(row) for row in output_rows)
    dispositions = Counter(row["claim_review"]["claim_disposition"] for row in output_rows)
    validity = Counter(row["claim_review"]["source_claim_validity"] for row in output_rows)
    visibility = Counter(row["claim_review"]["answer_visibility"] for row in output_rows)
    anomaly_codes = [code for row in output_rows for code in row["anomaly_codes"]]
    pb_present = sum(bool(row["putnambench_binding"]["present"]) for row in output_rows)
    formal_count = sum(row["variant_handling"]["formal_variant_count"] for row in output_rows)
    split_children = sum(len(row["claim_review"]["children"]) for row in output_rows)
    inputs = {
        "putnamgap": {
            "repository": PUTNAM_REPOSITORY,
            "commit": PUTNAM_COMMIT,
            "tree": PUTNAM_TREE,
            "clean_checkout_replayed": True,
            "question_and_solution_usage": "evidence_only_no_redistribution",
        },
        "full_putnam_inventory": file_binding(FULL_INVENTORY, 1),
        "full_putnam_source_candidates": file_binding(FULL_CANDIDATES, len(candidate_rows)),
        "full_putnam_seed_problems": file_binding(FULL_SEEDS, len(seed_rows)),
        "putnamgap_locator_manifest": file_binding(LOCATORS, len(locator_rows)),
        "putnambench_inventory": file_binding(PB_INVENTORY, 1),
        "putnambench_source_problems": file_binding(PB_PROBLEMS, len(pb_problem_rows)),
        "putnambench_formal_headers": file_binding(PB_HEADERS, len(pb_header_rows)),
        "parent_5_5_catalog": file_binding(PARENT, 1),
    }
    summary = seal({
        "schema_version": SCHEMA_SUMMARY,
        "review_range": {"first_year": 1988, "last_year": 1992, "rows": 60},
        "expected_problem_keys": expected_keys(),
        "inputs": inputs,
        "output": payload_binding(OUTPUT, output_payload, 60),
        "counts": {
            "rows": 60,
            "reviewed_semantic_claims": len(semantic_keys),
            "claim_dispositions": dict(sorted(dispositions.items())),
            "split_children": split_children,
            "source_claim_validity": dict(sorted(validity.items())),
            "answer_visibility": dict(sorted(visibility.items())),
            "repair_or_explicit_convention_rows": sum(
                row["claim_review"]["source_claim_validity"] != "valid_as_scoped"
                for row in output_rows),
            "anomaly_occurrences": len(anomaly_codes),
            "distinct_anomaly_codes": len(set(anomaly_codes)),
            "putnambench_present": pb_present,
            "putnambench_absent": 60 - pb_present,
            "formal_variant_headers": formal_count,
            "rows_with_existing_5_5_candidates": 0,
        },
        "coverage": {
            "exact_year_coordinate_grid": True,
            "all_problem_keys_and_source_candidate_ids_unique": True,
            "all_parts_and_answer_visibility_reviewed": True,
            "independently_written_statements_and_proof_summaries": True,
            "question_and_solution_value_hashes_bound": True,
            "full_putnam_locator_candidate_and_seed_bindings_replayed": True,
            "putnambench_formal_headers_bound_where_available": True,
            "formal_variants_do_not_grant_duplicate_credit": True,
            "semantic_keys_unique_within_shard": True,
            "source_defects_ocr_and_conventions_explicit": True,
        },
        "set_digests": {
            "problem_keys_sha256": set_digest([row["problem_key"] for row in output_rows]),
            "source_candidate_ids_sha256": set_digest([row["source_candidate_id"] for row in output_rows]),
            "semantic_keys_sha256": set_digest(semantic_keys),
            "row_seals_sha256": set_digest([row["row_sha256"] for row in output_rows]),
        },
        "publication_boundary": {
            "candidate_only": True,
            "benchmark_seed_catalog_disposition": "reviewed_noncatalog_benchmark_seed",
            "theorem_identity_credits_granted": 0,
            "conjecture_credits_granted": 0,
            "other_open_claim_credits_granted": 0,
            "release_entries_granted": 0,
            "release_mutation_authorized_or_performed": False,
            "question_or_solution_text_redistributed": False,
            "formal_variants_and_relation_edges_grant_duplicate_credit": False,
        },
    }, "authority_sha256")
    summary_payload = encoded(summary)
    receipt = seal({
        "schema_version": SCHEMA_RECEIPT,
        "review_range": summary["review_range"],
        "review_output": summary["output"],
        "review_summary": {
            **payload_binding(SUMMARY, summary_payload, 1),
            "authority_sha256": summary["authority_sha256"],
        },
        "source_authorities": inputs,
        "checks": {
            **summary["coverage"],
            "canonical_json_and_row_seals": True,
            "clean_putnamgap_checkout_and_raw_files_replayed": True,
            "full_source_and_putnambench_file_hashes_replayed": True,
            "summary_self_seal": True,
            "exact_output_hash_and_row_count": True,
            "noncatalog_zero_credit_boundary_enforced": True,
        },
        "publication_boundary": summary["publication_boundary"],
    }, "authority_sha256")
    receipt_payload = encoded(receipt)
    return output_payload, summary_payload, receipt_payload, summary, receipt


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output, summary_payload, receipt_payload, summary, receipt = build()
        emit(OUTPUT, output, args.check)
        emit(SUMMARY, summary_payload, args.check)
        emit(RECEIPT, receipt_payload, args.check)
    except (BuildError, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"FAIL Putnam seed review 1988-1992: {error}", file=os.sys.stderr)
        return 1
    print(
        "PASS Putnam seed review 1988-1992 "
        f"mode={'check' if args.check else 'write'} rows=60 "
        f"claims={summary['counts']['reviewed_semantic_claims']} "
        f"pb={summary['counts']['putnambench_present']}/60 "
        f"formal_headers={summary['counts']['formal_variant_headers']} "
        f"sha256={summary['output']['sha256']} receipt={receipt['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
