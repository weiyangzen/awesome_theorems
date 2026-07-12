import Mathlib.NumberTheory.Chebyshev
import Mathlib.NumberTheory.SumPrimeReciprocals

/-!
# THM-M-0508 anchor probes

These checks inventory pinned mathlib support. None has the three-primes
conclusion, and this module intentionally proves no part of the target.
-/

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
