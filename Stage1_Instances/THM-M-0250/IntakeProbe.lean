import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Complex.MeanValue

/-!
Discovery-only checks for pinned interfaces adjacent to the ambiguous THM-M-0250 catalog phrase.

These declarations provide a unit-disc model, complex analyticity, circle integration and a
mean-value result. They do not define a Hardy space, choose an exponent or radial norm, state a
source-selected theorem, or supply proof credit.
-/

#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#check AnalyticOnNhd
#check Real.circleAverage
#check CircleIntegrable
#check DiffContOnCl.circleAverage
