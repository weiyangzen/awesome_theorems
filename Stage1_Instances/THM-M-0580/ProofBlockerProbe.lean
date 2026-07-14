import ObligationTree

/-!
# THM-M-0580 proof-availability probe

This module checks two proof-phase boundaries. The exact topological target
implies the smooth-package proposition, so using the root to construct that
package would be circular. The matching mathlib `proof_wanted` entries are not
retained declarations in the pinned environment. Neither check proves the
Poincare target or the open smoothing package.
-/

noncomputable section

namespace Stage1Instances.THM_M_0580

universe u

/-- The frozen smooth package is a consequence of the canonical root. This is
a diagnostic direction only, not a proof of either proposition. -/
theorem smoothThreeDimensionalPoincare_of_perelmanPoincareTarget
    (root : PerelmanPoincareTarget.{u}) :
    SmoothThreeDimensionalPoincare.{u} := by
  intro M _topology _t2 _charted _smooth _simplyConnected _compact
  exact root M

#print axioms smoothThreeDimensionalPoincare_of_perelmanPoincareTarget

-- `proof_wanted` elaborates a statement without retaining a declaration.
#check_failure ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
#check_failure SimplyConnectedSpace.nonempty_homeomorph_sphere_three
#check_failure SimplyConnectedSpace.nonempty_diffeomorph_sphere_three

end Stage1Instances.THM_M_0580
