import «Statement»

/-! Checked composition interface for the frozen THM-M-0578 architecture. -/

namespace Stage1Instances.THM_M_0578.ObligationTree

open scoped Manifold ContDiff
open Metric (sphere)

/-- Output expected after construction, topology, and smooth obstruction. -/
def ExoticWitnessPackage : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞ M),
    Nonempty (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 8)) 1) ∧
      IsEmpty
        (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)),
          𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
            sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

/-- Child-to-parent composition. This consumes, but does not construct, a
complete exotic witness package. -/
theorem root_of_exoticWitnessPackage
    (h : ExoticWitnessPackage) : MilnorExoticSphereTarget := by
  rcases h with ⟨M, top, chart, manifold, ⟨homeo⟩, nondiff⟩
  exact ⟨M, top, chart, manifold, homeo, nondiff⟩

#check root_of_exoticWitnessPackage
#print axioms root_of_exoticWitnessPackage

end Stage1Instances.THM_M_0578.ObligationTree
