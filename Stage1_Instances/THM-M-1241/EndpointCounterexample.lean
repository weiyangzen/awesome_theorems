import ObligationTree

/-!
# THM-M-1241: registered endpoint-package refutation

The frozen counterexample is projected onto the exact terminal obligation
`M1241-T-ENDPOINT`. This is negative proof evidence for the blocked positive
proof phase, not a proof of the canonical target.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Instances.THM_M_1241

private theorem derivativeLpNorm_const_zero_endpoint :
    derivativeLpNorm 0 (⊤ : ENNReal) (fun _ : Space 1 => (1 : Real)) = 1 := by
  simp only [derivativeLpNorm]
  simp_rw [show forall directions : Fin 0 -> Fin 1,
      coordinateDerivative (fun _ : Space 1 => (1 : Real)) directions = fun _ => 1 by
    intro directions
    funext x
    rfl]
  rw [eLpNorm_exponent_top, eLpNormEssSup_const (1 : Real) (NeZero.ne volume)]
  simp

private theorem derivativeLpNorm_const_one_endpoint :
    derivativeLpNorm 1 1 (fun _ : Space 1 => (1 : Real)) = 0 := by
  simp only [derivativeLpNorm]
  simp_rw [show forall directions : Fin 1 -> Fin 1,
      coordinateDerivative (fun _ : Space 1 => (1 : Real)) directions = fun _ => 0 by
    intro directions
    funext x
    simp only [coordinateDerivative, iteratedFDeriv_const_of_ne one_ne_zero]
    rfl]
  simp

/-- The endpoint package contains the parameter specialization used by the
checked counterexample. -/
theorem not_infiniteEndpointPackage : ¬ InfiniteEndpointPackage := by
  intro endpoint
  obtain ⟨C, hC⟩ := endpoint 1 1 0 ⊤ 1 ⊤ 1
    (by norm_num [AdmissibleParameters, reciprocalExponent])
    (by simp)
  have bound := hC (fun _ : Space 1 => (1 : Real))
    (contDiff_const)
    (by simp [derivativeLpNorm_const_zero_endpoint])
    (by simp [derivativeLpNorm_const_one_endpoint])
    (by norm_num)
  rw [derivativeLpNorm_const_zero_endpoint,
    derivativeLpNorm_const_one_endpoint] at bound
  norm_num at bound

#print axioms not_infiniteEndpointPackage
#print sorries not_infiniteEndpointPackage

end Stage1Instances.THM_M_1241
