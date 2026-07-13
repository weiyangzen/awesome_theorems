import Mathlib.NumberTheory.PrimeCounting
import Mathlib.NumberTheory.SelbergSieve
import Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt

/-!
# THM-M-0491 discovery-only intake probe

These checks authenticate pinned nth-prime, prime-counting, generic Selberg upper-bound sieve, and
von Mangoldt interfaces. They do not select a theorem from Maynard's paper, define his
multidimensional sieve, state a bounded-prime-gap conclusion, or prove THM-M-0491.
-/

#check Nat.nth
#check Nat.Prime
#check Nat.infinite_setOf_prime
#check Nat.prime_nth_prime
#check Nat.nth_strictMono
#check Nat.exists_infinite_primes
#check Nat.primeCounting
#check Nat.tendsto_primeCounting
#check Filter.frequently_atTop
#check BoundingSieve
#check SelbergSieve
#check BoundingSieve.siftedSum_le_mainSum_errSum_of_upperMoebius
#check ArithmeticFunction.vonMangoldt
#check ArithmeticFunction.vonMangoldt_apply_prime
