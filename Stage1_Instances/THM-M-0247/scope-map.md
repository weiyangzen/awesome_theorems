# Scope map

## Included theorem family

- A real- or complex-valued summable periodic function on one angular period.
- Its harmonic conjugate in the unit disk and almost-everywhere nontangential boundary value, with
  the source principal-value formula
  `g(theta) = -(1/(2*pi)) p.v. integral f(theta+alpha)/tan(alpha/2) d alpha`.
- A source threshold `R` and the superlevel set `E_R = {theta | |g(theta)| > R}`. The printed
  theorem calls `R` an arbitrary number without an explicit sign condition; the statement phase
  must determine whether to preserve that literal domain or check a transport to the standard
  meaningful weak-type domain `R > 0`.
- Kolmogorov's absolute-constant estimate
  `Mes(E_R) * R <= C * integral |f(theta)| d theta`, allowing the source's printed strict `<` to be
  retained or transported to a modern non-strict formulation only by a checked argument.

This is the periodic circular Hilbert/conjugate-function weak `(1,1)` endpoint bound. The source
uses `[-pi, pi]` and angular Lebesgue measure, whose full mass is `2*pi`.

## Statement decisions

The source passage identifies a precise mathematical theorem, but these representation decisions
belong to the dependent statement phase and receive no intake proof credit:

1. Use an angular circle with its unnormalized length measure, or use `AddCircle.haarAddCircle` and
   explicitly transport the factor `2*pi` into the absolute constant.
2. Select real or complex inputs and state the checked complexification bridge if both are credited.
3. Encode `f` as an integrable representative or an `L^1` class, and make invariance under
   almost-everywhere representative changes explicit.
4. Define `g` through the disk harmonic conjugate and nontangential boundary limit, the circular
   principal value, or the Fourier multiplier. Any alternate definition needs a checked bridge.
5. Fix the additive constant/zero Fourier mode of the conjugate. The weak estimate is not invariant
   under arbitrary constant shifts.
6. Fix ordered binders for the absolute constant, input, conjugate witness, threshold, and set;
   decide strict versus non-strict superlevel sets and source strictness.

Boundary cases to test include `f = 0`, constant and mean-zero inputs, null-set representative
changes, zero measure superlevel sets, thresholds tending to zero, and the excluded threshold
`R = 0` or `R = infinity` encodings.

## Explicit exclusions

- Marcel Riesz's strong `L^p` conjugate-function theorem for `1 < p < infinity` (`THM-M-0349`).
- A generic Markov/Chebyshev bound applied after assuming that the conjugate already lies in `L^1`.
  Kolmogorov's theorem is precisely useful because an `L^1` conjugate need not be integrable.
- Only the `p = 2` Fourier-basis isometry, a Fourier coefficient definition, or a postulated bounded
  operator whose fields already contain the requested estimate.
- Theorem II (`|g|^(1-epsilon)` integrability) or Theorem III (mean convergence of Fourier sums) in
  the same paper as substitutes for Theorem I.
- Real-line Hilbert-transform weak type, higher-dimensional singular integrals, maximal conjugate
  operators, weighted estimates, BMO endpoints, or sharp-constant refinements without checked
  source-to-target transports.
- The repository label `已验证`, the primary-source citation, or the Lean probe as proof evidence.

No canonical Lean expression, expression fingerprint, obligation registry, or discovery-protocol
hash is frozen during this intake.
