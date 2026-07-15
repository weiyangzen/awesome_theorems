import Statement
import Mathlib.Data.ZMod.Defs
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0119 independent validation probe

This module deliberately does not import `Proof` or its integer countermodel.
It independently instantiates the frozen interface with `ZMod 2` cohomology.
The resulting checked negation corroborates an encoding blocker; it does not
refute the mathematical Kawamata--Viehweg vanishing theorem.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THMM0119.Validation

open Stage1Instances.THMM0119

private def booleanCohomologyData : KawamataViehwegData.{0, 0} Rat where
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
  cohomology := fun _ _ => ZMod 2
  cohomologyModelsDivisorialSheaf := True

private theorem booleanCohomologyHypotheses :
    booleanCohomologyData.Hypotheses := by
  repeat' apply And.intro trivial
  trivial

/-- A second, independently implemented countermodel to the frozen target. -/
theorem independent_root_countermodel :
    ¬ KawamataViehwegVanishingTarget.{0, 0} := by
  intro target
  have degreeOne :
      Subsingleton
        (booleanCohomologyData.cohomology booleanCohomologyData.D 1) :=
    target Rat booleanCohomologyData booleanCohomologyHypotheses 1 (by omega)
  change Subsingleton (ZMod 2) at degreeOne
  have zero_eq_one : (0 : ZMod 2) = 1 := degreeOne.elim 0 1
  have zero_ne_one : (0 : ZMod 2) ≠ 1 := by decide
  exact zero_ne_one zero_eq_one

assert_no_sorry independent_root_countermodel
#print sorries independent_root_countermodel
#print axioms independent_root_countermodel

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THMM0119.KawamataViehwegVanishingTarget,
    ``Stage1Instances.THMM0119.Validation.independent_root_countermodel
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THMM0119.Validation
