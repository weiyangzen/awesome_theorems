import Mathlib

/-!
Machine-facing closure for `S5-CLM-00003496`.

Frozen workset module spelling (the numeric path component requires escaping in
Lean source):
import FormalConjectures.Arxiv.2001.02665.RingelConjecture
Pinned declaration: Arxiv.«2001.02665».kotzig_conjecture_large

No local definition, notation, coercion, instance, syntax, macro, or namespace
alias intervenes between this declaration and the pinned provider theorem.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003496

open SimpleGraph

/-- Exact proposition-level transport with the mathematical proof supplied explicitly. -/
theorem kotzig_conjecture_large_proof
    (h :
      ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
        T.IsTree → T.edgeSet.ncard = n →
        ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
          (∀ i v, f i v = f 0 v + i) ∧
          Pairwise (fun i j => Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
          ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1)))) :
    ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
      T.IsTree → T.edgeSet.ncard = n →
      ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
        (∀ i v, f i v = f 0 v + i) ∧
        Pairwise (fun i j => Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
        ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1))) := by
  exact h

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003496
