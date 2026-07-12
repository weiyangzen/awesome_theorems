# Scope map

## Included theorem family

- A random oriented curve in a simply connected planar domain between two source-specified
  boundary points or prime ends, transported to a standard chordal domain.
- A source-specified form of conformal invariance and the domain Markov property.
- The chordal Loewner evolution of the remaining domain, with hydrodynamic normalization and a
  capacity parametrization fixed explicitly.
- Schramm's conditional conclusion that the real driving process has the source-stated Brownian
  form (commonly a scaled Brownian motion, with scale recorded by an SLE parameter).

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary result. It must freeze: chordal versus
radial geometry; the domain and marked endpoints; whether curves are simple, non-self-crossing, or
hulls modulo reparametrization; the curve sigma-algebra/topology; treatment of boundary regularity
and prime ends; conformal covariance versus equality in law; the precise filtration and domain
Markov conditional law; the half-plane-capacity convention; existence and continuity of the
Loewner driving function; Brownian variance convention; the parameter domain and whether positivity
or degeneracy is allowed; and the direction of every implication.

These choices alter domains, binders, hypotheses, and conclusions. In particular, the familiar
notation `SLE_kappa` does not determine whether `sqrt(kappa) B_t` or a standard Brownian driver with
a different Loewner coefficient is meant.

## Explicit exclusions

- The bare definition of an SLE process as the Loewner chain driven by Brownian motion.
- Assuming a structure field that already says the driver is Brownian and projecting that field.
- Existence, uniqueness, trace regularity, Hausdorff dimension, restriction, locality, reversibility,
  or duality results unless they occur in the selected source theorem.
- Identification of a particular lattice model's scaling limit with SLE, including percolation,
  loop-erased random walk, uniform spanning tree, or Ising interfaces.
- Cardy's formula, Smirnov's conformal-invariance theorem, or CFT/SLE correspondence as substitutes.
- Numerical simulations, pictures of Loewner traces, or the repository metadata value `已验证` as
  human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later formal target must expose the curve/hull
space, conformal transport, conditional-law hypothesis, Loewner transform and normalization, and
Brownian-law conclusion rather than packaging the result into assumed data.
