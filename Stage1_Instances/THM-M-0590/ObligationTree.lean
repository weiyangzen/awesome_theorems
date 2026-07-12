import Statement

/-!
# THM-M-0590 conditional obligation composition

This module checks only the final logical composition selected by the frozen
architecture.  The forward invariance and backward classification packages
remain explicit premises; no BDF proof is asserted here.
-/

namespace THMM0590

universe u v

/-- The forward half of the exact classification, retained as an open package. -/
def ForwardInvariantPackage : Prop :=
  forall (H : Type u) (K : Type v)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [TopologicalSpace.SeparableSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    [TopologicalSpace.SeparableSpace K]
    (T : H →L[ℂ] H) (S : K →L[ℂ] K),
    (¬ FiniteDimensional ℂ H) → (¬ FiniteDimensional ℂ K) →
    IsEssentiallyNormal T → IsEssentiallyNormal S →
    UnitaryEquivalentModuloCompacts T S →
      essentialSpectrum T = essentialSpectrum S ∧
        forall z : ℂ, z ∉ essentialSpectrum T →
          fredholmIndex (T - z • ContinuousLinearMap.id ℂ H) =
            fredholmIndex (S - z • ContinuousLinearMap.id ℂ K)

/-- The backward BDF classification half, retained as an open package. -/
def BackwardClassificationPackage : Prop :=
  forall (H : Type u) (K : Type v)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [TopologicalSpace.SeparableSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    [TopologicalSpace.SeparableSpace K]
    (T : H →L[ℂ] H) (S : K →L[ℂ] K),
    (¬ FiniteDimensional ℂ H) → (¬ FiniteDimensional ℂ K) →
    IsEssentiallyNormal T → IsEssentiallyNormal S →
    (essentialSpectrum T = essentialSpectrum S ∧
      forall z : ℂ, z ∉ essentialSpectrum T →
        fredholmIndex (T - z • ContinuousLinearMap.id ℂ H) =
          fredholmIndex (S - z • ContinuousLinearMap.id ℂ K)) →
      UnitaryEquivalentModuloCompacts T S

/-- Checked composition of the two exact directional packages into the canonical target. -/
theorem root_of_directional_packages
    (forward : ForwardInvariantPackage.{u, v})
    (backward : BackwardClassificationPackage.{u, v}) :
    brownDouglasFillmoreTarget.{u, v} := by
  intro H K _ _ _ _ _ _ _ _ T S hH hK hT hS
  constructor
  · exact forward H K T S hH hK hT hS
  · exact backward H K T S hH hK hT hS

#print axioms root_of_directional_packages

end THMM0590
