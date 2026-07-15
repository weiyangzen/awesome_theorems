import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0673 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact frozen sentence root directly from the pinned mathlib
terminal declaration. This supplies a separately elaborated local adapter, not
an independent proof body or a distinct-runner attestation.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0673.Validation

open Filter FirstOrder
open Stage1Instances.THM_M_0673

universe u v w x

/-- A separately written exact-target adapter over the pinned Los theorem. -/
theorem independentlyReconstructedRoot :
    LosSentenceTarget.{u, v, w, x} := by
  intro I M U L _ _ phi
  exact FirstOrder.Language.Ultraproduct.sentence_realize phi

#check independentlyReconstructedRoot

assert_no_sorry FirstOrder.Language.Ultraproduct.funMap_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.term_realize_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.realize_formula_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.sentence_realize
assert_no_sorry Stage1Instances.THM_M_0673.principal_boundary
assert_no_sorry independentlyReconstructedRoot

#print sorries FirstOrder.Language.Ultraproduct.funMap_cast
  FirstOrder.Language.Ultraproduct.term_realize_cast
  FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
  FirstOrder.Language.Ultraproduct.realize_formula_cast
  FirstOrder.Language.Ultraproduct.sentence_realize
  Stage1Instances.THM_M_0673.principal_boundary
  independentlyReconstructedRoot

#print axioms FirstOrder.Language.Ultraproduct.funMap_cast
#print axioms FirstOrder.Language.Ultraproduct.term_realize_cast
#print axioms FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
#print axioms FirstOrder.Language.Ultraproduct.realize_formula_cast
#print axioms FirstOrder.Language.Ultraproduct.sentence_realize
#print axioms Stage1Instances.THM_M_0673.principal_boundary
#print axioms independentlyReconstructedRoot

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0673.Validation.independentlyReconstructedRoot,
    ``Stage1Instances.THM_M_0673.principal_boundary
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
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0673.Validation
