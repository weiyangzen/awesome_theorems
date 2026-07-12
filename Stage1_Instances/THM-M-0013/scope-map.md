# THM-M-0013 scope map

## Preserved theorem family

The intake preserves the classical fixed-field Galois correspondence named by the catalog. For an
extension `E/F` that satisfies a source-selected Galois hypothesis, intermediate fields `M` are
sent to the automorphisms of `E` fixing `M`, and subgroups `H` are sent to their fixed fields. The
maps reverse inclusion. This description is a theorem-family boundary, not yet the canonical
proposition.

## Decisions required at statement freeze

1. Select one immutable, independently reviewed source statement and fix finite versus infinite
   Galois theory.
2. Fix the field universes, algebra structure, Galois convention, and any explicit finite-
   dimensional, algebraic, normal, or separable hypotheses.
3. In the finite case, decide whether the root is only the order equivalence or includes the
   index/degree, conjugacy, normal-subgroup/Galois-subextension, and quotient-group clauses.
4. In the infinite case, require the Krull topology and closed subgroups, and decide whether the
   open/finite, conjugacy, normality, and quotient clauses are root-critical.
5. Fix correspondence direction and notation: intermediate field to fixing subgroup, subgroup to
   fixed field, with an order dual rather than an order-preserving claim on ordinary inclusion.
6. Map subextensions to `IntermediateField F E` and the Galois group to `Gal(E/F)`, including all
   typeclass premises and universe parameters.
7. Resolve whether the catalog's 1832 attribution refers to this modern correspondence theorem or
   to Galois's solvability-by-radicals work; do not infer historical source fidelity from the date.

## Candidate scopes not credited

- Finite version: for a finite-dimensional Galois extension `E/F`, intermediate fields of `E/F`
  are order anti-isomorphic to all subgroups of `Gal(E/F)` via fixing subgroup and fixed field.
- Full finite textbook version: the correspondence plus degree/index, conjugacy, normality, and
  quotient-group consequences.
- Infinite version: for a Galois extension `K/k`, intermediate fields are order anti-isomorphic to
  closed subgroups of the Krull-topological Galois group.
- A fixed-field theorem giving only one inverse identity, rather than the entire correspondence.

## Boundary cases to resolve

- Trivial extensions, trivial and total subgroups, and bottom and top intermediate fields.
- Finite extensions versus infinite algebraic extensions.
- Non-Galois extensions, including finite separable but nonnormal and normal inseparable cases.
- Arbitrary subgroups versus topologically closed subgroups in the infinite case.
- Normal and nonnormal subgroups and the corresponding Galois or non-Galois intermediate fields.
- Infinite index/degree, quotient topology, and the precise meaning of quotient isomorphism.
- Universe-polymorphic fields and any finite-dimensional typeclass inferred rather than explicit.

## Excluded substitutions

- The inverse Galois problem, Galois's solvability-by-radicals criterion, or computation of a
  particular polynomial's Galois group.
- Differential, topological-covering, Grothendieck, Tannakian, or general order-theoretic Galois
  correspondences.
- A correspondence for only cyclic, abelian, normal, open, or finite-index subgroups unless the
  selected source root has exactly that scope.
- The finite theorem used for an infinite-extension claim, or the infinite closed-subgroup theorem
  used to imply a correspondence with all abstract subgroups.
- `IntermediateField.fixedField`, `IntermediateField.fixingSubgroup`, either inverse lemma, or a
  Galois insertion alone when the selected root requires the full order equivalence and its clauses.
- A structure that assumes the desired inverse laws or correspondence as fields.
- The catalog's `verified` label, successful `#check` output, or a theorem name as proof credit.

## Neighbor boundaries

`THM-M-0682` concerns differential Galois theory and cannot supply this target. Nearby catalog
items such as Kronecker-Weber and Artin reciprocity use Galois theory but do not establish the
fundamental correspondence. No status, receipt, proof body, or scope decision is shared.
