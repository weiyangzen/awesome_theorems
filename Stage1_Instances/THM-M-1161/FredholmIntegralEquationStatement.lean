import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Canonical statement for THM-M-1161

This file freezes the second-kind Fredholm integral-equation target.  The map
`realize` identifies the abstract Hilbert-space vectors with functions on the
compact measured domain, while `h_kernel` makes `T` the stated integral
operator rather than an unrelated compact operator.
-/

namespace AwesomeTheorems.Stage1.THM_M_1161

open scoped ComplexConjugate InnerProductSpace
open MeasureTheory

variable {X E : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X]
  (μ : Measure X) [IsFiniteMeasure μ]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- Data realizing a compact integral operator on a complex Hilbert space. -/
structure FredholmKernelModel where
  kernel : X → X → ℂ
  realize : E → X → ℂ
  compact_domain : IsCompact (Set.univ : Set X)
  continuous_kernel : Continuous (Function.uncurry kernel)
  realize_injective : Function.Injective realize
  operator : E →L[ℂ] E
  compact_operator : IsCompactOperator operator
  integrable_kernel (u : E) (x : X) : Integrable (fun y => kernel x y * realize u y) μ
  operator_eq_integral (u : E) (x : X) :
    realize (operator u) x = ∫ y, kernel x y * realize u y ∂μ

/-- Pointwise integral equation represented by a model. -/
def Solves (M : FredholmKernelModel (E := E) μ) (lambda : ℂ) (phi f : E) : Prop :=
  ∀ x : X, M.realize phi x - lambda * ∫ y, M.kernel x y * M.realize phi y ∂μ =
    M.realize f x

/-- The operator form of the second-kind Fredholm equation
`phi(x) - lambda * integral K(x,y) phi(y) dmu(y) = f(x)`.

The target records the full alternative.  Either the homogeneous equation has
only the zero solution, in which case every datum has a unique solution, or it
has a nonzero solution and solvability is exactly orthogonality to every
solution of the adjoint homogeneous equation.
-/
def FredholmSecondKindAlternative
    (M : FredholmKernelModel (E := E) μ) (lambda : ℂ) : Prop :=
  let A : E →L[ℂ] E := ContinuousLinearMap.id ℂ E - lambda • M.operator
  let Astar : E →L[ℂ] E := ContinuousLinearMap.adjoint A
  ((∀ u : E, Solves μ M lambda u 0 → u = 0) ∧
      ∀ f : E, ∃! phi : E, Solves μ M lambda phi f) ∨
    ((∃ u : E, u ≠ 0 ∧ Solves μ M lambda u 0) ∧
      ∀ f : E, (∃ phi : E, Solves μ M lambda phi f) ↔
        ∀ psi : E, Astar psi = 0 → ⟪f, psi⟫_ℂ = 0)

#check FredholmSecondKindAlternative

end AwesomeTheorems.Stage1.THM_M_1161
