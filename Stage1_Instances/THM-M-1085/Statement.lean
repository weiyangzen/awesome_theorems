import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic

/-!
# THM-M-1085: exact Slepian comparison statement

This module freezes and tests the finite-dimensional distributional statement only. It does not
contain a proof of Slepian's lemma.
-/

open MeasureTheory ProbabilityTheory Set

namespace Stage1Instances.THM_M_1085

universe u v w

/-- Every coordinate of a random vector is at most the threshold. This formulation avoids making
an arbitrary choice of a maximum and keeps the event meaningful on the declared nonempty index
type. -/
def BelowAll {I : Type u} {Ω : Type v} (X : Ω → I → ℝ) (t : ℝ) : Set Ω :=
  {ω | ∀ i, X ω i ≤ t}

/-- The intake-selected finite-dimensional form of Slepian's lemma. The vectors may live on
different probability spaces; comparison therefore depends only on their laws. -/
def SlepianTarget : Prop :=
  ∀ (I : Type u) [Fintype I] [Nonempty I]
    (ΩX : Type v) [MeasurableSpace ΩX] (μX : Measure ΩX)
    (ΩY : Type w) [MeasurableSpace ΩY] (μY : Measure ΩY)
    (X : ΩX → I → ℝ) (Y : ΩY → I → ℝ),
      HasGaussianLaw X μX →
      HasGaussianLaw Y μY →
      (∀ i, (∫ ω, X ω i ∂μX) = 0) →
      (∀ i, (∫ ω, Y ω i ∂μY) = 0) →
      (∀ i, covariance (fun ω => X ω i) (fun ω => X ω i) μX =
        covariance (fun ω => Y ω i) (fun ω => Y ω i) μY) →
      (∀ i j, i ≠ j →
        covariance (fun ω => X ω i) (fun ω => X ω j) μX ≤
          covariance (fun ω => Y ω i) (fun ω => Y ω j) μY) →
      ∀ t : ℝ, μX (BelowAll X t) ≤ μY (BelowAll Y t)

/-- Direct source-shape expansion used to check that `BelowAll` introduces no semantic change. -/
def DirectSlepianShape : Prop :=
  ∀ (I : Type u) [Fintype I] [Nonempty I]
    (ΩX : Type v) [MeasurableSpace ΩX] (μX : Measure ΩX)
    (ΩY : Type w) [MeasurableSpace ΩY] (μY : Measure ΩY)
    (X : ΩX → I → ℝ) (Y : ΩY → I → ℝ),
      HasGaussianLaw X μX → HasGaussianLaw Y μY →
      (∀ i, (∫ ω, X ω i ∂μX) = 0) →
      (∀ i, (∫ ω, Y ω i ∂μY) = 0) →
      (∀ i, covariance (fun ω => X ω i) (fun ω => X ω i) μX =
        covariance (fun ω => Y ω i) (fun ω => Y ω i) μY) →
      (∀ i j, i ≠ j → covariance (fun ω => X ω i) (fun ω => X ω j) μX ≤
        covariance (fun ω => Y ω i) (fun ω => Y ω j) μY) →
      ∀ t : ℝ, μX {ω | ∀ i, X ω i ≤ t} ≤ μY {ω | ∀ i, Y ω i ≤ t}

theorem slepianTarget_iff_directShape :
    SlepianTarget.{u, v, w} ↔ DirectSlepianShape.{u, v, w} := by
  rfl

-- Structural mutations are elaborated separately and rejected by the statement validator.
def mutationRemovedEqualVariance : Prop :=
  ∀ (I : Type u) [Fintype I] [Nonempty I]
    (ΩX : Type v) [MeasurableSpace ΩX] (μX : Measure ΩX)
    (ΩY : Type w) [MeasurableSpace ΩY] (μY : Measure ΩY)
    (X : ΩX → I → ℝ) (Y : ΩY → I → ℝ),
      HasGaussianLaw X μX → HasGaussianLaw Y μY →
      (∀ i, (∫ ω, X ω i ∂μX) = 0) →
      (∀ i, (∫ ω, Y ω i ∂μY) = 0) →
      (∀ i j, i ≠ j → covariance (fun ω => X ω i) (fun ω => X ω j) μX ≤
        covariance (fun ω => Y ω i) (fun ω => Y ω j) μY) →
      ∀ t : ℝ, μX (BelowAll X t) ≤ μY (BelowAll Y t)

def mutationChangedDomain : Prop :=
  ∀ (I : Type u) [Fintype I] [Nonempty I] (X Y : I → ℝ),
    (∀ i, X i = Y i) → ∀ t, (∀ i, X i ≤ t) ↔ ∀ i, Y i ≤ t

def mutationChangedBinderScope : Prop :=
  ∀ (I : Type u) [Fintype I] [Nonempty I]
    (ΩX : Type v) [MeasurableSpace ΩX] (μX : Measure ΩX)
    (ΩY : Type w) [MeasurableSpace ΩY] (μY : Measure ΩY)
    (X : ΩX → I → ℝ) (Y : ΩY → I → ℝ) (t : ℝ),
      HasGaussianLaw X μX → HasGaussianLaw Y μY →
      μX (BelowAll X t) ≤ μY (BelowAll Y t)

def mutationEmptyIndexAllowed : Prop :=
  ∀ (I : Type u) [Fintype I]
    (ΩX : Type v) [MeasurableSpace ΩX] (μX : Measure ΩX)
    (ΩY : Type w) [MeasurableSpace ΩY] (μY : Measure ΩY)
    (X : ΩX → I → ℝ) (Y : ΩY → I → ℝ),
      HasGaussianLaw X μX → HasGaussianLaw Y μY →
      ∀ t : ℝ, μX (BelowAll X t) ≤ μY (BelowAll Y t)

/-- On a singleton index, the lower-tail event is exactly the coordinate lower-tail event. -/
theorem singleton_boundary {Ω : Type v} (X : Ω → Unit → ℝ) (t : ℝ) :
    BelowAll X t = {ω | X ω () ≤ t} := by
  ext ω
  constructor
  · exact fun h => h ()
  · intro h i
    cases i
    exact h

end Stage1Instances.THM_M_1085

set_option pp.explicit true in
#print Stage1Instances.THM_M_1085.SlepianTarget
