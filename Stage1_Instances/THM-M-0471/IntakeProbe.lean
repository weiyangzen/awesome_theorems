import Mathlib.Data.Nat.Factorization.Defs

/-!
# THM-M-0471 discovery-only intake probe

These checks authenticate pinned natural-number prime-factorization interfaces and representative
boundaries. They do not freeze the canonical root, audit terminal proof bodies, or create an
accepted THM-M-0471 proof declaration.
-/

#check @Nat.primeFactorsList
#check @Nat.prime_of_mem_primeFactorsList
#check @Nat.prod_primeFactorsList
#check @Nat.primeFactorsList_ne_nil
#check @Nat.primeFactorsList_unique
#check @Nat.prod_factorization_pow_eq_self
#check @Nat.factorization_inj
#check @Nat.prod_pow_factorization_eq_self
#check @Nat.factorizationEquiv

example : Nat.primeFactorsList 2 = [2] := by
  exact Nat.primeFactorsList_two

example : List.Perm [2, 3] (Nat.primeFactorsList 6) := by
  apply Nat.primeFactorsList_unique
  · decide
  · decide

example : List.Perm [3, 2] (Nat.primeFactorsList 6) := by
  apply Nat.primeFactorsList_unique
  · decide
  · decide

example : Nat.primeFactorsList 0 = [] := Nat.primeFactorsList_zero

example : Nat.primeFactorsList 1 = [] := Nat.primeFactorsList_one
