import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Sites.ElladicCohomology

/-!
Pinned-environment substrate probe for the THM-M-0192 exact-statement blocker.

This checks only the available scheme, smooth/proper-morphism, and integral ell-adic cohomology
interfaces. It is not Deligne's theorem: the pinned API does not provide the required rational
ell-adic cohomology Frobenius action, eigenvalues, or weight predicate.
-/

#check AlgebraicGeometry.Scheme
#check AlgebraicGeometry.Smooth
#check AlgebraicGeometry.IsProper
#check AlgebraicGeometry.Scheme.EllAdicCohomology

