# Scope map

## Received claim

The repository supplies only the title Cauchy integral theorem, attribution to Augustin Cauchy,
the year 1825, and the gloss "the integral of a holomorphic function along a closed curve is
zero." It supplies no formula, bibliography, definition of curve or integral, ambient domain,
topological condition, proof boundary, or exception list.

Read as a universal assertion for every closed curve in every holomorphy domain, the gloss is
false. On `U = Complex \ {0}`, the function `f z = 1 / z` is holomorphic and the positively
oriented unit circle is a closed curve in `U`, but its contour integral is `2 * pi * I`. This
counterexample is a scope diagnostic, not a replacement theorem.

## Candidate classical families

An accountable source review must select exactly one root before statement elaboration. Plausible
but currently uncredited families include:

1. A triangle, rectangle, disk boundary, or other simple contour whose filled region lies in an
   open neighborhood on which `f` is holomorphic.
2. Every sufficiently regular closed path in an open simply connected domain on which `f` is
   holomorphic.
3. Every sufficiently regular closed path in an open domain that is null-homotopic there, with
   the homotopy and regularity required by the proof made explicit.
4. A homological or winding-number-zero cycle formulation in which all indices outside the
   holomorphy domain vanish.
5. A primitive formulation: the integral of a derivative along every closed path is zero, paired
   with a separate theorem that the selected holomorphic functions admit primitives.

These statements differ in domains, hypotheses, curve objects, and proof obligations. They may be
related by checked implications after one source-exact root is selected, but are not interchangeable
at intake.

## Decisions required at statement freeze

1. Pin and independently review an exact primary or authoritative source edition, theorem and
   definition locators, assumptions, proof boundary, corrections, and errata.
2. Fix `f : Complex -> Complex` versus Banach-valued functions and all completeness assumptions.
3. Fix the domain as an open set, region, disk, simply connected set, neighborhood of a filled
   contour, or another source-defined object.
4. Fix the curve object: parametrized interval map, mathlib `Path`, piecewise smooth contour,
   rectifiable path, simple closed curve, chain, or cycle.
5. Fix regularity at endpoints and joins, allowed self-intersections, constant paths, orientation,
   reparametrization, and whether the curve image is required to lie in the domain.
6. State the missing topological/geometric premise: filled-interior containment, simple
   connectedness, null-homotopy, zero winding numbers, or existence of a primitive.
7. Fix the contour-integral encoding: scalar interval integral, `Complex.circleIntegral`,
   boundary-of-rectangle expression, or `MeasureTheory.curveIntegral` of a one-form, and compile
   every claimed transport.
8. Decide classical Cauchy versus Cauchy-Goursat regularity: holomorphicity alone, continuity on a
   boundary plus interior differentiability, or differentiability off a countable set.
9. Freeze ordered binders, universes, all explicit hypotheses, exact conclusion, profiles, minimal
   imports, expression/environment hashes, and all four required mutation classes.

## Boundary cases

The statement phase must resolve the empty domain, empty or constant path, zero-radius circle,
degenerate rectangle, reversed orientation, repeated points, self-intersections, paths retracing
their image, non-simple null-homotopic paths, boundary-only differentiability, punctured domains,
and whether the whole complex plane or disconnected open sets are included.

## Explicit exclusions

- The catalog gloss repaired by an unstated simply-connectedness or filled-interior hypothesis.
- Only a rectangle, triangle, or circle theorem substituted for a general closed-curve theorem
  unless the accepted source selects that restricted root.
- The Cauchy integral formula, which represents function values by boundary integrals and is owned
  separately by `THM-M-0222`.
- The residue theorem (`THM-M-0223`), Morera's converse, primitive existence, path independence,
  or the Poincare lemma used as the root without a checked source equivalence.
- A result requiring a supplied primitive used as if it proved that every source-selected
  holomorphic function has one.
- A structure or hypothesis that stores the desired zero integral, homotopy, or primitive.
- The untrusted `已验证` label, a theorem-name match, an adjacent API check, or the displayed
  counterexample used as H0 or M0 evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, restricted rectangle and circle results elaborate,
as do curve-integral and smooth-homotopy APIs. Mathlib's primitive file explicitly leaves the
simply-connected-domain extension as future work. These are intake discovery facts, not an
exhaustive anchor audit, exact statement, or proof-credit decision.
