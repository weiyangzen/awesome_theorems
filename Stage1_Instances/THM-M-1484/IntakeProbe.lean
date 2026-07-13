import Mathlib.Analysis.SpecialFunctions.Sigmoid
import Mathlib.Data.Matrix.Mul

/-!
Discovery-only checks for APIs adjacent to the THM-M-1484 topic family.

These declarations provide a scalar activation and finite matrix-vector multiplication. They do
not define a neural-network architecture or evaluator, select a theorem, or prove THM-M-1484.
-/

#check Real.sigmoid
#check Real.sigmoid_pos
#check Real.sigmoid_strictMono
#check continuous_sigmoid
#check Matrix.mulVec
#check Matrix.mulVec_add
