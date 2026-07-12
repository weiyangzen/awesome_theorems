import Statement
import Mathlib.Algebra.Group.Int.Defs

/-!
# THM-M-0118 proof-phase result

The frozen abstract target is false. Its geometric predicates and cohomology
family are independent fields, so the hypotheses do not constrain the selected
cohomology group. The countermodel below makes every predicate true and uses
`Int` in every bidegree.
-/

namespace Stage1Instances.THMM0118

private def counterexampleData : NakanoVanishingData.{0, 0, 0} where
  X := Unit
  E := Unit
  complexDimension := 0
  Cohomology := fun _ _ => Int
  cohomologyAddCommGroup := fun _ _ => inferInstance
  compactKahler := True
  holomorphicVectorBundle := True
  nakanoPositive := True

/-- A kernel-checked countermodel to the exact frozen proposition. -/
theorem not_nakanoVanishingTarget :
    ¬ NakanoVanishingTarget.{0, 0, 0} := by
  intro target
  have degreeOne : Subsingleton (counterexampleData.Cohomology 1 0) :=
    target counterexampleData 1 0 trivial trivial trivial (by decide)
  change Subsingleton Int at degreeOne
  have zero_eq_one : (0 : Int) = 1 := degreeOne.elim 0 1
  exact Int.zero_ne_one zero_eq_one

#print not_nakanoVanishingTarget
#print axioms not_nakanoVanishingTarget

end Stage1Instances.THMM0118
