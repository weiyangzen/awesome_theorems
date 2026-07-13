# Scope map

## Received claim

`Docs/researches/math_theorems.md` supplies the title "Calderon-Zygmund decomposition" and only the
gloss "function decomposition technique." That is a theorem-family label rather than an ordered,
truth-valued proposition. This intake freezes the family boundary and the choices required at the
statement gate; it does not invent a canonical theorem.

## Candidate classical boundary

A common Euclidean form starts with a scalar integrable function `f` and a positive threshold
`lambda`, selects pairwise disjoint cubes, and writes `f = g + sum_i b_i`. Typically `g` is bounded
by a dimension-dependent multiple of `lambda`; each `b_i` is supported in its cube and has zero
integral; and the total measure or total `L1` mass of the bad region is controlled by
`lambda^(-1) * ||f||_1`. This is a candidate shape only.

The exact source must settle all of the following:

1. Ambient space and measure: `Real^n` with Lebesgue measure, a dyadic measure space, a doubling
   metric-measure space, or another setting; dimension and all regularity assumptions.
2. Function class and codomain: real, complex, or Banach-valued; `L1`, local integrability,
   compact support, nonnegative functions, or a finite-measure restriction; representatives versus
   equivalence classes.
3. Selection geometry: open, closed, or half-open cubes; balls; dyadic grid; maximality;
   countability; pairwise disjointness; and any dilation or bounded-overlap convention.
4. Threshold premise and comparison: whether `lambda > 0`, whether a global average restriction is
   required, and whether selected averages are `>`, `>=`, or otherwise normalized.
5. Decomposition data: a single bad function versus a family `b_i`; pointwise or almost-everywhere
   equality; the exact definition of `g`; and measurability and integrability assertions.
6. Conclusions and constants: the pointwise bound on `g`, `L1` control, mean-zero statements,
   support, measure of the bad union, overlap after enlargement, dependence on dimension or the
   doubling constant, and whether all or only some conclusions are part of the root.
7. Boundary cases: zero function, empty selection, dimension zero, zero or infinite threshold,
   zero/infinite-measure cubes, infinite norms, null-set changes, and convergence of an infinite
   bad-part sum.

## Pinned Lean feasibility boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.MeasureTheory.Integral.Average` provides `setAverage_eq` and
  `setIntegral_setAverage_sub`, the latter expressing the mean-zero identity for subtracting a set
  average under integrability and finite-measure hypotheses.
- `Mathlib.MeasureTheory.Measure.Lebesgue.Basic` provides `Real.volume_Icc_pi` and measurable
  Euclidean box infrastructure.
- `Mathlib.MeasureTheory.Covering.Vitali` provides
  `Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall`.
- `Mathlib.MeasureTheory.Covering.Besicovitch` provides disjoint ball-covering infrastructure in
  suitable metric spaces.

These are ingredients, not a source-identical root declaration. They do not decide cubes versus
balls, constants, output packaging, or the canonical statement.

An immutable external lead exists at
`fpvandoorn/carleson@fdcce451b494680b1fd5534236a71d9b258860b2`, principally
`Carleson/TwoSidedCarleson/WeakCalderonZygmund.lean`. It supplies a kernel-checked bundle for
bounded complex functions of finite-measure support on a doubling metric-measure space, using
balls, a threshold above the global average, good-part bounds, localized mean-zero remainders,
overlap, measure, and `L1` estimates. It pins Lean `v4.30.0-rc2` and mathlib
`1a4917a18b30ea1333c195e597067fe044ac9176`, not the local pins. It was source-inspected but not
fetched into, built in, or imported by this worker. Exact source identity and the theorem-bundle
root transport also remain open. This credible out-of-closure proof lead supports provisional
`M1`, not `M0-P`.

## Explicit exclusions

- The Hardy-Littlewood maximal theorem or its weak `(1,1)` estimate used as a substitute root.
- Singular-integral boundedness (`THM-M-0299`) or the broader Calderon-Zygmund theory
  (`THM-M-0352`) used in place of the decomposition.
- The PDE Calderon-Zygmund estimate (`THM-M-1171`) or an elliptic regularity result.
- A ball decomposition silently identified with a cube or dyadic source statement.
- A structure which assumes the desired equality, cancellation, support, or norm bounds as data
  and then merely projects them.
- A finite, compactly supported, nonnegative, one-dimensional, or one-cube special case used as an
  unrestricted root.
- The untrusted `已验证` label, theorem-name match, source URL, or intake probe used as proof credit.

No canonical Lean expression, binder list, hypothesis list, conclusion, alternate transport, or
degenerate-case exclusion is frozen by this intake.
