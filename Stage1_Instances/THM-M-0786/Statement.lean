import Mathlib.MeasureTheory.Constructions.Pi

/-!
# THM-M-0786: Martin's Borel determinacy theorem statement

This file freezes the Gale-Stewart formulation selected at intake. A strategy is
total on finite histories; its values are consulted only at positions belonging
to that player. `MeasurableSet` uses the product Borel structure on Baire space.
This module elaborates the target but does not prove Borel determinacy.
-/

namespace Stage1Instances.THM_M_0786

abbrev Play := ℕ → ℕ
abbrev History := List ℕ
abbrev Strategy := History → ℕ

/-- The first `n` moves of a play, in chronological order. -/
def initialHistory (x : Play) (n : ℕ) : History :=
  List.ofFn fun i : Fin n => x i

/-- A play follows the two strategies, with Player I moving at even stages. -/
def Compatible (first second : Strategy) (x : Play) : Prop :=
  ∀ n : ℕ, x n = if Even n then first (initialHistory x n) else second (initialHistory x n)

/-- Player I can force the resulting play into the payoff set. -/
def FirstWins (payoff : Set Play) (first : Strategy) : Prop :=
  ∀ (second : Strategy) (x : Play), Compatible first second x → x ∈ payoff

/-- Player II can force the resulting play outside the payoff set. -/
def SecondWins (payoff : Set Play) (second : Strategy) : Prop :=
  ∀ (first : Strategy) (x : Play), Compatible first second x → x ∉ payoff

/-- Every Borel Gale-Stewart game on natural-number moves is determined. -/
def BorelDeterminacyTarget : Prop :=
  ∀ payoff : Set Play, MeasurableSet payoff →
    (∃ first : Strategy, FirstWins payoff first) ∨
    (∃ second : Strategy, SecondWins payoff second)

/-- Direct expansion of the selected encoding. -/
def ExpandedTarget : Prop :=
  ∀ payoff : Set (ℕ → ℕ), MeasurableSet payoff →
    (∃ first : List ℕ → ℕ,
      ∀ (second : List ℕ → ℕ) (x : ℕ → ℕ),
        (∀ n : ℕ, x n = if Even n then first (List.ofFn fun i : Fin n => x i)
          else second (List.ofFn fun i : Fin n => x i)) → x ∈ payoff) ∨
    (∃ second : List ℕ → ℕ,
      ∀ (first : List ℕ → ℕ) (x : ℕ → ℕ),
        (∀ n : ℕ, x n = if Even n then first (List.ofFn fun i : Fin n => x i)
          else second (List.ofFn fun i : Fin n => x i)) → x ∉ payoff)

/-- Kernel-checked identity with the binder-level expansion. -/
theorem target_iff_expanded : BorelDeterminacyTarget ↔ ExpandedTarget := by
  rfl

-- Structural mutations used by the statement validator.
def mutationRemovedBorel : Prop :=
  ∀ payoff : Set Play,
    (∃ first : Strategy, FirstWins payoff first) ∨
    (∃ second : Strategy, SecondWins payoff second)

def mutationChangedMovesToBool : Prop :=
  ∀ payoff : Set (ℕ → Bool), MeasurableSet payoff → True

def mutationFirstMovesAtOddStages : Prop :=
  ∀ payoff : Set Play, MeasurableSet payoff →
    (∃ first : Strategy, ∀ (second : Strategy) (x : Play),
      (∀ n : ℕ, x n = if Odd n then first (initialHistory x n)
        else second (initialHistory x n)) → x ∈ payoff) ∨
    (∃ second : Strategy, SecondWins payoff second)

def mutationBothPlayersTargetPayoff : Prop :=
  ∀ payoff : Set Play, MeasurableSet payoff →
    (∃ first : Strategy, FirstWins payoff first) ∨
    (∃ second : Strategy, ∀ (first : Strategy) (x : Play),
      Compatible first second x → x ∈ payoff)

/-- Empty and universal payoff sets remain included boundary cases. -/
theorem empty_payoff_boundary : MeasurableSet (∅ : Set Play) := by simp
theorem universal_payoff_boundary : MeasurableSet (Set.univ : Set Play) := by simp

end Stage1Instances.THM_M_0786

set_option pp.explicit true in
#print Stage1Instances.THM_M_0786.BorelDeterminacyTarget
