import SLT.GaussianLSI.TensorizedGLSI
import ObligationTree

/-!
# THM-M-1244 proof execution

This module connects the complete vendored Gaussian logarithmic Sobolev proof
to the frozen statement and discharges the finite-dimensional energy mismatch.
-/

namespace Stage1Instances.THM_M_1244

open MeasureTheory ProbabilityTheory
open scoped BigOperators

/-- The statement's zero-safe entropy integrand agrees everywhere with the
upstream product used in its entropy definition. -/
theorem xlogx_eq_mul_log (s : Real) : xlogx s = s * Real.log s := by
  by_cases hs : s = 0
  · simp [xlogx, hs]
  · simp [xlogx, hs]

/-- The statement entropy is exactly the entropy used by the vendored proof. -/
theorem entropySquare_eq_upstream {n : Nat} (f : Euclidean n -> Real) :
    entropySquare f (standardGaussian n) =
      LogSobolev.entropy (GaussianMeasure.stdGaussianPi n) (fun x => f x ^ 2) := by
  simp only [entropySquare, LogSobolev.entropy, standardGaussian,
    GaussianMeasure.stdGaussianPi]
  apply congrArg (fun z => z -
    (∫ x, f x ^ 2 ∂Measure.pi fun _ : Fin n => gaussianReal 0 1) *
      Real.log (∫ x, f x ^ 2 ∂Measure.pi fun _ : Fin n => gaussianReal 0 1))
  apply integral_congr_ae
  exact Filter.Eventually.of_forall fun x => xlogx_eq_mul_log (f x ^ 2)

/-- The target's explicit square and operator-energy assumptions imply the
vendored coordinatewise Gaussian Sobolev membership predicate. -/
theorem memW12GaussianPi_of_assumptions {n : Nat} (f : Euclidean n -> Real)
    (hf : ContDiff Real 1 f)
    (hsq : Integrable (fun x => f x ^ 2) (standardGaussian n))
    (henergy : Integrable (fun x => ‖fderiv Real f x‖ ^ 2) (standardGaussian n)) :
    GaussianLSI.MemW12GaussianPi n f (GaussianMeasure.stdGaussianPi n) := by
  constructor
  · rw [MeasureTheory.memLp_two_iff_integrable_sq hf.continuous.aestronglyMeasurable]
    exact hsq
  · intro i
    rw [MeasureTheory.memLp_two_iff_integrable_sq]
    · apply Integrable.mono henergy
      · exact ((hf.continuous_fderiv one_ne_zero).clm_apply
          continuous_const).aestronglyMeasurable.pow 2
      · exact Filter.Eventually.of_forall fun x => by
          simp only [Real.norm_eq_abs, abs_pow, abs_norm]
          rw [sq_le_sq, abs_abs, abs_of_nonneg (norm_nonneg _)]
          simpa [GaussianLSI.partialDeriv] using
            (calc
              |(fderiv Real f x) (Pi.single i 1)|
                  <= ‖fderiv Real f x‖ * ‖Pi.single i 1‖ :=
                (fderiv Real f x).le_opNorm _
              _ = ‖fderiv Real f x‖ := by rw [Pi.norm_single]; simp)
    · exact ((hf.continuous_fderiv one_ne_zero).clm_apply
        continuous_const).aestronglyMeasurable

/-- The vendored theorem plus checked measure, entropy, and regularity
transports closes the frozen coordinate-gradient package. -/
theorem coordinateLogSobolevPackage : CoordinateLogSobolevPackage := by
  intro n f hf hsq hent henergy
  have hw12 := memW12GaussianPi_of_assumptions f hf hsq henergy
  have hdiff : Differentiable Real f := hf.differentiable_one
  have hgrad : forall i, Continuous (fun x => GaussianLSI.partialDeriv i f x) :=
    fun i => (hf.continuous_fderiv one_ne_zero).clm_apply continuous_const
  have hlog : Integrable (fun x => f x ^ 2 * Real.log (f x ^ 2))
      (GaussianMeasure.stdGaussianPi n) :=
    hent.congr (Filter.Eventually.of_forall fun x => xlogx_eq_mul_log (f x ^ 2))
  have h := GaussianLSI.gaussian_logSobolev_W12_pi hw12 hdiff hgrad hlog
  rw [entropySquare_eq_upstream f]
  simpa [coordinateEnergy, GaussianLSI.gradNormSq, GaussianLSI.partialDeriv] using h

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

/-- Exact kernel-checked root: the vendored coordinate theorem and local
energy comparison compose through the pre-frozen package interface. -/
theorem gaussianLogSobolev : GaussianLogSobolevTarget :=
  gaussianLogSobolevTarget_of_packages coordinateLogSobolevPackage
    coordinateToOperatorEnergyPackage

#print sorries GaussianLSI.gaussian_logSobolev_W12_pi
#print sorries coordinateLogSobolevPackage
#print sorries coordinateToOperatorEnergyPackage
#print sorries gaussianLogSobolev
#print axioms GaussianLSI.gaussian_logSobolev_W12_pi
#print axioms coordinateLogSobolevPackage
#print axioms coordinateToOperatorEnergyPackage
#print axioms gaussianLogSobolev

end Stage1Instances.THM_M_1244
