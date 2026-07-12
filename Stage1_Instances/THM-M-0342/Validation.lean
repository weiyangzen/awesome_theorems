import Statement

/-!
# THM-M-0342 same-worker differential validation

This module reconstructs the exact target directly from the pinned mathlib
anchor. It deliberately imports neither `Proof` nor `ObligationTree`.
-/

open MeasureTheory
open scoped FourierTransform ENNReal

namespace Stage1Instances.THM_M_0342.Validation

/-- Direct reconstruction of the frozen target for differential checking. -/
theorem plancherelTarget_direct :
    Stage1Instances.THM_M_0342.PlancherelTarget := by
  intro n f hf
  exact MeasureTheory.Lp.norm_fourier_eq (hf.toLp f)

#check plancherelTarget_direct
#print axioms plancherelTarget_direct

end Stage1Instances.THM_M_0342.Validation
