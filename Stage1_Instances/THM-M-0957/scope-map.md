# Scope map

## Preserved theorem family

The intake preserves Behrend's quantitative construction of large finite subsets of nonnegative
integers with no nontrivial three-term arithmetic progression. The inspected 1946 paper makes
"large" precise through an asymptotic lower bound on an extremal function. A fixed example, a
generic assertion that some 3AP-free set exists, or Roth's upper-density theorem is not the target.

The original source and pinned mathlib expose closely related but nonidentical formulations. A
future statement phase must choose a source-reviewed canonical root and add checked transports;
intake does not silently identify them.

## Decisions required at statement freeze

1. Whether the ambient interval is the source's inclusive nonnegative integers `<= N`,
   `{1, ..., N}`, or mathlib's zero-based `Finset.range N`.
2. Whether the root uses the maximum-cardinality function `v(N)`/`rothNumberNat`, directly
   existentially quantifies a large finite set, or retains both via a checked equivalence.
3. Whether "no three terms" means pairwise-distinct terms, distinct endpoints, a positive common
   difference, or the exact `ThreeAPFree` predicate, with a checked equivalence over naturals.
4. Whether the exact historical epsilon-and-eventual bound is canonical, a modern
   `N * exp (-C * sqrt (log N))` form is canonical, or one is only a proved consequence of the
   other.
5. The ordered binders for `epsilon`, `N`, and the sufficiently-large threshold; the positivity
   hypotheses; strict versus non-strict inequalities; all `Nat`-to-`Real` casts; and real
   exponentiation, logarithm, and square-root conventions.
6. Whether the historical constant `2 * sqrt (2 * log 2) + epsilon`, mathlib's explicit constant
   `4`, or only an existential absolute constant belongs in the root.
7. The exact source boundary between the theorem statement, the digit/sphere construction, and
   later strengthened or simplified reformulations.
8. Fixed Lean options, namespace, universes, typeclass context, minimal imports, foundation/TCB/
   computation profiles, exact expression fingerprint, and every credited alternate encoding.

## Degenerate and boundary cases

Source review and statement mutation must address `N = 0` and `N = 1`; empty and singleton sets;
the inclusive-versus-exclusive endpoint shift; constant triples; repeated terms; endpoints in
reverse order; even and odd endpoint sums; `epsilon = 0`; negative epsilon; `log N <= 0`; a zero
square root; a real lower bound below one; floor/ceiling or cardinality rounding; and the exact
meaning of "sufficiently large." No boundary case is silently excluded at intake.

## Excluded substitutions

- Roth's theorem (`THM-M-0947`) is an asymptotic upper bound on 3AP-free density, not Behrend's
  construction or lower bound.
- Elkin's improvement (`THM-M-0958`) and later lower-bound improvements are separate targets.
- A large cap set in a finite vector space, a sum-free set, a Sidon set, a Salem-Spencer existence
  claim without the Behrend scale, or a fixed finite witness cannot replace the target.
- `ThreeAPFree` alone is a definition, and `rothNumberNat_spec` alone merely realizes an extremal
  set; neither supplies the quantitative Behrend bound.
- `Behrend.threeAPFree_sphere` or `Behrend.threeAPFree_image_sphere` closes a construction layer,
  not necessarily the selected quantitative root.
- A theorem assuming the desired 3AP-free set or cardinality bound, a structure field containing
  it, a numerical experiment, or unchecked computation supplies no proof.
- The catalog's `verified` label, a theorem name, `#check`, or adjacent formal infrastructure
  supplies no accepted H, M, or R credit.

## Neighbor boundaries

`THM-M-0947` owns Roth's theorem, `THM-M-0958` Elkin's improvement, and `THM-M-0956` an
Erdos-Turan Sidon-set construction. Their artifacts and proof credit remain separate. A later exact
obligation graph may cite a dependency only after statement and provenance review.

## Formal boundary

No canonical Lean expression is frozen at intake. The pinned probe authenticates the exact names
and current types of the Behrend module's principal definition, construction, extremal, and bound
interfaces. This is unusually strong intake discovery evidence, but it is not the later statement
certificate, immutable anchor audit, axiom report, provenance closure, or proof receipt.
