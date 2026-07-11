import Mathlib.GroupTheory.Descent
import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.NumberTheory.NumberField.Basic

/-!
# Machine-anchor audit for THM-M-0450

The declarations below check the exact types of the useful pinned mathlib
anchors. They deliberately expose the missing arithmetic hypotheses and do
not prove `ExactTarget`.
-/

noncomputable section

universe u

namespace Stage1Instances.THM_M_0450

/-- Pinned mathlib's descent result, specialized to the exact point model. -/
theorem mathlib_descent_anchor {K : Type u} [Field K] [NumberField K]
    (E : WeierstrassCurve K) {h : E.toJacobian.Point -> Real} {C : Real}
    (weakMW : (nsmulAddMonoidHom (α := E.toJacobian.Point) 2).range.FiniteIndex)
    (height_nonnegative : forall P, 0 <= h P)
    (approx_parallelogram :
      forall P Q, |h (P + Q) + h (P - Q) - 2 * (h P + h Q)| <= C)
    [Northcott h] :
    AddGroup.FG E.toJacobian.Point :=
  AddCommGroup.fg_of_descent' weakMW height_nonnegative approx_parallelogram

-- Exact audit probes: an object-model instance and a conditional descent
-- theorem exist, while the ellipticity premise is unused by the latter.
#check WeierstrassCurve.Jacobian.Point.instAddCommGroup
#check AddCommGroup.fg_of_descent'
#check mathlib_descent_anchor

end Stage1Instances.THM_M_0450
