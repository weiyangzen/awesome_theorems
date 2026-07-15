import ObligationTree
import Vendor.GaussianField.HermiteFunctions
import Mathlib.Analysis.InnerProductSpace.l2Space
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0353 proof execution

This module adapts the proved real Hermite-function development vendored from
`mrdouglasny/gaussian-field` to the exact complex-valued Lebesgue-space target.
-/

namespace Stage1Instances.THM_M_0353

open scoped ENNReal ComplexConjugate
open MeasureTheory

/-- The normalization used in the real Hermite development equals the target normalization. -/
theorem realHermiteNormalization_eq (n : Nat) :
    Real.sqrt (((n.factorial : Real) * Real.sqrt Real.pi)⁻¹) =
      Real.pi ^ (-(1 : Real) / 4) / Real.sqrt (n.factorial : Real) := by
  have hfact : (0 : Real) < (n.factorial : Real) := by positivity
  have hpi : (0 : Real) < Real.pi := Real.pi_pos
  rw [Real.sqrt_inv, Real.sqrt_mul hfact.le]
  have hsqrtpi : Real.sqrt (Real.sqrt Real.pi) = Real.pi ^ (1 / 4 : Real) := by
    rw [Real.sqrt_eq_rpow, Real.sqrt_eq_rpow, ← Real.rpow_mul hpi.le]
    congr 1
    ring
  rw [hsqrtpi, mul_inv, div_eq_mul_inv, ← Real.rpow_neg hpi.le]
  rw [show (-(1 : Real) / 4) = -(1 / 4) by ring]
  ring

/-- The target's complex function is the coercion of the proved real function. -/
theorem target_hermiteFunction_eq_ofReal (n : Nat) (x : Real) :
    hermiteFunction n x = (_root_.hermiteFunction n x : Complex) := by
  rw [hermiteFunction, _root_.hermiteFunction, _root_.hermiteFunctionNormConst,
    realHermiteNormalization_eq]
  simp only [Polynomial.aeval_def, Polynomial.eval₂_eq_eval_map]
  rw [show algebraMap Int Real = Int.castRingHom Real from rfl]
  push_cast
  congr 2 <;> ring

/-- Every target function is in complex `L²`, transported from the proved real result. -/
theorem target_hermiteFunction_memLp (n : Nat) :
    MemLp (hermiteFunction n) (2 : ENNReal) leb := by
  rw [show leb = volume from rfl]
  exact (_root_.hermiteFunction_memLp n).ofReal.ae_eq
    (Filter.Eventually.of_forall fun x => (target_hermiteFunction_eq_ofReal n x).symm)

/-- The target function represented in complex `L²`. -/
noncomputable def targetHermiteLp (n : Nat) : Lp Complex 2 leb :=
  (target_hermiteFunction_memLp n).toLp (hermiteFunction n)

theorem targetHermiteLp_coe (n : Nat) :
    (targetHermiteLp n : Real → Complex) =ᵐ[leb] hermiteFunction n :=
  (target_hermiteFunction_memLp n).coeFn_toLp

theorem targetHermiteLp_coe_real (n : Nat) :
    (targetHermiteLp n : Real → Complex) =ᵐ[leb]
      fun x ↦ (_root_.hermiteFunction n x : Complex) :=
  (targetHermiteLp_coe n).trans
    (Filter.Eventually.of_forall (target_hermiteFunction_eq_ofReal n))

/-- The complex `L²` representatives inherit the real orthonormality theorem. -/
theorem targetHermiteLp_inner (n m : Nat) :
    @inner Complex _ _ (targetHermiteLp n) (targetHermiteLp m) =
      if n = m then 1 else 0 := by
  rw [L2.inner_def]
  calc
    (∫ x, @inner Complex _ _ (targetHermiteLp n x) (targetHermiteLp m x) ∂leb) =
        ∫ x, ((_root_.hermiteFunction n x * _root_.hermiteFunction m x : Real) : Complex)
          ∂leb := by
      apply integral_congr_ae
      filter_upwards [targetHermiteLp_coe_real n,
        targetHermiteLp_coe_real m] with x hnx hmx
      rw [hnx, hmx]
      simp [RCLike.inner_apply]
      ring
    _ = Complex.ofReal
        (∫ x, _root_.hermiteFunction n x * _root_.hermiteFunction m x ∂volume) := by
      simpa [leb] using
        (integral_ofReal (𝕜 := Complex)
          (μ := (volume : Measure Real))
          (f := fun x : Real ↦
            _root_.hermiteFunction n x * _root_.hermiteFunction m x))
    _ = if n = m then 1 else 0 := by
      rw [_root_.hermiteFunction_orthonormal n m]
      split_ifs <;> simp

theorem targetHermiteLp_orthonormal : Orthonormal Complex targetHermiteLp := by
  rw [orthonormal_iff_ite]
  exact targetHermiteLp_inner

/-- Real and imaginary parts reduce complex completeness to the proved real theorem. -/
theorem targetHermiteLp_span_orthogonal_eq_bot :
    (Submodule.span Complex (Set.range targetHermiteLp))ᗮ = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro f hf
  have hinner (n : Nat) :
      @inner Complex _ _ (targetHermiteLp n) f = 0 :=
    Submodule.inner_right_of_mem_orthogonal
      (Submodule.subset_span (Set.mem_range_self n)) hf
  have hint (n : Nat) :
      Integrable (fun x : Real ↦
        @inner Complex _ _ (targetHermiteLp n x) (f x)) leb :=
    L2.integrable_inner (targetHermiteLp n) f
  have hre_orth (n : Nat) :
      ∫ x, RCLike.re (f x) * _root_.hermiteFunction n x ∂leb = 0 := by
    calc
      (∫ x, RCLike.re (f x) * _root_.hermiteFunction n x ∂leb) =
          ∫ x, RCLike.re (@inner Complex _ _
            (targetHermiteLp n x) (f x)) ∂leb := by
        apply integral_congr_ae
        filter_upwards [targetHermiteLp_coe_real n] with x hnx
        rw [hnx]
        simp [RCLike.inner_apply]
      _ = RCLike.re (∫ x, @inner Complex _ _
            (targetHermiteLp n x) (f x) ∂leb) := integral_re (hint n)
      _ = 0 := by
        change RCLike.re (@inner Complex _ _ (targetHermiteLp n) f) = 0
        simp [hinner n]
  have him_orth (n : Nat) :
      ∫ x, RCLike.im (f x) * _root_.hermiteFunction n x ∂leb = 0 := by
    calc
      (∫ x, RCLike.im (f x) * _root_.hermiteFunction n x ∂leb) =
          ∫ x, RCLike.im (@inner Complex _ _
            (targetHermiteLp n x) (f x)) ∂leb := by
        apply integral_congr_ae
        filter_upwards [targetHermiteLp_coe_real n] with x hnx
        rw [hnx]
        simp [RCLike.inner_apply]
      _ = RCLike.im (∫ x, @inner Complex _ _
            (targetHermiteLp n x) (f x) ∂leb) := integral_im (hint n)
      _ = 0 := by
        change RCLike.im (@inner Complex _ _ (targetHermiteLp n) f) = 0
        simp [hinner n]
  have hre : (fun x : Real ↦ RCLike.re (f x)) =ᵐ[volume] 0 :=
    _root_.hermiteFunction_complete _ (by
      simpa [leb] using (Lp.memLp f).re) (by
      intro n
      simpa [leb] using hre_orth n)
  have him : (fun x : Real ↦ RCLike.im (f x)) =ᵐ[volume] 0 :=
    _root_.hermiteFunction_complete _ (by
      simpa [leb] using (Lp.memLp f).im) (by
      intro n
      simpa [leb] using him_orth n)
  rw [Lp.eq_zero_iff_ae_eq_zero]
  filter_upwards [hre, him] with x hr hi
  apply RCLike.ext
  · simpa using hr
  · simpa using hi

/-- The exact complex Hilbert basis requested by the target. -/
noncomputable def targetHermiteBasis :
    HilbertBasis Nat Complex (Lp Complex 2 leb) :=
  HilbertBasis.mkOfOrthogonalEqBot targetHermiteLp_orthonormal
    targetHermiteLp_span_orthogonal_eq_bot

theorem targetHermiteBasis_coe (n : Nat) :
    (targetHermiteBasis n : Real → Complex) =ᵐ[leb] hermiteFunction n := by
  rw [targetHermiteBasis, HilbertBasis.coe_mkOfOrthogonalEqBot]
  exact targetHermiteLp_coe n

/-- The universally quantified integrability package from the frozen proof graph. -/
theorem hermiteMemLpPackage_proof : HermiteMemLpPackage :=
  target_hermiteFunction_memLp

/-- The exact basis package from the frozen proof graph. -/
theorem hermiteBasisPackage_proof : HermiteBasisPackage :=
  ⟨targetHermiteBasis, targetHermiteBasis_coe⟩

/-- Exact closure of the canonical target through the frozen composer. -/
theorem hermiteCompletenessTarget_proof : HermiteCompletenessTarget := by
  exact root_of_hermite_packages
    hermiteMemLpPackage_proof hermiteBasisPackage_proof

assert_no_sorry _root_.hermiteFunction_memLp
assert_no_sorry _root_.hermiteFunction_orthonormal
assert_no_sorry _root_.hermiteFunction_complete
assert_no_sorry hermiteMemLpPackage_proof
assert_no_sorry hermiteBasisPackage_proof
assert_no_sorry hermiteCompletenessTarget_proof

#print sorries _root_.hermiteFunction_memLp
#print sorries _root_.hermiteFunction_orthonormal
#print sorries _root_.hermiteFunction_complete
#print sorries hermiteMemLpPackage_proof
#print sorries hermiteBasisPackage_proof
#print sorries hermiteCompletenessTarget_proof

#print axioms _root_.hermiteFunction_memLp
#print axioms _root_.hermiteFunction_orthonormal
#print axioms _root_.hermiteFunction_complete
#print axioms hermiteMemLpPackage_proof
#print axioms hermiteBasisPackage_proof
#print axioms hermiteCompletenessTarget_proof

end Stage1Instances.THM_M_0353
