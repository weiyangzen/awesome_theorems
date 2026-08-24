import Mathlib

/-!
Frozen provenance (not a canonical Lake import):
import FormalConjectures.ErdosProblems.1128
Erdos1128.erdos_1128

This file restates the frozen proposition with every provider-local definition
expanded.  In the provider, `answer(False)` reduces to `False`, and
`Erdos1128.IsMonochromaticBox f A₁ B₁ C₁` expands to the existential below.
-/

open Cardinal Set

namespace AwesomeTheorems.Stage5.S5_CLM_00003712

theorem statement_equivalent_to_counterexample :
    (False ↔
      ∀ (A B C : Type) (_ : #A = aleph 1) (_ : #B = aleph 1)
        (_ : #C = aleph 1) (f : A → B → C → Fin 2),
        ∃ (A₁ : Set A) (B₁ : Set B) (C₁ : Set C),
          #A₁ = aleph 0 ∧ #B₁ = aleph 0 ∧ #C₁ = aleph 0 ∧
          ∃ c : Fin 2,
            ∀ a ∈ A₁, ∀ b ∈ B₁, ∀ c' ∈ C₁, f a b c' = c) ↔
    ¬ (∀ (A B C : Type) (_ : #A = aleph 1) (_ : #B = aleph 1)
        (_ : #C = aleph 1) (f : A → B → C → Fin 2),
        ∃ (A₁ : Set A) (B₁ : Set B) (C₁ : Set C),
          #A₁ = aleph 0 ∧ #B₁ = aleph 0 ∧ #C₁ = aleph 0 ∧
          ∃ c : Fin 2,
            ∀ a ∈ A₁, ∀ b ∈ B₁, ∀ c' ∈ C₁, f a b c' = c) := by
  simp only [false_iff, iff_self]

end AwesomeTheorems.Stage5.S5_CLM_00003712
