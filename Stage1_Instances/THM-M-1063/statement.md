# Exact Lean statement

The canonical expression is `AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple` in
`DonskerTarget.lean`. It quantifies one probability space, an i.i.d. sequence `X : ℕ → Ω → ℝ`,
its positive standard deviation `sigma`, the full sequence of polygonal path random variables
`W`, and a continuous-path standard Brownian random variable `B` on an independently quantified
probability space. The conclusion
is mathlib's weak convergence of laws in `C(Set.Icc 0 1, ℝ)`:

```lean
TendstoInDistribution W atTop B (fun _ ↦ P) P
```

## Frozen conventions

- `X 0` is the first increment and `∑ i in Finset.range k, X i ω` is the partial sum after `k`
  increments; the empty sum is zero.
- For `n > 0`, `polygonalValue` linearly interpolates between the partial sums at mesh points
  `k / n` and divides by `sigma * Real.sqrt n`. The floor index is clipped at `n - 1`, so `t = 1`
  evaluates to the sum of exactly the first `n` increments. For `n = 0` the path is defined to be
  zero; this totalization does not affect the `atTop` limit.
- Identical distribution is stated against `X 0`; independence is `iIndepFun X P`.
- The moment assumptions are `MemLp (X 0) 2 P`, zero Bochner integral, and
  `Var[X 0; P] = sigma ^ 2`, with `0 < sigma` excluding the degenerate law.
- `IsStandardBrownian` fixes the limit by continuous sample paths, mathlib's joint Gaussian-process
  predicate, zero mean, and covariance `min s t`. Thus it does not assume the desired convergence.
- The path-space measurable structure is explicitly quantified with `BorelSpace`; this avoids an
  untracked local instance while forcing it to be the Borel structure of the uniform topology.

## Minimal pinned imports

The target elaborates with exactly two direct imports:

```lean
import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
```

The first owns `TendstoInDistribution`, probability measures, and the moment/independence APIs
re-exported through its dependency closure. The second is required for `IsGaussianProcess`. No
Brownian/Wiener-process declaration exists in pinned mathlib at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, so the exact standard-Brownian predicate is defined
locally rather than replaced by an abstract convergence hypothesis.

## Scope and status

This phase freezes and kernel-elaborates the exact proposition only. It supplies no inhabitant of
that proposition and claims no proof, H0, M0, audit completion, or theorem completion. The next
anchor-audit phase must determine the available proof infrastructure for the locally explicit
Brownian and polygonal-walk formulation.
