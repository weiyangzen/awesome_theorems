import «Stage1_Instances».«THM-M-1036».Statement

/-!
# THM-M-1036 obligation composition

This module checks only the final logical composition. The analytic existence,
uniqueness, and stochastic-integration packages remain explicit hypotheses.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1036

universe u

/-- The complete strong-existence output required by the root. -/
def StrongExistencePackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (n m : Nat) (D : Problem Omega P n m) (I : IntegralSemantics D),
      I.standard_time_integral -> I.standard_ito_integral ->
        Nonempty (StrongSolution D I)

/-- The complete pathwise-uniqueness output required by the root. -/
def PathwiseUniquenessPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (n m : Nat) (D : Problem Omega P n m) (I : IntegralSemantics D),
      I.standard_time_integral -> I.standard_ito_integral ->
        forall X Y : StrongSolution D I, Indistinguishable X Y

/-- Checked composition of the two complete analytic packages into the root. -/
theorem root_of_existence_and_uniqueness
    (existence : StrongExistencePackage.{u})
    (uniqueness : PathwiseUniquenessPackage.{u}) :
    SdeExistenceUniquenessTarget.{u} := by
  intro Omega _ P _ n m D I htime hito
  exact
    ⟨existence Omega P n m D I htime hito,
      uniqueness Omega P n m D I htime hito⟩

#print axioms root_of_existence_and_uniqueness

end Stage1Instances.THM_M_1036
