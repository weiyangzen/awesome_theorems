import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.CMField

/-!
# THM-M-0128 statement gate

The repository intake selects the CM-special-point family of Shimura reciprocity,
but it does not fix the source theorem or the conventions needed to determine one
Lean proposition. In particular, the CM type and reflex construction, idelic
quotient, Artin normalization, canonical model and level, action variance, and
the equality notion remain open.

This module therefore checks only the two pinned object-model anchors already
identified by intake. It deliberately declares no canonical target: adding an
abstract compatibility proposition would replace the requested theorem rather
than elaborate it.
-/

set_option autoImplicit false

#check NumberField.IsCMField
#check NumberField.AdeleRing
