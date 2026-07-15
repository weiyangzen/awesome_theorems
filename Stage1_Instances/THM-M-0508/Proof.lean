import Statement
import ObligationTree

/-!
# THM-M-0508 proof-phase composition interface

This module connects the standalone obligation-tree count to the canonical
statement by a kernel-checked equivalence. It does not prove that the count is
eventually positive and therefore does not prove Vinogradov's theorem.
-/

namespace Stage1Instances.THM_M_0508.Proof

open Stage1Instances.THM_M_0508

/-- The canonical target is exactly eventual positivity of the frozen finite
representation count. This closes the cross-module composition boundary only;
neither direction supplies eventual positivity. -/
theorem vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount :
    VinogradovThreePrimesTarget ↔
      ObligationTree.EventualPositiveRepresentationCount := by
  constructor <;>
    rintro ⟨N, hN⟩ <;>
    refine ⟨N, fun n hn hodd => ?_⟩
  · exact (ObligationTree.representationCount_pos_iff n).mpr (hN n hn hodd)
  · exact (ObligationTree.representationCount_pos_iff n).mp (hN n hn hodd)

/-- Exact canonical root composition from the still-open analytic leaf. -/
theorem vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount
    (h : ObligationTree.EventualPositiveRepresentationCount) :
    VinogradovThreePrimesTarget :=
  vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount.mpr h

#print axioms vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount
#print sorries vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount
#print axioms vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount
#print sorries vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount

end Stage1Instances.THM_M_0508.Proof
