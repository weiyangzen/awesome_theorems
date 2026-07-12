import Mathlib.Analysis.Complex.Basic
import Mathlib.LinearAlgebra.UnitaryGroup

/-!
# THM-M-0044: exact full rectangular singular-value decomposition statement

This module freezes the statement boundary only. It defines the rectangular
diagonal factor explicitly and contains no proof of singular-value decomposition.
-/

noncomputable section

set_option autoImplicit false

namespace Stage1Instances.THM_M_0044

universe u

/-- A rectangular matrix whose only potentially nonzero entries have equal
natural positions in the row and column index types. -/
def IsRectangularDiagonal {m n : Nat} {K : Type*} [Zero K]
    (Sigma : Matrix (Fin m) (Fin n) K) : Prop :=
  forall i j, i.val != j.val -> Sigma i j = 0

/-- A full SVD factorization, with nonnegative real diagonal data embedded in
the real-or-complex scalar field. -/
def IsFullSVD {m n : Nat} {K : Type u} [RCLike K]
    (A : Matrix (Fin m) (Fin n) K) : Prop :=
  exists U : Matrix (Fin m) (Fin m) K,
    exists V : Matrix (Fin n) (Fin n) K,
      exists sigma : Fin (Nat.min m n) -> Real,
        U ∈ Matrix.unitaryGroup (Fin m) K /\
        V ∈ Matrix.unitaryGroup (Fin n) K /\
        (forall k, 0 <= sigma k) /\
        let Sigma : Matrix (Fin m) (Fin n) K := fun i j =>
          if h : i.val = j.val then
            (sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : K)
          else 0
        IsRectangularDiagonal Sigma /\
          A = U * Sigma * star V

/-- Full SVD over one fixed real-or-complex scalar field. -/
def FullSVDOver (K : Type u) [RCLike K] : Prop :=
  forall (m n : Nat) (A : Matrix (Fin m) (Fin n) K), IsFullSVD A

/-- Exact intake-selected target: the full SVD over each of `Real` and
`Complex`. The closed pair avoids broadening the catalog's two fields to every
possible future instance of the open `RCLike` class. -/
def SingularValueDecompositionTarget : Prop :=
  FullSVDOver Real /\ FullSVDOver Complex

/-- Direct expansion of the named target and factor predicate. -/
def DirectFullSVDShape : Prop :=
  (forall (m n : Nat) (A : Matrix (Fin m) (Fin n) Real),
      exists U : Matrix (Fin m) (Fin m) Real,
        exists V : Matrix (Fin n) (Fin n) Real,
          exists sigma : Fin (Nat.min m n) -> Real,
            U ∈ Matrix.unitaryGroup (Fin m) Real /\
            V ∈ Matrix.unitaryGroup (Fin n) Real /\
            (forall k, 0 <= sigma k) /\
            let Sigma : Matrix (Fin m) (Fin n) Real := fun i j =>
              if h : i.val = j.val then
                sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩
              else 0
            IsRectangularDiagonal Sigma /\
              A = U * Sigma * star V) /\
  (forall (m n : Nat) (A : Matrix (Fin m) (Fin n) Complex),
      exists U : Matrix (Fin m) (Fin m) Complex,
        exists V : Matrix (Fin n) (Fin n) Complex,
          exists sigma : Fin (Nat.min m n) -> Real,
            U ∈ Matrix.unitaryGroup (Fin m) Complex /\
            V ∈ Matrix.unitaryGroup (Fin n) Complex /\
            (forall k, 0 <= sigma k) /\
            let Sigma : Matrix (Fin m) (Fin n) Complex := fun i j =>
              if h : i.val = j.val then
                (sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : Complex)
              else 0
            IsRectangularDiagonal Sigma /\
              A = U * Sigma * star V)

/-- The stronger polymorphic `RCLike` formulation implies the exact closed
real-and-complex target. It is recorded as an alternate, not as the root. -/
def RCLikeFullSVDShape : Prop :=
  forall (K : Type) [RCLike K], FullSVDOver K

/-- Checked transport from the canonical named form to its direct expansion. -/
theorem singularValueDecompositionTarget_iff_directFullSVDShape :
    SingularValueDecompositionTarget <-> DirectFullSVDShape :=
  Iff.rfl

/-- Checked one-way transport from the stronger open-class encoding. -/
theorem rclikeFullSVDShape_implies_target
    (h : RCLikeFullSVDShape) : SingularValueDecompositionTarget :=
  ⟨h Real, h Complex⟩

-- Structural mutations: each elaborates but is intentionally not the target.
def mutationRemovedNonnegative : Prop :=
  (forall (m n : Nat) (A : Matrix (Fin m) (Fin n) Real),
      exists U : Matrix (Fin m) (Fin m) Real,
        exists V : Matrix (Fin n) (Fin n) Real,
          exists sigma : Fin (Nat.min m n) -> Real,
            U ∈ Matrix.unitaryGroup (Fin m) Real /\
            V ∈ Matrix.unitaryGroup (Fin n) Real /\
            let Sigma : Matrix (Fin m) (Fin n) Real := fun i j =>
              if h : i.val = j.val then
                sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩
              else 0
            IsRectangularDiagonal Sigma /\
              A = U * Sigma * star V) /\
  (forall (m n : Nat) (A : Matrix (Fin m) (Fin n) Complex),
      exists U : Matrix (Fin m) (Fin m) Complex,
        exists V : Matrix (Fin n) (Fin n) Complex,
          exists sigma : Fin (Nat.min m n) -> Real,
            U ∈ Matrix.unitaryGroup (Fin m) Complex /\
            V ∈ Matrix.unitaryGroup (Fin n) Complex /\
            let Sigma : Matrix (Fin m) (Fin n) Complex := fun i j =>
              if h : i.val = j.val then
                (sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : Complex)
              else 0
            IsRectangularDiagonal Sigma /\
              A = U * Sigma * star V)

def mutationRemovedUnitaryHypothesis : Prop :=
  (forall (m n : Nat) (A : Matrix (Fin m) (Fin n) Real),
      exists U : Matrix (Fin m) (Fin m) Real,
        exists V : Matrix (Fin n) (Fin n) Real,
          exists sigma : Fin (Nat.min m n) -> Real,
            (forall k, 0 <= sigma k) /\
            let Sigma : Matrix (Fin m) (Fin n) Real := fun i j =>
              if h : i.val = j.val then sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ else 0
            IsRectangularDiagonal Sigma /\ A = U * Sigma * star V) /\
  (forall (m n : Nat) (A : Matrix (Fin m) (Fin n) Complex),
      exists U : Matrix (Fin m) (Fin m) Complex,
        exists V : Matrix (Fin n) (Fin n) Complex,
          exists sigma : Fin (Nat.min m n) -> Real,
            (forall k, 0 <= sigma k) /\
            let Sigma : Matrix (Fin m) (Fin n) Complex := fun i j =>
              if h : i.val = j.val then
                (sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : Complex)
              else 0
            IsRectangularDiagonal Sigma /\ A = U * Sigma * star V)

def mutationChangedScalarDomain : Prop := FullSVDOver Complex

def mutationChangedBinderScope : Prop :=
  (forall (m n : Nat),
    exists U : Matrix (Fin m) (Fin m) Real,
      exists V : Matrix (Fin n) (Fin n) Real,
        forall A : Matrix (Fin m) (Fin n) Real,
          exists sigma : Fin (Nat.min m n) -> Real,
            U ∈ Matrix.unitaryGroup (Fin m) Real /\
            V ∈ Matrix.unitaryGroup (Fin n) Real /\
            (forall k, 0 <= sigma k) /\
            let Sigma : Matrix (Fin m) (Fin n) Real := fun i j =>
              if h : i.val = j.val then sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ else 0
            IsRectangularDiagonal Sigma /\ A = U * Sigma * star V) /\
  FullSVDOver Complex

def mutationExcludedEmptyDimensions : Prop :=
  (forall (m n : Nat), 0 < m -> 0 < n ->
    forall A : Matrix (Fin m) (Fin n) Real, IsFullSVD A) /\
  (forall (m n : Nat), 0 < m -> 0 < n ->
    forall A : Matrix (Fin m) (Fin n) Complex, IsFullSVD A)

/-- The zero-by-`n` boundary remains part of the canonical factor predicate. -/
theorem zeroByNBoundary (K : Type u) [RCLike K] (n : Nat)
    (A : Matrix (Fin 0) (Fin n) K) : IsFullSVD A := by
  refine ⟨1, 1, fun k => Fin.elim0 (Fin.cast (by simp) k), ?_⟩
  refine ⟨Submonoid.one_mem _, Submonoid.one_mem _, ?_, ?_⟩
  · intro k
    exact Fin.elim0 (Fin.cast (by simp) k)
  · dsimp only
    constructor
    · simp [IsRectangularDiagonal]
    · ext i
      exact Fin.elim0 i

/-- The `m`-by-zero boundary remains part of the canonical factor predicate. -/
theorem mByZeroBoundary (K : Type u) [RCLike K] (m : Nat)
    (A : Matrix (Fin m) (Fin 0) K) : IsFullSVD A := by
  refine ⟨1, 1, fun k => Fin.elim0 (Fin.cast (by simp) k), ?_⟩
  refine ⟨Submonoid.one_mem _, Submonoid.one_mem _, ?_, ?_⟩
  · intro k
    exact Fin.elim0 (Fin.cast (by simp) k)
  · dsimp only
    constructor
    · simp [IsRectangularDiagonal]
    · ext i j
      exact Fin.elim0 j

end Stage1Instances.THM_M_0044

set_option pp.explicit true in
#print Stage1Instances.THM_M_0044.SingularValueDecompositionTarget
