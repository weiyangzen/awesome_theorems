import Mathlib.Combinatorics.Additive.Corner.Roth
import Mathlib.GroupTheory.FiniteAbelian.Basic

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0961 catalog statement.

The declarations below concern three-term-progression predicates and Roth-type qualitative density
bounds. They do not state the quantitative 1995 Meshulam cap-set bound, and this file declares no
target theorem.
-/

#check ThreeAPFree
#check addRothNumber
#check AddCommGroup.equiv_directSum_zmod_of_finite'
#check cornersTheoremBound
#check roth_3ap_theorem
#check roth_3ap_theorem_nat
#check rothNumberNat_isLittleO_id
