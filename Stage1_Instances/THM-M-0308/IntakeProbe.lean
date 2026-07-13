import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0308 discovery-only intake probe

These checks authenticate adjacent pinned `L^p`, continuous-linear-map, and Sobolev-inequality
interfaces. They do not select, state, or prove a Sobolev extension theorem.
-/

#check MeasureTheory.Lp
#check MeasureTheory.MemLp
#check ContinuousLinearMap
#check ContinuousLinearMap.id
#check ContinuousLinearMap.comp
#check ContinuousLinearMap.le_opNorm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le
