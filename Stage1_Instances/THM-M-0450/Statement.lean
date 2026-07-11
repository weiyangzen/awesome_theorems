import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.NumberTheory.NumberField.Basic

/-!
# Exact statement gate for THM-M-0450

This module contains only the canonical Mordell-Weil target and statement-gate
probes. It intentionally contains no proof of the target.
-/

noncomputable section

universe u

namespace Stage1Instances.THM_M_0450

/-- The full group of `K`-rational points, including the point at infinity. -/
abbrev RationalPoints (K : Type u) [Field K] (E : WeierstrassCurve K) :=
  E.toJacobian.Point

/--
The exact Lean 4 target for the Mordell-Weil theorem: the rational-point group
of every elliptic Weierstrass curve over every number field is finitely
generated.
-/
def ExactTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (E : WeierstrassCurve K),
    E.IsElliptic → AddGroup.FG (RationalPoints K E)

-- These probes make the inferred object model and the fully elaborated target
-- visible in the recorded Lean output.
#check WeierstrassCurve.Jacobian.Point.instAddCommGroup
#check ExactTarget
set_option pp.all true in
#print ExactTarget

end Stage1Instances.THM_M_0450
