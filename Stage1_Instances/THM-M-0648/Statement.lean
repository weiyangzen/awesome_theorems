import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0648: upward and downward Loewenheim-Skolem statement

This module freezes the paired first-order target. It states both directions and contains no proof
of either direction.
-/

namespace Stage1Instances.THM_M_0648

open Cardinal FirstOrder
open CategoryTheory

universe u v wM wK

/-- Downward Loewenheim-Skolem, including a distinguished subset and exact cardinality. -/
def DownwardTarget (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [Nonempty M] [L.Structure M]
      (A : Set M) (kappa : Cardinal.{wK}),
    aleph0 <= kappa ->
    Cardinal.lift.{wK} #A <= Cardinal.lift.{wM} kappa ->
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wM} kappa <= Cardinal.lift.{wK} #M ->
    exists S : L.ElementarySubstructure M,
      A ⊆ S ∧ Cardinal.lift.{wK} #S = Cardinal.lift.{wM} kappa

/-- Upward Loewenheim-Skolem, encoded by an elementary embedding into an exact-size model. -/
def UpwardTarget (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [L.Structure M] [Infinite M]
      (kappa : Cardinal.{wK}),
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wK} #M <= Cardinal.lift.{wM} kappa ->
    exists N : Bundled L.Structure, Nonempty (M ↪ₑ[L] N) ∧ #N = kappa

/-- The canonical paired target: neither direction alone closes this declaration. -/
def CanonicalTarget (L : Language.{u, v}) : Prop :=
  DownwardTarget.{u, v, wM, wK} L ∧ UpwardTarget.{u, v, wM, wK} L

/-- Checked direct expansion of the paired target. -/
theorem canonicalTarget_iff_expanded (L : Language.{u, v}) :
    CanonicalTarget.{u, v, wM, wK} L ↔
      DownwardTarget.{u, v, wM, wK} L ∧ UpwardTarget.{u, v, wM, wK} L :=
  Iff.rfl

-- Separately elaborated mutations guard the statement boundary.
def mutationDownwardOnly (L : Language.{u, v}) : Prop :=
  DownwardTarget.{u, v, wM, wK} L

def mutationRemovedDistinguishedSet (L : Language.{u, v}) : Prop :=
  forall (M : Type wM) [Nonempty M] [L.Structure M]
      (kappa : Cardinal.{wK}),
    aleph0 <= kappa ->
    Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
    Cardinal.lift.{wM} kappa <= Cardinal.lift.{wK} #M ->
    exists S : L.ElementarySubstructure M,
      Cardinal.lift.{wK} #S = Cardinal.lift.{wM} kappa

def mutationUpwardEquivalentModelOnly (L : Language.{u, v}) : Prop :=
  DownwardTarget.{u, v, wM, wK} L ∧
    forall (M : Type wM) [L.Structure M] [Infinite M]
        (kappa : Cardinal.{wK}),
      Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa ->
      Cardinal.lift.{wK} #M <= Cardinal.lift.{wM} kappa ->
      exists N : Bundled L.Structure, (M ≅[L] N) ∧ #N = kappa

end Stage1Instances.THM_M_0648

set_option pp.explicit true in
#print Stage1Instances.THM_M_0648.CanonicalTarget
