import Statement

/-!
# THM-M-0119 proof-phase result

The frozen target is false. Its named geometric predicates and its cohomology
model are independent fields, so the hypotheses do not constrain the supplied
cohomology groups. The countermodel below makes every predicate true and uses
`Int` as every cohomology group.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THMM0119

private def counterexampleData : KawamataViehwegData.{0, 0} Rat where
  X := SpecOf Rat
  structureMap := 𝟙 (SpecOf Rat)
  isVarietyOverBase := True
  isNormal := True
  isProjective := True
  qDivisor := Unit
  cartierDivisor := Unit
  delta := ()
  D := ()
  canonicalPlusBoundary := ()
  cartierToQDivisor := fun _ => ()
  qSub := fun _ _ => ()
  deltaEffective := True
  canonicalPlusBoundaryModels := True
  canonicalPlusBoundaryQCartier := True
  pairIsKlt := True
  isNef := fun _ => True
  isBig := fun _ => True
  isAmple := fun _ => True
  cohomology := fun _ _ => Int
  cohomologyModelsDivisorialSheaf := True

private theorem counterexampleHypotheses : counterexampleData.Hypotheses := by
  repeat' apply And.intro trivial
  trivial

/-- A kernel-checked countermodel to the exact frozen proposition. -/
theorem not_kawamataViehwegVanishingTarget :
    ¬ KawamataViehwegVanishingTarget.{0, 0} := by
  intro target
  have degreeOne : Subsingleton (counterexampleData.cohomology counterexampleData.D 1) :=
    target Rat counterexampleData counterexampleHypotheses 1 (by omega)
  change Subsingleton Int at degreeOne
  have zero_eq_one : (0 : Int) = 1 := degreeOne.elim 0 1
  exact Int.zero_ne_one zero_eq_one

#print not_kawamataViehwegVanishingTarget
#print axioms not_kawamataViehwegVanishingTarget

end Stage1Instances.THMM0119
