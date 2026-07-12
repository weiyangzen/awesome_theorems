# Scope map

## Preserved catalog boundary

The repository fixes target `THM-M-1382`, the title `最小作用量原理`, William Hamilton, 1834, the
gloss `物理系统的变分原理`, importance "high," and an untrusted `已验证` status. Intake preserves
that classical-mechanics variational-principle family. It does not silently choose a modern
textbook formulation, a historical fixed-energy principle, or a convenient Lean theorem.

## Proposition-changing decisions

An approved source and statement run must freeze all of the following:

- the physical/mathematical model: particles in a real vector space, a configuration manifold, a
  constrained system, a field, or another explicitly axiomatized system;
- time domain, configuration space, scalar field, universes, path space, differentiability and
  integrability assumptions, and whether the Lagrangian depends explicitly on time;
- the action convention: modern `integral L(t, q(t), q'(t)) dt`, Hamilton's accumulated living
  force, Maupertuis/Jacobi abbreviated action at fixed energy, or another source-defined functional;
- whether endpoint times and positions are fixed, endpoints are free, energy is fixed, variations
  obey constraints, and transversality or multiplier conditions are required;
- admissible paths and variations, their topology, compact support or endpoint behavior, and the
  meaning of first variation;
- whether "least/extremal" means global minimum, local minimum, maximum, general local extremum, or
  stationarity, and which implication or equivalence is asserted;
- the exact conclusion: equations of motion, Euler-Lagrange equations, vanishing first variation,
  existence or uniqueness of a minimizer, a Hamilton-Jacobi relation, or another source clause; and
- every ordered binder, hypothesis, exceptional case, proof boundary, and alternate-encoding
  transport.

These choices yield inequivalent propositions. They are a resolution ledger, not a canonical
statement.

## Candidate readings not credited

- Hamilton's fixed-endpoint stationary-action principle for a sufficiently regular finite-
  dimensional Lagrangian system.
- Stationarity of the action implies the Euler-Lagrange equation by differentiation under the
  integral, integration by parts, and the fundamental lemma of the calculus of variations.
- The converse implication from Euler-Lagrange plus analytic side conditions to vanishing first
  variation.
- A Fermat-style necessary condition: a local extremum of the action has zero first derivative.
- A literal minimum theorem under coercivity, lower-semicontinuity, compactness, convexity, or
  second-variation assumptions.
- Hamilton's 1834 fixed-energy law of stationary action or law of varying action.
- Maupertuis/Jacobi abbreviated action at fixed energy.

No item in this list is selected, conjoined, or asserted at intake.

## Neighbor and duplicate boundaries

- `THM-M-1381` separately owns the Maupertuis-principle label. Its fixed-energy abbreviated-action
  semantics cannot close this target.
- `THM-M-1378` separately owns the Euler-Lagrange-equation label. An Euler-Lagrange theorem is not
  automatically identical to a variational principle.
- `THM-M-1518` has the same Chinese title and gloss in another catalog category. Its existing
  stationary-action-to-Euler-Lagrange statement and legacy `S1-M-187` material are foreign-target
  discovery evidence, not an alias decision, source authority, or proof credit for `THM-M-1382`.
- `THM-P-0748` states that actual motion makes `S = integral L dt` extremal, while `THM-P-0749`
  separately describes an Euler-Lagrange necessary condition. These physics records expose overlap
  but are outside the rev-5.6 target set and do not select this target's proposition.

The integration lane must resolve whether the repeated labels are true aliases, distinct source
readings, or catalog duplicates before any shared root, transport, or coverage attribution exists.

## Exclusions and circular encodings

- A structure field or hypothesis that directly assumes stationarity, Euler-Lagrange, a minimizing
  path, or the desired implication is an interface, not a proof.
- A global-minimum slogan cannot replace stationarity: classical trajectories need not globally
  minimize an unrestricted action.
- A proof for a harmonic oscillator, geodesic, free particle, autonomous Lagrangian, one-dimensional
  system, or convex functional cannot replace a more general source claim.
- Numerical trajectory optimization, discretized action, symbolic differentiation, or physics
  observation is not a kernel proof of a continuum theorem.
- The catalog label `已验证` supplies no human-source or machine-proof evidence.

## Degenerate and boundary cases

The statement phase must decide zero-length time intervals; zero-dimensional configuration spaces;
constant paths; the zero, constant, or total-derivative Lagrangian; singular/degenerate
Lagrangians; empty admissible classes; free versus fixed endpoints; nonunique extrema; stationary
saddles and maxima; nonsmooth paths; improper or nonintegrable action; constrained variations;
gauge-equivalent Lagrangians; and whether conclusions hold pointwise, almost everywhere, weakly, or
only in the interval interior.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic interval fundamental-
theorem, integration-by-parts, and local-extremum derivative APIs. These are possible ingredients,
not a least-action statement or proof. A bounded local search found no source-identical declaration
for the unresolved target. Complete formal-candidate discovery belongs to the later anchor-audit
phase.
