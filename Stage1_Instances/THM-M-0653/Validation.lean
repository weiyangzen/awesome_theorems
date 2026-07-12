import Statement

/-!
# THM-M-0653 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the two proof-phase claims directly against the frozen statement.
It does not supply the open implicit-to-explicit Beth direction.
-/

namespace Stage1.THM_M_0653.Validation

open FirstOrder FirstOrder.Language FirstOrder.Language.Structure

universe u v w

theorem explicitToImplicitDirect (L : Language.{u, v}) (n : Nat)
    (T : (Expanded L n).Theory) :
    ExplicitlyDefines.{w, u, v} L n T -> ImplicitlyDefines.{w, u, v} L n T := by
  rintro ⟨phi, hphi⟩ M hM s1 s2 hs1 hs2 hreduct x
  rw [hphi M hM s1 hs1 x, hphi M hM s2 hs2 x, hreduct]

theorem conditionalRootDirect (L : Language.{u, v}) (n : Nat)
    (T : (Expanded L n).Theory)
    (hBeth : ImplicitlyDefines.{w, u, v} L n T ->
      ExplicitlyDefines.{w, u, v} L n T) :
    BethDefinabilityTarget.{u, v, w} L n T := by
  exact ⟨hBeth, explicitToImplicitDirect L n T⟩

#check explicitToImplicitDirect
#print axioms explicitToImplicitDirect
#check conditionalRootDirect
#print axioms conditionalRootDirect

end Stage1.THM_M_0653.Validation
