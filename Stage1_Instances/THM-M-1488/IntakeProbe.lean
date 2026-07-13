import Mathlib.Analysis.SpecialFunctions.Sigmoid
import Mathlib.Data.List.Basic
import Mathlib.Data.Matrix.Mul

/-!
# THM-M-1488 discovery-only intake probe

These checks authenticate adjacent pinned scalar-activation, list-fold, and finite matrix-vector
interfaces. They do not define a recurrent cell or evaluator, select a source proposition, or prove
THM-M-1488.
-/

#check Real.sigmoid
#check Real.sigmoid_pos
#check Real.sigmoid_strictMono
#check continuous_sigmoid
#check List.foldl
#check List.foldl_concat
#check Matrix.mulVec
#check Matrix.mulVec_add

#print axioms Real.sigmoid_strictMono
#print axioms continuous_sigmoid
#print axioms Matrix.mulVec_add
