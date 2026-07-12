import ObligationTree

/-!
# THM-M-0698 proof execution

This module closes the frozen reverse direction with the exact compactness
theorem from the manifest-pinned mathlib dependency, then checks both the
frozen child-to-root composition and a direct exact-target wrapper.
-/

namespace Stage1Instances.THM_M_0698.Proof

open FirstOrder

universe u v

/-- The substantive finite-satisfiability-to-satisfiability direction, pinned
to mathlib's ultraproduct proof body. -/
theorem finiteToSatisfiable_pinned : FiniteToSatisfiable.{u, v} := by
  intro L T h
  exact FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable.mpr h

/-- The exact frozen target, closed through the obligation-tree composition. -/
theorem firstOrderCompactness_via_frozen_composition :
    FirstOrderCompactnessTarget.{u, v} :=
  firstOrderCompactness_of_directions satisfiableToFinite_checked
    finiteToSatisfiable_pinned

/-- Independent direct exact-type wrapper around the same pinned terminal body. -/
theorem firstOrderCompactness_pinned :
    FirstOrderCompactnessTarget.{u, v} := by
  intro L T
  exact FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable

#print axioms finiteToSatisfiable_pinned
#print axioms firstOrderCompactness_via_frozen_composition
#print axioms firstOrderCompactness_pinned
#print axioms FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable

end Stage1Instances.THM_M_0698.Proof
