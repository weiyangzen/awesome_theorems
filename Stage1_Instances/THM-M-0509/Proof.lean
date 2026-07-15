import Mathlib.Data.Finset.Prod
import Mathlib.NumberTheory.ArithmeticFunction.Misc
import Statement

/-!
# THM-M-0509 proof-phase interfaces

This module implements exact, unconditional interfaces for the frozen `P₂`
predicate and finite representation count.  It does not prove the missing
eventual positivity estimate or Chen's theorem.
-/

namespace Stage1Instances.THM_M_0509.Proof

open Stage1Instances.THM_M_0509

/-- The product encoding selected for `IsP2` is equivalent to having one or
two prime factors counted with multiplicity. -/
theorem isP2_iff_cardFactors_pos_le_two (a : Nat) :
    IsP2 a ↔ 0 < ArithmeticFunction.cardFactors a ∧
      ArithmeticFunction.cardFactors a ≤ 2 := by
  constructor
  · rintro (ha | ⟨q, r, hq, hr, rfl⟩)
    · rw [ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr ha]
      omega
    · rw [ArithmeticFunction.cardFactors_mul hq.ne_zero hr.ne_zero,
        ArithmeticFunction.cardFactors_apply_prime hq,
        ArithmeticFunction.cardFactors_apply_prime hr]
      omega
  · rintro ⟨hpos, hle⟩
    have hcases : ArithmeticFunction.cardFactors a = 1 ∨
        ArithmeticFunction.cardFactors a = 2 := by
      omega
    rcases hcases with h1 | h2
    · exact Or.inl (ArithmeticFunction.cardFactors_eq_one_iff_prime.mp h1)
    · rw [ArithmeticFunction.cardFactors_apply] at h2
      obtain ⟨q, r, hlist⟩ := List.length_eq_two.mp h2
      have ha0 : a ≠ 0 := by
        intro ha
        subst a
        simp at hpos
      have hprod := Nat.prod_primeFactorsList ha0
      rw [hlist] at hprod
      refine Or.inr ⟨q, r, ?_, ?_, ?_⟩
      · apply Nat.prime_of_mem_primeFactorsList (n := a)
        rw [hlist]
        simp
      · apply Nat.prime_of_mem_primeFactorsList (n := a)
        rw [hlist]
        simp
      · simpa using hprod.symm

/-- All prime-plus-`P₂` representations of `N`.  Both witnesses lie below
`N + 1`, so this finite search is extensionally complete. -/
noncomputable def representations (N : Nat) : Finset (Nat × Nat) := by
  classical
  exact ((Finset.range (N + 1)).product (Finset.range (N + 1))).filter
    (fun x => Nat.Prime x.1 ∧ IsP2 x.2 ∧ N = x.1 + x.2)

/-- The finite number of prime-plus-`P₂` representations of `N`. -/
noncomputable def representationCount (N : Nat) : Nat :=
  (representations N).card

/-- Positivity of the finite count is exactly existence of a representation
in the canonical target's witness shape. -/
theorem representationCount_pos_iff (N : Nat) :
    0 < representationCount N ↔
      ∃ p a : Nat, Nat.Prime p ∧ IsP2 a ∧ N = p + a := by
  classical
  rw [representationCount, Finset.card_pos]
  constructor
  · rintro ⟨⟨p, a⟩, hpa⟩
    simp only [representations, Finset.mem_filter] at hpa
    exact ⟨p, a, hpa.2.1, hpa.2.2.1, hpa.2.2.2⟩
  · rintro ⟨p, a, hp, ha, hsum⟩
    have hp_le : p ≤ N := hsum.symm ▸ Nat.le_add_right p a
    have ha_le : a ≤ N := hsum.symm ▸ Nat.le_add_left a p
    refine ⟨(p, a), Finset.mem_filter.mpr ⟨?_, hp, ha, hsum⟩⟩
    exact Finset.mem_product.mpr
      ⟨Finset.mem_range.mpr (Nat.lt_succ_of_le hp_le),
        Finset.mem_range.mpr (Nat.lt_succ_of_le ha_le)⟩

/-- The exact analytic cut exposed by the finite representation count. -/
def EventualPositiveRepresentationCount : Prop :=
  ∃ threshold : Nat, ∀ N : Nat, threshold ≤ N → Even N →
    0 < representationCount N

/-- Checked bidirectional composition between the canonical target and the
eventual positivity cut.  Neither direction assumes an unlisted premise. -/
theorem chenTheoremTarget_iff_eventualPositiveRepresentationCount :
    ChenTheoremTarget ↔ EventualPositiveRepresentationCount := by
  constructor <;>
    rintro ⟨threshold, h⟩ <;>
    refine ⟨threshold, fun N hN hEven => ?_⟩
  · exact (representationCount_pos_iff N).mpr (h N hN hEven)
  · exact (representationCount_pos_iff N).mp (h N hN hEven)

#print axioms isP2_iff_cardFactors_pos_le_two
#print sorries isP2_iff_cardFactors_pos_le_two
#print axioms representationCount_pos_iff
#print sorries representationCount_pos_iff
#print axioms chenTheoremTarget_iff_eventualPositiveRepresentationCount
#print sorries chenTheoremTarget_iff_eventualPositiveRepresentationCount

end Stage1Instances.THM_M_0509.Proof
