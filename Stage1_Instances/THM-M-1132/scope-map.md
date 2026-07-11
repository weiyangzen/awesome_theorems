# Scope map

## Preserved source scope

- Subject: a fundamental solution associated with the heat equation.
- Named object: the heat kernel, described alternatively as a Gaussian kernel.
- Historical scope: nineteenth century and multiple mathematicians.
- Intended setting, as far as the phrase supports: an unspecified Euclidean or other heat-flow
  setting. No particular dimension, domain, coefficient, or boundary condition is fixed.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the ambient space and dimension,
scalar field, time domain, heat-operator sign and diffusivity, the kernel formula and normalization,
the meaning of derivatives and integration, and the solution/initial-data class. It must state which
property constitutes the theorem: satisfying the PDE for positive time, mass one and positivity,
convergence to a Dirac mass, convolution producing solutions, semigroup behavior, uniqueness, or a
specified conjunction. Boundary and degenerate cases (`t = 0`, zero diffusivity, dimension zero,
and empty or bounded domains where applicable) need explicit treatment.

## Explicit exclusions

- A bare identity about `Real.exp` or a normal density with no heat-equation semantics.
- A heat kernel on a manifold, graph, bounded domain, or discrete space chosen without source support.
- Treating positivity, normalization, the PDE identity, fundamental-solution convergence, and
  uniqueness as interchangeable claims.
- Treating the metadata label `已验证` as human-source or kernel evidence.
- Claiming the familiar formula `(4 * pi * t)^(-n/2) * exp (-|x|^2 / (4*t))` before the coefficient,
  dimension, domains, and boundary behavior have been sourced and frozen.
