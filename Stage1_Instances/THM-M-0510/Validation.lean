import Statement
import Mathlib.Combinatorics.Enumerative.Partition.Glaisher
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries
import ImportGraph.Imports.RequiredModules

/-!
# THM-M-0510 differential validation probe

This module imports neither `Proof` nor `ObligationTree`. It separately
reconstructs the ordinary-partition Euler-product normalization from the
pinned mathlib interfaces. It does not prove the Hardy-Ramanujan asymptotic.
-/

set_option autoImplicit false

noncomputable section

open scoped PowerSeries.WithPiTopology

namespace Stage1Instances.THM_M_0510.Validation

open PowerSeries
open Stage1Instances.THM_M_0510

/-- A separately declared copy of the ordinary partition series. -/
def validationPartitionSeries : Real⟦X⟧ :=
  PowerSeries.mk partitionCount

/-- Separate coefficient check for the validation copy. -/
@[simp]
theorem differentialCoeffValidationPartitionSeries (n : Nat) :
    validationPartitionSeries.coeff n = partitionCount n := by
  simp [validationPartitionSeries]

/-- Same-worker, no-`Proof` reconstruction of the reciprocal Euler product.
This validates only the frozen normalization obligation. -/
theorem differentialOrdinaryPartitionSeriesMulEulerProduct :
    validationPartitionSeries *
      ∏' i : Nat, (1 - (X : Real⟦X⟧) ^ (i + 1)) = 1 := by
  have hfactor (i : Nat) :
      (∑' j : Nat, (X : Real⟦X⟧) ^ ((i + 1) * j)) *
        (1 - X ^ (i + 1)) = 1 := by
    simpa [pow_mul] using
      (PowerSeries.WithPiTopology.tsum_pow_mul_one_sub_of_constantCoeff_eq_zero
        (f := (X : Real⟦X⟧) ^ (i + 1)) (by simp))
  have hprod :
      HasProd
        (fun i : Nat => ∑' j : Nat, (X : Real⟦X⟧) ^ ((i + 1) * j))
        validationPartitionSeries := by
    simpa [validationPartitionSeries, partitionCount, Nat.Partition.restricted] using
      (Nat.Partition.hasProd_powerSeriesMk_card_restricted Real (fun _ => True))
  rw [hprod.tprod_eq.symm]
  rw [← hprod.multipliable.tprod_mul
    (PowerSeries.WithPiTopology.multipliable_one_sub_X_pow Real)]
  simpa using tprod_congr (fun i => hfactor i)

#check differentialCoeffValidationPartitionSeries
#check differentialOrdinaryPartitionSeriesMulEulerProduct

assert_no_sorry differentialCoeffValidationPartitionSeries
assert_no_sorry differentialOrdinaryPartitionSeriesMulEulerProduct

#print sorries differentialCoeffValidationPartitionSeries
  differentialOrdinaryPartitionSeriesMulEulerProduct

#print axioms differentialCoeffValidationPartitionSeries
#print axioms differentialOrdinaryPartitionSeriesMulEulerProduct

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0510.Validation.differentialCoeffValidationPartitionSeries,
    ``Stage1Instances.THM_M_0510.Validation.differentialOrdinaryPartitionSeriesMulEulerProduct
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

end Stage1Instances.THM_M_0510.Validation
