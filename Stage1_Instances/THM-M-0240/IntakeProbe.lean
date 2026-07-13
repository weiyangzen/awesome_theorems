import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
# THM-M-0240 discovery-only intake probe

These checks authenticate adjacent pinned scheme, smoothness, properness, Weierstrass-curve, and
elliptic Jacobian-coordinate interfaces. `WeierstrassCurve.Jacobian` means a Weierstrass equation
in Jacobian coordinates, not the Jacobian variety of a general algebraic curve. No general Picard
functor, Abel-Jacobi map, target theorem, or proof body is declared here.
-/

#check AlgebraicGeometry.Scheme
#check AlgebraicGeometry.Smooth
#check AlgebraicGeometry.IsProper
#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.Jacobian
#check WeierstrassCurve.Jacobian.Point
