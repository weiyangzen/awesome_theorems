import Mathlib.Analysis.Calculus.FDeriv.Add
import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
# THM-M-1131: pinned anchor probes

The calculus declarations below are proof-enabling infrastructure for the
frozen pointwise Fourier-law implication. The integral divergence theorem is
an adjacent API for a future weak or boundary formulation. None is a terminal
proof of `Stage1Instances.THM_M_1131.Statement`.
-/

#check fderiv_fun_const_smul
#check fderiv_const_smul
#check fderiv_const_smul_of_invertible
#check fderiv_fun_neg
#check fderiv_neg
#check MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable
