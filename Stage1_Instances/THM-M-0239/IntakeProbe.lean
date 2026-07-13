import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.AlgebraicGeometry.Group.Abelian
import Mathlib.Data.Sym.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.NumberTheory.ModularForms.JacobiTheta.TwoVariable
import Mathlib.RingTheory.PicardGroup

/-!
# THM-M-0239 discovery-only intake probe

These checks authenticate adjacent pinned APIs for finite multisets, complex manifolds,
one-dimensional Jacobi theta functions, group schemes, ring Picard groups, and Weierstrass
Jacobian coordinates. They do not define a compact curve's geometric symmetric product,
Jacobian variety, Abel-Jacobi map, genus-g Riemann theta function, or Jacobi inversion theorem.
-/

#check Sym
#check Sym.cons
#check ModelWithCorners
#check IsManifold
#check CompactSpace
#check MDifferentiable.exists_eq_const_of_compactSpace
#check jacobiTheta₂
#check jacobiTheta₂_functional_equation
#check AlgebraicGeometry.isCommMonObj_of_isProper_of_geometricallyIntegral
#check CommRing.Pic
#check WeierstrassCurve.Jacobian.Point
