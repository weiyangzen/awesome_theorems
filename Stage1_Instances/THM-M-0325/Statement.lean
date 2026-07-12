import Mathlib.Analysis.InnerProductSpace.Basic

/-!
# THM-M-0325: exact finite real Grothendieck inequality statement

This module freezes and tests the statement boundary only. It contains no proof
of Grothendieck's inequality.
-/

noncomputable section

open scoped BigOperators RealInnerProductSpace

namespace Stage1Instances.THM_M_0325

universe u

/-- The scalar bilinear form of a finite real matrix. -/
def ScalarMatrixForm {m n : Type u} [Fintype m] [Fintype n]
    (A : m -> n -> Real) (s : m -> Real) (t : n -> Real) : Real :=
  ∑ i, ∑ j, A i j * s i * t j

/-- The corresponding form on two finite families in a real Hilbert space. -/
def HilbertMatrixForm {m n : Type u} [Fintype m] [Fintype n]
    (A : m -> n -> Real) (H : Type u)
    [NormedAddCommGroup H] [InnerProductSpace Real H]
    (x : m -> H) (y : n -> H) : Real :=
  ∑ i, ∑ j, A i j * ⟪x i, y j⟫

/-- A real matrix form is bounded by `C` on the scalar unit polydisc. -/
def ScalarUnitBoundedBy {m n : Type u} [Fintype m] [Fintype n]
    (A : m -> n -> Real) (C : Real) : Prop :=
  forall s : m -> Real, forall t : n -> Real,
    (forall i, abs (s i) <= 1) -> (forall j, abs (t j) <= 1) ->
      abs (ScalarMatrixForm A s t) <= C

/-- A real matrix form is bounded by `C` on Hilbert-space unit balls. -/
def HilbertUnitBoundedBy {m n : Type u} [Fintype m] [Fintype n]
    (A : m -> n -> Real) (C : Real) : Prop :=
  forall (H : Type u) [NormedAddCommGroup H] [InnerProductSpace Real H],
    forall x : m -> H, forall y : n -> H,
      (forall i, norm (x i) <= 1) -> (forall j, norm (y j) <= 1) ->
        abs (HilbertMatrixForm A H x y) <= C

/-- The exact finite real matrix form selected for Grothendieck's inequality. -/
def GrothendieckInequalityTarget : Prop :=
  ∃ K_G : Real, 0 <= K_G ∧
    forall (m n : Type u) [Fintype m] [Fintype n],
      forall (A : m -> n -> Real) (C : Real),
        0 <= C -> ScalarUnitBoundedBy A C ->
          HilbertUnitBoundedBy A (K_G * C)

/-- Direct expansion of the intake-selected finite real matrix formulation. -/
def IntakeSourceShape : Prop :=
  ∃ K_G : Real, 0 <= K_G ∧
    forall (m n : Type u) [Fintype m] [Fintype n],
      forall (A : m -> n -> Real) (C : Real), 0 <= C ->
        (forall s : m -> Real, forall t : n -> Real,
          (forall i, abs (s i) <= 1) -> (forall j, abs (t j) <= 1) ->
            abs (∑ i, ∑ j, A i j * s i * t j) <= C) ->
        forall (H : Type u) [NormedAddCommGroup H] [InnerProductSpace Real H],
          forall x : m -> H, forall y : n -> H,
            (forall i, norm (x i) <= 1) -> (forall j, norm (y j) <= 1) ->
              abs (∑ i, ∑ j, A i j * ⟪x i, y j⟫) <= K_G * C

/-- The canonical target is definitionally the expanded intake shape. -/
theorem target_iff_intakeSourceShape :
    GrothendieckInequalityTarget.{u} <-> IntakeSourceShape.{u} :=
  Iff.rfl

-- Separately elaborated structural mutations for statement review.
def mutationMatrixDependentConstant : Prop :=
  forall (m n : Type u) [Fintype m] [Fintype n],
    forall A : m -> n -> Real, ∃ K_G : Real, 0 <= K_G ∧
      forall C : Real, 0 <= C -> ScalarUnitBoundedBy A C ->
        HilbertUnitBoundedBy A (K_G * C)

def mutationSubsingletonHilbertSpaces : Prop :=
  ∃ K_G : Real, 0 <= K_G ∧
    forall (m n : Type u) [Fintype m] [Fintype n],
      forall (A : m -> n -> Real) (C : Real), 0 <= C ->
        ScalarUnitBoundedBy A C ->
        forall (H : Type u) [NormedAddCommGroup H] [InnerProductSpace Real H]
          [Subsingleton H], forall x : m -> H, forall y : n -> H,
            (forall i, norm (x i) <= 1) -> (forall j, norm (y j) <= 1) ->
              abs (HilbertMatrixForm A H x y) <= K_G * C

def mutationSignVectorsOnly : Prop :=
  ∃ K_G : Real, 0 <= K_G ∧
    forall (m n : Type u) [Fintype m] [Fintype n],
      forall (A : m -> n -> Real) (C : Real), 0 <= C ->
        (forall s : m -> Real, forall t : n -> Real,
          (forall i, abs (s i) = 1) -> (forall j, abs (t j) = 1) ->
            abs (ScalarMatrixForm A s t) <= C) ->
          HilbertUnitBoundedBy A (K_G * C)

def mutationComplexScalars : Prop :=
  ∃ K_G : Real, 0 <= K_G ∧
    forall (m n : Type u) [Fintype m] [Fintype n],
      forall (A : m -> n -> Complex) (C : Real),
        0 <= C ->
        (forall s : m -> Complex, forall t : n -> Complex,
          (forall i, norm (s i) <= 1) -> (forall j, norm (t j) <= 1) ->
            norm (∑ i, ∑ j, A i j * s i * t j) <= C) -> True

/-- Empty index types exercise the finite-sum boundary without extra hypotheses. -/
theorem empty_scalar_boundary (A : Empty -> Empty -> Real) :
    ScalarUnitBoundedBy A 0 := by
  intro s t hs ht
  simp [ScalarMatrixForm]

end Stage1Instances.THM_M_0325

set_option pp.explicit true in
#print Stage1Instances.THM_M_0325.GrothendieckInequalityTarget
