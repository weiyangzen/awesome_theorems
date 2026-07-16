import Mathlib.NumberTheory.LSeries.AbstractFuncEq
import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.ProductFormula

/-!
# THM-M-0426 statement boundary probe

The repository supplies only the phrase "the functional equation of the Hecke
L-function". It does not select a source-normalized proposition. These checks
authenticate the closest pinned functional-equation and number-field APIs
without declaring a canonical target, transport, mutation fixture, or proof.
-/

namespace Stage1Instances.THM_M_0426

#check WeakFEPair
#check WeakFEPair.functional_equation
#check StrongFEPair
#check StrongFEPair.functional_equation
#check DirichletCharacter.completedLFunction
#check DirichletCharacter.IsPrimitive.completedLFunction_one_sub
#check NumberField.AdeleRing
#check NumberField.AdeleRing.algebraMap_injective
#check NumberField.prod_abs_eq_one

end Stage1Instances.THM_M_0426
