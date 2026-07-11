# Scope map

## Included claim

- A bounded domain `Omega` in real finite-dimensional Euclidean space, with the boundary regularity
  needed by the chosen source (typically a Lipschitz or extension domain).
- The first-order Sobolev space `W^{1,p}(Omega)` and Lebesgue space `L^q(Omega)`.
- Compactness, not merely continuity, of the canonical inclusion in the strictly subcritical range.
- For `1 <= p < n`, the range `1 <= q < p*`, where `p* = np/(n-p)`; for `p >= n`, finite target
  exponents allowed by the selected source.

## Statement-phase decisions

The primary source must fix whether the scalar field is real or complex, whether `Omega` is open and
connected, its exact boundary/extension hypothesis, use of integer versus real dimension, and
whether `p = 1`, `p = n`, `n = 1`, `q = 1`, or `q = infinity` occur. It must also fix whether
compactness is expressed by a compact operator, compact map, subsequence convergence, or relative
compactness of bounded sets. Binder order, universes, measure restrictions, and norm conventions
must follow those choices.

## Explicit exclusions

- The continuous Sobolev embedding alone, the critical endpoint `q = p*`, or an unbounded-domain
  version without additional tightness hypotheses.
- Rellich compactness for abstract self-adjoint operators as a substitute for the Sobolev theorem.
- A finite-dimensional approximation or one-dimensional special case presented as the full claim.
- A structure or hypothesis that assumes the desired compact inclusion.

The later statement must use concrete Sobolev/Lebesgue objects and an actual compactness predicate,
or record the precise missing mathlib interface without weakening the human claim.
