import Mathlib.Geometry.Manifold.Complex

/-!
# THM-M-0183: Yau's Calabi conjecture statement boundary

The pinned mathlib snapshot has complex-manifold and compactness infrastructure,
but no native analytic Kahler metric, real first Chern class, Ricci tensor, or
Kahler cohomology-class API. The structures below expose those missing notions
as typed interfaces. No field assumes the existence of the desired metric.

This module freezes and elaborates the target only. It does not prove Yau's
theorem.
-/

noncomputable section

open scoped Manifold

namespace Stage1Instances.THMM0183

universe u

/-- A compact smooth complex manifold together with the missing cohomological
interfaces needed to state the Ricci-flat corollary of Yau's theorem. -/
structure CalabiYauDomain
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] where
  smoothComplexManifold : IsManifold I ω M
  hausdorff : T2Space M
  realDegreeTwoCohomology : Type u
  zeroClass : realDegreeTwoCohomology
  firstChernClassReal : realDegreeTwoCohomology
  kahlerClass : Type u
  isKahlerClass : kahlerClass → Prop

/-- The missing metric-side interface. Its predicates describe, but do not
provide, a compatible Kahler metric representing a prescribed class. -/
structure KahlerMetricInterface
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M]
    (X : CalabiYauDomain E H I M) where
  metric : Type u
  representsClass : metric → X.kahlerClass → Prop
  compatibleWithComplexStructure : metric → Prop
  isKahlerMetric : metric → Prop
  ricciTensorVanishes : metric → Prop

/-- Exact selected root: every prescribed Kahler class on a compact smooth
complex Kahler manifold with vanishing real first Chern class contains a
compatible Ricci-flat Kahler metric. -/
def YauCalabiConjectureTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [CompactSpace M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X)
    (κ : X.kahlerClass),
      X.firstChernClassReal = X.zeroClass →
      X.isKahlerClass κ →
      ∃ g : G.metric,
        G.representsClass g κ ∧
        G.compatibleWithComplexStructure g ∧
        G.isKahlerMetric g ∧
        G.ricciTensorVanishes g

/-- Direct expansion of the repository's historical normalized statement
shape, with its abstract missing-library interfaces made explicit. -/
def PinnedCandidateSourceShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [CompactSpace M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X)
    (κ : X.kahlerClass),
      X.firstChernClassReal = X.zeroClass →
      X.isKahlerClass κ →
      ∃ g : G.metric,
        G.representsClass g κ ∧
        G.compatibleWithComplexStructure g ∧
        G.isKahlerMetric g ∧
        G.ricciTensorVanishes g

/-- Checked identity with the direct historical-shape expansion. -/
theorem yauCalabiConjectureTarget_iff_pinnedCandidateSourceShape :
    YauCalabiConjectureTarget.{u} ↔ PinnedCandidateSourceShape.{u} :=
  Iff.rfl

-- Separately elaborated structural mutations; none receives equivalence credit.
def MutationRemovedCompactness : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X)
    (κ : X.kahlerClass),
      X.firstChernClassReal = X.zeroClass → X.isKahlerClass κ →
      ∃ g : G.metric, G.representsClass g κ ∧
        G.compatibleWithComplexStructure g ∧ G.isKahlerMetric g ∧
        G.ricciTensorVanishes g

def MutationRemovedFirstChernVanishing : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [CompactSpace M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X)
    (κ : X.kahlerClass), X.isKahlerClass κ →
      ∃ g : G.metric, G.representsClass g κ ∧ G.isKahlerMetric g ∧
        G.ricciTensorVanishes g

def MutationUnspecifiedKahlerClass : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [CompactSpace M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X),
      X.firstChernClassReal = X.zeroClass →
      ∃ κ : X.kahlerClass, X.isKahlerClass κ ∧
        ∃ g : G.metric, G.representsClass g κ ∧ G.isKahlerMetric g ∧
          G.ricciTensorVanishes g

def MutationRicciFlatRiemannianOnly : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [CompactSpace M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X)
    (κ : X.kahlerClass),
      X.firstChernClassReal = X.zeroClass → X.isKahlerClass κ →
      ∃ g : G.metric, G.ricciTensorVanishes g

end Stage1Instances.THMM0183

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0183.YauCalabiConjectureTarget
