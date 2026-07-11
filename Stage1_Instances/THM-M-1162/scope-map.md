# Scope map

## Preserved source scope

- Subject: a numerical-method family conventionally based on boundary integral formulations.
- Mathematical setting: an unspecified differential or partial differential boundary-value problem.
- Claimed action: numerical approximation using boundary data or boundary integrals.
- Attribution and period: multiple mathematicians, twentieth century.

This is all that the repository source fixes. It does not state a truth-valued theorem.

## Decisions required before statement freeze

The statement phase must identify a primary source and one exact theorem. It must freeze the PDE,
domain and boundary regularity, dimension and scalar field, boundary condition, solution concept,
fundamental solution and integral operator, trial/test spaces, mesh assumptions, discrete scheme,
stability or coercivity hypotheses, approximation quantity, norm, convergence rate, constants and
their dependencies. It must also address nonunique integral formulations, corners, singular data,
nullspaces, and degenerate or empty discretizations whenever relevant to the selected theorem.

## Explicit exclusions

- Treating the phrase "boundary element method" itself as a theorem.
- Substituting a generic Galerkin, finite-element, quadrature, Green-representation, or trace theorem.
- Choosing Laplace, Helmholtz, elasticity, or another model merely because Lean APIs are available.
- Reading the metadata label `已验证` as human proof or kernel evidence.
- Claiming convergence, stability, consistency, or an error estimate not present in an identified source.
