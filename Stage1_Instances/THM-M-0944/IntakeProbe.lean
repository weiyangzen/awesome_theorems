import Mathlib.Combinatorics.Additive.ApproximateSubgroup
import Mathlib.Combinatorics.Additive.DoublingConst
import Mathlib.Combinatorics.Additive.Energy
import Mathlib.Combinatorics.Additive.RuzsaCovering

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0944
catalog claim. These declarations do not state or prove a BSG theorem.
-/

open scoped Combinatorics.Additive Pointwise

#check Finset.addEnergy
#check Finset.addConst
#check IsApproximateAddSubgroup
#check Finset.ruzsa_covering_add
#check Finset.card_sq_le_card_mul_addEnergy
#check Finset.addConst_le_inv_dens
