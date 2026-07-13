# Scope map

## Preserved theorem family

The received scope is the root-space decomposition of a semisimple Lie algebra. A conventional
source formulation fixes a finite-dimensional semisimple Lie algebra `g`, a Cartan subalgebra `h`,
and writes `g` as the internal direct sum of `h` and its nonzero root spaces. This description
preserves the catalog family but is not yet the frozen canonical proposition.

The word "Cartan decomposition" is also widely used for the involution decomposition `g = k + p`
of a real semisimple Lie algebra and for group-level `KAK` or polar decompositions. The repository's
own root-space gloss rules those readings out.

## Decisions required at statement freeze

1. Fix the scalar field, algebraic-closure or splitting condition, characteristic, universes, and
   finite-dimensionality assumptions.
2. Fix the Lean meaning of semisimplicity and the existence or explicit choice of the Cartan
   subalgebra.
3. Decide whether roots are arbitrary functions, linear forms, or bundled nonzero weights, and how
   the finite set of roots is represented.
4. Choose ordinary simultaneous eigenspaces or generalized weight spaces. A checked equality is
   required before either encoding can receive credit for the other.
5. Express the direct decomposition, not merely spanning: both the sum-equals-top and independence
   components, or a checked equivalent internal-direct-sum construction, are required.
6. Decide whether the root includes only the decomposition clause or also bracket compatibility,
   orthogonality, and nondegenerate opposite-root pairing from the inspected source package.
7. Fix every ordered binder, hypothesis, conclusion, foundation profile, and credited alternate
   encoding with checked transports.

## Boundary cases

Source review must cover the zero Lie algebra, rank zero, an empty nonzero-root family, the zero
root, zero and top Cartan candidates, direct sums of semisimple ideals, repeated root dimensions,
non-split semisimple algebras, non-algebraically-closed fields, and positive characteristic. No case
is excluded at intake.

## Excluded substitutions

- The real symmetric-pair decomposition `g = k + p`, Cartan involutions, group-level `KAK`, polar,
  and Iwasawa decompositions are different theorem families.
- A spanning equality without independence is not an internal direct-sum theorem.
- Independence without spanning is likewise insufficient.
- Generalized root spaces cannot silently replace ordinary simultaneous eigenspaces.
- A theorem for `IsKilling` cannot silently replace a source theorem for every semisimple Lie
  algebra while the required converse bridge is absent.
- Cartan-subalgebra existence, root-system construction, bracket compatibility, or one-dimensional
  root spaces alone do not prove the requested decomposition.
- A structure or hypothesis storing the desired decomposition supplies no proof.
- The theorem name, an API `#check`, examples such as `sl2`, or the catalog's untrusted `verified`
  label supplies no H or M closure credit.

## Neighbor boundaries

`THM-M-0092` owns the separately named Cartan-Weyl theorem family, `THM-M-0093` highest-weight
classification, and `THM-M-0096` a Chevalley theorem family. Future dependencies must be frozen by
stable obligation IDs; proximity transfers no status or proof credit.

## Pinned formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `LieAlgebra.rootSpace`
abbreviates a generalized weight space. The library proves generalized-weight independence and
spanning and provides `LieAlgebra.cartan_sup_iSup_rootSpace_eq_top`. Under stronger Killing-form and
field hypotheses it also relates generalized root membership to the ordinary eigenvector equation.
These facts justify `M3` infrastructure status only. They neither select the received proposition
nor discharge its semisimple-to-ordinary-root bridge. The bounded inspection is not the later
exhaustive anchor audit.
