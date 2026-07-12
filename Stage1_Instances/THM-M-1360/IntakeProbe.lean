import Mathlib.Algebra.Ring.Periodic
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Analysis.CStarAlgebra.Spectrum

/-!
# THM-M-1360 discovery-only intake probe

These checks authenticate adjacent pinned periodicity, ODE, flow, differentiability, eigenvalue,
and spectrum APIs. They do not select a Hopf-bifurcation variant, define a critical spectral
crossing or periodic branch, or prove THM-M-1360.
-/

#check Function.Periodic
#check IsIntegralCurve
#check IsIntegralCurveAt
#check Flow
#check ContDiff
#check HasFDerivAt
#check Module.End.HasEigenvalue
#check Module.End.HasEigenvalue.mem_spectrum
#check spectrum
