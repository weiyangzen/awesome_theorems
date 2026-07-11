# Scope map

## Included claim

- A cadlag Levy process `X` with values in a finite-dimensional real space (initially `R^d`),
  starting at zero and having stationary independent increments.
- A fixed truncation convention, initially the unit ball, and a Levy measure `nu` satisfying
  `integral (min 1 |x|^2) d nu < infinity` and no mass at zero.
- A pathwise decomposition, simultaneously in time, into deterministic drift, a Gaussian Brownian
  component, a compensated Poisson integral over small jumps, and an uncompensated Poisson integral
  over large jumps.
- The independence relationships among the continuous Gaussian component and the Poisson random
  measure, together with the convergence mode needed to define the compensated small-jump term.

## Statement-phase decisions

The selected source must fix the state space, filtration and adaptedness conditions, time domain,
cadlag modification, equality mode (indistinguishability or almost-sure equality for each time),
construction versus representation formulation, and uniqueness content. It must also fix the sign
and cutoff convention for the drift, the covariance operator, the definition of the jump measure,
the compensated-integral convergence mode, and all measurability and sigma-finiteness assumptions.
The formal statement must explicitly test time zero, zero Gaussian covariance, finite-activity and
zero Levy measures, and changes of truncation.

## Explicit exclusions

- The Levy-Khintchine characteristic-exponent formula alone.
- A compound Poisson or finite-activity special case presented as the full decomposition.
- A semimartingale decomposition assumed as input, or an arbitrary process already assumed to have
  the four required components.
- A decomposition only in distribution when the selected source asserts a pathwise representation.
- A one-dimensional theorem substituted without a checked finite-dimensional transport.

The later formal target must connect an actual Levy process and its jump measure to every component,
or record a precise missing-API blocker rather than weakening the theorem.
