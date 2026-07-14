import Statement
import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1080 differential validation probe

This module deliberately imports neither `ObligationTree` nor `ExactRoot`. It binds the proof
phase's direct Azuma theorem to the exact frozen statement without using the frozen threshold
composition route. This is a separately written same-worker differential check, not a distinct
proof body or independent-runner attestation.
-/

noncomputable section

namespace Stage1Instances.THM_M_1080.Validation

universe u

/-- Direct exact-type bridge, separate from the proof phase's frozen-composition bridge. -/
theorem directExactRoot : Stage1Instances.THM_M_1080.Statement.{u} := by
  simpa only [
    Stage1Instances.THM_M_1080.Statement,
    Stage1Instances.THM_M_1080.AzumaUpperTail,
    Stage1Instances.THM_M_1080.squaredBoundSum,
    Proof.squaredBoundSum
  ] using Proof.azumaUpperTail

assert_no_sorry Proof.azumaUpperTail
assert_no_sorry directExactRoot

#print sorries Proof.azumaUpperTail directExactRoot
#print axioms Proof.azumaUpperTail
#print axioms directExactRoot

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1080.Proof.azumaUpperTail,
    ``Stage1Instances.THM_M_1080.Validation.directExactRoot
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

end Stage1Instances.THM_M_1080.Validation
