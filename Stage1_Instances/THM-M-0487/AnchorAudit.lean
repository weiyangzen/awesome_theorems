import Mathlib.NumberTheory.Chebyshev
import Mathlib.NumberTheory.SumPrimeReciprocals

/-!
# THM-M-0487 anchor-audit probes

These checks authenticate pinned prime-distribution support and the exact frozen proposition. None
of the checked mathlib declarations has a three-prime representation conclusion, and this module
deliberately supplies no proof of weak Goldbach.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0487_AnchorAudit

/-- Audit-local copy of the already frozen target, used only to print its elaborated shape. -/
def ExactTarget : Prop :=
  forall n : Nat, 5 < n -> Odd n ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r

#check Nat.Prime
#check Nat.primesBelow
#check Nat.mem_primesBelow
#check Nat.primeCounting
#check Nat.tendsto_primeCounting
#check Nat.primesBelow_card_eq_primeCounting'
#check Nat.infinite_setOf_prime
#check Chebyshev.theta
#check Chebyshev.eventually_primeCounting_le
#check not_summable_one_div_on_primes

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0487_AnchorAudit
