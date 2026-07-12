import Statement
import ObligationTree

/-!
# THM-M-0987 proof-phase bodies

This module closes the exact one-dimensional real-valued i.i.d. central limit
target with the terminal theorem in the repository's pinned mathlib snapshot.
The imported theorem retains every binder and hypothesis frozen by the
statement phase, including the zero-variance case.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Finset
open scoped Real Topology

namespace Stage1Instances.THM_M_0987

universe uOmega uOmega'

/-- Placeholder-free proof of the exact proposition frozen in `Statement.lean`. -/
theorem centralLimitTheorem_proof :
    CentralLimitTheoremTarget.{uOmega, uOmega'} := by
  intro Omega Omega' _ _ P P' _ _ X Y hY hL2 hIndep hIdent
  exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hY hL2 hIndep hIdent

#print axioms centralLimitTheorem_proof

end Stage1Instances.THM_M_0987

namespace Stage1Instances.THM_M_0987.ObligationTree

universe uOmega uOmega'

/-- The pinned bridge obligation is discharged by the terminal mathlib CLT. -/
theorem pinnedBridge_proof : PinnedBridge.{uOmega, uOmega'} := by
  intro Omega Omega' _ _ P P' _ _ X Y hY hL2 hIndep hIdent
  exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hY hL2 hIndep hIdent

/-- Checked final composition from the discharged bridge to the frozen root. -/
theorem canonicalRoot_proof : CanonicalRoot.{uOmega, uOmega'} :=
  root_of_pinnedBridge pinnedBridge_proof

#print axioms pinnedBridge_proof
#print axioms canonicalRoot_proof

end Stage1Instances.THM_M_0987.ObligationTree
