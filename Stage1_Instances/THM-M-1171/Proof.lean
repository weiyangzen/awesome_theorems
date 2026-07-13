import Mathlib.Analysis.Normed.Operator.Bilinear
import Mathlib.MeasureTheory.Function.LpSeminorm.TriangleInequality

/-!
# THM-M-1171 partial proof execution

This module proves the finite-dimensional operator-norm obligation. It does
not assume or state the unavailable strong `L^p` multiplier estimate. It also
records the finite-sum `L^p` inequality used by the later assembly step.
-/

set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 100000

namespace Stage1Instances.THM_M_1171

private abbrev CoordinateSpace (n : Nat) := Fin n → ℝ

/-- The norm of a bilinear map on `Fin n -> Real` is controlled by the sum of
its values on pairs of standard coordinate vectors. -/
theorem opNorm_le_componentSum {n : Nat}
    (A : CoordinateSpace n →L[ℝ] CoordinateSpace n →L[ℝ] ℝ) :
    ‖A‖ ≤ ∑ i : Fin n, ∑ j : Fin n,
      ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
  apply ContinuousLinearMap.opNorm_le_bound₂ A
    (Finset.sum_nonneg fun _ _ =>
      Finset.sum_nonneg fun _ _ => norm_nonneg _)
  intro x y
  have hxy : A x y = ∑ i : Fin n, ∑ j : Fin n,
      A (Pi.single i (x i)) (Pi.single j (y j)) := by
    calc
      A x y = A (∑ i : Fin n, Pi.single i (x i))
          (∑ j : Fin n, Pi.single j (y j)) := by
            rw [Finset.univ_sum_single, Finset.univ_sum_single]
      _ = ∑ i : Fin n, ∑ j : Fin n,
          A (Pi.single i (x i)) (Pi.single j (y j)) := by
            simp_rw [map_sum, ContinuousLinearMap.sum_apply]
            rw [Finset.sum_comm]
  rw [hxy]
  calc
    ‖∑ i : Fin n, ∑ j : Fin n,
        A (Pi.single i (x i)) (Pi.single j (y j))‖
        ≤ ∑ i : Fin n, ∑ j : Fin n,
          ‖A (Pi.single i (x i)) (Pi.single j (y j))‖ := by
            exact (norm_sum_le _ _).trans
              (Finset.sum_le_sum fun i _ => norm_sum_le _ _)
    _ = ∑ i : Fin n, ∑ j : Fin n,
          (|x i| * |y j|) *
            ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      have hi : Pi.single i (x i) =
          (x i) • (Pi.single i (1 : ℝ) : CoordinateSpace n) := by
        ext k
        simp [Pi.single_apply]
      have hj : Pi.single j (y j) =
          (y j) • (Pi.single j (1 : ℝ) : CoordinateSpace n) := by
        ext k
        simp [Pi.single_apply]
      calc
        ‖A (Pi.single i (x i)) (Pi.single j (y j))‖
            = ‖(x i * y j) •
                A (Pi.single i 1) (Pi.single j 1)‖ := by
              rw [hi, hj, map_smul, map_smul]
              simp
              ring
        _ = |x i| * |y j| *
              ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
              rw [norm_smul, Real.norm_eq_abs, abs_mul]
    _ ≤ ∑ i : Fin n, ∑ j : Fin n,
          (‖x‖ * ‖y‖) *
            ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
      apply Finset.sum_le_sum
      intro i _
      apply Finset.sum_le_sum
      intro j _
      have hx : |x i| ≤ ‖x‖ := by
        simpa [Real.norm_eq_abs] using norm_le_pi_norm x i
      have hy : |y j| ≤ ‖y‖ := by
        simpa [Real.norm_eq_abs] using norm_le_pi_norm y j
      gcongr
    _ = (∑ i : Fin n, ∑ j : Fin n,
          ‖A (Pi.single i 1) (Pi.single j 1)‖) * ‖x‖ * ‖y‖ := by
      calc
        ∑ i : Fin n, ∑ j : Fin n,
            (‖x‖ * ‖y‖) * ‖A (Pi.single i 1) (Pi.single j 1)‖
          = (‖x‖ * ‖y‖) *
              (∑ i : Fin n, ∑ j : Fin n,
                ‖A (Pi.single i 1) (Pi.single j 1)‖) := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro i _
              rw [Finset.mul_sum]
        _ = (∑ i : Fin n, ∑ j : Fin n,
              ‖A (Pi.single i 1) (Pi.single j 1)‖) * ‖x‖ * ‖y‖ := by
              ring

/-- For `p >= 1`, the `L^p` seminorm of a finite scalar sum is bounded by the
sum of the component seminorms. This is the finite-sum analytic ingredient of
the frozen assembly obligation; it does not supply any component estimate. -/
theorem eLpNorm_finset_sum_le {alpha : Type*} [MeasurableSpace alpha]
    {iota : Type*} (s : Finset iota) (f : iota -> alpha -> Real)
    (p : ENNReal) (mu : MeasureTheory.Measure alpha)
    (hf : forall i, i ∈ s -> MeasureTheory.AEStronglyMeasurable (f i) mu)
    (hp : 1 <= p) :
    MeasureTheory.eLpNorm (∑ i ∈ s, f i) p mu <=
      ∑ i ∈ s, MeasureTheory.eLpNorm (f i) p mu := by
  exact MeasureTheory.eLpNorm_sum_le hf hp

#print axioms opNorm_le_componentSum
#print axioms eLpNorm_finset_sum_le

end Stage1Instances.THM_M_1171
