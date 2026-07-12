import Mathlib.ModelTheory.Satisfiability

/-! Repo-local proof closure for the frozen THM-M-0648 target. -/

namespace Stage1Instances.THM_M_0648

open Cardinal FirstOrder
open CategoryTheory

universe u v wM wK

def DownwardTarget (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [Nonempty M] [L.Structure M]
      (A : Set M) (kappa : Cardinal.{wK}),
    aleph0 <= kappa ->
    Cardinal.lift.{wK} #A <= Cardinal.lift.{wM} kappa ->
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wM} kappa <= Cardinal.lift.{wK} #M ->
    exists S : L.ElementarySubstructure M,
      A ⊆ S ∧ Cardinal.lift.{wK} #S = Cardinal.lift.{wM} kappa

def UpwardTarget (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [L.Structure M] [Infinite M]
      (kappa : Cardinal.{wK}),
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wK} #M <= Cardinal.lift.{wM} kappa ->
    exists N : Bundled L.Structure, Nonempty (M ↪ₑ[L] N) ∧ #N = kappa

def CanonicalTarget (L : Language.{u, v}) : Prop :=
  DownwardTarget.{u, v, wM, wK} L ∧ UpwardTarget.{u, v, wM, wK} L

/-- Both exact directions, discharged by the pinned mathlib proof bodies. -/
theorem canonicalTarget (L : Language.{u, v}) :
    CanonicalTarget.{u, v, wM, wK} L := by
  constructor
  · intro M _ _ A kappa hInfinite hA hL hM
    exact L.exists_elementarySubstructure_card_eq A kappa hInfinite hA hL hM
  · intro M _ _ kappa hL hM
    exact L.exists_elementaryEmbedding_card_eq_of_ge M kappa hL hM

#print axioms canonicalTarget

end Stage1Instances.THM_M_0648
