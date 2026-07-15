import DomainProof
import Mathlib.Util.PrintSorries

/-!
# THM-M-0032 validation probes

This module independently observes the transitive declaration and axiom closure of the proof-phase
regular-local domain package and the frozen conditional root composition. It does not provide the
missing prime-element package and therefore does not close the UFD root.
-/

namespace Stage1Instances.THM_M_0032.Validation

open Stage1Instances.THM_M_0032.DomainProof
open Stage1Instances.THM_M_0032.ObligationTree

assert_no_sorry regularLocalRing_isDomain
assert_no_sorry regularLocalDomainPackage
assert_no_sorry pinnedKaplanskyCriterionPackage
assert_no_sorry root_of_domain_primeElement_and_kaplansky

#print sorries regularLocalRing_isDomain
#print sorries regularLocalDomainPackage
#print sorries pinnedKaplanskyCriterionPackage
#print sorries root_of_domain_primeElement_and_kaplansky
#print axioms regularLocalRing_isDomain
#print axioms regularLocalDomainPackage
#print axioms pinnedKaplanskyCriterionPackage
#print axioms root_of_domain_primeElement_and_kaplansky

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0032.DomainProof.regularLocalRing_isDomain,
    ``Stage1Instances.THM_M_0032.DomainProof.regularLocalDomainPackage,
    ``Stage1Instances.THM_M_0032.ObligationTree.pinnedKaplanskyCriterionPackage,
    ``Stage1Instances.THM_M_0032.ObligationTree.root_of_domain_primeElement_and_kaplansky
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
  logInfo m!"VALIDATION_CLOSURE roots={roots.size} declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0032.Validation
