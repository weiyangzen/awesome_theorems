import Statement
import ObligationTree

/-!
# THM-M-0276 proof-phase installation

This module installs the three transparent Banach open-mapping proof bodies from the pinned
mathlib revision, specializes the terminal theorem to the exact real and complex branches, and
checks both direct and frozen-composition proofs of the canonical conjunction. The semantic
substeps remain in the upstream transparent declarations rather than being copied into aliases.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0276.Proof

open Stage1Instances.THM_M_0276

universe u v k l

/-- The pinned Baire-category approximation body at its exact generic interface. -/
theorem pinnedApproximatePreimage
    {𝕜 : Type k} {𝕜' : Type l}
    [NontriviallyNormedField 𝕜] [NontriviallyNormedField 𝕜']
    {σ : 𝕜 →+* 𝕜'} {σ' : 𝕜' →+* 𝕜}
    [RingHomInvPair σ σ'] [RingHomIsometric σ] [RingHomIsometric σ']
    {E : Type u} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace 𝕜' F] [CompleteSpace F]
    (f : E →SL[σ] F) (surj : Function.Surjective f) :
    ∃ C ≥ 0, ∀ y, ∃ x, dist (f x) y ≤ 1 / 2 * ‖y‖ ∧ ‖x‖ ≤ C * ‖y‖ := by
  exact ContinuousLinearMap.exists_approx_preimage_norm_le f surj

/-- The pinned residual-series body producing exact controlled preimages. -/
theorem pinnedExactPreimage
    {𝕜 : Type k} {𝕜' : Type l}
    [NontriviallyNormedField 𝕜] [NontriviallyNormedField 𝕜']
    {σ : 𝕜 →+* 𝕜'} {σ' : 𝕜' →+* 𝕜}
    [RingHomInvPair σ σ'] [RingHomIsometric σ] [RingHomIsometric σ']
    {E : Type u} [NormedAddCommGroup E] [NormedSpace 𝕜 E] [CompleteSpace E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace 𝕜' F] [CompleteSpace F]
    (f : E →SL[σ] F) (surj : Function.Surjective f) :
    ∃ C > 0, ∀ y, ∃ x, f x = y ∧ ‖x‖ ≤ C * ‖y‖ := by
  exact ContinuousLinearMap.exists_preimage_norm_le f surj

/-- The pinned terminal body turning controlled preimages into an open map. -/
theorem pinnedOpenMap
    {𝕜 : Type k} {𝕜' : Type l}
    [NontriviallyNormedField 𝕜] [NontriviallyNormedField 𝕜']
    {σ : 𝕜 →+* 𝕜'} {σ' : 𝕜' →+* 𝕜}
    [RingHomInvPair σ σ'] [RingHomIsometric σ] [RingHomIsometric σ']
    {E : Type u} [NormedAddCommGroup E] [NormedSpace 𝕜 E] [CompleteSpace E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace 𝕜' F] [CompleteSpace F]
    (f : E →SL[σ] F) (surj : Function.Surjective f) : IsOpenMap f := by
  exact ContinuousLinearMap.isOpenMap f surj

/-- The generic pinned terminal installed at the obligation tree's literal interface. -/
theorem pinnedMathlibTerminal :
    Stage1Instances.THM_M_0276_Obligations.MathlibTerminal.{u, v, k, l} := by
  intro 𝕜 𝕜' _ _ σ σ' _ _ _ E _ _ _ F _ _ _ f surj
  exact pinnedOpenMap f surj

/-- Exact real branch, including the original completeness and surjectivity boundary. -/
theorem realOpenMapping : RealOpenMappingTarget.{u, v} := by
  intro E F _ _ _ _ _ _ f surj
  exact pinnedOpenMap f surj

/-- Exact complex branch, including the original completeness and surjectivity boundary. -/
theorem complexOpenMapping : ComplexOpenMappingTarget.{u, v} := by
  intro E F _ _ _ _ _ _ f surj
  exact pinnedOpenMap f surj

/-- The exact source-selected root assembled directly from its two scalar branches. -/
theorem banachOpenMapping_direct : BanachOpenMappingTarget.{u, v} :=
  ⟨realOpenMapping, complexOpenMapping⟩

/-- The exact root obtained through both frozen abstract children and their checked composer. -/
theorem banachOpenMapping_via_frozen_composition : BanachOpenMappingTarget.{u, v} := by
  exact Stage1Instances.THM_M_0276_Obligations.compose_root
    Stage1Instances.THM_M_0276_Obligations.terminal_adapter pinnedMathlibTerminal

/-- Corroborating closure of the statement phase's definitionally expanded open-image target. -/
theorem expandedBanachOpenMapping : ExpandedOpenMappingTarget.{u, v} :=
  banachOpenMappingTarget_iff_expandedOpenMappingTarget.mp
    banachOpenMapping_via_frozen_composition

assert_no_sorry ContinuousLinearMap.exists_approx_preimage_norm_le
assert_no_sorry ContinuousLinearMap.exists_preimage_norm_le
assert_no_sorry ContinuousLinearMap.isOpenMap
assert_no_sorry pinnedApproximatePreimage
assert_no_sorry pinnedExactPreimage
assert_no_sorry pinnedOpenMap
assert_no_sorry pinnedMathlibTerminal
assert_no_sorry realOpenMapping
assert_no_sorry complexOpenMapping
assert_no_sorry banachOpenMapping_direct
assert_no_sorry banachOpenMapping_via_frozen_composition
assert_no_sorry expandedBanachOpenMapping

#print sorries ContinuousLinearMap.exists_approx_preimage_norm_le
#print sorries ContinuousLinearMap.exists_preimage_norm_le
#print sorries ContinuousLinearMap.isOpenMap
#print sorries pinnedApproximatePreimage
#print sorries pinnedExactPreimage
#print sorries pinnedOpenMap
#print sorries pinnedMathlibTerminal
#print sorries realOpenMapping
#print sorries complexOpenMapping
#print sorries banachOpenMapping_direct
#print sorries banachOpenMapping_via_frozen_composition
#print sorries expandedBanachOpenMapping

#print axioms ContinuousLinearMap.exists_approx_preimage_norm_le
#print axioms ContinuousLinearMap.exists_preimage_norm_le
#print axioms ContinuousLinearMap.isOpenMap
#print axioms pinnedApproximatePreimage
#print axioms pinnedExactPreimage
#print axioms pinnedOpenMap
#print axioms pinnedMathlibTerminal
#print axioms realOpenMapping
#print axioms complexOpenMapping
#print axioms banachOpenMapping_direct
#print axioms banachOpenMapping_via_frozen_composition
#print axioms expandedBanachOpenMapping

end Stage1Instances.THM_M_0276.Proof
