import Mathlib.Order.Zorn

/-!
# THM-M-0774 statement probes

These propositions expose the unresolved statement choices recorded by the
intake. None is designated as the canonical target.
-/

namespace Stage1Instances.THM_M_0774

universe u

/-- Whole-poset form in which bounding the empty chain entails that the
carrier is nonempty. -/
def WholePosetEmptyChainForm : Prop :=
  forall (alpha : Type u) [PartialOrder alpha],
    (forall c : Set alpha, IsChain (fun x y => x <= y) c -> BddAbove c) ->
      Exists fun m : alpha => IsMax m

/-- Whole-poset form with carrier nonemptiness explicit and only nonempty
chains required to have an upper bound. -/
def WholePosetNonemptyChainForm : Prop :=
  forall (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (forall c : Set alpha,
      IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      Exists fun m : alpha => IsMax m

/-- Subset-relative form; upper bounds are required to remain in the selected
subset, and maximality is relative to that subset. -/
def SubsetRelativeForm : Prop :=
  forall (alpha : Type u) [PartialOrder alpha] (s : Set alpha),
    (forall c : Set alpha, c ⊆ s ->
      IsChain (fun x y => x <= y) c ->
        Exists fun ub : alpha => ub ∈ s ∧ forall z, z ∈ c -> z <= ub) ->
      Exists fun m : alpha => Maximal (fun x => x ∈ s) m

#check WholePosetEmptyChainForm
#check WholePosetNonemptyChainForm
#check SubsetRelativeForm
#check @zorn_le
#check @zorn_le_nonempty
#check @zorn_le₀

end Stage1Instances.THM_M_0774
