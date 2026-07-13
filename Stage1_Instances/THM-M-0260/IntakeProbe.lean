import Mathlib.Analysis.Analytic.Composition
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Logic.Function.Conjugate

/-!
# THM-M-0260 discovery-only intake probe

These checks authenticate adjacent pinned analytic, complex unit-disc, and semiconjugacy APIs. They
do not define a Brjuno condition or Siegel disk and do not select or prove a Yoccoz theorem.
-/

#check Complex.UnitDisc
#check Complex.UnitDisc.coe
#check Complex.UnitDisc.norm_lt_one
#check AnalyticAt
#check AnalyticAt.comp
#check Function.Semiconj
#check Function.semiconj_iff_comp_eq
#check Function.Semiconj.trans
