import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0890 validation probe

This module rechecks the proof phase's exact terminal obligations and canonical root. It adds only
exact-type aliases and a transitive Lean-environment inspection; it adds no mathematical proof.

The probe runs in this validation worker and shares the pinned dependency artifacts. It is not the
distinct signed runner or independently implemented verifier required for release.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0890_Validation

open Stage1Instances.THM_M_0890
open Stage1Instances.THM_M_0890_Obligations
open Stage1Instances.THM_M_0890_Proof

universe u

/-- Exact-type replay of the proof phase's division-free terminal. -/
theorem exactDivisionFreeReplay : DivisionFreeInequalityTarget.{u} :=
  divisionFreeInequality_proof

/-- Exact-type replay of the proof phase's unchanged canonical root. -/
theorem exactRootReplay : HoffmanRatioBoundTarget.{u} :=
  hoffmanRatioBound_proof

assert_no_sorry leastAdjacencyEigenvalue_le_eigenvalue
assert_no_sorry leastAdjacencyEigenvalue_neg
assert_no_sorry denominatorPositive_proof
assert_no_sorry shiftedAdjacency_posSemidef
assert_no_sorry independentSet_adjacency_quadratic_zero
assert_no_sorry independentSet_characteristic_norm
assert_no_sorry regular_adjacency_mulVec_one
assert_no_sorry independentSet_adjacency_one
assert_no_sorry one_dotProduct_one_real
assert_no_sorry centered_shifted_quadratic
assert_no_sorry independentSet_scalar_nonnegative
assert_no_sorry indepNum_pos
assert_no_sorry maximumIndependentSetEstimate_proof
assert_no_sorry divisionFreeInequality_proof
assert_no_sorry ratioAssembly_proof
assert_no_sorry hoffmanRatioBound_proof
assert_no_sorry exactDivisionFreeReplay
assert_no_sorry exactRootReplay

#print sorries leastAdjacencyEigenvalue_le_eigenvalue
#print sorries leastAdjacencyEigenvalue_neg
#print sorries denominatorPositive_proof
#print sorries shiftedAdjacency_posSemidef
#print sorries independentSet_adjacency_quadratic_zero
#print sorries independentSet_characteristic_norm
#print sorries regular_adjacency_mulVec_one
#print sorries independentSet_adjacency_one
#print sorries one_dotProduct_one_real
#print sorries centered_shifted_quadratic
#print sorries independentSet_scalar_nonnegative
#print sorries indepNum_pos
#print sorries maximumIndependentSetEstimate_proof
#print sorries divisionFreeInequality_proof
#print sorries ratioAssembly_proof
#print sorries hoffmanRatioBound_proof
#print sorries exactDivisionFreeReplay
#print sorries exactRootReplay

#print axioms leastAdjacencyEigenvalue_le_eigenvalue
#print axioms leastAdjacencyEigenvalue_neg
#print axioms denominatorPositive_proof
#print axioms shiftedAdjacency_posSemidef
#print axioms independentSet_adjacency_quadratic_zero
#print axioms independentSet_characteristic_norm
#print axioms regular_adjacency_mulVec_one
#print axioms independentSet_adjacency_one
#print axioms one_dotProduct_one_real
#print axioms centered_shifted_quadratic
#print axioms independentSet_scalar_nonnegative
#print axioms indepNum_pos
#print axioms maximumIndependentSetEstimate_proof
#print axioms divisionFreeInequality_proof
#print axioms ratioAssembly_proof
#print axioms hoffmanRatioBound_proof
#print axioms exactDivisionFreeReplay
#print axioms exactRootReplay

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0890_Proof.divisionFreeInequality_proof,
    ``Stage1Instances.THM_M_0890_Proof.hoffmanRatioBound_proof,
    ``Stage1Instances.THM_M_0890_Validation.exactDivisionFreeReplay,
    ``Stage1Instances.THM_M_0890_Validation.exactRootReplay
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut unexpectedAxioms : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !uniqueAxioms.contains name then unexpectedAxioms := unexpectedAxioms.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unexpected_axioms={unexpectedAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0890_Validation
