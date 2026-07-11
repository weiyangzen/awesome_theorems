import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.NumberTheory.NumberField.Basic

noncomputable section
universe u

namespace Stage1Instances.THM_M_0450.Mutations

abbrev RationalPoints (K : Type u) [Field K] (E : WeierstrassCurve K) :=
  E.toJacobian.Point

def ExactTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (E : WeierstrassCurve K),
    E.IsElliptic → AddGroup.FG (RationalPoints K E)

-- Expected rejection: the canonical number-field claim cannot be widened to
-- all fields by application of its hypothesis.
example (h : ExactTarget) :
    ∀ (K : Type u) [Field K] (E : WeierstrassCurve K),
      E.IsElliptic → AddGroup.FG (RationalPoints K E) := by
  exact h

end Stage1Instances.THM_M_0450.Mutations
