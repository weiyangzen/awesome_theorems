import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.ODE.Basic
import Mathlib.FieldTheory.RatFunc.AsPolynomial
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1478 discovery-only intake probe

These checks authenticate adjacent pinned complex-limit, rational-function, finite-matrix, and ODE
interfaces. They do not define L-stability or A-stability, select a numerical method or source
proposition, or prove THM-M-1478.
-/

#check Complex.normSq
#check Filter.Tendsto
#check Filter.cocompact
#check tendsto_norm_cobounded_atTop
#check Complex.tendsto_normSq_cocompact_atTop
#check tendsto_zero_iff_norm_tendsto_zero
#check RatFunc.num
#check RatFunc.denom
#check RatFunc.eval
#check RatFunc.eval_X
#check RatFunc.eval_eq_zero_of_eval₂_denom_eq_zero
#check RatFunc.eval₂_denom_ne_zero
#check Matrix.mulVec
#check Matrix.mulVecLin
#check IsIntegralCurveOn
#check IsIntegralCurveAt

#print axioms tendsto_norm_cobounded_atTop
#print axioms RatFunc.eval_eq_zero_of_eval₂_denom_eq_zero
#print axioms RatFunc.eval_X
