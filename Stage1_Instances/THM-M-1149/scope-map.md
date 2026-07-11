# Scope map

## Preserved source scope

- Equation family: Laplace's equation.
- Boundary condition family: prescribed boundary values (Dirichlet data).
- Historical attribution: Peter Dirichlet, 1850, as repository metadata only.
- Result kind: unspecified. The source says "problem", not whether the intended claim is
  solvability, uniqueness, regularity, a variational characterization, or a representation formula.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the domain, dimension, scalar field,
boundary regularity, solution and data spaces, classical or weak Laplacian, trace or pointwise
boundary meaning, existence/uniqueness/regularity conclusion, and every constant dependency.
Connectedness, boundedness, empty boundary, discontinuous data, irregular boundary points, and
low-dimensional cases require explicit scope.

## Explicit exclusions

- The Neumann or Robin problem as a substitute.
- A universal solvability claim for arbitrary domains and boundary data.
- A uniqueness claim without its domain and regularity/maximum-principle hypotheses.
- The disk Poisson formula, a finite graph Laplacian, or another convenient special case selected
  merely because Lean APIs exist.
- The metadata label `已验证` as human-source or kernel evidence.
