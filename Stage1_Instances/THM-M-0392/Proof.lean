import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Basic
import Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms
import Mathlib.Tactic

/-!
# THM-M-0392 proof execution

This module implements the algebraic model, discriminant calculation, and
coordinate transport from the frozen obligation tree. The uniform finiteness
root remains open because no checked Siegel/integral-points theorem is
available in the pinned Lean 4 dependency closure.
-/

namespace Stage1Instances.THMM0392.Proof

/-- The short Weierstrass model `Y^2 = X^3 + k`. -/
def mordellCurve (k : Int) : WeierstrassCurve Int :=
  ⟨0, 0, 0, 0, k⟩

instance (k : Int) : (mordellCurve k).IsShortNF :=
  ⟨rfl, rfl, rfl⟩

/-- The mathlib affine equation of the selected curve is exactly the frozen
Mordell equation. This closes the equation-correspondence part of
`M0392-C-CURVE`. -/
theorem mordellCurve_equation_iff (k x y : Int) :
    (mordellCurve k).toAffine.Equation x y ↔ y ^ 2 = x ^ 3 + k := by
  rw [WeierstrassCurve.Affine.equation_iff]
  simp [mordellCurve]

/-- The discriminant of the selected integral model. -/
theorem mordellCurve_discriminant (k : Int) :
    (mordellCurve k).Δ = -432 * k ^ 2 := by
  rw [WeierstrassCurve.Δ_of_isShortNF]
  simp [mordellCurve]
  ring

/-- A nonzero Mordell parameter gives a nonzero discriminant. This closes
frozen obligation `M0392-L-NONSINGULAR`. -/
theorem mordellCurve_discriminant_ne_zero {k : Int} (hk : k ≠ 0) :
    (mordellCurve k).Δ ≠ 0 := by
  rw [mordellCurve_discriminant]
  exact mul_ne_zero (by norm_num) (pow_ne_zero 2 hk)

/-- Integer points represented through mathlib's affine equation predicate. -/
def IntegralCurvePoints (k : Int) :=
  {p : Int × Int // (mordellCurve k).toAffine.Equation p.1 p.2}

/-- The checked coordinate map from equation solutions to integral affine
curve points. -/
def toIntegralCurvePoint (k : Int) :
    {p : Int × Int // p.2 ^ 2 = p.1 ^ 3 + k} → IntegralCurvePoints k :=
  fun p => ⟨p.1, (mordellCurve_equation_iff k p.1.1 p.1.2).2 p.2⟩

/-- The coordinate map preserves the underlying pair and is injective. This
closes frozen obligation `M0392-T-COORDINATES`. -/
theorem toIntegralCurvePoint_injective (k : Int) :
    Function.Injective (toIntegralCurvePoint k) := by
  intro p q hpq
  apply Subtype.ext
  change p.1 = q.1
  exact congrArg (fun r : IntegralCurvePoints k => r.1) hpq

#print axioms mordellCurve_equation_iff
#print axioms mordellCurve_discriminant
#print axioms mordellCurve_discriminant_ne_zero
#print axioms toIntegralCurvePoint_injective

end Stage1Instances.THMM0392.Proof
