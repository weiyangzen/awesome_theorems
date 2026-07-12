import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.NumberTheory.SmoothNumbers

/-!
# THM-M-0509: pinned anchor probes

These declarations are arithmetic infrastructure that could support a later
formalization. None states or proves Chen's theorem.
-/

#check Nat.Prime
#check Nat.prime_def
#check Nat.prime_iff_not_exists_mul_eq
#check Nat.factorization
#check Nat.factorization_eq_zero_of_not_dvd
#check Nat.primeFactors
#check Nat.primeFactorsList
#check Nat.mem_primeFactors
#check Nat.mem_primeFactorsList
#check Nat.prod_primeFactorsList
#check Nat.smoothNumbers
#check Nat.mem_smoothNumbers
#check Nat.smoothNumbers_eq_factoredNumbers_primesBelow
