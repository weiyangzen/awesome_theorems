import Mathlib.Probability.StrongLaw

/-!
# THM-M-0985 anchor compatibility audit

This module checks that the pinned mathlib strong-law declaration has the
right interfaces for the frozen target. The wrapper is audit evidence for the
candidate crosswalk; later nodes must still register its proof obligations and
perform the full trust and release validation.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THMM0985.AnchorAudit

universe u

/-- Mutual independence supplies the pairwise independence required by the
pinned Etemadi-style mathlib theorem. -/
theorem pairwise_of_iIndepFun {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ℕ → Ω → ℝ)
    (hX : ProbabilityTheory.iIndepFun X μ) :
    Pairwise (Function.onFun (fun f g => ProbabilityTheory.IndepFun f g μ) X) := by
  intro i j hij
  exact hX.indepFun hij

/-- Exact compatibility witness for the expression frozen in `Statement.lean`
to the pinned `ProbabilityTheory.strong_law_ae`. Its binders, assumptions,
zero-based sum, a.e. convergence, and integral agree literally with the
checked expansion `kolmogorovStrongLaw_iff`. -/
theorem mathlib_candidate_matches_exact_target :
    ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
        (X : ℕ → Ω → ℝ),
      (∀ n, Measurable (X n)) →
      ProbabilityTheory.iIndepFun X μ →
      (∀ n, ProbabilityTheory.IdentDistrib (X n) (X 0) μ μ) →
      Integrable (X 0) μ →
      ∀ᵐ ω ∂μ,
        Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * ∑ i ∈ range n, X i ω)
          atTop (𝓝 (∫ x, X 0 x ∂μ)) := by
  intro Ω _ μ _ X _hMeas hIndep hIdent hIntegrable
  simpa [smul_eq_mul] using
    (ProbabilityTheory.strong_law_ae X hIntegrable
      (pairwise_of_iIndepFun μ X hIndep) hIdent)

#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_Lp
#print axioms pairwise_of_iIndepFun
#print axioms mathlib_candidate_matches_exact_target

end Stage1Instances.THMM0985.AnchorAudit
