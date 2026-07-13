import Mathlib.Geometry.Manifold.WhitneyEmbedding
import Mathlib.Topology.Maps.Proper.Basic

/-!
# Checked proof support for THM-M-0594

These lemmas close two infrastructure interfaces used by the frozen proof
architecture. They do not construct the finite-dimensional smooth embedding
required by the unrestricted root.
-/

noncomputable section

open Function Set Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594

universe uE uH uM uN

/-- The target assumptions provide a compact exhaustion of the source manifold. -/
theorem exists_compact_exhaustion
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M] :
    Nonempty (CompactExhaustion M) := by
  letI : LocallyCompactSpace M := Manifold.locallyCompact_of_finiteDimensional I
  letI : SigmaCompactSpace M :=
    sigmaCompactSpace_of_locallyCompact_secondCountable
  exact ⟨CompactExhaustion.choice M⟩

/-- The target assumptions provide a locally finite smooth bump covering. -/
theorem exists_global_smooth_bump_covering
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M] :
    ∃ (ι : Type uM) (f : SmoothBumpCovering ι I M),
      f.IsSubordinate (fun _ : M => univ) := by
  letI : LocallyCompactSpace M := Manifold.locallyCompact_of_finiteDimensional I
  letI : SigmaCompactSpace M :=
    sigmaCompactSpace_of_locallyCompact_secondCountable
  exact SmoothBumpCovering.exists_isSubordinate I isClosed_univ
    (fun _ _ => Filter.univ_mem)

/-- A proper injective continuous map is a topological embedding. -/
theorem isEmbedding_of_isProperMap_of_injective
    {M : Type uM} {N : Type uN} [TopologicalSpace M] [TopologicalSpace N]
    {f : M -> N} (proper : IsProperMap f) (injective : Injective f) :
    IsEmbedding f :=
  (IsClosedEmbedding.of_continuous_injective_isClosedMap
    proper.continuous injective proper.isClosedMap).isEmbedding

#print axioms exists_compact_exhaustion
#print axioms exists_global_smooth_bump_covering
#print axioms isEmbedding_of_isProperMap_of_injective

#check @SmoothBumpCovering.exists_immersion_euclidean
#check @SmoothBumpCovering.fintype

end Stage1Instances.THM_M_0594
