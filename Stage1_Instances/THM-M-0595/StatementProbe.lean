import Mathlib.Geometry.Manifold.SmoothApprox

/-!
Elaboration probe for the THM-M-0595 exact-statement blocker.

This checks the closest pinned mathlib formulation of the theorem family. It is
not declared as the canonical target because the repository source does not fix
its domain, codomain, approximation notion, or relative/support conclusions.
-/

#check Continuous.exists_contMDiff_approx
#check Continuous.exists_contDiff_approx

