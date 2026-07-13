import ObligationTree

/-!
# THM-M-1272 independent compactness validation probe

This module reconstructs the compactness branch under independently named
declarations. It deliberately imports the frozen statement and composer, not
`Proof`, and keeps the symmetric minimax package as an explicit premise.
-/

noncomputable section

open Filter Set
open scoped Topology

namespace Stage1Instances.THM_M_1272.Validation

universe u

/-- Convergence to a finite level makes the functional values bounded. -/
theorem convergent_level_has_bounded_range
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Phi : E → ℝ} {v : ℕ → E} {c : ℝ}
    (hvalue : Tendsto (fun n ↦ Phi (v n)) atTop (nhds c)) :
    Bornology.IsBounded (Set.range (fun n ↦ Phi (v n))) := by
  exact Metric.isBounded_range_of_tendsto _ hvalue

/-- Global Palais-Smale compactness applies to a sequence at a fixed level. -/
theorem extract_level_subsequence
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Phi : E → ℝ} {v : ℕ → E} {c : ℝ}
    (hPS : PalaisSmale Phi)
    (hvalue : Tendsto (fun n ↦ Phi (v n)) atTop (nhds c))
    (hderiv : Tendsto (fun n ↦ ‖fderiv ℝ Phi (v n)‖) atTop (nhds 0)) :
    ∃ x : E, ∃ sigma : ℕ → ℕ,
      StrictMono sigma ∧ Tendsto (fun n ↦ v (sigma n)) atTop (nhds x) := by
  have hb : Bornology.IsBounded (Set.range (Phi ∘ v)) := by
    simpa [Function.comp_def] using convergent_level_has_bounded_range hvalue
  obtain ⟨x, sigma, hsigma, hx⟩ := hPS v hb hderiv
  exact ⟨x, sigma, hsigma, by simpa [Function.comp_def] using hx⟩

/-- Continuity of a `C¹` functional and its derivative identifies the limit. -/
theorem identify_level_limit
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Phi : E → ℝ} {v : ℕ → E} {c : ℝ} {x : E} {sigma : ℕ → ℕ}
    (hC1 : ContDiff ℝ 1 Phi)
    (hvalue : Tendsto (fun n ↦ Phi (v n)) atTop (nhds c))
    (hderiv : Tendsto (fun n ↦ ‖fderiv ℝ Phi (v n)‖) atTop (nhds 0))
    (hsigma : StrictMono sigma)
    (hconv : Tendsto (fun n ↦ v (sigma n)) atTop (nhds x)) :
    IsCriticalPoint Phi x ∧ Phi x = c := by
  have hvalues_c : Tendsto (fun n ↦ Phi (v (sigma n))) atTop (nhds c) :=
    hvalue.comp hsigma.tendsto_atTop
  have hvalues_x : Tendsto (fun n ↦ Phi (v (sigma n))) atTop (nhds (Phi x)) :=
    (hC1.continuous.tendsto x).comp hconv
  have hnorm_zero :
      Tendsto (fun n ↦ ‖fderiv ℝ Phi (v (sigma n))‖) atTop (nhds (0 : ℝ)) :=
    hderiv.comp hsigma.tendsto_atTop
  have hnorm_x :
      Tendsto (fun n ↦ ‖fderiv ℝ Phi (v (sigma n))‖) atTop
        (nhds ‖fderiv ℝ Phi x‖) := by
    exact (((hC1.continuous_fderiv one_ne_zero).tendsto x).comp hconv).norm
  constructor
  · exact norm_eq_zero.mp (tendsto_nhds_unique hnorm_x hnorm_zero)
  · exact tendsto_nhds_unique hvalues_x hvalues_c

/-- Independently reconstructed exact compactness package. -/
theorem independentlyReconstructedLimitPackage : FountainLimitPackage.{u} := by
  intro E _group _inner _complete Phi c v hC1 hPS hvalue hderiv
  choose x sigma hsigma hconv using fun k ↦
    extract_level_subsequence hPS (hvalue k) (hderiv k)
  refine ⟨x, ?_, ?_⟩
  · intro k
    exact (identify_level_limit hC1 (hvalue k) (hderiv k) (hsigma k) (hconv k)).1
  · intro k
    exact (identify_level_limit hC1 (hvalue k) (hderiv k) (hsigma k) (hconv k)).2

/-- The frozen composer reaches the exact root only under the still-open
symmetric minimax premise. -/
theorem independentlyValidatedConditionalRoot
    (minimax : FountainMinimaxPackage.{u}) : FountainTheoremTarget.{u} := by
  exact root_of_minimax_and_limit_packages minimax independentlyReconstructedLimitPackage

example : FountainLimitPackage.{u} := independentlyReconstructedLimitPackage

#check convergent_level_has_bounded_range
#check extract_level_subsequence
#check identify_level_limit
#check independentlyReconstructedLimitPackage
#check independentlyValidatedConditionalRoot
#print axioms convergent_level_has_bounded_range
#print axioms extract_level_subsequence
#print axioms identify_level_limit
#print axioms independentlyReconstructedLimitPackage
#print axioms independentlyValidatedConditionalRoot

end Stage1Instances.THM_M_1272.Validation
