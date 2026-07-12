import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Analysis.ODE.Basic

/-!
# THM-M-1380 discovery-only intake probe

These checks authenticate pinned generic interfaces adjacent to possible Hamilton-Jacobi
encodings. They do not define a complete integral, select a Jacobi theorem, state the
Hamilton-Jacobi equation, or prove any part of THM-M-1380.
-/

#check ContDiff
#check HasFDerivAt
#check fderiv
#check ContinuousLinearMap
#check ContinuousLinearMap.fst
#check ContinuousLinearMap.snd
#check IsIntegralCurve
