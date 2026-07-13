import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0471 proof execution

This module installs the manifest-pinned `Nat.primeFactorsList` proof family at the interfaces in
the frozen obligation tree and composes those interfaces to the exact canonical target. The direct
root wrapper and the frozen-composition wrapper share the same upstream mathlib proof bodies and
do not receive duplicate proof credit.
-/

namespace Stage1Instances.THM_M_0471.Proof

open Stage1Instances.THM_M_0471
open Stage1Instances.THM_M_0471.ObligationTree

/-! Exact interfaces for the lower-level leaves exposed by the pinned uniqueness body. -/

/-- Nonzero normalizations used by product reconstruction and uniqueness (`M0471-N-NONZERO`). -/
def NonzeroNormalization : Prop :=
  (forall n : Nat, 1 < n -> n ≠ 0) ∧
    forall (l : List Nat), (forall p, p ∈ l -> p.Prime) -> l.prod ≠ 0

/-- Prime divisibility exposes a member of the product list (`M0471-L-PRIME-DVD-PRODUCT`). -/
def PrimeDvdProduct : Prop :=
  forall (p : Nat) (l : List Nat), p.Prime -> p ∣ l.prod -> exists a, a ∈ l ∧ p ∣ a

/-- A prime divisor of a product of primes occurs in the list (`M0471-L-MEM-PRIME-DIVISOR`). -/
def PrimeDivisorMembership : Prop :=
  forall (p : Nat) (l : List Nat),
    p.Prime -> (forall q, q ∈ l -> q.Prime) -> p ∣ l.prod -> p ∈ l

/-- Move a selected occurrence to the head while erasing it (`M0471-C-ERASE-PERM`). -/
def ErasePermutation : Prop :=
  forall (p : Nat) (l : List Nat), p ∈ l -> l.Perm (p :: l.erase p)

/-- Cancel a common nonzero head from equal natural-number products (`M0471-N-CANCEL-HEAD`). -/
def CancelCommonHead : Prop :=
  forall (p a b : Nat), p ≠ 0 -> p * a = p * b -> a = b

/-- Equal products of prime lists determine the same multiset (`M0471-L-PERM-PRODUCT`). -/
def PrimeProductPermutation : Prop :=
  forall (l1 l2 : List Nat),
    l1.prod = l2.prod ->
      (forall p, p ∈ l1 -> p.Prime) ->
      (forall p, p ∈ l2 -> p.Prime) ->
      l1.Perm l2

/-- Checked nonzero side conditions used inside the pinned factorization family. -/
theorem nonzeroNormalization : NonzeroNormalization := by
  constructor
  · intro n hn
    exact Nat.ne_zero_of_lt hn
  · intro l hprime
    apply List.prod_ne_zero
    intro hzero
    exact (hprime 0 hzero).ne_zero rfl

/-- Install the pinned prime-divides-product theorem at the frozen leaf interface. -/
theorem primeDvdProduct : PrimeDvdProduct := by
  intro p l hp hdvd
  exact (Prime.dvd_prod_iff (Nat.prime_iff.mp hp)).mp hdvd

/-- Install the pinned divisor-to-membership theorem at the frozen leaf interface. -/
theorem primeDivisorMembership : PrimeDivisorMembership := by
  intro p l hp hprime hdvd
  exact mem_list_primes_of_dvd_prod (Nat.prime_iff.mp hp)
    (fun q hq => Nat.prime_iff.mp (hprime q hq)) hdvd

/-- Install the list erasure permutation used by the recursive uniqueness proof. -/
theorem erasePermutation : ErasePermutation := by
  intro p l hp
  exact List.perm_cons_erase hp

/-- Install natural-number cancellation at the recursive uniqueness interface. -/
theorem cancelCommonHead : CancelCommonHead := by
  intro p a b hp h
  exact (mul_right_inj' hp).mp h

/-- Install the pinned recursive prime-product permutation theorem. -/
theorem primeProductPermutation : PrimeProductPermutation := by
  intro l1 l2 hprod hprime1 hprime2
  exact perm_of_prod_eq_prod hprod
    (fun p hp => Nat.prime_iff.mp (hprime1 p hp))
    (fun p hp => Nat.prime_iff.mp (hprime2 p hp))

/-- The canonical factor-list construction (`M0471-C-WITNESS`). -/
abbrev primeFactorWitness : PrimeFactorWitness := Nat.primeFactorsList

/-- The pinned exact boundary theorem supplies nonemptiness (`M0471-L-NONEMPTY`). -/
theorem witnessNonempty : WitnessNonempty primeFactorWitness := by
  intro n hn
  exact (Nat.primeFactorsList_ne_nil n).2 hn

/-- Every member of the canonical factor list is prime (`M0471-L-PRIMALITY`). -/
theorem witnessPrimality : WitnessPrimality primeFactorWitness := by
  intro n p hp
  exact Nat.prime_of_mem_primeFactorsList hp

/-- The canonical factor list reconstructs each input greater than one (`M0471-L-PRODUCT`). -/
theorem witnessProduct : WitnessProduct primeFactorWitness := by
  intro n hn
  exact Nat.prod_primeFactorsList (nonzeroNormalization.1 n hn)

/-- Every alternative prime list is a permutation of the canonical list (`M0471-L-UNIQUENESS`). -/
theorem primeFactorUniqueness : PrimeFactorUniqueness primeFactorWitness := by
  intro n k hk
  exact Nat.primeFactorsList_unique hk.2 hk.1

/-- Reconstruct uniqueness through the frozen product-permutation and nonzero interfaces. -/
theorem primeFactorUniqueness_via_components : PrimeFactorUniqueness primeFactorWitness := by
  intro n k hk
  apply primeProductPermutation k (primeFactorWitness n)
  · rw [hk.2]
    apply (Nat.prod_primeFactorsList ?_).symm
    intro hn
    subst n
    exact (nonzeroNormalization.2 k hk.1) hk.2
  · exact hk.1
  · intro p hp
    exact witnessPrimality n p hp

/-- Assemble the exact audited child proposition through the frozen package interface. -/
theorem exactPrimeListAnchor : ExactPrimeListAnchor :=
  exactPrimeListAnchor_of_packages primeFactorWitness witnessNonempty witnessPrimality
    witnessProduct primeFactorUniqueness_via_components

/-- The exact canonical root obtained through the frozen child-to-parent composition. -/
theorem fundamentalTheoremOfArithmetic_via_frozen_composition :
    FundamentalTheoremOfArithmeticTarget :=
  root_of_exactPrimeListAnchor exactPrimeListAnchor

/-- A direct exact-root wrapper over the same deduplicated pinned proof family. -/
theorem fundamentalTheoremOfArithmetic : FundamentalTheoremOfArithmeticTarget := by
  intro n hn
  refine ⟨n.primeFactorsList, (Nat.primeFactorsList_ne_nil n).2 hn, ?_, ?_⟩
  · exact
      ⟨fun p hp => Nat.prime_of_mem_primeFactorsList hp,
        Nat.prod_primeFactorsList (Nat.ne_zero_of_lt hn)⟩
  · intro k hk
    exact Nat.primeFactorsList_unique hk.2 hk.1

assert_no_sorry Nat.primeFactorsList
assert_no_sorry Nat.primeFactorsList_ne_nil
assert_no_sorry Nat.prime_of_mem_primeFactorsList
assert_no_sorry Nat.prod_primeFactorsList
assert_no_sorry Nat.primeFactorsList_unique
assert_no_sorry perm_of_prod_eq_prod
assert_no_sorry Prime.dvd_prod_iff
assert_no_sorry mem_list_primes_of_dvd_prod
assert_no_sorry List.perm_cons_erase
assert_no_sorry mul_right_inj'
assert_no_sorry nonzeroNormalization
assert_no_sorry primeDvdProduct
assert_no_sorry primeDivisorMembership
assert_no_sorry erasePermutation
assert_no_sorry cancelCommonHead
assert_no_sorry primeProductPermutation
assert_no_sorry witnessNonempty
assert_no_sorry witnessPrimality
assert_no_sorry witnessProduct
assert_no_sorry primeFactorUniqueness
assert_no_sorry primeFactorUniqueness_via_components
assert_no_sorry exactPrimeListAnchor
assert_no_sorry fundamentalTheoremOfArithmetic_via_frozen_composition
assert_no_sorry fundamentalTheoremOfArithmetic

#print sorries Nat.primeFactorsList
#print sorries Nat.primeFactorsList_ne_nil
#print sorries Nat.prime_of_mem_primeFactorsList
#print sorries Nat.prod_primeFactorsList
#print sorries Nat.primeFactorsList_unique
#print sorries perm_of_prod_eq_prod
#print sorries Prime.dvd_prod_iff
#print sorries mem_list_primes_of_dvd_prod
#print sorries List.perm_cons_erase
#print sorries mul_right_inj'
#print sorries nonzeroNormalization
#print sorries primeDvdProduct
#print sorries primeDivisorMembership
#print sorries erasePermutation
#print sorries cancelCommonHead
#print sorries primeProductPermutation
#print sorries witnessNonempty
#print sorries witnessPrimality
#print sorries witnessProduct
#print sorries primeFactorUniqueness
#print sorries primeFactorUniqueness_via_components
#print sorries exactPrimeListAnchor
#print sorries fundamentalTheoremOfArithmetic_via_frozen_composition
#print sorries fundamentalTheoremOfArithmetic

#print axioms Nat.primeFactorsList_ne_nil
#print axioms Nat.prime_of_mem_primeFactorsList
#print axioms Nat.prod_primeFactorsList
#print axioms Nat.primeFactorsList_unique
#print axioms perm_of_prod_eq_prod
#print axioms Prime.dvd_prod_iff
#print axioms mem_list_primes_of_dvd_prod
#print axioms List.perm_cons_erase
#print axioms mul_right_inj'
#print axioms nonzeroNormalization
#print axioms primeDvdProduct
#print axioms primeDivisorMembership
#print axioms erasePermutation
#print axioms cancelCommonHead
#print axioms primeProductPermutation
#print axioms witnessNonempty
#print axioms witnessPrimality
#print axioms witnessProduct
#print axioms primeFactorUniqueness
#print axioms primeFactorUniqueness_via_components
#print axioms exactPrimeListAnchor
#print axioms fundamentalTheoremOfArithmetic_via_frozen_composition
#print axioms fundamentalTheoremOfArithmetic

end Stage1Instances.THM_M_0471.Proof
