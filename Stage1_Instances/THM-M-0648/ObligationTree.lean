import Mathlib.ModelTheory.Satisfiability

/-! Conditional composition certificate for the frozen THM-M-0648 architecture. -/

namespace Stage1Instances.THM_M_0648.ObligationTree

open Cardinal FirstOrder
open CategoryTheory

universe u v wM wK

def Downward (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [Nonempty M] [L.Structure M]
      (A : Set M) (kappa : Cardinal.{wK}),
    aleph0 <= kappa ->
    Cardinal.lift.{wK} #A <= Cardinal.lift.{wM} kappa ->
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wM} kappa <= Cardinal.lift.{wK} #M ->
    exists S : L.ElementarySubstructure M,
      A ⊆ S ∧ Cardinal.lift.{wK} #S = Cardinal.lift.{wM} kappa

def Upward (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [L.Structure M] [Infinite M]
      (kappa : Cardinal.{wK}),
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wK} #M <= Cardinal.lift.{wM} kappa ->
    exists N : Bundled L.Structure, Nonempty (M ↪ₑ[L] N) ∧ #N = kappa

def Root (L : Language.{u, v}) : Prop :=
  Downward.{u, v, wM, wK} L ∧ Upward.{u, v, wM, wK} L

/-- Consumes both exact direction packages. It proves neither package. -/
theorem root_compose (L : Language.{u, v})
    (downward : Downward.{u, v, wM, wK} L)
    (upward : Upward.{u, v, wM, wK} L) :
    Root.{u, v, wM, wK} L :=
  ⟨downward, upward⟩

theorem root_exact_type (L : Language.{u, v}) :
    Root.{u, v, wM, wK} L =
      (Downward.{u, v, wM, wK} L ∧ Upward.{u, v, wM, wK} L) :=
  rfl

#print axioms root_compose

end Stage1Instances.THM_M_0648.ObligationTree
