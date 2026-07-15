import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0814 validation probe

This module audits the proof-phase declarations and their conditional composition without adding
mathematical proof content.  The exact root still requires `MaximalFlowAttainment` and
`EqualCutForMaximalFlow`; this probe therefore supplies no premise-free max-flow/min-cut theorem.
-/

namespace Stage1Instances.THM_M_0814_Validation

open Stage1Instances.THM_M_0814_Obligations

assert_no_sorry weakDuality_proof
assert_no_sorry noChain_case
assert_no_sorry cutCertificate_of_equalCut
assert_no_sorry root_of_maximalFlowAttainment_and_equalCut

#print sorries weakDuality_proof noChain_case cutCertificate_of_equalCut
  root_of_maximalFlowAttainment_and_equalCut
#print axioms weakDuality_proof
#print axioms noChain_case
#print axioms cutCertificate_of_equalCut
#print axioms root_of_maximalFlowAttainment_and_equalCut

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``weakDuality_proof,
    ``noChain_case,
    ``cutCertificate_of_equalCut,
    ``root_of_maximalFlowAttainment_and_equalCut
  ]
  let allowed : NameSet := .ofArray #[
    ``propext,
    ``Classical.choice,
    ``Quot.sound
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
      if !allowed.contains name then
        unexpectedBodyless := unexpectedBodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unexpected_bodyless={unexpectedBodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0814_Validation
