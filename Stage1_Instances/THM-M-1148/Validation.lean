import Statement
import PoissonUnitDisk

/-!
# THM-M-1148 validation probes

This module deliberately does not import `Proof.lean`. It rebuilds the
last composition from the implemented disk construction to the exact frozen
target, so validation does not merely import the claimed root declaration.
-/

noncomputable section

open InnerProductSpace Metric Real Set

namespace Stage1Instances.THM_M_1148.Validation

open Stage1Instances.THM_M_1148
open Stage1Instances.THM_M_1148.PoissonUnitDisk

theorem reconstructedPoissonIntegralFormula : PoissonIntegralFormula := by
  intro c R hR g hg
  obtain ⟨u, huH, huC, hug⟩ := generalDiskConstruction c R hR g hg
  refine ⟨u, huH, huC, hug, ?_⟩
  intro w hw
  have hR' : 0 < R := pos_of_mem_ball hw
  apply (circleAverage_congr_sphere (fun x hx => ?_)).trans
    ((HarmonicContOnCl.mk_ball huH huC).circleAverage_poissonKernel_smul hw)
  rw [abs_of_pos hR'] at hx
  simp only [smul_eq_mul, Pi.mul_apply, hug hx]

#print axioms reconstructedPoissonIntegralFormula

end Stage1Instances.THM_M_1148.Validation
