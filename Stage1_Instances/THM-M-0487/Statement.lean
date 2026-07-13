import Mathlib.Algebra.Ring.Int.Parity
import Mathlib.Data.Nat.Prime.Defs

/-!
# THM-M-0487 canonical Lean statement

This module freezes the weak Goldbach target, a checked presentation transport, statement
mutations, and boundary witnesses. It deliberately contains no proof of the unbounded target.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0487

/-- Every odd natural number greater than five is a sum of three natural primes. -/
def WeakGoldbachTarget : Prop :=
  forall n : Nat, 5 < n -> Odd n ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r

/-- Literal integer-input encoding of the source claim, with positive natural prime witnesses. -/
def IntegerWeakGoldbachTarget : Prop :=
  forall z : Int, (5 : Int) < z -> Odd z ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ z = (p : Int) + q + r

/-- Equality-reversed form with the same binders and hypotheses. -/
def ReversedEqualityWeakGoldbachTarget : Prop :=
  forall n : Nat, 5 < n -> Odd n ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ p + q + r = n

/-- Equality orientation is presentation only. -/
theorem weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget :
    WeakGoldbachTarget <-> ReversedEqualityWeakGoldbachTarget := by
  constructor
  . intro h n hn hodd
    obtain ⟨p, q, r, hp, hq, hr, hsum⟩ := h n hn hodd
    exact ⟨p, q, r, hp, hq, hr, hsum.symm⟩
  . intro h n hn hodd
    obtain ⟨p, q, r, hp, hq, hr, hsum⟩ := h n hn hodd
    exact ⟨p, q, r, hp, hq, hr, hsum.symm⟩

/-- Positivity of every source input gives a checked source-domain transport. -/
theorem weakGoldbachTarget_iff_integerWeakGoldbachTarget :
    WeakGoldbachTarget <-> IntegerWeakGoldbachTarget := by
  constructor
  . intro h z hz hodd
    have hz_nonneg : 0 ≤ z := by omega
    obtain ⟨p, q, r, hp, hq, hr, hsum⟩ :=
      h z.toNat (by simpa [Int.toNat_of_nonneg hz_nonneg] using hz)
        (by
          rw [← Int.odd_coe_nat]
          simpa [Int.toNat_of_nonneg hz_nonneg] using hodd)
    refine ⟨p, q, r, hp, hq, hr, ?_⟩
    simpa [Int.toNat_of_nonneg hz_nonneg] using
      congrArg (fun n : Nat => (n : Int)) hsum
  . intro h n hn hodd
    obtain ⟨p, q, r, hp, hq, hr, hsum⟩ :=
      h (n : Int) (by exact_mod_cast hn) (Odd.natCast hodd)
    refine ⟨p, q, r, hp, hq, hr, ?_⟩
    exact_mod_cast hsum
/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedOddHypothesis : Prop :=
  forall n : Nat, 5 < n ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r

def mutationChangedDomainToFinEight : Prop :=
  forall n : Fin 8, 5 < n.val -> Odd n.val ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n.val = p + q + r

def mutationChangedBinderScope : Prop :=
  exists p q r : Nat, forall n : Nat, 5 < n -> Odd n ->
    Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r

def mutationIncludedFiveBoundary : Prop :=
  forall n : Nat, 5 ≤ n -> Odd n ->
    exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r

variable
  (hRemoved : mutationRemovedOddHypothesis)
  (hDomain : mutationChangedDomainToFinEight)
  (hScope : mutationChangedBinderScope)
  (hBoundary : mutationIncludedFiveBoundary)

#check_failure (show WeakGoldbachTarget from hRemoved)
#check_failure (show WeakGoldbachTarget from hDomain)
#check_failure (show WeakGoldbachTarget from hScope)
#check_failure (show WeakGoldbachTarget from hBoundary)

/-! Boundary witnesses check the antecedent and witness shape, not the unbounded target. -/

/-- Five is excluded by the strict lower bound. -/
theorem five_excluded : Not (5 < (5 : Nat)) := by decide

/-- The inclusive-boundary mutation is false because three natural primes cannot sum to five. -/
theorem five_not_three_prime_sum :
    Not (exists p q r : Nat,
      Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ (5 : Nat) = p + q + r) := by
  rintro ⟨p, q, r, hp, hq, hr, hsum⟩
  have hp_two := hp.two_le
  have hq_two := hq.two_le
  have hr_two := hr.two_le
  omega

theorem mutationIncludedFiveBoundary_is_false : Not mutationIncludedFiveBoundary := by
  intro h
  exact five_not_three_prime_sum (h 5 (by decide) (by decide))

/-- The finite-domain mutation collapses to the single qualifying input seven. -/
theorem mutationChangedDomainToFinEight_is_true : mutationChangedDomainToFinEight := by
  intro n hn hodd
  have hn_le : n.val ≤ 7 := Nat.le_pred_of_lt n.isLt
  have hn_cases : n.val = 6 ∨ n.val = 7 := by omega
  rcases hn_cases with hn_eq | hn_eq
  . have : Not (Odd (6 : Nat)) := by decide
    exact (this (hn_eq ▸ hodd)).elim
  . exact ⟨2, 2, 3, Nat.prime_two, Nat.prime_two, Nat.prime_three, hn_eq⟩

/-- Seven is the first natural satisfying both canonical hypotheses. -/
theorem seven_included : 5 < (7 : Nat) ∧ Odd (7 : Nat) := by decide

/-- Seven verifies that repetitions and the even prime two must remain admissible. -/
theorem seven_repeated_prime_representation :
    Nat.Prime 2 ∧ Nat.Prime 2 ∧ Nat.Prime 3 ∧ (7 : Nat) = 2 + 2 + 3 :=
  ⟨Nat.prime_two, Nat.prime_two, Nat.prime_three, rfl⟩

/-- Even inputs are outside the canonical antecedent. -/
theorem eight_not_odd : Not (Odd (8 : Nat)) := by decide

#check weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget
#check weakGoldbachTarget_iff_integerWeakGoldbachTarget
#print axioms weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget
#print axioms weakGoldbachTarget_iff_integerWeakGoldbachTarget

set_option pp.universes true in
set_option pp.explicit true in
#print WeakGoldbachTarget

end Stage1Instances.THM_M_0487
