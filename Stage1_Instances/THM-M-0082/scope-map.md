# Scope map

## Included claim

- Freyd's general adjoint functor theorem in its right-adjoint orientation.
- Categories `D` and `C` and a functor `G : D -> C`.
- Completeness of `D` at the required diagram sizes.
- Preservation by `G` of those limits.
- The solution-set condition for `G`.
- The conclusion that `G` has a left adjoint, equivalently that `G` is a right adjoint.

## Statement-phase boundary decisions

The selected primary statement must fix local smallness, completeness, and solution-set definitions,
including all size qualifications. The Lean statement must then freeze universes, binder order,
typeclass versus explicit hypotheses, and the exact equivalence between `G.IsRightAdjoint` and an
exhibited adjunction. It must also test empty or large indexing categories and locally smallness
requirements rather than silently strengthening them.

## Explicit exclusions

- The special adjoint functor theorem using well-poweredness and a small coseparating family.
- The dual left-adjoint theorem, except as an explicitly checked transport later.
- The elementary fact that an already given adjoint preserves limits or colimits.
- Homological long exact sequences and other downstream applications.
- A conclusion assumed through a package or structure field.

The historical `S1_M_135.lean` module and its mathlib declarations are candidate evidence only.
Their exact types, dependency revisions, proof bodies, axioms, and match to the source claim must be
re-audited in later phases.
