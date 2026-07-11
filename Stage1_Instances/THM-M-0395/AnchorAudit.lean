import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Properties
import Mathlib.GroupTheory.Descent
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.Basic

/-!
# THM-M-0395 immutable anchor probe

This file checks only partial infrastructure found by the anchor audit. None of
the declarations below proves the Faltings/Mordell root.
-/

open AlgebraicGeometry

#check NumberField
#check Scheme
#check Smooth
#check IsProper
#check IsIntegral
#check Northcott.finite_le
#check AddCommGroup.fg_of_descent'
