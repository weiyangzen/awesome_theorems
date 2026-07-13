import ObligationTree

/-!
# THM-M-0030 proof-phase installation

This module installs the pinned mathlib bodies at the interfaces frozen in the obligation
registry. It checks the canonical root both directly and through the checked visible
child-to-parent interfaces. The deeper filtration, stability, and Nakayama steps remain the
deduplicated transparent bodies in the pinned mathlib dependency rather than copied declarations.
-/

namespace Stage1Instances.THM_M_0030.Proof

open Stage1Instances.THM_M_0030
open Stage1Instances.THM_M_0030.ObligationTree

universe u v

/-- The exact pinned Krull-intersection declaration installed at its frozen anchor interface. -/
theorem exactMathlibAnchor : ExactMathlibAnchor.{u} := by
  intro R _ I _ _ hI
  exact Ideal.iInf_pow_eq_bot_of_isLocalRing I hI

/-- The pinned finite-module specialization immediately below the ideal theorem. -/
theorem finiteModuleIntersection : FiniteModuleIntersectionTarget.{u, v} := by
  intro R M _ _ _ _ _ _ I hI
  exact Ideal.iInf_pow_smul_eq_bot_of_isLocalRing I hI

/-- The pinned Jacobson-radical form of the finite-module intersection theorem. -/
theorem jacobsonIntersection : JacobsonIntersectionTarget.{u, v} := by
  intro R M _ _ _ _ _ I hI
  exact Ideal.iInf_pow_smul_eq_bot_of_le_jacobson I hI

/-- A proper ideal in a local ring lies below its unique maximal ideal. -/
theorem properToMaximal : ProperToMaximalTarget.{u} := by
  intro R _ _ I hI
  exact IsLocalRing.le_maximalIdeal hI

/-- The unique maximal ideal lies below the Jacobson radical of the zero ideal. -/
theorem maximalToJacobson : MaximalToJacobsonTarget.{u} := by
  intro R _ _
  exact IsLocalRing.maximalIdeal_le_jacobson (⊥ : Ideal R)

/-- The exact source-shaped Jacobson unit theorem from pinned mathlib. -/
theorem jacobsonUnitSource : JacobsonUnitSourceTarget.{u} := by
  intro R _ s hs
  exact Ideal.isUnit_of_sub_one_mem_jacobson_bot s hs

/-- The fixed-point characterization carrying the filtration, stability, and Nakayama route. -/
theorem fixedPointCharacterization : FixedPointCharacterizationTarget.{u, v} := by
  intro R M _ _ _ _ _ I x
  exact Ideal.mem_iInf_smul_pow_eq_bot_iff I x

/-- Forward branch of the pinned fixed-point characterization. -/
theorem fixedPointForward : FixedPointForwardTarget.{u, v} := by
  intro R M _ _ _ _ _ I x hx
  exact (Ideal.mem_iInf_smul_pow_eq_bot_iff I x).mp hx

/-- Backward branch of the pinned fixed-point characterization. -/
theorem fixedPointBackward : FixedPointBackwardTarget.{u, v} := by
  intro R M _ _ _ _ _ I x hx
  exact (Ideal.mem_iInf_smul_pow_eq_bot_iff I x).mpr hx

/-- Frozen local-containment composition with both pinned children installed. -/
theorem localProperIdealJacobson : LocalProperIdealJacobsonTarget.{u} :=
  localProperIdealJacobson_of_bounds properToMaximal (by
    intro R _ _
    exact maximalToJacobson (R := R))

/-- Frozen sign transport from the pinned source-shaped Jacobson unit theorem. -/
theorem jacobsonUnit : JacobsonUnitTarget.{u} :=
  jacobsonUnit_of_source jacobsonUnitSource

/-- Frozen branch composition for the fixed-point equivalence. -/
theorem fixedPointCharacterization_via_branches :
    FixedPointCharacterizationTarget.{u, v} :=
  fixedPointCharacterization_of_branches fixedPointForward fixedPointBackward

/-- Jacobson intersection reconstructed through the frozen fixed-point and unit composition. -/
theorem jacobsonIntersection_via_frozen_composition :
    JacobsonIntersectionTarget.{u, v} :=
  jacobsonIntersection_of_fixedPoint fixedPointCharacterization_via_branches jacobsonUnit

/-- Local finite-module theorem reconstructed from the Jacobson and containment children. -/
theorem finiteModuleIntersection_via_frozen_composition :
    FiniteModuleIntersectionTarget.{u, v} :=
  finiteModuleIntersection_of_jacobson jacobsonIntersection_via_frozen_composition
    localProperIdealJacobson

/-- The audited exact anchor reconstructed from the finite-module route at `M = R`. -/
theorem exactMathlibAnchor_via_frozen_composition : ExactMathlibAnchor.{u} :=
  exactMathlibAnchor_of_finiteModuleIntersection
    finiteModuleIntersection_via_frozen_composition

/-- Direct exact-root wrapper over the pinned terminal theorem. -/
theorem krullIntersection_direct : KrullIntersectionTarget.{u} := by
  intro R _ _ _ I hI
  exact Ideal.iInf_pow_eq_bot_of_isLocalRing I hI

/-- Exact canonical root obtained from the pinned anchor through the frozen root adapter. -/
theorem krullIntersection_via_pinned_anchor : KrullIntersectionTarget.{u} :=
  root_of_exactMathlibAnchor exactMathlibAnchor

/-- Exact root through the checked frozen interfaces; deeper refinements remain source-mapped. -/
theorem krullIntersection_via_frozen_composition : KrullIntersectionTarget.{u} :=
  root_of_exactMathlibAnchor exactMathlibAnchor_via_frozen_composition

#print sorries Ideal.iInf_pow_eq_bot_of_isLocalRing
#print sorries Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#print sorries Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print sorries Ideal.mem_iInf_smul_pow_eq_bot_iff
#print sorries exactMathlibAnchor
#print sorries fixedPointCharacterization
#print sorries krullIntersection_direct
#print sorries krullIntersection_via_pinned_anchor
#print sorries krullIntersection_via_frozen_composition

#print axioms Ideal.iInf_pow_eq_bot_of_isLocalRing
#print axioms Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#print axioms Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print axioms Ideal.mem_iInf_smul_pow_eq_bot_iff
#print axioms exactMathlibAnchor
#print axioms finiteModuleIntersection
#print axioms jacobsonIntersection
#print axioms properToMaximal
#print axioms maximalToJacobson
#print axioms jacobsonUnitSource
#print axioms fixedPointCharacterization
#print axioms fixedPointForward
#print axioms fixedPointBackward
#print axioms localProperIdealJacobson
#print axioms jacobsonUnit
#print axioms fixedPointCharacterization_via_branches
#print axioms jacobsonIntersection_via_frozen_composition
#print axioms finiteModuleIntersection_via_frozen_composition
#print axioms exactMathlibAnchor_via_frozen_composition
#print axioms krullIntersection_direct
#print axioms krullIntersection_via_pinned_anchor
#print axioms krullIntersection_via_frozen_composition

end Stage1Instances.THM_M_0030.Proof
