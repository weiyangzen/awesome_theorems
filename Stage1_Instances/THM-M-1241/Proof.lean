import ObligationTree

/-!
# THM-M-1241 partial proof execution

The exact interpolation packages remain open. This module implements the
degenerate output-exponent branch `p = 0`, which is admitted by the frozen
ENNReal encoding and is definitionally zero in mathlib's `eLpNorm`.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Instances.THM_M_1241

/-- Every derivative seminorm at exponent zero vanishes. -/
theorem derivativeLpNorm_exponent_zero {n : Nat} (j : Nat)
    (u : Space n -> Real) : derivativeLpNorm j 0 u = 0 := by
  simp [derivativeLpNorm]

/-- The exact fixed-parameter conclusion in the `p = 0` branch, with a
uniform constant `C = 1`. No regularity or integrability hypothesis is used. -/
theorem parameterConclusion_exponent_zero
    (n m j : Nat) (q r : ENNReal) (a : Real) :
    ParameterConclusion n m j q r 0 a := by
  refine ⟨1, ?_⟩
  intro u _ _ _ _
  simp [derivativeLpNorm_exponent_zero]

/-- The scaling equation determines only the reciprocal-exponent convention:
both `p = 0` and `p = infinity` have reciprocal exponent zero. This records the
exact boundary exposed by the degenerate branch above. -/
theorem reciprocalExponent_eq_zero_iff (p : ENNReal) :
    reciprocalExponent p = 0 <-> p = 0 ∨ p = (⊤ : ENNReal) := by
  by_cases hp : p = (⊤ : ENNReal)
  · simp [reciprocalExponent, hp]
  · simp only [reciprocalExponent, hp, if_false, inv_eq_zero]
    rw [ENNReal.toReal_eq_zero_iff]
    simp [hp]

#print axioms derivativeLpNorm_exponent_zero
#print axioms parameterConclusion_exponent_zero
#print axioms reciprocalExponent_eq_zero_iff
#print sorries derivativeLpNorm_exponent_zero
#print sorries parameterConclusion_exponent_zero
#print sorries reciprocalExponent_eq_zero_iff

end Stage1Instances.THM_M_1241
