import Statement

/-!
# THM-M-1019 proof execution

This module proves the exact characteristic-function uniqueness proposition frozen in
`Statement.lean`. The two explicit probability hypotheses are installed as local instances before
the pinned mathlib uniqueness theorem is invoked.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1019.Proof

open Stage1Instances.THM_M_1019

/-- Equality of the characteristic functions of two real probability measures determines the
measures. This has exactly the frozen `Statement` type. -/
theorem characteristicFunctionUniqueness : Statement := by
  intro mu nu hmu hnu hchar
  letI : IsProbabilityMeasure mu := hmu
  letI : IsProbabilityMeasure nu := hnu
  exact Measure.ext_of_charFun hchar

#check characteristicFunctionUniqueness
#print axioms characteristicFunctionUniqueness

end Stage1Instances.THM_M_1019.Proof
