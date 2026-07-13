import Statement
import Birkhoff
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1053 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen root directly from the locally ported Birkhoff theorems. This is same-worker differential
corroboration, not a distinct proof body or independent-runner attestation.
-/

noncomputable section

open Filter Function MeasureTheory

namespace Stage1.THM_M_1053.Validation

universe u

/-- A separately written exact-type reconstruction from the ported terminal theorems. -/
theorem differentialStatementShape : Stage1.THM_M_1053.StatementShape.{u} := by
  intro X _ mu _ T hT f hf
  let g : X -> Real := mu[f | MeasurableSpace.invariants T]
  have hgLim :
      ∀ᵐ x ∂mu, Tendsto (fun n : Nat =>
        Stage1.THM_M_1053.timeAverage T f n x) atTop (nhds (g x)) := by
    simpa only [Stage1.THM_M_1053.timeAverage, birkhoffAverage, birkhoffSum,
      smul_eq_mul] using ErgodicTheory.tendsto_birkhoffAverage_ae hT hf
  refine ⟨g, integrable_condExp, ?_, hgLim, ?_⟩
  · exact ErgodicTheory.condExp_invariants_comp_self hT hT.measurable hf
  · intro hErgodic
    have hIntegralLim :
        ∀ᵐ x ∂mu, Tendsto (fun n : Nat =>
          Stage1.THM_M_1053.timeAverage T f n x) atTop
          (nhds (∫ y, f y ∂mu)) := by
      simpa only [Stage1.THM_M_1053.timeAverage, birkhoffAverage, birkhoffSum,
        smul_eq_mul] using
        ErgodicTheory.tendsto_birkhoffAverage_ae_integral hErgodic hf
    filter_upwards [hgLim, hIntegralLim] with x hx hIntegral
    exact tendsto_nhds_unique hx hIntegral

assert_no_sorry ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
assert_no_sorry ErgodicTheory.tendsto_birkhoffAverage_ae
assert_no_sorry ErgodicTheory.tendsto_birkhoffAverage_ae_integral
assert_no_sorry differentialStatementShape

#print sorries ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print sorries differentialStatementShape

#print axioms ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print axioms differentialStatementShape

end Stage1.THM_M_1053.Validation
