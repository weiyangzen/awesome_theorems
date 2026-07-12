# Scope map

## Included claim

- The classical one-dimensional periodic Carleson theorem for complex-valued `L^2` functions.
- Fourier coefficients taken against the characters of the circle.
- Symmetric partial sums over integer frequencies `-N <= n <= N`.
- Pointwise convergence to the input function outside a Haar-null set.

## Decisions required at statement freeze

The statement phase must inspect a stable primary-source edition and freeze the circle model and
period, normalization of Haar measure and Fourier coefficients, whether the source starts with an
actual function or an `L^2` equivalence class, the representative used in the conclusion, the exact
finite frequency set, and whether convergence is expressed by a sequence limit or by convergence of
a directed family. It must also decide the treatment of real-valued functions, endpoints in an
interval presentation, equality modulo null sets, cutoff `N = 0`, and changes of representative.

In Lean, `fourierCoeff` accepts an `Lp` value and `fourierLp` supplies the `L^2` Fourier basis, while
pointwise evaluation requires a chosen representative. The bridge between these levels is part of
the theorem statement, not harmless notation. The already available `hasSum_fourier_series_L2`
asserts convergence in the `L^2` topology and must not be substituted for almost-everywhere
pointwise convergence.

## Explicit exclusions

- Carleson-Hunt convergence for every `L^p`, `1 < p < infinity`, as the target; it is a stronger
  later extension and may only be used through a checked specialization.
- Mere `L^2`-norm convergence, Cesaro/Fejer convergence, convergence in measure, or existence of a
  subsequence.
- Pointwise convergence under extra smoothness, continuity, bounded variation, or absolute
  summability assumptions.
- A maximal-operator inequality without a checked derivation of the almost-everywhere conclusion.
- A structure or hypothesis that assumes the desired convergence.
- The repository label `已验证` as human-proof or kernel evidence.

No exact Lean target is frozen during intake. These boundaries prevent a later implementation from
quietly replacing Carleson's theorem by the much easier Hilbert-space Fourier expansion already in
mathlib.

