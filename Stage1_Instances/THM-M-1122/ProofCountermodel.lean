import Statement

/-!
# THM-M-1122 proof-phase countermodel

The frozen target quantifies over opaque interface predicates.  Consequently,
it is not valid for all of its explicit parameters: the predicates can accept
an arbitrary trace whose law differs from the alleged LERW limit.  This module
kernel-checks that obstruction rather than introducing an unproved body.
-/

namespace Stage1Instances.THM_M_1122

open MeasureTheory ProbabilityTheory

/-- A concrete instantiation refuting universal closure of the frozen target. -/
theorem proofPhaseCountermodel :
    ¬ SchrammLoewnerEvolutionTarget
      (Measure.dirac ()) (Measure.dirac false) True
      (fun _ : Unit ↦ true)
      (fun _ : Bool → ℝ → Unit ↦ True)
      (fun _ : NegativeTime → Unit ↦ fun _ : Bool ↦ True) := by
  intro target
  have hdist : IdentDistrib (fun b : Bool ↦ b) (fun _ : Unit ↦ true)
      (Measure.dirac false) (Measure.dirac ()) :=
    target trivial (fun _ _ ↦ ()) trivial (fun b ↦ b) (fun _ ↦ trivial)
  have impossible := hdist.measure_preimage_eq (MeasurableSet.singleton true)
  simpa using impossible

#print axioms proofPhaseCountermodel

end Stage1Instances.THM_M_1122
