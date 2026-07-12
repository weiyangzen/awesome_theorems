import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-0981: anchor audit

This file checks the types and composition of the minimal mathlib candidates.
It deliberately defines an audit-local target rather than claiming that the
later proof phase has integrated a proof of the canonical declaration.
-/

open Function MeasureTheory Set

namespace Stage1Instances.THM_M_0981.AnchorAudit

universe u

def CandidateTarget (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P ->
    P (∅ : Set Omega) = 0 /\
      P univ = 1 /\
        forall A : Nat -> Set Omega,
          (forall n, MeasurableSet (A n)) ->
            Pairwise (Disjoint on A) ->
              P (iUnion A) = tsum (fun n => P (A n))

/-- Candidate composition check only: `Measure.empty`, the probability class's
normalization field, and `measure_iUnion` have the required combined type. -/
theorem candidateTarget_by_mathlib
    (Omega : Type u) [MeasurableSpace Omega] : CandidateTarget Omega := by
  intro P hP
  letI : IsProbabilityMeasure P := hP
  refine And.intro (measure_empty) (And.intro measure_univ ?_)
  intro A hmeas hdisjoint
  exact measure_iUnion hdisjoint hmeas

#check measure_empty
#check IsProbabilityMeasure.measure_univ
#check measure_iUnion
#print axioms candidateTarget_by_mathlib

end Stage1Instances.THM_M_0981.AnchorAudit
