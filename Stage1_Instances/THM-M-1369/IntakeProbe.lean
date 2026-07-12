import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Fourier.AddCircleMulti
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.LinearAlgebra.SymplecticGroup

/-!
# THM-M-1369 discovery-only intake probe

These checks authenticate adjacent pinned analytic, finite-torus Fourier, ODE, flow, and
symplectic-matrix APIs. They do not turn the catalog's KAM-theory topic label into a proposition,
select a KAM variant, or prove THM-M-1369.
-/

#check AnalyticAt
#check UnitAddTorus
#check UnitAddTorus.mFourier
#check IsIntegralCurve
#check Flow
#check Matrix.J
#check Matrix.J_transpose
#check Matrix.symplecticGroup
