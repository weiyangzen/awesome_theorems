import Statement
import Mathlib.FieldTheory.Finite.Basic

/-!
# THM-M-0474 conditional obligation composition

This module checks only the child-to-root interface frozen by the obligation registry. The exact
mathlib theorem remains an explicit premise; installing it as the canonical proof belongs to the
later proof phase.
-/

namespace Stage1Instances.THM_M_0474.ObligationTree

/-- Exact conclusion exposed by the audited pinned `Nat.ModEq` theorem. -/
def ExactNatAnchor : Prop :=
  forall (p a : Nat), p.Prime -> a.Coprime p ->
    a ^ (p - 1) ≡ 1 [MOD p]

/-- Conditional child-to-root composition. It consumes the exact child and introduces no premise. -/
theorem root_of_exactNatAnchor
    (anchor : ExactNatAnchor) :
    Stage1Instances.THM_M_0474.FermatLittleTheoremTarget := by
  exact anchor

#check Nat.ModEq.pow_card_sub_one_eq_one
#print axioms root_of_exactNatAnchor

end Stage1Instances.THM_M_0474.ObligationTree
