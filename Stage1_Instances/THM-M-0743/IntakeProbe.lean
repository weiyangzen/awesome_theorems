import Mathlib.Computability.PartrecCode

/-!
Discovery-only checks for the two pinned recursion-theoretic fixed-point candidates.

This file deliberately declares no canonical target and no wrapper theorem. The repository source
does not yet determine which candidate, if either, belongs to THM-M-0743 rather than THM-M-0742.
-/

namespace Stage1Instances.THM_M_0743

#check Nat.Partrec.Code
#check Nat.Partrec.Code.eval
#check Computable
#check Partrec₂
#check Nat.Partrec.Code.smn
#check Nat.Partrec.Code.fixed_point
#check Nat.Partrec.Code.fixed_point₂

#print axioms Nat.Partrec.Code.fixed_point
#print axioms Nat.Partrec.Code.fixed_point₂

end Stage1Instances.THM_M_0743
