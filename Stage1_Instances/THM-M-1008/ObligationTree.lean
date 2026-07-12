import Statement
import Mathlib.Probability.Independence.ZeroOne

/-!
# THM-M-1008 conditional obligation composition

This module checks the last semantic bridge and the pinned zero-one endpoint.
The self-independence package remains an explicit premise: no Hewitt-Savage
proof or root closure is asserted here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1008

universe u v

/-- Output required from the finite-coordinate approximation and permutation route. -/
def SelfIndependencePackage : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> E) (event : Set (Nat -> E)),
      iIndepFun X mu ->
      (forall i j : Nat, IdentDistrib (X i) (X j) mu mu) ->
      MeasurableSet event ->
      IsSymmetricEvent event ->
      IndepSet (processPath X ⁻¹' event) (processPath X ⁻¹' event) mu

/-- The audited mathlib endpoint turns self-independence into zero-or-one measure. -/
theorem zeroOne_of_selfIndependence
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] {s : Set Omega}
    (hself : IndepSet s s mu) : mu s = 0 ∨ mu s = 1 :=
  measure_eq_zero_or_one_of_indepSet_self hself

/-- Checked composition of the open bridge and pinned endpoint into the exact root. -/
theorem root_of_selfIndependencePackage
    (bridge : SelfIndependencePackage.{u, v}) :
    HewittSavageZeroOneTarget.{u, v} := by
  intro Omega E _ _ mu _ X event hindep hiid hmeas hsymm
  exact zeroOne_of_selfIndependence mu
    (bridge Omega E mu X event hindep hiid hmeas hsymm)

#print axioms zeroOne_of_selfIndependence
#print axioms root_of_selfIndependencePackage

end Stage1Instances.THM_M_1008
