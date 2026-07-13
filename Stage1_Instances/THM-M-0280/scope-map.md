# Scope map

## Preserved theorem family

The intake preserves exactly the family named by the catalogue: Minkowski's triangle inequality in
`L^p` space. In conventional measure-theoretic notation, a prospective finite-exponent version has
the shape

`||f + g||_p <= ||f||_p + ||g||_p` for `1 <= p`,

but this formula is an orientation aid, not a frozen canonical statement. The repository record
does not define any symbol in it or identify a source edition.

## Decisions required at statement freeze

An exact, source-reviewed proposition must decide all of the following:

1. Whether the root is the integral inequality for representative functions, an `eLpNorm` or
   `lpNorm` seminorm inequality, closure of `MemLp` under addition, or the triangle inequality for
   the quotient space `Lp`.
2. Whether the exponent is real or `ENNReal`, whether it ranges over `1 <= p < infinity` or includes
   `p = infinity`, and how `p = 1` is represented. The `p < 1` quasi-triangle regime is not the
   ordinary Minkowski inequality named by the catalogue.
3. The measurable-space and measure binders, including whether sigma-finiteness, finiteness, or no
   extra measure hypothesis is required.
4. The function codomain: nonnegative extended reals, real or complex scalars, or a general
   (extended) seminormed additive group, with its universe and topology/typeclass context.
5. Whether `AEStronglyMeasurable`, `AEMeasurable`, or `MemLp` hypotheses are explicit, inherited
   from membership in `Lp`, or discharged by a more specialized domain.
6. Whether both summands must have finite seminorm, or an extended-valued inequality is stated even
   when a right-hand seminorm is infinite.
7. The exact ordered binders, coercions, almost-everywhere quotient convention, pointwise addition,
   norm normalization, conclusion type, universes, and foundation profile.
8. Which alternate formulations are part of the canonical claim and which directions between them
   require checked equality, `Iff`, or implication transports.

## Degenerate and boundary cases

Source review must explicitly cover the zero measure; empty or subsingleton domains; zero and
almost-everywhere-zero functions; `p = 1`; any admitted `p = infinity` case; functions with infinite
extended seminorm; functions outside `MemLp`; null-set changes of representatives; scalar versus
vector-valued functions; and equality versus strict-inequality examples. No case is excluded before
the proposition is selected.

## Excluded substitutions

- Finite-dimensional or finite-sum `l^p` inequalities alone are special cases, not automatically
  the requested measure-theoretic `L^p` theorem.
- Infinite series or sequence-space variants alone do not establish the general measure-space root.
- The `p < 1` quasi-triangle estimate with a constant is not the norm triangle inequality.
- Holder, Jensen, Young, or generalized mean inequalities may be proof ingredients but are not the
  requested root.
- The Minkowski convex-body theorem, Brunn-Minkowski inequality, Minkowski functional, Minkowski
  spacetime, Hasse-Minkowski theorem, and number-field Minkowski bounds are distinct namesakes.
- A normed-space instance whose triangle law was assumed rather than derived from the `L^p`
  construction cannot supply the analytic proof boundary by itself.
- A theorem name, `#check`, direct axiom report, or the catalogue's untrusted `已验证` label supplies
  no source or machine-completion credit.

## Neighbor boundaries

`THM-M-0279` owns Holder's inequality and `THM-M-0281` Jensen's inequality. They may become proof
dependencies after the exact statement and obligation registry are frozen, but neither is
interchangeable with this root. Separate repository targets own the convex-body theorem and
number-field Minkowski bound; their artifacts and evidence do not transfer.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks exact-topic extended-
seminorm, real seminorm, quotient-space, integral-formula, and finite-sum interfaces. These are
bounded discovery leads, not an exhaustive anchor audit, exact statement identity, a minimal-import
certificate, or proof-body provenance evidence.
