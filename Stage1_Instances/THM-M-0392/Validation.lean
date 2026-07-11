import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Basic
import Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms
import Mathlib.Tactic

/-!
# THM-M-0392 independent validation probe

This module reconstructs the locally closed Mordell-curve obligations without
importing `Proof.lean`. It deliberately does not assert the missing
integral-points finiteness bridge or the canonical root.
-/

namespace Stage1Instances.THMM0392.Validation

def validationCurve (k : Int) : WeierstrassCurve Int :=
  ⟨0, 0, 0, 0, k⟩

instance (k : Int) : (validationCurve k).IsShortNF :=
  ⟨rfl, rfl, rfl⟩

theorem independent_equation_iff (k x y : Int) :
    (validationCurve k).toAffine.Equation x y ↔ y ^ 2 = x ^ 3 + k := by
  rw [WeierstrassCurve.Affine.equation_iff]
  simp [validationCurve]

theorem independent_discriminant (k : Int) :
    (validationCurve k).Δ = -432 * k ^ 2 := by
  rw [WeierstrassCurve.Δ_of_isShortNF]
  simp [validationCurve]
  ring

theorem independent_discriminant_ne_zero {k : Int} (hk : k ≠ 0) :
    (validationCurve k).Δ ≠ 0 := by
  rw [independent_discriminant]
  exact mul_ne_zero (by norm_num) (pow_ne_zero 2 hk)

def ValidationIntegralPoints (k : Int) :=
  {p : Int × Int // (validationCurve k).toAffine.Equation p.1 p.2}

def independentEmbedding (k : Int) :
    {p : Int × Int // p.2 ^ 2 = p.1 ^ 3 + k} → ValidationIntegralPoints k :=
  fun p => ⟨p.1, (independent_equation_iff k p.1.1 p.1.2).2 p.2⟩

theorem independent_embedding_injective (k : Int) :
    Function.Injective (independentEmbedding k) := by
  intro p q hpq
  apply Subtype.ext
  change p.1 = q.1
  exact congrArg (fun r : ValidationIntegralPoints k => r.1) hpq

#print axioms independent_equation_iff
#print axioms independent_discriminant_ne_zero
#print axioms independent_embedding_injective

end Stage1Instances.THMM0392.Validation
