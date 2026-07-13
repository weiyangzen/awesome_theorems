import Mathlib.Analysis.Complex.CanonicalDecomposition
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0251 discovery-only intake probe

These checks authenticate pinned APIs adjacent to a possible Hardy-space inner-outer
factorization statement. They do not define a Hardy space, inner function, outer function,
boundary-value convention, canonical factorization target, or proof of THM-M-0251.
-/

#check Complex.UnitDisc
#check AnalyticOnNhd
#check MeasureTheory.MemLp
#check Complex.canonicalFactor
#check Complex.meromorphicOn_canonicalFactor
#check Complex.analyticOnNhd_canonicalFactor
#check Complex.canonicalFactor_ne_zero
#check Complex.norm_canonicalFactor_eval_circle_eq_one

#print axioms Complex.meromorphicOn_canonicalFactor
#print axioms Complex.norm_canonicalFactor_eval_circle_eq_one
