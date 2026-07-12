# Scope map

## Included claim

- A topological space `X` expressed as the union of subspaces `A` and `B`, subject to the cover or
  excision condition selected from the primary statement.
- Singular homology with one fixed coefficient system.
- The maps induced by `A intersection B -> A`, `A intersection B -> B`, `A -> X`, and `B -> X`,
  together with the connecting morphism.
- Exactness in every degree of the resulting long sequence. The sign on the map into the direct
  sum is part of the target and cannot be discarded.

## Statement-phase decisions

An inspected edition must decide whether the hypothesis is an open cover, a cover by subcomplexes,
or that the interiors of `A` and `B` cover `X`; whether the theory is reduced or unreduced; whether
the sequence is indexed by natural or integer degrees; and whether coefficients are `Z`, a fixed
abelian group, or a ring/module. It must also fix the order and signs of the inclusion maps and the
behavior in degree zero, for empty intersection, and for empty subspaces.

The formal statement must bind the spaces, topology/subspace data, cover evidence, coefficient
object, degree, homology objects, all maps, and exactness predicate explicitly. Universes, binder
order, and foundation profile remain open until this exact target is elaborated.

## Explicit exclusions

- The Mayer-Vietoris sequence in sheaf cohomology as a substitute for singular homology.
- A Cech cohomology sequence, van Kampen theorem, excision theorem alone, or only a short segment of
  the long exact sequence.
- Mere equality of Betti numbers or Euler characteristics.
- A structure that accepts exactness or the connecting map as an assumption.
- Any version that removes the cover/excision hypothesis or silently fixes a convenient degree.

The pinned mathlib sheaf-cohomology declaration is an adjacent API lead only. A later anchor audit
must determine whether concrete relative singular homology, excision, connecting morphisms, and
long-exact-sequence composition are available for the intended homology statement.
