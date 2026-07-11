import Mathlib.Data.Nat.GCD.Basic

/-!
# THM-M-0390 independent validation probe

This module independently rechecks the one implemented arithmetic leaf from
`Proof.lean`. It deliberately does not import that module or assert the open
Catalan root and exponent branches.
-/

namespace Stage1.THM_M_0390.Validation

/-- Independent reconstruction of the implemented coprime-bases invariant. -/
theorem independent_solution_bases_coprime {x p y q : Nat}
    (hp : 0 < p) (hq : 0 < q)
    (heq : x ^ p + 1 = y ^ q) :
    Nat.Coprime x y := by
  have powers_coprime : Nat.Coprime (x ^ p) (y ^ q) := by
    rw [← heq]
    exact Nat.coprime_self_add_right.mpr (Nat.coprime_one_right _)
  exact (Nat.coprime_pow_right_iff hq x y).mp
    ((Nat.coprime_pow_left_iff hp x (y ^ q)).mp powers_coprime)

#print axioms independent_solution_bases_coprime

end Stage1.THM_M_0390.Validation
