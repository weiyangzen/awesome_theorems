import Init

/-!
# THM-M-0391 exact statement boundary

This module contains only the canonical proposition and checked statement-level
transports. It does not assert or prove Mihailescu's theorem.
-/

namespace Stage1Instances.THMM0391

/-- The exact rev-5.6 target, with binders and hypotheses in intake order. -/
def MihailescuTarget : Prop :=
  ∀ x a y b : Nat,
    1 < x →
      1 < a →
        1 < y →
          1 < b →
            x ^ a = y ^ b + 1 →
              x = 3 ∧ a = 2 ∧ y = 2 ∧ b = 3

/-- The legacy named-predicate presentation, restated locally for an exact
checked comparison without importing the much broader `Mathlib.Tactic`. -/
def LegacyStatementShape : Prop :=
  ∀ x a y b : Nat,
    (1 < x ∧ 1 < a ∧ 1 < y ∧ 1 < b) →
      x ^ a = y ^ b + 1 →
        x = 3 ∧ a = 2 ∧ y = 2 ∧ b = 3

/-- Checked transport between the curried canonical target and the legacy
conjunction encoding. This is statement identity evidence, not proof closure. -/
theorem mihailescuTarget_iff_legacyStatementShape :
    MihailescuTarget ↔ LegacyStatementShape := by
  constructor
  · intro h x a y b hnontrivial heq
    exact h x a y b hnontrivial.1 hnontrivial.2.1
      hnontrivial.2.2.1 hnontrivial.2.2.2 heq
  · intro h x a y b hx ha hy hb heq
    exact h x a y b ⟨hx, ha, hy, hb⟩ heq

/-- Boundary mutation: allowing exponent `b = 1` admits `3^2 = 8^1 + 1`. -/
theorem weakening_right_exponent_hypothesis_is_invalid :
    ¬ (∀ x a y b : Nat,
      1 < x → 1 < a → 1 < y → 0 < b →
      x ^ a = y ^ b + 1 →
      x = 3 ∧ a = 2 ∧ y = 2 ∧ b = 3) := by
  intro h
  have bad := h 3 2 8 1 (by decide) (by decide) (by decide) (by decide) (by decide)
  exact (by decide : (8 : Nat) ≠ 2) bad.2.2.1

/-- Boundary mutation: allowing exponent `a = 1` admits `9 = 2^3 + 1`. -/
theorem weakening_left_exponent_hypothesis_is_invalid :
    ¬ (∀ x a y b : Nat,
      1 < x → 0 < a → 1 < y → 1 < b →
      x ^ a = y ^ b + 1 →
      x = 3 ∧ a = 2 ∧ y = 2 ∧ b = 3) := by
  intro h
  have bad := h 9 1 2 3 (by decide) (by decide) (by decide) (by decide) (by decide)
  exact (by decide : (9 : Nat) ≠ 3) bad.1

end Stage1Instances.THMM0391
