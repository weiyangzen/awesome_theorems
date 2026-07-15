import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0338 validation probe

This module audits the two proof-phase extension-existence declarations and
their conditional root composition. It adds no uniqueness or Kadison-Singer
proof and therefore cannot close the canonical root.
-/

namespace Stage1.THM_M_0338.Validation

assert_no_sorry Stage1.THM_M_0338.root_of_components
assert_no_sorry Stage1.THM_M_0338.extension_exists_for_state
assert_no_sorry Stage1.THM_M_0338.extension_exists_for_kadison_singer_input

#print sorries Stage1.THM_M_0338.root_of_components
#print sorries Stage1.THM_M_0338.extension_exists_for_state
#print sorries Stage1.THM_M_0338.extension_exists_for_kadison_singer_input

#print axioms Stage1.THM_M_0338.root_of_components
#print axioms Stage1.THM_M_0338.extension_exists_for_state
#print axioms Stage1.THM_M_0338.extension_exists_for_kadison_singer_input

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1.THM_M_0338.root_of_components,
    ``Stage1.THM_M_0338.extension_exists_for_state,
    ``Stage1.THM_M_0338.extension_exists_for_kadison_singer_input
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut unexpectedBodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !uniqueAxioms.contains name then unexpectedBodyless := unexpectedBodyless.push name
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unexpected_bodyless={unexpectedBodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1.THM_M_0338.Validation
