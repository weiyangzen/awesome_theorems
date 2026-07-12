/-!
# THM-M-1061 proof-phase kernel lemmas

These lemmas discharge the direct boundary projections used by both analytic
branches.  They are intentionally stated against the frozen `SatisfiesLDP`
definition, so each body is checked rather than recorded only in prose.

The lower-bound localization, compact-core estimate, tail estimate, and
extended-real limit merge are not supplied by the pinned dependency closure.
Consequently this module is partial proof work and does not close the root.
-/

namespace Stage1Instances.THM_M_1061.Proof

open Filter MeasureTheory

universe u

variable {X : Type u} [MeasurableSpace X] [TopologicalSpace X]
variable {mu : Nat -> Measure X} {a : Nat -> Real} {I : X -> ENNReal}

/-- The probability-measure boundary is a direct consequence of the frozen
full-LDP hypothesis. -/
theorem probabilityMeasure_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall n, IsProbabilityMeasure (mu n) :=
  h.1

/-- Every speed is strictly positive under the frozen full-LDP hypothesis. -/
theorem speed_pos_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall n, 0 < a n :=
  h.2.1

/-- The speed tends to zero under the frozen full-LDP hypothesis. -/
theorem speed_tendsto_zero_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    Tendsto a atTop (nhds 0) :=
  h.2.2.1

/-- Package the three elementary boundary facts without changing their types. -/
theorem basic_boundaries_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    (forall n, IsProbabilityMeasure (mu n)) /\
      (forall n, 0 < a n) /\ Tendsto a atTop (nhds 0) :=
  ⟨probabilityMeasure_of_satisfiesLDP h,
    speed_pos_of_satisfiesLDP h,
    speed_tendsto_zero_of_satisfiesLDP h⟩

#check probabilityMeasure_of_satisfiesLDP
#check speed_pos_of_satisfiesLDP
#check speed_tendsto_zero_of_satisfiesLDP
#check basic_boundaries_of_satisfiesLDP

#print axioms probabilityMeasure_of_satisfiesLDP
#print axioms speed_pos_of_satisfiesLDP
#print axioms speed_tendsto_zero_of_satisfiesLDP
#print axioms basic_boundaries_of_satisfiesLDP

end Stage1Instances.THM_M_1061.Proof
