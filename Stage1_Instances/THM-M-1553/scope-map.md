# Scope map

## Included first claim

- The fixed KdV normalization `u_t + 6 u u_x + u_xxx = 0`.
- A concrete tau function of space and time, the transform `u = 2 partial_x^2 log tau`, and the
  bilinear equation `(D_x^4 + D_x D_t) tau . tau = 0`.
- Explicit differentiability and nonvanishing/positivity assumptions sufficient for every derivative
  and logarithm; equality on a declared real or complex domain.
- The forward bilinear-to-KdV implication. A one- or multi-soliton result is a separate downstream
  corollary requiring an explicit tau formula, admissible parameters, and dispersion relation.

## Decisions reserved for statement phase

The inspected primary theorem must determine the scalar field and domain, derivative convention,
minimal regularity, whether `tau` is positive or merely nonzero, local versus global equality, and
the exact order of quantifiers. It must also verify the signs and scaling constants rather than
inheriting them from the legacy module.

## Explicit exclusions

- A claim that every nonlinear integrable system admits a Hirota representation.
- KP, Toda, sine-Gordon, or another equation substituted for the selected KdV theorem.
- Experimental/physical soliton claims, inverse-scattering completeness, or classification of all
  KdV solutions.
- An abstract certificate whose fields assume the bilinear-to-nonlinear bridge or tau identity.
- Bilinearity lemmas alone as proof of the KdV bridge.

The future statement must concretely define partial derivatives and the Hirota `D` polynomial, or
record a precise mathlib API blocker without weakening the mathematical claim.
