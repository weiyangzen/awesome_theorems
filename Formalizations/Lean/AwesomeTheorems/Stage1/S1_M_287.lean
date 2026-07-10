import Mathlib.Probability.StrongLaw
import Mathlib.Probability.Martingale.BorelCantelli
import Mathlib.Probability.Moments.Variance

/-!
# S1-M-287 / THM-M-1007: Kolmogorov three-series theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for
Kolmogorov's three-series theorem for independent real random variables.

The pinned mathlib snapshot has the needed substrate for a future proof:
independence of random variables, Bochner integrability, variance, Borel-Cantelli
lemmas, truncation infrastructure used in the strong law, and almost-sure
convergence predicates.  A terminal theorem named `Kolmogorov three-series`, or a
direct equivalence for convergence of independent real series, was not found in
the repo-local dependency closure.  Accordingly this file supplies a precise
statement shape and small checked wrappers only; it does not claim the theorem is
machine-closed in this repository.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped MeasureTheory Topology ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_287

universe u

/-- Partial sums of a real-valued random series. -/
def partialSum {Ω : Type u} (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  ∑ i ∈ Finset.range n, X i ω

/-- Truncation at radius `c`, used in Kolmogorov's three-series conditions. -/
def truncation {Ω : Type u} (c : ℝ) (Xn : Ω → ℝ) (ω : Ω) : ℝ :=
  if ‖Xn ω‖ ≤ c then Xn ω else 0

/-- Scalar truncation map used to postcompose independent real random variables. -/
def truncationFunction (c : ℝ) (x : ℝ) : ℝ :=
  if ‖x‖ ≤ c then x else 0

/-- Large-jump event for the `n`-th random variable at radius `c`. -/
def largeJumpEvent {Ω : Type u} (X : ℕ → Ω → ℝ) (c : ℝ) (n : ℕ) : Set Ω :=
  {ω | c < ‖X n ω‖}

/--
Input package for the real-valued independent random variables in the
three-series theorem.
-/
structure ThreeSeriesData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  isProbability : IsProbabilityMeasure μ
  X : ℕ → Ω → ℝ
  measurable : ∀ n : ℕ, Measurable (X n)
  independent : iIndepFun X μ

/-- Centered truncated variable for the `n`-th random variable. -/
def centeredTruncation {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  truncation c (D.X n) ω - ∫ ω, truncation c (D.X n) ω ∂D.μ

/--
Scalar postcomposition map for centered truncations.  The centering constant may
depend on `n`, but the map still depends only on the original scalar value.
-/
def centeredTruncationFunction {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) (x : ℝ) : ℝ :=
  truncationFunction c x - ∫ ω, truncation c (D.X n) ω ∂D.μ

/-- Almost-sure convergence of the random series `∑ n, X n`. -/
def AlmostSureSummable {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) : Prop :=
  ∀ᵐ ω ∂D.μ, Summable fun n : ℕ => D.X n ω

/--
Kolmogorov's three scalar series at truncation radius `c`.

The three components are:
* summability of large-jump probabilities;
* convergence of the series of expectations of truncated variables;
* summability of the variances of truncated variables.

Integrability and `L^2` hypotheses for the truncated variables are recorded
explicitly so later proof work does not rely on undefined behavior of the
integral or variance APIs outside their intended mathematical domain.
-/
def ThreeSeriesConditions {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) : Prop :=
  0 < c ∧
    (∀ n : ℕ, Integrable (truncation c (D.X n)) D.μ) ∧
    (∀ n : ℕ, MemLp (truncation c (D.X n)) 2 D.μ) ∧
    Summable (fun n : ℕ => D.μ.real (largeJumpEvent D.X c n)) ∧
    Summable (fun n : ℕ => ∫ ω, truncation c (D.X n) ω ∂D.μ) ∧
    Summable (fun n : ℕ => variance (truncation c (D.X n)) D.μ)

/--
Stage1 normalized statement shape for Kolmogorov's three-series theorem.

For each positive truncation radius, the almost-sure convergence of the
independent real random series is equivalent to the three scalar series
conditions.  This declaration is a proposition only; the terminal proof is left
as formalization debt until an upstream or local Lean proof is located and
integrated.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : ThreeSeriesData Ω,
      ∀ c : ℝ, 0 < c →
        (AlmostSureSummable D ↔ ThreeSeriesConditions D c)

/-- The normalized statement unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : ThreeSeriesData Ω,
          ∀ c : ℝ, 0 < c →
            (AlmostSureSummable D ↔ ThreeSeriesConditions D c) :=
  Iff.rfl

/-- Project the probability-measure instance from the normalized data package. -/
theorem isProbability_from_data {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) :
    IsProbabilityMeasure D.μ :=
  D.isProbability

/-- Project coordinate measurability from the normalized data package. -/
theorem measurable_X {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (n : ℕ) :
    Measurable (D.X n) :=
  D.measurable n

/-- The scalar truncation postcomposition map is Borel-measurable. -/
theorem measurable_truncationFunction (c : ℝ) :
    Measurable (truncationFunction c) := by
  exact Measurable.ite (measurableSet_le measurable_norm measurable_const)
    measurable_id measurable_const

/-- Truncating a measurable real random variable preserves measurability. -/
theorem measurable_truncation {Ω : Type u} [MeasurableSpace Ω]
    {c : ℝ} {Xn : Ω → ℝ} (hXn : Measurable Xn) :
    Measurable (truncation c Xn) := by
  simpa [truncation, truncationFunction, Function.comp_def] using
    (measurable_truncationFunction c).comp hXn

/-- Truncated coordinates from the normalized data package are measurable. -/
theorem measurable_truncation_X {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) :
    Measurable (truncation c (D.X n)) :=
  measurable_truncation (D.measurable n)

/-- Large-jump events from the normalized data package are measurable. -/
theorem measurableSet_largeJumpEvent {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) :
    MeasurableSet (largeJumpEvent D.X c n) := by
  exact measurableSet_lt measurable_const (D.measurable n).norm

/-- The scalar centered-truncation postcomposition map is Borel-measurable. -/
theorem measurable_centeredTruncationFunction {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) :
    Measurable (centeredTruncationFunction D c n) := by
  exact (measurable_truncationFunction c).sub measurable_const

/-- Centered truncated coordinates from the normalized data package are measurable. -/
theorem measurable_centeredTruncation {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) :
    Measurable (centeredTruncation D c n) := by
  simpa [centeredTruncation, centeredTruncationFunction, truncation,
    truncationFunction, Function.comp_def] using
    (measurable_centeredTruncationFunction D c n).comp (D.measurable n)

/-- Project independence from the normalized data package. -/
theorem independent_X {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) :
    iIndepFun D.X D.μ :=
  D.independent

/--
Independence of truncated variables, obtained by measurable postcomposition of
the independent original variables.
-/
theorem independent_truncation {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) :
    iIndepFun (fun n : ℕ => truncation c (D.X n)) D.μ := by
  simpa [truncation, truncationFunction, Function.comp_def] using
    D.independent.comp (fun _ : ℕ => truncationFunction c)
      (fun _ : ℕ => measurable_truncationFunction c)

/--
Independence of centered truncated variables, again by measurable
postcomposition.  The centering constant is index-dependent, which is allowed by
`ProbabilityTheory.iIndepFun.comp`.
-/
theorem independent_centeredTruncation {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) :
    iIndepFun (fun n : ℕ => centeredTruncation D c n) D.μ := by
  simpa [centeredTruncation, centeredTruncationFunction, truncation,
    truncationFunction, Function.comp_def] using
    D.independent.comp (fun n : ℕ => centeredTruncationFunction D c n)
      (fun n : ℕ => measurable_centeredTruncationFunction D c n)

/-- The normalized partial-sum notation unfolds to the finite range sum. -/
theorem partialSum_apply {Ω : Type u} (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) :
    partialSum X n ω = ∑ i ∈ Finset.range n, X i ω :=
  rfl

/-- Inside the truncation radius, truncation leaves the variable unchanged. -/
theorem truncation_eq_of_norm_le {Ω : Type u} {c : ℝ} {Xn : Ω → ℝ} {ω : Ω}
    (h : ‖Xn ω‖ ≤ c) :
    truncation c Xn ω = Xn ω := by
  rw [truncation, if_pos h]

/-- Outside the truncation radius, truncation is zero. -/
theorem truncation_eq_zero_of_lt_norm {Ω : Type u} {c : ℝ} {Xn : Ω → ℝ} {ω : Ω}
    (h : c < ‖Xn ω‖) :
    truncation c Xn ω = 0 := by
  rw [truncation, if_neg (not_le.mpr h)]

/-- The large-jump event notation unfolds to the expected norm inequality. -/
theorem mem_largeJumpEvent {Ω : Type u} (X : ℕ → Ω → ℝ) (c : ℝ) (n : ℕ) (ω : Ω) :
    ω ∈ largeJumpEvent X c n ↔ c < ‖X n ω‖ :=
  Iff.rfl

/--
For a probability measure, the `ENNReal` measure of a large-jump event is the
`ENNReal.ofReal` coercion of its real-valued probability.
-/
theorem ofReal_real_largeJump_measure {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) (c : ℝ) (n : ℕ) :
    ENNReal.ofReal (D.μ.real (largeJumpEvent D.X c n)) =
      D.μ (largeJumpEvent D.X c n) := by
  haveI : IsProbabilityMeasure D.μ := D.isProbability
  exact ofReal_measureReal

/--
Real summability of the large-jump probabilities implies the `ℝ≥0∞`
Borel-Cantelli summability hypothesis.

This closes the child `S1-M-287-C004` bridge needed before applying
`MeasureTheory.ae_eventually_notMem`.
-/
theorem largeJump_real_summable_to_ennreal {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) {c : ℝ}
    (hs : Summable (fun n : ℕ => D.μ.real (largeJumpEvent D.X c n))) :
    ∑' n : ℕ, D.μ (largeJumpEvent D.X c n) ≠ ⊤ := by
  haveI : IsProbabilityMeasure D.μ := D.isProbability
  simpa [ofReal_measureReal] using
    (Summable.tsum_ofReal_ne_top
      (f := fun n : ℕ => D.μ.real (largeJumpEvent D.X c n)) hs)

/--
Checked Borel-Cantelli wrapper for the large-jump branch: if the large-jump
probabilities are summable in `ℝ≥0∞`, then almost every sample point eventually
avoids those events.
-/
theorem ae_eventually_not_largeJump {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) {c : ℝ}
    (hs : ∑' n : ℕ, D.μ (largeJumpEvent D.X c n) ≠ ⊤) :
    ∀ᵐ ω ∂D.μ, ∀ᶠ n : ℕ in atTop, ω ∉ largeJumpEvent D.X c n :=
  ae_eventually_notMem hs

/--
Checked Borel-Cantelli wrapper in the scalar form used by the three-series
conditions: real summability of the large-jump probabilities is enough to get
almost-sure eventual avoidance of large jumps.
-/
theorem ae_eventually_not_largeJump_of_real_summable {Ω : Type u} [MeasurableSpace Ω]
    (D : ThreeSeriesData Ω) {c : ℝ}
    (hs : Summable (fun n : ℕ => D.μ.real (largeJumpEvent D.X c n))) :
    ∀ᵐ ω ∂D.μ, ∀ᶠ n : ℕ in atTop, ω ∉ largeJumpEvent D.X c n :=
  ae_eventually_not_largeJump D (largeJump_real_summable_to_ennreal D hs)

/--
Checked variance anchor: mathlib has the finite-sum variance formula for
pairwise independent real random variables with finite second moment.
-/
theorem variance_sum_pairwise_indep_anchor {Ω : Type u} [MeasurableSpace Ω]
    {ι : Type*} {X : ι → Ω → ℝ} {s : Finset ι} {μ : Measure Ω}
    (hs : ∀ i ∈ s, MemLp (X i) 2 μ)
    (h : Set.Pairwise ↑s fun i j => X i ⟂ᵢ[μ] X j) :
    variance (∑ i ∈ s, X i) μ = ∑ i ∈ s, variance (X i) μ :=
  IndepFun.variance_sum hs h

/-- Pinned mathlib revision used for the public anchor audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- One row in the integration-ready public mathlib anchor table. -/
structure MathlibAnchorRow where
  declarationName : String
  moduleName : String
  sourceFile : String
  sourceLine : String
  role : String
  repoLocalEvidence : String
  completionUse : String
deriving Repr

/--
Integration-ready anchor table for the public `S1-M-287 / THM-M-1007`
backfill.  These are substrate anchors from the pinned mathlib dependency, not
a terminal Kolmogorov three-series theorem.
-/
def publicMathlibAnchorTable : List MathlibAnchorRow := [
  {
    declarationName := "ProbabilityTheory.iIndepFun"
    moduleName := "Mathlib.Probability.Independence.Basic"
    sourceFile := "Mathlib/Probability/Independence/Basic.lean"
    sourceLine := "136"
    role := "independence package for countable families of random variables"
    repoLocalEvidence := "#check ProbabilityTheory.iIndepFun and theorem independent_X"
    completionUse := "substrate anchor only; future proof must build the truncated-variable independence wrappers"
  },
  {
    declarationName := "MeasureTheory.ae_eventually_notMem"
    moduleName := "Mathlib.MeasureTheory.OuterMeasure.BorelCantelli"
    sourceFile := "Mathlib/MeasureTheory/OuterMeasure/BorelCantelli.lean"
    sourceLine := "86"
    role := "first Borel-Cantelli implication for summable large-jump events"
    repoLocalEvidence := "#check MeasureTheory.ae_eventually_notMem and theorem ae_eventually_not_largeJump"
    completionUse := "substrate anchor with local wrapper; theorem largeJump_real_summable_to_ennreal closes the real-to-ENNReal summability bridge"
  },
  {
    declarationName := "MeasureTheory.ae_mem_limsup_atTop_iff"
    moduleName := "Mathlib.Probability.Martingale.BorelCantelli"
    sourceFile := "Mathlib/Probability/Martingale/BorelCantelli.lean"
    sourceLine := "341"
    role := "Levy generalized Borel-Cantelli limsup characterization"
    repoLocalEvidence := "#check MeasureTheory.ae_mem_limsup_atTop_iff"
    completionUse := "adjacent substrate anchor; no terminal three-series equivalence is claimed"
  },
  {
    declarationName := "ProbabilityTheory.IndepFun.variance_sum"
    moduleName := "Mathlib.Probability.Moments.Variance"
    sourceFile := "Mathlib/Probability/Moments/Variance.lean"
    sourceLine := "422"
    role := "variance of a finite sum of pairwise independent real variables"
    repoLocalEvidence := "#check ProbabilityTheory.IndepFun.variance_sum and theorem variance_sum_pairwise_indep_anchor"
    completionUse := "substrate anchor only; future proof must connect centered truncations to this finite-sum formula"
  },
  {
    declarationName := "ProbabilityTheory.strong_law_ae"
    moduleName := "Mathlib.Probability.StrongLaw"
    sourceFile := "Mathlib/Probability/StrongLaw.lean"
    sourceLine := "788"
    role := "almost-sure strong law anchor for independent identically distributed variables"
    repoLocalEvidence := "#check ProbabilityTheory.strong_law_ae"
    completionUse := "adjacent strong-law anchor; it does not specialize directly to Kolmogorov three-series"
  },
  {
    declarationName := "ProbabilityTheory.variance"
    moduleName := "Mathlib.Probability.Moments.Variance"
    sourceFile := "Mathlib/Probability/Moments/Variance.lean"
    sourceLine := "63"
    role := "variance scalar used in the third Kolmogorov scalar series"
    repoLocalEvidence := "#check ProbabilityTheory.variance and def ThreeSeriesConditions"
    completionUse := "substrate anchor only; terminal theorem remains formalization_debt"
  }
]

/-- Declaration names in the public anchor table requested by child `S1-M-287-C002`. -/
def publicMathlibAnchorNames : List String :=
  publicMathlibAnchorTable.map (fun row => row.declarationName)

/--
The requested public anchor table contains exactly the six substrate declarations
named by child `S1-M-287-C002`.
-/
theorem publicMathlibAnchorTable_length :
    publicMathlibAnchorTable.length = 6 :=
  rfl

/-- mathlib modules checked while locating repo-local three-series anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.StrongLaw",
  "Mathlib.Probability.BorelCantelli",
  "Mathlib.Probability.Martingale.BorelCantelli",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integrable",
  "Mathlib.Probability.Moments.Variance",
  "Mathlib.MeasureTheory.Function.L1Space.Integrable",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/-- Checked declaration names used or audited as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.comp",
  "ProbabilityTheory.IndepFun.variance_sum",
  "MeasureTheory.measure_limsup_atTop_eq_zero",
  "MeasureTheory.ae_eventually_notMem",
  "MeasureTheory.ae_mem_limsup_atTop_iff",
  "ProbabilityTheory.strong_law_ae",
  "ProbabilityTheory.strong_law_ae_real",
  "ProbabilityTheory.variance",
  "MeasureTheory.Integrable",
  "MeasureTheory.MemLp",
  "Filter.Tendsto",
  "Summable"
]

/--
Search terms that did not locate a terminal Kolmogorov three-series theorem in
the pinned local mathlib dependency closure.
-/
def absentTerminalSearchTerms : List String := [
  "Kolmogorov three-series",
  "Kolmogorov three series",
  "three-series theorem",
  "ThreeSeries",
  "independent random series convergence",
  "series of independent random variables"
]

/-! ## External Lean 4 terminal theorem audit for child `S1-M-287-C006`. -/

/--
One row in the external Lean 4 primary-source audit for a terminal
Kolmogorov three-series theorem.

These rows are audit metadata only.  A row may not be used as completion
evidence unless it names a theorem that has been pinned/imported/checked in the
repo-local Lake closure.
-/
structure ExternalLeanAuditRow where
  sourceSurface : String
  queryOrScope : String
  finding : String
  integrationDecision : String
deriving Repr

/--
External Lean 4 primary-source audit rows for child `S1-M-287-C006`.

The audit did not identify a terminal Lean 4 theorem for Kolmogorov's
three-series equivalence.  Therefore this repository has no known external proof
anchor to pin or import for this child, and the terminal theorem remains
`formalization_debt` rather than `repo_local_integration_debt`.
-/
def c006ExternalLeanAuditRows : List ExternalLeanAuditRow := [
  {
    sourceSurface := "repo-local pinned mathlib source"
    queryOrScope := "rg Kolmogorov, ThreeSeries, three-series, three series, independent random series under Mathlib/Probability and Mathlib/MeasureTheory at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    finding := "only adjacent Kolmogorov process, Kolmogorov zero-one law, Chapman-Kolmogorov, strong-law, Borel-Cantelli, independence, and variance substrate was found; no terminal three-series theorem was found"
    integrationDecision := "no external theorem to pin/import/check from this surface"
  },
  {
    sourceSurface := "GitHub repository search API"
    queryOrScope := "Kolmogorov three series Lean; ThreeSeries Lean; probability Lean 4 Kolmogorov"
    finding := "repository search returned zero candidate repositories for these terminal-theorem queries"
    integrationDecision := "no candidate dependency identified"
  },
  {
    sourceSurface := "Loogle mathlib declaration search"
    queryOrScope := "Kolmogorov three series; ThreeSeries; three-series; series of independent random variables"
    finding := "no declaration corresponding to a terminal three-series theorem was returned"
    integrationDecision := "confirms absence from searchable mathlib declarations; no upstream wrapper available"
  },
  {
    sourceSurface := "public web search restricted to GitHub source surfaces"
    queryOrScope := "site:github.com Kolmogorov three series lean; site:github.com Kolmogorov three-series lean; site:github.com ThreeSeries lean"
    finding := "no concrete Lean 4 source file, module, or theorem name for the terminal theorem was identified"
    integrationDecision := "no anchor-only external proof is retained as completed evidence"
  }
]

/-- Search terms used by child `S1-M-287-C006` for the external terminal theorem audit. -/
def c006ExternalLeanAuditSearchTerms : List String := [
  "Kolmogorov three series Lean",
  "Kolmogorov three-series Lean",
  "Kolmogorov three-series theorem Lean 4",
  "ThreeSeries Lean",
  "KolmogorovThreeSeries",
  "kolmogorov_three_series",
  "series of independent random variables Lean",
  "independent random series iIndepFun Summable"
]

/--
Child `S1-M-287-C006` did not find an external Lean 4 terminal theorem to
integrate.
-/
def c006ExternalTerminalProofFound : Bool :=
  false

/--
Child `S1-M-287-C006` leaves no completed-state repo-local integration debt:
there is no known external terminal proof being used as anchor-only completion
evidence.
-/
def c006RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The C006 external audit table has the four recorded source-surface rows. -/
theorem c006ExternalLeanAuditRows_length :
    c006ExternalLeanAuditRows.length = 4 :=
  rfl

/-- C006 found no external terminal Lean 4 proof to pin/import/check. -/
theorem c006ExternalTerminalProofFound_eq_false :
    c006ExternalTerminalProofFound = false :=
  rfl

/-- C006 retains no completed-state repo-local integration debt. -/
theorem c006RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c006RepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## Theorem-tree package ledger for child `S1-M-287-C003`. -/

namespace K3S

/--
One package row in the Kolmogorov three-series theorem tree.

This metadata is intentionally checked as data, not as a proof of any package.
The `status` field remains `unchecked` until a future worker supplies local
proof bodies or pinned/imported upstream closures for the corresponding leaves.
-/
structure PackageRow where
  packageId : String
  packageName : String
  role : String
  primaryLeafIds : List String
  status : String
deriving Repr

/-- One theorem-tree leaf row for the `K3S` package split. -/
structure LeafRow where
  leafId : String
  packageId : String
  goal : String
  status : String
deriving Repr

/--
Integration-ready theorem-tree package split for Kolmogorov's three-series
theorem.  The package ids are the public ids requested by child
`S1-M-287-C003`: `K3S.P1` through `K3S.P8`.
-/
def theoremTreePackages : List PackageRow := [
  {
    packageId := "K3S.P1"
    packageName := "statement_normalization"
    role := "freeze the probability-space data, random-variable family, truncation radius, large-jump event, truncated variables, expectation and variance series, and almost-sure convergence target"
    primaryLeafIds := ["K3S.L001", "K3S.L002", "K3S.L022", "K3S.L023"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P2"
    packageName := "mathlib_object_model"
    role := "align the statement with iIndepFun, Integrable, MemLp, variance, Summable, Tendsto, and almost-everywhere filters"
    primaryLeafIds := ["K3S.L001", "K3S.L002", "K3S.L003", "K3S.L008", "K3S.L009", "K3S.L010"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P3"
    packageName := "large_jump_branch"
    role := "turn summable large-jump probabilities into eventual agreement between original and truncated series using Borel-Cantelli"
    primaryLeafIds := ["K3S.L004", "K3S.L005", "K3S.L006", "K3S.L007"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P4"
    packageName := "truncated_centered_branch"
    role := "reduce convergence of centered truncated partial sums to variance summability and independence"
    primaryLeafIds := ["K3S.L008", "K3S.L009", "K3S.L010", "K3S.L011", "K3S.L012", "K3S.L013", "K3S.L014", "K3S.L015", "K3S.L016"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P5"
    packageName := "expectation_branch"
    role := "combine centered convergence with convergence of the deterministic expectation series"
    primaryLeafIds := ["K3S.L017"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P6"
    packageName := "forward_direction"
    role := "derive the three scalar series from almost-sure convergence of the original independent series"
    primaryLeafIds := ["K3S.L019", "K3S.L020", "K3S.L021", "K3S.L022", "K3S.L023"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P7"
    packageName := "reverse_direction"
    role := "derive almost-sure convergence of the original series from the three scalar conditions"
    primaryLeafIds := ["K3S.L004", "K3S.L005", "K3S.L006", "K3S.L007", "K3S.L008", "K3S.L009", "K3S.L010", "K3S.L011", "K3S.L012", "K3S.L013", "K3S.L014", "K3S.L015", "K3S.L016", "K3S.L017", "K3S.L018"]
    status := "unchecked"
  },
  {
    packageId := "K3S.P8"
    packageName := "repo_local_closure_gate"
    role := "replace the statement boundary with a local proof, mathlib wrapper, or pinned external proof only after repo-local validation"
    primaryLeafIds := ["K3S.L024"]
    status := "unchecked"
  }
]

/--
Theorem-tree leaves preserved from the parent `S1-M-287` ledger.  Individual
rows may move out of `unchecked` only when a child supplies repo-local checked
evidence for that leaf; this file still does not claim the terminal theorem.
-/
def uncheckedLeafLedger : List LeafRow := [
  {
    leafId := "K3S.L001"
    packageId := "K3S.P1/K3S.P2"
    goal := "prove measurability of truncation c (D.X n) from D.measurable n"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    leafId := "K3S.L002"
    packageId := "K3S.P1/K3S.P2"
    goal := "show largeJumpEvent D.X c n is measurable for 0 < c"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    leafId := "K3S.L003"
    packageId := "K3S.P2"
    goal := "prove D.independent.comp preserves independence of truncated variables"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    leafId := "K3S.L004"
    packageId := "K3S.P3/K3S.P7"
    goal := "convert real summability of large-jump probabilities to the ENNReal hypothesis needed by ae_eventually_notMem"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    leafId := "K3S.L005"
    packageId := "K3S.P3/K3S.P7"
    goal := "use Borel-Cantelli to prove only finitely many large jumps occur almost surely"
    status := "unchecked"
  },
  {
    leafId := "K3S.L006"
    packageId := "K3S.P3/K3S.P7"
    goal := "prove eventual equality of original and truncated tails outside the large-jump limsup"
    status := "unchecked"
  },
  {
    leafId := "K3S.L007"
    packageId := "K3S.P3/K3S.P7"
    goal := "prove almost-sure summability is invariant under changing finitely many terms"
    status := "unchecked"
  },
  {
    leafId := "K3S.L008"
    packageId := "K3S.P2/K3S.P4/K3S.P7"
    goal := "define centered truncations and prove their integrability"
    status := "unchecked"
  },
  {
    leafId := "K3S.L009"
    packageId := "K3S.P2/K3S.P4/K3S.P7"
    goal := "prove MemLp of centered truncations from MemLp of truncations"
    status := "unchecked"
  },
  {
    leafId := "K3S.L010"
    packageId := "K3S.P2/K3S.P4/K3S.P7"
    goal := "prove independence of centered truncations"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    leafId := "K3S.L011"
    packageId := "K3S.P4/K3S.P7"
    goal := "use IndepFun.variance_sum on finite centered truncated sums"
    status := "unchecked"
  },
  {
    leafId := "K3S.L012"
    packageId := "K3S.P4/K3S.P7"
    goal := "derive finite-sum variance bounds from variance summability"
    status := "unchecked"
  },
  {
    leafId := "K3S.L013"
    packageId := "K3S.P4/K3S.P7"
    goal := "apply Chebyshev or Markov inequality to centered truncated partial sums"
    status := "unchecked"
  },
  {
    leafId := "K3S.L014"
    packageId := "K3S.P4/K3S.P7"
    goal := "sum the tail probabilities for centered truncated partial sums"
    status := "unchecked"
  },
  {
    leafId := "K3S.L015"
    packageId := "K3S.P4/K3S.P7"
    goal := "apply Borel-Cantelli to get almost-sure Cauchy behavior of centered truncated partial sums"
    status := "unchecked"
  },
  {
    leafId := "K3S.L016"
    packageId := "K3S.P4/K3S.P7"
    goal := "turn almost-sure Cauchy partial sums in real numbers into almost-sure summability"
    status := "unchecked"
  },
  {
    leafId := "K3S.L017"
    packageId := "K3S.P5/K3S.P7"
    goal := "combine centered convergence with convergence of expectation series"
    status := "unchecked"
  },
  {
    leafId := "K3S.L018"
    packageId := "K3S.P7"
    goal := "prove the reverse direction from the three conditions to almost-sure convergence"
    status := "unchecked"
  },
  {
    leafId := "K3S.L019"
    packageId := "K3S.P6"
    goal := "derive large-jump summability from almost-sure convergence of the original series"
    status := "unchecked"
  },
  {
    leafId := "K3S.L020"
    packageId := "K3S.P6"
    goal := "derive expectation-series convergence from almost-sure convergence"
    status := "unchecked"
  },
  {
    leafId := "K3S.L021"
    packageId := "K3S.P6"
    goal := "derive variance summability of truncations from almost-sure convergence"
    status := "unchecked"
  },
  {
    leafId := "K3S.L022"
    packageId := "K3S.P1/K3S.P6"
    goal := "prove cutoff-independence for positive truncation radii"
    status := "unchecked"
  },
  {
    leafId := "K3S.L023"
    packageId := "K3S.P1/K3S.P6"
    goal := "reconcile fixed-cutoff, some-cutoff, and every-cutoff theorem statement variants"
    status := "unchecked"
  },
  {
    leafId := "K3S.L024"
    packageId := "K3S.P8"
    goal := "package the terminal theorem as statementShape_from_local_proof or statementShape_from_upstream"
    status := "unchecked"
  }
]

/-- Public package ids requested by child `S1-M-287-C003`. -/
def theoremTreePackageIds : List String :=
  theoremTreePackages.map (fun row => row.packageId)

/-- Leaf ids preserved by child `S1-M-287-C003`. -/
def uncheckedLeafIds : List String :=
  uncheckedLeafLedger.map (fun row => row.leafId)

/-- The package split contains exactly `K3S.P1` through `K3S.P8`. -/
theorem theoremTreePackages_length :
    theoremTreePackages.length = 8 :=
  rfl

/-- The leaf ledger preserves exactly `K3S.L001` through `K3S.L024`. -/
theorem uncheckedLeafLedger_length :
    uncheckedLeafLedger.length = 24 :=
  rfl

end K3S

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check statementShape_iff
#check truncationFunction
#check centeredTruncation
#check centeredTruncationFunction
#check measurable_truncationFunction
#check measurable_truncation
#check measurable_truncation_X
#check measurableSet_largeJumpEvent
#check measurable_centeredTruncationFunction
#check measurable_centeredTruncation
#check independent_truncation
#check independent_centeredTruncation
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.comp
#check ProbabilityTheory.IndepFun.variance_sum
#check MeasureTheory.measure_limsup_atTop_eq_zero
#check MeasureTheory.ae_eventually_notMem
#check MeasureTheory.ae_mem_limsup_atTop_iff
#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.variance
#check MeasureTheory.Integrable
#check MeasureTheory.MemLp
#check Filter.Tendsto
#check Summable
#check ofReal_real_largeJump_measure
#check largeJump_real_summable_to_ennreal
#check ae_eventually_not_largeJump
#check ae_eventually_not_largeJump_of_real_summable
#check mathlibAnchorRevision
#check publicMathlibAnchorTable
#check publicMathlibAnchorNames
#check publicMathlibAnchorTable_length
#check c006ExternalLeanAuditRows
#check c006ExternalLeanAuditSearchTerms
#check c006ExternalLeanAuditRows_length
#check c006ExternalTerminalProofFound_eq_false
#check c006RepoLocalIntegrationDebtRetainedInCompletedState_eq_false
#check K3S.theoremTreePackages
#check K3S.theoremTreePackageIds
#check K3S.theoremTreePackages_length
#check K3S.uncheckedLeafLedger
#check K3S.uncheckedLeafIds
#check K3S.uncheckedLeafLedger_length

end S1_M_287
end Stage1
end AwesomeTheorems
