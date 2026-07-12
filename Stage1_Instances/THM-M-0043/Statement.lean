import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.UnitaryGroup

/-!
# THM-M-0043 canonical Lean statement

This module freezes the finite complex normal-matrix formulation of the spectral theorem selected
from the repository gloss and Axler's finite-dimensional complex spectral theorem. It states only
the target and checked statement transports; it does not prove the spectral theorem.
-/

namespace Stage1Instances.THM_M_0043

universe u

/-- Every nonzero finite-dimensional complex normal matrix is unitarily diagonalizable. -/
def SpectralTheoremTarget : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n] (A : Matrix n n Complex),
    IsStarNormal A ->
      exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
        A = (U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex)

/-- The same target with unitary membership carried as an explicit hypothesis. -/
def ExplicitUnitaryMembershipTarget : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n] (A : Matrix n n Complex),
    IsStarNormal A ->
      exists (U : Matrix n n Complex) (d : n -> Complex),
        U ∈ Matrix.unitaryGroup n Complex ∧ A = U * Matrix.diagonal d * star U

/-- Equivalent change-of-orthonormal-basis orientation: the conjugated matrix is diagonal. -/
def ConjugatedDiagonalTarget : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n] (A : Matrix n n Complex),
    IsStarNormal A ->
      exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
        star (U : Matrix n n Complex) * A * (U : Matrix n n Complex) = Matrix.diagonal d

/-- Checked transport between subtype and explicit-membership unitary witnesses. -/
theorem spectralTheoremTarget_iff_explicitUnitaryMembershipTarget :
    SpectralTheoremTarget.{u} <-> ExplicitUnitaryMembershipTarget.{u} := by
  constructor
  · intro h n _ _ _ A hA
    obtain ⟨U, d, hU⟩ := h n A hA
    exact ⟨U, d, U.property, hU⟩
  · intro h n _ _ _ A hA
    obtain ⟨U, d, hU, hA⟩ := h n A hA
    exact ⟨⟨U, hU⟩, d, hA⟩

/-- Checked transport between the two standard unitary-conjugation orientations. -/
theorem spectralTheoremTarget_iff_conjugatedDiagonalTarget :
    SpectralTheoremTarget.{u} <-> ConjugatedDiagonalTarget.{u} := by
  constructor
  · intro h n _ _ _ A hA
    obtain ⟨U, d, hA⟩ := h n A hA
    refine ⟨U, d, ?_⟩
    rw [hA]
    calc
      star (U : Matrix n n Complex) *
          ((U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex)) *
          (U : Matrix n n Complex) =
          (star (U : Matrix n n Complex) * (U : Matrix n n Complex)) *
          Matrix.diagonal d *
          (star (U : Matrix n n Complex) * (U : Matrix n n Complex)) := by
            simp only [mul_assoc]
      _ = Matrix.diagonal d := by
        rw [Matrix.UnitaryGroup.star_mul_self U]
        simp
  · intro h n _ _ _ A hA
    obtain ⟨U, d, hA⟩ := h n A hA
    refine ⟨U, d, ?_⟩
    calc
      A = (1 : Matrix n n Complex) * A * 1 := by simp
      _ = ((U : Matrix n n Complex) * star (U : Matrix n n Complex)) * A *
          ((U : Matrix n n Complex) * star (U : Matrix n n Complex)) := by
            rw [Matrix.mem_unitaryGroup_iff.mp U.property]
      _ = (U : Matrix n n Complex) *
          (star (U : Matrix n n Complex) * A * (U : Matrix n n Complex)) *
          star (U : Matrix n n Complex) := by simp only [mul_assoc]
      _ = (U : Matrix n n Complex) * Matrix.diagonal d *
          star (U : Matrix n n Complex) := by rw [hA]

/-! Structural mutations elaborate but are intentionally distinct from the canonical target. -/

def mutationRemovedNormalityHypothesis : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n] (A : Matrix n n Complex),
    exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
      A = (U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex)

def mutationChangedScalarDomain : Prop :=
  forall (K : Type u) [CommRing K] [StarRing K]
      (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n] (A : Matrix n n K),
    IsStarNormal A ->
      exists (U : Matrix.unitaryGroup n K) (d : n -> K),
        A = (U : Matrix n n K) * Matrix.diagonal d * star (U : Matrix n n K)

def mutationChangedBinderScope : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n],
    exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
      forall A : Matrix n n Complex, IsStarNormal A ->
        A = (U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex)

def mutationIncludedEmptyBoundary : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] (A : Matrix n n Complex),
    IsStarNormal A ->
      exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
        A = (U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex)

variable
  (hRemoved : mutationRemovedNormalityHypothesis.{u})
  (hDomain : mutationChangedScalarDomain.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationIncludedEmptyBoundary.{u})

#check_failure (hRemoved : SpectralTheoremTarget.{u})
#check_failure (hDomain : SpectralTheoremTarget.{u})
#check_failure (hScope : SpectralTheoremTarget.{u})
#check_failure (hBoundary : SpectralTheoremTarget.{u})

#check spectralTheoremTarget_iff_explicitUnitaryMembershipTarget
#check spectralTheoremTarget_iff_conjugatedDiagonalTarget
#print axioms spectralTheoremTarget_iff_explicitUnitaryMembershipTarget
#print axioms spectralTheoremTarget_iff_conjugatedDiagonalTarget

set_option pp.universes true in
set_option pp.explicit true in
#print SpectralTheoremTarget

end Stage1Instances.THM_M_0043
