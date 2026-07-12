import Mathlib.Data.Nat.Prime.Basic

/-!
# THM-M-0509: exact Chen-theorem statement

This module freezes and tests the statement boundary only. It contains no proof
of Chen's theorem.
-/

namespace Stage1Instances.THM_M_0509

/-- A natural number is a `P₂` when it is prime or a product of two primes.
The two prime witnesses may coincide. This deliberately excludes `0` and `1`.
-/
def IsP2 (a : Nat) : Prop :=
  Nat.Prime a ∨ ∃ q r : Nat, Nat.Prime q ∧ Nat.Prime r ∧ a = q * r

/-- The exact natural-number `P + P₂` form of Chen's theorem: above one
uniform threshold, every even natural is a prime plus a `P₂`. -/
def ChenTheoremTarget : Prop :=
  ∃ threshold : Nat, ∀ N : Nat, threshold ≤ N → Even N →
    ∃ p a : Nat, Nat.Prime p ∧ IsP2 a ∧ N = p + a

/-- Direct expansion of the selected classical `P + P₂` source shape. -/
def PinnedSourceShape : Prop :=
  ∃ threshold : Nat, ∀ N : Nat, threshold ≤ N → Even N →
    ∃ p a : Nat, Nat.Prime p ∧
      (Nat.Prime a ∨ ∃ q r : Nat, Nat.Prime q ∧ Nat.Prime r ∧ a = q * r) ∧
      N = p + a

/-- Checked identity between the canonical target and its direct expansion. -/
theorem chenTheoremTarget_iff_pinnedSourceShape :
    ChenTheoremTarget ↔ PinnedSourceShape := by
  rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedEvenness : Prop :=
  ∃ threshold : Nat, ∀ N : Nat, threshold ≤ N →
    ∃ p a : Nat, Nat.Prime p ∧ IsP2 a ∧ N = p + a

def mutationExactTwoPrimes : Prop :=
  ∃ threshold : Nat, ∀ N : Nat, threshold ≤ N → Even N →
    ∃ p q r : Nat, Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ N = p + q * r

def mutationChangedDomain : Prop :=
  ∃ threshold : Int, ∀ N : Int, threshold ≤ N → Even N →
    ∃ p a : Int, Nat.Prime p.natAbs ∧ IsP2 a.natAbs ∧ N = p + a

def mutationNonuniformThreshold : Prop :=
  ∀ N : Nat, Even N → ∃ threshold : Nat, threshold ≤ N →
    ∃ p a : Nat, Nat.Prime p ∧ IsP2 a ∧ N = p + a

/-- A prime is admitted as a `P₂`. -/
theorem prime_boundary {p : Nat} (hp : Nat.Prime p) : IsP2 p :=
  Or.inl hp

/-- A square of a prime is admitted, so multiplicity and repeated factors are
part of the frozen boundary convention. -/
theorem prime_square_boundary {p : Nat} (hp : Nat.Prime p) : IsP2 (p * p) :=
  Or.inr ⟨p, p, hp, hp, rfl⟩

/-- Zero is not a `P₂`. -/
theorem zero_not_p2 : ¬ IsP2 0 := by
  rintro (h | ⟨q, r, hq, hr, hqr⟩)
  · exact Nat.not_prime_zero h
  · have hq0 : q ≠ 0 := Nat.Prime.ne_zero hq
    have hr0 : r ≠ 0 := Nat.Prime.ne_zero hr
    exact Nat.mul_ne_zero hq0 hr0 hqr.symm

/-- One is not a `P₂`. -/
theorem one_not_p2 : ¬ IsP2 1 := by
  rintro (h | ⟨q, r, hq, hr, hqr⟩)
  · exact Nat.not_prime_one h
  · have hq2 : 2 ≤ q := Nat.Prime.two_le hq
    have hr2 : 2 ≤ r := Nat.Prime.two_le hr
    have : 4 ≤ q * r := Nat.mul_le_mul hq2 hr2
    omega

end Stage1Instances.THM_M_0509

set_option pp.explicit true in
#print Stage1Instances.THM_M_0509.ChenTheoremTarget
