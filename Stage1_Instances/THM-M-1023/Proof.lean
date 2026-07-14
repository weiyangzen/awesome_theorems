import Statement
import LeanLevy.Levy.LevyKhintchineUniqueness

/-!
# THM-M-1023 exact Levy-Khinchin proof

This module transports the vendored real-line LeanLevy theorem from open unit truncation to the
frozen closed unit truncation, then closes both directions and representation-data uniqueness.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1023

open ProbabilityTheory

private def boundary : Set Real := {x | |x| = 1}

private theorem measurableSet_boundary : MeasurableSet boundary := by
  exact measurableSet_eq_fun continuous_abs.measurable measurable_const

private theorem boundary_subset_large : boundary ⊆ {x : Real | 1 <= |x|} := by
  intro x hx
  exact le_of_eq hx.symm

private theorem integrableOn_boundary (hnu : ProbabilityTheory.IsLevyMeasure nu) :
    IntegrableOn (fun x : Real => x) boundary nu := by
  apply Measure.integrableOn_of_bounded
      ((measure_mono boundary_subset_large).trans_lt
        (hnu.measure_setOf_abs_ge_lt_top one_pos)).ne
      measurable_id'.aestronglyMeasurable (M := 1)
  filter_upwards [ae_restrict_mem measurableSet_boundary] with (x : Real) hx
  rw [Real.norm_eq_abs, hx]

private def boundaryMoment (nu : Measure Real) : Real :=
  ∫ x in boundary, x ∂nu

private def toExternal (d : LevyKhintchineData) : ProbabilityTheory.LevyKhintchineTriple where
  drift := d.drift - boundaryMoment d.jumpMeasure
  gaussianVariance := d.gaussianVariance
  levyMeasure := d.jumpMeasure
  levyMeasure_isLevyMeasure := ⟨d.noAtomAtZero, d.integrableMinOneSq⟩

private def fromExternal (T : ProbabilityTheory.LevyKhintchineTriple) : LevyKhintchineData where
  drift := T.drift + boundaryMoment T.levyMeasure
  gaussianVariance := T.gaussianVariance
  jumpMeasure := T.levyMeasure
  noAtomAtZero := T.levyMeasure_isLevyMeasure.zero_singleton
  integrableMinOneSq := T.levyMeasure_isLevyMeasure.lintegral_min_one_sq_lt_top

private theorem convolutionPower_eq_iteratedConv (mu : Measure Real) (n : Nat) :
    convolutionPower mu n = mu.iteratedConv n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [convolutionPower, Measure.iteratedConv_succ, ih]

private theorem fromExternal_toExternal (d : LevyKhintchineData) :
    fromExternal (toExternal d) = d := by
  cases d
  simp [toExternal, fromExternal]

private theorem boundary_integral_complex (nu : Measure Real) :
    (∫ x in boundary, (x : Complex) ∂nu) = (boundaryMoment nu : Complex) := by
  exact integral_complex_ofReal

private theorem local_integrand_eq_external_add_boundary (t x : Real) :
    (Complex.exp (Complex.I * (t * x)) - 1 -
      if |x| <= 1 then Complex.I * (t * x) else 0) =
      ProbabilityTheory.levyCompensatedIntegrand t x -
        boundary.indicator (fun x : Real => (x : Complex) * t * Complex.I) x := by
  rcases lt_trichotomy |x| 1 with hx | hx | hx
  · simp [boundary, ProbabilityTheory.levyCompensatedIntegrand, hx, hx.le, ne_of_lt hx]
    have harg : Complex.I * ((t : Complex) * (x : Complex)) =
        (x : Complex) * (t : Complex) * Complex.I := by ring
    rw [harg]
  · simp [boundary, ProbabilityTheory.levyCompensatedIntegrand, hx]
    have harg : Complex.I * ((t : Complex) * (x : Complex)) =
        (x : Complex) * (t : Complex) * Complex.I := by ring
    rw [harg]
  · have hnotle : ¬ |x| <= 1 := not_le.mpr hx
    have hnotlt : ¬ |x| < 1 := not_lt.mpr hx.le
    have hne : |x| ≠ 1 := ne_of_gt hx
    simp [boundary, ProbabilityTheory.levyCompensatedIntegrand, hnotle, hnotlt, hne]
    congr 1
    ring

private theorem integral_boundary_linear (nu : Measure Real) (t : Real) :
    ∫ x, boundary.indicator (fun x : Real => (x : Complex) * t * Complex.I) x ∂nu =
      (boundaryMoment nu : Complex) * t * Complex.I := by
  rw [integral_indicator measurableSet_boundary]
  have h1 : (∫ x in boundary, (x : Complex) * t * Complex.I ∂nu) =
      (∫ x in boundary, (x : Complex) ∂nu) * t * Complex.I := by
    exact (integral_mul_const _ _).trans
      (congrArg (fun z : Complex => z * Complex.I) (integral_mul_const _ _))
  rw [h1, boundary_integral_complex]

private theorem exponent_fromExternal (T : ProbabilityTheory.LevyKhintchineTriple) (t : Real) :
    (fromExternal T).exponent t = T.exponent t := by
  rw [LevyKhintchineData.exponent, ProbabilityTheory.LevyKhintchineTriple.exponent_def]
  simp only [fromExternal]
  have hInt := integrable_levyCompensatedIntegrand T.levyMeasure_isLevyMeasure t
  have hBoundary := integrableOn_boundary T.levyMeasure_isLevyMeasure
  rw [integral_congr_ae (Filter.Eventually.of_forall
    (local_integrand_eq_external_add_boundary t))]
  have hBoundaryComplex : IntegrableOn (fun x : Real => (x : Complex)) boundary T.levyMeasure := by
    exact hBoundary.ofReal
  have hBoundaryTerm : Integrable
      (boundary.indicator (fun x : Real => (x : Complex) * t * Complex.I)) T.levyMeasure := by
    exact (integrable_indicator_iff measurableSet_boundary).mpr
      ((hBoundaryComplex.mul_const t).mul_const Complex.I)
  rw [integral_sub hInt hBoundaryTerm]
  rw [integral_boundary_linear]
  push_cast
  ring

private theorem exponent_toExternal (d : LevyKhintchineData) (t : Real) :
    (toExternal d).exponent t = d.exponent t := by
  have h := exponent_fromExternal (toExternal d) t
  rw [fromExternal_toExternal] at h
  exact h.symm

/-- The exact frozen real-line Levy-Khinchin characterization. -/
theorem infinitelyDivisibleIffLevyKhintchine :
    InfinitelyDivisibleIffLevyKhintchine := by
  intro mu
  constructor
  · rintro ⟨hprob, hdiv⟩
    letI : IsProbabilityMeasure mu := hprob
    have hext : ProbabilityTheory.IsInfinitelyDivisible mu := by
      intro n hn
      obtain ⟨root, hroot, hpow⟩ := hdiv n hn
      refine ⟨root, hroot, ?_⟩
      rw [← hpow, convolutionPower_eq_iteratedConv]
    obtain ⟨T, hT, huniq⟩ := ProbabilityTheory.existsUnique_levyKhintchineTriple hext
    refine ⟨fromExternal T, ?_, ?_⟩
    · intro t
      rw [exponent_fromExternal]
      exact hT t
    · intro e he
      have hextrep : ∀ t, charFun mu t = Complex.exp ((toExternal e).exponent t) := by
        intro t
        rw [exponent_toExternal]
        exact he t
      have heq := huniq (toExternal e) hextrep
      rw [← heq, fromExternal_toExternal]
  · rintro ⟨d, hd, _⟩
    have hprob : IsProbabilityMeasure mu := by
      apply isProbabilityMeasure_iff_real.mpr
      have hzero := hd 0
      rw [charFun_zero] at hzero
      simpa [LevyKhintchineData.exponent] using hzero
    letI : IsProbabilityMeasure mu := hprob
    have hextrep : ∃ T : ProbabilityTheory.LevyKhintchineTriple,
        ∀ t, charFun mu t = Complex.exp (T.exponent t) := by
      refine ⟨toExternal d, ?_⟩
      intro t
      rw [exponent_toExternal]
      exact hd t
    have hext := ProbabilityTheory.isInfinitelyDivisible_iff_exists_levyKhintchineTriple.mpr hextrep
    refine ⟨hprob, ?_⟩
    intro n hn
    obtain ⟨root, hroot, hpow⟩ := hext n hn
    refine ⟨root, hroot, ?_⟩
    rw [convolutionPower_eq_iteratedConv, ← hpow]

#print sorries infinitelyDivisibleIffLevyKhintchine
#print sorries ProbabilityTheory.levyKhintchine_representation
#print sorries ProbabilityTheory.levyKhintchine_converse
#print sorries ProbabilityTheory.existsUnique_levyKhintchineTriple
#print axioms infinitelyDivisibleIffLevyKhintchine
#print axioms ProbabilityTheory.levyKhintchine_representation
#print axioms ProbabilityTheory.levyKhintchine_converse
#print axioms ProbabilityTheory.existsUnique_levyKhintchineTriple

end Stage1Instances.THM_M_1023
