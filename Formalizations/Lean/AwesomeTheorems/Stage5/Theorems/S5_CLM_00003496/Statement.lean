import Mathlib

/-
Frozen provenance only; the canonical package deliberately does not import this module:
import FormalConjectures.Arxiv.2001.02665.RingelConjecture
Arxiv.«2001.02665».kotzig_conjecture_large
Provider revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003496

open SimpleGraph

/-- The claim-owned surface is definitionally identical in both directions. -/
theorem statement_bidirectional :
    (∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
      T.IsTree → T.edgeSet.ncard = n →
      ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
        (∀ i v, f i v = f 0 v + i) ∧
        Pairwise (fun i j => Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
        ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1)))) ↔
    (∀ᶠ (n : ℕ) in Filter.atTop, ∀ {V : Type} [Finite V] (T : SimpleGraph V),
      T.IsTree → T.edgeSet.ncard = n →
      ∃ f : Fin (2 * n + 1) → (V ↪ Fin (2 * n + 1)),
        (∀ i v, f i v = f 0 v + i) ∧
        Pairwise (fun i j => Disjoint (T.map (f i)).edgeSet (T.map (f j)).edgeSet) ∧
        ⨆ i, T.map (f i) = (⊤ : SimpleGraph (Fin (2 * n + 1)))) := by
  exact Iff.rfl

end AwesomeTheorems.Stage5.S5_CLM_00003496
