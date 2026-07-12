import Mathlib.Analysis.Calculus.ContDiff.Basic

/-!
# THM-M-0612: Gromov nonsqueezing statement

This module fixes the local-domain coordinate formulation of Gromov's
symplectic nonsqueezing theorem. It contains the target proposition, not a
proof of that proposition.
-/

noncomputable section

open scoped BigOperators

namespace Stage1.THM_M_0612

universe u

/-- Standard real phase space with coordinates `(q, p)` indexed by `Q`. -/
abbrev PhaseSpace (Q : Type u) := Q ⊕ Q → ℝ

/-- Squared Euclidean norm in standard phase-space coordinates. -/
def normSq {Q : Type u} [Fintype Q] (x : PhaseSpace Q) : ℝ :=
  ∑ a : Q ⊕ Q, x a ^ 2

/-- The open standard ball of radius `r`. -/
def ball {Q : Type u} [Fintype Q] (r : ℝ) : Set (PhaseSpace Q) :=
  {x | normSq x < r ^ 2}

/-- The standard cylinder over the conjugate coordinate pair indexed by `i`. -/
def cylinder {Q : Type u} (i : Q) (R : ℝ) : Set (PhaseSpace Q) :=
  {x | x (Sum.inl i) ^ 2 + x (Sum.inr i) ^ 2 < R ^ 2}

/-- The standard symplectic form `sum_i (dq_i wedge dp_i)`. -/
def standardForm {Q : Type u} [Fintype Q] (x y : PhaseSpace Q) : ℝ :=
  ∑ i : Q, (x (Sum.inl i) * y (Sum.inr i) - x (Sum.inr i) * y (Sum.inl i))

/--
A smooth symplectic embedding whose domain is the open ball.

The total function is only an encoding device: every condition is restricted
to `ball r`, so no smoothness, injectivity, or symplectic condition is imposed
outside the mathematical domain of the embedding.
-/
def IsSymplecticEmbeddingOnBall
    {Q : Type u} [Fintype Q]
    (r : ℝ) (f : PhaseSpace Q → PhaseSpace Q) : Prop :=
  ContDiffOn ℝ ⊤ f (ball r) ∧
    Set.InjOn f (ball r) ∧
    ∀ x ∈ ball r, ∀ v w : PhaseSpace Q,
      standardForm (fderiv ℝ f x v) (fderiv ℝ f x w) = standardForm v w

/--
Canonical Lean target for Gromov's symplectic nonsqueezing theorem.

For every positive pair of radii, a symplectic embedding of the standard open
`2 * |Q|`-ball into a standard symplectic cylinder forces `r <= R`. The binder
`i : Q` makes the positive-dimensional hypothesis explicit.
-/
def StatementShape : Prop :=
  ∀ (Q : Type u) [Fintype Q] (i : Q) (r R : ℝ),
    0 < r → 0 < R →
    ∀ f : PhaseSpace Q → PhaseSpace Q,
      IsSymplecticEmbeddingOnBall r f →
      Set.MapsTo f (ball r) (cylinder i R) →
      r ≤ R

end Stage1.THM_M_0612
