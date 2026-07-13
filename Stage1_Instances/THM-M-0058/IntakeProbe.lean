import Mathlib.Analysis.InnerProductSpace.SingularValues
import Mathlib.Analysis.InnerProductSpace.Trace
import Mathlib.LinearAlgebra.Matrix.Trace

/-!
Discovery-only checks for pinned APIs adjacent to the unresolved THM-M-0058
catalog claim. These checks do not state or prove von Neumann's trace inequality.
-/

#check Matrix.trace
#check Matrix.trace_conjTranspose
#check Matrix.trace_mul_comm
#check LinearMap.trace_eq_sum_inner
#check LinearMap.IsSymmetric.trace_eq_sum_eigenvalues
#check LinearMap.singularValues
#check LinearMap.singularValues_nonneg
#check LinearMap.singularValues_antitone
#check LinearMap.support_singularValues
