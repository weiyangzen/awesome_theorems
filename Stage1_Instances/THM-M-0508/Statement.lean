import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Order.Filter.AtTopBot.CountablyGenerated

/-!
# THM-M-0508: exact Vinogradov three-primes statement

This module freezes the repository claim "every sufficiently large odd natural
number is a sum of three primes." It contains no proof of that claim.
-/

namespace Stage1Instances.THM_M_0508

/-- An additive representation by three natural primes. Witnesses are not
required to be distinct, matching the unqualified repository phrase "three
primes." -/
def IsSumOfThreePrimes (n : Nat) : Prop :=
  ∃ p q r : Nat, p.Prime ∧ q.Prime ∧ r.Prime ∧ n = p + q + r

/-- Canonical target: one uniform threshold works for every later odd natural
number. The threshold itself need not be odd. -/
def VinogradovThreePrimesTarget : Prop :=
  ∃ N : Nat, ∀ n : Nat, N ≤ n → Odd n → IsSumOfThreePrimes n

/-- Equivalent eventual-filter presentation of the canonical target. -/
def VinogradovThreePrimesEventually : Prop :=
  ∀ᶠ n : Nat in Filter.atTop, Odd n → IsSumOfThreePrimes n

/-- Checked transport between explicit-threshold and eventual presentations. -/
theorem target_iff_eventually :
    VinogradovThreePrimesTarget ↔ VinogradovThreePrimesEventually := by
  simp only [VinogradovThreePrimesTarget, VinogradovThreePrimesEventually,
    Filter.eventually_atTop]

-- Structural mutations are elaborated but receive no proof credit. Their
-- distinct printed expressions are checked by the statement validator.

/-- Removed-hypothesis mutation: incorrectly includes even inputs. -/
def mutationRemovedOddHypothesis : Prop :=
  ∃ N : Nat, ∀ n : Nat, N ≤ n → IsSumOfThreePrimes n

/-- Changed-domain mutation: integer inputs and natural-prime casts. -/
def mutationChangedDomain : Prop :=
  ∃ N : Int, ∀ n : Int, N ≤ n → n % 2 = 1 →
    ∃ p q r : Nat, p.Prime ∧ q.Prime ∧ r.Prime ∧
      n = (p : Int) + (q : Int) + (r : Int)

/-- Changed-binder-scope mutation: the threshold may depend on the input. -/
def mutationChangedBinderScope : Prop :=
  ∀ n : Nat, ∃ N : Nat, N ≤ n → Odd n → IsSumOfThreePrimes n

/-- Boundary mutation: incorrectly requires the conclusion at the threshold
without restricting that input to be odd. -/
def mutationThresholdUnconditionallyIncluded : Prop :=
  ∃ N : Nat, IsSumOfThreePrimes N ∧
    ∀ n : Nat, N ≤ n → Odd n → IsSumOfThreePrimes n

/-- The target says nothing about even inputs, including even inputs beyond a
witnessed threshold. This checks the intended implication boundary without
assuming the number-theory theorem. -/
theorem even_input_boundary (N n : Nat) (_hn : N ≤ n) (heven : Even n) :
    ¬ Odd n := by
  exact Nat.not_odd_iff_even.mpr heven

end Stage1Instances.THM_M_0508

set_option pp.explicit true in
#print Stage1Instances.THM_M_0508.VinogradovThreePrimesTarget
