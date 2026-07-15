import Statement

/-!
# THM-M-0349 proof execution

This module contains the repo-local one-mode construction and a concrete `L2`
conjugate-function estimate.  The frozen registry gives the `L2` node only a
planned target rather than an exact Lean type, so the latter is a candidate
body pending master reconciliation.  This module deliberately does not declare
the all-`p` root theorem.
-/

namespace Stage1Instances.THM_M_0349

open MeasureTheory

/-- Apply the conjugate-function multiplier to one Fourier mode. -/
noncomputable def conjugateMode (n : Int) (a : Complex) : Circle -> Complex :=
  fun x => (conjugateMultiplier n * a) * fourier n x

/-- The one-mode construction has exactly the intended Fourier coefficients. -/
theorem fourierCoeff_conjugateMode (n : Int) (a : Complex) :
    forall k : Int, fourierCoeff (conjugateMode n a) k =
      (conjugateMultiplier n * a) * (Pi.single n 1 : Int -> Complex) k := by
  intro k
  unfold conjugateMode
  rw [fourierCoeff.const_mul]
  rw [congrFun (fourierCoeff_fourier (T := (1 : Real)) n) k]

/-- The multiplier vanishes on the constant mode. -/
theorem conjugateMultiplier_zero : conjugateMultiplier 0 = 0 := by
  rfl

/-- The conjugate multiplier has modulus at most one. -/
theorem norm_conjugateMultiplier_le_one (n : Int) :
    ‖conjugateMultiplier n‖ ≤ 1 := by
  unfold conjugateMultiplier
  split_ifs <;> simp

/-- Multiplication by the conjugate multiplier preserves square summability. -/
theorem conjugateMultiplier_memℓp_two (a : lp (fun _ : Int => Complex) 2) :
    Memℓp (fun n => conjugateMultiplier n * a n) 2 := by
  apply memℓp_gen
  have ha : Summable (fun n : Int => ‖a n‖ ^ (2 : ENNReal).toReal) :=
    (lp.memℓp a).summable (by norm_num)
  refine Summable.of_nonneg_of_le (fun _ => by positivity) (fun n => ?_) ha
  rw [norm_mul]
  exact Real.rpow_le_rpow
    (mul_nonneg (norm_nonneg (conjugateMultiplier n)) (norm_nonneg (a n)))
    (mul_le_of_le_one_left (norm_nonneg (a n))
      (norm_conjugateMultiplier_le_one n)) (by positivity)

/-- The diagonal conjugate multiplier on Fourier coefficient space. -/
noncomputable def conjugateSequence (a : lp (fun _ : Int => Complex) 2) :
    lp (fun _ : Int => Complex) 2 :=
  ⟨fun n => conjugateMultiplier n * a n, conjugateMultiplier_memℓp_two a⟩

@[simp]
theorem conjugateSequence_apply (a : lp (fun _ : Int => Complex) 2) (n : Int) :
    conjugateSequence a n = conjugateMultiplier n * a n :=
  rfl

/-- The diagonal conjugate multiplier is a contraction on square-summable sequences. -/
theorem norm_conjugateSequence_le (a : lp (fun _ : Int => Complex) 2) :
    ‖conjugateSequence a‖ ≤ ‖a‖ := by
  apply lp.norm_le_of_tsum_le (by norm_num) (norm_nonneg a)
  have ha : Summable (fun n : Int => ‖a n‖ ^ (2 : ENNReal).toReal) :=
    (lp.memℓp a).summable (by norm_num)
  have hle : forall n : Int,
      ‖conjugateSequence a n‖ ^ (2 : ENNReal).toReal ≤
        ‖a n‖ ^ (2 : ENNReal).toReal := by
    intro n
    rw [conjugateSequence_apply, norm_mul]
    exact Real.rpow_le_rpow
      (mul_nonneg (norm_nonneg (conjugateMultiplier n)) (norm_nonneg (a n)))
      (mul_le_of_le_one_left (norm_nonneg (a n))
        (norm_conjugateMultiplier_le_one n)) (by positivity)
  rw [lp.norm_rpow_eq_tsum (by norm_num : 0 < (2 : ENNReal).toReal)]
  exact (conjugateMultiplier_memℓp_two a).summable (by norm_num) |>.tsum_le_tsum hle ha

/-- The periodic conjugate function on `L²`, transported through the Fourier Hilbert basis. -/
noncomputable def conjugateL2
    (f : Lp Complex 2 (AddCircle.haarAddCircle (T := (1 : Real)))) :
    Lp Complex 2 (AddCircle.haarAddCircle (T := (1 : Real))) :=
  (@fourierBasis (1 : Real) ⟨by positivity⟩).repr.symm
    (conjugateSequence ((@fourierBasis (1 : Real) ⟨by positivity⟩).repr f))

/-- The `L²` conjugate function has exactly the prescribed Fourier coefficients. -/
theorem fourierCoeff_conjugateL2
    (f : Lp Complex 2 (AddCircle.haarAddCircle (T := (1 : Real)))) (n : Int) :
    fourierCoeff (conjugateL2 f) n =
      conjugateMultiplier n * fourierCoeff f n := by
  rw [← fourierBasis_repr, conjugateL2,
    LinearIsometryEquiv.apply_symm_apply, conjugateSequence_apply,
    fourierBasis_repr]

/-- The periodic conjugate-function multiplier is an `L²` contraction. -/
theorem norm_conjugateL2_le
    (f : Lp Complex 2 (AddCircle.haarAddCircle (T := (1 : Real)))) :
    ‖conjugateL2 f‖ ≤ ‖f‖ := by
  rw [conjugateL2, LinearIsometryEquiv.norm_map]
  simpa only [LinearIsometryEquiv.norm_map] using
    norm_conjugateSequence_le ((@fourierBasis (1 : Real) ⟨by positivity⟩).repr f)

/-- Candidate for planned obligation `M0349-L-L2`: existence and the sharp
constant-one bound at exponent two. -/
theorem conjugate_l2_bound
    (f : Lp Complex 2 (AddCircle.haarAddCircle (T := (1 : Real)))) :
    exists g : Lp Complex 2 (AddCircle.haarAddCircle (T := (1 : Real))),
      AreConjugate (fun x => f x) (fun x => g x) /\ ‖g‖ ≤ ‖f‖ := by
  exact ⟨conjugateL2 f, fourierCoeff_conjugateL2 f, norm_conjugateL2_le f⟩

#print axioms fourierCoeff_conjugateMode
#print axioms conjugateMultiplier_zero
#print axioms conjugate_l2_bound

end Stage1Instances.THM_M_0349
