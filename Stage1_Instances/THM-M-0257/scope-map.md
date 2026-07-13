# Scope map

## Preserved theorem family

The intake preserves the Ahlfors-Bers family connecting normalized quasiconformal solutions,
analytic variation of complex structures, and Teichmuller-space complex geometry. It does not
choose a canonical proposition. Candidate readings, none credited as the target, include:

- existence and uniqueness of a normalized quasiconformal solution for a Beltrami coefficient;
- holomorphic dependence of that normalized solution on a holomorphic family of coefficients;
- construction of a complex or complex-Banach manifold structure on a selected Teichmuller space;
- the finite-dimensional complex structure and dimension for surfaces of fixed finite type; and
- a bounded-domain or Bers-embedding formulation related to the complex structure.

## Decisions required at statement freeze

1. Select a lawful immutable source edition and exact theorem passage; map incorporated
   definitions, proof boundaries, corrections and errata, translations, and independent review.
2. Reconcile the catalog's joint attribution and 1960 date with the joint variable-metric paper,
   the Ahlfors complex-structure paper, and the Bers bounded-domain paper.
3. Fix the base surface: closed or punctured, finite or infinite type, genus and number of marked
   points, orientation, boundary, compactness, connectedness, and exceptional low-complexity types.
4. Fix markings, isotopy or homotopy convention, conformal equivalence, quotient relation, base
   point, mapping-class action, and whether the target is Teichmuller space or moduli space.
5. If using Beltrami coefficients, fix the domain, measurable or almost-everywhere convention,
   `L-infinity` norm bound, representative equality, normalization (such as fixing `0`, `1`, and
   infinity), solution regularity, and exact Beltrami equation.
6. Select the conclusion: solution existence, uniqueness, parameter continuity, complex
   differentiability or holomorphicity, atlas compatibility, manifold structure, complex
   dimension, bounded-domain embedding, or a sourced conjunction with explicit components.
7. Fix finite-dimensional versus Banach-manifold charts, local and global conclusions, topology,
   chart model, quotient well-definedness, and every analyticity convention.
8. Freeze universes, ordered binders, hypotheses, conclusion, alternate encodings and directions,
   foundation/TCB/computation profiles, minimal imports, and all statement mutations.

## Degenerate and boundary cases

Source review must dispose of coefficients with norm zero or norm one; equality only almost
everywhere; disconnected or empty carriers; the sphere with too few marked points; tori and other
low-complexity types; punctures, boundary components, and nodes; orientation reversal; conformal
automorphisms that defeat uniqueness without normalization; base-point and marking changes;
finite-type versus universal Teichmuller space; trivial or zero-dimensional Teichmuller spaces;
and equality of maps versus equality in a quotient.

## Neighbor ownership and exclusions

- `THM-M-0255` owns the catalog's quasiconformal existence-and-uniqueness family. It does not
  donate a measurable Riemann mapping statement or proof to this target.
- `THM-M-0256` owns the broader Teichmuller theory and Riemann-surface moduli entry. It does not
  supply the exact complex-structure root here.
- `THM-M-0258` owns the neighboring Teichmuller-space boundary entry. Boundary or compactification
  statements cannot be folded into this root.
- A generic complex manifold, analytic map, conformal map, group action, orbit quotient, or
  homeomorphism interface is substrate only.
- A structure storing the desired atlas, solution, or holomorphicity as data is not a proof.
- The catalog status, a theorem name, bibliography, API probe, or bounded search gives no H or M
  credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, generic complex
analyticity, conformal-calculus, manifold, group-action, and quotient interfaces elaborate.
`IntakeProbe.lean` checks representative declarations. They define no Beltrami coefficient,
quasiconformal homeomorphism, marked Riemann surface, Teichmuller quotient, or Ahlfors-Bers result.
A bounded exact-topic search found no target declaration; this is intake discovery, not the
downstream anchor audit or a global absence claim.

No canonical Lean target, checked transport, expression fingerprint, discovery-protocol hash,
obligation registry, or proof state is frozen in this phase.
