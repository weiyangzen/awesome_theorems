import Mathlib.Data.Nat.Prime.Defs

/-!
# THM-M-0471 canonical Lean statement

This module freezes the natural-number, prime-list formulation of the fundamental theorem of
arithmetic selected at intake. It defines the exact target and statement-boundary fixtures, but
does not prove the target or import the proof-bearing natural-factorization module.
-/

namespace Stage1Instances.THM_M_0471

/-- `l` is a prime factor list for `n`; order is deliberately not fixed. -/
def IsPrimeFactorList (n : Nat) (l : List Nat) : Prop :=
  (forall p, p ∈ l -> p.Prime) ∧ l.prod = n

/--
Every natural number greater than one has a nonempty prime factor list, and every other prime
factor list for the same number differs from it only by permutation.
-/
def FundamentalTheoremOfArithmeticTarget : Prop :=
  forall n : Nat, 1 < n ->
    exists l : List Nat,
      l ≠ [] ∧ IsPrimeFactorList n l ∧
        forall k : List Nat, IsPrimeFactorList n k -> k.Perm l

/-- Direct expansion of the selected target, used as a checked representation transport. -/
def ExpandedPrimeListTarget : Prop :=
  forall n : Nat, 1 < n ->
    exists l : List Nat,
      l ≠ [] ∧
        (forall p, p ∈ l -> p.Prime) ∧
        l.prod = n ∧
        forall k : List Nat,
          (forall p, p ∈ k -> p.Prime) -> k.prod = n -> k.Perm l

/-- Checked transport to the fully expanded prime-list spelling. -/
theorem fundamentalTheoremOfArithmeticTarget_iff_expanded :
    FundamentalTheoremOfArithmeticTarget ↔ ExpandedPrimeListTarget := by
  constructor
  · intro h n hn
    obtain ⟨l, hne, ⟨hprime, hprod⟩, hunique⟩ := h n hn
    exact ⟨l, hne, hprime, hprod, fun k hkprime hkprod =>
      hunique k ⟨hkprime, hkprod⟩⟩
  · intro h n hn
    obtain ⟨l, hne, hprime, hprod, hunique⟩ := h n hn
    exact ⟨l, hne, ⟨hprime, hprod⟩, fun k hk =>
      hunique k hk.1 hk.2⟩

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedGreaterThanOne : Prop :=
  forall n : Nat,
    exists l : List Nat,
      l ≠ [] ∧ IsPrimeFactorList n l ∧
        forall k : List Nat, IsPrimeFactorList n k -> k.Perm l

def mutationChangedDomainToInt : Prop :=
  forall n : Int, 1 < n ->
    exists l : List Nat,
      l ≠ [] ∧ IsPrimeFactorList n.natAbs l ∧
        forall k : List Nat, IsPrimeFactorList n.natAbs k -> k.Perm l

def mutationChangedWitnessBinderScope : Prop :=
  exists l : List Nat, forall n : Nat, 1 < n ->
    l ≠ [] ∧ IsPrimeFactorList n l ∧
      forall k : List Nat, IsPrimeFactorList n k -> k.Perm l

def mutationExcludedTwo : Prop :=
  forall n : Nat, 2 < n ->
    exists l : List Nat,
      l ≠ [] ∧ IsPrimeFactorList n l ∧
        forall k : List Nat, IsPrimeFactorList n k -> k.Perm l

variable
  (hRemoved : mutationRemovedGreaterThanOne)
  (hDomain : mutationChangedDomainToInt)
  (hScope : mutationChangedWitnessBinderScope)
  (hBoundary : mutationExcludedTwo)

/-- The least in-scope natural number is included by the canonical antecedent. -/
theorem two_boundary_in_domain : 1 < (2 : Nat) := by decide

#check fundamentalTheoremOfArithmeticTarget_iff_expanded
#print axioms fundamentalTheoremOfArithmeticTarget_iff_expanded

set_option pp.explicit true in
set_option pp.universes true in
#print FundamentalTheoremOfArithmeticTarget

end Stage1Instances.THM_M_0471
