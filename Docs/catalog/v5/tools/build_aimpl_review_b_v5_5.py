#!/usr/bin/env python3
"""Materialize the manual review for AimPL candidates 31--59."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = REPO_ROOT / "Docs/catalog/v5/sources/aimpl"
CURATION_DIR = REPO_ROOT / "Docs/catalog/v5/curation/aimpl_v5_5"
CANDIDATES = {
    row["candidate_index"]: row
    for row in map(json.loads, (SOURCE_DIR / "candidates.jsonl").read_text(encoding="utf-8").splitlines())
}


# decision, reason, tier, exact selector, basis, summary, duplicate hints
# Selectors are exact substrings of source body_html.  None uses the whole body.
REVIEWS = {
    31: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "Canonical and still source-listed K_4^3 Turan-density conjecture, with several constructions, successive upper bounds, and an Erdős prize context.",
         "The Turan density of the complete 3-uniform hypergraph on four vertices is 5/9.", []),
    32: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "Broad complete-3-graph Turan-density formula in a prominent prize problem family; the source gives lower-bound constructions and does not mark it solved.",
         "For complete 3-uniform hypergraphs K_m^3, the Turan density equals 1-(2/(m-1))^2.", []),
    33: ("accept", "explicit_open_atomic_component", "medium",
         "\\[\r\n \\pi(B_{5,5})=\\frac{40}{81},\r\n\\]",
         "The first displayed equality is an exact standalone component of a two-equality source block, with explicit lower and upper-bound research context.",
         "The Turan density of the hypergraph book B_(5,5) is 40/81.", []),
    34: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Exact density conjecture with construction and a close flag-algebra upper bound; no resolution appears in status or remarks.",
         "The tight 3-uniform 5-cycle has Turan density 2 sqrt(3)-3.", []),
    35: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Exact density claim with a matching recursive lower-bound construction in the source context and no solved marker.",
         "The tight 3-uniform 5-cycle with one edge removed has Turan density 1/4.", []),
    36: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Research-level asymptotic extremal claim; the linked remark identifies the first remaining case as probably very hard and records only a weaker theorem.",
         "For r>=3 and s>=4, f^r(n,s(r-2)+3,s)=o(n^2).", []),
    37: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "A fully defined asymptotic matching claim whose source explains that it would imply Roth's theorem and has a Szemeredi-type generalization.",
         "The specified linear union M of tripartite matchings avoiding the crossing configuration has size o(n^2).", []),
    38: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Complete quantified extremal-graph proposition, introduced literally as a conjecture and not marked resolved.",
         "A graph formed as an edge-disjoint union of epsilon*n^alpha copies of F must contain an additional copy of F under the stated extremal-number hypothesis.", []),
    39: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "Prominent sharp cutoff-location conjecture with explicit best lower and upper bounds in the source status.",
         "Random-to-random card shuffle on S_n has cutoff at (3/4)n log n.", []),
    40: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "A precise parity-specific form of the named colored-Jones volume conjecture for hyperbolic links.",
         "The normalized colored Jones polynomial of a hyperbolic link has the stated volume/Chern-Simons asymptotic along even colors.",
         ["aimpl-candidate/41 is the odd-color companion, not semantically equivalent"]),
    41: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "A precise parity-specific form of the named colored-Jones volume conjecture for hyperbolic links.",
         "The normalized colored Jones polynomial of a hyperbolic link has the stated volume/Chern-Simons asymptotic along odd colors.",
         ["aimpl-candidate/40 is the even-color companion, not semantically equivalent"]),
    42: ("reject", "non_truth_apt_imperative_request", "none", None,
         "The body asks researchers to formulate and prove a conjecture but does not itself state the conjecture; no affirmative claim may be invented.",
         "A request to formulate a Teichmuller-TQFT volume conjecture for Fundamental Shadow Link complements.", []),
    43: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "The source supplies definitions and an iff criterion attributed to Berger-Coburn; no solved or resolved marker appears.",
         "A Toeplitz operator on Fock space is bounded exactly when the time-1/4 heat evolution of its symbol is bounded.", []),
    44: ("accept", "explicit_open_atomic_component", "medium",
         "For a bounded convex domain $\\Omega \\subset \\mathbb{R}^n$, the spectral gap $\\lambda_2(\\Omega, \\alpha)-\\lambda_1(\\Omega, \\alpha)$ is strictly increasing as a function of $\\alpha>0$.",
         "The exact first sentence is the primary monotonicity conjecture; the following inequality is explicitly only its consequence. Status records special cases, not a general solution.",
         "For every bounded convex domain, the first Robin spectral gap strictly increases with positive boundary parameter.", []),
    45: ("accept", "explicit_open_atomic_component", "medium",
         "\\item In two dimensions, the disk maximizes $\\lambda_1(\\Omega, \\alpha)$ among all simply connected domains of the same area.",
         "The selected first enumerated item is a literal standalone restricted Bareket conjecture. The intro says the unrestricted conjecture was disproved, but this restricted case remains source-listed.",
         "For negative Robin parameter in two dimensions, the disk maximizes the lowest eigenvalue among equal-area simply connected domains.", []),
    46: ("accept", "explicit_open_atomic_component", "medium",
         "\\item minimized by the equilateral triangle when $\\alpha>0$.",
         "The selected positive-parameter item is an exact standalone component with the triangle and fixed-area scope supplied immediately before it.",
         "Among equal-area triangles and positive Robin parameter, the equilateral triangle minimizes the lowest Robin eigenvalue.", []),
    47: ("reject", "non_truth_apt_imperative_request", "none", None,
         "The source body is an instruction to prove an equality rather than an asserted proposition; extracting the equality alone would drop its quantified minimizer context.",
         "A request to prove multiplicity of an optimal kth Dirichlet eigenvalue.", []),
    48: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Complete shape-optimization maximizer claim with all classes and transformations defined in the source intro; only a modified two-dimensional case is marked settled.",
         "A hypercube attains the stated affine-normalized maximum of the product of principal Dirichlet eigenvalues of a symmetric convex body and its polar.", []),
    49: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "The source calls this a longstanding polygonal Faber-Krahn conjecture and marks only N=3,4 solved, leaving the general N claim open.",
         "Among equal-area polygons with at most N edges, the regular N-gon minimizes the principal Dirichlet eigenvalue.", []),
    50: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Precise dimension-uniform eigenfunction estimate with domain and geometric parameters defined in the intro; status proves n=2 only.",
         "Principal Dirichlet eigenfunctions on convex domains satisfy the stated inradius/diameter-improved L-infinity bound.", []),
    51: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "A complete named shape-optimization claim with the concavity exponent defined in the source intro and no solved marker.",
         "The ball maximizes the best power-concavity exponent of the principal Dirichlet eigenfunction among bounded convex domains.", []),
    52: ("accept", "explicit_open_atomic_conjecture_with_redundant_special_case", "medium", None,
         "The general k-bound in item (b) contains item (a) as k=2, so the block is semantically one general eigenvalue-ratio claim rather than two independent credits.",
         "For every convex domain, the kth nonzero Neumann eigenvalue is at most k^2 times the first nonzero one.", []),
    53: ("accept", "explicit_open_atomic_conjecture", "high", None,
         "Named hot-spots conjecture with precise alternative domain hypotheses, extensive special-case results, and an explicit counterexample only outside those hypotheses.",
         "The first nontrivial Neumann eigenfunction has no interior global extrema on simply connected planar or convex higher-dimensional domains.", []),
    54: ("accept", "explicit_open_atomic_conjecture", "medium", None,
         "Exact lower-bound conjecture with the operator and curve normalization defined in the intro and a documented current lower bound below 1.",
         "The lowest eigenvalue of the curvature-potential operator associated with a closed plane curve of length 2pi is at least 1.", []),
    55: ("reject", "non_truth_apt_imperative_request", "none", None,
         "The body is phrased as an instruction to show an inequality, not an asserted proposition; independently, the intended proposition already appears in ConjectureBench.",
         "The intended claim is the origin-symmetric log-Brunn-Minkowski inequality.", ["conjecturebench/cb-0088"]),
    56: ("reject", "non_truth_apt_imperative_request", "none", None,
         "The body is a proof instruction rather than an asserted proposition, so the inequality cannot be promoted by rewriting it affirmatively.",
         "The intended claim is an L_p-Brunn-Minkowski inequality for symmetric convex bodies, including p=0.", ["overlaps conjecturebench/cb-0088 at p=0; not equivalent"]),
    57: ("pending", "formula_integrity_and_context_check_required", "none", None,
         "Although grammatically assertive, the displayed inequality repeats the same right-hand factor and supplies no citation or status note; authoritative confirmation is needed before treating the literal formula as the named conjecture.",
         "A Cordero-Erausquin intersection/polar-body volume inequality, as literally printed by AimPL.", []),
    58: ("pending", "formula_integrity_and_citation_check_required", "none", None,
         "The printed Dar inequality is dimensionally suspicious because powers of the overlap volume appear absent, and the page supplies no supporting citation; it must not be silently corrected.",
         "Dar's conjectured lower bound for the volume radius of a Minkowski sum in terms of maximal overlap.", []),
    59: ("reject", "question_not_affirmative_conjecture", "none", None,
         "The source explicitly asks whether two bounds hold. Its conjecture tag does not authorize converting that question into an affirmative proposition.",
         "A question asking for sharp lower and upper bounds on lambda_1 times torsional rigidity for planar convex sets.", []),
}


def main() -> None:
    rows = []
    for index in range(31, 60):
        candidate = CANDIDATES[index]
        decision, reason, tier, selector, basis, summary, duplicates = REVIEWS[index]
        if decision == "accept":
            exact = candidate["exact_source"]["body_html"] if selector is None else selector
            assert exact in candidate["exact_source"]["body_html"], (index, exact)
        else:
            exact = None
        rows.append({
            "candidate_index": index,
            "candidate_key": candidate["candidate_key"],
            "decision": decision,
            "reason_code": reason,
            "exact_claim_html": exact,
            "truth_apt": decision in {"accept", "pending"},
            "context_complete": decision == "accept",
            "source_asserted_open": True,
            "tier": tier,
            "basis": basis,
            "semantic_summary": summary,
            "duplicate_hints": duplicates,
        })
    output = CURATION_DIR / "review-b.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        for row in rows
    )
    output.write_bytes(payload)
    counts = {d: sum(row["decision"] == d for row in rows) for d in ("accept", "reject", "pending")}
    print(f"PASS review-b rows={len(rows)} counts={counts} sha256={hashlib.sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
