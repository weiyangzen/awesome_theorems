import Mathlib.Probability.StrongLaw

/-!
# THM-M-0984 anchor-audit probe

This file checks the exact pinned mathlib endpoint for the modern target frozen
in `Statement.lean`. The proof body remains in mathlib; this is only the narrow
repo-local wrapper needed to verify the candidate's type and trust report.
-/

noncomputable section

open Filter Finset Function MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0984.AnchorAudit

universe u v

/-- Exact wrapper for the frozen explicit target. -/
theorem strongLawAnchor
    (Omega : Type u) [MeasurableSpace Omega]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [CompleteSpace E] [MeasurableSpace E] [BorelSpace E]
    (mu : Measure Omega) (X : Nat -> Omega -> E)
    (h_integrable : Integrable (X 0) mu)
    (h_independent : Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X))
    (h_identical : forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) :
    ∀ᵐ omega ∂mu,
      Tendsto (fun n : Nat => (n : Real)⁻¹ • (∑ i ∈ range n, X i omega))
        atTop (nhds (integral mu (X 0))) :=
  ProbabilityTheory.strong_law_ae X h_integrable h_independent h_identical

#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_Lp
#check strongLawAnchor

#print axioms ProbabilityTheory.strong_law_ae
#print axioms strongLawAnchor

end Stage1Instances.THM_M_0984.AnchorAudit
