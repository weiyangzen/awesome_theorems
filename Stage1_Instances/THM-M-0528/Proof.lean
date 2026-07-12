import Statement

set_option autoImplicit false

namespace Stage1Instances.THM_M_0528

universe u v w

/-!
# THM-M-0528 proof execution

The frozen target is discharged by the exact pinned mathlib covering-map
uniqueness theorem.  This wrapper instantiates every binder explicitly, so its
type is the canonical target rather than a nearby pointwise formulation.
-/

/-- Canonical proof body for uniqueness of two continuous lifts through a
covering map after agreement at one point. -/
theorem coveringLiftUniqueness :
    CoveringLiftUniquenessTarget.{u, v, w} := by
  intro E X A _ _ _ _ p hp g₁ g₂ hg₁ hg₂ hproj a ha
  exact hp.eq_of_comp_eq hg₁ hg₂ hproj a ha

/-- Exact-type guard against accidental drift of the exported proof body. -/
example : CoveringLiftUniquenessTarget.{u, v, w} :=
  coveringLiftUniqueness

#print axioms coveringLiftUniqueness

end Stage1Instances.THM_M_0528
