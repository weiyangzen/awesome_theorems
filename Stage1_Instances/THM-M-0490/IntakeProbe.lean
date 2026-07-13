import Mathlib.NumberTheory.PrimeCounting

/-!
# THM-M-0490 discovery-only intake probe

These checks authenticate pinned nth-prime and monotonicity APIs and elaborate one prospective
discrete bounded-gap proposition type. They do not freeze a canonical target, relate that type to
Zhang's published liminf statement, or prove a bounded-prime-gap theorem.
-/

namespace Stage1Instances.THM_M_0490

#check Nat.nth
#check Nat.Prime
#check Nat.infinite_setOf_prime
#check Nat.prime_nth_prime
#check Nat.nth_strictMono
#check Nat.primeCounting

example (n : Nat) : Nat.Prime (Nat.nth Nat.Prime n) :=
  Nat.prime_nth_prime n

example (n : Nat) : Nat.nth Nat.Prime n < Nat.nth Nat.Prime (n + 1) :=
  Nat.nth_strictMono Nat.infinite_setOf_prime (Nat.lt_succ_self n)

#check (show Prop from
  forall N : Nat, exists n : Nat, And (N <= n)
    (Nat.nth Nat.Prime (n + 1) - Nat.nth Nat.Prime n < 70000000))

end Stage1Instances.THM_M_0490
