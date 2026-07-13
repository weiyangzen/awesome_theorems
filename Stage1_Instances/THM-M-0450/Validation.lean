import Statement
import Mathlib.GroupTheory.Descent
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0450 validation probe

This module independently reconstructs the conditional descent composition
against the canonical target. It deliberately does not import `Proof` or
`ObligationTree`, and it does not construct either arithmetic premise.
-/

noncomputable section

universe u

namespace Stage1Instances.THM_M_0450.Validation

open Stage1Instances.THM_M_0450

/-- The weak Mordell-Weil input in the canonical Jacobian-point model. -/
def WeakMordellWeil (K : Type u) [Field K] (E : WeierstrassCurve K) : Prop :=
  (nsmulAddMonoidHom (α := RationalPoints K E) 2).range.FiniteIndex

/-- The exact abstract height data consumed by mathlib's descent theorem. -/
structure HeightPackage (K : Type u) [Field K] (E : WeierstrassCurve K) where
  height : RationalPoints K E -> Real
  bound : Real
  nonnegative : forall P, 0 <= height P
  parallelogram :
    forall P Q, |height (P + Q) + height (P - Q) -
      2 * (height P + height Q)| <= bound
  northcott : Northcott height

/-- Implementation-diverse exact-type probe for conditional root composition.

The result is the imported canonical `ExactTarget`, but only after callers
supply weak Mordell-Weil and a height package for every curve in its scope.
-/
theorem exactTarget_conditional_probe
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

#print axioms exactTarget_conditional_probe
assert_no_sorry exactTarget_conditional_probe
#print sorries exactTarget_conditional_probe

end Stage1Instances.THM_M_0450.Validation
