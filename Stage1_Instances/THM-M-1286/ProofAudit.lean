import Mathlib.Analysis.InnerProductSpace.PiL2
import «Stage1_Instances».«THM-M-1286».Statement

open scoped ENNReal MeasureTheory

namespace Stage1Instances.THM_M_1286.ProofAudit

open MeasureTheory

/-!
These checked lemmas expose a mismatch in the frozen proof target. The
abbreviation named `Euclidean` is an ordinary finite Pi type, so its norm is
the coordinate supremum norm. This file is a proof-phase blocker certificate;
it does not prove or refute the complete root proposition.
-/

/-- The frozen vector type has the ordinary finite Pi supremum norm. -/
theorem frozen_vector_norm_eq_coordinate_sup {n : Nat} (x : Euclidean n) :
    ‖x‖ = (Finset.univ.sup fun i => ‖x i‖₊ : NNReal) := by
  exact Pi.norm_def x

/-- A concrete norm calculation on the frozen domain. -/
theorem frozen_finTwo_vector_norm : ‖(![1, -1] : Euclidean 2)‖ = 1 := by
  apply le_antisymm
  · rw [pi_norm_le_iff_of_nonneg (by norm_num : (0 : Real) ≤ 1)]
    intro i
    fin_cases i <;> norm_num
  · have h := norm_le_pi_norm (![1, -1] : Euclidean 2) (0 : Fin 2)
    norm_num at h ⊢
    exact h

/-- The actual mathlib Euclidean-space encoding gives squared norm two for
the same coordinates, in contrast to `frozen_finTwo_vector_norm`. -/
theorem standard_euclidean_finTwo_vector_norm_sq :
    ‖(!₂[1, -1] : EuclideanSpace Real (Fin 2))‖ ^ 2 = 2 := by
  rw [EuclideanSpace.real_norm_sq_eq]
  norm_num [Fin.sum_univ_two]

/-- At exponent one, the frozen gradient energy integrates the norm installed
on `Euclidean n`, hence the coordinate supremum norm above. -/
theorem frozen_gradient_eLpNorm_one_eq_lintegral
    {n : Nat} (g : Euclidean n → Euclidean n) :
    eLpNorm g 1 volume = ∫⁻ x, ‖g x‖ₑ ∂volume := by
  exact eLpNorm_one_eq_lintegral_enorm

/-- Metric balls for the frozen finite Pi type have the product/sup-metric
volume formula, rather than the Euclidean-ball formula. -/
theorem frozen_metric_ball_volume {n : Nat} (r : Real) (hr : 0 < r) :
    volume (Metric.ball (0 : Euclidean n) r) =
      ENNReal.ofReal ((2 * r) ^ Fintype.card (Fin n)) := by
  exact Real.volume_pi_ball _ hr

#print axioms frozen_vector_norm_eq_coordinate_sup
#print axioms frozen_finTwo_vector_norm
#print axioms standard_euclidean_finTwo_vector_norm_sq
#print axioms frozen_gradient_eLpNorm_one_eq_lintegral
#print axioms frozen_metric_ball_volume

end Stage1Instances.THM_M_1286.ProofAudit
