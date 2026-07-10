import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# S1-M-295 / THM-M-1016: Delta method

This Stage1 artifact records a Lean 4 statement shape and a checked local
bridge for the one-dimensional Delta method.

The full Delta method says that if `a n * (X n - theta)` converges in
distribution to `Z`, `g` is differentiable at `theta`, and the usual local
linearization hypotheses make the Taylor remainder negligible, then
`a n * (g (X n) - g theta)` converges in distribution to `g' * Z`.

The pinned mathlib snapshot contains the continuous mapping theorem and a
Slutsky-style bridge from convergence in distribution plus convergence in
measure of a difference.  This file therefore proves the repo-local bridge
under an explicit `TendstoInMeasure` remainder hypothesis.  It does not claim a
terminal proof of the analytic Taylor-remainder step.

Scope decision for Stage1 backfill: keep the public target as the
one-dimensional real Delta method first.  A normed-space Frechet-derivative
generalization should be a later branch after the vector-valued
`TendstoInDistribution`, bounded-in-probability, measurability, and Taylor
remainder APIs have been audited.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_295

universe uΩ uΩ'

/-- Data appearing in a one-dimensional Delta-method statement. -/
structure DeltaMethodData
    (Ω : Type uΩ) (Ω' : Type uΩ') [MeasurableSpace Ω] [MeasurableSpace Ω'] :
    Type (max uΩ uΩ') where
  P : Measure Ω
  P' : Measure Ω'
  isProbabilityP : IsProbabilityMeasure P
  isProbabilityP' : IsProbabilityMeasure P'
  X : ℕ → Ω → ℝ
  Z : Ω' → ℝ
  theta : ℝ
  scale : ℕ → ℝ
  g : ℝ → ℝ
  gDeriv : ℝ

/-- The normalized input statistic `a_n (X_n - theta)`. -/
def normalizedInputStatistic
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω => D.scale n * (D.X n ω - D.theta)

/-- The linearized target statistic `g'(theta) * a_n (X_n - theta)`. -/
def linearizedStatistic
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω => D.gDeriv * normalizedInputStatistic D n ω

/-- The transformed statistic `a_n (g(X_n) - g(theta))`. -/
def deltaStatistic
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω => D.scale n * (D.g (D.X n ω) - D.g D.theta)

/-- The limiting linear transform of the distributional limit. -/
def linearizedLimit
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : Ω' → ℝ :=
  fun ω' => D.gDeriv * D.Z ω'

/-- The pointwise difference quotient used in the Taylor-remainder package.

It is defined as `0` at the expansion point so that the expression is total;
the algebraic product identity below shows that this convention does not
change the normalized Taylor remainder.
-/
def taylorDifferenceQuotient
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω =>
    if D.X n ω = D.theta then 0
    else (D.g (D.X n ω) - D.g D.theta) / (D.X n ω - D.theta)

/-- Difference quotient centered by the derivative at the expansion point. -/
def taylorRemainderQuotient
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω => taylorDifferenceQuotient D n ω - D.gDeriv

/-- Product form of the normalized Taylor remainder. -/
def taylorProductRemainder
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω => taylorRemainderQuotient D n ω * normalizedInputStatistic D n ω

/--
Boundedness in probability for a real-valued sequence of random variables.

This is the tightness-style input used in the textbook proof that a quotient
converging to zero in probability times a bounded-in-probability sequence also
converges to zero in probability.
-/
def BoundedInProbability
    {Ω : Type uΩ} [MeasurableSpace Ω] (P : Measure Ω) (Y : ℕ → Ω → ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ M : ℝ, 0 ≤ M ∧
    ∀ᶠ n in atTop, P.real {ω | M ≤ |Y n ω|} < ε

/--
The theorem-tree branch still missing from the terminal one-dimensional Delta
method proof.

The first two fields are the analytic/probabilistic inputs needed for the
standard product argument.  The third field is the product-to-zero result that
would follow from them once the bounded-in-probability product lemma is
formalized.  The remaining fields keep the measurability leaves visible.
-/
structure TaylorRemainderPackage
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : Prop where
  quotientConvergesInMeasure :
    letI : IsProbabilityMeasure D.P := D.isProbabilityP
    TendstoInMeasure D.P (taylorRemainderQuotient D) atTop 0
  normalizedInputBoundedInProbability :
    BoundedInProbability D.P (normalizedInputStatistic D)
  productToZeroInMeasure :
    letI : IsProbabilityMeasure D.P := D.isProbabilityP
    TendstoInMeasure D.P (taylorProductRemainder D) atTop 0
  quotientAEMeasurable :
    ∀ n : ℕ, AEMeasurable (taylorRemainderQuotient D n) D.P
  productAEMeasurable :
    ∀ n : ℕ, AEMeasurable (taylorProductRemainder D n) D.P
  deltaAEMeasurable :
    ∀ n : ℕ, AEMeasurable (deltaStatistic D n) D.P

/--
Full Delta-method assumptions, with the Taylor-remainder reduction still left
as an explicit formalization boundary.

The final analytic package should replace `taylorRemainderBoundary` by a
checked theorem deriving the `TendstoInMeasure` remainder from differentiability
at `theta`, convergence of `X n` to `theta`, and divergence/nondegeneracy
conditions on `scale`.
-/
def FullDeltaMethodAssumptions
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : Prop := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  exact
    HasDerivAt D.g D.gDeriv D.theta ∧
      TendstoInDistribution (normalizedInputStatistic D) atTop D.Z (fun _ : ℕ => D.P) D.P' ∧
      TendstoInMeasure D.P (fun n ω => D.X n ω) atTop (fun _ => D.theta) ∧
      Tendsto D.scale atTop atTop ∧
      ∀ n : ℕ, AEMeasurable (deltaStatistic D n) D.P

/--
Assumptions for the checked bridge: normalized input convergence plus an
already-proved negligible linearization remainder.
-/
def DeltaMethodBridgeAssumptions
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : Prop := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  exact
    HasDerivAt D.g D.gDeriv D.theta ∧
      TendstoInDistribution (normalizedInputStatistic D) atTop D.Z (fun _ : ℕ => D.P) D.P' ∧
      TendstoInMeasure D.P (deltaStatistic D - linearizedStatistic D) atTop 0 ∧
      ∀ n : ℕ, AEMeasurable (deltaStatistic D n) D.P

/-- Delta-method distributional conclusion. -/
def DeltaMethodConclusion
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') : Prop := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  exact TendstoInDistribution (deltaStatistic D) atTop (linearizedLimit D) (fun _ : ℕ => D.P) D.P'

/--
Stage1 normalized full statement shape for THM-M-1016.

This is intentionally only a `Prop`: the local file has not closed the Taylor
remainder package needed to prove the terminal Delta method.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) (Ω' : Type uΩ') [MeasurableSpace Ω] [MeasurableSpace Ω'],
    ∀ D : DeltaMethodData Ω Ω',
      FullDeltaMethodAssumptions D → DeltaMethodConclusion D

/-- Checked bridge statement closed by mathlib's convergence APIs. -/
def BridgeStatementShape : Prop :=
  ∀ (Ω : Type uΩ) (Ω' : Type uΩ') [MeasurableSpace Ω] [MeasurableSpace Ω'],
    ∀ D : DeltaMethodData Ω Ω',
      DeltaMethodBridgeAssumptions D → DeltaMethodConclusion D

/-- Differentiability at the expansion point gives the local continuity anchor. -/
theorem hasDerivAt_continuousAt
    {g : ℝ → ℝ} {gDeriv theta : ℝ} (h : HasDerivAt g gDeriv theta) :
    ContinuousAt g theta :=
  h.continuousAt

/--
Continuous mapping theorem specialized to the linear map used in the Delta
method.
-/
theorem normalizedInput_linearized_converges
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω')
    (h :
      letI : IsProbabilityMeasure D.P := D.isProbabilityP
      letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
      TendstoInDistribution (normalizedInputStatistic D) atTop D.Z (fun _ : ℕ => D.P) D.P') :
    letI : IsProbabilityMeasure D.P := D.isProbabilityP
    letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
    TendstoInDistribution (linearizedStatistic D) atTop (linearizedLimit D)
      (fun _ : ℕ => D.P) D.P' := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  have hg : Continuous (fun x : ℝ => D.gDeriv * x) := continuous_const.mul continuous_id
  simpa [linearizedStatistic, normalizedInputStatistic, linearizedLimit, Function.comp_def] using
    h.continuous_comp hg

/--
Repo-local checked bridge: if the nonlinear statistic differs from its
linearization by a term converging to zero in probability, the transformed
statistic has the claimed limiting distribution.
-/
theorem deltaMethod_bridge
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') :
    DeltaMethodBridgeAssumptions D → DeltaMethodConclusion D := by
  intro h
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  rcases h with ⟨_hDeriv, hNorm, hRem, hDeltaMeas⟩
  exact tendstoInDistribution_of_tendstoInMeasure_sub
    (l := atTop) (μ'' := D.P) (μ' := D.P') (X := linearizedStatistic D)
    (Y := deltaStatistic D) (Z := linearizedLimit D)
    (normalizedInput_linearized_converges D hNorm) hRem hDeltaMeas

/-- The checked bridge statement is closed repo-locally. -/
theorem bridgeStatementShape_mathlib :
    BridgeStatementShape.{uΩ, uΩ'} :=
  fun _ _ _ _ D h => deltaMethod_bridge D h

/-- The normalized input statistic unfolds to the source expression. -/
theorem normalizedInputStatistic_apply
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') (n : ℕ) (ω : Ω) :
    normalizedInputStatistic D n ω = D.scale n * (D.X n ω - D.theta) :=
  rfl

/-- The transformed Delta statistic unfolds to the source expression. -/
theorem deltaStatistic_apply
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') (n : ℕ) (ω : Ω) :
    deltaStatistic D n ω = D.scale n * (D.g (D.X n ω) - D.g D.theta) :=
  rfl

/-- The centered quotient unfolds to the intended totalized expression. -/
theorem taylorRemainderQuotient_apply
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') (n : ℕ) (ω : Ω) :
    taylorRemainderQuotient D n ω =
      (if D.X n ω = D.theta then 0
       else (D.g (D.X n ω) - D.g D.theta) / (D.X n ω - D.theta)) - D.gDeriv :=
  rfl

/--
Algebraic quotient representation of the normalized Taylor remainder.

The branch still needs the probabilistic proof that the product on the left
converges to zero in measure; this lemma closes the deterministic algebraic
identification with the bridge remainder already consumed by mathlib.
-/
theorem taylorProductRemainder_eq_delta_sub_linearized_apply
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') (n : ℕ) (ω : Ω) :
    taylorProductRemainder D n ω =
      (deltaStatistic D - linearizedStatistic D) n ω := by
  by_cases hX : D.X n ω = D.theta
  · simp [taylorProductRemainder, taylorRemainderQuotient, taylorDifferenceQuotient,
      normalizedInputStatistic, deltaStatistic, linearizedStatistic, hX]
  · simp [taylorProductRemainder, taylorRemainderQuotient, taylorDifferenceQuotient,
      normalizedInputStatistic, deltaStatistic, linearizedStatistic, hX]
    field_simp [sub_ne_zero.mpr hX]

/-- Function-level version of the checked quotient/product representation. -/
theorem taylorProductRemainder_eq_delta_sub_linearized
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') :
    taylorProductRemainder D = deltaStatistic D - linearizedStatistic D := by
  funext n ω
  exact taylorProductRemainder_eq_delta_sub_linearized_apply D n ω

/--
The Taylor-remainder package supplies the exact `TendstoInMeasure` hypothesis
needed by the checked Delta-method bridge.
-/
theorem taylorPackage_tendstoInMeasure_remainder
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω') (hTaylor : TaylorRemainderPackage D) :
    letI : IsProbabilityMeasure D.P := D.isProbabilityP
    TendstoInMeasure D.P (deltaStatistic D - linearizedStatistic D) atTop 0 := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  simpa [taylorProductRemainder_eq_delta_sub_linearized D] using
    hTaylor.productToZeroInMeasure

/--
Once the Taylor-remainder package is available, the existing bridge assumptions
are recovered without changing the one-dimensional target.
-/
theorem deltaMethodBridgeAssumptions_of_taylorPackage
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω')
    (hDeriv : HasDerivAt D.g D.gDeriv D.theta)
    (hNorm :
      letI : IsProbabilityMeasure D.P := D.isProbabilityP
      letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
      TendstoInDistribution (normalizedInputStatistic D) atTop D.Z (fun _ : ℕ => D.P) D.P')
    (hTaylor : TaylorRemainderPackage D) :
    DeltaMethodBridgeAssumptions D := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  exact ⟨hDeriv, hNorm, taylorPackage_tendstoInMeasure_remainder D hTaylor,
    hTaylor.deltaAEMeasurable⟩

/--
End-to-end checked reduction from the Taylor-remainder package to the
distributional Delta-method conclusion.
-/
theorem deltaMethod_of_taylorPackage
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : DeltaMethodData Ω Ω')
    (hDeriv : HasDerivAt D.g D.gDeriv D.theta)
    (hNorm :
      letI : IsProbabilityMeasure D.P := D.isProbabilityP
      letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
      TendstoInDistribution (normalizedInputStatistic D) atTop D.Z (fun _ : ℕ => D.P) D.P')
    (hTaylor : TaylorRemainderPackage D) :
    DeltaMethodConclusion D :=
  deltaMethod_bridge D
    (deltaMethodBridgeAssumptions_of_taylorPackage D hDeriv hNorm hTaylor)

/-- Pinned mathlib revision used for the Stage1 anchor audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.Probability.CentralLimitTheorem",
  "Mathlib.Analysis.Calculus.Deriv.Basic"
]

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.TendstoInDistribution",
  "MeasureTheory.TendstoInDistribution.continuous_comp",
  "MeasureTheory.tendstoInDistribution_of_tendstoInMeasure_sub",
  "MeasureTheory.TendstoInMeasure",
  "MeasureTheory.tendstoInMeasure_iff_measureReal_norm",
  "HasDerivAt.continuousAt",
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IdentDistrib"
]

/-- Source-file locations for the core audited mathlib anchors. -/
def mathlibAnchorSourceFiles : List (String × String) := [
  ("MeasureTheory.TendstoInDistribution.continuous_comp",
    "Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean"),
  ("MeasureTheory.tendstoInDistribution_of_tendstoInMeasure_sub",
    "Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean"),
  ("MeasureTheory.TendstoInMeasure",
    "Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean"),
  ("HasDerivAt.continuousAt",
    "Mathlib/Analysis/Calculus/Deriv/Basic.lean")
]

/-- Search terms that did not resolve to a terminal Delta-method theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Delta method",
  "delta method",
  "TendstoInDistribution HasDerivAt",
  "continuous mapping theorem Taylor remainder",
  "asymptotic distribution differentiable transform"
]

/-! ## External proof audit gate -/

/--
Date of the retained external Lean 4 terminal-proof audit for the child gate.
-/
def externalDeltaMethodProofAuditDate : String :=
  "2026-05-01"

/--
Primary-source query families used when checking for an external Lean 4
terminal Delta-method proof.
-/
def externalDeltaMethodProofSearchQueries : List String := [
  "\"Delta method\" \"TendstoInDistribution\" language:Lean",
  "\"delta method\" language:Lean",
  "\"TendstoInDistribution\" \"HasDerivAt\" language:Lean",
  "\"tendstoInDistribution_of_tendstoInMeasure_sub\" language:Lean",
  "\"DeltaMethod\" language:Lean",
  "\"delta_method\" language:Lean"
]

/--
External-proof audit conclusion retained in the checked file.

This is metadata, not theorem evidence: no external Lean 4 terminal Delta-method
proof was found in this pass, so there is no anchor-only external proof to
promote to completion and no completed state carrying repo-local integration
debt.
-/
def externalDeltaMethodProofAuditConclusion : String :=
  "no_external_lean4_terminal_delta_method_proof_found"

/-- Search-tool limitations that keep the audit from being a completion claim. -/
def externalDeltaMethodProofAuditLimitations : List String := [
  "local pinned mathlib source search found no terminal Delta-method theorem",
  "GitHub CLI code search required authentication in this environment",
  "GitHub REST code search was rate-limited for unauthenticated requests",
  "unauthenticated GitHub web code search required sign-in for full code search"
]

/-! ## Public target scope decision -/

/--
Public Stage1 target recommended by the child scope audit.

The value is metadata, not a theorem claim: it records that the checked artifact
should remain the one-dimensional real Delta-method bridge until the broader
normed-space API has been audited.
-/
def publicTargetScopeDecision : String :=
  "one_dimensional_real_delta_method_first"

/-- API branches that must be checked before promoting a Frechet generalization. -/
def frechetGeneralizationAuditNeeds : List String := [
  "vector-valued TendstoInDistribution target and continuous mapping API",
  "ContinuousLinearMap/HasFDerivAt statement normalization",
  "bounded-in-probability or tightness in normed spaces",
  "normed Taylor-remainder quotient/product-to-zero package",
  "measurability of normed-space transforms and remainders"
]

/-! ## Audit probes retained in the checked file. -/

#check MeasureTheory.TendstoInDistribution
#check MeasureTheory.TendstoInDistribution.continuous_comp
#check MeasureTheory.tendstoInDistribution_of_tendstoInMeasure_sub
#check MeasureTheory.TendstoInMeasure
#check HasDerivAt.continuousAt
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.IdentDistrib
#check StatementShape
#check BridgeStatementShape
#check bridgeStatementShape_mathlib
#check TaylorRemainderPackage
#check taylorProductRemainder_eq_delta_sub_linearized
#check deltaMethod_of_taylorPackage
#check mathlibAnchorRevision
#check mathlibAnchorSourceFiles
#check externalDeltaMethodProofAuditDate
#check externalDeltaMethodProofSearchQueries
#check externalDeltaMethodProofAuditConclusion
#check externalDeltaMethodProofAuditLimitations
#check publicTargetScopeDecision
#check frechetGeneralizationAuditNeeds

end S1_M_295
end Stage1
end AwesomeTheorems
