import Statement

/-!
# THM-M-0650 conditional obligation composition

This module checks the substructure-to-embedding composition boundary selected
by the frozen obligation architecture. The central structural-induction theorem
is an explicit premise here; this file does not claim proof-phase credit for it.
-/

namespace Stage1Instances.THM_M_0650

universe u v w

open FirstOrder

/-- The exact embedding-level Tarski-Vaught theorem used by the pinned
substructure wrapper. Keeping it as a proposition makes the imported terminal
body an explicit obligation rather than hiding it behind a short invocation. -/
def EmbeddingTarskiVaughtPackage : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) (N : Type u)
      [L.Structure M] [L.Structure N] (f : L.Embedding M N),
    (forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> M) (a : N),
      phi.Realize default (Fin.snoc (f ∘ x) a : _ -> N) ->
        exists b : M,
          phi.Realize default (Fin.snoc (f ∘ x) (f b) : _ -> N)) ->
      forall {n : Nat} (phi : L.Formula (Fin n)) (x : Fin n -> M),
        phi.Realize (f ∘ x) <-> phi.Realize x

/-- Checked composition from the embedding theorem to the exact canonical
substructure target. The only substantive premise is the named bridge package. -/
theorem root_of_embeddingTarskiVaughtPackage
    (embeddingTV : EmbeddingTarskiVaughtPackage.{u, v, w}) :
    TarskiVaughtTarget.{u, v, w} := by
  intro L M _ S htv
  exact fun n phi x => embeddingTV L S M S.subtype htv phi x

#print axioms root_of_embeddingTarskiVaughtPackage

end Stage1Instances.THM_M_0650
