# Canonical Lean statement

## Declaration

`Stage1Instances.THM_M_0990.StatementShape` in `Statement.lean` is the canonical target. It says
that a row-wise jointly independent triangular array, satisfying a positive `2 + delta` Lyapunov
moment condition and eventually positive row variance, has normalized centered row sums converging
in distribution to the standard Gaussian law.

## Encoding decisions

- Row `n` consists of the first `n` entries `X n k`, for `k` in `Finset.range n`.
- All rows live on one probability space. Independence is `iIndepFun (X n) P`, which is stronger
  than and supplies joint independence for the used finite prefix.
- Centering subtracts the Bochner integral. The scale is the square root of the sum of mathlib
  variances, and eventual strict positivity excludes only asymptotically degenerate rows.
- The Lyapunov numerator is the sum of centered absolute `2 + delta` moments, expressed using
  `Real.rpow`; its denominator is the row scale to the same power.
- The conclusion uses mathlib `TendstoInDistribution` against any random variable having law
  `gaussianReal 0 1`. This avoids selecting a privileged realization of the standard normal.
- Measurability, finite second moments, and integrability of every Lyapunov moment are explicit.

The whole-row independence premise deliberately avoids pairwise independence, and no
characteristic-function convergence, Taylor bridge, or desired conclusion is included among the
hypotheses.

## Boundary and mutations

The proposition covers `delta > 0`; `delta = 0` is not a Lyapunov condition. Rows with zero total
variance may occur finitely often, while eventual positivity makes the asymptotic division
meaningful. Three separately elaborated mutations expose removal of the Lyapunov condition,
variance rather than standard-deviation normalization, and pairwise rather than joint
independence. They are intentionally not proved.

The source imports only `Mathlib.Probability.CentralLimitTheorem`; a deletion probe confirmed that
this single feature module already exports every API used. The project pins Lean `v4.29.0` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Elaboration establishes only that the exact proposition is well typed. No axiom, `sorry`, proof
closure, source acceptance, or theorem completion is claimed.
