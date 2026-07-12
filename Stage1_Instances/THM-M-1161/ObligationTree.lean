import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1161 conditional obligation composition

This file restates the frozen target, gives exact interfaces for its two
branches, and checks their composition. It assumes the analytic branch
results; it does not prove them or the Fredholm alternative.
-/

namespace AwesomeTheorems.Stage1.THM_M_1161.ObligationTree

open scoped ComplexConjugate InnerProductSpace
open MeasureTheory

variable {X E : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X]
  (μ : Measure X) [IsFiniteMeasure μ]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

structure Model where
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

def Solves (M : Model (E := E) μ) (lambda : ℂ) (phi f : E) : Prop :=
  ∀ x : X, M.realize phi x - lambda * ∫ y, M.kernel x y * M.realize phi y ∂μ =
    M.realize f x

def Root (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  let A : E →L[ℂ] E := ContinuousLinearMap.id ℂ E - lambda • M.operator
  let Astar : E →L[ℂ] E := ContinuousLinearMap.adjoint A
  ((∀ u : E, Solves μ M lambda u 0 → u = 0) ∧
      ∀ f : E, ∃! phi : E, Solves μ M lambda phi f) ∨
    ((∃ u : E, u ≠ 0 ∧ Solves μ M lambda u 0) ∧
      ∀ f : E, (∃ phi : E, Solves μ M lambda phi f) ↔
        ∀ psi : E, Astar psi = 0 → ⟪f, psi⟫_ℂ = 0)

def HomogeneousTrivial (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  ∀ u : E, Solves μ M lambda u 0 → u = 0

def HomogeneousNontrivial (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  ∃ u : E, u ≠ 0 ∧ Solves μ M lambda u 0

def UniqueForEveryDatum (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  ∀ f : E, ∃! phi : E, Solves μ M lambda phi f

def AdjointCompatible (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  let A : E →L[ℂ] E := ContinuousLinearMap.id ℂ E - lambda • M.operator
  let Astar : E →L[ℂ] E := ContinuousLinearMap.adjoint A
  ∀ f : E, (∃ phi : E, Solves μ M lambda phi f) ↔
    ∀ psi : E, Astar psi = 0 → ⟪f, psi⟫_ℂ = 0

def KernelDichotomy (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  HomogeneousTrivial μ M lambda ∨ HomogeneousNontrivial μ M lambda

def FirstBranchBridge (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  HomogeneousTrivial μ M lambda → UniqueForEveryDatum μ M lambda

def SecondBranchBridge (M : Model (E := E) μ) (lambda : ℂ) : Prop :=
  HomogeneousNontrivial μ M lambda → AdjointCompatible μ M lambda

/-- Exact child-to-root composition. The analytic content is confined to the
three explicit premises, all of which remain open in this phase. -/
theorem root_compose (M : Model (E := E) μ) (lambda : ℂ)
    (cases : KernelDichotomy μ M lambda)
    (first : FirstBranchBridge μ M lambda)
    (second : SecondBranchBridge μ M lambda) : Root μ M lambda := by
  rcases cases with htrivial | hnontrivial
  · left
    exact ⟨htrivial, first htrivial⟩
  · right
    exact ⟨hnontrivial, second hnontrivial⟩

#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check ContinuousLinearMap.orthogonal_range
#print axioms root_compose

end AwesomeTheorems.Stage1.THM_M_1161.ObligationTree
