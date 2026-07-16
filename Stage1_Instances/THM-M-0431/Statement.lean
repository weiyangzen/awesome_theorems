import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.RepresentationTheory.Basic

/-!
# THM-M-0431 statement-gate probe

The repository source says only "the local Langlands correspondence for local fields" and does
not select an exact theorem. This module therefore checks the smallest pinned interfaces needed
to expose the current boundary: nonarchimedean local fields, general linear groups, and ordinary
representations. It intentionally declares no canonical target. In particular, it does not replace
smooth irreducible admissible representations or Frobenius-semisimple Weil-Deligne parameters with
abstract caller-supplied predicates.
-/

namespace Stage1Instances.THM_M_0431

#check IsNonarchimedeanLocalField
#check Matrix.GeneralLinearGroup
#check Representation

end Stage1Instances.THM_M_0431
