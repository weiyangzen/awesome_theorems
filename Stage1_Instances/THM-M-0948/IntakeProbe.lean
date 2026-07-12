import Mathlib.Combinatorics.Additive.Corner.Roth
import Mathlib.Combinatorics.HalesJewett
import Mathlib.Combinatorics.Schnirelmann

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0948 catalog statement.

Schnirelmann density is not an upper-asymptotic-density definition, Roth covers length three only,
and the homothetic-copy theorem assumes a finite coloring. None states or proves the target.
-/

#check schnirelmannDensity
#check ThreeAPFree
#check roth_3ap_theorem_nat
#check rothNumberNat_isLittleO_id
#check Combinatorics.Line.exists_mono_in_high_dimension
#check Combinatorics.exists_mono_homothetic_copy
