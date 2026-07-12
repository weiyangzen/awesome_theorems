import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.InnerProductSpace.l2Space

/-!
# THM-M-1272 immutable mathlib anchor probe

These declarations check calculus and orthogonal-decomposition infrastructure
at the pinned mathlib revision. None is a Fountain, minimax, genus, deformation,
or Palais-Smale theorem.
-/

noncomputable section

open Filter Set
open scoped Topology

namespace Stage1Instances.THM_M_1272.AnchorAudit

universe u

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- A checked bridge from a local minimum to the derivative-zero predicate used by the target. -/
theorem localMin_has_zero_fderiv {Phi : E → ℝ} {x : E} (h : IsLocalMin Phi x) :
    fderiv ℝ Phi x = 0 :=
  h.fderiv_eq_zero

/-- The selected `C^1` hypothesis supplies ordinary continuity. -/
theorem contDiff_one_continuous {Phi : E → ℝ} (h : ContDiff ℝ 1 Phi) :
    Continuous Phi :=
  h.continuous

/-- The selected `C^1` hypothesis supplies Frechet differentiability. -/
theorem contDiff_one_differentiable {Phi : E → ℝ} (h : ContDiff ℝ 1 Phi) :
    Differentiable ℝ Phi :=
  h.differentiable_one

/-- A complete submodule and its orthogonal complement form a checked Hilbert sum. -/
theorem orthogonal_core_tail
    (K : Submodule ℝ E) [CompleteSpace E] [CompleteSpace K] :
    IsHilbertSum ℝ (fun b : Bool ↦ ↥(bif b then K else Kᗮ))
      (fun b ↦ (bif b then K else Kᗮ).subtypeₗᵢ) :=
  Submodule.isHilbertSumOrthogonal K

-- Object/API probes only. Their types do not close the Fountain target.
#check fderiv
#check ContDiff
#check ContDiff.continuous
#check ContDiff.differentiable_one
#check IsLocalMin.fderiv_eq_zero
#check HilbertBasis
#check exists_hilbertBasis
#check IsHilbertSum
#check Submodule.isHilbertSumOrthogonal
#check Orthonormal
#check Submodule.orthogonal
#check StrictMono.tendsto_atTop

end Stage1Instances.THM_M_1272.AnchorAudit
