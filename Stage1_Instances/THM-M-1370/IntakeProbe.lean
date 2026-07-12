import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Fourier.AddCircleMulti
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.LinearAlgebra.SymplecticGroup

/-!
# THM-M-1370 discovery-only intake probe

These checks authenticate adjacent pinned analytic, finite-torus Fourier, ODE, flow, and
symplectic-matrix APIs. They do not select a KAM variant, define its arithmetic and perturbation
contract, or prove THM-M-1370.
-/

#check AnalyticAt
#check UnitAddTorus
#check UnitAddTorus.mFourier
#check IsIntegralCurve
#check Flow
#check Matrix.J
#check Matrix.J_transpose
#check Matrix.symplecticGroup
