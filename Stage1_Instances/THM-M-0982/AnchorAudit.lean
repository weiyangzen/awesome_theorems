import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-!
# THM-M-0982: pinned formal-anchor audit

This module checks the two mathlib declarations selected by the audit and an
exact wrapper for the frozen conjunction. It is candidate evidence only; later
obligation, proof, validation, and release phases remain separate gates.
-/

noncomputable section

open Filter MeasureTheory Set Topology

universe u

namespace Stage1Instances.THM_M_0982.AnchorAudit

/-- Exact local copy of the frozen statement, used to test candidate fit
without importing or changing the statement artifact. -/
def AuditedTarget : Prop :=
  (∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) →
      Monotone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋃ n, A n)))) ∧
  (∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) →
      Antitone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋂ n, A n))))

/-- Candidate wrapper composed only from the two pinned mathlib continuity
anchors and the probability-measure finiteness fact. -/
theorem auditedTarget_mathlib : AuditedTarget.{u} := by
  constructor
  · intro Omega _ P _ A _ hmono
    simpa [Function.comp_def] using
      (tendsto_measure_iUnion_atTop (μ := P) hmono)
  · intro Omega _ P _ A hmeas hanti
    simpa [Function.comp_def] using
      (tendsto_measure_iInter_atTop (μ := P)
        (fun n => (hmeas n).nullMeasurableSet) hanti
        ⟨0, measure_ne_top P (A 0)⟩)

#check MeasureTheory.tendsto_measure_iUnion_atTop
#check MeasureTheory.tendsto_measure_iInter_atTop
#check MeasureTheory.measure_ne_top
#check MeasurableSet.nullMeasurableSet
#check auditedTarget_mathlib

#print axioms MeasureTheory.tendsto_measure_iUnion_atTop
#print axioms MeasureTheory.tendsto_measure_iInter_atTop
#print axioms auditedTarget_mathlib

end Stage1Instances.THM_M_0982.AnchorAudit
