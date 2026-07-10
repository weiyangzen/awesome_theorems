import Mathlib.Probability.CentralLimitTheorem
import Mathlib.Probability.Moments.Basic
import Mathlib.MeasureTheory.Measure.Portmanteau

/-!
# S1-M-270 / THM-M-0990: Lyapunov central limit theorem

This Stage1 artifact records a conservative Lean 4 boundary for the Lyapunov
central limit theorem for triangular arrays of independent real random
variables.

The pinned mathlib snapshot contains a one-dimensional i.i.d. central limit
theorem, characteristic-function infrastructure, weak convergence in
distribution, Gaussian laws, finite sums, independence, Bochner integration, and
variance/moment APIs.  This file did not locate a terminal Lyapunov or
Lindeberg-Feller triangular-array CLT in mathlib.

Accordingly, the local content is a checked statement shape plus low-risk
wrappers around mathlib anchors.  No terminal proof of the Lyapunov central
limit theorem is claimed here.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped Real Topology

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_270

/-- A real triangular array, encoded as row `n`, column `k`, sample point `ω`. -/
abbrev TriangularArray (Ω : Type u) :=
  ℕ → ℕ → Ω → ℝ

/-- Center the `(n,k)` entry of a triangular array by subtracting its mean. -/
def centeredEntry {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (n k : ℕ) (ω : Ω) : ℝ :=
  X n k ω - ∫ ω, X n k ω ∂P

/-- Sum of row variances for the first `n` entries of row `n`. -/
def rowVarianceSum {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (n : ℕ) : ℝ :=
  ∑ k ∈ Finset.range n, Var[X n k; P]

/--
The standard-deviation scale `s_n` used in the textbook Lyapunov denominator,
with `s_n^2 = rowVarianceSum` once the variance sum is nonnegative.
-/
def rowStandardDeviation {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (n : ℕ) : ℝ :=
  √(rowVarianceSum X P n)

/-- Normalized centered row sum used in the Lyapunov CLT conclusion. -/
def normalizedRowSum {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (n : ℕ) (ω : Ω) : ℝ :=
  (rowStandardDeviation X P n)⁻¹ *
    ∑ k ∈ Finset.range n, centeredEntry X P n k ω

/--
Finite-row independence for the first `n` entries of row `n`.

This is the finite predicate needed by the characteristic-function product
package.  It is deliberately not the public statement field: current mathlib
finite-sum characteristic-function APIs are reached from the stronger row-wise
`iIndepFun (X n) P` hypothesis by `iIndepFun.restrict`.
-/
def finiteRowIndependence {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (n : ℕ) : Prop :=
  ProbabilityTheory.iIndepFun ((Finset.range n).restrict (X n)) P

/--
The Lyapunov fraction for row `n` and exponent offset `δ`.

The denominator is written using the standard-deviation scale
`sqrt(rowVarianceSum) ^ (2 + δ)`.  Positivity/nonzero side conditions are kept
as named hypotheses in `LyapunovData`.
-/
def lyapunovTextbookDenominator {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (δ : ℝ) (n : ℕ) : ℝ :=
  Real.rpow (rowStandardDeviation X P n) (2 + δ)

/-- The Lyapunov fraction for row `n` and exponent offset `δ`. -/
def lyapunovFraction {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (δ : ℝ) (n : ℕ) : ℝ :=
  (lyapunovTextbookDenominator X P δ n)⁻¹ *
    ∑ k ∈ Finset.range n,
      ∫ ω, Real.rpow |centeredEntry X P n k ω| (2 + δ) ∂P

/--
Normalized data for the Lyapunov central limit theorem.

The checked fields use current mathlib objects.  The triangular-array
characteristic-function/Taylor remainder bridge is left as a proposition field,
because the pinned dependency closure does not expose a terminal Lyapunov CLT.

The public independence field stays at full row independence
`iIndepFun (X n) P`.  The finite first-`n` row predicate is a derived bridge
recorded by `finiteRowIndependence_of_data`; this matches the mathlib route
used by characteristic-function finite-sum lemmas.
-/
structure LyapunovData (Ω : Type u) [MeasurableSpace Ω] where
  P : Measure Ω
  X : TriangularArray Ω
  delta : ℝ
  delta_pos : 0 < delta
  isProbability : IsProbabilityMeasure P
  measurable : ∀ n k : ℕ, Measurable (X n k)
  rowIndependent : ∀ n : ℕ, ProbabilityTheory.iIndepFun (X n) P
  rowVariancePositive : ∀ᶠ n in atTop, 0 < rowVarianceSum X P n
  finiteSecondMoment : ∀ n k : ℕ, MemLp (X n k) 2 P
  finiteLyapunovMoment :
    ∀ n k : ℕ, Integrable (fun ω => Real.rpow |centeredEntry X P n k ω| (2 + delta)) P
  lyapunovCondition :
    Tendsto (fun n : ℕ => lyapunovFraction X P delta n) atTop (𝓝 0)
  characteristicFunctionTaylorBridge : Prop

/-- The standard Gaussian target package for the normalized row sums. -/
structure GaussianTarget (Ω' : Type v) [MeasurableSpace Ω'] where
  P' : Measure Ω'
  Y : Ω' → ℝ
  isProbability : IsProbabilityMeasure P'
  hasLaw_standardGaussian : ProbabilityTheory.HasLaw Y (ProbabilityTheory.gaussianReal 0 1) P'

/-- Hypotheses that remain as named bridge packages in this Stage1 boundary. -/
def LyapunovHypotheses {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) : Prop :=
  D.characteristicFunctionTaylorBridge

/-- Conclusion expected from a completed Lyapunov CLT formalization. -/
def LyapunovConclusion {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω'] (D : LyapunovData Ω)
    (G : GaussianTarget Ω') : Prop :=
  letI : IsProbabilityMeasure D.P := D.isProbability
  letI : IsProbabilityMeasure G.P' := G.isProbability
  TendstoInDistribution
    (fun n : ℕ => normalizedRowSum D.X D.P n) atTop G.Y (fun _ => D.P) G.P'

/--
Stage1 normalized statement shape for the Lyapunov central limit theorem.

For every probability space, triangular array, positive Lyapunov exponent
offset, independent row data, finite moments, positive asymptotic variance, and
Lyapunov fraction tending to zero, the normalized centered row sums converge in
distribution to a standard Gaussian variable.

This declaration is a formalization boundary only.  The repo-local Lean closure
does not contain the triangular-array proof body.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : LyapunovData Ω,
      LyapunovHypotheses D →
        ∀ (Ω' : Type v) [MeasurableSpace Ω'],
          ∀ G : GaussianTarget Ω',
            LyapunovConclusion D G

/--
Checked Stage1 boundary-audit row for the public `StatementShape` note.

This metadata is intentionally weaker than a theorem proof: it records that the
repo-local artifact validates the statement boundary named by
`validatedDeclaration`, while `terminalProofCompletionClaim = false` keeps the
Lyapunov CLT itself open.
-/
structure StatementShapeBoundaryAudit where
  artifactPath : String
  validatedDeclaration : String
  boundaryKind : String
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note carried by the checked Lean artifact. -/
def statementShapeBoundaryAudit : StatementShapeBoundaryAudit where
  artifactPath := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_270.lean"
  validatedDeclaration := "AwesomeTheorems.Stage1.S1_M_270.StatementShape"
  boundaryKind := "Lyapunov CLT statement boundary; not terminal proof completion"
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The checked boundary-audit row does not claim a terminal Lyapunov CLT proof. -/
theorem statementShapeBoundaryAudit_no_terminal_completion :
    statementShapeBoundaryAudit.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for this statement-shape child: no completed state is claimed, and
therefore no completed state retains repo-local integration debt.
-/
theorem statementShapeBoundaryAudit_no_completed_integration_debt :
    statementShapeBoundaryAudit.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/--
Checked Stage1 audit row for the pinned mathlib CLT anchor.

The Boolean fields record the human audit boundary: the checked dependency
contains the i.i.d. wrapper named by `anchorDeclaration`, while this pass did
not locate a terminal Lyapunov or Lindeberg triangular-array CLT in the pinned
mathlib revision.
-/
structure MathlibAnchorAudit where
  pinnedMathlibRevision : String
  importModule : String
  anchorDeclaration : String
  anchorKind : String
  lyapunovTriangularArrayDeclarationLocated : Bool
  lindebergTriangularArrayDeclarationLocated : Bool
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note for the mathlib i.i.d. CLT anchor. -/
def mathlibAnchorAudit : MathlibAnchorAudit where
  pinnedMathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  importModule := "Mathlib.Probability.CentralLimitTheorem"
  anchorDeclaration := "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub"
  anchorKind := "one-dimensional i.i.d. CLT wrapper anchor; not Lyapunov/Lindeberg triangular-array CLT"
  lyapunovTriangularArrayDeclarationLocated := false
  lindebergTriangularArrayDeclarationLocated := false
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The pinned mathlib anchor recorded for this child is the i.i.d. CLT wrapper. -/
theorem mathlibAnchorAudit_anchorDeclaration :
    mathlibAnchorAudit.anchorDeclaration =
      "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub" :=
  rfl

/-- The local audit did not locate a Lyapunov triangular-array CLT in mathlib. -/
theorem mathlibAnchorAudit_no_located_lyapunov_triangular_array :
    mathlibAnchorAudit.lyapunovTriangularArrayDeclarationLocated = false :=
  rfl

/-- The local audit did not locate a Lindeberg triangular-array CLT in mathlib. -/
theorem mathlibAnchorAudit_no_located_lindeberg_triangular_array :
    mathlibAnchorAudit.lindebergTriangularArrayDeclarationLocated = false :=
  rfl

/-- The mathlib anchor audit does not claim terminal Lyapunov CLT completion. -/
theorem mathlibAnchorAudit_no_terminal_completion :
    mathlibAnchorAudit.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for this mathlib-anchor child: no completed state is claimed, so no
completed state retains repo-local integration debt.
-/
theorem mathlibAnchorAudit_no_completed_integration_debt :
    mathlibAnchorAudit.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/--
Checked Stage1 audit row for the external primary-source repository
`uw-math-ai/central_limit_theorem`.

The pinned source is adjacent to this slot because it targets a central limit
theorem, but it is not a Lyapunov triangular-array CLT integration target:
the audited revision contains `sorry` and no terminal Lyapunov declaration was
located there.
-/
structure ExternalPrimarySourceAudit where
  repository : String
  pinnedRevision : String
  sourceKind : String
  auditedFiles : List String
  visibleTheoremName : String
  adjacentKind : String
  containsSorry : Bool
  terminalLyapunovDeclarationLocated : Bool
  integrationTargetForCompletion : Bool
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note for the adjacent external CLT repository audit. -/
def externalPrimarySourceAudit : ExternalPrimarySourceAudit where
  repository := "https://github.com/uw-math-ai/central_limit_theorem"
  pinnedRevision := "0ed57e943d642eaa95fe547780024b9e3a0dfbdf"
  sourceKind := "external Lean 4 primary-source audit"
  auditedFiles := [
    "CentralLimitTheorem/main.lean",
    "CentralLimitTheorem/main_theorem.lean",
    "CentralLimitTheorem/mgf_of_sum.lean",
    "CentralLimitTheorem.lean",
    "lakefile.lean",
    "lean-toolchain"
  ]
  visibleTheoremName := "CLT"
  adjacentKind := "i.i.d. central limit theorem adjacent source; not Lyapunov triangular-array CLT"
  containsSorry := true
  terminalLyapunovDeclarationLocated := false
  integrationTargetForCompletion := false
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The external audit is pinned to the requested repository revision. -/
theorem externalPrimarySourceAudit_pinnedRevision :
    externalPrimarySourceAudit.pinnedRevision =
      "0ed57e943d642eaa95fe547780024b9e3a0dfbdf" :=
  rfl

/-- The adjacent external source contains `sorry`, so it is not proof closure. -/
theorem externalPrimarySourceAudit_containsSorry :
    externalPrimarySourceAudit.containsSorry = true :=
  rfl

/-- The adjacent external source did not locate a terminal Lyapunov CLT theorem. -/
theorem externalPrimarySourceAudit_no_terminal_lyapunov :
    externalPrimarySourceAudit.terminalLyapunovDeclarationLocated = false :=
  rfl

/-- The adjacent external source is not an integration target for completion. -/
theorem externalPrimarySourceAudit_not_integration_target :
    externalPrimarySourceAudit.integrationTargetForCompletion = false :=
  rfl

/-- The external audit does not claim terminal Lyapunov CLT completion. -/
theorem externalPrimarySourceAudit_no_terminal_completion :
    externalPrimarySourceAudit.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for this external-audit child: the adjacent source is recorded only
as non-completing evidence, so no completed state retains repo-local
integration debt.
-/
theorem externalPrimarySourceAudit_no_completed_integration_debt :
    externalPrimarySourceAudit.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω],
      ∀ D : LyapunovData Ω,
        LyapunovHypotheses D →
          ∀ (Ω' : Type v) [MeasurableSpace Ω'],
            ∀ G : GaussianTarget Ω',
              LyapunovConclusion D G) :
    StatementShape.{u, v} :=
  h

/-- The statement shape unfolds to the expected data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : LyapunovData Ω,
          LyapunovHypotheses D →
            ∀ (Ω' : Type v) [MeasurableSpace Ω'],
              ∀ G : GaussianTarget Ω',
                LyapunovConclusion D G :=
  Iff.rfl

/-- Project the row-wise independence predicate from the normalized data. -/
theorem rowIndependent_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) (n : ℕ) :
    ProbabilityTheory.iIndepFun (D.X n) D.P :=
  D.rowIndependent n

/--
The finite-row independence package needed for row `n` is obtained by
restricting the public full-row `iIndepFun` hypothesis to `Finset.range n`.
-/
theorem finiteRowIndependence_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) (n : ℕ) :
    finiteRowIndependence D.X D.P n :=
  (D.rowIndependent n).restrict (Finset.range n)

/-- Project measurability of a triangular-array entry. -/
theorem measurable_entry {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) (n k : ℕ) :
    Measurable (D.X n k) :=
  D.measurable n k

/-- Project the finite second-moment field. -/
theorem finiteSecondMoment_entry {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) (n k : ℕ) :
    MemLp (D.X n k) 2 D.P :=
  D.finiteSecondMoment n k

/-- Project the Lyapunov moment-integrability field. -/
theorem finiteLyapunovMoment_entry {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) (n k : ℕ) :
    Integrable (fun ω => Real.rpow |centeredEntry D.X D.P n k ω| (2 + D.delta)) D.P :=
  D.finiteLyapunovMoment n k

/-! ## Lyapunov denominator bridges for child `S1-M-270-C005`. -/

/--
If the variance sum is positive, the textbook scale
`s_n = sqrt(rowVarianceSum)` is positive.
-/
theorem rowStandardDeviation_pos_of_rowVarianceSum_pos {Ω : Type u}
    [MeasurableSpace Ω] {X : TriangularArray Ω} {P : Measure Ω} {n : ℕ}
    (h : 0 < rowVarianceSum X P n) :
    0 < rowStandardDeviation X P n := by
  simpa [rowStandardDeviation] using Real.sqrt_pos_of_pos h

/--
If the variance sum is positive, the textbook scale
`s_n = sqrt(rowVarianceSum)` is nonzero.
-/
theorem rowStandardDeviation_ne_zero_of_rowVarianceSum_pos {Ω : Type u}
    [MeasurableSpace Ω] {X : TriangularArray Ω} {P : Measure Ω} {n : ℕ}
    (h : 0 < rowVarianceSum X P n) :
    rowStandardDeviation X P n ≠ 0 :=
  (rowStandardDeviation_pos_of_rowVarianceSum_pos h).ne'

/-- The defining square bridge for `s_n`: if the variance sum is nonnegative, then `s_n^2` is it. -/
theorem rowStandardDeviation_sq_of_rowVarianceSum_nonneg {Ω : Type u}
    [MeasurableSpace Ω] {X : TriangularArray Ω} {P : Measure Ω} {n : ℕ}
    (h : 0 ≤ rowVarianceSum X P n) :
    rowStandardDeviation X P n ^ 2 = rowVarianceSum X P n := by
  simpa [rowStandardDeviation] using Real.sq_sqrt h

/-- Positive variance sums give the textbook bridge `s_n^2 = rowVarianceSum`. -/
theorem rowStandardDeviation_sq_of_rowVarianceSum_pos {Ω : Type u}
    [MeasurableSpace Ω] {X : TriangularArray Ω} {P : Measure Ω} {n : ℕ}
    (h : 0 < rowVarianceSum X P n) :
    rowStandardDeviation X P n ^ 2 = rowVarianceSum X P n :=
  rowStandardDeviation_sq_of_rowVarianceSum_nonneg h.le

/-- The eventual variance-positivity field gives eventual positivity of `s_n`. -/
theorem rowStandardDeviation_eventually_pos {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) :
    ∀ᶠ n in atTop, 0 < rowStandardDeviation D.X D.P n :=
  D.rowVariancePositive.mono fun _ hn =>
    rowStandardDeviation_pos_of_rowVarianceSum_pos hn

/-- The eventual variance-positivity field gives eventual nonzero `s_n`. -/
theorem rowStandardDeviation_eventually_ne_zero {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) :
    ∀ᶠ n in atTop, rowStandardDeviation D.X D.P n ≠ 0 :=
  D.rowVariancePositive.mono fun _ hn =>
    rowStandardDeviation_ne_zero_of_rowVarianceSum_pos hn

/--
The denominator in `lyapunovFraction` is exactly the textbook `s_n^(2 + δ)`
after naming `s_n = rowStandardDeviation`.
-/
theorem lyapunovFraction_uses_textbook_denominator {Ω : Type u} [MeasurableSpace Ω]
    (X : TriangularArray Ω) (P : Measure Ω) (δ : ℝ) (n : ℕ) :
    lyapunovFraction X P δ n =
      (lyapunovTextbookDenominator X P δ n)⁻¹ *
        ∑ k ∈ Finset.range n,
          ∫ ω, Real.rpow |centeredEntry X P n k ω| (2 + δ) ∂P :=
  rfl

/-- Positive variance sum makes the textbook denominator positive for every real exponent. -/
theorem lyapunovTextbookDenominator_pos_of_rowVarianceSum_pos {Ω : Type u}
    [MeasurableSpace Ω] {X : TriangularArray Ω} {P : Measure Ω} {δ : ℝ} {n : ℕ}
    (h : 0 < rowVarianceSum X P n) :
    0 < lyapunovTextbookDenominator X P δ n :=
  Real.rpow_pos_of_pos (rowStandardDeviation_pos_of_rowVarianceSum_pos h) (2 + δ)

/-- Positive variance sum makes the textbook denominator nonzero. -/
theorem lyapunovTextbookDenominator_ne_zero_of_rowVarianceSum_pos {Ω : Type u}
    [MeasurableSpace Ω] {X : TriangularArray Ω} {P : Measure Ω} {δ : ℝ} {n : ℕ}
    (h : 0 < rowVarianceSum X P n) :
    lyapunovTextbookDenominator X P δ n ≠ 0 :=
  (lyapunovTextbookDenominator_pos_of_rowVarianceSum_pos h).ne'

/--
Checked audit row for the Lyapunov denominator convention.

The local statement uses `s_n = sqrt(rowVarianceSum)` and the denominator
`s_n^(2 + δ)`.  The bridge lemmas above expose positivity, nonzero, and
`s_n^2 = rowVarianceSum` facts needed before characteristic-function proof work.
-/
structure LyapunovDenominatorAudit where
  childTaskId : String
  standardDeviationDeclaration : String
  denominatorDeclaration : String
  textbookConvention : String
  squareBridgeDeclaration : String
  positivityBridgeDeclaration : String
  nonzeroBridgeDeclaration : String
  denominatorPositiveBridgeDeclaration : String
  denominatorNonzeroBridgeDeclaration : String
  matchesTextbookConvention : Bool
  proofTreeBridgeLeaf : String
  proofTreeBridgeLeafChecked : Bool
  characteristicFunctionPackageStillOpen : Bool
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note for `THM-M-0990.lyapunov-denominator`. -/
def lyapunovDenominatorAudit : LyapunovDenominatorAudit where
  childTaskId := "S1-M-270-C005"
  standardDeviationDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.rowStandardDeviation"
  denominatorDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.lyapunovTextbookDenominator"
  textbookConvention := "s_n^(2 + δ), where s_n^2 = rowVarianceSum"
  squareBridgeDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.rowStandardDeviation_sq_of_rowVarianceSum_pos"
  positivityBridgeDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.rowStandardDeviation_pos_of_rowVarianceSum_pos"
  nonzeroBridgeDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.rowStandardDeviation_ne_zero_of_rowVarianceSum_pos"
  denominatorPositiveBridgeDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.lyapunovTextbookDenominator_pos_of_rowVarianceSum_pos"
  denominatorNonzeroBridgeDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.lyapunovTextbookDenominator_ne_zero_of_rowVarianceSum_pos"
  matchesTextbookConvention := true
  proofTreeBridgeLeaf := "M0990-L021"
  proofTreeBridgeLeafChecked := true
  characteristicFunctionPackageStillOpen := true
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The denominator audit records the textbook convention `s_n^(2 + δ)`. -/
theorem lyapunovDenominatorAudit_matches_textbook :
    lyapunovDenominatorAudit.matchesTextbookConvention = true :=
  rfl

/-- The denominator bridge leaf is locally checked by named Lean declarations. -/
theorem lyapunovDenominatorAudit_leaf_checked :
    lyapunovDenominatorAudit.proofTreeBridgeLeafChecked = true :=
  rfl

/-- The denominator audit does not claim terminal Lyapunov CLT completion. -/
theorem lyapunovDenominatorAudit_no_terminal_completion :
    lyapunovDenominatorAudit.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for the denominator child: the denominator bridge is locally checked,
but no completed Lyapunov CLT state is claimed, so no completed state retains
repo-local integration debt.
-/
theorem lyapunovDenominatorAudit_no_completed_integration_debt :
    lyapunovDenominatorAudit.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/-- Project the Lyapunov fraction convergence field. -/
theorem lyapunovCondition_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : LyapunovData Ω) :
    Tendsto (fun n : ℕ => lyapunovFraction D.X D.P D.delta n) atTop (𝓝 0) :=
  D.lyapunovCondition

/-- Project the standard-Gaussian law from a target package. -/
theorem GaussianTarget.hasLaw {Ω' : Type v} [MeasurableSpace Ω']
    (G : GaussianTarget Ω') :
    ProbabilityTheory.HasLaw G.Y (ProbabilityTheory.gaussianReal 0 1) G.P' :=
  G.hasLaw_standardGaussian

/--
Checked mathlib anchor: the pinned mathlib dependency proves the one-dimensional
i.i.d. central limit theorem.  This is adjacent substrate, not the Lyapunov
triangular-array theorem.
-/
theorem iid_clt_mathlib_anchor {Ω Ω' : Type u} [MeasurableSpace Ω] [MeasurableSpace Ω']
    {P : Measure Ω} {P' : Measure Ω'} [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    {X : ℕ → Ω → ℝ} {Y : Ω' → ℝ}
    (hY : ProbabilityTheory.HasLaw Y (ProbabilityTheory.gaussianReal 0 Var[X 0; P].toNNReal) P')
    (hX : MemLp (X 0) 2 P)
    (hindep : ProbabilityTheory.iIndepFun X P)
    (hident : ∀ i : ℕ, ProbabilityTheory.IdentDistrib (X i) (X 0) P P) :
    TendstoInDistribution
      (fun n : ℕ => fun ω => (√n)⁻¹ * (∑ k ∈ Finset.range n, X k ω - n * P[X 0]))
      atTop Y (fun _ => P) P' :=
  ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub hY hX hindep hident

/-! ## Independence API decision for child `S1-M-270-C004`. -/

/--
Checked audit row for the public independence API decision.

The statement boundary keeps full row-wise independence as the canonical public
hypothesis.  A finite-row predicate is retained only as a derived proof package
interface, because it is obtained locally from `iIndepFun.restrict` and feeds
mathlib's finite characteristic-function product lemmas.
-/
structure IndependenceAPIDecision where
  childTaskId : String
  publicStatementPredicate : String
  finiteRowPredicate : String
  keepFullRowIndependence : Bool
  replaceStatementWithFiniteRowPredicate : Bool
  finiteRowPredicateDerivedLocally : Bool
  checkedBridgeDeclaration : String
  proofTreeDecisionLeaf : String
  proofTreeDecisionLeafChecked : Bool
  characteristicFunctionPackageStillOpen : Bool
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note for `THM-M-0990.independence-api`. -/
def independenceAPIDecision : IndependenceAPIDecision where
  childTaskId := "S1-M-270-C004"
  publicStatementPredicate := "∀ n : ℕ, ProbabilityTheory.iIndepFun (X n) P"
  finiteRowPredicate := "finiteRowIndependence X P n"
  keepFullRowIndependence := true
  replaceStatementWithFiniteRowPredicate := false
  finiteRowPredicateDerivedLocally := true
  checkedBridgeDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.finiteRowIndependence_of_data"
  proofTreeDecisionLeaf := "M0990-L022"
  proofTreeDecisionLeafChecked := true
  characteristicFunctionPackageStillOpen := true
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The public statement keeps full row-wise `iIndepFun`. -/
theorem independenceAPIDecision_keeps_full_row :
    independenceAPIDecision.keepFullRowIndependence = true :=
  rfl

/-- The public statement is not replaced by a finite-row-only predicate. -/
theorem independenceAPIDecision_no_statement_replacement :
    independenceAPIDecision.replaceStatementWithFiniteRowPredicate = false :=
  rfl

/-- The finite-row predicate is a locally checked derived bridge. -/
theorem independenceAPIDecision_finite_row_derived :
    independenceAPIDecision.finiteRowPredicateDerivedLocally = true :=
  rfl

/-- The API-decision leaf is closed by this checked audit row. -/
theorem independenceAPIDecision_leaf_checked :
    independenceAPIDecision.proofTreeDecisionLeafChecked = true :=
  rfl

/-- Characteristic-function factorization remains a separate open package. -/
theorem independenceAPIDecision_characteristic_function_package_open :
    independenceAPIDecision.characteristicFunctionPackageStillOpen = true :=
  rfl

/-- The independence API decision does not claim terminal Lyapunov CLT completion. -/
theorem independenceAPIDecision_no_terminal_completion :
    independenceAPIDecision.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for the independence-api child: the API decision is locally checked,
but no completed Lyapunov CLT state is claimed, so no completed state retains
repo-local integration debt.
-/
theorem independenceAPIDecision_no_completed_integration_debt :
    independenceAPIDecision.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Characteristic-function package public backfill for child `S1-M-270-C006`. -/

/--
Checked audit row for the public child-task split of the characteristic-function
package.

This is a backfill package, not a proof of the Lyapunov characteristic-function
argument.  It records that leaves `M0990-L020` through `M0990-L030` have stable
public task names and individual `<=100` proof-step budgets for later workers.
-/
structure CharacteristicFunctionPackageBackfill where
  childTaskId : String
  parentTask : String
  packageId : String
  firstLeaf : String
  lastLeaf : String
  publicLeafIds : List String
  localProofStepBudgetPerLeaf : Nat
  publicBackfillPrepared : Bool
  localProofLeavesClosed : Bool
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note for `THM-M-0990.characteristic-function-package`. -/
def characteristicFunctionPackageBackfill : CharacteristicFunctionPackageBackfill where
  childTaskId := "S1-M-270-C006"
  parentTask := "THM-M-0990.characteristic-function-package"
  packageId := "M0990.P2-P5.characteristic_function_package"
  firstLeaf := "M0990-L020"
  lastLeaf := "M0990-L030"
  publicLeafIds := [
    "M0990-L020",
    "M0990-L021",
    "M0990-L022",
    "M0990-L023",
    "M0990-L024",
    "M0990-L025",
    "M0990-L026",
    "M0990-L027",
    "M0990-L028",
    "M0990-L029",
    "M0990-L030"
  ]
  localProofStepBudgetPerLeaf := 100
  publicBackfillPrepared := true
  localProofLeavesClosed := false
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The characteristic-function package backfill starts at `M0990-L020`. -/
theorem characteristicFunctionPackageBackfill_firstLeaf :
    characteristicFunctionPackageBackfill.firstLeaf = "M0990-L020" :=
  rfl

/-- The characteristic-function package backfill ends at `M0990-L030`. -/
theorem characteristicFunctionPackageBackfill_lastLeaf :
    characteristicFunctionPackageBackfill.lastLeaf = "M0990-L030" :=
  rfl

/-- Each public child leaf in this package keeps the M0387 `<=100` step budget. -/
theorem characteristicFunctionPackageBackfill_budget :
    characteristicFunctionPackageBackfill.localProofStepBudgetPerLeaf = 100 :=
  rfl

/-- The C006 package prepares public backfill only; it does not close proof leaves. -/
theorem characteristicFunctionPackageBackfill_proofs_open :
    characteristicFunctionPackageBackfill.localProofLeavesClosed = false :=
  rfl

/-- The characteristic-function package backfill does not claim terminal Lyapunov CLT completion. -/
theorem characteristicFunctionPackageBackfill_no_terminal_completion :
    characteristicFunctionPackageBackfill.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for the characteristic-function public-backfill child: no terminal
completion state is claimed, so no completed state retains repo-local
integration debt.
-/
theorem characteristicFunctionPackageBackfill_no_completed_integration_debt :
    characteristicFunctionPackageBackfill.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Integration gate for child `S1-M-270-C007`. -/

/--
Checked Stage1 integration gate for the Lyapunov CLT slot.

This row is deliberately negative evidence: it records the exact closure routes
that have not yet been achieved locally.  The parent item must remain open until
one of these routes is changed to a locally validated proof closure.
-/
structure IntegrationGateAudit where
  childTaskId : String
  parentTask : String
  terminalStatementDeclaration : String
  currentMachineState : String
  localProofBodyValidated : Bool
  exactMathlibLyapunovWrapperValidated : Bool
  pinnedExternalProofClosureValidated : Bool
  externalAnchorOnlyCompletionClaim : Bool
  repoLocalValidationCommand : String
  keepStage1ItemOpen : Bool
  activeDebtClass : String
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note for `THM-M-0990.integration-gate`. -/
def integrationGateAudit : IntegrationGateAudit where
  childTaskId := "S1-M-270-C007"
  parentTask := "THM-M-0990.integration-gate"
  terminalStatementDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_270.StatementShape"
  currentMachineState := "not_repo_local_closed"
  localProofBodyValidated := false
  exactMathlibLyapunovWrapperValidated := false
  pinnedExternalProofClosureValidated := false
  externalAnchorOnlyCompletionClaim := false
  repoLocalValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_270.lean"
  keepStage1ItemOpen := true
  activeDebtClass := "formalization_debt"
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The C007 gate keeps the Stage1 Lyapunov CLT item open. -/
theorem integrationGateAudit_keeps_item_open :
    integrationGateAudit.keepStage1ItemOpen = true :=
  rfl

/-- No local proof body has been validated for the terminal Lyapunov CLT. -/
theorem integrationGateAudit_no_local_proof_body :
    integrationGateAudit.localProofBodyValidated = false :=
  rfl

/-- No exact mathlib wrapper for a Lyapunov triangular-array CLT has been validated. -/
theorem integrationGateAudit_no_exact_mathlib_wrapper :
    integrationGateAudit.exactMathlibLyapunovWrapperValidated = false :=
  rfl

/-- No pinned external proof closure has been validated in this repository. -/
theorem integrationGateAudit_no_pinned_external_closure :
    integrationGateAudit.pinnedExternalProofClosureValidated = false :=
  rfl

/-- The C007 gate does not allow anchor-only evidence to count as completion. -/
theorem integrationGateAudit_no_anchor_only_completion :
    integrationGateAudit.externalAnchorOnlyCompletionClaim = false :=
  rfl

/-- The active terminal-theorem debt remains formalization debt, not integration closure. -/
theorem integrationGateAudit_active_debt :
    integrationGateAudit.activeDebtClass = "formalization_debt" :=
  rfl

/-- The C007 gate does not claim terminal Lyapunov CLT completion. -/
theorem integrationGateAudit_no_terminal_completion :
    integrationGateAudit.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 integration gate: the current state is open, and no completed state
retains repo-local integration debt.
-/
theorem integrationGateAudit_no_completed_integration_debt :
    integrationGateAudit.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.charFun_inv_sqrt_mul_sum
#check ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow
#check MeasureTheory.TendstoInDistribution
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.restrict
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.gaussianReal
#check charFun
#check ProbabilityTheory.variance
#check MemLp
#check Integrable
#check rowVarianceSum
#check rowStandardDeviation
#check rowStandardDeviation_pos_of_rowVarianceSum_pos
#check rowStandardDeviation_ne_zero_of_rowVarianceSum_pos
#check rowStandardDeviation_sq_of_rowVarianceSum_nonneg
#check rowStandardDeviation_sq_of_rowVarianceSum_pos
#check rowStandardDeviation_eventually_pos
#check rowStandardDeviation_eventually_ne_zero
#check finiteRowIndependence
#check finiteRowIndependence_of_data
#check lyapunovTextbookDenominator
#check lyapunovFraction_uses_textbook_denominator
#check lyapunovTextbookDenominator_pos_of_rowVarianceSum_pos
#check lyapunovTextbookDenominator_ne_zero_of_rowVarianceSum_pos
#check lyapunovFraction
#check StatementShape
#check statementShapeBoundaryAudit
#check statementShapeBoundaryAudit_no_terminal_completion
#check statementShapeBoundaryAudit_no_completed_integration_debt
#check mathlibAnchorAudit
#check mathlibAnchorAudit_anchorDeclaration
#check mathlibAnchorAudit_no_located_lyapunov_triangular_array
#check mathlibAnchorAudit_no_located_lindeberg_triangular_array
#check mathlibAnchorAudit_no_terminal_completion
#check mathlibAnchorAudit_no_completed_integration_debt
#check externalPrimarySourceAudit
#check externalPrimarySourceAudit_pinnedRevision
#check externalPrimarySourceAudit_containsSorry
#check externalPrimarySourceAudit_no_terminal_lyapunov
#check externalPrimarySourceAudit_not_integration_target
#check externalPrimarySourceAudit_no_terminal_completion
#check externalPrimarySourceAudit_no_completed_integration_debt
#check independenceAPIDecision
#check independenceAPIDecision_keeps_full_row
#check independenceAPIDecision_no_statement_replacement
#check independenceAPIDecision_finite_row_derived
#check independenceAPIDecision_leaf_checked
#check independenceAPIDecision_characteristic_function_package_open
#check independenceAPIDecision_no_terminal_completion
#check independenceAPIDecision_no_completed_integration_debt
#check characteristicFunctionPackageBackfill
#check characteristicFunctionPackageBackfill_firstLeaf
#check characteristicFunctionPackageBackfill_lastLeaf
#check characteristicFunctionPackageBackfill_budget
#check characteristicFunctionPackageBackfill_proofs_open
#check characteristicFunctionPackageBackfill_no_terminal_completion
#check characteristicFunctionPackageBackfill_no_completed_integration_debt
#check integrationGateAudit
#check integrationGateAudit_keeps_item_open
#check integrationGateAudit_no_local_proof_body
#check integrationGateAudit_no_exact_mathlib_wrapper
#check integrationGateAudit_no_pinned_external_closure
#check integrationGateAudit_no_anchor_only_completion
#check integrationGateAudit_active_debt
#check integrationGateAudit_no_terminal_completion
#check integrationGateAudit_no_completed_integration_debt
#check lyapunovDenominatorAudit
#check lyapunovDenominatorAudit_matches_textbook
#check lyapunovDenominatorAudit_leaf_checked
#check lyapunovDenominatorAudit_no_terminal_completion
#check lyapunovDenominatorAudit_no_completed_integration_debt

/-- mathlib modules checked while locating repo-local Lyapunov CLT anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.CentralLimitTheorem",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.MeasureTheory.Measure.CharacteristicFunction",
  "Mathlib.MeasureTheory.Measure.CharacteristicFunction.TaylorExpansion",
  "Mathlib.Probability.Independence.CharacteristicFunction",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.MeasureTheory.Measure.Portmanteau"
]

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum",
  "ProbabilityTheory.charFun_inv_sqrt_mul_sum",
  "ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow",
  "MeasureTheory.TendstoInDistribution",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.restrict",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.gaussianReal",
  "ProbabilityTheory.charFun",
  "ProbabilityTheory.Var",
  "MeasureTheory.MemLp",
  "MeasureTheory.Integrable"
]

/-- Search terms that did not locate a terminal Lyapunov CLT in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Lyapunov",
  "Lindeberg",
  "Feller",
  "triangular array",
  "TriangularArray",
  "CentralLimit",
  "CLT"
]

/-- External primary-source files audited for the C003 child pass. -/
def externalPrimarySourceAuditFiles : List String := [
  "https://github.com/uw-math-ai/central_limit_theorem/blob/0ed57e943d642eaa95fe547780024b9e3a0dfbdf/CentralLimitTheorem/main.lean",
  "https://github.com/uw-math-ai/central_limit_theorem/blob/0ed57e943d642eaa95fe547780024b9e3a0dfbdf/CentralLimitTheorem/main_theorem.lean",
  "https://github.com/uw-math-ai/central_limit_theorem/blob/0ed57e943d642eaa95fe547780024b9e3a0dfbdf/CentralLimitTheorem/mgf_of_sum.lean",
  "https://github.com/uw-math-ai/central_limit_theorem/blob/0ed57e943d642eaa95fe547780024b9e3a0dfbdf/CentralLimitTheorem.lean",
  "https://github.com/uw-math-ai/central_limit_theorem/blob/0ed57e943d642eaa95fe547780024b9e3a0dfbdf/lakefile.lean",
  "https://github.com/uw-math-ai/central_limit_theorem/blob/0ed57e943d642eaa95fe547780024b9e3a0dfbdf/lean-toolchain"
]

end S1_M_270
end Stage1
end AwesomeTheorems
