import Statement
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FieldSimp

/-!
# THM-M-0403 proof execution

This module implements the frozen one- and two-term branches and an exact
conditional composition into the canonical root. The ESS finite-rank
multiplicative-group theorem remains an explicit, unasserted premise.
-/

open scoped BigOperators

namespace Stage1.THM_M_0403.Proof

universe u

open Stage1.THM_M_0403

/-- The zero set of a one-term exponential polynomial is empty. -/
theorem oneTerm_zeroSet_empty {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 1) : zeroSet D = ∅ := by
  ext n
  simp [zeroSet, ExponentialPolynomialData.eval,
    D.coeff_ne_zero 0, D.root_ne_zero 0]

/-- Frozen base case of `M0403-B-TERM-INDUCTION`. -/
theorem oneTerm_zeroSet_finite {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 1) : (zeroSet D).Finite := by
  rw [oneTerm_zeroSet_empty D]
  exact Set.finite_empty

/-- The nonzero quotient of the two roots, viewed as a unit. -/
abbrev rootRatioUnit {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) : Kˣ :=
  Units.mk0 (D.root 0 / D.root 1)
    (div_ne_zero (D.root_ne_zero 0) (D.root_ne_zero 1))

/-- The concrete two-term zero equation after division by the second root. -/
theorem twoTerm_eval_zero_iff {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) (n : Nat) :
    D.eval n = 0 ↔
      D.coeff 0 * ((rootRatioUnit D : Kˣ) : K) ^ n + D.coeff 1 = 0 := by
  have hroot : D.root 1 ^ n ≠ 0 := pow_ne_zero n (D.root_ne_zero 1)
  have hratio :
      ((rootRatioUnit D : Kˣ) : K) ^ n = D.root 0 ^ n / D.root 1 ^ n := by
    simp [rootRatioUnit, div_pow]
  calc
    D.eval n = 0 ↔ D.eval n / D.root 1 ^ n = 0 := by
      constructor
      · intro h
        simp [h]
      · intro h
        exact (div_eq_zero_iff.mp h).resolve_right hroot
    _ ↔ D.coeff 0 * ((rootRatioUnit D : Kˣ) : K) ^ n + D.coeff 1 = 0 := by
      rw [hratio]
      simp [ExponentialPolynomialData.eval, Fin.sum_univ_two]
      field_simp [hroot]
      simp [D.root_ne_zero 1]

/-- Frozen low-dimensional case of `M0403-L-INDEX-INJECTIVE`: two distinct
zero indices would make the root quotient torsion. -/
theorem twoTerm_zeroSet_subsingleton {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) : (zeroSet D).Subsingleton := by
  intro n hn m hm
  have hn' := (twoTerm_eval_zero_iff D n).mp hn
  have hm' := (twoTerm_eval_zero_iff D m).mp hm
  have hp : ((rootRatioUnit D : Kˣ) : K) ^ n =
      ((rootRatioUnit D : Kˣ) : K) ^ m := by
    apply mul_left_cancel₀ (D.coeff_ne_zero 0)
    exact (eq_neg_of_add_eq_zero_left hn').trans
      (eq_neg_of_add_eq_zero_left hm').symm
  have hpu : rootRatioUnit D ^ n = rootRatioUnit D ^ m := by
    ext
    simpa using hp
  apply (injective_pow_iff_not_isOfFinOrder.mpr ?_) hpu
  intro hfin
  exact D.ratio_nontorsion 0 1 (by decide) ((Units.isOfFinOrder_val).mpr hfin)

/-- The complete two-term zero set is finite. -/
theorem twoTerm_zeroSet_finite {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) : (zeroSet D).Finite :=
  (twoTerm_zeroSet_subsingleton D).finite

/-- Exact binder-level composition for `M0403-T-FINITE-ZEROSET`. The deep
terminal theorem is deliberately an explicit premise, not a local axiom. -/
theorem statement_of_finiteZeroSet
    (finiteZeroSet : ∀ (K : Type u) [Field K] [CharZero K]
      (r : Nat), 0 < r → ∀ D : ExponentialPolynomialData K r,
        (zeroSet D).Finite) :
    ∀ (K : Type u) [Field K] [CharZero K], SchlickeweiEvertseStatement K := by
  intro K _ _ r hr D
  exact finiteZeroSet K r hr D

#print axioms oneTerm_zeroSet_empty
#print axioms oneTerm_zeroSet_finite
#print axioms twoTerm_eval_zero_iff
#print axioms twoTerm_zeroSet_subsingleton
#print axioms twoTerm_zeroSet_finite
#print axioms statement_of_finiteZeroSet

end Stage1.THM_M_0403.Proof
