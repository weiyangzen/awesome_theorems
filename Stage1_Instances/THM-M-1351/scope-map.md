# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1351`, the label `Poincaré映射` (Poincare map), the gloss
`周期轨道的稳定性` (stability of periodic orbits), Henri Poincare, and 1881. It does not identify
a source passage or one theorem. Importance and the untrusted `已验证` label supply neither
statement nor proof evidence.

The intended family concerns a local first-return map near a periodic orbit and the relationship
between the continuous-time dynamics and the discrete dynamics on a transverse section.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from an immutable source:

- an autonomous ODE, a local or global flow, or another dynamical system, together with its phase
  space, scalar field, dimensions, regularity, existence interval, and uniqueness assumptions;
- a nonconstant periodic solution or geometric periodic orbit, its period convention, base point,
  and whether stability ignores phase along the orbit;
- the transverse section: local/global, codimension, embedded/chart representation, regularity,
  orientation if relevant, and the exact transversality condition;
- the first positive return time, its domain and uniqueness, treatment of earlier intersections,
  and the neighborhood on which the return map exists;
- continuity or differentiability of the return time and return map, and whether construction and
  regularity are premises, separate obligations, or part of the root conclusion;
- the stability predicate: Lyapunov, orbital, asymptotic, exponential, attracting, repelling, or
  structural, including all neighborhood quantifiers and forward/backward time conventions;
- whether the root is an equivalence with fixed-point stability, a sufficient derivative/spectral
  criterion, a monodromy comparison, a section-independence result, or a conjunction;
- real versus complex characteristic multipliers, multiplicity, the unavoidable flow-direction
  multiplier, strict versus non-strict unit-circle inequalities, and hyperbolic boundary cases.

## Boundary cases to resolve

- equilibria viewed as constant periodic solutions and zero or nonminimal periods;
- multiple crossings, tangential returns, grazing the section, and return times tending to zero;
- points that never return, leave the flow domain, or return only outside the chosen local section;
- a one-dimensional phase space or zero-dimensional transversal;
- noncompact periodic parametrizations versus the compact geometric orbit;
- eigenvalues on the unit circle, the neutral phase direction, and defective derivatives;
- changing the base point or transverse section and the resulting conjugacy or spectrum relation;
- semiflows without negative time and incomplete vector fields.

## Explicit exclusions

- Poincare recurrence, the Poincare-Bendixson theorem, the Poincare lemma, or an unrelated use of
  the name Poincare;
- Floquet theory alone, a monodromy matrix alone, or discrete periodic-point facts presented as the
  full continuous-time return-map theorem;
- an arbitrary self-map called a return map without a checked construction from a flow and section;
- a theorem assuming the target stability equivalence or spectral conclusion as a field or premise;
- a numerical orbit, phase portrait, sampled return time, or floating-point multiplier computation;
- the untrusted catalog label `已验证` used as source, formalization, or proof credit.

No canonical proposition or excluded degenerate case is frozen at intake. The exact-source statement
phase owns those decisions; all downstream nodes remain open.
