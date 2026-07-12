import Statement

/-!
# THM-M-0650 proof integration

This module closes the frozen Tarski-Vaught target against the proof-bearing
declarations in the repository's pinned mathlib revision. The embedding-level
declaration is exposed separately so the short substructure specialization
does not conceal the terminal proof body.
-/

namespace Stage1Instances.THM_M_0650.Proof

universe u v w

open FirstOrder

/-- The pinned embedding-level terminal body, with its complete theorem shape
restated locally for an exact elaboration check. -/
theorem embeddingTarskiVaught
    (L : FirstOrder.Language.{v, w}) (M N : Type u)
    [L.Structure M] [L.Structure N] (f : L.Embedding M N)
    (h : forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> M) (a : N),
      phi.Realize default (Fin.snoc (f ∘ x) a : _ -> N) ->
        exists b : M,
          phi.Realize default (Fin.snoc (f ∘ x) (f b) : _ -> N)) :
    forall {n : Nat} (phi : L.Formula (Fin n)) (x : Fin n -> M),
      phi.Realize (f ∘ x) <-> phi.Realize x :=
  f.isElementary_of_exists h

/-- Exact proof of the frozen root. This is definitionally the selected
substructure statement and uses the already pinned, proof-bearing mathlib
wrapper. -/
theorem tarskiVaught : TarskiVaughtTarget.{u, v, w} := by
  intro L M _ S h
  exact S.isElementary_of_exists h

#print axioms embeddingTarskiVaught
#print axioms tarskiVaught

end Stage1Instances.THM_M_0650.Proof
