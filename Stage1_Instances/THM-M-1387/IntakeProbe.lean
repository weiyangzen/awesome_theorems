import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Data.Set.Finite.Basic

/-!
# THM-M-1387 discovery-only intake probe

These checks authenticate adjacent pinned solution, derivative, infinity, and filter APIs. They do
not define ODE oscillation, select the catalog's exact statement, or prove THM-M-1387.
-/

#check IsIntegralCurveOn
#check IsIntegralCurve
#check HasDerivAt
#check iteratedDeriv
#check Set.Infinite
#check Filter.Frequently
#check Filter.atTop
