import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic

-- Expected failure: `ℤ` is not a field, so it cannot replace the rational base.
#check IsAbelianGalois ℤ ℚ
