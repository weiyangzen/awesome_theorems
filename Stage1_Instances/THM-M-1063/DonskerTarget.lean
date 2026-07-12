import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic

open Filter Finset MeasureTheory ProbabilityTheory Set
open scoped Topology

namespace AwesomeTheorems.Stage1.THM_M_1063

noncomputable section

universe u v

/-- The compact time interval used for the continuous sample paths. -/
abbrev UnitInterval := Set.Icc (0 : ℝ) 1

/-- The value at `t` of the diffusively rescaled polygonal interpolation through the partial sums
`S k = ∑ i < k, X i`. The clipped floor makes the formula total at `t = 1`; the coefficient then
equals one and supplies the last increment. -/
def polygonalValue {Ω : Type*} (X : ℕ → Ω → ℝ) (sigma : ℝ) (n : ℕ) (ω : Ω)
    (t : UnitInterval) : ℝ :=
  if n = 0 then 0
  else
    let k := min ⌊(n : ℝ) * (t : ℝ)⌋₊ (n - 1)
    ((∑ i ∈ range k, X i ω) + ((n : ℝ) * (t : ℝ) - k) * X k ω) /
      (sigma * Real.sqrt n)

/-- A continuous-path random variable is the required interpolation of `X` at scale `n`. -/
def IsPolygonalWalk {Ω : Type*} (X : ℕ → Ω → ℝ) (sigma : ℝ) (n : ℕ)
    (W : Ω → C(UnitInterval, ℝ)) : Prop :=
  ∀ ω t, W ω t = polygonalValue X sigma n ω t

/-- The pinned mathlib characterization of standard real Brownian motion needed by Donsker's
principle: continuous paths, jointly Gaussian evaluations, zero mean, and covariance `min s t`. -/
def IsStandardBrownian {Ω : Type*} [MeasurableSpace Ω] (B : Ω → C(UnitInterval, ℝ))
    (P : Measure Ω) : Prop :=
  IsGaussianProcess (fun t ω ↦ B ω t) P ∧
    (∀ t, ∫ ω, B ω t ∂P = 0) ∧
    (∀ s t, cov[fun ω ↦ B ω s, fun ω ↦ B ω t; P] = min (s : ℝ) (t : ℝ))

/-- Donsker's invariance principle, frozen as convergence in distribution in continuous path
space for the exact polygonally interpolated, variance-normalized partial-sum process. -/
def DonskerInvariancePrinciple : Prop :=
  ∀ (Ω ΩB : Type*) (_ : MeasurableSpace Ω) (_ : MeasurableSpace ΩB)
    (_ : MeasurableSpace C(UnitInterval, ℝ)) (_ : BorelSpace C(UnitInterval, ℝ))
    (P : Measure Ω) (_ : IsProbabilityMeasure P)
    (PB : Measure ΩB) (_ : IsProbabilityMeasure PB)
    (X : ℕ → Ω → ℝ) (sigma : ℝ) (W : ℕ → Ω → C(UnitInterval, ℝ))
    (B : ΩB → C(UnitInterval, ℝ)),
    0 < sigma →
    (∀ i, AEMeasurable (X i) P) →
    iIndepFun X P →
    (∀ i, IdentDistrib (X i) (X 0) P P) →
    MemLp (X 0) 2 P →
    (∫ ω, X 0 ω ∂P) = 0 →
    Var[X 0; P] = sigma ^ 2 →
    (∀ n, IsPolygonalWalk X sigma n (W n)) →
    IsStandardBrownian B PB →
    TendstoInDistribution W atTop B (fun _ ↦ P) PB

/-- Direct expansion used to check that the target name hides no theorem-strengthening premise. -/
def ExpandedSourceShape : Prop :=
  ∀ (Ω ΩB : Type*) (_ : MeasurableSpace Ω) (_ : MeasurableSpace ΩB)
    (_ : MeasurableSpace C(UnitInterval, ℝ)) (_ : BorelSpace C(UnitInterval, ℝ))
    (P : Measure Ω) (_ : IsProbabilityMeasure P)
    (PB : Measure ΩB) (_ : IsProbabilityMeasure PB)
    (X : ℕ → Ω → ℝ) (sigma : ℝ) (W : ℕ → Ω → C(UnitInterval, ℝ))
    (B : ΩB → C(UnitInterval, ℝ)),
    0 < sigma → (∀ i, AEMeasurable (X i) P) → iIndepFun X P →
    (∀ i, IdentDistrib (X i) (X 0) P P) → MemLp (X 0) 2 P →
    (∫ ω, X 0 ω ∂P) = 0 → Var[X 0; P] = sigma ^ 2 →
    (∀ n ω t, W n ω t = polygonalValue X sigma n ω t) →
    (IsGaussianProcess (fun t ω ↦ B ω t) PB ∧
      (∀ t, ∫ ω, B ω t ∂PB = 0) ∧
      (∀ s t, cov[fun ω ↦ B ω s, fun ω ↦ B ω t; PB] = min (s : ℝ) (t : ℝ))) →
    TendstoInDistribution W atTop B (fun _ ↦ P) PB

theorem target_iff_expandedSourceShape :
    DonskerInvariancePrinciple.{u, v} ↔ ExpandedSourceShape.{u, v} := by
  simp only [DonskerInvariancePrinciple, ExpandedSourceShape, IsPolygonalWalk,
    IsStandardBrownian]

#check DonskerInvariancePrinciple

end

end AwesomeTheorems.Stage1.THM_M_1063
