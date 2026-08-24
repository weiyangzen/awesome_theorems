import Mathlib

/-!
Statement transport for `S5-CLM-00003496`.

Frozen workset module spelling (the numeric path component requires escaping in
Lean source):
import FormalConjectures.Arxiv.2001.02665.RingelConjecture
Pinned declaration: Arxiv.«2001.02665».kotzig_conjecture_large

The target proposition is deliberately written out rather than hidden behind a
local definition.  This keeps every source symbol visible to the elaborator and
makes the two directions of the crosswalk definitionally transparent.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003496

open SimpleGraph

/-- The source-to-target direction, with proof authority explicit as an input. -/
theorem kotzig_conjecture_large_statement
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

/-- Reverse transport is the identity because the two propositions elaborate identically. -/
theorem kotzig_conjecture_large_statement_to_source
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
