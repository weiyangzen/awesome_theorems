import ObligationTree
import Birkhoff

/-!
# THM-M-1055 proof installation

This module applies the locally ported pointwise Birkhoff theorem to the exact
frozen target. The analytic proof bodies are in `External/MaximalErgodic.lean`
and `External/Birkhoff.lean`.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1055

universe u

/-- The full invariant-limit package required by the frozen composition. -/
theorem invariantLimitPackage_proof : InvariantLimitPackage.{u} := by
  intro Omega _ mu _ T f hT hf
  refine ⟨fun _ => ∫ y, f y ∂mu, ?_, Eventually.of_forall (fun _ => rfl)⟩
  exact ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf

/-- The exact canonical Birkhoff ergodic target. -/
theorem birkhoffErgodicTarget : BirkhoffErgodicTarget.{u} :=
  root_of_invariantLimitPackage invariantLimitPackage_proof

#check ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#check invariantLimitPackage_proof
#check birkhoffErgodicTarget

#print sorries ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print sorries invariantLimitPackage_proof
#print sorries birkhoffErgodicTarget

#print axioms ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print axioms ErgodicTheory.condExp_invariants_comp
#print axioms ErgodicTheory.ae_tendsto_orbit_div_atTop_zero
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print axioms invariantLimitPackage_proof
#print axioms birkhoffErgodicTarget

end Stage1Instances.THM_M_1055
