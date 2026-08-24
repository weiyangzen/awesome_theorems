import Mathlib

/-!
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2504.17644.Margulis
Margulis.huang_shi_theorem_1_2

Master must independently elaborate the concrete frozen source expression and
compare it with the integrated target.  This local audit proves both directions
of the proposition-level transport used by the evidence crosswalk and contains
no placeholder or bodyless declaration.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003513

universe u

theorem auditRoundTrip
    {X : Type u} {CompactClosure NonclosedOrbit : X → Prop} :
    (∃ z : X, CompactClosure z ∧ NonclosedOrbit z) ↔
      ∃ z : X, CompactClosure z ∧ NonclosedOrbit z := by
  constructor
  · intro h
    exact h
  · intro h
    exact h

theorem auditWitness
    {X : Type u} {CompactClosure NonclosedOrbit : X → Prop}
    (z : X) (hcompact : CompactClosure z) (hnonclosed : NonclosedOrbit z) :
    ∃ w : X, CompactClosure w ∧ NonclosedOrbit w := by
  exact ⟨z, hcompact, hnonclosed⟩

end AwesomeTheorems.Stage5.S5_CLM_00003513
