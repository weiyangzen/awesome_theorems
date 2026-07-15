import GrowthBridge
import ErgodicTheory.TwoSided.SplittingAssembly

open Filter Function MeasureTheory
open scoped Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

variable {Omega : Type u} [MeasurableSpace Omega]
variable {mu : Measure Omega} [IsProbabilityMeasure mu]
variable {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
variable [FiniteDimensional Real E]

theorem external_oseledets_on_arbitrary_fiber_coordinates
    (T : Omega ≃ᵐ Omega) (hT : Ergodic T mu)
    (A : Omega -> E ≃L[Real] E)
    (hAstrong : StronglyMeasurable (fun omega => (A omega).toContinuousLinearMap))
    (hint : Integrable (fun omega => bridgeLogPlus ‖(A omega).toContinuousLinearMap‖) mu)
    (hint' : Integrable (fun omega => bridgeLogPlus ‖(A omega).symm.toContinuousLinearMap‖) mu) :
    ∃ (k : Nat) (lambda : Fin k -> Real)
      (V : Fin k -> Omega -> Submodule Real
        (EuclideanSpace Real (Fin (dE (E := E))))),
      StrictAnti lambda ∧
      (∀ i, ErgodicTheory.MeasurableSubspace (fun omega => V i omega)) ∧
      ∀ᵐ omega ∂mu,
        DirectSum.IsInternal (fun i => V i omega) ∧
        (∀ i, V i omega ≠ ⊥) ∧
        (∀ i, Submodule.map
          (Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)).toLinearMap
          (V i omega) = V i (T omega)) ∧
        (∀ i, ∀ y ∈ V i omega, y ≠ 0 ->
          Tendsto
            (fun n : Nat => (n : Real)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := Real)
                (ErgodicTheory.cocycle (matrixGenerator A) T n omega) y‖)
            atTop (nhds (lambda i)) ∧
          Tendsto
            (fun n : Nat => (n : Real)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := Real)
                (ErgodicTheory.cocycle (matrixGenerator A) T n ((T.symm : Omega -> Omega)^[n] omega))⁻¹ y‖)
            atTop (nhds (-lambda i))) := by
  have hmeas : Measurable (matrixGenerator A) :=
    measurable_matrixOfCLM hAstrong
  have hdet : ∀ omega, (matrixGenerator A omega).det ≠ 0 :=
    fun omega => det_matrixOf_equiv_ne_zero (A omega)
  have hpos : ErgodicTheory.IntegrableLogNorm (matrixGenerator A) mu := by
    apply integrable_posLog_norm_matrixOfCLM hAstrong
    simpa only [logPlus_eq_posLog] using hint
  have hposinv : ErgodicTheory.IntegrableLogNorm
      (fun omega => (matrixGenerator A omega)⁻¹) mu := by
    have hinvmeas : Measurable (fun omega =>
        matrixOfCLM (A omega).symm.toContinuousLinearMap) := by
      simpa only [matrixOf_equiv_symm] using
        ErgodicTheory.measurable_inv_matrix.comp hmeas
    have h := integrable_posLog_norm_matrixOfCLM_of_measurable_matrix hinvmeas
      (show Integrable (fun omega => Real.posLog ‖(A omega).symm.toContinuousLinearMap‖) mu by
        simpa only [logPlus_eq_posLog] using hint')
    simpa only [matrixOf_equiv_symm] using h
  exact ErgodicTheory.oseledets_splitting hT (matrixGenerator A) hdet hmeas hpos hposinv

end Stage1Instances.THM_M_1056

