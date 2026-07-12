import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.NumberTheory.LSeries.Deriv

/-!
Pinned-environment substrate probe for the THM-M-0522 statement gate.

This file checks only the nearby objects already present in mathlib: rational points on a
Weierstrass elliptic curve and generic complex L-series derivatives. The generic series is not the
elliptic Hasse-Weil L-function needed to define the canonical theorem, so this file deliberately
declares no theorem target.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0522.StatementProbe

/-- The rational-point group already supplied for a nonsingular Weierstrass curve. -/
abbrev RationalPointGroup (E : WeierstrassCurve ℚ) [E.IsElliptic] : Type :=
  E⟮ℚ⟯

variable (E : WeierstrassCurve ℚ) [E.IsElliptic]

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check RationalPointGroup
#synth AddCommGroup (RationalPointGroup E)
#check LSeries
#check iteratedDeriv

end Stage1Instances.THM_M_0522.StatementProbe
