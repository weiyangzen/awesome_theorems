import Mathlib.RingTheory.Polynomial.Basic

/-!
# THM-M-0025 immutable mathlib anchor

This module checks the exact frozen commutative one-variable target against the pinned mathlib
theorem. It supplies anchor-audit evidence only, not an accepted proof-phase or release declaration.
-/

namespace Stage1Instances.THM_M_0025_AnchorAudit

universe u

/-- A literal copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R],
    IsNoetherianRing (Polynomial R)

/-- Exact wrapper over the pinned mathlib terminal theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro R _ _
  exact Polynomial.isNoetherianRing

#check Polynomial.isNoetherianRing
#print Polynomial.isNoetherianRing
#print sorries Polynomial.isNoetherianRing
#print axioms Polynomial.isNoetherianRing
#print axioms exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0025_AnchorAudit
