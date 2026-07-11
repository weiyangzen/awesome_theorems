import ObligationTree

/-!
# THM-M-0396 proof execution

This module implements the elementary logarithm/product normalization part of
the frozen proof architecture and rechecks the exact conditional composition
into the root. It does not supply the Baker-Matveev analytic estimate.
-/

noncomputable section

open scoped BigOperators

namespace Stage1Rev56.THMM0396.Proof

universe u

open Stage1Rev56.THMM0396

/-- A positive real base raised to an integer coefficient is the exponential
of the corresponding integer multiple of its real logarithm. -/
theorem exp_intCast_mul_log_eq_zpow (x : Real) (b : Int) (hx : 0 < x) :
    Real.exp ((b : Real) * Real.log x) = x ^ b := by
  cases b with
  | ofNat n =>
      simp only [Int.cast_natCast, Int.ofNat_eq_natCast, zpow_natCast]
      rw [Real.exp_nat_mul, Real.exp_log hx]
  | negSucc n =>
      simp only [Int.cast_negSucc, zpow_negSucc]
      rw [neg_mul, Real.exp_neg, Real.exp_nat_mul, Real.exp_log hx]

/-- Frozen normalization obligation `M0396-N1`: exponentiating the additive
logarithmic form recovers the multiplicative algebraic product. -/
theorem exp_sum_log_eq_algebraicProduct
    {K : Type u} [Field K] {n : Nat}
    (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
    (hpos : ∀ i, 0 < embedding (alpha i)) :
    Real.exp (∑ i, (coeff i : Real) * Real.log (embedding (alpha i))) =
      algebraicProduct embedding alpha coeff := by
  rw [Real.exp_sum]
  apply Finset.prod_congr rfl
  intro i _
  exact exp_intCast_mul_log_eq_zpow (embedding (alpha i)) (coeff i) (hpos i)

/-- Proof-phase copy of the exact terminal-to-root composition. The terminal
estimate remains an explicit premise and is not asserted by this module. -/
theorem statement_of_core
    (core : ∀ (n : Nat) (K : Type u) [Field K] [NumberField K]
      (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
      (A : Fin n → Real) (B : Real),
      ObligationTree.CoreEstimate n K embedding alpha coeff A B) : Statement.{u} :=
  ObligationTree.root_compose core

#print axioms exp_intCast_mul_log_eq_zpow
#print axioms exp_sum_log_eq_algebraicProduct
#print axioms statement_of_core

end Stage1Rev56.THMM0396.Proof
