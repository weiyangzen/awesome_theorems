# Scope map

## Preserved theorem family

The intake preserves the classical analytic Mittag-Leffler theorem family indicated by the catalog:
discrete local polar data can be realized by a meromorphic function, equivalently leading to an
appropriate partial-fraction expansion modulo a holomorphic term. This is a scope description, not
an accepted canonical statement.

A future statement phase may select a prescribed-principal-parts existence formulation, a
decomposition formulation for a given meromorphic function, or a checked equivalent encoding only
after the exact source and transport boundaries below are reviewed.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative source edition and exact theorem and definition
   locators, including assumptions, corrections, errata, dependent source IDs, and independent
   review.
2. Fix the ambient domain: the whole complex plane, a nonempty connected open subset of it, an open
   Riemann surface, or another source-defined object. These variants need different infrastructure.
3. Fix the exceptional set and its condition: a sequence without finite accumulation points, a
   closed discrete subset, or a locally finite family indexed with or without duplicates.
4. Define each prescribed principal part, including a center, finite negative-power Laurent
   polynomial, pole order, nonzero leading coefficient convention, and zero-principal-part cases.
5. Decide whether the root takes local principal parts as input and constructs a meromorphic
   function, or starts with a meromorphic function and decomposes it. Neither direction may be
   inferred from the terse catalog phrase alone.
6. State the exact local matching condition, such as holomorphicity of the difference near every
   prescribed point, equality of Laurent negative coefficients, or equality of local orders and
   trailing data. These are not definitionally interchangeable.
7. Freeze the global representation and convergence claim: locally uniform convergence on compact
   subsets away from poles, convergence after subtracting correcting polynomials, or only an
   existential meromorphic conclusion.
8. Decide whether uniqueness modulo a holomorphic function, normalization at a base point, growth
   restrictions, reality or symmetry conditions, or a rational finite-pole corollary belongs to the
   root.
9. Freeze ordered binders, universes, typeclass assumptions, foundation and TCB profiles, and every
   alternate encoding with a checked equality, iff, or implication witness.

## Boundary and degenerate cases

The statement phase must resolve an empty pole set; finite versus infinite pole sets; a singleton;
repeated centers; zero principal parts; order-zero data; poles at zero; unbounded pole sequences;
finite accumulation at a boundary point versus inside the domain; disconnected or empty domains;
the identically zero and entire functions; finite-pole rational decompositions; and whether a pole
at infinity is represented or excluded.

## Excluded substitutions

- The concrete cotangent expansion `cot_series_rep` is a valuable special case, not the arbitrary
  prescribed-principal-parts theorem.
- Polynomial/rational partial fractions in `Mathlib.Algebra.Polynomial.PartialFractions` cover
  finite algebraic denominators, not general meromorphic functions with an infinite discrete pole
  set.
- `Function.FactorizedRational.divisor` realizes a finite-support zero/pole-order divisor; it does
  not realize arbitrary principal-part coefficients or infinite locally finite polar data.
- The Weierstrass product theorem, Runge theorem, Cousin problems, residue theorem, Laurent
  expansion, or meromorphic-order calculus alone cannot replace the requested root.
- `CategoryTheory.Functor.IsMittagLeffler` is the inverse-system Mittag-Leffler condition and is a
  homonym, not an analytic target or dependency by name alone.
- A structure or hypothesis storing the desired meromorphic function, convergence, or local
  matching equation supplies no proof.
- A theorem name, API `#check`, finite numerical approximation, plotted partial sum, or the
  catalog's `已验证` label supplies no H or M credit.

## Neighbor boundaries

`THM-M-0230` owns the Weierstrass factorization theorem and `THM-M-0238` owns Abel's theorem. Their
future sources and artifacts remain separate. Runge approximation may become an explicit proof
dependency after exact statement and obligation freezes, but no neighboring target grants status by
proximity.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks plane/domain meromorphic predicates,
orders and divisors, finite-support factorized rational functions, and the cotangent expansion. A
bounded exact-topic search found the concrete cotangent expansion and the unrelated category-theory
condition, but no arbitrary analytic prescribed-principal-parts existence declaration. This is
scoped discovery evidence, not an exhaustive anchor audit or proof of global absence.
