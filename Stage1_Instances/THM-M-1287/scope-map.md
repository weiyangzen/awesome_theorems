# Scope map

## Included claim

- An admissible bounded domain `Omega` in Euclidean space of dimension `n`, with finite positive
  Lebesgue volume.
- The first Dirichlet eigenvalue of the negative Laplacian, ultimately tied to a concrete spectral
  or Rayleigh-quotient definition.
- Comparison with a Euclidean ball `B` satisfying `volume B = volume Omega`:
  `lambda1 B <= lambda1 Omega`.
- The sharp equality characterization (a ball, up to the equivalence allowed by the source) only
  after its regularity and null-set conventions have been sourced.

## Decisions deferred to the statement phase

The primary-source theorem must determine `n` and its lower bound; whether domains are open,
connected, Lipschitz, or merely measurable/quasi-open; how `lambda1` is defined when classical
eigenfunctions are unavailable; and whether equality is literal, up to translation, or up to a
null/capacity-zero set. The statement must also freeze normalization of the Laplacian, volume,
Sobolev space, radius of the comparison ball, binder order, and degenerate cases.

## Explicit exclusions

- A perimeter isoperimetric inequality without the Dirichlet eigenvalue comparison.
- A one-dimensional interval-only result or a fixed-shape numerical estimate as a substitute.
- Neumann, Robin, higher-eigenvalue, graph-Laplacian, or Riemannian variants.
- Assuming the desired comparison or equality case as a structure field.
- Treating the metadata phrase or `verified` source label as mathematical or machine evidence.

The later Lean statement must expose concrete measure, domain, Sobolev/Dirichlet, Rayleigh quotient
or spectral interfaces. An abstract real-valued `lambda1` with the inequality assumed earns no
statement or proof credit.
