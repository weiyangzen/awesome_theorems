import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Algebra.Lie.Character
import Mathlib.Algebra.Lie.Loop
import Mathlib.Algebra.Lie.Weights.Basic
import Mathlib.LinearAlgebra.RootSystem.WeylGroup
import Mathlib.RingTheory.HahnSeries.Basic

/-!
# THM-M-0137 anchor-audit probe

This file checks the exact repo-local interfaces and adjacent pinned mathlib declarations used by
the bounded anchor inventory. It intentionally declares no canonical Kac-Peterson or Weyl-Kac
target: the admitted source record does not yet select one of those materially different formulas.
-/

namespace Stage1Instances.THM_M_0137_AnchorAudit

#check AddMonoidAlgebra
#check HahnSeries
#check LieAlgebra.loopAlgebra
#check LieAlgebra.LieCharacter
#check LieModule.weightSpace
#check RootPairing.weylGroup

end Stage1Instances.THM_M_0137_AnchorAudit
