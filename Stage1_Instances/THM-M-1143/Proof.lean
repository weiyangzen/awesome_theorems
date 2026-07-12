import ObligationTree
import Mathlib.Analysis.Calculus.MeanValue

/-!
# THM-M-1143 proof-phase bodies

This module implements the bounded-range normalization and the
zero-derivative-to-constant branch of the frozen proof tree. The arbitrary-dimensional interior
gradient estimate, and hence the vanishing-derivative package and exact root, remain open.
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

#print axioms exists_uniform_abs_bound
#print axioms zeroDerivativeConstantPackage
#print axioms root_of_vanishingDerivativePackage

end Stage1Instances.THM_M_1143
