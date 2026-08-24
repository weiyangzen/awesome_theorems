/-
Frozen provider provenance; this is deliberately not an executable import in
the canonical Lake environment:
import FormalConjectures.Arxiv.2001.02665.RingelConjecture
Arxiv.«2001.02665».ringel_conjecture_large
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003497

/-- Forgetting the cyclic-shift condition turns the stronger asymptotic
Kotzig decomposition into the exact asymptotic Ringel decomposition. -/
theorem ringel_conjecture_large_of_cyclic
    (hcyclic :
      ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
        T.IsTree → T.edgeSet.ncard = n →
        ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
          (∀ i v, f i v = f 0 v + i) ∧
          Pairwise (fun i j =>
            Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
          ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1)))) :
    ∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
      T.IsTree → T.edgeSet.ncard = n →
      ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
        Pairwise (fun i j =>
          Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
        ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1))) := by
  refine hcyclic.mono ?_
  intro n hn V _ T htree hedge
  obtain ⟨f, _hshift, hdisjoint, hcover⟩ := hn T htree hedge
  exact ⟨f, hdisjoint, hcover⟩

end AwesomeTheorems.Stage5.S5_CLM_00003497
