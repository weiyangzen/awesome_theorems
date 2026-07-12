# Scope map

## Preserved theorem family

The intake preserves the finite density Hales-Jewett family identified by the title, date, and
attribution: a positive-density subset of a sufficiently high-dimensional finite word cube over a
fixed nonempty alphabet contains a nondegenerate combinatorial line. This family boundary does not
yet assert one canonical proposition. A statement phase must adopt an immutable source passage and
independently review every proposition-changing choice below.

## Candidate source proposition

D. H. J. Polymath, Annals of Mathematics 175 (2012), Theorem 1.4, states that for every positive
integer `k` and every real `delta > 0`, there is a positive integer `dhj(k, delta)` such that, for
every `n >= dhj(k, delta)`, each subset `A` of `[k]^n` with density at least `delta` contains a
combinatorial line. This is the candidate exact mathematical root, not an accepted canonical claim.

## Decisions required at statement freeze

1. Fix the reviewed edition and theorem locator, the relationship to Furstenberg-Katznelson 1991,
   all incorporated definitions, the proof boundary, correction history, and independent review.
2. Fix whether the alphabet is `Fin k`, an arbitrary finite type of cardinality `k`, or another
   checked equivalent encoding, and preserve the source condition `0 < k`.
3. Fix whether dimension is `n : Nat` with words `Fin n -> Fin k`, a general finite coordinate
   type, or a threshold-independent existential coordinate type. The source quantifies over every
   `n` beyond a threshold; the ordinary mathlib Hales-Jewett existential dimension is not identical.
4. Fix density as `|A| / k^n`, including the codomain (`Real` versus `NNRat`), casts, and the exact
   weak inequality `delta <= density(A)`.
5. Fix the representation of `A` as a set or finset and the decidability/finiteness interfaces
   needed to count it without adding a mathematical assumption.
6. Fix combinatorial lines as nonempty wildcard sets. Under the pinned mathlib representation this
   is `Combinatorics.Line.proper`; a degenerate singleton word is not allowed.
7. Fix the ordered quantifiers and dependencies: `k`, `delta`, threshold, dimension, subset, density
   premise, then the line contained in that subset.
8. Decide whether the threshold must itself be positive or merely may be replaced by a positive
   one, and whether natural-number conventions include dimension zero.

## Degenerate and boundary cases

Source review must explicitly dispose of an empty alphabet (`k = 0`), the singleton alphabet,
`delta <= 0`, `delta > 1`, dimension zero, an empty subset, equality at the density threshold, and
the fact that a proper line over a singleton alphabet may have only one distinct point while its
wildcard set is still nonempty. These cases cannot be silently removed or used to weaken the root.

## Neighbor and substitution exclusions

- `THM-M-0948` (Szemeredi's theorem) is a consequence/neighbor, not the requested word-cube root.
- `THM-M-0950` catalogs the Polymath proof project. Its proof-route identity is separate from this
  theorem target, so no task state or proof credit transfers between them.
- `Combinatorics.Line.exists_mono_in_high_dimension` is the ordinary finite-coloring
  Hales-Jewett theorem. A density theorem implies an ordinary coloring result by a color-density
  argument, but the converse is not the density result and the pinned declaration cannot substitute.
- `Combinatorics.Subspace.exists_mono_in_high_dimension` is multidimensional Hales-Jewett and is
  likewise not the density theorem.
- A fixed alphabet such as `k = 3`, a quantitative bound only, a finite check at one dimension, or
  an arithmetic-progression corollary cannot replace the all-positive-`k`, all-positive-density root.
- A structure or hypothesis that assumes the desired line, and the catalog's untrusted `verified`
  label, supply no proof credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, obligation registry,
discovery protocol, or proof state is frozen at intake.
