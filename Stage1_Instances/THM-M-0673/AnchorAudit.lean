import Mathlib.ModelTheory.Ultraproducts
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0673 immutable mathlib anchor audit

This module copies the frozen sentence target and checks it against the theorem
at the repository's pinned mathlib revision. It is anchor-audit evidence only;
the proof, validation, release, and master-acceptance phases remain downstream.
-/

namespace Stage1Instances.THM_M_0673_AnchorAudit

open Filter FirstOrder

universe u v w x

/-- A literal copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  ∀ (I : Type u) (M : I → Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)]
    (phi : L.Sentence),
      (U : Filter I).Product M ⊨ phi ↔ ∀ᶠ i : I in U, M i ⊨ phi

/-- Exact audit wrapper over the pinned mathlib terminal theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u, v, w, x} := by
  intro I M U L _ _ phi
  exact FirstOrder.Language.Ultraproduct.sentence_realize phi

#check FirstOrder.Language.Ultraproduct.sentence_realize
#check @FirstOrder.Language.Ultraproduct.sentence_realize
#check FirstOrder.Language.Ultraproduct.realize_formula_cast
#check FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast

#print FirstOrder.Language.Ultraproduct.sentence_realize
#print FirstOrder.Language.Ultraproduct.realize_formula_cast
#print FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast

assert_no_sorry FirstOrder.Language.Ultraproduct.sentence_realize
assert_no_sorry FirstOrder.Language.Ultraproduct.realize_formula_cast
assert_no_sorry FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
assert_no_sorry exactTarget_mathlib_candidate

#print sorries FirstOrder.Language.Ultraproduct.sentence_realize
#print sorries FirstOrder.Language.Ultraproduct.realize_formula_cast
#print sorries FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
#print sorries exactTarget_mathlib_candidate

#print axioms FirstOrder.Language.Ultraproduct.sentence_realize
#print axioms FirstOrder.Language.Ultraproduct.realize_formula_cast
#print axioms FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast
#print axioms exactTarget_mathlib_candidate

open Lean Elab Command in
elab "#print_anchor_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``FirstOrder.Language.Ultraproduct.sentence_realize,
    ``FirstOrder.Language.Ultraproduct.realize_formula_cast,
    ``FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast,
    ``Stage1Instances.THM_M_0673_AnchorAudit.exactTarget_mathlib_candidate
  ]
  let closure ← NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms ← roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env ← getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info ← getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"ANCHOR_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"ANCHOR_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"ANCHOR_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"ANCHOR_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_anchor_closure

set_option pp.all true in
#print ExactTarget

end Stage1Instances.THM_M_0673_AnchorAudit
