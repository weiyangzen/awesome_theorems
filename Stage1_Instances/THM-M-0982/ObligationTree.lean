import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-! Conditional composition checks for the frozen THM-M-0982 architecture. -/

noncomputable section

open Filter MeasureTheory Set Topology

universe u

namespace Stage1Instances.THM_M_0982.ObligationTree

def Below : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) → Monotone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋃ n, A n)))

def Above : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) → Antitone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋂ n, A n)))

def Target : Prop := Below.{u} ∧ Above.{u}

/-- The exact root is obtained only from both independently tracked branches. -/
theorem target_of_branches (below : Below.{u}) (above : Above.{u}) : Target.{u} :=
  ⟨below, above⟩

/-- Ordinary event measurability supplies the null-measurability input of the
continuity-from-above anchor. -/
theorem measurable_to_nullMeasurable {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (A : Nat → Set Omega)
    (hA : ∀ n, MeasurableSet (A n)) :
    ∀ n, NullMeasurableSet (A n) P :=
  fun n => (hA n).nullMeasurableSet

/-- Probability normalization supplies the finite-member premise of the
continuity-from-above anchor. -/
theorem probability_member_ne_top {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P] (A : Nat → Set Omega) :
    P (A 0) ≠ ⊤ :=
  measure_ne_top P (A 0)

#check MeasureTheory.tendsto_measure_iUnion_atTop
#check MeasureTheory.tendsto_measure_iInter_atTop
#check target_of_branches
#print axioms target_of_branches
#print axioms measurable_to_nullMeasurable
#print axioms probability_member_ne_top

end Stage1Instances.THM_M_0982.ObligationTree
