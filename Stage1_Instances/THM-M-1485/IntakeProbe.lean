import Mathlib.Analysis.Calculus.FDeriv.Add
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.SpecialFunctions.Sigmoid
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1485 discovery-only intake probe

These checks authenticate generic pinned chain-rule, finite-sum, sigmoid, squared-loss, and
matrix-vector interfaces adjacent to possible backpropagation encodings. They do not define a
neural network, backward recurrence, training algorithm, canonical target, or proof.
-/

#check HasFDerivAt.comp
#check fderiv_comp
#check HasFDerivAt.fun_sum
#check fderiv_sum
#check Real.sigmoid
#check Real.hasDerivAt_sigmoid
#check HasFDerivAt.norm_sq
#check Matrix.mulVecLin
#check Matrix.mulVecLin_mul

#print axioms Real.hasDerivAt_sigmoid
#print axioms HasFDerivAt.comp
#print axioms HasFDerivAt.norm_sq
