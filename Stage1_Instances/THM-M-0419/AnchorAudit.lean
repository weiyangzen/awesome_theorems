import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic
import Mathlib.NumberTheory.NumberField.Cyclotomic.Ideal
import Mathlib.NumberTheory.DirichletCharacter.Basic
import Mathlib.NumberTheory.RamificationInertia.HilbertTheory

/-!
# THM-M-0419: pinned mathlib anchor probes

These declarations are supporting infrastructure or the easy cyclotomic-to-
abelian direction. None proves that every finite abelian extension of `ℚ`
embeds in a cyclotomic field.
-/

#check CyclotomicField
#check CyclotomicField.algebraBase
#check CyclotomicField.isCyclotomicExtension
#check IsCyclotomicExtension.isAbelianGalois
#check CyclotomicField.instNumberField
#check DirichletCharacter.conductor
#check DirichletCharacter.factorsThrough_conductor
#check Ideal.ramificationIdxIn
#check Ideal.inertiaDegIn
#check IsCyclotomicExtension.Rat.ramificationIdxIn_eq
#check IsCyclotomicExtension.Rat.inertiaDegIn_eq
#check IsDecompositionField
#check IsInertiaField
