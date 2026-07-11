# Scope map

## Preserved source scope

- Equation family: Laplace's equation.
- Boundary condition family: prescribed normal derivative (Neumann data).
- Historical attribution: Carl Neumann, 1877, as repository metadata only.
- Result kind: unspecified. The source says "problem", not whether the intended claim is
  solvability, uniqueness modulo constants, compatibility, regularity, or a representation formula.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the domain, dimension, scalar field,
boundary regularity and orientation, solution space, weak or classical Laplacian, trace/normal
derivative meaning, data space, compatibility condition, normalization or quotient by constants,
existence/uniqueness/regularity conclusion, and every constant dependency. Connected versus
disconnected domains, empty boundary, zero data, and low-dimensional cases require explicit scope.

## Explicit exclusions

- The Dirichlet or Robin problem as a substitute.
- A uniqueness claim without accounting for additive constants.
- An existence claim omitting the necessary zero-total-flux compatibility condition on a bounded
  domain (or the componentwise form when appropriate).
- A finite-dimensional graph Laplacian, half-space formula, or smooth-ball special case selected
  merely for convenient Lean APIs.
- The metadata label `已验证` as human-source or kernel evidence.

