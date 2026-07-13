# Scope map

## Preserved theorem family

The intake preserves the catalog's geometric-realization family for compact-Lie-group
representations. A conventional full Borel-Weil-Bott candidate associates a homogeneous line
bundle to an integral weight on a flag variety and describes all of its cohomology: in the regular
case exactly one degree is nonzero and realizes an irreducible representation determined by the
Weyl dot action; in the singular case all degrees vanish. This description identifies decisions
that change the proposition. It is not frozen as the exact root.

## Decisions required at statement freeze

1. Preserve and independently review a lawful authoritative source edition, exact theorem and
   page, incorporated definitions, proof boundary, translations, corrections, and errata.
2. Preserve the full higher-cohomology Borel-Weil-Bott root selected by the title. Treat the
   degree-zero Borel-Weil theorem only as a special case or antecedent, never as the root.
3. Fix the group formulation: compact connected Lie group, compact connected semisimple group,
   complex semisimple algebraic group, or complex semisimple Lie algebra, plus the checked bridges
   needed to match the catalog.
4. Fix a maximal torus/Borel subgroup and flag variety, the analytic or algebraic category, the
   line-bundle construction and sign convention, and the scalar field.
5. Fix the weight lattice, integrality and dominance conventions, positive roots, Weyl vector,
   Weyl dot action, regularity/singularity, Weyl element, and length convention.
6. Fix the result: vanishing outside one degree, the surviving cohomology group and its dual/sign
   convention, irreducibility, highest weight, equivariance, and whether an isomorphism or equality
   is asserted.
7. Resolve trivial/rank-zero, torus/central, disconnected, singular-wall, non-integral, and
   non-dominant cases, together with empty products/cohomology and universe/coercion choices.
8. Fix ordered binders, typeclasses, minimal imports, foundation/TCB/computation profiles, the exact
   Lean expression and environment fingerprint, and checked transports for all credited alternate
   encodings.

## Boundary cases

Source and statement review must explicitly address trivial and rank-zero groups; central tori and
empty root systems; disconnected groups; singular versus regular shifted weights; weights on
walls; non-integral and non-dominant weights; the degree-zero dominant case; the Weyl element of
length zero; dualization and line-bundle sign choices; real versus complex representations; and
analytic versus algebraic cohomology. No case is excluded at intake.

## Explicit substitutions excluded

- The degree-zero Borel-Weil theorem cannot replace the full Bott cohomology theorem; doing so
  would require an authoritative correction to the repository target identity.
- The Weyl character or dimension formula, highest-weight classification, Bott periodicity, Bott
  vanishing, and Borel fixed-point theorem are different theorem roots.
- Abstract sheaf cohomology does not construct a flag variety, a homogeneous line bundle, its group
  action, or the representation/cohomology identification.
- Generic group representations, root systems, Lie weights, and irreducibility APIs are only
  substrate; they do not state this theorem.
- A rank-one, dominant-only, finite-group, torus-only, or other special case cannot close the
  general source-selected target.
- A structure field, assumed proposition, numerical table, or unchecked computer-algebra output
  cannot stand in for the theorem.
- The catalog's `已验证` label, an API probe, a theorem-name match, or a citation alone supplies no
  machine or source-fidelity proof credit.

## First retry condition

Admit and independently review one exact source statement and its correction history; reconcile the
Borel/Weil/Bott attribution and date; then select the exact full-theorem formulation and every group, geometric,
cohomological, weight, action, degree, representation, binder, and boundary convention. Only then
may the statement phase encode, fingerprint, transport, and mutation-test a canonical Lean target.
