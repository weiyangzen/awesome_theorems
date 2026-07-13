import Mathlib.Combinatorics.Additive.AP.Three.Behrend

/-!
Discovery-only checks for pinned APIs directly relevant to the THM-M-0957 intake.

These checks authenticate names and types. They do not select a canonical source statement, prove
source-to-formal identity, audit the imported terminal body, or grant machine-proof credit.
-/

#check ThreeAPFree
#check threeAPFree_iff_eq_right
#check rothNumberNat
#check rothNumberNat_spec
#check Behrend.sphere
#check Behrend.map
#check Behrend.threeAPFree_sphere
#check Behrend.threeAPFree_image_sphere
#check Behrend.card_sphere_le_rothNumberNat
#check Behrend.roth_lower_bound_explicit
#check Behrend.roth_lower_bound
