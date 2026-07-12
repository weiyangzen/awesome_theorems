# Scope map

## Included theorem family

- Critical planar percolation on a source-specified lattice, provisionally critical site
  percolation on the triangular lattice (equivalently its hexagonal faces).
- Discrete approximations of a simply connected planar domain with two marked boundary points and
  source-specified exploration, or Dobrushin, boundary conditions.
- The percolation exploration interface viewed modulo increasing reparametrization in a
  source-specified curve space.
- Weak convergence of its law as mesh tends to zero to chordal SLE with parameter `kappa = 6`,
  including only the domain and boundary regularity asserted by the selected primary result.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze: site versus
bond percolation and the lattice embedding; the critical occupation probability; the domain class,
prime-end or boundary-point interpretation, and discrete approximation rule; boundary colors and
interface orientation; the exploration path interpolation; the metric/topology on unparametrized
curves; weak convergence as probability measures or convergence in distribution; the Loewner
normalization and SLE driving Brownian-motion convention; stopping at the target point versus a
stopped/local formulation; and the order of domain, mesh, event, and limit quantifiers.

These choices change the proposition. In particular, convergence of crossing probabilities to
Cardy's formula is an essential nearby result but is not identical to convergence of interface
laws, and convergence of one interface does not by itself give the full collection-of-loops
scaling limit.

## Explicit exclusions

- Cardy's crossing formula or conformal invariance of crossing probabilities alone.
- A definition of SLE or the Loewner differential equation without the percolation convergence
  theorem.
- The full percolation loop ensemble, CLE6 identification, cluster-boundary ensemble, or
  near-critical scaling limit unless that exact stronger result is selected and crosswalked.
- Brownian intersection exponents, frontier dimensions, locality, or restriction properties as a
  substitute for the scaling-limit identification.
- Bond percolation on the square lattice, a general universality claim for arbitrary planar
  lattices, or an off-critical model without a source-checked transport.
- Assuming the desired convergence or SLE6 law in a structure and proving it by field projection.
- Simulated interfaces, numerical driving functions, physics predictions, or the metadata value
  `\u5df2\u9a8c\u8bc1` as mathematical or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose concrete probability
measures, discrete paths, the curve-space topology, mesh limit, and chordal SLE6 law rather than
packaging the conclusion as input data.
