import Mathlib.GroupTheory.Descent
import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.NumberTheory.NumberField.Basic

/-!
# THM-M-0450 conditional obligation composition

This module gives typed interfaces for the two arithmetic inputs to descent.
No instance of either interface is constructed, so this is not a proof of the
Mordell-Weil theorem.
-/

noncomputable section

universe u

namespace Stage1Instances.THM_M_0450.ObligationTree

abbrev RationalPoints (K : Type u) [Field K] (E : WeierstrassCurve K) :=
  E.toJacobian.Point

def ExactTarget : Prop :=
  forall (K : Type u) [Field K] [NumberField K] (E : WeierstrassCurve K),
    E.IsElliptic -> AddGroup.FG (RationalPoints K E)

/-- The weak Mordell-Weil input in exactly the frozen Jacobian point model. -/
def WeakMordellWeil (K : Type u) [Field K] (E : WeierstrassCurve K) : Prop :=
  (nsmulAddMonoidHom (α := RationalPoints K E) 2).range.FiniteIndex

/-- The height inputs required by pinned mathlib's abstract descent theorem. -/
structure HeightPackage (K : Type u) [Field K] (E : WeierstrassCurve K) where
  height : RationalPoints K E -> Real
  bound : Real
  nonnegative : forall P, 0 <= height P
  parallelogram :
    forall P Q, |height (P + Q) + height (P - Q) -
      2 * (height P + height Q)| <= bound
  northcott : Northcott height

/-- Kernel-checked assembly of the two open arithmetic packages into the exact
target. The ellipticity premise is preserved for the package providers. -/
theorem root_of_descent_packages
    (weakMW : forall (K : Type u) [Field K] [NumberField K]
      (E : WeierstrassCurve K), E.IsElliptic -> WeakMordellWeil K E)
    (heights : forall (K : Type u) [Field K] [NumberField K]
      (E : WeierstrassCurve K), E.IsElliptic -> HeightPackage K E) :
    ExactTarget.{u} := by
  intro K _ _ E hE
  let package := heights K E hE
  letI : Northcott package.height := package.northcott
  exact AddCommGroup.fg_of_descent' (weakMW K E hE)
    package.nonnegative package.parallelogram

#check root_of_descent_packages
#print axioms root_of_descent_packages

end Stage1Instances.THM_M_0450.ObligationTree
