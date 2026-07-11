import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
Elaboration probe for the THM-M-0175 exact-statement blocker.

This checks only the concrete curve predicates currently available in the
pinned environment. It deliberately does not manufacture abstract divisor,
degree, genus, canonical-divisor, or global-section fields and call that
package the Riemann-Roch theorem.
-/

open AlgebraicGeometry

#check Scheme
#check Scheme.Hom
#check Spec
#check Smooth
#check IsProper
#check GeometricallyIntegral

