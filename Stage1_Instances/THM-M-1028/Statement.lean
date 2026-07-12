import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Independence.Basic

/-!
Exact statement boundary for `THM-M-1028` (Wiener path regularity).

The statement deliberately does not reuse the historical conclusion package:
both terminal path properties occur in the conclusion of the target itself.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped NNReal ProbabilityTheory Topology

namespace AwesomeTheorems.Stage1.THM_M_1028

universe u

/-- A real stochastic process, with the theorem restricted to nonnegative time. -/
abbrev RealProcess (Ω : Type u) := ℝ → Ω → ℝ

/-- The adjacent increments of `X` along a finite time grid. -/
def increment {Ω : Type u} (X : RealProcess Ω) {n : ℕ}
    (t : Fin (n + 1) → ℝ) (i : Fin n) : Ω → ℝ :=
  fun ω => X (t i.succ) ω - X (t i.castSucc) ω

/-- A finite grid in nonnegative time, in increasing order. -/
def IsNonnegativeGrid {n : ℕ} (t : Fin (n + 1) → ℝ) : Prop :=
  (∀ i, 0 ≤ t i) ∧ Monotone t

/--
The standard Wiener finite-dimensional increment law: on every ordered
nonnegative grid, adjacent increments are mutually independent and increment
`i` has the centered Gaussian law with variance `t (i+1) - t i`.
-/
def HasStandardWienerIncrements {Ω : Type u} [MeasurableSpace Ω]
    (X : RealProcess Ω) (P : Measure Ω) : Prop :=
  ∀ {n : ℕ} (t : Fin (n + 1) → ℝ), ∀ ht : IsNonnegativeGrid t,
    iIndepFun (fun i : Fin n => increment X t i) P ∧
      ∀ i : Fin n,
        HasLaw (increment X t i)
          (gaussianReal 0 ⟨t i.succ - t i.castSucc, by
            exact sub_nonneg.mpr (ht.2 (Fin.castSucc_le_succ i))⟩) P

/-- Coordinatewise modification (the standard stochastic-process convention). -/
def IsModification {Ω : Type u} [MeasurableSpace Ω]
    (X Y : RealProcess Ω) (P : Measure Ω) : Prop :=
  ∀ t, X t =ᵐ[P] Y t

/-- Failure of the domain-relative derivative at every nonnegative time. -/
def NowhereDifferentiableOnNonnegative (f : ℝ → ℝ) : Prop :=
  ∀ t ∈ Ici (0 : ℝ), ¬ DifferentiableWithinAt ℝ f (Ici (0 : ℝ)) t

/--
Canonical Lean target for the classical path-regularity theorem for a real
standard Wiener process: it has a modification whose paths are almost surely
continuous and nowhere differentiable on nonnegative time.
-/
def Statement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (X : RealProcess Ω),
    (∀ᵐ ω ∂P, X 0 ω = 0) →
    HasStandardWienerIncrements X P →
    ∃ Y : RealProcess Ω, IsModification X Y P ∧
      ∀ᵐ ω ∂P,
        ContinuousOn (fun t => Y t ω) (Ici (0 : ℝ)) ∧
          NowhereDifferentiableOnNonnegative (fun t => Y t ω)

/- Scope mutations used by the statement validator. -/
def mutationContinuityOnly : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (X : RealProcess Ω),
    (∀ᵐ ω ∂P, X 0 ω = 0) → HasStandardWienerIncrements X P →
    ∃ Y : RealProcess Ω, IsModification X Y P ∧
      ∀ᵐ ω ∂P, ContinuousOn (fun t => Y t ω) (Ici (0 : ℝ))

def mutationIndistinguishableVersion : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (X : RealProcess Ω),
    (∀ᵐ ω ∂P, X 0 ω = 0) → HasStandardWienerIncrements X P →
    ∃ Y : RealProcess Ω, (∀ᵐ ω ∂P, ∀ t, X t ω = Y t ω) ∧
      ∀ᵐ ω ∂P, ContinuousOn (fun t => Y t ω) (Ici (0 : ℝ)) ∧
        NowhereDifferentiableOnNonnegative (fun t => Y t ω)

def mutationNoIncrementIndependence : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (X : RealProcess Ω),
    (∀ᵐ ω ∂P, X 0 ω = 0) →
    (∀ {n : ℕ} (t : Fin (n + 1) → ℝ), ∀ ht : IsNonnegativeGrid t,
      ∀ i : Fin n, HasLaw (increment X t i)
        (gaussianReal 0 ⟨t i.succ - t i.castSucc,
          sub_nonneg.mpr (ht.2 (Fin.castSucc_le_succ i))⟩) P) →
    ∃ Y : RealProcess Ω, IsModification X Y P ∧
      ∀ᵐ ω ∂P, ContinuousOn (fun t => Y t ω) (Ici (0 : ℝ)) ∧
        NowhereDifferentiableOnNonnegative (fun t => Y t ω)

def mutationWholeRealTime : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (X : RealProcess Ω),
    (∀ᵐ ω ∂P, X 0 ω = 0) → HasStandardWienerIncrements X P →
    ∃ Y : RealProcess Ω, IsModification X Y P ∧
      ∀ᵐ ω ∂P, Continuous (fun t => Y t ω) ∧
        (∀ t : ℝ, ¬ DifferentiableAt ℝ (fun s => Y s ω) t)

#print AwesomeTheorems.Stage1.THM_M_1028.Statement

end AwesomeTheorems.Stage1.THM_M_1028
