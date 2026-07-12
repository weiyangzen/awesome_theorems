import Mathlib.Order.Zorn

/-!
# THM-M-0770 anchor audit

This module checks the exact canonical statement against the immutable mathlib
dependency. It records an anchor/wrapper candidate, not release completion.
-/

namespace Stage1Instances.THM_M_0770.AnchorAudit

universe u

/-- The canonical statement, repeated here so this audit has one narrow import. -/
def CanonicalTarget : Prop :=
  forall (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (forall c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      Exists fun m : alpha => IsMax m

/-- Exact checked wrapper around pinned mathlib's nonempty-chain variant. -/
theorem canonical_of_pinned_mathlib : CanonicalTarget.{u} := by
  intro alpha _ _ h
  exact zorn_le_nonempty h

end Stage1Instances.THM_M_0770.AnchorAudit

#check @zorn_le_nonempty
#print axioms zorn_le_nonempty
#print axioms Stage1Instances.THM_M_0770.AnchorAudit.canonical_of_pinned_mathlib
