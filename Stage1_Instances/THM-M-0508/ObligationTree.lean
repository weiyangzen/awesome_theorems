import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Finset.Prod

/-!
# THM-M-0508 conditional obligation composition

This module gives a checked finite representation-count interface and composes
an explicitly open eventual-positivity premise into the exact frozen target.
It does not supply the circle-method estimate behind that premise.
-/

namespace Stage1Instances.THM_M_0508.ObligationTree

/-- Local expansion of the frozen representation predicate, used because the
standalone validation command intentionally creates no mutable `.olean`. -/
def IsSumOfThreePrimes (n : Nat) : Prop :=
  ∃ p q r : Nat, p.Prime ∧ q.Prime ∧ r.Prime ∧ n = p + q + r

/-- Local expansion definitionally identical to the canonical target in
`Statement.lean`; the structural validator binds this file to that source hash. -/
def VinogradovThreePrimesTarget : Prop :=
  ∃ N : Nat, ∀ n : Nat, N ≤ n → Odd n → IsSumOfThreePrimes n

/-- Ordered prime triples below `n + 1` whose sum is `n`. -/
def primeTriples (n : Nat) : Finset (Nat × Nat × Nat) :=
  ((Finset.range (n + 1)).product
      ((Finset.range (n + 1)).product (Finset.range (n + 1)))).filter
    (fun x => x.1.Prime ∧ x.2.1.Prime ∧ x.2.2.Prime ∧
      n = x.1 + x.2.1 + x.2.2)

/-- The finite ordered representation count used by the architecture. -/
def representationCount (n : Nat) : Nat := (primeTriples n).card

/-- A positive finite count is exactly existence of three prime summands. -/
theorem representationCount_pos_iff (n : Nat) :
    0 < representationCount n ↔ IsSumOfThreePrimes n := by
  rw [representationCount, Finset.card_pos]
  constructor
  · rintro ⟨⟨p, ⟨q, r⟩⟩, hx⟩
    simp only [primeTriples, Finset.mem_filter, Finset.mem_product,
      Finset.mem_range] at hx
    exact ⟨p, q, r, hx.2.1, hx.2.2.1, hx.2.2.2.1, hx.2.2.2.2⟩
  · rintro ⟨p, q, r, hp, hq, hr, hsum⟩
    have hp_le : p ≤ n := hsum.symm ▸ by
      simpa [Nat.add_assoc] using Nat.le_add_right p (q + r)
    have hq_le : q ≤ n := hsum.symm ▸
      by simpa [Nat.add_assoc] using
        le_trans (Nat.le_add_right q r) (Nat.le_add_left (q + r) p)
    have hr_le : r ≤ n := hsum.symm ▸
      by simpa [Nat.add_assoc] using
        le_trans (Nat.le_add_left r q) (Nat.le_add_left (q + r) p)
    refine ⟨(p, (q, r)), Finset.mem_filter.mpr ⟨?_, hp, hq, hr, hsum⟩⟩
    exact Finset.mem_product.mpr ⟨Finset.mem_range.mpr (Nat.lt_succ_of_le hp_le),
      Finset.mem_product.mpr ⟨Finset.mem_range.mpr (Nat.lt_succ_of_le hq_le),
        Finset.mem_range.mpr (Nat.lt_succ_of_le hr_le)⟩⟩

/-- Open analytic leaf: the representation count is eventually positive on
odd inputs. A future circle-method development must prove this proposition. -/
def EventualPositiveRepresentationCount : Prop :=
  ∃ N : Nat, ∀ n : Nat, N ≤ n → Odd n → 0 < representationCount n

/-- Checked child-to-root composition. The analytic premise remains open. -/
theorem root_of_eventualPositiveRepresentationCount
    (h : EventualPositiveRepresentationCount) :
    VinogradovThreePrimesTarget := by
  rcases h with ⟨N, hN⟩
  refine ⟨N, fun n hn hodd => ?_⟩
  exact (representationCount_pos_iff n).mp (hN n hn hodd)

#check representationCount_pos_iff
#check root_of_eventualPositiveRepresentationCount
#print axioms representationCount_pos_iff
#print axioms root_of_eventualPositiveRepresentationCount

end Stage1Instances.THM_M_0508.ObligationTree
