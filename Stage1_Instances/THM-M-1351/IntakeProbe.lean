import Mathlib.Analysis.Calculus.Implicit
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.PeriodicPts.Defs

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-1351 catalog wording.

These declarations do not construct a transverse section, first-return time, or Poincare map and do
not state any orbit/fixed-point stability theorem. They supply no statement or proof credit.
-/

#check Flow
#check Flow.orbit
#check IsIntegralCurve
#check Function.IsFixedPt
#check Function.IsPeriodicPt
#check HasFDerivAt
#check ImplicitFunctionData.implicitFunction
