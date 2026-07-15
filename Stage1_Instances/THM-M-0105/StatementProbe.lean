import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic

/-!
# THM-M-0105 pinned statement-surface probe

This file checks only adjacent pinned interfaces. It is not the canonical
Riemann--Roch target: the pinned snapshot does not expose the required
algebraic-curve divisor, canonical-divisor, divisor-sheaf, degree, or genus
interfaces.
-/

open CategoryTheory AlgebraicGeometry

#check Scheme
#check Spec
#check Smooth
#check IsProper
#check GeometricallyIntegral
#check Scheme.Modules
#check Scheme.Modules.presheaf
#check Sheaf.H
#check Module.finrank
