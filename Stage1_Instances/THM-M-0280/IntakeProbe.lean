import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.Analysis.MeanInequalities

/-!
# THM-M-0280 discovery-only intake probe

These checks authenticate pinned mathlib interfaces for several distinct meanings of
"the triangle inequality in L^p space": the extended seminorm on measurable functions, the
real-valued `lpNorm`, the normed quotient `Lp`, an explicit nonnegative integral formula, and a
finite-sum variant. They do not select a canonical source statement or claim proof credit.
-/

#check MeasureTheory.eLpNorm_add_le
#print axioms MeasureTheory.eLpNorm_add_le

#check MeasureTheory.lpNorm_add_le
#print axioms MeasureTheory.lpNorm_add_le

#check MeasureTheory.Lp.instNormedAddCommGroup

#check ENNReal.lintegral_Lp_add_le
#print axioms ENNReal.lintegral_Lp_add_le

#check Real.Lp_add_le
#print axioms Real.Lp_add_le
