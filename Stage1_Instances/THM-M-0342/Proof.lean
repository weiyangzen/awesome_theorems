import ObligationTree

/-!
# THM-M-0342 proof-phase bodies

This module closes the frozen exact norm anchor with the pinned mathlib
Plancherel theorem, then checks its composition into the exact target.
-/

open MeasureTheory
open scoped FourierTransform ENNReal

namespace Stage1Instances.THM_M_0342

/-- The pinned mathlib norm theorem discharges the exact frozen anchor. -/
theorem exactNormAnchor_proof : ExactNormAnchor := by
  intro n f hf
  exact MeasureTheory.Lp.norm_fourier_eq (hf.toLp f)

/-- Unconditional proof of the exact frozen Plancherel target. -/
theorem plancherelTarget_proof : PlancherelTarget :=
  root_of_exact_norm_anchor exactNormAnchor_proof

#check exactNormAnchor_proof
#print axioms exactNormAnchor_proof
#check plancherelTarget_proof
#print axioms plancherelTarget_proof

end Stage1Instances.THM_M_0342
