import ObligationTree
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-1143 proof-phase bodies

This module implements the bounded-range normalization, the radius-to-infinity limit, and the
zero-derivative-to-constant branch of the frozen proof tree. The arbitrary-dimensional interior
gradient estimate, and hence the unconditional vanishing-derivative package and exact root, remain
open.
-/

open Bornology Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1143

/-- A bounded real range supplies a single absolute-value bound at every point. -/
theorem exists_uniform_abs_bound {n : Nat} {f : Space n -> Real}
    (hb : IsBounded (range f)) :
    exists C : Real, forall x, |f x| <= C := by
  rw [isBounded_iff_forall_norm_le] at hb
  obtain ⟨C, hC⟩ := hb
  exact ⟨C, fun x => by simpa only [Real.norm_eq_abs] using hC (f x) ⟨x, rfl⟩⟩

/-- The uniform absolute-value bound can be chosen nonnegative. -/
theorem exists_nonnegative_uniform_abs_bound {n : Nat} {f : Space n -> Real}
    (hb : IsBounded (range f)) :
    exists C : Real, 0 <= C ∧ forall x, |f x| <= C := by
  obtain ⟨C, hC⟩ := exists_uniform_abs_bound hb
  exact ⟨max C 0, le_max_right C 0, fun x => (hC x).trans (le_max_left C 0)⟩

/--
The one still-open analytic interface: a uniform bound and global harmonicity give an interior
gradient estimate at every center and every positive radius.
-/
def InteriorGradientEstimatePackage : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n -> HarmonicOnNhd f univ ->
    forall C : Real, 0 <= C -> (forall x, |f x| <= C) ->
    exists A : Real, 0 <= A ∧
      forall (x : Space n) (R : Real), 0 < R -> ‖fderiv Real f x‖ <= A / R

/-- A `C / R` bound at every positive radius forces a continuous linear map to vanish. -/
theorem continuousLinearMap_eq_zero_of_norm_le_div
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace Real E]
    [NormedAddCommGroup F] [NormedSpace Real F]
    (L : E →L[Real] F) (A : Real) (hA : 0 <= A)
    (hbound : forall R : Real, 0 < R -> ‖L‖ <= A / R) :
    L = 0 := by
  by_contra hL
  have hLnorm : 0 < ‖L‖ := norm_pos_iff.mpr hL
  let R : Real := A / ‖L‖ + 1
  have hR : 0 < R := by
    dsimp [R]
    positivity
  have hle := hbound R hR
  have hlt : A / R < ‖L‖ := by
    rw [div_lt_iff₀ hR]
    dsimp [R]
    rw [mul_add, mul_div_cancel₀ A hLnorm.ne']
    linarith
  exact (not_lt_of_ge hle) hlt

/-- The frozen radius-limit and derivative-construction steps, conditional only on the estimate. -/
theorem vanishingDerivativePackage_of_interiorGradientEstimate
    (hgradient : InteriorGradientEstimatePackage) : VanishingDerivativePackage := by
  intro n f hn hh hb x
  obtain ⟨C, hC, hfC⟩ := exists_nonnegative_uniform_abs_bound hb
  obtain ⟨A, hA, hestimate⟩ := hgradient n f hn hh C hC hfC
  have hzero : fderiv Real f x = 0 :=
    continuousLinearMap_eq_zero_of_norm_le_div (fderiv Real f x) A hA
      (fun R hR => hestimate x R hR)
  have hdiff : DifferentiableAt Real f x :=
    (hh x (mem_univ x)).1.differentiableAt (by norm_num)
  simpa only [hzero] using hdiff.hasFDerivAt

/-- On a real normed vector space, an everywhere-zero Frechet derivative forces constancy. -/
theorem zeroDerivativeConstantPackage : ZeroDerivativeConstantPackage := by
  intro n f _ hf x y
  apply is_const_of_fderiv_eq_zero (fun z => (hf z).differentiableAt) _ x y
  intro z
  exact (hf z).fderiv

/-- Recheck exact root composition while leaving the analytic package explicit. -/
theorem root_of_vanishingDerivativePackage
    (hvanish : VanishingDerivativePackage) : BoundedHarmonicIsConstant :=
  root_of_vanishingDerivative_packages hvanish zeroDerivativeConstantPackage

/-- Exact root composition, conditional only on the frozen interior gradient estimate. -/
theorem root_of_interiorGradientEstimate
    (hgradient : InteriorGradientEstimatePackage) : BoundedHarmonicIsConstant :=
  root_of_vanishingDerivativePackage
    (vanishingDerivativePackage_of_interiorGradientEstimate hgradient)

assert_no_sorry exists_uniform_abs_bound
assert_no_sorry exists_nonnegative_uniform_abs_bound
assert_no_sorry continuousLinearMap_eq_zero_of_norm_le_div
assert_no_sorry vanishingDerivativePackage_of_interiorGradientEstimate
assert_no_sorry zeroDerivativeConstantPackage
assert_no_sorry root_of_vanishingDerivativePackage
assert_no_sorry root_of_interiorGradientEstimate

#print axioms exists_uniform_abs_bound
#print axioms exists_nonnegative_uniform_abs_bound
#print axioms continuousLinearMap_eq_zero_of_norm_le_div
#print axioms vanishingDerivativePackage_of_interiorGradientEstimate
#print axioms zeroDerivativeConstantPackage
#print axioms root_of_vanishingDerivativePackage
#print axioms root_of_interiorGradientEstimate

end Stage1Instances.THM_M_1143
