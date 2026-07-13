import Mathlib.Computability.PartrecCode

/-!
Discovery-only checks for the two pinned recursion-theorem candidates.

This file deliberately declares no canonical target and no wrapper theorem. The repository source
does not yet determine which formulation belongs to THM-M-0742 or how it differs from THM-M-0743.
-/

namespace Stage1Instances.THM_M_0742

#check Nat.Partrec.Code
#check Nat.Partrec.Code.eval
#check Computable
#check Partrec₂
#check Nat.Partrec.Code.smn
#check Nat.Partrec.Code.fixed_point
#check Nat.Partrec.Code.fixed_point₂

#print axioms Nat.Partrec.Code.fixed_point
#print axioms Nat.Partrec.Code.fixed_point₂

end Stage1Instances.THM_M_0742
