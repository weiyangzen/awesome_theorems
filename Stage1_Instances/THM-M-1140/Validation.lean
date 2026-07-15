import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1140 validation probe

This module checks the proof phase through a separately written exact-type and
composition probe. It imports the existing proof body, so it is same-worker
corroboration rather than an independent proof or runner attestation.
-/

namespace Stage1Instances.THM_M_1140.Validation

/-- Import-dependent exact-type probe for the repo-local strong maximum root. -/
theorem exactRootProbe : HarmonicStrongMaximumPrinciple :=
  harmonicStrongMaximumPrinciple

/-- Recompose the exact root from the two frozen package interfaces. -/
theorem exactCompositionProbe : HarmonicStrongMaximumPrinciple :=
  harmonicStrongMaximumPrinciple_of_packages
    interiorLocalRigidity connectedLevelPropagation

assert_no_sorry harmonicStrongMaximumPrinciple_of_packages
assert_no_sorry interiorLocalRigidity
assert_no_sorry connectedLevelPropagation
assert_no_sorry harmonicStrongMaximumPrinciple
assert_no_sorry exactRootProbe
assert_no_sorry exactCompositionProbe

#print sorries harmonicStrongMaximumPrinciple_of_packages
  interiorLocalRigidity connectedLevelPropagation
  harmonicStrongMaximumPrinciple exactRootProbe exactCompositionProbe

#print axioms exactRootProbe
#print axioms exactCompositionProbe

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple_of_packages,
    ``Stage1Instances.THM_M_1140.interiorLocalRigidity,
    ``Stage1Instances.THM_M_1140.connectedLevelPropagation,
    ``Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple,
    ``Stage1Instances.THM_M_1140.Validation.exactRootProbe,
    ``Stage1Instances.THM_M_1140.Validation.exactCompositionProbe
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

end Stage1Instances.THM_M_1140.Validation
