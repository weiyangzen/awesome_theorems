# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1375`, the title `Liouville定理`, Joseph Liouville, 1838,
the gloss `相空间体积守恒` (phase-space volume conservation), importance "high," and the
untrusted status `已验证`. Its ordinary-differential-equations category and neighboring Hamiltonian
mechanics records identify the classical Hamiltonian Liouville theorem family. These metadata do not
select one truth-valued proposition or supply source or proof credit.

## Proposition-changing decisions

An approved statement run must freeze all of the following from a reviewed immutable source:

- canonical `R^n x R^n` coordinates, a general symplectic vector space, or a symplectic manifold,
  including dimension, scalar field, orientation, topology, measurable structure, and volume
  normalization;
- autonomous or time-dependent Hamiltonian, its domain and exact regularity, and the sign convention
  for Hamilton's equations or the Hamiltonian vector field;
- a locally defined flow on a source-specified time/domain set, a complete global flow, or a single
  time-evolution map, including existence, uniqueness, invertibility, and differentiability;
- infinitesimal zero-divergence, Jacobian determinant one, preservation of the symplectic form or
  Liouville volume form, equality of volumes of regions, or `MeasurePreserving` as the exact root,
  together with every required transport direction;
- the class of regions or measurable sets, whether finite/infinite volume matters, and whether the
  result concerns image volume, preimage measure, density evolution, or all of these;
- whether a time-dependent Hamiltonian is included, and whether energy conservation is explicitly
  absent from the hypotheses; and
- all ordered binders, incorporated definitions, hypotheses, boundary cases, proof boundary,
  source corrections, and errata decisions.

These formulations are related but not definitionally interchangeable. A convenient global
Euclidean statement cannot stand in for a source whose theorem is local or geometric.

## Duplicate and neighboring boundaries

- `THM-M-1520` independently records Joseph Liouville, 1838, and the identical gloss in the
  mathematical-physics category. Its later dossier chose a global canonical-coordinate
  `MeasurePreserving` statement. That choice is discovery evidence, not authority or credit for
  `THM-M-1375`; master duplicate reconciliation is required.
- `THM-P-0800` is outside the 1546-target Stage1 mathematics set and says phase-space volume is
  invariant under Hamiltonian flow. It corroborates the intended family but cannot supply this
  target's statement, status, or denominator credit.
- `THM-M-1373` (Hamiltonian systems), `THM-M-1381` (symplectic geometry), and related Poisson or
  canonical-transformation items may supply future definitions, but they do not close this root.

## Explicit exclusions

- `THM-M-1143` bounded harmonic functions, `THM-M-0224` bounded entire holomorphic functions,
  number-theoretic and differential-field Liouville theorems, Sturm-Liouville theory, and unrelated
  named results;
- Liouville-Arnold/action-angle integrability, including the claim that invariant regular level
  components are tori;
- the Liouville equation for a density used as an unproved substitute for volume preservation, or
  conversely volume preservation silently strengthened to a source-specific density theorem;
- an arbitrary divergence-free flow, symplectic map, or volume-preserving map broadened beyond the
  Hamiltonian source statement;
- a structure field or premise that assumes `MeasurePreserving`, symplectic preservation,
  determinant one, zero divergence, or the desired volume equality;
- numerical trajectories, sampled Jacobians, symbolic algebra without a checked certificate, or
  the catalog label `已验证` used as theorem evidence.

## Boundary cases to resolve

The source-selected statement must decide zero degrees of freedom, empty regions, null or
infinite-volume sets, constant Hamiltonians, equilibrium flows, noncomplete flows, local domains,
singular/noncanonical coordinates, nonorientable manifolds, boundary/corner phase spaces,
time-dependent Hamiltonians, lower regularity, and the difference between infinitesimal and
finite-time preservation.

## Formal boundary

No canonical Lean expression is frozen at intake. Pinned mathlib provides generic gradient,
continuous-differentiability, ODE/flow, volume-measure, `MeasurePreserving`, and finite-dimensional
symplectic-matrix interfaces. The probe authenticates a small subset of those APIs only. It neither
chooses the target nor establishes a transport, formal anchor, proof body, or absence result.
