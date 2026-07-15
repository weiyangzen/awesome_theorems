import Statement
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0657 proof-phase progress

This module implements the exact-cardinality model-existence branch and the
Los-Vaught completeness reduction for the infinite-model part of the theory.
It also checks the final conjunction and binder composition from a still-open
categoricity-transfer premise.  It does not implement Morley rank, stability,
saturation, or saturated-model uniqueness, so it does not prove the root.
-/

namespace Stage1Instances.THM_M_0657

open FirstOrder FirstOrder.Language

universe u v w

/-- Frozen obligation `M0657-C-EXISTENCE`: a source model at an uncountable
cardinal is infinite, so Lowenheim-Skolem supplies a model at every requested
uncountable target cardinal. -/
theorem hasModelCardinality_of_uncountably_categorical
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
    (by
      exact (Cardinal.lift_le.mpr hL).trans
        (by simpa only [Cardinal.lift_aleph0] using Cardinal.lift_le.mpr hlambda.le))
  haveI : Nonempty N := hN.nonempty
  exact ⟨hN.theory_model.bundled, rfl⟩

/-- The source categoricity hypothesis also applies to the theory restricted
to infinite models.  The restriction is essential: the canonical target does
not rule out additional finite models of `T`. -/
theorem infinitePart_categorical
    {L : Language.{u, v}} {T : L.Theory} {kappa : Cardinal.{w}}
    (hcat : CategoricalWithExistence L T kappa) :
    Cardinal.Categorical kappa (T ∪ L.infiniteTheory) := by
  intro M N hM hN
  exact hcat.2
    (M.subtheoryModel Set.subset_union_left)
    (N.subtheoryModel Set.subset_union_left)
    hM hN

/-- Frozen obligation `M0657-L-COMPLETENESS`: the theory describing the
infinite `T`-models is complete.  This is the precise Los-Vaught working
context needed by an uncountable transfer proof without falsely asserting
that `T` has no finite models. -/
theorem infinitePart_isComplete
    {L : Language.{u, v}} {T : L.Theory} {kappa : Cardinal.{w}}
    (hL : L.card <= Cardinal.aleph0)
    (hkappa : Cardinal.aleph0 < kappa)
    (hcat : CategoricalWithExistence L T kappa) :
    (T ∪ L.infiniteTheory).IsComplete := by
  obtain ⟨M, hM⟩ := hcat.1
  haveI : Infinite M := Cardinal.infinite_iff.mpr (hkappa.le.trans_eq hM.symm)
  have hS : (T ∪ L.infiniteTheory).IsSatisfiable := by
    letI : M ⊨ T ∪ L.infiniteTheory := Theory.Model.union M.is_model inferInstance
    apply Theory.Model.isSatisfiable M
  have hInf :
      ∀ N : Theory.ModelType.{u, v, max u v} (T ∪ L.infiniteTheory), Infinite N := by
    intro N
    exact (model_infiniteTheory_iff L).mp (Theory.model_union_iff.mp N.is_model).2
  exact (infinitePart_categorical hcat).isComplete kappa _ hkappa.le
    ((Cardinal.lift_le.mpr hL).trans
      (by simpa only [Cardinal.lift_aleph0] using Cardinal.lift_le.mpr hkappa.le))
    hS hInf

/-- Pointwise terminal composition for `M0657-T-TARGET-CAT`.  The existence
half is implemented above; the uniqueness half remains an explicit premise
until the stability/saturation branch is formalized. -/
theorem categoricalWithExistence_of_categorical
    {L : Language.{u, v}} {T : L.Theory} {kappa lambda : Cardinal.{w}}
    (hL : L.card <= Cardinal.aleph0)
    (hkappa : Cardinal.aleph0 < kappa)
    (hcat : CategoricalWithExistence L T kappa)
    (hlambda : Cardinal.aleph0 < lambda)
    (huniq : Cardinal.Categorical lambda T) :
    CategoricalWithExistence L T lambda := by
  exact ⟨hasModelCardinality_of_uncountably_categorical hL hkappa hcat hlambda, huniq⟩

/-- The remaining semantic cut after the existence branch: uniqueness in
every uncountable target cardinal. -/
def UncountableCategoricityTransfer : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    L.card <= Cardinal.aleph0 ->
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa ->
      CategoricalWithExistence L T kappa ->
      ∀ lambda : Cardinal.{w}, Cardinal.aleph0 < lambda ->
        Cardinal.Categorical lambda T

/-- Frozen terminal composition `M0657-T-ASSEMBLE`: a proof of the remaining
uniqueness transfer, together with the implemented existence construction,
yields the unchanged canonical root.  The premise receives no proof credit. -/
theorem morleyCategoricityTarget_of_categoricalTransfer
    (huniq : UncountableCategoricityTransfer.{u, v, w}) :
    MorleyCategoricityTarget.{u, v, w} := by
  intro L T hL kappa hkappa hcat lambda hlambda
  exact categoricalWithExistence_of_categorical hL hkappa hcat hlambda
    (huniq L T hL kappa hkappa hcat lambda hlambda)

#print axioms hasModelCardinality_of_uncountably_categorical
#print axioms infinitePart_categorical
#print axioms infinitePart_isComplete
#print axioms categoricalWithExistence_of_categorical
#print axioms morleyCategoricityTarget_of_categoricalTransfer

assert_no_sorry hasModelCardinality_of_uncountably_categorical
assert_no_sorry infinitePart_categorical
assert_no_sorry infinitePart_isComplete
assert_no_sorry categoricalWithExistence_of_categorical
assert_no_sorry morleyCategoricityTarget_of_categoricalTransfer

end Stage1Instances.THM_M_0657
