import Mathlib.Order.Zorn

/-!
# THM-M-0770: exact Zorn's lemma statement

This module freezes and tests the statement boundary only. It does not use the
mathlib proof of Zorn's lemma to prove the target.
-/

namespace Stage1Instances.THM_M_0770

universe u

/-- The nonempty-poset formulation of Zorn's lemma selected by the intake.
Every nonempty chain has an upper bound, and the conclusion is an order-theoretic
maximal element, not a greatest element. -/
def ZornsLemmaTarget : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, IsMax m

/-- Direct local copy of the type of pinned mathlib's `zorn_le_nonempty`, with
the stronger `PartialOrder` selected by the human theorem boundary. -/
def PinnedMathlibSourceShape : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, IsMax m

/-- Checked identity with the locally copied pinned declaration shape. -/
theorem zornsLemmaTarget_iff_pinnedMathlibSourceShape :
    ZornsLemmaTarget.{u} <-> PinnedMathlibSourceShape.{u} :=
  Iff.rfl

/-- In a partial order, mathlib's `IsMax` is equivalent to saying that every
element above `m` equals `m`. -/
theorem isMax_iff_no_strictly_larger {alpha : Type u} [PartialOrder alpha] (m : alpha) :
    IsMax m <-> ∀ a : alpha, m <= a -> a = m := by
  constructor
  · intro hm a hma
    exact le_antisymm (hm hma) hma
  · intro hm a hma
    exact (hm a hma).le

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationAllowsEmptyCarrier : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, IsMax m

def mutationUsesPreorder : Prop :=
  ∀ (alpha : Type u) [Preorder alpha] [Nonempty alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, IsMax m

def mutationBoundsEmptyChain : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> BddAbove c) ->
      ∃ m : alpha, IsMax m

def mutationRequiresGreatestElement : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, ∀ a : alpha, a <= m

/-- Omitting carrier nonemptiness is genuinely invalid: the chain premise is
vacuous on `Empty`, while the conclusion would construct an element. -/
theorem mutationAllowsEmptyCarrier_is_false :
    ¬ mutationAllowsEmptyCarrier.{0} := by
  intro h
  have impossible := h Empty (fun c _hc hc => by
    obtain ⟨x, _hx⟩ := hc
    exact Empty.elim x)
  obtain ⟨m, _hm⟩ := impossible
  exact Empty.elim m

/-- The selected maximality predicate specializes to the expected equality
form on a singleton carrier. -/
theorem singleton_maximal_boundary :
    IsMax (PUnit.unit : PUnit) := by
  intro a _ha
  exact le_rfl

end Stage1Instances.THM_M_0770

set_option pp.explicit true in
#print Stage1Instances.THM_M_0770.ZornsLemmaTarget
