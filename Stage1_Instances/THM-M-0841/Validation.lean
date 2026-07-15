import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0841 validation probes

This module rechecks every proof-phase declaration and separately recomposes the exact canonical
root from the still-open dense base and induction step.  Those two products remain explicit
premises, so this is neither a proof of Erdos-Stone nor independent-runner evidence.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0841_Validation

open Stage1Instances.THM_M_0841
open Stage1Instances.THM_M_0841_Obligations
open Stage1Instances.THM_M_0841_Proof

/-- A separately written conditional route from the two missing dense products to the exact root. -/
theorem rootFromDenseProducts (base : DenseBase) (step : DenseStep) : ErdosStoneTarget := by
  apply sparseFromDense
  intro r hr
  induction r using Nat.strong_induction_on with
  | h r ih =>
      by_cases htwo : r = 2
      · simpa [DenseBase, htwo] using base
      · exact step r (by omega) (fun s hs hsr => ih s hsr hs)

assert_no_sorry cast_choose_two
assert_no_sorry card_edgeFinset_compl
assert_no_sorry sparseFromDense
assert_no_sorry denseFamily_of_base_step
assert_no_sorry erdosStone_of_dense_base_step
assert_no_sorry rootFromDenseProducts

#print sorries cast_choose_two
  card_edgeFinset_compl
  sparseFromDense
  denseFamily_of_base_step
  erdosStone_of_dense_base_step
  rootFromDenseProducts

#print axioms cast_choose_two
#print axioms card_edgeFinset_compl
#print axioms sparseFromDense
#print axioms denseFamily_of_base_step
#print axioms erdosStone_of_dense_base_step
#print axioms rootFromDenseProducts

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0841_Proof.cast_choose_two,
    ``Stage1Instances.THM_M_0841_Proof.card_edgeFinset_compl,
    ``Stage1Instances.THM_M_0841_Proof.sparseFromDense,
    ``Stage1Instances.THM_M_0841_Proof.denseFamily_of_base_step,
    ``Stage1Instances.THM_M_0841_Proof.erdosStone_of_dense_base_step,
    ``Stage1Instances.THM_M_0841_Validation.rootFromDenseProducts
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

end Stage1Instances.THM_M_0841_Validation
