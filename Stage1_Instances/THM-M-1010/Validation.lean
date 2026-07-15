import «Stage1_Instances».«THM-M-1010».Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1010 validation trust audit

This module adds no Skorokhod proof. It rechecks the proof phase's three partial
declarations and the frozen conditional composer. The exact root remains open
because no unconditional `CouplingPackage` is available.
-/

namespace Stage1Instances.THM_M_1010.Validation

assert_no_sorry Stage1Instances.THM_M_1010.exists_common_space_exact_marginals
assert_no_sorry Stage1Instances.THM_M_1010.representation_of_constant_laws
assert_no_sorry Stage1Instances.THM_M_1010.target_for_constant_sequence
assert_no_sorry Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage

#print sorries Stage1Instances.THM_M_1010.exists_common_space_exact_marginals
#print sorries Stage1Instances.THM_M_1010.representation_of_constant_laws
#print sorries Stage1Instances.THM_M_1010.target_for_constant_sequence
#print sorries Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage

#print axioms Stage1Instances.THM_M_1010.exists_common_space_exact_marginals
#print axioms Stage1Instances.THM_M_1010.representation_of_constant_laws
#print axioms Stage1Instances.THM_M_1010.target_for_constant_sequence
#print axioms Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1010.exists_common_space_exact_marginals,
    ``Stage1Instances.THM_M_1010.representation_of_constant_laws,
    ``Stage1Instances.THM_M_1010.target_for_constant_sequence,
    ``Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage
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
  logInfo m!"VALIDATION_CLOSURE roots={roots.size} declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_1010.Validation
