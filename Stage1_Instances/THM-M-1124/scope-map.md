# Scope map

## Provisional included theorem family

- Planar Brownian motions or excursions in a plane or half-plane geometry, as fixed by the selected
  primary Lawler-Schramm-Werner result.
- A nonintersection or disconnection event defined up to a source-specified large spatial or time
  scale, with an exponent obtained from its asymptotic decay.
- The source's admissible multiplicity or real parameter range and the exact exponent convention.
- An explicit exponent value derived using Schramm-Loewner evolution, not merely existence of a
  decay rate or conformal invariance of an unrelated model.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze: plane versus
half-plane geometry; Brownian path, excursion, packet, or restriction-measure encoding; starting
and stopping sets; independence; whether paths must avoid each other or merely fail to disconnect;
the definition of the exponent as a limit, logarithmic asymptotic, or two-sided comparison; the
number of paths or packet weights and their parameter range; formula and normalization; degenerate
zero-path and boundary cases; and the order of scale, parameter, and error quantifiers.

These choices distinguish inequivalent results in the authors' series and change the Lean domains,
binders, hypotheses, and conclusion.

## Explicit exclusions

- The definition or existence of chordal/radial SLE alone.
- Smirnov's conformal invariance theorem, Cardy's formula, or the SLE/percolation identification
  scheduled as neighboring targets.
- Hausdorff-dimension consequences, self-avoiding-walk exponents, or uniform-spanning-tree results
  unless that exact result is selected from the source record.
- A special numerical exponent substituted for a theorem asserting a parameterized family.
- A finite simulation, heuristic scaling law, or a structure that contains the desired asymptotic
  or exponent formula as assumed data.
- The repository metadata value `已验证` as source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose Brownian paths,
stopping geometry, avoidance/disconnection events, probabilities, limits, parameter domains, and
the asserted exponent formula concretely.
