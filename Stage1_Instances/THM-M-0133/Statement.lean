import Init

/-!
# THM-M-0133: exact Fermat's Last Theorem statement

This module freezes and tests the statement boundary only. It contains no proof
of Fermat's Last Theorem or of the Wiles--Taylor-Wiles argument.
-/

namespace Stage1Instances.THM_M_0133

/-- The exact natural-number target: every exponent at least three has no
nonzero natural solution to the Fermat equation. -/
def WilesFermatLastTheoremTarget : Prop :=
  ∀ n : Nat, 3 ≤ n →
    ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

/-- A direct expansion of the pinned mathlib definitions
`FermatLastTheorem`, `FermatLastTheoremFor`, and `FermatLastTheoremWith`. -/
def PinnedMathlibSourceShape : Prop :=
  ∀ n : Nat, n ≥ 3 →
    ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

/-- Checked identity with the expanded pinned mathlib source shape. -/
theorem target_iff_pinnedMathlibSourceShape :
    WilesFermatLastTheoremTarget ↔ PinnedMathlibSourceShape :=
  Iff.rfl

/-- The positive-natural wording used in the intake's human claim. -/
def PositiveNaturalSourceShape : Prop :=
  ∀ n : Nat, n > 2 →
    ∀ a b c : Nat, 0 < a → 0 < b → 0 < c →
      a ^ n + b ^ n ≠ c ^ n

/-- Checked transport between nonzero naturals and positive naturals, including
the equivalent exponent boundary `n > 2`. -/
theorem target_iff_positiveNaturalSourceShape :
    WilesFermatLastTheoremTarget ↔ PositiveNaturalSourceShape := by
  constructor
  · intro h n hn a b c ha hb hc
    exact h n hn a b c (Nat.ne_of_gt ha) (Nat.ne_of_gt hb) (Nat.ne_of_gt hc)
  · intro h n hn a b c ha hb hc
    exact h n hn a b c (Nat.pos_of_ne_zero ha) (Nat.pos_of_ne_zero hb)
      (Nat.pos_of_ne_zero hc)

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedExponentBound : Prop :=
  ∀ n a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
    a ^ n + b ^ n ≠ c ^ n

def mutationChangedValueDomain : Prop :=
  ∀ n : Nat, 3 ≤ n →
    ∀ a b c : Int, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

def mutationChangedBinderScope : Prop :=
  ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
    ∀ n : Nat, 3 ≤ n → a ^ n + b ^ n ≠ c ^ n

def mutationIncludesExponentTwo : Prop :=
  ∀ n : Nat, 2 ≤ n →
    ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

/-- The removed-bound mutation is concretely invalid at exponent two. -/
theorem mutationRemovedExponentBound_is_false :
    ¬ mutationRemovedExponentBound := by
  intro h
  exact h 2 3 4 5 (by decide) (by decide) (by decide) (by decide)

/-- The weakened-boundary mutation is concretely invalid at exponent two. -/
theorem mutationIncludesExponentTwo_is_false :
    ¬ mutationIncludesExponentTwo := by
  intro h
  exact h 2 (by decide) 3 4 5 (by decide) (by decide) (by decide) (by decide)

end Stage1Instances.THM_M_0133

set_option pp.explicit true in
#print Stage1Instances.THM_M_0133.WilesFermatLastTheoremTarget
