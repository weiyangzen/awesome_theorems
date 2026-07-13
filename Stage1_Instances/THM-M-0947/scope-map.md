# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0947`, the name "Roth theorem," Klaus Roth, 1953, and the slogan
"integer sets contain a three-term arithmetic progression." The attribution and date identify the
classical density theorem for three-term progressions, but the slogan alone is false for arbitrary
integer sets and is not a binder-complete proposition.

A later statement phase may select an exact root only from an immutable, independently reviewed
source passage. The usual family says that sufficiently dense finite sets, equivalently in an
appropriate asymptotic formulation positive-density integer sets, contain a nonconstant
three-term arithmetic progression. That family description is a scope locator, not an accepted
statement or equivalence.

## Proposition-changing decisions

The exact-source statement phase must freeze all of the following:

1. Whether the root is a quantitative finite threshold theorem, an extremal limit such as
   `r_3(N) = o(N)`, an infinite positive-density theorem, or an explicit checked relationship among
   these forms.
2. Whether the ambient domain is `Nat`, positive integers, `Int`, or a finite abelian group, and
   whether the finite interval is `[0, N)`, `[1, N]`, or another source-defined carrier.
3. The exact density or cardinality hypothesis. The catalog currently states none, so it cannot
   determine upper, lower, natural, or Banach density or the quantifiers in a finitary version.
4. The ordered quantifiers over density, threshold, interval size, set, and progression witnesses,
   including strict versus non-strict inequalities and real/natural coercions.
5. The progression encoding: witnesses `a, b, c` with `a + c = 2 * b`, or `a, a + d, a + 2*d`,
   together with order, membership, and the requirement `d > 0` or otherwise nonzero.
6. Whether repeated endpoints are excluded by `a != c`, `a != b`, `d != 0`, or an ordered triple,
   and the exact checked transport to mathlib's `ThreeAPFree` convention.
7. Whether all three terms must lie in the selected finite interval by construction or by explicit
   hypotheses, and how zero-based and one-based versions are transported.
8. The accepted logical, choice, noncomputability, limit, cardinality, and computation profiles.

The available formulations are mathematically related but not definitionally interchangeable.
Every credited alternate encoding requires a checked transport after source selection.

## Boundary cases

- Empty, singleton, two-element, and finite sparse sets.
- The whole interval, density one, zero density, and a missing or nonpositive density parameter.
- Interval sizes zero through two and thresholds that make the finite statement vacuous.
- The trivial progression `a = b = c`, common difference zero, and integer progressions with a
  negative difference or reversed order.
- Sets containing a nontrivial triple that is not ordered as written.
- `Nat` addition versus integer addition and casts between cardinalities, naturals, and reals.
- Torsion in finite abelian groups, where `a + c = 2*b` can have different degeneracies.

No boundary case is excluded at intake. The source-selected statement must resolve each one.

## Explicit non-substitutions

- The unconditional assertion that every integer set contains a nontrivial three-term progression.
- A theorem that merely assumes the desired progression or assumes `not ThreeAPFree A`.
- A finite abelian-group result used as the integer root without a checked transfer.
- A single quantitative bound involving mathlib's implementation-specific
  `cornersTheoremBound` used as the historical root without source and formulation mapping.
- Szemeredi's arbitrary-length theorem (`THM-M-0948`) used without specializing and mapping every
  density convention.
- Green-Tao for primes (`THM-M-0945`), Van der Waerden colorings, density Hales-Jewett
  (`THM-M-0949`), or the Ruzsa-Szemeredi extremal graph theorem.
- Roth's algebraic-irrational approximation theorem (the Thue-Siegel-Roth theorem), which is a
  different result sharing the surname.
- Behrend lower bounds, finite examples, computation, or the untrusted `verified` label as root
  proof evidence.

## Statement-gate retry condition

Admit a lawful immutable copy or independently reviewed transcription of the exact primary or
approved authoritative statement, definitions, assumptions, proof boundary, corrections, and
errata. Then select one formulation, freeze all binders and boundary conventions, elaborate it with
minimal pinned imports, serialize its expression and environment fingerprints, check every claimed
transport, and run the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.
