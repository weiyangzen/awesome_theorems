import Proof
import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0349 validation probe

This module audits the proof-phase declarations and the conditional root
composition without adding a conjugate-function proof.  In particular,
`root_of_conjugate_packages` still consumes the two unproved all-`p` packages,
and `conjugate_l2_bound` remains a candidate for a planned-only registry node.
-/

namespace Stage1Instances.THM_M_0349.Validation

assert_no_sorry Stage1Instances.THM_M_0349.conjugateMode
assert_no_sorry Stage1Instances.THM_M_0349.fourierCoeff_conjugateMode
assert_no_sorry Stage1Instances.THM_M_0349.conjugateMultiplier_zero
assert_no_sorry Stage1Instances.THM_M_0349.norm_conjugateMultiplier_le_one
assert_no_sorry Stage1Instances.THM_M_0349.conjugateMultiplier_memℓp_two
assert_no_sorry Stage1Instances.THM_M_0349.conjugateSequence
assert_no_sorry Stage1Instances.THM_M_0349.conjugateSequence_apply
assert_no_sorry Stage1Instances.THM_M_0349.norm_conjugateSequence_le
assert_no_sorry Stage1Instances.THM_M_0349.conjugateL2
assert_no_sorry Stage1Instances.THM_M_0349.fourierCoeff_conjugateL2
assert_no_sorry Stage1Instances.THM_M_0349.norm_conjugateL2_le
assert_no_sorry Stage1Instances.THM_M_0349.conjugate_l2_bound
assert_no_sorry Stage1Instances.THM_M_0349.root_of_conjugate_packages

#print axioms Stage1Instances.THM_M_0349.conjugate_l2_bound
#print axioms Stage1Instances.THM_M_0349.root_of_conjugate_packages

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0349.conjugate_l2_bound,
    ``Stage1Instances.THM_M_0349.root_of_conjugate_packages
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

end Stage1Instances.THM_M_0349.Validation
