import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0657 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the two unconditional proof-phase claims through separately
written terms and checks the terminal binder composition from an explicit
uniqueness-transfer premise. It does not implement that premise or prove
Morley's categoricity theorem.
-/

namespace Stage1Instances.THM_M_0657.Validation

open FirstOrder FirstOrder.Language
open Stage1Instances.THM_M_0657

universe u v w

/-- A separately written exact-cardinality construction replaying mathlib's
Lowenheim-Skolem consequence without importing the proof module. -/
theorem differentialHasModelCardinality
    {L : Language.{u, v}} {T : L.Theory} {kappa lambda : Cardinal.{w}}
    (hL : L.card <= Cardinal.aleph0)
    (hkappa : Cardinal.aleph0 < kappa)
    (hcat : CategoricalWithExistence L T kappa)
    (hlambda : Cardinal.aleph0 < lambda) :
    HasModelCardinality L T lambda := by
  obtain ⟨M, hM⟩ := hcat.1
  haveI : Infinite M := Cardinal.infinite_iff.mpr (hkappa.le.trans_eq hM.symm)
  obtain ⟨N, hN, rfl⟩ := exists_elementarilyEquivalent_card_eq L M lambda
    hlambda.le
    ((Cardinal.lift_le.mpr hL).trans
      (by simpa only [Cardinal.lift_aleph0] using Cardinal.lift_le.mpr hlambda.le))
  haveI : Nonempty N := hN.nonempty
  exact ⟨hN.theory_model.bundled, rfl⟩

/-- Directly transport source categoricity to the theory of infinite
`T`-models. -/
theorem differentialInfinitePartCategorical
    {L : Language.{u, v}} {T : L.Theory} {kappa : Cardinal.{w}}
    (hcat : CategoricalWithExistence L T kappa) :
    Cardinal.Categorical kappa (T ∪ L.infiniteTheory) := by
  intro M N hM hN
  exact hcat.2
    (M.subtheoryModel Set.subset_union_left)
    (N.subtheoryModel Set.subset_union_left)
    hM hN

/-- A no-import reimplementation of the Los-Vaught completeness reduction
for the infinite-model part of the theory. -/
theorem differentialInfinitePartIsComplete
    {L : Language.{u, v}} {T : L.Theory} {kappa : Cardinal.{w}}
    (hL : L.card <= Cardinal.aleph0)
    (hkappa : Cardinal.aleph0 < kappa)
    (hcat : CategoricalWithExistence L T kappa) :
    (T ∪ L.infiniteTheory).IsComplete := by
  obtain ⟨M, hM⟩ := hcat.1
  haveI : Infinite M := Cardinal.infinite_iff.mpr (hkappa.le.trans_eq hM.symm)
  have hSat : (T ∪ L.infiniteTheory).IsSatisfiable := by
    letI : M ⊨ T ∪ L.infiniteTheory := Theory.Model.union M.is_model inferInstance
    exact Theory.Model.isSatisfiable M
  have hAllInfinite :
      ∀ N : Theory.ModelType.{u, v, max u v} (T ∪ L.infiniteTheory), Infinite N := by
    intro N
    exact (model_infiniteTheory_iff L).mp (Theory.model_union_iff.mp N.is_model).2
  exact (differentialInfinitePartCategorical hcat).isComplete kappa _ hkappa.le
    ((Cardinal.lift_le.mpr hL).trans
      (by simpa only [Cardinal.lift_aleph0] using Cardinal.lift_le.mpr hkappa.le))
    hSat hAllInfinite

/-- The still-open semantic cut, restated locally so this probe need not
import the proof implementation. -/
def DifferentialUniquenessTransfer : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    L.card <= Cardinal.aleph0 ->
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa ->
      CategoricalWithExistence L T kappa ->
      ∀ lambda : Cardinal.{w}, Cardinal.aleph0 < lambda ->
        Cardinal.Categorical lambda T

/-- Differential terminal composition. The uniqueness-transfer argument is
an explicit premise and receives no closure credit. -/
theorem differentialConditionalRoot
    (huniq : DifferentialUniquenessTransfer.{u, v, w}) :
    MorleyCategoricityTarget.{u, v, w} := by
  intro L T hL kappa hkappa hcat lambda hlambda
  exact ⟨differentialHasModelCardinality hL hkappa hcat hlambda,
    huniq L T hL kappa hkappa hcat lambda hlambda⟩

assert_no_sorry differentialHasModelCardinality
assert_no_sorry differentialInfinitePartCategorical
assert_no_sorry differentialInfinitePartIsComplete
assert_no_sorry differentialConditionalRoot

#print sorries differentialHasModelCardinality
#print sorries differentialInfinitePartCategorical
#print sorries differentialInfinitePartIsComplete
#print sorries differentialConditionalRoot

#print axioms differentialHasModelCardinality
#print axioms differentialInfinitePartCategorical
#print axioms differentialInfinitePartIsComplete
#print axioms differentialConditionalRoot

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0657.Validation.differentialHasModelCardinality,
    ``Stage1Instances.THM_M_0657.Validation.differentialInfinitePartCategorical,
    ``Stage1Instances.THM_M_0657.Validation.differentialInfinitePartIsComplete,
    ``Stage1Instances.THM_M_0657.Validation.differentialConditionalRoot
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

end Stage1Instances.THM_M_0657.Validation
