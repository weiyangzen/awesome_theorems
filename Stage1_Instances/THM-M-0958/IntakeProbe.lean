import Mathlib.Combinatorics.Additive.AP.Three.Behrend

/-!
# THM-M-0958 discovery-only intake probe

These checks authenticate pinned three-term-progression, extremal-number, interval-translation,
and Behrend-bound interfaces. The checked Behrend result is weaker than Elkin's improvement. This
file does not select, state, or prove the THM-M-0958 target.
-/

#check ThreeAPFree
#check threeAPFree_iff_eq_right
#check rothNumberNat
#check rothNumberNat_spec
#check addRothNumber_Ico
#check Behrend.card_sphere_le_rothNumberNat
#check Behrend.roth_lower_bound
