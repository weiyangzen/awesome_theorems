import Mathlib.LinearAlgebra.QuadraticForm.Radical
import Mathlib.LinearAlgebra.QuadraticForm.TensorProduct
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace
import Mathlib.NumberTheory.NumberField.Completion.InfinitePlace

/-!
# THM-M-0020 discovery-only intake probe

These checks authenticate adjacent pinned quadratic-form, scalar-extension, and number-field-place
APIs. They do not select an isotropy, representation, equivalence, or classification formulation
and do not state or prove the Hasse-Minkowski theorem.
-/

#check QuadraticForm
#check QuadraticMap.Anisotropic
#check QuadraticMap.not_anisotropic_iff_exists
#check QuadraticMap.Nondegenerate
#check QuadraticForm.baseChange
#check QuadraticForm.baseChange_tmul
#check NumberField
#check NumberField.FinitePlace
#check NumberField.InfinitePlace
