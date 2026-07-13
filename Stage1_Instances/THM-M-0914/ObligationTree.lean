import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0914 conditional obligation composition

This module checks the child-to-parent interfaces selected by the frozen
obligation architecture. Imported theorem bodies remain abstract premises at
the composition boundaries, so this phase does not install the audited mathlib
candidate as an accepted root proof.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0914_ObligationTree

universe u v

/-- Literal copy of the already-frozen canonical proposition. -/
def Root : Prop :=
  forall (n : Nat) (f : Fin (n + 1) -> Fin n),
    exists x y, x ≠ y /\ f x = f y

/-- The cardinal arithmetic premise needed by the finite-type wrapper. -/
def CardFinPackage : Prop :=
  forall n : Nat, Fintype.card (Fin n) < Fintype.card (Fin (n + 1))

/-- The concrete `Fin` cardinal identity used in that normalization. -/
def FinCardIdentity : Prop :=
  forall n : Nat, Fintype.card (Fin n) = n

/-- The arithmetic inequality remaining after cardinality normalization. -/
def NatSuccessorInequality : Prop :=
  forall n : Nat, n < n + 1

/-- The exact polymorphic interface exported by the shallow finite-type wrapper. -/
def FintypeCollisionPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [Fintype alpha] [Fintype beta]
    (f : alpha -> beta),
    Fintype.card beta < Fintype.card alpha ->
      exists x y, x ≠ y /\ f x = f y

/-- The exact finite-set interface implemented by the substantive terminal body. -/
def FinsetCollisionPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} {s : Finset alpha} {t : Finset beta},
    t.card < s.card ->
    forall {f : alpha -> beta}, Set.MapsTo f (s : Set alpha) (t : Set beta) ->
      exists x, x ∈ s /\ exists y, y ∈ s /\ x ≠ y /\ f x = f y

/-- The cardinal monotonicity bridge used by the finite-set terminal body. -/
def FinsetCardInjOnBound : Prop :=
  forall {alpha : Type u} {beta : Type v} (s : Finset alpha) (t : Finset beta)
    (f : alpha -> beta), Set.MapsTo f (s : Set alpha) (t : Set beta) ->
      Set.InjOn f (s : Set alpha) -> s.card <= t.card

/-- Negating the requested collision gives injectivity on the finite source. -/
def NoCollisionImpliesInjOn : Prop :=
  forall {alpha : Type u} {beta : Type v} (s : Finset alpha) (f : alpha -> beta),
    (Not (exists x, x ∈ s /\ exists y, y ∈ s /\ x ≠ y /\ f x = f y)) ->
      Set.InjOn f (s : Set alpha)

/-- Checked `Fin` cardinality identity. -/
theorem finCardIdentity_checked : FinCardIdentity := by
  intro n
  exact Fintype.card_fin n

/-- Checked successor inequality. -/
theorem natSuccessorInequality_checked : NatSuccessorInequality := by
  intro n
  exact Nat.lt_add_one n

/-- Checked composition of both cardinality-normalization children. -/
theorem cardFinPackage_of_identity_and_successor
    (identity : FinCardIdentity)
    (successor : NatSuccessorInequality) : CardFinPackage := by
  intro n
  rw [identity n, identity (n + 1)]
  exact successor n

/-- The local checked realization of the concrete cardinal arithmetic package. -/
theorem cardFinPackage : CardFinPackage :=
  cardFinPackage_of_identity_and_successor
    finCardIdentity_checked natSuccessorInequality_checked

/-- Checked logical conversion used by the terminal contradiction proof. -/
theorem noCollisionImpliesInjOn_checked : NoCollisionImpliesInjOn.{u, v} := by
  intro alpha beta s f hNoCollision x hx y hy hxy
  by_contra hne
  exact hNoCollision ⟨x, hx, y, hy, hne, hxy⟩

/-- Checked terminal composition retaining both material children as premises. -/
theorem finsetCollisionPackage_of_cardBound_and_noCollision
    (cardBound : FinsetCardInjOnBound.{u, v})
    (noCollision : NoCollisionImpliesInjOn.{u, v}) :
    FinsetCollisionPackage.{u, v} := by
  intro alpha beta s t hCard f hMaps
  by_contra hCollision
  exact (Nat.not_le_of_lt hCard)
    (cardBound s t f hMaps (noCollision s f hCollision))

/-- Checked universe-membership normalization for an arbitrary total map. -/
theorem univMapsTo_checked
    {alpha : Type u} {beta : Type v} [Fintype alpha] [Fintype beta]
    (f : alpha -> beta) :
    Set.MapsTo f ((Finset.univ : Finset alpha) : Set alpha)
      ((Finset.univ : Finset beta) : Set beta) := by
  intro x hx
  exact Finset.mem_univ (f x)

/-- Checked wrapper composition from the terminal finite-set package. -/
theorem fintypePackage_of_finsetPackage
    (terminal : FinsetCollisionPackage.{u, v}) : FintypeCollisionPackage.{u, v} := by
  intro alpha beta _ _ f hcard
  obtain ⟨x, _, y, _, hxy, hmap⟩ :=
    terminal (alpha := alpha) (beta := beta)
      (s := Finset.univ) (t := Finset.univ)
      (by simpa only [Finset.card_univ] using hcard)
      (f := f) (univMapsTo_checked f)
  exact ⟨x, y, hxy, hmap⟩

/-- Checked specialization from the general package to the concrete root. -/
theorem root_of_fintypePackage
    (wrapper : FintypeCollisionPackage.{0, 0})
    (cardFin : CardFinPackage) : Root := by
  intro n f
  exact wrapper f (cardFin n)

/-- Checked route composition retaining the terminal package as an open premise. -/
theorem root_of_finsetPackage
    (terminal : FinsetCollisionPackage.{0, 0}) : Root := by
  exact root_of_fintypePackage
    (fintypePackage_of_finsetPackage terminal) cardFinPackage

/-- Candidate adapters identify pinned declarations but are not consumed above. -/
theorem pinnedFintypeCandidate : FintypeCollisionPackage.{u, v} := by
  intro alpha beta _ _ f hcard
  exact Fintype.exists_ne_map_eq_of_card_lt f hcard

theorem pinnedFinsetCandidate : FinsetCollisionPackage.{u, v} := by
  intro alpha beta s t hcard f hMapsTo
  exact Finset.exists_ne_map_eq_of_card_lt_of_maps_to hcard hMapsTo

assert_no_sorry cardFinPackage
assert_no_sorry finCardIdentity_checked
assert_no_sorry natSuccessorInequality_checked
assert_no_sorry cardFinPackage_of_identity_and_successor
assert_no_sorry noCollisionImpliesInjOn_checked
assert_no_sorry finsetCollisionPackage_of_cardBound_and_noCollision
assert_no_sorry univMapsTo_checked
assert_no_sorry fintypePackage_of_finsetPackage
assert_no_sorry root_of_fintypePackage
assert_no_sorry root_of_finsetPackage
assert_no_sorry pinnedFintypeCandidate
assert_no_sorry pinnedFinsetCandidate

#print sorries cardFinPackage
#print sorries finCardIdentity_checked
#print sorries natSuccessorInequality_checked
#print sorries cardFinPackage_of_identity_and_successor
#print sorries noCollisionImpliesInjOn_checked
#print sorries finsetCollisionPackage_of_cardBound_and_noCollision
#print sorries univMapsTo_checked
#print sorries fintypePackage_of_finsetPackage
#print sorries root_of_fintypePackage
#print sorries root_of_finsetPackage
#print sorries pinnedFintypeCandidate
#print sorries pinnedFinsetCandidate

#print axioms cardFinPackage
#print axioms finCardIdentity_checked
#print axioms natSuccessorInequality_checked
#print axioms cardFinPackage_of_identity_and_successor
#print axioms noCollisionImpliesInjOn_checked
#print axioms finsetCollisionPackage_of_cardBound_and_noCollision
#print axioms univMapsTo_checked
#print axioms fintypePackage_of_finsetPackage
#print axioms root_of_fintypePackage
#print axioms root_of_finsetPackage
#print axioms pinnedFintypeCandidate
#print axioms pinnedFinsetCandidate

open Lean Elab Command in
elab "#print_obligation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0914_ObligationTree.cardFinPackage,
    ``Stage1Instances.THM_M_0914_ObligationTree.finCardIdentity_checked,
    ``Stage1Instances.THM_M_0914_ObligationTree.natSuccessorInequality_checked,
    ``Stage1Instances.THM_M_0914_ObligationTree.cardFinPackage_of_identity_and_successor,
    ``Stage1Instances.THM_M_0914_ObligationTree.noCollisionImpliesInjOn_checked,
    ``Stage1Instances.THM_M_0914_ObligationTree.finsetCollisionPackage_of_cardBound_and_noCollision,
    ``Stage1Instances.THM_M_0914_ObligationTree.univMapsTo_checked,
    ``Stage1Instances.THM_M_0914_ObligationTree.fintypePackage_of_finsetPackage,
    ``Stage1Instances.THM_M_0914_ObligationTree.root_of_fintypePackage,
    ``Stage1Instances.THM_M_0914_ObligationTree.root_of_finsetPackage
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
  logInfo m!"OBLIGATION_CLOSURE declarations={closure.size}"
  logInfo m!"OBLIGATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"OBLIGATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"OBLIGATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_obligation_closure

set_option pp.universes true in
set_option pp.explicit true in
#print Root

end Stage1Instances.THM_M_0914_ObligationTree
