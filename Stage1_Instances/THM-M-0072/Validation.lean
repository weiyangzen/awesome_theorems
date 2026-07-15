import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0072 validation probe

This module rechecks the proof phase's exact Thompson-transfer declarations and
their transitive Lean environment. It adds only exact-type aliases and trust
inspection commands; it does not add a second mathematical proof.

The probe runs in the validation worker and shares the pinned dependency
artifacts, so it is not the distinct-runner attestation required for release.
-/

namespace Stage1Instances.THM_M_0072.Validation

open Stage1Instances.THM_M_0072
open Stage1Instances.THM_M_0072.ObligationTree

universe u

/-- Exact-type replay of the proof phase's outside-maximal terminal. -/
theorem exactOutsideReplay : TransferOutsideTarget.{u} :=
  Proof.outsideTransferConclusion

/-- Exact-type replay of the unchanged canonical root. -/
theorem exactRootReplay : ThompsonTransferLemmaTarget.{u} :=
  Proof.thompsonTransferLemma_proof

assert_no_sorry insideMaximalConclusion
assert_no_sorry assembly_of_outside_and_inside
assert_no_sorry root_of_assembly
assert_no_sorry root_of_outsideTransfer
assert_no_sorry Proof.maximal_normal_of_pgroup
assert_no_sorry Proof.quotient_isSimpleGroup_of_isCoatom
assert_no_sorry Proof.maximal_index_prime_of_pgroup
assert_no_sorry Proof.maximal_index_two_of_2group
assert_no_sorry Proof.period_eq_one_or_two
assert_no_sorry Proof.quotient_eq_of_both_not_mem
assert_no_sorry Proof.outsideTransferConclusion
assert_no_sorry Proof.thompsonTransferLemma_proof
assert_no_sorry exactOutsideReplay
assert_no_sorry exactRootReplay

#print sorries insideMaximalConclusion
#print sorries assembly_of_outside_and_inside
#print sorries root_of_assembly
#print sorries root_of_outsideTransfer
#print sorries Proof.maximal_normal_of_pgroup
#print sorries Proof.quotient_isSimpleGroup_of_isCoatom
#print sorries Proof.maximal_index_prime_of_pgroup
#print sorries Proof.maximal_index_two_of_2group
#print sorries Proof.period_eq_one_or_two
#print sorries Proof.quotient_eq_of_both_not_mem
#print sorries Proof.outsideTransferConclusion
#print sorries Proof.thompsonTransferLemma_proof
#print sorries exactOutsideReplay
#print sorries exactRootReplay

#print axioms insideMaximalConclusion
#print axioms assembly_of_outside_and_inside
#print axioms root_of_assembly
#print axioms root_of_outsideTransfer
#print axioms Proof.maximal_normal_of_pgroup
#print axioms Proof.quotient_isSimpleGroup_of_isCoatom
#print axioms Proof.maximal_index_prime_of_pgroup
#print axioms Proof.maximal_index_two_of_2group
#print axioms Proof.period_eq_one_or_two
#print axioms Proof.quotient_eq_of_both_not_mem
#print axioms Proof.outsideTransferConclusion
#print axioms Proof.thompsonTransferLemma_proof
#print axioms exactOutsideReplay
#print axioms exactRootReplay

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0072.Proof.outsideTransferConclusion,
    ``Stage1Instances.THM_M_0072.Proof.thompsonTransferLemma_proof,
    ``Stage1Instances.THM_M_0072.Validation.exactOutsideReplay,
    ``Stage1Instances.THM_M_0072.Validation.exactRootReplay
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
      if !uniqueAxioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0072.Validation
