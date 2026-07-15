import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries
import «Stage1_Instances».«THM-M-0034».Statement
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.MainTheorem

/-!
# THM-M-0034 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It independently writes the
exact adapter from the vendored PID theorem to the frozen field target. This is same-worker
corroboration, not a second proof body or an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0034.Validation

universe u v

/-- An independently written exact-target adapter over the vendored stronger PID theorem. -/
theorem differentialQuillenSuslinTarget :
    Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact quillenSuslin k (Fin n) P

assert_no_sorry quillenSuslin
assert_no_sorry differentialQuillenSuslinTarget

#print sorries quillenSuslin
#print sorries differentialQuillenSuslinTarget
#print axioms quillenSuslin
#print axioms differentialQuillenSuslinTarget

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``quillenSuslin,
    ``Stage1Instances.THM_M_0034.Validation.differentialQuillenSuslinTarget
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

end Stage1Instances.THM_M_0034.Validation
