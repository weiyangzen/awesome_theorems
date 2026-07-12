import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.Complex.Harmonic.Poisson
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Integral.Bochner.Basic

open MeasureTheory Metric Set
open scoped RealInnerProductSpace

namespace Stage1.THM_M_1129.AnchorAudit

abbrev Plane := EuclideanSpace Real (Fin 2)

-- Kernel-elaborated types for the supporting mathlib declarations credited by the audit.
#check Laplacian.laplacian
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis
#check integral_add
#check integral_smul
#check integral_map
#check hasDerivAt_integral_of_dominated_loc_of_lip
#check hasDerivAt_integral_of_dominated_loc_of_deriv_le
#check poissonKernel
#check InnerProductSpace.HarmonicOnNhd.circleAverage_poissonKernel_smul
#check InnerProductSpace.HarmonicContOnCl.circleAverage_poissonKernel_smul

/-- The pinned Poisson theorem is a boundary-circle identity for a harmonic complex-plane
function. It does not state the two-dimensional wave Cauchy representation. -/
def HarmonicPoissonCandidate : Prop :=
  forall (f : Complex -> Real) (c w : Complex) (R : Real),
    InnerProductSpace.HarmonicOnNhd f (closedBall c R) -> w ∈ ball c R ->
      Real.circleAverage (poissonKernel c w • f) c R = f w

def WavePoissonShape : Prop :=
  forall (c : Real) (_f _g : Plane -> Real) (u : Plane -> Real -> Real),
    0 < c -> forall x t, 0 < t -> u x t = u x t

#check_failure (rfl : HarmonicPoissonCandidate = WavePoissonShape)

end Stage1.THM_M_1129.AnchorAudit
