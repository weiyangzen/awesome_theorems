import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Calculus.FDeriv.CompCLM

/-!
# THM-M-1341 discovery-only intake probe

These checks authenticate pinned integral-curve, derivative, Frechet-derivative, and
continuous-linear-map interfaces adjacent to a future sensitivity-equation encoding. They do not
select the catalog's exact statement, define a solution map, or prove THM-M-1341.
-/

#check IsIntegralCurve
#check IsIntegralCurveAt.hasDerivAt
#check HasDerivAt
#check HasFDerivAt
#check fderiv
#check ContinuousLinearMap
#check ContinuousLinearMap.comp
#check HasFDerivAt.comp
#check HasFDerivAt.clm_apply
