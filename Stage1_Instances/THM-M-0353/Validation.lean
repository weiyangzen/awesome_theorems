import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0353 same-worker validation probe

This module reconstructs the exact frozen target from the two proved packages
rather than invoking the proof-phase root declaration. It shares the proof
helpers, worker, toolchain, and cache, so it is a differential composition
check, not an independent proof or distinct-runner attestation.
-/

namespace Stage1Instances.THM_M_0353.Validation

/-- Recompose the exact canonical target without invoking the terminal root. -/
theorem recomposedHermiteCompleteness : HermiteCompletenessTarget :=
  And.intro hermiteMemLpPackage_proof hermiteBasisPackage_proof

assert_no_sorry _root_.hermiteFunction_memLp
assert_no_sorry _root_.hermiteFunction_orthonormal
assert_no_sorry _root_.hermiteFunction_complete
assert_no_sorry Stage1Instances.THM_M_0353.hermiteMemLpPackage_proof
assert_no_sorry Stage1Instances.THM_M_0353.hermiteBasisPackage_proof
assert_no_sorry Stage1Instances.THM_M_0353.hermiteCompletenessTarget_proof
assert_no_sorry recomposedHermiteCompleteness

#print sorries Stage1Instances.THM_M_0353.hermiteCompletenessTarget_proof
#print sorries recomposedHermiteCompleteness
#print axioms Stage1Instances.THM_M_0353.hermiteCompletenessTarget_proof
#print axioms recomposedHermiteCompleteness

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0353.hermiteCompletenessTarget_proof,
    ``Stage1Instances.THM_M_0353.Validation.recomposedHermiteCompleteness
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
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0353.Validation
