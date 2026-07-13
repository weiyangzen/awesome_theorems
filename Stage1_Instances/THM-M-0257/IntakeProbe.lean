import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Calculus.Conformal.NormedSpace
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.ConformalGroupoid
import Mathlib.GroupTheory.GroupAction.Defs

/-!
# THM-M-0257 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for complex analyticity, conformal maps,
complex manifolds, group actions, and quotients. They do not define Beltrami coefficients,
quasiconformal maps, marked Riemann surfaces, Teichmuller space, or the Ahlfors-Bers theorem.
-/

#check AnalyticAt
#check ModelWithCorners
#check ChartedSpace
#check IsManifold
#check MDifferentiable
#check Homeomorph
#check IsConformalMap
#check ConformalAt
#check conformalGroupoid
#check MulAction.orbitRel
#check MulAction.orbitRel.Quotient
#check Quotient.mk
