import Proof
import ObligationTree
import ProofProgress20260715Slot21
import ProofDirectSum20260715Head5bb51543Slot21
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0005 validation probe

This module checks every extant local proof or composition declaration without adding a Kunneth
proof. In particular, `root_compose` and `kunnethFormula_of_fields` remain conditional on the
missing Kunneth construction, exactness, and naturality families. This probe therefore supplies no
premise-free inhabitant of the canonical root.
-/

namespace AwesomeTheorems.Stage1.THM_M_0005.Validation

assert_no_sorry Proof.singularChains_projective
assert_no_sorry Proof.tensorMap
assert_no_sorry Proof.tensorMap_component
assert_no_sorry Proof.torMap
assert_no_sorry Proof.torMap_component

assert_no_sorry ProofProgress20260715Slot21.singularChains_free
assert_no_sorry ProofProgress20260715Slot21.singularChains_free_and_projective
assert_no_sorry ProofProgress20260715Slot21.tensorMap_id
assert_no_sorry ProofProgress20260715Slot21.tensorMap_comp
assert_no_sorry ProofProgress20260715Slot21.torMap_id
assert_no_sorry ProofProgress20260715Slot21.torMap_comp
assert_no_sorry ProofProgress20260715Slot21.kunnethFormula_of_fields

assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_apply
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_symm_apply
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torDegrees_zero_empty
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torTerm_zero_isZero
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_hom_ι
assert_no_sorry ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_inv_ι

assert_no_sorry ObligationTree.assemble_sequence
assert_no_sorry ObligationTree.root_compose

#print sorries Proof.singularChains_projective
#print sorries Proof.tensorMap
#print sorries Proof.tensorMap_component
#print sorries Proof.torMap
#print sorries Proof.torMap_component

#print sorries ProofProgress20260715Slot21.singularChains_free
#print sorries ProofProgress20260715Slot21.singularChains_free_and_projective
#print sorries ProofProgress20260715Slot21.tensorMap_id
#print sorries ProofProgress20260715Slot21.tensorMap_comp
#print sorries ProofProgress20260715Slot21.torMap_id
#print sorries ProofProgress20260715Slot21.torMap_comp
#print sorries ProofProgress20260715Slot21.kunnethFormula_of_fields

#print sorries ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_apply
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_symm_apply
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torDegrees_zero_empty
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torTerm_zero_isZero
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_hom_ι
#print sorries ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_inv_ι

#print sorries ObligationTree.assemble_sequence
#print sorries ObligationTree.root_compose

#print axioms Proof.singularChains_projective
#print axioms Proof.tensorMap
#print axioms Proof.tensorMap_component
#print axioms Proof.torMap
#print axioms Proof.torMap_component

#print axioms ProofProgress20260715Slot21.singularChains_free
#print axioms ProofProgress20260715Slot21.singularChains_free_and_projective
#print axioms ProofProgress20260715Slot21.tensorMap_id
#print axioms ProofProgress20260715Slot21.tensorMap_comp
#print axioms ProofProgress20260715Slot21.torMap_id
#print axioms ProofProgress20260715Slot21.torMap_comp
#print axioms ProofProgress20260715Slot21.kunnethFormula_of_fields

#print axioms ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_apply
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_symm_apply
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torDegrees_zero_empty
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torTerm_zero_isZero
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_hom_ι
#print axioms ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_inv_ι

#print axioms ObligationTree.assemble_sequence
#print axioms ObligationTree.root_compose

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Proof.singularChains_projective,
    ``Proof.tensorMap,
    ``Proof.tensorMap_component,
    ``Proof.torMap,
    ``Proof.torMap_component,
    ``ProofProgress20260715Slot21.singularChains_free,
    ``ProofProgress20260715Slot21.singularChains_free_and_projective,
    ``ProofProgress20260715Slot21.tensorMap_id,
    ``ProofProgress20260715Slot21.tensorMap_comp,
    ``ProofProgress20260715Slot21.torMap_id,
    ``ProofProgress20260715Slot21.torMap_comp,
    ``ProofProgress20260715Slot21.kunnethFormula_of_fields,
    ``ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees,
    ``ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_apply,
    ``ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_symm_apply,
    ``ProofDirectSum20260715Head5bb51543Slot21.torDegrees_zero_empty,
    ``ProofDirectSum20260715Head5bb51543Slot21.torTerm_zero_isZero,
    ``ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso,
    ``ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_hom_ι,
    ``ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_inv_ι,
    ``ObligationTree.assemble_sequence,
    ``ObligationTree.root_compose
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

end AwesomeTheorems.Stage1.THM_M_0005.Validation
