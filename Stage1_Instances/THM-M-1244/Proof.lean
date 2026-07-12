import ObligationTree

/-!
# THM-M-1244 proof execution

This module discharges the finite-dimensional energy mismatch independently of
the unavailable external logarithmic Sobolev package.
-/

namespace Stage1Instances.THM_M_1244

open MeasureTheory
open scoped BigOperators

/-- Every coordinate square of a functional on the product sup norm is
controlled collectively by its squared operator norm. -/
theorem coordinateEnergy_le_operatorEnergy {n : Nat}
    (L : Euclidean n →L[Real] Real) :
    (∑ i : Fin n, (L (Pi.single i 1)) ^ 2) <= ‖L‖ ^ 2 := by
  classical
  by_cases hn : n = 0
  · subst n
    simp
  let signs : Euclidean n := fun i => if 0 <= L (Pi.single i 1) then 1 else -1
  have hsigns : ‖signs‖ = 1 := by
    apply le_antisymm
    · exact (pi_norm_le_iff_of_nonneg (by positivity)).2 (fun i => by
        dsimp [signs]
        split <;> simp)
    · have hi : Fin n := ⟨0, Nat.pos_of_ne_zero hn⟩
      calc
        1 = ‖signs hi‖ := by
          dsimp [signs]
          split <;> simp
        _ <= ‖signs‖ := norm_le_pi_norm signs hi
  have hsum : (∑ i : Fin n, |L (Pi.single i 1)|) = L signs := by
    rw [show signs = ∑ i : Fin n, ((if 0 <= L (Pi.single i 1) then 1 else -1) •
        Pi.single i 1) by
      ext j
      simp only [Finset.sum_apply]
      rw [Finset.sum_eq_single j]
      · simp [signs]
      · intro b _ hb
        simp [hb]
      · simp
    ]
    simp only [map_sum]
    apply Finset.sum_congr rfl
    intro i _
    split_ifs with hi
    · simp [abs_of_nonneg hi]
    · simp [abs_of_neg (lt_of_not_ge hi)]
  calc
    (∑ i : Fin n, (L (Pi.single i 1)) ^ 2)
        <= (∑ i : Fin n, |L (Pi.single i 1)|) ^ 2 :=
      (by
        simpa only [sq_abs] using
          (Finset.sum_sq_le_sq_sum_of_nonneg (s := Finset.univ)
            (fun i _ => abs_nonneg (L (Pi.single i 1)))))
    _ = |L signs| ^ 2 := by rw [hsum, sq_abs]
    _ <= (‖L‖ * ‖signs‖) ^ 2 := by
      gcongr
      simpa only [Real.norm_eq_abs] using L.le_opNorm signs
    _ = ‖L‖ ^ 2 := by rw [hsigns, mul_one]

/-- The pointwise energy comparison integrated against the standard Gaussian. -/
theorem coordinateEnergy_integral_le {n : Nat} (f : Euclidean n -> Real)
    (henergy : Integrable (fun x => ‖fderiv Real f x‖ ^ 2) (standardGaussian n)) :
    (∫ x, coordinateEnergy f x ∂(standardGaussian n)) <=
      ∫ x, ‖fderiv Real f x‖ ^ 2 ∂(standardGaussian n) := by
  apply integral_mono_of_nonneg
  · exact Filter.Eventually.of_forall (fun x => Finset.sum_nonneg (fun _ _ => sq_nonneg _))
  · exact henergy
  · exact Filter.Eventually.of_forall (fun x => coordinateEnergy_le_operatorEnergy (fderiv Real f x))

/-- The frozen coordinate-to-operator package is locally closed. -/
theorem coordinateToOperatorEnergyPackage : CoordinateToOperatorEnergyPackage := by
  intro n f hf _ _ henergy
  exact mul_le_mul_of_nonneg_left (coordinateEnergy_integral_le f henergy) (by positivity)

#print axioms coordinateToOperatorEnergyPackage

end Stage1Instances.THM_M_1244
