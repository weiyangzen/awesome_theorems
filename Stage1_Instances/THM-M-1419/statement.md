# Statement freeze

## Selected proposition

The canonical target is the finite-dimensional real, invertible, ergodic, two-sided splitting
form of Oseledets' multiplicative ergodic theorem. It is declared as
`Stage1Instances.THM_M_1419.OseledetsMultiplicativeErgodicTarget` in
`OseledetsStatement.lean`.

The binder order is: positive dimension `d`; measurable probability space `(Ω, μ)`; invertible
base transformation `T`; matrix field `A`; measure preservation and ergodicity; measurability of
`A` and `A⁻¹`; almost-everywhere invertibility; both logarithmic moment hypotheses; then the
existential exponent and splitting data. The conclusion supplies:

- a nonempty finite exponent index and strictly decreasing real exponents;
- a concretely measurable subspace field, expressed by measurable distance to each fiber rather
  than an invented measurable-space instance on `Submodule`;
- on one common conull set, an internal direct sum spanning the whole fiber, positive-dimensional
  summands, one-step equivariance, and the forward growth limit for every nonzero vector in every
  summand.

The forward product is fixed as
`A(T^(n-1)ω) * ... * A(Tω) * A(ω)`. The logarithm in the conclusion is the actual vector-norm
logarithm, not `log⁺`; invertibility and a nonzero input ensure the mathematical limit is not being
silently truncated. Dimension zero is excluded. Repeated exponents are represented by one
summand with higher finrank. Nonergodic exponent functions, singular cocycles, one-sided
filtrations, complex scalars, varying fiber dimension, singular-value-only conclusions, and
continuous time are different propositions and are not the selected target.

## Source boundary

The repository's two duplicate source rows say only "random-matrix Lyapunov exponents" and
"existence of Lyapunov exponents". They do not determine a numbered primary-source variant. The
selection above therefore makes the strongest conventional choices explicit and does not claim
`H0` or an exact theorem-number crosswalk. The primary-source audit and independent source review
remain downstream work. This statement phase freezes an exact, kernel-elaborated proposition; it
does not upgrade source fidelity or prove the proposition.

## Mutation boundary

`MutationWithoutInverseMoment` visibly removes inverse measurability and inverse moment data.
`MutationOneSidedBase` visibly changes `T : Ω ≃ Ω` to `T : Ω → Ω`. Both elaborate and print as
different expressions, demonstrating that these common weakenings are not silently accepted as
the canonical target. The positive-dimension binder and the placement of every conclusion under
one `∀ᵐ ω ∂μ` likewise expose the zero-dimensional and quantifier-scope boundaries directly in the
printed canonical expression.

## Environment and imports

Toolchain: `leanprover/lean4:v4.29.0`, Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. The repository pins mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the worker reused its existing compiled artifacts
read-only.

The direct imports are exactly:

1. `Mathlib.Analysis.Matrix.Normed`
2. `Mathlib.Dynamics.Ergodic.Ergodic`
3. `Mathlib.LinearAlgebra.DFinsupp`
4. `Mathlib.MeasureTheory.Function.L1Space.Integrable`
5. `Mathlib.Topology.MetricSpace.Pseudo.Defs`

Each owns a visible target surface: matrix operator norms, ergodicity/measure preservation,
`iSupIndep`, `Integrable`, and `Metric.infDist`. Narrow elaboration resolved these five direct
mathlib oleans and Lean `Init.olean`; no repository theorem module or separately owned target was
imported.

