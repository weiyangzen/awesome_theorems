# Scope map

## Preserved source scope

- Subject: a solution of an unspecified differential or partial differential equation.
- Location: behavior at the boundary of an unspecified domain.
- Claimed property: unspecified regularity, described by the repository as a "boundary estimate".
- Historical scope: twentieth-century work by multiple mathematicians; no unique named theorem.

This is the complete scope justified by the repository source. It is intentionally not promoted to
a more precise theorem.

## Decisions required before statement freeze

The statement phase must obtain a primary theorem and freeze the differential operator (elliptic,
parabolic, or otherwise), weak/classical solution notion, dimension and scalar field, domain and
boundary smoothness, boundary condition, coefficient assumptions, forcing data, regularity spaces,
norms, constants and their dependencies, local/global character, and all compatibility conditions.
It must also cover degenerate dimensions, empty boundary, zero data, and endpoint exponents where
the selected theorem admits them.

## Explicit exclusions

- A trace theorem for arbitrary Sobolev functions as a substitute for PDE solution regularity.
- An interior estimate, maximum principle, or compact-support Sobolev inequality.
- A Schauder, Calderon-Zygmund, harmonic, Dirichlet, or Neumann theorem chosen only because its API
  is convenient rather than because a primary source identifies it.
- The abstract `BoundaryRegularityProblem` package in the legacy module as the source theorem.
- The metadata label `已验证` as human-source or kernel evidence.

The legacy module's selected compact-support/zero-trace family is a discovery proposal only and is
not adopted by this intake because it would broaden or substitute the unidentified source claim.
