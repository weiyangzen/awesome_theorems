import ObligationTree

/-!
# THM-M-1272 proved compactness and assembly units

This module implements the compactness half of the frozen Fountain architecture.
The genuinely variational minimax construction remains an explicit input to the
final composition theorem; no unconditional Fountain theorem is declared here.
-/

noncomputable section

open Filter Set
open scoped Topology

namespace Stage1Instances.THM_M_1272

universe u

/-- Levelwise Palais-Smale data used by the compactness package. -/
def IsPalaisSmaleSequence
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (Phi : E → ℝ) (c : ℝ) (v : ℕ → E) : Prop :=
  Tendsto (fun n => Phi (v n)) atTop (nhds c) ∧
    Tendsto (fun n => ‖fderiv ℝ Phi (v n)‖) atTop (nhds 0)

/-- Convergence of the functional values at a level supplies the bounded-range
premise required by the global Palais-Smale hypothesis. -/
theorem bounded_values_of_level_tendsto
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Phi : E → ℝ} {v : ℕ → E} {c : ℝ}
    (hvalue : Tendsto (Phi ∘ v) atTop (nhds c)) :
    Bornology.IsBounded (Set.range (Phi ∘ v)) := by
  exact Metric.isBounded_range_of_tendsto (Phi ∘ v) hvalue

/-- The global Palais-Smale hypothesis extracts a convergent subsequence from
levelwise Palais-Smale data. -/
theorem palaisSmale_subsequence
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Phi : E → ℝ} {c : ℝ} {v : ℕ → E}
    (hPS : PalaisSmale Phi) (hv : IsPalaisSmaleSequence Phi c v) :
    ∃ x : E, ∃ sigma : ℕ → ℕ,
      StrictMono sigma ∧ Tendsto (v ∘ sigma) atTop (nhds x) := by
  apply hPS v
  · exact bounded_values_of_level_tendsto hv.1
  · exact hv.2

/-- A convergent Palais-Smale subsequence converges to a critical point at the
specified level. Continuity of both maps follows from the canonical `C^1`
hypothesis. -/
theorem critical_point_at_level_of_subsequence
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Phi : E → ℝ} {c : ℝ} {v : ℕ → E} {x : E} {sigma : ℕ → ℕ}
    (hC1 : ContDiff ℝ 1 Phi) (hv : IsPalaisSmaleSequence Phi c v)
    (hsigma : StrictMono sigma)
    (hx : Tendsto (v ∘ sigma) atTop (nhds x)) :
    IsCriticalPoint Phi x ∧ Phi x = c := by
  have hvalueSub :
      Tendsto (fun n => Phi (v (sigma n))) atTop (nhds c) := by
    simpa [Function.comp_def] using hv.1.comp hsigma.tendsto_atTop
  have hvalueAtX :
      Tendsto (fun n => Phi (v (sigma n))) atTop (nhds (Phi x)) := by
    simpa [Function.comp_def] using hC1.continuous.tendsto x |>.comp hx
  have hderivSub :
      Tendsto (fun n => ‖fderiv ℝ Phi (v (sigma n))‖) atTop (nhds (0 : ℝ)) := by
    simpa [Function.comp_def] using hv.2.comp hsigma.tendsto_atTop
  have hderivAtX :
      Tendsto (fun n => ‖fderiv ℝ Phi (v (sigma n))‖) atTop
        (nhds ‖fderiv ℝ Phi x‖) := by
    have hmap :
        Tendsto (fun n => fderiv ℝ Phi (v (sigma n))) atTop
          (nhds (fderiv ℝ Phi x)) := by
      simpa [Function.comp_def] using
        (hC1.continuous_fderiv one_ne_zero).tendsto x |>.comp hx
    exact hmap.norm
  constructor
  · exact norm_eq_zero.mp (tendsto_nhds_unique hderivAtX hderivSub)
  · exact tendsto_nhds_unique hvalueAtX hvalueSub

/-- The compactness half of the frozen architecture, proved from the canonical
`C^1` and global Palais-Smale hypotheses. -/
theorem fountainLimitPackage_proof : FountainLimitPackage.{u} := by
  intro E _group _inner _complete Phi c v hC1 hPS hvalue hderiv
  choose x sigma hsigma hx using fun k =>
    palaisSmale_subsequence hPS ⟨hvalue k, hderiv k⟩
  refine ⟨x, ?_, ?_⟩
  · intro k
    exact (critical_point_at_level_of_subsequence hC1 ⟨hvalue k, hderiv k⟩
      (hsigma k) (hx k)).1
  · intro k
    exact (critical_point_at_level_of_subsequence hC1 ⟨hvalue k, hderiv k⟩
      (hsigma k) (hx k)).2

/-- Exact-root assembly from the still-open symmetric minimax package and the
proved compactness package. The minimax premise is visible in the type and
therefore receives no proof credit from this declaration. -/
theorem fountainTheoremTarget_of_minimax
    (minimax : FountainMinimaxPackage.{u}) : FountainTheoremTarget.{u} :=
  root_of_minimax_and_limit_packages minimax fountainLimitPackage_proof

#check bounded_values_of_level_tendsto
#check palaisSmale_subsequence
#check critical_point_at_level_of_subsequence
#check fountainLimitPackage_proof
#check fountainTheoremTarget_of_minimax
#print axioms bounded_values_of_level_tendsto
#print axioms palaisSmale_subsequence
#print axioms critical_point_at_level_of_subsequence
#print axioms fountainLimitPackage_proof
#print axioms fountainTheoremTarget_of_minimax

end Stage1Instances.THM_M_1272
