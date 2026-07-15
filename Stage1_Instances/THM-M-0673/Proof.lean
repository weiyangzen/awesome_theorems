import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0673 proof-phase installation

This module installs the manifest-pinned mathlib proof at the bounded-formula
interface frozen by `ObligationTree.lean`. It then checks every frozen adapter
through the exact sentence root. The direct root wrapper is a second exact-type
check over the same upstream body, not a second proof-body credit.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0673_Proof

open Filter FirstOrder
open Stage1Instances.THM_M_0673
open Stage1Instances.THM_M_0673_Obligations

universe u v w x y

/-- Install the substantive pinned induction body at the frozen bounded-formula
package interface. -/
theorem boundedFormulaRealize_pinned :
    BoundedFormulaRealizePackage.{u, v, w, x, y} := by
  intro I M U L _ _ beta n phi assign bound
  exact FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
    phi assign bound

/-- Checked bounded-formula-to-formula composition from the frozen tree. -/
theorem formulaRealize_via_frozen :
    FormulaRealizePackage.{u, v, w, x, y} :=
  formula_of_bounded boundedFormulaRealize_pinned

/-- Checked formula-to-sentence composition from the frozen tree. -/
theorem sentenceRealize_via_frozen :
    SentenceRealizePackage.{u, v, w, x} :=
  sentence_of_formula formulaRealize_via_frozen

/-- Checked sentence-to-terminal composition from the frozen tree. -/
theorem terminalRoot_via_frozen :
    TerminalRootPackage.{u, v, w, x} :=
  terminal_of_sentence sentenceRealize_via_frozen

/-- Exact canonical root through every frozen proof adapter. -/
theorem losSentence_via_frozen :
    LosSentenceTarget.{u, v, w, x} :=
  root_of_terminal terminalRoot_via_frozen

/-- Independent exact-target wrapper over the same pinned terminal body. -/
theorem losSentence_pinned :
    LosSentenceTarget.{u, v, w, x} := by
  intro I M U L _ _ phi
  exact FirstOrder.Language.Ultraproduct.sentence_realize phi

#check boundedFormulaRealize_pinned
#check formulaRealize_via_frozen
#check sentenceRealize_via_frozen
#check terminalRoot_via_frozen
#check losSentence_via_frozen
#check losSentence_pinned

assert_no_sorry FirstOrder.Language.Ultraproduct.funMap_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.term_realize_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.realize_formula_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.sentence_realize
assert_no_sorry boundedFormulaRealize_pinned
assert_no_sorry formulaRealize_via_frozen
assert_no_sorry sentenceRealize_via_frozen
assert_no_sorry terminalRoot_via_frozen
assert_no_sorry losSentence_via_frozen
assert_no_sorry losSentence_pinned

#print sorries FirstOrder.Language.Ultraproduct.funMap_cast
  FirstOrder.Language.Ultraproduct.term_realize_cast
  FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
  FirstOrder.Language.Ultraproduct.realize_formula_cast
  FirstOrder.Language.Ultraproduct.sentence_realize
  boundedFormulaRealize_pinned formulaRealize_via_frozen
  sentenceRealize_via_frozen terminalRoot_via_frozen
  losSentence_via_frozen losSentence_pinned

#print axioms FirstOrder.Language.Ultraproduct.funMap_cast
#print axioms FirstOrder.Language.Ultraproduct.term_realize_cast
#print axioms FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
#print axioms FirstOrder.Language.Ultraproduct.realize_formula_cast
#print axioms FirstOrder.Language.Ultraproduct.sentence_realize
#print axioms boundedFormulaRealize_pinned
#print axioms formulaRealize_via_frozen
#print axioms sentenceRealize_via_frozen
#print axioms terminalRoot_via_frozen
#print axioms losSentence_via_frozen
#print axioms losSentence_pinned

open Lean Elab Command in
elab "#print_proof_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0673_Proof.boundedFormulaRealize_pinned,
    ``Stage1Instances.THM_M_0673_Proof.losSentence_via_frozen,
    ``Stage1Instances.THM_M_0673_Proof.losSentence_pinned
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
  logInfo m!"PROOF_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"PROOF_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"PROOF_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"PROOF_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_proof_closure

end Stage1Instances.THM_M_0673_Proof
