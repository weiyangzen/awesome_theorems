import CoordinateBridge
import Mathlib.Analysis.SpecialFunctions.Log.PosLog
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

open MeasureTheory
open scoped Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

instance instOpensMeasurableSpaceMatrixBridge {d : Nat} :
    OpensMeasurableSpace (Matrix (Fin d) (Fin d) Real) :=
  inferInstanceAs (OpensMeasurableSpace (Fin d -> Fin d -> Real))

variable {Omega : Type u} [MeasurableSpace Omega]
variable {mu : Measure Omega} [IsProbabilityMeasure mu]
variable {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
variable [FiniteDimensional Real E]

def bridgeLogPlus (x : Real) : Real := max (Real.log x) 0

theorem logPlus_eq_posLog (x : Real) : bridgeLogPlus x = Real.posLog x := by
  rw [bridgeLogPlus, Real.posLog_def, max_comm]

theorem stronglyMeasurable_posLog_norm
    {F : Omega → E →L[Real] E} (hF : StronglyMeasurable F) :
    StronglyMeasurable (fun omega => Real.posLog ‖F omega‖) := by
  exact ((Measurable.max measurable_const
    (Real.measurable_log.comp hF.norm.measurable))).stronglyMeasurable

theorem norm_conjugateCLM_le
    (L : E →L[Real] E) :
    ‖conjugateCLM L‖ ≤
      ‖(coordEquiv (E := E)).toContinuousLinearMap‖ *
        (‖L‖ * ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖) := by
  exact (ContinuousLinearMap.opNorm_comp_le _ _).trans
    (mul_le_mul_of_nonneg_left (ContinuousLinearMap.opNorm_comp_le _ _) (norm_nonneg _))

theorem posLog_norm_matrixOfCLM_le
    (L : E →L[Real] E) :
    Real.posLog ‖matrixOfCLM L‖ ≤
      Real.posLog ‖(coordEquiv (E := E)).toContinuousLinearMap‖ +
        (Real.posLog ‖L‖ +
          Real.posLog ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖) := by
  rw [← Matrix.l2_opNorm_toEuclideanCLM, toEuclideanCLM_matrixOfCLM]
  calc
    Real.posLog ‖conjugateCLM L‖ ≤
        Real.posLog
          (‖(coordEquiv (E := E)).toContinuousLinearMap‖ *
            (‖L‖ * ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖)) :=
      Real.posLog_le_posLog (norm_nonneg _) (norm_conjugateCLM_le L)
    _ ≤ _ := le_trans Real.posLog_mul
      (add_le_add_right Real.posLog_mul _)

theorem integrable_posLog_norm_matrixOfCLM
    {F : Omega → E →L[Real] E} (hF : StronglyMeasurable F)
    (hint : Integrable (fun omega => Real.posLog ‖F omega‖) mu) :
    Integrable (fun omega => Real.posLog ‖matrixOfCLM (F omega)‖) mu := by
  have hmat : StronglyMeasurable (fun omega => matrixOfCLM (F omega)) := by
    let invLM :
        (EuclideanSpace Real (Fin (dE (E := E))) →L[Real]
          EuclideanSpace Real (Fin (dE (E := E)))) →ₗ[Real]
        Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real :=
      { toFun := (Matrix.toEuclideanCLM (n := Fin (dE (E := E))) (𝕜 := Real)).symm
        map_add' := map_add _
        map_smul' := map_smul _ }
    let inv := invLM.toContinuousLinearMap
    have hconj := stronglyMeasurable_conjugateCLM (F := F) hF
    have h := inv.continuous.comp_stronglyMeasurable hconj
    simpa only [inv, invLM, matrixOfCLM] using h
  have hmeas : AEStronglyMeasurable
      (fun omega => Real.posLog ‖matrixOfCLM (F omega)‖) mu :=
    ((Measurable.max measurable_const
      (Real.measurable_log.comp hmat.norm.measurable))).stronglyMeasurable.aestronglyMeasurable
  let C : Real :=
    Real.posLog ‖(coordEquiv (E := E)).toContinuousLinearMap‖ +
      Real.posLog ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖
  have hdom : Integrable (fun omega => C + Real.posLog ‖F omega‖) mu :=
    (integrable_const C).add hint
  apply hdom.mono' hmeas
  filter_upwards with omega
  rw [Real.norm_eq_abs, abs_of_nonneg Real.posLog_nonneg]
  have h := posLog_norm_matrixOfCLM_le (F omega)
  dsimp [C]
  linarith

theorem integrable_posLog_norm_matrixOfCLM_of_measurable_matrix
    {F : Omega → E →L[Real] E}
    (hF : Measurable (fun omega => matrixOfCLM (F omega)))
    (hint : Integrable (fun omega => Real.posLog ‖F omega‖) mu) :
    Integrable (fun omega => Real.posLog ‖matrixOfCLM (F omega)‖) mu := by
  have hmeas : AEStronglyMeasurable
      (fun omega => Real.posLog ‖matrixOfCLM (F omega)‖) mu :=
    ((Measurable.max measurable_const
      (Real.measurable_log.comp hF.norm))).stronglyMeasurable.aestronglyMeasurable
  let C : Real :=
    Real.posLog ‖(coordEquiv (E := E)).toContinuousLinearMap‖ +
      Real.posLog ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖
  have hdom : Integrable (fun omega => C + Real.posLog ‖F omega‖) mu :=
    (integrable_const C).add hint
  apply hdom.mono' hmeas
  filter_upwards with omega
  rw [Real.norm_eq_abs, abs_of_nonneg Real.posLog_nonneg]
  have h := posLog_norm_matrixOfCLM_le (F omega)
  dsimp [C]
  linarith

end Stage1Instances.THM_M_1056

