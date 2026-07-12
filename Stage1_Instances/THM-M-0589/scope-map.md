# Scope map

## Included theorem family

- A compact manifold (possibly with a separately specified boundary) in one selected smooth, PL,
  or topological category and in the source's stable/high-dimensional range.
- A fixed reference manifold or Poincare complex and degree-one normal maps into it.
- Normal invariants, surgery obstructions in the appropriate decorated `L`-groups, and the
  structure set appropriate to the chosen category and equivalence relation.
- A source-selected realization, obstruction-vanishing, classification, or surgery exact-sequence
  theorem linking those objects.

This is a theorem-family boundary, not an exact claim. No one bullet is accepted as an assumed
premise or as a machine-checked result.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze the category
(smooth, PL, or topological), dimension and any exceptional dimensions, compactness and boundary
conditions, connectedness and orientation data, the reference homotopy type, fundamental group and
orientation character, simple versus ordinary homotopy equivalence, relative versus closed form,
normal structure and normal-invariant encoding, the exact decorated surgery obstruction group,
basepoints and actions on the structure set, and the quantifier order.

It must also decide whether the root is an exact sequence, an obstruction-vanishing `if and only
if`, a realization theorem, or a classification bijection. These forms are related by substantial
mathematics but are not interchangeable statements. Low-dimensional cases, nontrivial fundamental
groups, non-simply-connected boundaries, and category-changing comparison maps must be handled
explicitly rather than absorbed into a slogan.

## Explicit exclusions

- High-dimensional Poincare, h-cobordism, or s-cobordism alone as a substitute for the selected
  general surgery theorem.
- Classification of surfaces, the three-manifold geometrization theorem, or the smooth
  four-dimensional classification problem.
- A simply-connected special case substituted for a source theorem with arbitrary fundamental
  group, or a closed-manifold form substituted for a relative theorem.
- An abstract structure that contains the desired exactness, obstruction-vanishing implication,
  or classification equivalence as a field.
- The repository metadata value `已验证`, a bibliography entry, or an adjacent Poincare artifact as
  source-fidelity or kernel-proof evidence.

No canonical Lean expression is frozen at intake. A later statement must expose concrete manifold,
normal-map, structure-set, normal-invariant, and surgery-obstruction interfaces, or record the exact
missing API without encoding the desired theorem as data.
