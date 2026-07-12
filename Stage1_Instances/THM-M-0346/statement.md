# Canonical Lean statement

## Frozen target

`Statement.lean` freezes the repository claim as the classical complex `L²` Carleson theorem on
the unit additive circle. For every
`f : Lp ℂ 2 AddCircle.haarAddCircle`, the symmetric sums over the inclusive integer interval
`[-N, N]` tend to the canonical `Lp` coercion `f x` for Haar-almost every `x` as `N : ℕ` tends to
infinity.

The period is `T = 1`; `AddCircle.haarAddCircle` is mathlib's probability-normalized Haar measure.
The coefficient is mathlib's `fourierCoeff`, whose characters use
`exp (2 * pi * I * n * x / T)`. The target quantifies over `Lp` classes, and the a.e. conclusion
makes evaluation independent of the representative chosen by the `Lp` coercion. The cutoff begins
at `N = 0`; this causes no boundary exception. The codomain is complex. The real-valued theorem is
not separately included because it is not the frozen repository claim.

Canonical declaration: `Stage1.THM_M_0346.CarlesonTarget`.

Minimal direct import: `Mathlib.Analysis.Fourier.AddCircle`. No broader umbrella import is used.

## Fidelity boundary

This is the literal formal expansion of the repository's claim that the Fourier series of every
`L²` function converges almost everywhere. It is not `hasSum_fourier_series_L2`: that existing
theorem gives convergence in the `L²` topology. It is also not Cesaro convergence, convergence in
measure, a subsequential limit, a smooth-function restriction, or the stronger Carleson-Hunt
`L^p` theorem.

The earlier intake's primary-source pinpoint and errata review remain human-source debt (`H3`) and
belong to the source/anchor audit. They do not prevent this exact repository target from being
typed. No proof of `CarlesonTarget` is supplied or claimed in this phase; machine debt remains open.

## Statement receipt

- Item: `S56-M-0346-STATEMENT`
- Base revision: `c9694802ae049af37973e49a65f11b833135333f`
- Lean toolchain: `leanprover/lean4:v4.29.0`
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Result: exact target and its helper definition elaborate with exit code 0.
- Status boundary: self-tested statement-phase work only; master acceptance is pending, and neither
  theorem proof nor theorem completion is claimed.

