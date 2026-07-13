import Mathlib.Data.Nat.Factors

/-!
# THM-M-0471 anchor-audit candidate

This module checks the frozen prime-list target through the manifest-pinned mathlib factorization
API. The theorem below is provisional anchor evidence only. It is not an accepted proof-phase
artifact or a theorem-completion claim.
-/

namespace Stage1Instances.THM_M_0471_AnchorAudit

/-- Audit-local copy of the frozen factor-list predicate. -/
def IsPrimeFactorList (n : Nat) (l : List Nat) : Prop :=
  (forall p, p ∈ l -> p.Prime) ∧ l.prod = n

/-- Literal audit copy of the statement phase's frozen canonical proposition. -/
def ExactTarget : Prop :=
  forall n : Nat, 1 < n ->
    exists l : List Nat,
      l ≠ [] ∧
        IsPrimeFactorList n l ∧
        forall k : List Nat, IsPrimeFactorList n k -> k.Perm l

/-- Exact candidate assembled from the pinned `Nat.primeFactorsList` theorem family. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro n hn
  refine ⟨n.primeFactorsList, (Nat.primeFactorsList_ne_nil n).2 hn, ?_, ?_⟩
  · exact
      ⟨fun p hp => Nat.prime_of_mem_primeFactorsList hp,
        Nat.prod_primeFactorsList (Nat.ne_zero_of_lt hn)⟩
  · intro k hk
    exact Nat.primeFactorsList_unique hk.2 hk.1

#check Nat.primeFactorsList
#check Nat.prime_of_mem_primeFactorsList
#check Nat.prod_primeFactorsList
#check Nat.primeFactorsList_ne_nil
#check Nat.primeFactorsList_unique
#check perm_of_prod_eq_prod

#print axioms Nat.prime_of_mem_primeFactorsList
#print axioms Nat.prod_primeFactorsList
#print axioms Nat.primeFactorsList_ne_nil
#print axioms Nat.primeFactorsList_unique
#print axioms perm_of_prod_eq_prod
#print axioms exactTarget_mathlib_candidate

#print sorries Nat.prime_of_mem_primeFactorsList
#print sorries Nat.prod_primeFactorsList
#print sorries Nat.primeFactorsList_ne_nil
#print sorries Nat.primeFactorsList_unique
#print sorries perm_of_prod_eq_prod
#print sorries exactTarget_mathlib_candidate

set_option pp.proofs false in
#print Nat.primeFactorsList_unique
set_option pp.proofs false in
#print perm_of_prod_eq_prod

set_option pp.explicit true in
set_option pp.universes true in
#print ExactTarget

end Stage1Instances.THM_M_0471_AnchorAudit
