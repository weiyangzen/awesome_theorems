# Scope map

## Preserved catalog scope

The intake preserves the classical complex-analytic residue-theorem family indicated by the title,
Cauchy attribution, 1831 date, complex-analysis category, and gloss relating contour integrals to
residues. A later statement phase may freeze a proposition only after an immutable authoritative
source and its incorporated definitions are selected and independently reviewed.

A standard candidate shape, recorded only to expose the missing decisions, is

`integral of f around gamma = 2 * pi * i * sum over poles a of windingNumber gamma a * residue f a`.

This formula is not the canonical statement and receives no proof credit at intake.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved source:

1. The source edition, theorem/section/page, incorporated definitions, proof boundary, correction
   and errata history, and independent source review.
2. The ambient open set or region and whether it must be connected, simply connected, bounded, or
   merely contain the contour image and relevant winding-number support.
3. The contour representation: a circle, piecewise differentiable closed path, cycle, chain, or a
   finite union, including orientation, regularity, parametrization, and integral convention.
4. The function class and locality assumptions: meromorphic on which neighborhood, holomorphic off
   which singularities, behavior at infinity, and whether vector-valued or scalar-valued variants
   are in scope.
5. How poles are selected and shown finite, whether removable singularities are included, how pole
   multiplicity is represented, and whether the pole set is explicit or derived.
6. The exact residue definition: Laurent coefficient of exponent `-1`, punctured-neighborhood
   limit for a simple pole, contour integral normalization, or a checked equivalent.
7. The conclusion convention: weighted winding-number sum for a general contour, an unweighted sum
   for a positively oriented simple boundary, or a circle-only specialization, including the sign
   and factor `2 * pi * i`.
8. Every universe, ordered binder, hypothesis, conclusion clause, alternate transport, foundation,
   trusted-base, and computation policy.

These alternatives are related but not definitionally identical. They form a resolution ledger,
not a theorem statement.

## Degenerate and mutation cases

Source and statement review must explicitly dispose of a constant or self-intersecting closed path,
reversed orientation, zero-radius circles, no poles, removable singularities, repeated pole-list
entries, poles outside the contour, poles on the contour, winding number zero or greater than one,
an identically zero function, non-meromorphic points, and an unbounded or non-simply-connected
domain. Removed meromorphicity, changed contour domain, changed binder scope, and boundary contact
must be mutation-tested later. No case is silently excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-0221` separately owns the Cauchy integral theorem and `THM-M-0222` the Cauchy integral
  formula. Either may become a proof dependency, but neither is the residue theorem by itself.
- `THM-M-0232` (Rouche's theorem) and `THM-M-0233` (argument principle) are consequences or close
  relatives in common developments; their statements and evidence are not inherited.
- A single-pole circle computation, the Cauchy formula, a logarithmic-derivative limit, a residue
  definition, or a rational-function example cannot substitute for the source-selected root.
- A pole-free special case, an unweighted simple-contour formula selected without source support,
  or a structure storing the desired equality is not the general theorem.
- The untrusted `已验证` label and adjacent API checks supply no H0 or M0 evidence.

## Formal boundary

No canonical Lean proposition is frozen. Pinned mathlib exposes `circleIntegral`, Cauchy integral
formulas, `MeromorphicAt`, `MeromorphicOn`, `meromorphicOrderAt`, and
`meromorphicTrailingCoeffAt`; the intake probe authenticates only these adjacent interfaces. The
bounded source search found no declaration connecting a general contour integral to a finite
weighted sum of complex residues. Exact target elaboration, minimal imports, residue encoding,
checked alternate forms, expression fingerprint, and mutations belong to
`S56-M-0223-STATEMENT`.
