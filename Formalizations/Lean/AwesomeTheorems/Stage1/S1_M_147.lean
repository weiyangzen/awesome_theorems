import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.DerivNotation

/-!
# S1-M-147 / THM-M-1172: `W^{2,p}` regularity

This Stage1 file records a conservative Lean statement-shape boundary for
second-order `L^p` regularity of PDE solutions.

The pinned mathlib snapshot has concrete substrates for `MemLp`, `eLpNorm`,
Fréchet derivatives, vector-valued distributions, and the
Gagliardo-Nirenberg-Sobolev inequality.  It does not contain a terminal
Calderon-Zygmund or elliptic `W^{2,p}` regularity theorem for weak PDE
solutions.

The declarations below therefore avoid proof placeholders and false completion
claims: they normalize the second-derivative `L^p` conclusion and provide
checked wrappers around available mathlib analysis anchors.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal Distributions

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_147

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {F : Type v} [NormedAddCommGroup F] [NormedSpace ℝ F]

/-- The first Fréchet derivative field of a candidate solution. -/
abbrev FirstFDeriv (u : E → F) : E → (E →L[ℝ] F) :=
  fderiv ℝ u

/-- The second Fréchet derivative field of a candidate solution. -/
abbrev SecondFDeriv (u : E → F) : E → (E →L[ℝ] (E →L[ℝ] F)) :=
  fderiv ℝ (FirstFDeriv u)

/-- The second Fréchet derivative abbreviation is definitionally transparent. -/
theorem secondFDeriv_eq_fderiv_first (u : E → F) :
    SecondFDeriv u = fderiv ℝ (FirstFDeriv u) :=
  rfl

variable [MeasurableSpace E]

/-- The normalized local conclusion: the second derivative belongs to `L^p`. -/
def HasSecondDerivativesInLp (μ : Measure E) (p : ℝ≥0∞) (u : E → F) : Prop :=
  MemLp (SecondFDeriv u) p μ

/--
Statement-shape data for a `W^{2,p}` regularity theorem.

The fields deliberately keep the PDE equation and ellipticity hypotheses as
explicit propositions.  A terminal theorem must replace these abstract fields
by concrete weak/classical PDE hypotheses and prove the `MemLp` and estimate
fields from them.
-/
structure W2pRegularityData (μ : Measure E) (u : E → F) : Type (max u v) where
  exponent : ℝ≥0∞
  sourceTerm : E → F
  weakEquation : Prop
  ellipticityHypotheses : Prop
  boundaryHypotheses : Prop
  firstDerivativeMemLp : MemLp (FirstFDeriv u) exponent μ
  secondDerivativeMemLp : HasSecondDerivativesInLp μ exponent u
  aPrioriConstant : ℝ≥0∞
  estimate :
    eLpNorm (SecondFDeriv u) exponent μ ≤
      aPrioriConstant * (eLpNorm sourceTerm exponent μ + eLpNorm u exponent μ)

/--
Stage1 statement-shape candidate for `W^{2,p}` regularity.

This is intentionally a data-boundary statement, not a proof of elliptic
regularity.
-/
def StatementShape (μ : Measure E) (u : E → F) : Prop :=
  Nonempty (W2pRegularityData μ u)

/--
Public statement-normalization boundary for the Stage1 blueprint.

This is only an alias for `StatementShape`: it records the current repo-local
Lean boundary that public documentation may cite.  It is deliberately not a
terminal `W^{2,p}` regularity theorem, since the PDE operator, weak-solution
predicate, ellipticity hypotheses, weak derivative bridge, and
Calderon-Zygmund/elliptic estimate remain unformalized here.
-/
abbrev PublicStatementNormalizationBoundary (μ : Measure E) (u : E → F) : Prop :=
  StatementShape μ u

/-- The statement-shape definition unfolds to nonemptiness of the normalized data package. -/
theorem statementShape_iff_nonempty (μ : Measure E) (u : E → F) :
    StatementShape μ u ↔ Nonempty (W2pRegularityData μ u) :=
  Iff.rfl

/-- The public normalization boundary is exactly the checked `StatementShape`. -/
theorem publicStatementNormalizationBoundary_eq_statementShape
    (μ : Measure E) (u : E → F) :
    PublicStatementNormalizationBoundary μ u = StatementShape μ u :=
  rfl

/-- A data package exposes the second-derivative `L^p` conclusion. -/
theorem secondDerivativesInLp_of_data {μ : Measure E} {u : E → F}
    (d : W2pRegularityData μ u) :
    HasSecondDerivativesInLp μ d.exponent u :=
  d.secondDerivativeMemLp

/-- Scalar distributions on an open domain, using mathlib's current distribution object. -/
abbrev ScalarDistributionOn (Ω : TopologicalSpace.Opens E) (n : ℕ∞ := ⊤) : Type u :=
  Distribution Ω ℝ n

/--
Checked wrapper around mathlib's Gagliardo-Nirenberg-Sobolev estimate.

This is a first-derivative Sobolev inequality for compact/boundedly supported
smooth functions.  It is useful PDE infrastructure, but it is not a
second-order elliptic `W^{2,p}` regularity theorem.
-/
theorem gns_firstDerivative_eLpNorm_bound
    [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] [FiniteDimensional ℝ F]
    {u : E → F} {s : Set E} (hu : ContDiff ℝ 1 u)
    (h2u : Function.support u ⊆ s) {p : ℝ≥0}
    (hp : 1 ≤ p) (h2p : p < Module.finrank ℝ E)
    (hs : Bornology.IsBounded s) :
    eLpNorm u p μ ≤
      eLpNormLESNormFDerivOfLeConst F μ s p p * eLpNorm (fderiv ℝ u) p μ := by
  exact MeasureTheory.eLpNorm_le_eLpNorm_fderiv μ hu h2u hp h2p hs

/--
Checked wrapper around the equal-exponent Gagliardo-Nirenberg-Sobolev API.

The target exponent `p'` is related to `p` by the usual Sobolev conjugacy
formula.  This remains a first-derivative estimate.
-/
theorem gns_firstDerivative_conjugate_eLpNorm_bound
    [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] [FiniteDimensional ℝ F]
    {u : E → F} (hu : ContDiff ℝ 1 u) (h2u : HasCompactSupport u)
    {p p' : ℝ≥0} (hp : 1 ≤ p) (hn : 0 < Module.finrank ℝ E)
    (hp' : (p' : ℝ)⁻¹ = (p : ℝ)⁻¹ - (Module.finrank ℝ E : ℝ)⁻¹) :
    eLpNorm u p' μ ≤
      SNormLESNormFDerivOfEqConst F μ p * eLpNorm (fderiv ℝ u) p μ := by
  exact MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq μ hu h2u hp hn hp'

/--
Audit classification for the local wrappers available to this Stage1 slot.

These rows are public-backfill metadata: both wrappers may be cited as
first-derivative Sobolev infrastructure, and neither row is evidence for a
terminal second-order elliptic `W^{2,p}` regularity theorem.
-/
def availableWrapperBoundary : List String := [
  "gns_firstDerivative_eLpNorm_bound: checked wrapper for MeasureTheory.eLpNorm_le_eLpNorm_fderiv; cite only as first-derivative Sobolev infrastructure, not as second-order PDE regularity.",
  "gns_firstDerivative_conjugate_eLpNorm_bound: checked wrapper for MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq; cite only as first-derivative Sobolev infrastructure, not as second-order PDE regularity."
]

/--
One missing formal API leaf for a terminal elliptic `W^{2,p}` regularity theorem.

The fields are documentation metadata inside Lean: they split the formalization
debt without postulating any mathematical theorem.
-/
structure MissingFormalApiLeaf where
  api : String
  requiredObject : String
  repoLocalStatus : String
  closureGate : String

/--
Explicit split of the formal APIs still missing before this Stage1 slot can
claim a terminal `W^{2,p}` regularity theorem.

This inventory is intentionally debt metadata.  It does not assert that these
objects exist in mathlib or that the elliptic estimate has been proved.
-/
def missingFormalApiSplit : List MissingFormalApiLeaf := [
  {
    api := "weak derivative",
    requiredObject := "A reusable weak or distributional first-derivative predicate for functions on a domain, connected to mathlib distributions or test functions.",
    repoLocalStatus := "Only classical Frechet derivatives and distribution anchors are present in this Stage1 artifact.",
    closureGate := "Define or import a weak first-derivative API and prove its bridge to the chosen distribution/test-function model."
  },
  {
    api := "weak second derivative",
    requiredObject := "A second weak derivative or Hessian-level distributional derivative predicate with coordinate/index or multilinear structure.",
    repoLocalStatus := "The current `SecondFDeriv` abbreviation is classical and does not encode weak second derivatives.",
    closureGate := "Formalize weak second derivatives and prove compatibility with classical second Frechet derivatives under sufficient smoothness."
  },
  {
    api := "concrete W2p membership",
    requiredObject := "A concrete `W^{2,p}` membership predicate bundling function, weak first derivatives, and weak second derivatives in `L^p`.",
    repoLocalStatus := "`HasSecondDerivativesInLp` records only `MemLp (SecondFDeriv u) p μ`; it is not a Sobolev-space membership definition.",
    closureGate := "Define the exact Sobolev membership object used by the theorem and prove equivalence to the normalized second-derivative conclusion when appropriate."
  },
  {
    api := "elliptic operator and coefficient model",
    requiredObject := "A second-order elliptic operator with coefficient regularity, ellipticity constants, and source term model.",
    repoLocalStatus := "`W2pRegularityData` keeps `weakEquation` and `ellipticityHypotheses` as abstract propositions.",
    closureGate := "Replace the abstract fields with a concrete operator/coefficient structure and checked ellipticity hypotheses."
  },
  {
    api := "weak solution predicate",
    requiredObject := "A weak-solution predicate pairing the operator, source term, domain, test functions, and integration-by-parts identity.",
    repoLocalStatus := "No weak PDE solution predicate is defined repo-locally for this slot.",
    closureGate := "Define the weak formulation and prove it is well-typed for the chosen function spaces and domain hypotheses."
  },
  {
    api := "domain and boundary hypotheses",
    requiredObject := "Domain assumptions and boundary or localization hypotheses sufficient for the selected regularity theorem.",
    repoLocalStatus := "`boundaryHypotheses` is an abstract proposition with no domain geometry or trace model.",
    closureGate := "Choose the domain class and boundary condition model, then connect them to the weak solution predicate and estimate theorem."
  },
  {
    api := "Calderon-Zygmund or equivalent estimate",
    requiredObject := "A checked a priori estimate controlling second derivatives by the PDE source and lower-order norms.",
    repoLocalStatus := "Only first-derivative Gagliardo-Nirenberg-Sobolev wrappers are checked; no second-order elliptic estimate is present.",
    closureGate := "Prove or import a Calderon-Zygmund-style estimate, or document a concrete integration blocker for a pinned external theorem."
  },
  {
    api := "classical/weak bridge",
    requiredObject := "Bridge theorems between classical derivatives/equations and the weak/distributional Sobolev formulation.",
    repoLocalStatus := "The current statement shape uses classical `fderiv`; no bridge proves that it represents weak PDE regularity.",
    closureGate := "Prove smooth-to-weak and weak-regularity-to-classical-conclusion bridge lemmas needed by the terminal statement."
  }
]

/-- The missing formal API split has the eight public leaves requested for this child. -/
theorem missingFormalApiSplit_length : missingFormalApiSplit.length = 8 :=
  rfl

/--
Pinned mathlib revision used for the Stage1 mathlib audit of this slot.

This is metadata for the audit boundary, not a theorem-completion claim.
-/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Modules requested by the public mathlib-audit leaf and found in the pinned
mathlib source tree.
-/
def requestedMathlibAuditModules : List String := [
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv"
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "fderiv",
  "ContDiff",
  "HasCompactSupport",
  "Distribution",
  "Distribution.mapCLM",
  "LineDeriv.iteratedLineDerivOp",
  "LineDeriv.lineDerivOpCLM",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one"
]

/--
Search terms that did not locate a terminal elliptic `W^{2,p}` regularity theorem
in local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "W2p",
  "W^{2,p}",
  "Sobolev space",
  "weak derivative",
  "WeakDerivative",
  "Calderon",
  "Calderón",
  "Zygmund",
  "elliptic regularity",
  "PDE regularity",
  "Laplacian regularity",
  "second derivative Lp"
]

/--
One row in the external Lean 4 audit for this Stage1 slot.

These rows are source and integration metadata only.  A row does not close the
terminal theorem unless its exact statement is pinned, imported, and checked by
this repository's Lake build.
-/
structure ExternalLean4AuditRow where
  repository : String
  commit : String
  searchTermsHit : List String
  theoremOrApiNames : List String
  toolchain : String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  terminalW2pStatus : String

/--
Primary-source external Lean 4 audit rows for the requested `W^{2,p}` search.

The De Giorgi project is relevant PDE regularity infrastructure, especially for
weak derivatives and first-order Sobolev witnesses.  It is not a terminal
Calderon-Zygmund or elliptic `W^{2,p}` theorem for second derivatives.
-/
def externalLean4AuditRows : List ExternalLean4AuditRow := [
  {
    repository := "https://github.com/leanprover-community/mathlib4",
    commit := pinnedMathlibRevision,
    searchTermsHit := [
      "MemLp",
      "second derivative"
    ],
    theoremOrApiNames := [
      "MeasureTheory.MemLp",
      "MeasureTheory.eLpNorm",
      "LineDeriv.iteratedLineDerivOp",
      "SchwartzMap.laplacian_eq_sum"
    ],
    toolchain := "leanprover/lean4:v4.29.0",
    placeholderStatus := "pinned repo-local dependency; no proof-placeholder declaration introduced by this Stage1 wrapper",
    lakeDependencyFeasibility := "already pinned in this repository's lake-manifest.json",
    terminalW2pStatus := "infrastructure only; local exact-term search found no terminal W2p, W^{2,p}, WeakDerivative, Calderon-Zygmund, elliptic regularity, PDE regularity, or second-derivative MemLp theorem for THM-M-1172"
  },
  {
    repository := "https://github.com/scottnarmstrong/DeGiorgi",
    commit := "4c1b3077d3782b24065184df4ba59501b2e56fc7",
    searchTermsHit := [
      "WeakDerivative",
      "weak derivative",
      "Calderon",
      "Calderón",
      "Zygmund",
      "elliptic regularity",
      "PDE regularity",
      "MemLp"
    ],
    theoremOrApiNames := [
      "HasWeakPartialDeriv",
      "HasWeakGrad",
      "HasWeakDiv",
      "MemW1p",
      "MemW1pWitness",
      "linfty_subsolution_DeGiorgi_normalized",
      "weak_harnack",
      "weak_harnack_on_ball",
      "harnack",
      "harnack_of_homogeneousWeakSolution",
      "holder_Moser",
      "holder_Moser_of_homogeneousWeakSolution"
    ],
    toolchain := "leanprover/lean4:v4.29.0-rc6; mathlib 5c8398df528176d9c87ccd9226ba8f7c8852d59c",
    placeholderStatus := "public source scan found no proof-placeholder declarations; one assumption-word occurrence appeared only in a prose comment; README states placeholder-free status beyond Lean and Mathlib",
    lakeDependencyFeasibility := "not drop-in for this repo-local closure: toolchain and mathlib revision differ from this repository's leanprover/lean4:v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; integration would require pinning as an external dependency or porting the needed APIs",
    terminalW2pStatus := "related external upstream PDE regularity infrastructure only; no W2p/W^{2,p} or second-derivative MemLp terminal theorem was located"
  }
]

/--
External Lean 4 anchor audit for this slot.

The checked local artifact does not import an external project proving a
terminal Calderon-Zygmund or elliptic `W^{2,p}` regularity theorem.  Related
public Lean 4 PDE regularity work may be relevant infrastructure, but it is not
repo-local closure for this theorem unless a later integrator pins, imports, and
checks the exact terminal statement.
-/
def externalLean4AnchorAudit : List String := [
  "Local gh authentication was unavailable, so authenticated GitHub code search could not be honestly recorded; public primary-source repository searches were used and this remains an audit blocker for the public child leaf.",
  "No terminal Lean 4 Calderon-Zygmund or elliptic W2p regularity theorem is in this repo-local Lake closure.",
  "No external Lean 4 proof is pinned, imported, or checked by this Stage1 module.",
  "The external scottnarmstrong/DeGiorgi Lean 4 project is relevant weak-derivative, Sobolev, Harnack, and Holder regularity infrastructure, but it is not a located terminal W2p theorem and is not currently pinned in this repository.",
  "Any later external upstream candidate must identify exact project, revision, module, theorem name, license, and Lake compatibility before reuse.",
  "Therefore this Stage1 artifact remains statement-shape plus mathlib wrappers, with formalization_debt and no completed-state repo_local_integration_debt claim."
]

/--
Repo-local integration-gate status for one audited upstream candidate.

These rows are checked metadata only.  They prevent an anchor-only external
source from being mistaken for a completed theorem in this repository.
-/
structure RepoLocalIntegrationGateRow where
  candidate : String
  terminalClosureLocated : Bool
  repoLocalPinnedImportedChecked : Bool
  gateStatus : String
  integrationBlocker : String

/--
Integration-gate rows for `THM-M-1172`.

Since no terminal external Lean 4 `W^{2,p}` theorem was located in the audit,
there is nothing to mark as `external_upstream_pinned`.  The De Giorgi row is
kept open as relevant infrastructure with concrete blockers, not completion
evidence.
-/
def repoLocalIntegrationGateRows : List RepoLocalIntegrationGateRow := [
  {
    candidate := "pinned mathlib infrastructure",
    terminalClosureLocated := false,
    repoLocalPinnedImportedChecked := true,
    gateStatus := "not a terminal W2p closure; usable only as already-pinned infrastructure",
    integrationBlocker := "no Calderon-Zygmund or elliptic W2p second-derivative MemLp theorem was found in the pinned mathlib revision"
  },
  {
    candidate := "https://github.com/scottnarmstrong/DeGiorgi @ 4c1b3077d3782b24065184df4ba59501b2e56fc7",
    terminalClosureLocated := false,
    repoLocalPinnedImportedChecked := false,
    gateStatus := "external_upstream_anchor_only is not completed; candidate remains background infrastructure",
    integrationBlocker := "no terminal W2p theorem was located; the project also uses leanprover/lean4:v4.29.0-rc6 and mathlib 5c8398df528176d9c87ccd9226ba8f7c8852d59c, so reuse would require a separate pin/port/check task"
  }
]

/--
The integration gate currently has no completed external-upstream theorem.

This proposition is deliberately weak and data-oriented: it records that every
audited row with `terminalClosureLocated = true` would still need to be
repo-locally pinned/imported/checked before completion could be claimed.
-/
def repoLocalIntegrationDebtGate : Prop :=
  ∀ row ∈ repoLocalIntegrationGateRows,
    row.terminalClosureLocated = true → row.repoLocalPinnedImportedChecked = true

/-- The current integration-gate metadata contains no terminal external closure rows. -/
theorem repoLocalIntegrationDebtGate_current : repoLocalIntegrationDebtGate := by
  intro row hrow hterminal
  simp [repoLocalIntegrationGateRows] at hrow
  rcases hrow with hrow | hrow
  · subst row
    contradiction
  · subst row
    contradiction

end S1_M_147
end Stage1
end AwesomeTheorems
