import Statement
import Mathlib.Data.Nat.Factors

/-!
# THM-M-0471 conditional obligation composition

This module checks the child-to-root interfaces frozen by the obligation registry. The pinned
mathlib factorization family remains an explicit premise: this phase does not install it as the
canonical proof or claim machine closure.
-/

namespace Stage1Instances.THM_M_0471.ObligationTree

/-- The exact prime-factor-list conclusion supplied by the audited pinned candidate. -/
def ExactPrimeListAnchor : Prop :=
  Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget

/-- A candidate canonical factor-list construction. -/
abbrev PrimeFactorWitness := Nat -> List Nat

/-- Nonemptiness package for a candidate factor-list construction. -/
def WitnessNonempty (factors : PrimeFactorWitness) : Prop :=
  forall n : Nat, 1 < n ->
    Not (factors n = [])

/-- Primality package for every member of a candidate factor list. -/
def WitnessPrimality (factors : PrimeFactorWitness) : Prop :=
  forall (n p : Nat), p ∈ factors n -> p.Prime

/-- Product-reconstruction package for a candidate factor-list construction. -/
def WitnessProduct (factors : PrimeFactorWitness) : Prop :=
  forall n : Nat, 1 < n -> (factors n).prod = n

/-- Uniqueness data for every prime list with the same product. -/
def PrimeFactorUniqueness (factors : PrimeFactorWitness) : Prop :=
  forall (n : Nat) (k : List Nat),
    Stage1Instances.THM_M_0471.IsPrimeFactorList n k ->
    k.Perm (factors n)

/-- Checked assembly of existence and uniqueness into the exact frozen target. -/
theorem exactPrimeListAnchor_of_packages
    (factors : PrimeFactorWitness)
    (nonempty : WitnessNonempty factors)
    (primality : WitnessPrimality factors)
    (product : WitnessProduct factors)
    (uniqueness : PrimeFactorUniqueness factors) : ExactPrimeListAnchor := by
  intro n hn
  exact ⟨factors n, nonempty n hn, ⟨fun p hp => primality n p hp, product n hn⟩,
    fun k hk => uniqueness n k hk⟩

/-- Conditional child-to-root composition with no new mathematical premise. -/
theorem root_of_exactPrimeListAnchor
    (anchor : ExactPrimeListAnchor) :
    Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget := by
  exact anchor

#check Nat.primeFactorsList
#check Nat.primeFactorsList_ne_nil
#check Nat.prime_of_mem_primeFactorsList
#check Nat.prod_primeFactorsList
#check Nat.primeFactorsList_unique
#check perm_of_prod_eq_prod

#print axioms exactPrimeListAnchor_of_packages
#print axioms root_of_exactPrimeListAnchor

end Stage1Instances.THM_M_0471.ObligationTree
