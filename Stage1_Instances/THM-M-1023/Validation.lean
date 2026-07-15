import Statement
import LeanLevy.Levy.LevyKhintchineUniqueness

/-!
# THM-M-1023 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen root from the vendored LeanLevy terminal declarations with separately named convention and
convolution transports. This is same-workspace differential evidence, not a distinct-runner
attestation.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1023.Validation

open ProbabilityTheory

private def unitBoundary : Set Real := {x | |x| = 1}

private theorem measurableSet_unitBoundary : MeasurableSet unitBoundary := by
  exact measurableSet_eq_fun continuous_abs.measurable measurable_const

private theorem unitBoundary_subset_large :
    unitBoundary ⊆ {x : Real | 1 <= |x|} := by
  intro x hx
  exact le_of_eq hx.symm

private theorem integrableOn_unitBoundary (hnu : IsLevyMeasure nu) :
    IntegrableOn (fun x : Real => x) unitBoundary nu := by
  apply Measure.integrableOn_of_bounded
      ((measure_mono unitBoundary_subset_large).trans_lt
        (hnu.measure_setOf_abs_ge_lt_top one_pos)).ne
      measurable_id'.aestronglyMeasurable (M := 1)
  filter_upwards [ae_restrict_mem measurableSet_unitBoundary] with (x : Real) hx
  rw [Real.norm_eq_abs, hx]

private def boundaryCorrection (nu : Measure Real) : Real :=
  ∫ x in unitBoundary, x ∂nu

private def externalize (d : LevyKhintchineData) : LevyKhintchineTriple where
  drift := d.drift - boundaryCorrection d.jumpMeasure
  gaussianVariance := d.gaussianVariance
  levyMeasure := d.jumpMeasure
  levyMeasure_isLevyMeasure := ⟨d.noAtomAtZero, d.integrableMinOneSq⟩

private def internalize (T : LevyKhintchineTriple) : LevyKhintchineData where
  drift := T.drift + boundaryCorrection T.levyMeasure
  gaussianVariance := T.gaussianVariance
  jumpMeasure := T.levyMeasure
  noAtomAtZero := T.levyMeasure_isLevyMeasure.zero_singleton
  integrableMinOneSq := T.levyMeasure_isLevyMeasure.lintegral_min_one_sq_lt_top

private theorem internalize_externalize (d : LevyKhintchineData) :
    internalize (externalize d) = d := by
  cases d
  simp [externalize, internalize]

private theorem convolutionPower_matches_iteratedConv (mu : Measure Real) (n : Nat) :
    convolutionPower mu n = mu.iteratedConv n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [convolutionPower, Measure.iteratedConv_succ, ih]

private theorem boundaryIntegral_complex (nu : Measure Real) :
    (∫ x in unitBoundary, (x : Complex) ∂nu) = (boundaryCorrection nu : Complex) := by
  exact integral_complex_ofReal

private theorem integrand_split (t x : Real) :
    (Complex.exp (Complex.I * (t * x)) - 1 -
      if |x| <= 1 then Complex.I * (t * x) else 0) =
      levyCompensatedIntegrand t x -
        unitBoundary.indicator (fun y : Real => (y : Complex) * t * Complex.I) x := by
  rcases lt_trichotomy |x| 1 with hx | hx | hx
  · simp [unitBoundary, levyCompensatedIntegrand, hx, hx.le, ne_of_lt hx]
    have : Complex.I * ((t : Complex) * (x : Complex)) =
        (x : Complex) * (t : Complex) * Complex.I := by ring
    rw [this]
  · simp [unitBoundary, levyCompensatedIntegrand, hx]
    have : Complex.I * ((t : Complex) * (x : Complex)) =
        (x : Complex) * (t : Complex) * Complex.I := by ring
    rw [this]
  · have hnotle : ¬ |x| <= 1 := not_le.mpr hx
    have hnotlt : ¬ |x| < 1 := not_lt.mpr hx.le
    have hne : |x| ≠ 1 := ne_of_gt hx
    simp [unitBoundary, levyCompensatedIntegrand, hnotle, hnotlt, hne]
    congr 1
    ring

private theorem integral_boundaryTerm (nu : Measure Real) (t : Real) :
    ∫ x, unitBoundary.indicator
        (fun y : Real => (y : Complex) * t * Complex.I) x ∂nu =
      (boundaryCorrection nu : Complex) * t * Complex.I := by
  rw [integral_indicator measurableSet_unitBoundary]
  have hfactor :
      (∫ x in unitBoundary, (x : Complex) * t * Complex.I ∂nu) =
        (∫ x in unitBoundary, (x : Complex) ∂nu) * t * Complex.I := by
    exact (integral_mul_const _ _).trans
      (congrArg (fun z : Complex => z * Complex.I) (integral_mul_const _ _))
  rw [hfactor, boundaryIntegral_complex]

private theorem internalized_exponent (T : LevyKhintchineTriple) (t : Real) :
    (internalize T).exponent t = T.exponent t := by
  rw [LevyKhintchineData.exponent, LevyKhintchineTriple.exponent_def]
  simp only [internalize]
  have hMain := integrable_levyCompensatedIntegrand T.levyMeasure_isLevyMeasure t
  have hBoundary := integrableOn_unitBoundary T.levyMeasure_isLevyMeasure
  rw [integral_congr_ae (Filter.Eventually.of_forall (integrand_split t))]
  have hBoundaryComplex :
      IntegrableOn (fun x : Real => (x : Complex)) unitBoundary T.levyMeasure :=
    hBoundary.ofReal
  have hBoundaryTerm : Integrable
      (unitBoundary.indicator
        (fun x : Real => (x : Complex) * t * Complex.I)) T.levyMeasure := by
    exact (integrable_indicator_iff measurableSet_unitBoundary).mpr
      ((hBoundaryComplex.mul_const t).mul_const Complex.I)
  rw [integral_sub hMain hBoundaryTerm, integral_boundaryTerm]
  push_cast
  ring

private theorem externalized_exponent (d : LevyKhintchineData) (t : Real) :
    (externalize d).exponent t = d.exponent t := by
  have h := internalized_exponent (externalize d) t
  rw [internalize_externalize] at h
  exact h.symm

/-- A separately reconstructed inhabitant of the exact canonical target. -/
theorem independentlyReconstructedRoot : InfinitelyDivisibleIffLevyKhintchine := by
  intro mu
  constructor
  · rintro ⟨hProbability, hRoots⟩
    letI : IsProbabilityMeasure mu := hProbability
    have hExternal : ProbabilityTheory.IsInfinitelyDivisible mu := by
      intro n hn
      obtain ⟨root, hRootProbability, hPower⟩ := hRoots n hn
      refine ⟨root, hRootProbability, ?_⟩
      rw [← hPower, convolutionPower_matches_iteratedConv]
    obtain ⟨T, hRepresents, hUnique⟩ := existsUnique_levyKhintchineTriple hExternal
    refine ⟨internalize T, ?_, ?_⟩
    · intro t
      rw [internalized_exponent]
      exact hRepresents t
    · intro d hd
      have hExternalRepresents :
          ∀ t, charFun mu t = Complex.exp ((externalize d).exponent t) := by
        intro t
        rw [externalized_exponent]
        exact hd t
      have hSame := hUnique (externalize d) hExternalRepresents
      rw [← hSame, internalize_externalize]
  · rintro ⟨d, hd, _⟩
    have hProbability : IsProbabilityMeasure mu := by
      apply isProbabilityMeasure_iff_real.mpr
      have hAtZero := hd 0
      rw [charFun_zero] at hAtZero
      simpa [LevyKhintchineData.exponent] using hAtZero
    letI : IsProbabilityMeasure mu := hProbability
    have hExternalRepresents : ∃ T : LevyKhintchineTriple,
        ∀ t, charFun mu t = Complex.exp (T.exponent t) := by
      refine ⟨externalize d, ?_⟩
      intro t
      rw [externalized_exponent]
      exact hd t
    have hExternal :=
      isInfinitelyDivisible_iff_exists_levyKhintchineTriple.mpr hExternalRepresents
    refine ⟨hProbability, ?_⟩
    intro n hn
    obtain ⟨root, hRootProbability, hPower⟩ := hExternal n hn
    refine ⟨root, hRootProbability, ?_⟩
    rw [convolutionPower_matches_iteratedConv, ← hPower]

#check (independentlyReconstructedRoot : InfinitelyDivisibleIffLevyKhintchine)
#print sorries independentlyReconstructedRoot
#print axioms independentlyReconstructedRoot

end Stage1Instances.THM_M_1023.Validation
