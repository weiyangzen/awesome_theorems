# Scope map

## Included theorem family

- Independent site percolation at critical parameter `p = 1/2` on the triangular lattice, or the
  exactly dual hexagonal-face-coloring presentation used by the selected primary theorem.
- A sequence of mesh-size discretizations of a source-specified simply connected planar domain,
  with marked boundary points or arcs and explicitly defined boundary approximation.
- The source's crossing event between prescribed boundary arcs and its probability under the
  critical product measure.
- Convergence as mesh tends to zero to Cardy's formula, with conformal invariance stated either by
  an explicit conformal-map expression or by its source-approved equivalent.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary result. It must freeze: triangular
vertices versus hexagonal faces; lattice orientation and mesh normalization; the product sample
space and critical parameter; domain class (for example Jordan or more general simply connected
domains); ordered marked boundary points, prime ends, or boundary arcs; discrete domain and marked
point approximation; the exact open/closed crossing event; boundary conditions; the Cardy function
and conformal normalization; pointwise versus uniform convergence; and the order of all domain,
mesh, approximation, and error quantifiers. Degenerate marked points, nonsimple boundaries,
disconnected approximations, and mesh sequences that do not satisfy the source hypotheses must not
be silently included.

These choices change the Lean domains, binders, hypotheses, and conclusion. In particular,
conformal invariance of one crossing probability does not automatically assert convergence of the
entire percolation configuration or of exploration paths.

## Explicit exclusions

- Cardy's nonrigorous prediction by itself, Kesten's critical-probability theorem, Russo-Seymour-
  Welsh estimates, or discrete holomorphicity alone as a substitute for the limiting theorem.
- Full convergence of exploration interfaces to `SLE_6`, a quad-crossing configuration-space
  scaling limit, or conformal invariance of all observables unless selected from an exact source
  theorem and mapped separately.
- Bond percolation on the square lattice, off-critical percolation, other lattices, or dependent
  models.
- A statement assuming Cardy's limit, conformal invariance, or the desired convergence inside a
  structure and merely projecting that field.
- A finite-mesh symmetry identity, Monte Carlo agreement, numerical evaluation of Cardy's formula,
  or physics universality heuristic.
- The repository metadata value `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the lattice model,
probability measure, discrete approximation, crossing event, conformal data, limiting expression,
and convergence mode rather than hiding the desired conclusion in an assumption.
