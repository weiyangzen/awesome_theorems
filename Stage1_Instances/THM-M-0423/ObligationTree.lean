import Mathlib.RingTheory.TensorProduct.Basic
import Mathlib.RingTheory.Flat.FaithfullyFlat.Algebra
import Statement

/-!
# THM-M-0423 conditional obligation composition

This module checks the exact high-level decomposition of the frozen
Hasse-Minkowski proposition.  The difficult local-to-global implication is an
explicit hypothesis.  No declaration here supplies that hypothesis.
-/

noncomputable section

namespace Stage1.THM_M_0423.ObligationTree

universe u v

open TensorProduct

/-- The functorial global-to-local direction, stated against the exact frozen
finite- and infinite-place predicates. -/
def GlobalToLocalObligation : Prop :=
  forall (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V),
    IsIsotropic Q ->
      IsIsotropicAtEveryFinitePlace Q /\ IsIsotropicAtEveryInfinitePlace Q

/-- The hard Hasse-Minkowski direction.  It is deliberately only a proposition
in this architecture phase. -/
def LocalToGlobalObligation : Prop :=
  forall (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V),
    Q.Nondegenerate ->
      IsIsotropicAtEveryFinitePlace Q ->
      IsIsotropicAtEveryInfinitePlace Q ->
      IsIsotropic Q

/-- The exact pair of directional obligations used to compose the root. -/
def DirectionPackage : Prop :=
  GlobalToLocalObligation.{u, v} /\ LocalToGlobalObligation.{u, v}

/-- Scalar extension preserves a nonzero isotropic witness over a field
extension.  This is infrastructure only, not the local-to-global theorem. -/
theorem isotropic_after_baseChange
    {K A : Type u} {V : Type v}
    [Field K] [Field A] [Algebra K A] [CharZero K] [CharZero A]
    [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) (hQ : IsIsotropic Q) :
    IsIsotropicAfterBaseChange Q A := by
  letI : Invertible (2 : A) := invertibleOfNonzero (by norm_num)
  rcases hQ with ⟨x, hx, hQx⟩
  refine ⟨(1 : A) ⊗ₜ[K] x, ?_, ?_⟩
  · simpa using (Module.FaithfullyFlat.tensorProduct_mk_injective
      (A := K) (B := A) V).ne hx
  · simp [QuadraticForm.baseChange_tmul, hQx]

/-- Checked proof of the easy direction for both concrete completion families. -/
theorem global_to_local : GlobalToLocalObligation.{u, v} := by
  intro K _ _ V _ _ _ Q hQ
  constructor
  · intro w
    letI : CharZero ((NumberField.FinitePlace.maximalIdeal w).adicCompletion K) :=
      charZero_of_injective_algebraMap (algebraMap K _).injective
    exact isotropic_after_baseChange Q hQ
  · intro w
    letI : CharZero w.Completion :=
      charZero_of_injective_algebraMap (algebraMap K _).injective
    exact isotropic_after_baseChange Q hQ

/-- Exact conditional composition.  The local-to-global engine is consumed as
an abstract child, so this declaration proves no unconditional root theorem. -/
theorem root_composition
    (easy : GlobalToLocalObligation.{u, v})
    (hard : LocalToGlobalObligation.{u, v}) :
    HasseMinkowskiStatement.{u, v} := by
  intro K _ _ V _ _ _ Q hnondegenerate
  constructor
  · exact easy K V Q
  · rintro ⟨hfinite, hinfinite⟩
    exact hard K V Q hnondegenerate hfinite hinfinite

/-- Package both directional children without closing either one implicitly. -/
theorem direction_package
    (easy : GlobalToLocalObligation.{u, v})
    (hard : LocalToGlobalObligation.{u, v}) :
    DirectionPackage.{u, v} := ⟨easy, hard⟩

/-- The packaged directional result has exactly the canonical root conclusion. -/
theorem root_from_direction_package
    (directions : DirectionPackage.{u, v}) :
    HasseMinkowskiStatement.{u, v} :=
  root_composition directions.1 directions.2

#check isotropic_after_baseChange
#check global_to_local
#check root_composition
#check direction_package
#check root_from_direction_package
#print axioms isotropic_after_baseChange
#print axioms global_to_local
#print axioms root_composition
#print axioms direction_package
#print axioms root_from_direction_package

end Stage1.THM_M_0423.ObligationTree
