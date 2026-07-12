import Mathlib.Analysis.CStarAlgebra.PositiveLinearMap
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.Analysis.InnerProductSpace.l2Space
import Mathlib.Analysis.InnerProductSpace.StarOrder

namespace Stage1.THM_M_0338

open scoped ComplexOrder

/-- A state is a positive complex-linear functional normalized at the unit. -/
structure State (A : Type*) [Ring A] [Module ℂ A] [One A] [PartialOrder A] where
  toPositiveLinearMap : A →ₚ[ℂ] ℂ
  map_one : toPositiveLinearMap 1 = 1

noncomputable instance {A : Type*} [Ring A] [Module ℂ A] [One A] [PartialOrder A] :
    CoeFun (State A) (fun _ ↦ A → ℂ) :=
  ⟨fun φ ↦ φ.toPositiveLinearMap⟩

/-- Extreme-point purity, stated directly in the convex set of states. -/
def IsPure {A : Type*} [Ring A] [Module ℂ A] [One A] [PartialOrder A]
    (φ : State A) : Prop :=
  ∀ (ψ χ : State A) (t : ℝ), 0 < t → t < 1 →
    (∀ a, φ a = (t : ℂ) * ψ a + ((1 - t : ℝ) : ℂ) * χ a) →
    ψ = φ ∧ χ = φ

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

abbrev Operators (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] :=
  H →L[ℂ] H

/-- The exact affirmative Kadison-Singer assertion, with the diagonal masa characterized by
matrix coefficients relative to a countably infinite Hilbert basis. -/
def KadisonSingerStatement : Prop :=
  ∀ (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (basis : HilbertBasis ℕ ℂ H) (diagonal : StarSubalgebra ℂ (Operators H)),
    (∀ T : Operators H,
      T ∈ diagonal ↔ ∀ i j : ℕ, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0) →
    ∀ φ : State diagonal, IsPure φ →
      ∃! extension : State (Operators H),
        ∀ d : diagonal, extension d = φ d

/- Structural mutations are elaborated but not credited. The statement validator verifies that
their explicit expressions differ from the canonical target. -/
def mutationRemovedPurity : Prop :=
  ∀ (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (basis : HilbertBasis ℕ ℂ H) (diagonal : StarSubalgebra ℂ (Operators H)),
    (∀ T : Operators H,
      T ∈ diagonal ↔ ∀ i j : ℕ, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0) →
    ∀ φ : State diagonal,
      ∃! extension : State (Operators H), ∀ d : diagonal, extension d = φ d

def mutationFiniteDomain : Prop :=
  ∀ (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (basis : HilbertBasis (Fin 2) ℂ H) (diagonal : StarSubalgebra ℂ (Operators H)),
    (∀ T : Operators H,
      T ∈ diagonal ↔ ∀ i j : Fin 2, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0) →
    ∀ φ : State diagonal, IsPure φ →
      ∃! extension : State (Operators H), ∀ d : diagonal, extension d = φ d

def mutationChangedBinderScope : Prop :=
  ∀ (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (basis : HilbertBasis ℕ ℂ H),
    ∃ diagonal : StarSubalgebra ℂ (Operators H),
      (∀ T : Operators H,
        T ∈ diagonal ↔ ∀ i j : ℕ, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0) ∧
      ∀ φ : State diagonal, IsPure φ →
        ∃! extension : State (Operators H), ∀ d : diagonal, extension d = φ d

def mutationPureExtensionsOnly : Prop :=
  ∀ (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (basis : HilbertBasis ℕ ℂ H) (diagonal : StarSubalgebra ℂ (Operators H)),
    (∀ T : Operators H,
      T ∈ diagonal ↔ ∀ i j : ℕ, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0) →
    ∀ φ : State diagonal, IsPure φ →
      ∃! extension : State (Operators H),
        IsPure extension ∧ ∀ d : diagonal, extension d = φ d

end Stage1.THM_M_0338

#print Stage1.THM_M_0338.KadisonSingerStatement
