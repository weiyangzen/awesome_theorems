import Statement
import Mathlib.Data.ZMod.Defs

/-!
# THM-M-0118 independent validation probe

This file independently checks the proof-phase blocker with a different finite
model. It deliberately does not import `Proof`: the selected abstract target
would force `ZMod 2` to be a subsingleton even though zero and one differ.
-/

namespace Stage1Instances.THMM0118.Validation

private def booleanModel : NakanoVanishingData.{0, 0, 0} where
  X := Unit
  E := Unit
  complexDimension := 0
  Cohomology := fun _ _ => ZMod 2
  cohomologyAddCommGroup := fun _ _ => inferInstance
  compactKahler := True
  holomorphicVectorBundle := True
  nakanoPositive := True

/-- A second kernel-checked model showing that the frozen positive root is false. -/
theorem independent_root_countermodel :
    ¬ NakanoVanishingTarget.{0, 0, 0} := by
  intro target
  have h : Subsingleton (booleanModel.Cohomology 1 0) :=
    target booleanModel 1 0 trivial trivial trivial (by decide)
  change Subsingleton (ZMod 2) at h
  have : (0 : ZMod 2) = 1 := h.elim 0 1
  have hne : (0 : ZMod 2) ≠ 1 := by decide
  exact hne this

#print axioms independent_root_countermodel

end Stage1Instances.THMM0118.Validation
