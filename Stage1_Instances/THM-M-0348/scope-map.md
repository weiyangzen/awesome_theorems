# Scope map

## Included topic boundary

- A source-identified theorem jointly associated with Riesz and Fejer.
- If the intended theorem is about Fourier convergence: the exact Fourier domain, coefficient
  convention, partial sums or summability means, function class, and convergence mode.
- If the intended theorem is factorization: the exact nonnegative trigonometric/Laurent polynomial
  domain, coefficient field, degree/support condition, and analytic polynomial factor.
- All hypotheses and boundary cases stated by the selected source.

## Ambiguities to resolve at statement freeze

The repository gloss "convergence of Fourier series" does not decide among ordinary partial-sum
convergence, Cesaro/Fejer summability, convergence in norm, pointwise convergence, almost-everywhere
convergence, or a coefficient realization result. It also does not specify the circle or interval,
period normalization, real or complex scalars, continuity or integrability hypotheses, or whether
the conclusion is uniform, pointwise, almost everywhere, or in an `L^p` norm.

A second established reading of the paired name is Fejer-Riesz factorization: a nonnegative
trigonometric polynomial on the unit circle is the squared modulus of an analytic polynomial.
That is not a Fourier-series convergence result. The statement phase must inspect an immutable
source and determine whether the repository title, gloss, attribution, or date is erroneous before
freezing any proposition.

Boundary cases requiring an explicit source decision include the zero polynomial, vanishing on the
circle, constant polynomials, endpoints/period representatives, coefficient symmetry, exceptional
null sets, and the endpoint values of any `p` range.

## Explicit exclusions

- Fejer's theorem on Cesaro means as a silent replacement for the paired-name entry.
- The Riesz-Fischer theorem, the Riesz representation theorems, or Riesz-Markov-Kakutani.
- Carleson's almost-everywhere convergence theorem or a generic Cesaro lemma.
- Parseval's identity, density of Fourier monomials, or `L^2` Fourier convergence without a checked
  source-to-target bridge.
- Fejer-Riesz factorization unless a source review establishes that it is the intended target.
- A theorem made tautological by assuming the desired convergence or factorization as typeclass or
  structure data.
- The inventory label `verified` as evidence of human proof fidelity or kernel closure.

No canonical Lean target is frozen at intake because the source record does not identify one.
