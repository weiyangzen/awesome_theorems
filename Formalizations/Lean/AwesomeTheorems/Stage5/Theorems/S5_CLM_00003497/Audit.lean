/-
Frozen provider provenance; this is deliberately not an executable import in
the canonical Lake environment:
import FormalConjectures.Arxiv.2001.02665.RingelConjecture
Arxiv.«2001.02665».ringel_conjecture_large
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003497

/-- An independently spelled audit term for the cyclic-to-Ringel projection. -/
theorem audit_ringel_transport
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
  rintro n hn V _ T htree hedge
  rcases hn T htree hedge with ⟨f, _hshift, hdisjoint, hcover⟩
  exact ⟨f, hdisjoint, hcover⟩

end AwesomeTheorems.Stage5.S5_CLM_00003497
