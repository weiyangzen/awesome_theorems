import Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point

/-!
# THM-M-1599 discovery-only intake probe

These checks authenticate generic pinned elliptic-curve and projective point-group APIs. They do
not define ECDH or another cryptosystem, select a canonical proposition, establish security, or
prove THM-M-1599.
-/

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.Projective.Point
#check WeierstrassCurve.Projective.Point.instAddCommGroup
#check WeierstrassCurve.toProjective
#print axioms WeierstrassCurve.Projective.Point.instAddCommGroup
