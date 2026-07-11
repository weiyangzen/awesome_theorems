# Scope map

## Included claim

- Hausdorff locally convex topological vector spaces over the source theorem's scalar field.
- Nuclearity of at least one factor, with completeness or quasi-completeness hypotheses exactly as
  required by the selected theorem.
- Completed projective and injective topological tensor products and their canonical comparison.
- A dual description by continuous bilinear forms or continuous maps into an appropriate dual only
  if it is part of the selected source theorem.

## Decisions deferred to statement freeze

The source inspection must determine the scalar field, separation and completeness assumptions,
which epsilon/injective and pi/projective completions are meant, whether both factors are nuclear,
and which topology (weak, strong, bounded convergence, or another) is placed on each dual. It must
also settle degenerate spaces, the direction and naturality of comparison maps, and whether the
result is an equality of topologies, a homeomorphism, or a topological vector-space isomorphism.

## Explicit exclusions

- Grothendieck duality in algebraic geometry or derived categories.
- Grothendieck's inequality, the approximation property, or a Banach-space result substituted for
  the nuclear locally convex tensor theorem.
- Finite algebraic `PiTensorProduct` seminorm inequalities as the terminal claim.
- An abstract record that assumes nuclearity, topology agreement, or duality representation as
  uninterpreted proposition fields.

The formal statement must eventually use concrete definitions or document an exact API blocker;
the legacy `NuclearTensorProductDualityData` is not an acceptable encoding of the theorem.
