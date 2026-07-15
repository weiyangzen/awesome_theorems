import Mathlib.Data.Finset.Prod
import ObligationTree

/-!
# THM-M-0487 proof-phase finite-count interface

This module implements a finite ordered representation count and proves that its positivity is
exactly the frozen three-prime witness condition. It does not prove that the count is positive,
either in the analytic range or across the Helfgott-Platt finite range.
-/

set_option autoImplicit false
set_option linter.unnecessarySimpa false

namespace Stage1Instances.THM_M_0487.Proof

open Stage1Instances.THM_M_0487
open Stage1Instances.THM_M_0487.ObligationTree

/-- Ordered prime triples below `n + 1` whose sum is `n`. -/
def primeTriples (n : Nat) : Finset (Nat × Nat × Nat) :=
  ((Finset.range (n + 1)).product
      ((Finset.range (n + 1)).product (Finset.range (n + 1)))).filter
    (fun x => x.1.Prime ∧ x.2.1.Prime ∧ x.2.2.Prime ∧
      n = x.1 + x.2.1 + x.2.2)

/-- The finite number of ordered three-prime representations of `n`. -/
def representationCount (n : Nat) : Nat := (primeTriples n).card

/-- Count positivity is exactly the frozen obligation tree's witness predicate. -/
theorem representationCount_pos_iff (n : Nat) :
    0 < representationCount n ↔ ThreePrimeRepresentation n := by
  rw [representationCount, Finset.card_pos]
  constructor
  · rintro ⟨⟨p, ⟨q, r⟩⟩, hx⟩
    simp only [primeTriples, Finset.mem_filter] at hx
    exact ⟨p, q, r, hx.2.1, hx.2.2.1, hx.2.2.2.1, hx.2.2.2.2⟩
  · rintro ⟨p, q, r, hp, hq, hr, hsum⟩
    have hp_le : p ≤ n := hsum.symm ▸ by
      simpa [Nat.add_assoc] using Nat.le_add_right p (q + r)
    have hq_le : q ≤ n := hsum.symm ▸ by
      simpa [Nat.add_assoc] using
        le_trans (Nat.le_add_right q r) (Nat.le_add_left (q + r) p)
    have hr_le : r ≤ n := hsum.symm ▸ by
      simpa [Nat.add_assoc] using
        le_trans (Nat.le_add_left r q) (Nat.le_add_left (q + r) p)
    refine ⟨(p, (q, r)), Finset.mem_filter.mpr ⟨?_, hp, hq, hr, hsum⟩⟩
    exact Finset.mem_product.mpr
      ⟨Finset.mem_range.mpr (Nat.lt_succ_of_le hp_le),
        Finset.mem_product.mpr
          ⟨Finset.mem_range.mpr (Nat.lt_succ_of_le hq_le),
            Finset.mem_range.mpr (Nat.lt_succ_of_le hr_le)⟩⟩

/-- Exact count-positivity reformulation of the canonical target. -/
def PositiveRepresentationCountTarget : Prop :=
  ∀ n : Nat, 5 < n → Odd n → 0 < representationCount n

/-- The canonical root is equivalent to positivity of the complete finite count at every input. -/
theorem weakGoldbachTarget_iff_positiveRepresentationCountTarget :
    WeakGoldbachTarget ↔ PositiveRepresentationCountTarget := by
  constructor <;> intro h n hn hodd
  · exact (representationCount_pos_iff n).mpr (h n hn hodd)
  · exact (representationCount_pos_iff n).mp (h n hn hodd)

#print axioms representationCount_pos_iff
#print axioms weakGoldbachTarget_iff_positiveRepresentationCountTarget
#print sorries representationCount_pos_iff
#print sorries weakGoldbachTarget_iff_positiveRepresentationCountTarget

end Stage1Instances.THM_M_0487.Proof
