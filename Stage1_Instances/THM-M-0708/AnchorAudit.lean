import Mathlib.Computability.Halting

/-!
# THM-M-0708 anchor audit

This module checks that the pinned mathlib declaration `Nat.Partrec.Code.rice`
has enough strength to close the separately frozen target.  It is candidate
evidence for the anchor-audit node, not the proof-node deliverable.
-/

namespace Stage1Instances.THM_M_0708.AnchorAudit

open Nat.Partrec (Code)
open Nat.Partrec.Code

def FrozenTarget : Prop :=
  forall C : Set (Nat →. Nat),
    (exists f : Nat →. Nat, Nat.Partrec f /\ f ∈ C) ->
    (exists g : Nat →. Nat, Nat.Partrec g /\ g ∉ C) ->
    Not (ComputablePred fun c : Code => eval c ∈ C)

/-- Exact-type feasibility wrapper around the pinned mathlib Rice theorem. -/
theorem mathlib_rice_exact_candidate : FrozenTarget := by
  intro C ⟨f, hf, fC⟩ ⟨g, hg, gC⟩ hdec
  exact gC (ComputablePred.rice C hdec hf hg fC)

end Stage1Instances.THM_M_0708.AnchorAudit

#check ComputablePred.rice
#print axioms ComputablePred.rice
#print axioms Stage1Instances.THM_M_0708.AnchorAudit.mathlib_rice_exact_candidate
