import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1019 pinned anchor audit

This file checks that the immutable mathlib declaration `Measure.ext_of_charFun` closes the exact
statement frozen by the preceding phase. It is candidate evidence for the anchor-audit phase, not a
release or theorem-completion claim.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1019.AnchorAudit

/-- Exact wrapper from the frozen probability-measure target to pinned mathlib's finite-measure
extensionality theorem. -/
theorem pinned_mathlib_candidate :
    forall (mu nu : Measure Real),
      IsProbabilityMeasure mu ->
      IsProbabilityMeasure nu ->
      charFun mu = charFun nu ->
      mu = nu := by
  intro mu nu hmu hnu hchar
  letI : IsProbabilityMeasure mu := hmu
  letI : IsProbabilityMeasure nu := hnu
  exact Measure.ext_of_charFun hchar

#check Measure.ext_of_charFun
#check pinned_mathlib_candidate
#print axioms Measure.ext_of_charFun
#print axioms pinned_mathlib_candidate

end Stage1Instances.THM_M_1019.AnchorAudit
