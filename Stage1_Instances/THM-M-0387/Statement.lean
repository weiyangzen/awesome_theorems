import Init

/-!
# THM-M-0387: exact Fermat's Last Theorem statement

This module freezes and tests the statement boundary only. It contains no proof
of Fermat's Last Theorem.
-/

namespace Stage1Instances.THM_M_0387

/-- The exact natural-number target: every exponent at least three has no
nonzero natural solution to the Fermat equation. -/
def FermatLastTheoremTarget : Prop :=
  ∀ n : Nat, 3 ≤ n →
    ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

/-- A local expansion of the pinned mathlib source definitions
`FermatLastTheorem`, `FermatLastTheoremFor`, and `FermatLastTheoremWith`.
Keeping the expansion explicit lets the statement elaborate with only `Init`.
-/
def PinnedMathlibSourceShape : Prop :=
  ∀ n : Nat, n ≥ 3 →
    ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

/-- Checked identity with the expanded pinned mathlib source shape. -/
theorem fermatLastTheoremTarget_iff_pinnedMathlibSourceShape :
    FermatLastTheoremTarget ↔ PinnedMathlibSourceShape :=
  Iff.rfl

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

/-- The boundary mutation is concretely invalid at exponent two. -/
theorem mutationIncludesExponentTwo_is_false :
    ¬ mutationIncludesExponentTwo := by
  intro h
  exact h 2 (by decide) 3 4 5 (by decide) (by decide) (by decide) (by decide)

end Stage1Instances.THM_M_0387

set_option pp.explicit true in
#print Stage1Instances.THM_M_0387.FermatLastTheoremTarget
