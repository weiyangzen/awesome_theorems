import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0276 immutable anchor probes

This module checks the exact real-and-complex target against the pinned mathlib Banach open
mapping theorem. The wrappers are provisional anchor-audit evidence, not accepted proof-phase or
theorem-completion declarations.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0276_AnchorAudit

universe u v

/-- A literal audit-local copy of the frozen statement-phase target. -/
def ExactTarget : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Surjective f -> IsOpenMap f) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Surjective f -> IsOpenMap f)

/-- The frozen target with the open-map conclusion expanded exactly as in the statement phase. -/
def ExpandedExactTarget : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Surjective f ->
      forall U : Set E, IsOpen U -> IsOpen (f '' U)) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Surjective f ->
      forall U : Set E, IsOpen U -> IsOpen (f '' U))

/-- Checked identity with the statement phase's expanded open-image formulation. -/
theorem exactTarget_iff_expandedExactTarget :
    ExactTarget.{u, v} <-> ExpandedExactTarget.{u, v} :=
  Iff.rfl

/-- Exact real-and-complex specialization of the stronger pinned semilinear theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u, v} := by
  constructor
  · intro E F _ _ _ _ _ _ f hf
    exact ContinuousLinearMap.isOpenMap f hf
  · intro E F _ _ _ _ _ _ f hf
    exact ContinuousLinearMap.isOpenMap f hf

#check ContinuousLinearMap.exists_approx_preimage_norm_le
#check ContinuousLinearMap.exists_preimage_norm_le
#check ContinuousLinearMap.isOpenMap
#check ContinuousLinearMap.isQuotientMap

#print ContinuousLinearMap.exists_approx_preimage_norm_le
#print ContinuousLinearMap.exists_preimage_norm_le
#print ContinuousLinearMap.isOpenMap

assert_no_sorry ContinuousLinearMap.exists_approx_preimage_norm_le
assert_no_sorry ContinuousLinearMap.exists_preimage_norm_le
assert_no_sorry ContinuousLinearMap.isOpenMap
assert_no_sorry exactTarget_mathlib_candidate

#print sorries ContinuousLinearMap.exists_approx_preimage_norm_le
#print sorries ContinuousLinearMap.exists_preimage_norm_le
#print sorries ContinuousLinearMap.isOpenMap
#print sorries exactTarget_mathlib_candidate

#print axioms ContinuousLinearMap.exists_approx_preimage_norm_le
#print axioms ContinuousLinearMap.exists_preimage_norm_le
#print axioms ContinuousLinearMap.isOpenMap
#print axioms exactTarget_mathlib_candidate

open Lean Elab Command in
elab "#print_anchor_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``ContinuousLinearMap.exists_approx_preimage_norm_le,
    ``ContinuousLinearMap.exists_preimage_norm_le,
    ``ContinuousLinearMap.isOpenMap,
    ``Stage1Instances.THM_M_0276_AnchorAudit.exactTarget_mathlib_candidate
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
  logInfo m!"ANCHOR_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"ANCHOR_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"ANCHOR_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"ANCHOR_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_anchor_closure

set_option pp.universes true in
set_option pp.explicit true in
#print ExpandedExactTarget

end Stage1Instances.THM_M_0276_AnchorAudit
