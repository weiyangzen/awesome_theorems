import ObligationTree
import Birkhoff

/-!
# THM-M-1053 proof installation

The exact frozen root is proved from the locally ported pointwise Birkhoff
theorem. The general limit is the conditional expectation onto the invariant
sigma-algebra. In the ergodic branch, uniqueness of limits compares that
general limit with the port's space-integral corollary.

The pre-proof `ErgodicLimitIdentificationPackage` remains inconsistent because
it omits the relation between `f` and an arbitrary invariant `g`. The exact
root proof therefore cannot pass through `statementShape_of_packages`; the
counterexample below records that frozen-graph defect without weakening the
canonical theorem.
-/

noncomputable section

open Filter Function MeasureTheory

namespace Stage1.THM_M_1053

universe u

/-- The general invariant-limit package, implemented by conditional
expectation onto the invariant measurable space. -/
theorem generalInvariantLimitPackage_proof :
    GeneralInvariantLimitPackage.{u} := by
  intro X _ mu _ T hT f hf
  let g : X -> Real := mu[f | MeasurableSpace.invariants T]
  refine ⟨g, integrable_condExp, ?_, ?_⟩
  · exact ErgodicTheory.condExp_invariants_comp_self hT hT.measurable hf
  · simpa only [timeAverage, birkhoffAverage, birkhoffSum, smul_eq_mul] using
      ErgodicTheory.tendsto_birkhoffAverage_ae hT hf

/-- Placeholder-free proof of the exact canonical statement. The ergodic
identification follows by uniqueness between the general Birkhoff limit and
the independently proved ergodic space-integral limit. -/
theorem statementShape_proof : StatementShape.{u} := by
  intro X _ mu _ T hT f hf
  obtain ⟨g, hgInt, hgInv, hgLim⟩ :=
    generalInvariantLimitPackage_proof X _ mu
      (inferInstance : IsProbabilityMeasure mu) T hT f hf
  refine ⟨g, hgInt, hgInv, hgLim, ?_⟩
  intro hErgodic
  have hIntegralLim :
      ∀ᵐ x ∂mu, Tendsto (fun n : Nat => timeAverage T f n x) atTop
        (nhds (∫ y, f y ∂mu)) := by
    simpa only [timeAverage, birkhoffAverage, birkhoffSum, smul_eq_mul] using
      ErgodicTheory.tendsto_birkhoffAverage_ae_integral hErgodic hf
  filter_upwards [hgLim, hIntegralLim] with x hx hIntegral
  exact tendsto_nhds_unique hx hIntegral

/-- The identity map on a one-point probability space is ergodic. -/
private theorem ergodic_id_punit :
    Ergodic (id : PUnit -> PUnit) (Measure.dirac PUnit.unit) := by
  refine ⟨MeasurePreserving.id _, ?_⟩
  constructor
  intro s _hs _hinv
  rw [Filter.eventuallyConst_set', ae_dirac_eq]
  by_cases h : PUnit.unit ∈ s
  · refine Or.inr ?_
    rw [Filter.EventuallyEq, Filter.eventually_pure]
    apply propext
    exact iff_true_intro h
  · refine Or.inl ?_
    rw [Filter.EventuallyEq, Filter.eventually_pure]
    apply propext
    exact iff_false_intro h

/-- Formal obstruction to closing the inconsistent frozen identification
package. This does not refute `StatementShape`. -/
theorem not_ergodicLimitIdentificationPackage :
    ¬ ErgodicLimitIdentificationPackage.{0} := by
  intro identify
  let mu : Measure PUnit := Measure.dirac PUnit.unit
  haveI : IsProbabilityMeasure mu := inferInstance
  have h := identify PUnit inferInstance mu inferInstance id
    (MeasurePreserving.id mu) (fun _ => 0) (fun _ => 1)
    (by fun_prop) (by fun_prop) (by simp) ergodic_id_punit
  simpa [mu, ae_dirac_eq] using h

#check generalInvariantLimitPackage_proof
#check statementShape_proof
#print sorries ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print sorries generalInvariantLimitPackage_proof
#print sorries statementShape_proof
#print sorries not_ergodicLimitIdentificationPackage
#print axioms ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print axioms generalInvariantLimitPackage_proof
#print axioms statementShape_proof
#print axioms not_ergodicLimitIdentificationPackage

end Stage1.THM_M_1053
