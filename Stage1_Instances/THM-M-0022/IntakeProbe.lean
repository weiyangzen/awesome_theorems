import Mathlib.NumberTheory.LSeries.AbstractFuncEq
import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.ProductFormula

/-!
# THM-M-0022 discovery-only intake probe

These checks authenticate adjacent pinned functional-equation and number-field APIs. They do not
define a Hecke character, select a canonical Hecke L-function equation, resolve THM-M-0426, or
claim proof credit.
-/

#check WeakFEPair
#check WeakFEPair.functional_equation
#check StrongFEPair
#check StrongFEPair.functional_equation
#check DirichletCharacter.completedLFunction
#check DirichletCharacter.IsPrimitive.completedLFunction_one_sub
#check NumberField.AdeleRing
#check NumberField.AdeleRing.algebraMap_injective
#check NumberField.prod_abs_eq_one
