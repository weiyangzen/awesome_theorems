import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic

/-! A checked exact-root interface for the frozen THM-M-1063 architecture. -/

open Filter Finset MeasureTheory ProbabilityTheory Set
open scoped Topology

namespace AwesomeTheorems.Stage1.THM_M_1063

noncomputable section

abbrev UnitInterval := Set.Icc (0 : ℝ) 1

def polygonalValue {Ω : Type*} (X : ℕ → Ω → ℝ) (sigma : ℝ) (n : ℕ) (ω : Ω)
    (t : UnitInterval) : ℝ :=
  if n = 0 then 0
  else
    let k := min ⌊(n : ℝ) * (t : ℝ)⌋₊ (n - 1)
    ((∑ i ∈ range k, X i ω) + ((n : ℝ) * (t : ℝ) - k) * X k ω) /
      (sigma * Real.sqrt n)

def IsPolygonalWalk {Ω : Type*} (X : ℕ → Ω → ℝ) (sigma : ℝ) (n : ℕ)
    (W : Ω → C(UnitInterval, ℝ)) : Prop :=
  ∀ ω t, W ω t = polygonalValue X sigma n ω t

def IsStandardBrownian {Ω : Type*} [MeasurableSpace Ω] (B : Ω → C(UnitInterval, ℝ))
    (P : Measure Ω) : Prop :=
  IsGaussianProcess (fun t ω ↦ B ω t) P ∧
    (∀ t, ∫ ω, B ω t ∂P = 0) ∧
    (∀ s t, cov[fun ω ↦ B ω s, fun ω ↦ B ω t; P] = min (s : ℝ) (t : ℝ))

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

namespace ObligationTree

universe u v

/-- This checks the architecture's terminal-to-root type boundary only. The hypothesis is the
exact open root, so this declaration supplies no Donsker proof or machine-closure credit. -/
theorem exactRoot_of_exactRoot
    (h : AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple.{u, v}) :
    AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple.{u, v} := h

#check exactRoot_of_exactRoot

end ObligationTree
end
end AwesomeTheorems.Stage1.THM_M_1063
