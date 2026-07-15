import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1056 validation audit

This module audits the pinned external terminal, the checked coordinate/projection transport, and
both public inhabitants of the exact frozen target. It deliberately adds no mathematical proof.
It is a same-worker trust probe, not an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_1056.Validation

#check Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget
#check ErgodicTheory.oseledets_splitting
#check Stage1Instances.THM_M_1056.external_oseledets_on_arbitrary_fiber_coordinates
#check Stage1Instances.THM_M_1056.measurableObliqueProjectionPackage
#check Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target
#check Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic
#check Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget

assert_no_sorry ErgodicTheory.oseledets_splitting
assert_no_sorry Stage1Instances.THM_M_1056.external_oseledets_on_arbitrary_fiber_coordinates
assert_no_sorry Stage1Instances.THM_M_1056.measurableObliqueProjectionPackage
assert_no_sorry Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target
assert_no_sorry Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic
assert_no_sorry Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget

#print sorries ErgodicTheory.oseledets_splitting
#print sorries Stage1Instances.THM_M_1056.external_oseledets_on_arbitrary_fiber_coordinates
#print sorries Stage1Instances.THM_M_1056.measurableObliqueProjectionPackage
#print sorries Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target
#print sorries Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic
#print sorries Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget

#print axioms ErgodicTheory.oseledets_splitting
#print axioms Stage1Instances.THM_M_1056.external_oseledets_on_arbitrary_fiber_coordinates
#print axioms Stage1Instances.THM_M_1056.measurableObliqueProjectionPackage
#print axioms Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target
#print axioms Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic
#print axioms Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``ErgodicTheory.oseledets_splitting,
    ``Stage1Instances.THM_M_1056.external_oseledets_on_arbitrary_fiber_coordinates,
    ``Stage1Instances.THM_M_1056.measurableObliqueProjectionPackage,
    ``Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target,
    ``Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic,
    ``Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget
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

end Stage1Instances.THM_M_1056.Validation
