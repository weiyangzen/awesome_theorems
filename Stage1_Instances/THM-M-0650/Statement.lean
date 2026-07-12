import Mathlib.ModelTheory.ElementarySubstructures

/-!
# THM-M-0650: exact Tarski-Vaught statement

This module freezes the witness-to-elementarity direction of the Tarski-Vaught
test selected by the intake. It does not claim a source audit or theorem proof.
-/

namespace Stage1Instances.THM_M_0650

universe u v w

open FirstOrder

/-- The witness condition used in the Tarski-Vaught test. The last variable of
the bounded formula is the witness; the first `n` variables are parameters from
the substructure. -/
def TarskiVaughtWitnessCondition (L : FirstOrder.Language.{v, w}) (M : Type u)
    [L.Structure M] (S : L.Substructure M) : Prop :=
  forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
      (x : Fin n -> S) (a : M),
    phi.Realize default (Fin.snoc ((↑) ∘ x) a : _ -> M) ->
      exists b : S,
        phi.Realize default (Fin.snoc ((↑) ∘ x) b : _ -> M)

/-- The exact statement-phase target: witness closure implies that the given
substructure is elementary in the ambient structure. -/
def TarskiVaughtTarget : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
      (S : L.Substructure M),
    TarskiVaughtWitnessCondition L M S -> S.IsElementary

/-- A direct spelling using the binders of mathlib's pinned theorem. -/
def PinnedMathlibStatementShape : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
      (S : L.Substructure M),
    (forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> S) (a : M),
      phi.Realize default (Fin.snoc ((↑) ∘ x) a : _ -> M) ->
        exists b : S,
          phi.Realize default (Fin.snoc ((↑) ∘ x) b : _ -> M)) ->
      S.IsElementary

/-- Checked definitional transport to the exact pinned mathlib declaration
shape. -/
theorem tarskiVaughtTarget_iff_pinnedMathlibStatementShape :
    TarskiVaughtTarget.{u, v, w} <-> PinnedMathlibStatementShape.{u, v, w} :=
  Iff.rfl

-- Structural mutations elaborated separately and distinguished by the checker.
def mutationRemovedWitnessHypothesis : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
      (S : L.Substructure M),
    S.IsElementary

def mutationChangedDomainToEmbedding : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M N : Type u)
      [L.Structure M] [L.Structure N] (f : L.Embedding M N),
    (forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> M) (a : N),
      phi.Realize default (Fin.snoc (f ∘ x) a) ->
        exists b : M, phi.Realize default (Fin.snoc (f ∘ x) (f b))) ->
      forall {n : Nat} (phi : L.Formula (Fin n)) (x : Fin n -> M),
        phi.Realize (f ∘ x) <-> phi.Realize x

def mutationChangedBinderScope : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
      (S : L.Substructure M),
    forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> S),
      (forall a : M,
        phi.Realize default (Fin.snoc ((↑) ∘ x) a : _ -> M) ->
          exists b : S,
            phi.Realize default (Fin.snoc ((↑) ∘ x) b : _ -> M)) ->
        S.IsElementary

def mutationPositiveParameterArityOnly : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
      (S : L.Substructure M),
    (forall (n : Nat), 0 < n -> forall (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> S) (a : M),
      phi.Realize default (Fin.snoc ((↑) ∘ x) a : _ -> M) ->
        exists b : S,
          phi.Realize default (Fin.snoc ((↑) ∘ x) b : _ -> M)) ->
      S.IsElementary

/-- The frozen premise includes the parameter-free (`n = 0`) boundary case. -/
theorem nullaryParameterBoundary
    (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
    (S : L.Substructure M) (h : TarskiVaughtWitnessCondition L M S)
    (phi : L.BoundedFormula Empty 1) (x : Fin 0 -> S) (a : M)
    (ha : phi.Realize default (Fin.snoc ((↑) ∘ x) a : _ -> M)) :
    exists b : S,
      phi.Realize default (Fin.snoc ((↑) ∘ x) b : _ -> M) :=
  h 0 phi x a ha

end Stage1Instances.THM_M_0650

set_option pp.explicit true in
#print Stage1Instances.THM_M_0650.TarskiVaughtTarget
