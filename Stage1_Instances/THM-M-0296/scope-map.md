# Scope map

## Preserved theorem family

The intake preserves the classical Riesz-Thorin strong-type interpolation family named by the
catalog: endpoint boundedness of a linear operator between two pairs of `Lp` spaces yields an
intermediate strong-type bound with interpolated reciprocal exponents. This is a family-level
description for source selection, not a frozen proposition.

The future statement must come from one inspected source formulation. It must not combine clauses
from inequivalent modern variants merely because they share the Riesz-Thorin name.

## Required statement decisions

1. Fix both measure spaces, sigma-algebras, measures, and any sigma-finiteness or semifiniteness
   assumptions.
2. Fix real or complex scalar-valued functions and the exact linearity field of the operator.
3. Define the operator's initial domain, normally an intersection or a dense class, and state how
   equality almost everywhere and extensions to completed `Lp` spaces are handled.
4. Fix endpoint exponents `p0`, `p1`, `q0`, and `q1`, their legal ranges, and the representation of
   infinity.
5. Fix the interpolation parameter and its range, including whether endpoints are included.
6. State the reciprocal-exponent equations for the intermediate `p` and `q` and address zero
   reciprocals at infinite exponents.
7. State both endpoint strong-type hypotheses, including whether their constants are nonnegative,
   positive, optimal, or only upper bounds.
8. Fix the exact conclusion: existence and uniqueness of an extension, its operator-norm bound,
   the pointwise-on-domain estimate, or a conjunction of these.
9. Fix the interpolated constant and conventions for zero endpoint bounds and zero powers.
10. Freeze ordered binders, universes, typeclasses, all hypotheses and conclusion, foundation/TCB/
    computation profiles, and every alternate encoding with a checked transport.

## Boundary and degenerate cases

Source review must explicitly resolve interpolation parameter `0` and `1`; equal endpoint
exponents; `p` or `q` equal to `1` or infinity; zero and infinite endpoint constants; the zero
operator; zero, empty, finite, atomic, and infinite measure spaces; null representatives; a
non-dense initial domain; real versus complex interpolation; endpoint extensions that disagree on
an intersection; and the behavior of `0^0` in the displayed bound. No case is silently excluded at
intake.

## Excluded substitutions

- Marcinkiewicz weak-type interpolation (`THM-M-0297`) is a different theorem.
- The generic interpolation catalog entry (`THM-M-0374`) does not supply this target's statement.
- Hadamard three-lines alone is not the operator theorem, even when used in its standard proof.
- Hausdorff-Young, Plancherel, Fourier endpoint estimates, or a finite-dimensional matrix norm
  inequality are applications or special cases, not the general target.
- Interpolation-space identities, Stein interpolation, real interpolation, Riesz convexity only on
  finite matrices, and nonlinear or sublinear variants require a source identity proof before use.
- A structure or hypothesis storing the desired intermediate bound assumes rather than proves the
  conclusion.
- A theorem name, bounded search, API `#check`, numerical example, or the catalog's `已验证` label
  supplies no human-source or machine-proof credit.

## Neighbor boundaries

`THM-M-0295` owns Hausdorff-Young, `THM-M-0297` Marcinkiewicz interpolation, and `THM-M-0374` the
generic interpolation label. They may eventually become explicit applications, contrasts, or
dependencies after statement and obligation freezes, but their wording and evidence do not select
or close this target.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe authenticates generic `Lp`, `MemLp`,
`ContinuousLinearMap.compLp`, `ContinuousLinearMap.compLpL`, and Hadamard three-lines interfaces.
The exact-name search found no Riesz-Thorin declaration. This is bounded discovery evidence, not an
exhaustive anchor or transitive-provenance audit and not proof of global absence.
