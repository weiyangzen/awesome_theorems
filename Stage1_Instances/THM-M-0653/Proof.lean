import Statement

/-!
# THM-M-0653 proved proof units

This module contains only unconditional proof bodies.  In particular, it does
not postulate the Craig interpolation/Beth direction which is absent from the
pinned dependency closure.
-/

namespace Stage1.THM_M_0653

open FirstOrder FirstOrder.Language FirstOrder.Language.Structure

universe u v w

/-- A uniform old-language definition forces uniqueness of the distinguished
relation on any two expansions with the same reduct. -/
theorem explicitToImplicit (L : Language.{u, v}) (n : Nat)
    (T : (Expanded L n).Theory) :
    ExplicitlyDefines.{w, u, v} L n T -> ImplicitlyDefines.{w, u, v} L n T := by
  rintro ⟨phi, hphi⟩ M hM s1 s2 hs1 hs2 hreduct x
  have h1 := hphi M hM s1 hs1 x
  have h2 := hphi M hM s2 hs2 x
  rw [h1, h2, hreduct]

/-- Exact-root assembly from the still-open Beth direction and the proved
elementary converse.  The open direction is visible in the theorem type and
therefore receives no proof credit from this composition lemma. -/
theorem bethDefinability_of_implicitToExplicit (L : Language.{u, v}) (n : Nat)
    (T : (Expanded L n).Theory)
    (hBeth : ImplicitlyDefines.{w, u, v} L n T ->
      ExplicitlyDefines.{w, u, v} L n T) :
    BethDefinabilityTarget.{u, v, w} L n T := by
  change ImplicitlyDefines L n T <-> ExplicitlyDefines L n T
  exact ⟨hBeth, explicitToImplicit L n T⟩

#check explicitToImplicit
#print axioms explicitToImplicit
#check bethDefinability_of_implicitToExplicit
#print axioms bethDefinability_of_implicitToExplicit

end Stage1.THM_M_0653
