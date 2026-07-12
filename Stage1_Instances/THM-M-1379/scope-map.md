# Scope map

## Preserved source scope

The intake preserves only the name "Hamilton-Jacobi equation," the broad description "the PDE
formulation of classical mechanics," the Hamilton/Jacobi attribution, and the year 1837. It does
not treat that label as a proposition. The manifest's ODE category conflicts with the PDE gloss;
this is an unresolved catalog boundary, not permission to choose an encoding.

A later statement phase may select a root only from an immutable, independently reviewed source
passage. Possible mathematical components, none credited here, include:

- a configuration space, its cotangent or phase-space model, and a scalar time domain;
- a Hamiltonian and an action or principal function with source-specified regularity;
- a time-dependent equation of the schematic form `partial_t S + H(q, d_q S, t) = 0`;
- a stationary equation of the schematic form `H(q, d_q S) = E`;
- a relationship between solutions and Hamiltonian characteristic curves; and
- a canonical transformation, action-principle derivation, or PDE solution theorem, if and only if
  an approved source selects it; a complete-integral claim remains reserved to `THM-M-1380` absent
  an explicit cross-target reallocation decision.

## Decisions required at statement freeze

The statement phase must freeze all of the following from the selected source rather than from
textbook convention:

1. The exact edition, theorem/equation/page locator, incorporated definitions, proof boundary,
   corrections or errata, translation if needed, and independent review.
2. Whether the root is an equation definition, derivation, equivalence, characteristics theorem,
   existence/uniqueness result, or canonical-transformation theorem, while preserving the separate
   `THM-M-1380` complete-integral boundary.
3. Time-dependent versus stationary form, including sign, time orientation, energy parameter,
   normalization, and physical-units conventions.
4. The configuration and phase spaces, dimensions, scalar field, manifolds or coordinate charts,
   cotangent/covector model, and every Lean universe and typeclass assumption.
5. The Hamiltonian's domain, time dependence, differentiability, convexity, coercivity, and any
   nondegeneracy or Legendre-transform assumptions.
6. The action function's domain and regularity, and whether `d_q S` is a Frechet derivative,
   gradient after a metric choice, manifold differential, coordinate covector, or another object.
7. Classical, weak, viscosity, or another solution notion, including equality pointwise,
   almost-everywhere, or in a generalized sense.
8. Initial or boundary data, spatial and time domains, compatibility assumptions, and local versus
   global scope.
9. Ordered binders, quantifier dependencies, every hypothesis, exact conclusion, and all credited
   alternate encodings with checked transports.

## Degenerate and boundary cases

Source review must explicitly dispose of zero-dimensional configuration spaces; empty or singleton
domains; autonomous Hamiltonians; constant action functions; zero or constant Hamiltonians;
nondifferentiable actions; degenerate Legendre transforms; characteristics that leave the domain;
finite-time singularities; multiple classical or generalized solutions; caustics and crossing
characteristics; stationary versus time-dependent reductions; boundary points; and empty or
incompatible data. No case is silently excluded at intake.

## Neighbor and substitution exclusions

- `THM-P-0755` is a distinct physics target. Its displayed equation schema is contextual notation,
  not an identity or statement witness for this mathematical target.
- `THM-M-1380` (Jacobi theorem / complete solution) is not silently absorbed into this root.
- `THM-M-1373`, `THM-M-1377`, `THM-M-1378`, `THM-M-1381`, and `THM-M-1382` separately own
  Hamiltonian-system, variational, Euler-Lagrange, Maupertuis, and least-action boundaries.
- `THM-M-1198` separately owns the method of characteristics; a characteristic construction cannot
  replace an unidentified Hamilton-Jacobi result.
- `THM-M-1516` and `THM-M-1520` separately own Hamiltonian mechanics and a Hamiltonian Liouville
  theorem. Their source leads or formal artifacts confer no status here.
- A free-particle, harmonic-oscillator, one-dimensional, autonomous, stationary, or quadratic
  special case cannot be selected merely because it is convenient to formalize.
- A predicate or structure that assumes the desired equation, solution, equivalence, or complete
  integral cannot turn that assumption into theorem evidence.
- Numerical trajectories, PDE solvers, symbolic manipulation, and the untrusted `已验证` label
  provide no human-source or kernel-proof credit.

No canonical Lean expression, expression fingerprint, checked alternate encoding, discovery
protocol, obligation registry, or proof state is frozen at intake.
