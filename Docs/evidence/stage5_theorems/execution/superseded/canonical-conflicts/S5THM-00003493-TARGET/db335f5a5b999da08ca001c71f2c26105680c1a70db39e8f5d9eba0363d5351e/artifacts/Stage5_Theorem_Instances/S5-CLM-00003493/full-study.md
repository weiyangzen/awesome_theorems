# Full study: S5-CLM-00003493

## FRAG-01 — SEMANTIC-ROOT

Hypotheses: the frozen provider file, declaration range, namespace, and four
source-local definition bodies are fixed. Inference: delta-reduce
`Real.iteratedLog`, `maximalLength`, `IsIncreasing₂`, and `lt₂`, retaining every
cast, filter, exponent, and quantifier. Output: the explicit target proposition
in all three Lean files. Formal anchor: `maximalLength_le_isBigO_statement` and
`audit_source_to_target`. Downstream uses: every machine and readable node.
Exceptional case: the provider theorem body is sorry-backed and is excluded
from proof authority. Trust boundary: the canonical Master must independently
recompute the elaborated expression and transitive environment.

## FRAG-02 — FIXED-COORDINATE-OBSTRUCTION

Hypotheses: two distinct coordinates `i,j` of `b` are at most those of `a`.
Inference: if `a` were strictly smaller than `b` at two distinct coordinates,
the three-element index type forces one strict coordinate to equal `i` or `j`,
contradicting its non-strict reverse inequality. Output: negation of the
two-coordinate strict relation. Formal anchor: `not_two_less_of_fixed` and
`audit_not_two_less_of_fixed`. Downstream uses: the pairwise contradiction.
Exceptional case: both orientations of the two list positions are handled.
Trust boundary: finite-index exhaustion is discharged by kernel-checked Omega.

## FRAG-03 — PIGEONHOLE-COLLISION

Hypotheses: every coordinate of every triple is in `[1,n]`, and the list length
is greater than `n²`. Inference: map list positions into the product of two
finite intervals using the first two coordinates. Its cardinality is `n²`, so
two distinct positions have the same image. Output: a collision in coordinates
zero and one. Formal anchor: `exists_first_two_collision` and
`audit_exists_first_two_collision`. Downstream uses: the quadratic bound.
Exceptional case: the cardinality identity handles all naturals, including
zero and one. Trust boundary: Mathlib's finite pigeonhole theorem is pinned.

## FRAG-04 — QUADRATIC-SUPREMUM

Hypotheses: membership in the unfolded supremum set gives an admissible pairwise
increasing list. Inference: if its length exceeded `n²`, FRAG-03 yields two
positions with equal first coordinates; order the positions and apply FRAG-02
to contradict pairwise increasingness. Output: every member length and hence
the natural supremum is at most `n²`. Formal anchor:
`unfolded_maximalLength_le` and `audit_unfolded_maximalLength_le`. Downstream
uses: the final pointwise inequality. Exceptional case: the empty list proves
the supremum set nonempty. Trust boundary: conditional supremum and list
pairwise access are pinned Mathlib declarations.

## FRAG-05 — BIG-O-WITNESS

Hypotheses: `L(n)` is the natural-valued unfolded iterated logarithm, cast to
the reals. Inference: choose `Ω(n)=-L(n)`; reflexive Big-O and invariance under
negating the comparison function prove `L =O[atTop] Ω`. Output: the first
conjunct of the root. Formal anchor: the first branch of
`maximalLength_le_isBigO_proof` and `audit_exact_root`. Downstream uses: root
existential assembly. Exceptional case: no eventual threshold is required.
Trust boundary: only the norm-based Mathlib Big-O relation is used.

## FRAG-06 — EXPONENTIAL-DENOMINATOR

Hypotheses: `L(n)` is a cast natural and so nonnegative. Inference:
`-L(n) ≤ 0`, hence `exp(-L(n)) ≤ 1`; exponential positivity allows division.
Multiplying the denominator by the nonnegative square cannot exceed the square,
so `n² ≤ n² / exp(-L(n))`. Output: denominator enlargement inequality. Formal
anchor: the second branch of `maximalLength_le_isBigO_proof` and
`audit_exact_root`. Downstream uses: final bound. Exceptional case: positivity
rules out division by zero for every `n`. Trust boundary: pinned real
exponential order laws.

## FRAG-07 — ROOT-COMPOSITION

Hypotheses: FRAG-04, FRAG-05, and FRAG-06. Inference: cast the natural supremum
bound to the reals, compose it with the denominator inequality, pair it with
the Big-O witness, and introduce the chosen `Ω`. Output: the exact unfolded
frozen theorem root. Formal anchor: `maximalLength_le_isBigO_proof` and
`audit_exact_root`. Downstream uses: provisional release decision and Stage6
handoff. Exceptional case: none remain. Trust boundary: release remains
provisional until canonical Master recomputation and integration.
