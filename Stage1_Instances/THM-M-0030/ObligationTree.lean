import Statement
import Mathlib.RingTheory.Filtration
import Mathlib.RingTheory.Jacobson.Ideal

/-!
# THM-M-0030 conditional obligation composition

This module checks the child-to-parent interfaces frozen by the obligation registry. The exact
mathlib theorem and its fixed-point characterization remain explicit premises. Installing the
pinned terminal theorem as the canonical proof belongs to the later proof phase.
-/

namespace Stage1Instances.THM_M_0030.ObligationTree

universe u v

/-- The exact proposition exported by the audited mathlib terminal declaration, with its source
binder order retained. -/
def ExactMathlibAnchor : Prop :=
  forall {R : Type u} [CommRing R] (I : Ideal R) [IsNoetherianRing R] [IsLocalRing R],
    I ≠ ⊤ -> (iInf fun n : Nat => I ^ n) = ⊥

/-- The finite-module form immediately below the exact ideal theorem. -/
def FiniteModuleIntersectionTarget : Prop :=
  forall {R : Type u} {M : Type v} [CommRing R] [AddCommGroup M] [Module R M]
    [IsNoetherianRing R] [IsLocalRing R] [Module.Finite R M] (I : Ideal R),
    I ≠ ⊤ -> (iInf fun n : Nat => I ^ n • ⊤ : Submodule R M) = ⊥

/-- The Jacobson-radical form used before the local-ring specialization. -/
def JacobsonIntersectionTarget : Prop :=
  forall {R : Type u} {M : Type v} [CommRing R] [AddCommGroup M] [Module R M]
    [IsNoetherianRing R] [Module.Finite R M] (I : Ideal R),
    I ≤ Ideal.jacobson ⊥ -> (iInf fun n : Nat => I ^ n • ⊤ : Submodule R M) = ⊥

/-- Proper ideals lie below the unique maximal ideal in a local ring. -/
def ProperToMaximalTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsLocalRing R] (I : Ideal R),
    I ≠ ⊤ -> I ≤ IsLocalRing.maximalIdeal R

/-- The maximal ideal of a local ring lies in the Jacobson radical of bottom. -/
def MaximalToJacobsonTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsLocalRing R],
    IsLocalRing.maximalIdeal R ≤ Ideal.jacobson (⊥ : Ideal R)

/-- The exact proper-local-ideal containment consumed by the finite-module composition. -/
def LocalProperIdealJacobsonTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsLocalRing R] (I : Ideal R),
    I ≠ ⊤ -> I ≤ Ideal.jacobson (⊥ : Ideal R)

/-- The fixed-point characterization at the core of the visible pinned proof body. -/
def FixedPointCharacterizationTarget : Prop :=
  forall {R : Type u} {M : Type v} [CommRing R] [AddCommGroup M] [Module R M]
    [IsNoetherianRing R] [Module.Finite R M] (I : Ideal R) (x : M),
    x ∈ (iInf fun n : Nat => I ^ n • ⊤ : Submodule R M) <->
      exists r : I, (r : R) • x = x

/-- The Jacobson unit fact consumed by the cancellation step. Keeping it separate prevents the
fixed-point characterization from hiding a second material imported theorem. -/
def JacobsonUnitTarget : Prop :=
  forall {R : Type u} [CommRing R] (r : R),
    r ∈ Ideal.jacobson (⊥ : Ideal R) -> IsUnit (1 - r)

/-- Source-shaped unit theorem used to derive `JacobsonUnitTarget`. -/
def JacobsonUnitSourceTarget : Prop :=
  forall {R : Type u} [CommRing R] (s : R),
    s - 1 ∈ Ideal.jacobson (⊥ : Ideal R) -> IsUnit s

/-- The forward branch of the pinned fixed-point characterization. -/
def FixedPointForwardTarget : Prop :=
  forall {R : Type u} {M : Type v} [CommRing R] [AddCommGroup M] [Module R M]
    [IsNoetherianRing R] [Module.Finite R M] (I : Ideal R) (x : M),
    x ∈ (iInf fun n : Nat => I ^ n • ⊤ : Submodule R M) ->
      exists r : I, (r : R) • x = x

/-- The backward branch of the pinned fixed-point characterization. -/
def FixedPointBackwardTarget : Prop :=
  forall {R : Type u} {M : Type v} [CommRing R] [AddCommGroup M] [Module R M]
    [IsNoetherianRing R] [Module.Finite R M] (I : Ideal R) (x : M),
    (exists r : I, (r : R) • x = x) ->
      x ∈ (iInf fun n : Nat => I ^ n • ⊤ : Submodule R M)

/-- Checked binder-order adapter from the audited exact anchor to the canonical root. -/
theorem root_of_exactMathlibAnchor (anchor : ExactMathlibAnchor.{u}) :
    Stage1Instances.THM_M_0030.KrullIntersectionTarget.{u} := by
  intro R _ _ _ I hI
  exact anchor I hI

/-- Checked specialization from the finite-module theorem at `M = R` to ideal powers. -/
theorem exactMathlibAnchor_of_finiteModuleIntersection
    (finiteModule : FiniteModuleIntersectionTarget.{u, u}) : ExactMathlibAnchor.{u} := by
  intro R _ I _ _ hI
  convert finiteModule (M := R) I hI
  ext n
  rw [smul_eq_mul, <- Ideal.one_eq_top, mul_one]

/-- Checked local-ring reduction through the maximal ideal and the Jacobson radical. -/
theorem finiteModuleIntersection_of_jacobson
    (jacobson : JacobsonIntersectionTarget.{u, v})
    (localContainment : LocalProperIdealJacobsonTarget.{u}) :
    FiniteModuleIntersectionTarget.{u, v} := by
  intro R M _ _ _ _ _ _ I hI
  exact jacobson I (localContainment I hI)

/-- Checked composition of the two local-ring ideal containments. -/
theorem localProperIdealJacobson_of_bounds
    (properToMaximal : ProperToMaximalTarget.{u})
    (maximalToJacobson : MaximalToJacobsonTarget.{u}) :
    LocalProperIdealJacobsonTarget.{u} := by
  intro R _ _ I hI
  exact (properToMaximal I hI).trans (maximalToJacobson (R := R))

/-- Checked sign adapter from the source-shaped Jacobson unit theorem. -/
theorem jacobsonUnit_of_source
    (source : JacobsonUnitSourceTarget.{u}) : JacobsonUnitTarget.{u} := by
  intro R _ r hr
  apply source (1 - r)
  simpa using (Ideal.jacobson (⊥ : Ideal R)).neg_mem hr

/-- Checked composition of the two visible branches into the exact fixed-point iff. -/
theorem fixedPointCharacterization_of_branches
    (forward : FixedPointForwardTarget.{u, v})
    (backward : FixedPointBackwardTarget.{u, v}) :
    FixedPointCharacterizationTarget.{u, v} := by
  intro R M _ _ _ _ _ I x
  exact ⟨forward I x, backward I x⟩

/-- Checked Jacobson composition from the fixed-point characterization and unit cancellation. -/
theorem jacobsonIntersection_of_fixedPoint
    (fixedPoint : FixedPointCharacterizationTarget.{u, v})
    (jacobsonUnit : JacobsonUnitTarget.{u}) :
    JacobsonIntersectionTarget.{u, v} := by
  intro R M _ _ _ _ _ I hI
  rw [eq_bot_iff]
  intro x hx
  obtain ⟨r, hr⟩ := (fixedPoint I x).mp hx
  have hunit := jacobsonUnit r.1 (hI r.2)
  apply hunit.smul_left_cancel.mp
  simp [sub_smul, hr]

#check Ideal.iInf_pow_eq_bot_of_isLocalRing
#check Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#check Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#check Ideal.mem_iInf_smul_pow_eq_bot_iff
#check Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul
#print axioms root_of_exactMathlibAnchor
#print axioms exactMathlibAnchor_of_finiteModuleIntersection
#print axioms finiteModuleIntersection_of_jacobson
#print axioms localProperIdealJacobson_of_bounds
#print axioms jacobsonUnit_of_source
#print axioms fixedPointCharacterization_of_branches
#print axioms jacobsonIntersection_of_fixedPoint

end Stage1Instances.THM_M_0030.ObligationTree
