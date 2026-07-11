import ObligationTree

/-!
# THM-M-0396 independent validation probes

These probes reimplement the proof phase's normalization and conditional root
composition without importing `Proof`. They validate only the partial closure
claimed by the proof receipt; the Baker-Matveev core estimate remains open.
-/

noncomputable section

open scoped BigOperators

namespace Stage1Rev56.THMM0396.Validation

universe u

open Stage1Rev56.THMM0396

theorem independent_exp_intCast_mul_log_eq_zpow
    (x : Real) (b : Int) (hx : 0 < x) :
    Real.exp ((b : Real) * Real.log x) = x ^ b := by
  cases b with
  | ofNat n =>
      simp only [Int.cast_natCast, Int.ofNat_eq_natCast, zpow_natCast]
      simpa [Real.exp_log hx] using Real.exp_nat_mul (Real.log x) n
  | negSucc n =>
      simp only [Int.cast_negSucc, zpow_negSucc]
      rw [neg_mul, Real.exp_neg, Real.exp_nat_mul, Real.exp_log hx]

theorem independent_exp_sum_log_eq_algebraicProduct
    {K : Type u} [Field K] {n : Nat}
    (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
    (hpos : ∀ i, 0 < embedding (alpha i)) :
    Real.exp (∑ i, (coeff i : Real) * Real.log (embedding (alpha i))) =
      algebraicProduct embedding alpha coeff := by
  rw [Real.exp_sum]
  exact Finset.prod_congr rfl fun i _ =>
    independent_exp_intCast_mul_log_eq_zpow
      (embedding (alpha i)) (coeff i) (hpos i)

theorem independent_statement_of_core
    (core : ∀ (n : Nat) (K : Type u) [Field K] [NumberField K]
      (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
      (A : Fin n → Real) (B : Real),
      ObligationTree.CoreEstimate n K embedding alpha coeff A B) : Statement.{u} := by
  intro n hn K _ _ embedding alpha coeff A B hpos hheight hA hB hcoeff hnonzero
  exact core n K embedding alpha coeff A B hn hpos hheight hA hB hcoeff hnonzero

#print axioms independent_exp_intCast_mul_log_eq_zpow
#print axioms independent_exp_sum_log_eq_algebraicProduct
#print axioms independent_statement_of_core

end Stage1Rev56.THMM0396.Validation
