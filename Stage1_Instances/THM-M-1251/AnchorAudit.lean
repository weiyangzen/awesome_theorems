import Mathlib.Analysis.Distribution.TemperedDistribution

/-!
# THM-M-1251: pinned formal-anchor probes

The canonical target uses exactly mathlib's pointwise-convergence definition.
The stronger locally convex strong-dual interpretation is not asserted here.
-/

noncomputable section

open scoped SchwartzMap

universe u

namespace Stage1Instances.THM_M_1251.AnchorAudit

/-- The statement-gate target, repeated here because standalone Lean checks do
not create an importable olean for the dossier's statement source. -/
def CanonicalTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E],
      TemperedDistribution E ℂ = (SchwartzMap E ℂ →Lₚₜ[ℂ] ℂ)

#check TemperedDistribution
#check SchwartzMap
#check PointwiseConvergenceCLM
#check SchwartzMap.toTemperedDistributionCLM
#check SchwartzMap.toTemperedDistributionCLM_apply_apply

/-- Exact checked wrapper around the pinned mathlib definitional anchor. -/
theorem exactMathlibAnchor :
    CanonicalTarget.{u} := by
  intro E _ _ _
  rfl

end Stage1Instances.THM_M_1251.AnchorAudit

#print axioms Stage1Instances.THM_M_1251.AnchorAudit.exactMathlibAnchor
