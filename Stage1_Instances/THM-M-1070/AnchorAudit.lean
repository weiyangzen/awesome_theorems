import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.IdentDistrib

/-!
# THM-M-1070 anchor audit probes

These declarations check the mathlib surfaces used by the frozen statement. They do not prove
existence, regularization, or a characterization theorem for Levy processes.
-/

open Filter MeasureTheory
open scoped NNReal Topology

namespace Stage1Instances.THM_M_1070.AnchorAudit

open ProbabilityTheory

/-- The pinned mathlib independent-increment predicate has exactly the finite-family expansion
used by the canonical target. -/
theorem hasIndepIncrements_iff_finiteFamily
    {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) (X : ℝ≥0 → Ω → ℝ) :
    HasIndepIncrements X P ↔
      ∀ n, ∀ t : Fin (n + 1) → ℝ≥0, Monotone t →
        iIndepFun (fun (i : Fin n) ω ↦ X (t i.succ) ω - X (t i.castSucc) ω) P := by
  rfl

/-- Pinned mathlib also supplies the pairwise consequence, but the converse is not credited. -/
theorem pairwiseConsequence
    {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) (X : ℝ≥0 → Ω → ℝ)
    (h : HasIndepIncrements X P) {r s t : ℝ≥0} (hrs : r ≤ s) (hst : s ≤ t) :
    IndepFun (X s - X r) (X t - X s) P :=
  h.indepFun_sub_sub hrs hst

#check ProbabilityTheory.IdentDistrib
#check MeasureTheory.TendstoInMeasure
#check ProbabilityTheory.hasIndepIncrements_iff_nat
#check ProbabilityTheory.HasIndepIncrements.indepFun_sub_sub

end Stage1Instances.THM_M_1070.AnchorAudit

#print axioms Stage1Instances.THM_M_1070.AnchorAudit.hasIndepIncrements_iff_finiteFamily
#print axioms Stage1Instances.THM_M_1070.AnchorAudit.pairwiseConsequence
