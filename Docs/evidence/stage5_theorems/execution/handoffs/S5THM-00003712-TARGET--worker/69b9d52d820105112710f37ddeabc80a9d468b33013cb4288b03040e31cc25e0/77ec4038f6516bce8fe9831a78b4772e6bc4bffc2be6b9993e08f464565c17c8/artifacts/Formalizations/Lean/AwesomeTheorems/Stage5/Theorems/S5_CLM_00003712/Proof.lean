import Mathlib

/-!
Frozen provenance (not a canonical Lake import):
import FormalConjectures.ErdosProblems.1128
Erdos1128.erdos_1128

The provider proof depends on a placeholder-backed Prikry--Mills declaration.
This claim-owned file therefore imports only Mathlib and records the complete
logical composition from an independently kernel-checked counterexample.
-/

open Cardinal Set

namespace AwesomeTheorems.Stage5.S5_CLM_00003712

theorem erdos_1128_of_prikry_mills
    (hPM :
      ∃ (X : Type) (_ : #X = aleph 1) (f : X → X → X → Fin 2),
        ∀ (A₁ B₁ C₁ : Set X),
          #A₁ = aleph 0 → #B₁ = aleph 0 → #C₁ = aleph 0 →
          ¬ (∃ c : Fin 2,
            ∀ a ∈ A₁, ∀ b ∈ B₁, ∀ c' ∈ C₁, f a b c' = c)) :
    False ↔
      ∀ (A B C : Type) (_ : #A = aleph 1) (_ : #B = aleph 1)
        (_ : #C = aleph 1) (f : A → B → C → Fin 2),
        ∃ (A₁ : Set A) (B₁ : Set B) (C₁ : Set C),
          #A₁ = aleph 0 ∧ #B₁ = aleph 0 ∧ #C₁ = aleph 0 ∧
          ∃ c : Fin 2,
            ∀ a ∈ A₁, ∀ b ∈ B₁, ∀ c' ∈ C₁, f a b c' = c := by
  constructor
  · intro h
    exact h.elim
  · intro h
    obtain ⟨X, hX, f, hf⟩ := hPM
    obtain ⟨A₁, B₁, C₁, hA, hB, hC, hbox⟩ := h X X X hX hX hX f
    exact hf A₁ B₁ C₁ hA hB hC hbox

end AwesomeTheorems.Stage5.S5_CLM_00003712
