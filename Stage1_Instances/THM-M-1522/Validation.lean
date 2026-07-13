import Statement
import Birkhoff
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-1522 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact frozen target directly from the vendored terminal
theorem. This is a same-worker differential check, not the distinct signed
runner required for release-grade independent verification.
-/

open Filter MeasureTheory

namespace Stage1Instances.THM_M_1522.Validation

universe u

/-- A separately written exact-root adapter over the frozen statement. -/
theorem independentlyReconstructedBirkhoffPointwiseErgodic :
    Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget.{u} := by
  intro X _ mu _ T f hT hf
  exact ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf

#check independentlyReconstructedBirkhoffPointwiseErgodic
assert_no_sorry ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
assert_no_sorry ErgodicTheory.tendsto_birkhoffAverage_ae
assert_no_sorry ErgodicTheory.tendsto_birkhoffAverage_ae_integral
assert_no_sorry independentlyReconstructedBirkhoffPointwiseErgodic
#print sorries ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print sorries independentlyReconstructedBirkhoffPointwiseErgodic
#print axioms ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print axioms independentlyReconstructedBirkhoffPointwiseErgodic

end Stage1Instances.THM_M_1522.Validation
