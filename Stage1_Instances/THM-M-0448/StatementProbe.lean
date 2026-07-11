import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.NumberTheory.LocalField.Basic

/-!
This is an elaboration probe, not the Harris--Taylor statement.  It checks the
closest concrete objects available in the pinned dependency closure without
postulating the missing local-Langlands categories or correspondence.
-/

open ValuativeRel

universe uK uN

namespace Stage1Instances.THM_M_0448.StatementProbe

abbrev GLn
    (n : Type uN) (K : Type uK)
    [Fintype n] [DecidableEq n] [Field K] : Type (max uN uK) :=
  Matrix.GeneralLinearGroup n K

abbrev AbsoluteGaloisGroup
    (K : Type uK) [Field K] : Type uK :=
  Field.absoluteGaloisGroup K

section LocalFieldContext

variable (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
  [IsNonarchimedeanLocalField K]

#check 𝓀[K]

end LocalFieldContext

end Stage1Instances.THM_M_0448.StatementProbe
