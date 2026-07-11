import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction

/-!
# THM-M-0446 statement substrate probe

This file checks the smallest pinned mathlib import that exposes the local
reduction notions relevant to semistability. It deliberately declares no
surrogate semistability or modularity predicate: the pinned environment does
not supply the global predicates needed to state the intake-selected theorem
exactly.
-/

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.HasGoodReduction
#check WeierstrassCurve.HasMultiplicativeReduction
#check WeierstrassCurve.HasAdditiveReduction
#check WeierstrassCurve.hasGoodReduction_or_hasMultiplicativeReduction_or_hasAdditiveReduction

/-- The pinned object model can express a nonsingular Weierstrass curve over
the rational numbers without adding an abstract stand-in for the theorem. -/
def Stage1Instances.THM_M_0446.RationalEllipticCurve : Type :=
  { W : WeierstrassCurve ℚ // W.IsElliptic }

#check Stage1Instances.THM_M_0446.RationalEllipticCurve
