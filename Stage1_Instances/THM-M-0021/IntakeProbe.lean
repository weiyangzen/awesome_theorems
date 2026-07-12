import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.NumberField.Units.Regulator

/-!
Discovery-only substrate checks for a later source-selected Brauer-Siegel statement.

This file deliberately states no asymptotic theorem over a family of number fields. In particular,
the checked invariants and generic filter interface do not select the missing family, growth
hypotheses, normalization, or conclusion.
-/

#check NumberField
#check NumberField.classNumber
#check NumberField.classNumber_pos
#check NumberField.Units.regulator
#check NumberField.Units.regulator_pos
#check NumberField.discr
#check NumberField.discr_ne_zero
#check Filter.Tendsto
