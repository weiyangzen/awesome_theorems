import Mathlib.AlgebraicGeometry.RationalMap

/-!
# THM-M-0121 statement-gate boundary

The repository source does not identify one exact proposition behind the label
"Mori rationality theorem" and the gloss "rationality of Fano varieties".
This module therefore checks only the smallest pinned rational-map substrate
already justified by the intake. It intentionally declares no canonical target:
choosing nef-threshold rationality, rational curves or uniruledness, rational
connectedness, or unqualified birational rationality would substitute a claim.
-/

open AlgebraicGeometry

universe u

namespace Stage1Instances.THM_M_0121

#check Scheme.RationalMap
#check Scheme.RationalMap.domain
#check Scheme.RationalMap.equivFunctionField

end Stage1Instances.THM_M_0121
