# Scope map

## Included topic boundary

- Interpolation results used in harmonic analysis.
- Endpoint data, interpolation parameters, intermediate exponents, operator assumptions, and the
  norm bound or function-space conclusion stated by the exact source eventually selected.
- Measure-space, scalar-field, measurability, linearity or sublinearity, and endpoint conditions
  needed by that result.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different theorem families:

1. **Riesz-Thorin:** a linear operator with two strong-type endpoint bounds has an interpolated
   strong-type `L^p -> L^q` bound, normally proved by complex interpolation.
2. **Marcinkiewicz:** a sublinear or quasilinear operator with weak-type endpoint bounds has a
   strong-type intermediate bound under parameter and measure-space restrictions.
3. **Hadamard three-lines:** an analytic function on a strip obeys a log-convex bound between its
   two boundary bounds.
4. **Interpolation spaces:** a real or complex interpolation functor produces an intermediate
   space, embedding, or norm equivalence from a compatible couple.

The source must freeze one proposition, ordered binders, normalization of interpolated exponents
and constants, hypotheses, conclusion, and boundary cases. It must also explain why this generic
record is not merely a duplicate of the separately cataloged Riesz-Thorin (`THM-M-0296`) or
Marcinkiewicz (`THM-M-0297`) target.

## Explicit exclusions

- Selecting Riesz-Thorin or Marcinkiewicz solely because those are familiar examples.
- Substituting Hadamard three-lines, a finite-dimensional convexity inequality, polynomial
  interpolation, Sobolev interpolation, or Craig logical interpolation for an unidentified claim.
- Treating an abstract interpolation operator whose fields assume the desired result as a proof.
- Treating the repository label `已验证` or an available mathlib theorem as source fidelity or
  proof credit for this target.

No canonical Lean target is frozen at intake. Degenerate cases such as equal endpoints, parameter
`0` or `1`, exponent infinity, zero endpoint bounds, and failure of sigma-finiteness remain open.
