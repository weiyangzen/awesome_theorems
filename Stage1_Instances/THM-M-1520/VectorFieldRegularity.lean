import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.ContDiff.FiniteDimension
import Mathlib.Analysis.Calculus.ContDiff.WithLp

import Statement

/-!
# THM-M-1520 Hamiltonian-vector-field regularity

This module implements the regularity input to the frozen divergence and spatial-flow branches.
-/

namespace Stage1.THM_M_1520

/-- A twice continuously differentiable Hamiltonian has a continuously differentiable canonical
Hamiltonian vector field. -/
theorem hamiltonianVectorField_contDiff_one
    {n : Nat} {H : PhaseSpace n -> Real} (hH : ContDiff Real 2 H) :
    ContDiff Real 1 (hamiltonianVectorField H) := by
  unfold hamiltonianVectorField symplecticRotation
  apply WithLp.contDiff_toLp.comp
  apply ContDiff.prodMk
  · exact WithLp.contDiff_ofLp.snd.comp
      ((InnerProductSpace.toDual Real (PhaseSpace n)).symm.toContinuousLinearEquiv.contDiff.comp
        (hH.fderiv_right (m := 1) (by norm_num)))
  · exact (WithLp.contDiff_ofLp.fst.comp
      ((InnerProductSpace.toDual Real (PhaseSpace n)).symm.toContinuousLinearEquiv.contDiff.comp
        (hH.fderiv_right (m := 1) (by norm_num)))).neg

#print sorries hamiltonianVectorField_contDiff_one
#print axioms hamiltonianVectorField_contDiff_one

end Stage1.THM_M_1520
