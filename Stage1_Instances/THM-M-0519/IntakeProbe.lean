import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.Δ
#check WeierstrassCurve.j

example (E : WeierstrassCurve Rat) [E.IsElliptic] : IsUnit E.Δ := E.isUnit_Δ
