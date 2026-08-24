/-
Frozen provider provenance; this is deliberately not an executable import in
the canonical Lake environment:
import FormalConjectures.Arxiv.2001.02665.RingelConjecture
Arxiv.«2001.02665».ringel_conjecture_large
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003497

/-- The source-to-target leg for the text-identical Ringel proposition. -/
theorem ringel_source_to_target
    (h :
      ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
        T.IsTree → T.edgeSet.ncard = n →
        ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
          Pairwise (fun i j =>
            Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
          ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1)))) :
    ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
      T.IsTree → T.edgeSet.ncard = n →
      ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
        Pairwise (fun i j =>
          Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
        ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1))) := h

/-- The target-to-source leg for the text-identical Ringel proposition. -/
theorem ringel_target_to_source
    (h :
      ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
        T.IsTree → T.edgeSet.ncard = n →
        ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
          Pairwise (fun i j =>
            Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
          ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1)))) :
    ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
      T.IsTree → T.edgeSet.ncard = n →
      ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
        Pairwise (fun i j =>
          Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
        ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1))) := h

end AwesomeTheorems.Stage5.S5_CLM_00003497
