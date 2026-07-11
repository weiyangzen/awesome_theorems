import Mathlib.Data.Nat.GCD.Basic

/-!
# THM-M-0390 proof execution

This module records a kernel-checked arithmetic invariant needed by the frozen
normalization obligation. It does not assert the open Catalan root or any of
its three exponent branches.
-/

namespace Stage1.THM_M_0390

/-- Any natural-number solution of the oriented Catalan equation with positive
exponents has coprime bases. This discharges the coprimality step `NP.4` of the
frozen normalization ledger; the rest of `THM-M-0390-N-PRIMITIVE` remains open.
-/
theorem solution_bases_coprime {x p y q : Nat}
    (hp : 0 < p) (hq : 0 < q)
    (heq : x ^ p + 1 = y ^ q) :
    Nat.Coprime x y := by
  have hpowers : Nat.Coprime (x ^ p) (y ^ q) := by
    rw [← heq]
    exact Nat.coprime_self_add_right.mpr (Nat.coprime_one_right _)
  have hleft : Nat.Coprime x (y ^ q) :=
    (Nat.coprime_pow_left_iff hp x (y ^ q)).mp hpowers
  exact (Nat.coprime_pow_right_iff hq x y).mp hleft

/-- Wrapper specialized to the exact root hypotheses. -/
theorem catalan_solution_bases_coprime {x p y q : Nat}
    (_hx : 1 < x) (hp : 1 < p) (_hy : 1 < y) (hq : 1 < q)
    (heq : x ^ p + 1 = y ^ q) :
    Nat.Coprime x y :=
  solution_bases_coprime (Nat.zero_lt_of_lt hp) (Nat.zero_lt_of_lt hq) heq

#print axioms solution_bases_coprime
#print axioms catalan_solution_bases_coprime

end Stage1.THM_M_0390
