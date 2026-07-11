import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.CMField

/-!
# THM-M-0128 statement-substrate probe

This file checks only the pinned object-model surface available to the statement
phase. It deliberately declares no Shimura reciprocity target: the pinned
environment has no CM-type, reflex-field/reflex-norm, Artin reciprocity, canonical
Shimura model, or CM-special-point API from which the intake claim can be encoded
without inventing uninterpreted stand-ins.
-/

#check NumberField.IsCMField
#check NumberField.AdeleRing
