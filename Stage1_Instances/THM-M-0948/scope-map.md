# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0948`, the name `Szemeredi theorem`, Endre Szemeredi, 1975, and
the slogan "positive-density sets contain arbitrarily long arithmetic progressions." This points to
the classical density theorem for arithmetic progressions. It does not yet fix one binder-complete
claim.

A later statement phase may select an exact root only from an immutable, independently reviewed
source passage. The standard infinite family is a scope locator, not an accepted statement: a set
of integers with a suitable positive density contains a nonconstant arithmetic progression of each
prescribed finite length.

## Proposition-changing decisions

The exact-source statement phase must freeze all of the following:

1. Whether the ambient set is a subset of `Nat`, the positive integers, or `Int`, and how these
   encodings are transported.
2. Whether positive density means upper asymptotic, lower asymptotic, natural, upper Banach, or a
   source-specific finite density condition.
3. The interval convention, such as `[0, N)`, `[1, N]`, or translated intervals, the cardinality
   normalization, and the exact `limsup`, `liminf`, or limit expression.
4. The ordered quantifiers over the set, density witness, progression length, finite threshold,
   first term, and common difference.
5. Whether the root is the infinite positive-density form, a finitary threshold theorem, an
   extremal-density limit, or an explicit checked conjunction/equivalence.
6. The progression encoding, normally `a + i * d` for `i` in `range k`, and whether `d` is positive
   in `Nat` or merely nonzero in `Int`.
7. Whether every progression term must remain in the selected finite interval in a finitary form.
8. The exact relationship between "arbitrarily long" and `forall k`, including any lower bound on
   `k` and the behavior at `k = 0`, `1`, and `2`.

These choices are mathematically related but not definitionally interchangeable. Every alternate
encoding needs a checked transport before it can receive statement or proof credit.

## Boundary cases

- The empty and finite sets and density zero.
- The whole ambient set and density one.
- Progression lengths zero, one, and two.
- Common difference zero, which would make every constant sequence a degenerate progression.
- A starting value or final term outside the chosen natural-number or finite-interval domain.
- Density existing as a true limit versus only a positive upper density.
- Shifts between zero-based and one-based intervals and between `Nat` and positive integers.
- Infinite-form hypotheses that use a positive real density witness versus a strict positivity
  assertion on a defined density.

No case is excluded at intake because no canonical proposition is selected.

## Explicit exclusions

- Roth's theorem or `THM-M-0947`, which treats progressions of length three only.
- Van der Waerden's theorem, which concerns finite colorings rather than positive-density sets.
- Green-Tao (`THM-M-0945`), which concerns arithmetic progressions in the primes.
- The density Hales-Jewett theorem (`THM-M-0949`) or a combinatorial-line theorem without checked
  transports to the frozen root.
- Szemeredi's regularity lemma (`THM-M-0843`) and the distinct Ruzsa-Szemeredi extremal problem.
- Polynomial, multidimensional, relative, ergodic, quantitative-bound, or finite-group variants
  selected merely because their formal interfaces are convenient.
- Schnirelmann density used as a substitute for the source's unidentified density convention.
- A structure or premise that assumes the desired progression-existence conclusion.
- The catalog's untrusted `verified` label or a bounded API search used as proof evidence.

No canonical Lean target, expression fingerprint, alternate encoding, discovery protocol,
obligation registry, or proof state is frozen during intake.
