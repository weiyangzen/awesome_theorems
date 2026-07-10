import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.Probability.Moments.SubGaussian

/-!
# S1-M-276 / THM-M-0996: Gaussian concentration / isoperimetric inequality

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Gaussian measure isoperimetric inequality.  The intended theorem says that
metric enlargements of measurable sets under a Gaussian measure satisfy the
Gaussian isoperimetric profile bound.

The pinned mathlib snapshot has Gaussian measures in Banach spaces, real
Gaussian laws, Fernique integrability, Gaussian-process infrastructure, and
sub-Gaussian tail inequalities.  It does not expose a terminal theorem named
for Gaussian isoperimetry, Ehrhard/Borell isoperimetry, or Gaussian
concentration for metric neighborhoods.  Accordingly, the declarations below
freeze the normalized statement shape and add checked wrappers around current
mathlib anchors.  No terminal Gaussian-isoperimetric proof is claimed here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set Real
open scoped ENNReal NNReal Topology BigOperators

namespace AwesomeTheorems.Stage1.S1_M_276

universe u

/-- The canonical standard Gaussian measure for the THM-M-0996 profile API. -/
def standardGaussianMeasure : Measure ℝ :=
  gaussianReal 0 (1 : ℝ≥0)

/--
The canonical standard Gaussian profile used by the Stage1 statement boundary.

This is the normal distribution function `Φ(a) = P[Z ≤ a]`, represented directly
as the `ℝ≥0∞`-valued measure of the half-line `(-∞, a]`.  This codomain matches
mathlib's `Measure` API and avoids adding coercion side conditions to the
isoperimetric profile inequality.
-/
def standardGaussianProfile (a : ℝ) : ℝ≥0∞ :=
  standardGaussianMeasure (Set.Iic a)

/--
Real-valued projection of `standardGaussianProfile` for later probability-real
corollaries.  The canonical Stage1 profile inequality remains
`ℝ≥0∞`-valued; this definition is only a bridge for downstream statements that
want real probabilities.
-/
def standardGaussianProfileReal (a : ℝ) : ℝ :=
  (standardGaussianProfile a).toReal

/--
Parameter convention for the THM-M-0996 Gaussian profile.

The profile is indexed by the real halfspace threshold `a` itself: the target
inequality has the form `gamma s ≥ Φ(a) → gamma (s_r) ≥ Φ(a + r)`.  No inverse
CDF/quantile function is introduced in this Stage1 artifact.
-/
def standardGaussianProfileParameterConvention : String :=
  "Use the direct halfspace threshold a: Phi(a) = gaussianReal 0 1 (Iic a), and shift a to a + r."

/-- Checked unfolding of the canonical standard Gaussian profile. -/
theorem standardGaussianProfile_eq (a : ℝ) :
    standardGaussianProfile a = gaussianReal 0 (1 : ℝ≥0) (Set.Iic a) :=
  rfl

/-- Half-lines used by the canonical profile are Borel measurable. -/
theorem measurableSet_standardGaussianProfile_halfline (a : ℝ) :
    MeasurableSet (Set.Iic a) :=
  measurableSet_Iic

/-- The canonical standard Gaussian profile is monotone in its threshold. -/
theorem standardGaussianProfile_mono : Monotone standardGaussianProfile := by
  intro a b hab
  exact measure_mono (Set.Iic_subset_Iic.mpr hab)

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- Closed metric enlargement of a set by radius `r`. -/
def closedMetricEnlargement (r : ℝ) (s : Set E) : Set E :=
  {x | ∃ y ∈ s, dist x y ≤ r}

/--
The one-sided Gaussian isoperimetric profile bound for a fixed Gaussian
measure/profile pair.

If `gamma s` is at least the profile value at `a`, then the `r`-enlargement of
`s` has measure at least the profile value at `a + r`.
-/
def GaussianIsoperimetricBound (gamma : Measure E) (profile : ℝ → ℝ≥0∞) : Prop :=
  ∀ {a r : ℝ} {s : Set E},
    0 ≤ r →
      MeasurableSet s →
        profile a ≤ gamma s →
          profile (a + r) ≤ gamma (closedMetricEnlargement r s)

/--
Abstract Stage1 model for the Gaussian isoperimetric inequality.

The concrete Gaussian profile is kept as a supplied function.  A later terminal
formalization should replace it by the standard normal distribution function
and should prove the `gaussian_isoperimetric` field from a local proof body or a
pinned external Lean dependency.
-/
structure GaussianIsoperimetricModel where
  gamma : Measure E
  isGaussian : IsGaussian gamma
  profile : ℝ → ℝ≥0∞
  profile_mono : Monotone profile
  enlargement_measurable :
    ∀ {r : ℝ} {s : Set E}, 0 ≤ r → MeasurableSet s →
      MeasurableSet (closedMetricEnlargement (E := E) r s)
  gaussian_isoperimetric :
    GaussianIsoperimetricBound (E := E) gamma profile

attribute [instance] GaussianIsoperimetricModel.isGaussian

/-- The formal conclusion expected from the Gaussian isoperimetric theorem. -/
def GaussianIsoperimetricConclusion (M : GaussianIsoperimetricModel (E := E)) : Prop :=
  GaussianIsoperimetricBound (E := E) M.gamma M.profile

/--
Public statement-normalization note for THM-M-0996.

`StatementShape` is the current repo-local Lean boundary: it normalizes the
expected Gaussian-concentration/isoperimetric conclusion after a
`GaussianIsoperimetricModel` has already supplied a Gaussian measure, a profile,
measurable metric enlargements, and the terminal `gaussian_isoperimetric` field.
This is a statement-shape boundary only.  It is not a proof of Gaussian
isoperimetry, Borell/Ehrhard isoperimetry, or Gaussian concentration for metric
neighborhoods.
-/
def statementNormalizationNote : String :=
  "StatementShape is a statement-shape boundary for THM-M-0996, not a proof of Gaussian isoperimetry."

/--
Stage1 normalized statement shape for THM-M-0996.

For every explicitly declared Gaussian-isoperimetric model, the declared
terminal field implies the expected Gaussian profile bound.  This records only
the statement shape and projection boundary; it does not prove Gaussian
isoperimetry itself.
-/
def StatementShape : Prop :=
  ∀ M : GaussianIsoperimetricModel (E := E), GaussianIsoperimetricConclusion M

omit [BorelSpace E] in
/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ M : GaussianIsoperimetricModel (E := E),
      GaussianIsoperimetricConclusion M) :
    StatementShape (E := E) :=
  h

omit [BorelSpace E] in
/-- The statement shape is obtained by projecting the model's terminal field. -/
theorem statementShape_from_model_fields : StatementShape (E := E) := by
  intro M
  exact M.gaussian_isoperimetric

omit [BorelSpace E] in
/-- A Gaussian measure in the model is a probability measure by mathlib. -/
theorem model_isProbabilityMeasure (M : GaussianIsoperimetricModel (E := E)) :
    IsProbabilityMeasure M.gamma := by
  infer_instance

omit [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- The original set is contained in every nonnegative closed enlargement. -/
theorem subset_closedMetricEnlargement_of_nonneg {r : ℝ} {s : Set E} (hr : 0 ≤ r) :
    s ⊆ closedMetricEnlargement (E := E) r s := by
  intro x hx
  exact ⟨x, hx, by simpa using hr⟩

omit [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- Closed metric enlargement as the union of closed balls centered on the source set. -/
theorem closedMetricEnlargement_eq_iUnion_closedBall (r : ℝ) (s : Set E) :
    closedMetricEnlargement (E := E) r s = ⋃ y : s, Metric.closedBall (y : E) r := by
  ext x
  constructor
  · rintro ⟨y, hy, hdist⟩
    exact Set.mem_iUnion.2 ⟨⟨y, hy⟩, by simpa [Metric.mem_closedBall] using hdist⟩
  · intro hx
    rcases Set.mem_iUnion.1 hx with ⟨y, hyx⟩
    exact ⟨y, y.property, by simpa [Metric.mem_closedBall] using hyx⟩

omit [NormedSpace ℝ E] in
/--
Closed metric enlargements of countable sets are Borel measurable.

This is a checked local base case for the enlargement API.  The arbitrary
measurable-set case remains deliberately model-provided above: for an
existential enlargement, Borel measurability is a genuine projection/analytic
set issue and needs the final ambient regularity hypotheses before it should be
claimed as a theorem.
-/
theorem measurableSet_closedMetricEnlargement_of_countable {r : ℝ} {s : Set E}
    (hs : s.Countable) :
    MeasurableSet (closedMetricEnlargement (E := E) r s) := by
  rw [closedMetricEnlargement_eq_iUnion_closedBall]
  letI : Countable s := hs.to_subtype
  exact MeasurableSet.iUnion fun y => measurableSet_closedBall

omit [BorelSpace E] in
/-- Checked wrapper: the model records measurability of nonnegative enlargements. -/
theorem model_enlargement_measurable (M : GaussianIsoperimetricModel (E := E))
    {r : ℝ} {s : Set E} (hr : 0 ≤ r) (hs : MeasurableSet s) :
    MeasurableSet (closedMetricEnlargement (E := E) r s) :=
  M.enlargement_measurable hr hs

omit [BorelSpace E] in
/-- Checked wrapper: project the normalized Gaussian profile inequality. -/
theorem model_profile_bound (M : GaussianIsoperimetricModel (E := E))
    {a r : ℝ} {s : Set E} (hr : 0 ≤ r) (hs : MeasurableSet s)
    (hprofile : M.profile a ≤ M.gamma s) :
    M.profile (a + r) ≤ M.gamma (closedMetricEnlargement (E := E) r s) :=
  M.gaussian_isoperimetric hr hs hprofile

/-- Mapping a Gaussian measure by a continuous linear map is Gaussian in mathlib. -/
theorem isGaussian_map_continuousLinearMap
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    [MeasurableSpace F] [BorelSpace F]
    {mu : Measure E} [IsGaussian mu] (L : E →L[ℝ] F) :
    IsGaussian (mu.map L) := by
  infer_instance

/-- Checked mathlib anchor: continuous linear functionals are integrable under Gaussian measures. -/
theorem gaussian_dual_integrable (mu : Measure E) [IsGaussian mu] (L : StrongDual ℝ E) :
    Integrable L mu :=
  IsGaussian.integrable_dual mu L

/-- Checked Fernique anchor for Gaussian measures on normed spaces. -/
theorem gaussian_measure_fernique
    [SecondCountableTopology E] [CompleteSpace E] (mu : Measure E) [IsGaussian mu] :
    ∃ C, 0 < C ∧ Integrable (fun x => Real.exp (C * ‖x‖ ^ 2)) mu :=
  IsGaussian.exists_integrable_exp_sq mu

/-- Checked sub-Gaussian anchor: Chernoff right-tail inequality from mathlib. -/
theorem subgaussian_right_tail_bound
    {Omega : Type*} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → ℝ} {c : ℝ≥0} (hX : HasSubgaussianMGF X c mu)
    {epsilon : ℝ} (hepsilon : 0 ≤ epsilon) :
    mu.real {omega | epsilon ≤ X omega} ≤
      Real.exp (-epsilon ^ 2 / (2 * c)) :=
  hX.measure_ge_le hepsilon

/-- Checked sub-Gaussian anchor: all finite `L^p` controls from the mgf hypothesis. -/
theorem subgaussian_memLp
    {Omega : Type*} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → ℝ} {c : ℝ≥0} (hX : HasSubgaussianMGF X c mu) (p : ℝ≥0) :
    MemLp X p mu :=
  hX.memLp p

/-- Checked real Gaussian-law anchor: `gaussianReal` is Gaussian in mathlib. -/
theorem gaussianReal_isGaussian (m : ℝ) (v : ℝ≥0) :
    IsGaussian (gaussianReal m v) := by
  infer_instance

/-- Checked real Gaussian-law anchor: `gaussianReal` is a probability measure in mathlib. -/
theorem gaussianReal_isProbabilityMeasure (m : ℝ) (v : ℝ≥0) :
    IsProbabilityMeasure (gaussianReal m v) := by
  infer_instance

/-- Checked Hoeffding anchor for independent sub-Gaussian finite sums. -/
theorem hoeffding_iIndepFun_tail_bound
    {Omega ι : Type*} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : ι → Omega → ℝ} (h_indep : iIndepFun X mu) {c : ι → ℝ≥0}
    {s : Finset ι} (h_subG : ∀ i ∈ s, HasSubgaussianMGF (X i) (c i) mu)
    {epsilon : ℝ} (hepsilon : 0 ≤ epsilon) :
    mu.real {omega | epsilon ≤ ∑ i ∈ s, X i omega} ≤
      Real.exp (-epsilon ^ 2 / (2 * ∑ i ∈ s, c i)) :=
  ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun h_indep h_subG hepsilon

/-- Checked Hoeffding-lemma anchor for bounded random variables. -/
theorem hoeffding_bounded_subgaussian_anchor
    {Omega : Type*} [MeasurableSpace Omega] {mu : Measure Omega}
    [IsProbabilityMeasure mu] {X : Omega → ℝ} {a b : ℝ}
    (hm : AEMeasurable X mu) (hb : ∀ᵐ omega ∂mu, X omega ∈ Set.Icc a b) :
    HasSubgaussianMGF (fun omega => X omega - mu[X]) ((‖b - a‖₊ / 2) ^ 2) mu :=
  ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc hm hb

/-- Checked Azuma-Hoeffding anchor for conditionally sub-Gaussian finite sums. -/
theorem azuma_hoeffding_tail_bound
    {Omega : Type*} [mOmega : MeasurableSpace Omega] [StandardBorelSpace Omega]
    {mu : Measure Omega} [IsZeroOrProbabilityMeasure mu]
    {Y : ℕ → Omega → ℝ} {cY : ℕ → ℝ≥0} {filtration : Filtration ℕ mOmega}
    (h_adapted : StronglyAdapted filtration Y)
    (h0 : HasSubgaussianMGF (Y 0) (cY 0) mu) (n : ℕ)
    (h_subG : ∀ i < n - 1,
      HasCondSubgaussianMGF (filtration i) (filtration.le i) (Y (i + 1)) (cY (i + 1)) mu)
    {epsilon : ℝ} (hepsilon : 0 ≤ epsilon) :
    mu.real {omega | epsilon ≤ ∑ i ∈ Finset.range n, Y i omega}
      ≤ Real.exp (-epsilon ^ 2 / (2 * ∑ i ∈ Finset.range n, cY i)) :=
  ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF h_adapted h0 n h_subG hepsilon

/-- Pinned mathlib revision used for the THM-M-0996 mathlib-anchor audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Distributions.Gaussian.Basic",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.Probability.Distributions.Gaussian.Fernique",
  "Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.Moments.SubGaussian",
  "Mathlib.MeasureTheory.Integral.Layercake",
  "Mathlib.MeasureTheory.Integral.MeanInequalities"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.IsGaussian",
  "ProbabilityTheory.IsGaussian.map_eq_gaussianReal",
  "ProbabilityTheory.isGaussian_map",
  "ProbabilityTheory.IsGaussian.integrable_dual",
  "ProbabilityTheory.IsGaussian.exists_integrable_exp_sq",
  "ProbabilityTheory.gaussianReal",
  "ProbabilityTheory.isGaussian_gaussianReal",
  "ProbabilityTheory.instIsProbabilityMeasureGaussianReal",
  "ProbabilityTheory.HasSubgaussianMGF",
  "ProbabilityTheory.HasSubgaussianMGF.measure_ge_le",
  "ProbabilityTheory.HasSubgaussianMGF.memLp",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun",
  "ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero",
  "ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc",
  "ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF",
  "ProbabilityTheory.measure_sum_ge_le_of_HasCondSubgaussianMGF"
]

/--
Search terms that did not locate a terminal Gaussian-isoperimetric theorem in
the pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "GaussianIsoperimetric",
  "gaussian isoperimetric",
  "Ehrhard",
  "Borell",
  "Gaussian concentration",
  "metric enlargement",
  "closedMetricEnlargement"
]

/--
External Lean 4 anchor found during the THM-M-0996 audit.

This is anchor-only metadata.  It is not imported by this repository, and the
theorems below formalize finite-dimensional Gaussian Lipschitz concentration,
not the Borell/Ehrhard Gaussian isoperimetric profile theorem for metric
enlargements.
-/
def externalLeanAnchorSources : List String := [
  "YuanheZ/lean-stat-learning-theory@4aaea15591360ccfffa1befdf0e7162f5af17f60",
  "SLT/GaussianLipConcen.lean: GaussianLipConcen.gaussian_lipschitz_concentration_one_sided",
  "SLT/GaussianLipConcen.lean: GaussianLipConcen.gaussian_lipschitz_concentration"
]

/-- Lake/toolchain compatibility status for the external anchor audit. -/
def externalLeanAnchorLakeCompatibility : List String := [
  "external lean-toolchain: leanprover/lean4:v4.27.0-rc1",
  "external mathlib manifest revision: d68c4dc09f5e000d3c968adae8def120a0758729",
  "repo lean-toolchain: leanprover/lean4:v4.29.0",
  "repo mathlib manifest revision: 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "not Lake-compatible with this repo without a port/pin/import check"
]

/--
Repo-local integration gate for the external audit.

No completed THM-M-0996 state may cite the external concentration theorem as a
repo-local proof until it is ported or pinned and imported into this Lake
project.  The current repo-local theorem remains a statement-shape boundary.
-/
def externalLeanAnchorIntegrationStatus : String :=
  "external_upstream_anchor_only; integration blocked by Lean/mathlib version mismatch and narrower theorem shape"

/--
Integration-gate diagnosis for THM-M-0996.

This list is checked repo-local metadata, not theorem completion evidence.  It
records that no terminal external Borell/Ehrhard Gaussian-isoperimetric Lean
proof has been found and integrated into this Lake project.
-/
def integrationGateDiagnosis : List String := [
  "gate=open",
  "terminal_external_proof_found=false",
  "repo_local_import_checked=false",
  "related_external_anchor=finite-dimensional Gaussian Lipschitz concentration only",
  "blocker=theorem-shape mismatch plus Lean/mathlib version mismatch",
  "current_machine_status=not_repo_local_closed/formalization_debt"
]

/--
Repo-local completion gate for THM-M-0996.

The parent theorem must remain open until this gate is replaced by either a
checked local proof body or a pinned/imported/checked upstream theorem matching
the final Gaussian isoperimetric profile/enlargement statement.
-/
def repoLocalIntegrationDebtGate : String :=
  "No completed THM-M-0996 state is claimed; anchor-only external evidence is not repo-local closure."

/--
Proof-tree package split for THM-M-0996.

These are integration-ready package names for the public theorem tree.  They
are checked metadata only: the isoperimetric core and concentration corollaries
remain open until supplied by a local proof body or a pinned upstream import.
-/
def proofTreePackages : List String := [
  "PT-0996-01.statement-normalization",
  "PT-0996-02.mathlib-object-model",
  "PT-0996-03.profile-enlargement-api",
  "PT-0996-04.isoperimetric-core",
  "PT-0996-05.concentration-corollaries",
  "PT-0996-06.repo-local-closure-gate"
]

/-- `<=100` leaf ledger for the statement-normalization proof-tree package. -/
def statementNormalizationLeafLedger : List String := [
  "SN-01.checked: define GaussianIsoperimetricBound as the target profile/enlargement proposition; local proof is definitional, <=100 steps",
  "SN-02.checked: define GaussianIsoperimetricModel with gamma, IsGaussian, profile, monotonicity, enlargement measurability, and terminal field; local proof is structural, <=100 steps",
  "SN-03.checked: project StatementShape from model.gaussian_isoperimetric; theorem statementShape_from_model_fields validates locally, <=100 steps",
  "SN-04.open: public blueprint merge must keep this package described as statement-shape only, not terminal Gaussian isoperimetry"
]

/-- `<=100` leaf ledger for the mathlib object-model proof-tree package. -/
def mathlibObjectModelLeafLedger : List String := [
  "MO-01.checked: gaussianReal_isGaussian wrapper validates the standard real Gaussian law object, <=100 steps",
  "MO-02.checked: gaussianReal_isProbabilityMeasure wrapper validates probability-measure status, <=100 steps",
  "MO-03.checked: gaussian_dual_integrable and gaussian_measure_fernique wrap current Gaussian Banach-space anchors, each <=100 steps",
  "MO-04.checked: subgaussian_right_tail_bound, Hoeffding, bounded-variable, and Azuma-Hoeffding wrappers validate concentration substrate anchors, each <=100 steps",
  "MO-05.open: no mathlib terminal Borell/Ehrhard Gaussian-isoperimetric theorem was found at the pinned revision"
]

/-- `<=100` leaf ledger for the profile/enlargement API proof-tree package. -/
def profileEnlargementLeafLedger : List String := [
  "PE-01.checked: standardGaussianProfile fixes Phi(a) as gaussianReal 0 1 (Iic a) with ENNReal codomain, <=100 steps",
  "PE-02.checked: standardGaussianProfile_eq and measurableSet_standardGaussianProfile_halfline validate profile unfolding and halfline measurability, each <=100 steps",
  "PE-03.checked: standardGaussianProfile_mono validates monotonicity by measure_mono, <=100 steps",
  "PE-04.checked: closedMetricEnlargement, subset_closedMetricEnlargement_of_nonneg, and closedMetricEnlargement_eq_iUnion_closedBall validate the local enlargement shape, each <=100 steps",
  "PE-05.checked-partial: measurableSet_closedMetricEnlargement_of_countable gives a countable-set Borel base case, <=100 steps",
  "PE-06.open: arbitrary measurable closed metric enlargement remains model-provided until final ambient regularity hypotheses are selected"
]

/-- `<=100` leaf ledger for the isoperimetric-core proof-tree package. -/
def isoperimetricCoreLeafLedger : List String := [
  "IC-01.open: choose the terminal Borell/Ehrhard proof route for GaussianIsoperimetricBound",
  "IC-02.open: formalize or import the halfspace extremal statement for the selected Gaussian profile convention",
  "IC-03.open: bridge the halfspace extremal statement to closedMetricEnlargement under the final ambient hypotheses",
  "IC-04.open: split any analytic-set/regularity branch into leaves whose local proof scripts are each <=100 steps",
  "IC-05.open: replace the GaussianIsoperimetricModel terminal field with a repo-local proof body or pinned upstream theorem when available"
]

/-- `<=100` leaf ledger for the concentration-corollaries proof-tree package. -/
def concentrationCorollaryLeafLedger : List String := [
  "CC-01.open: derive one-sided set-enlargement concentration from GaussianIsoperimetricBound and the selected profile normalization",
  "CC-02.open: derive Lipschitz-function concentration from set-enlargement concentration via sublevel-set enlargement",
  "CC-03.open: decide whether finite-dimensional Gaussian Lipschitz concentration from the external anchor is auxiliary or separately ported",
  "CC-04.open: keep sub-Gaussian Hoeffding/Azuma wrappers as substrate anchors only unless the public theorem target is explicitly changed",
  "CC-05.open: split each corollary proof into independent <=100-step Lean leaves before any public completion checkbox is checked"
]

/-- `<=100` leaf ledger for the repo-local closure-gate proof-tree package. -/
def repoLocalClosureGateLeafLedger : List String := [
  "RG-01.checked: externalLeanAnchorIntegrationStatus records the external concentration source as anchor-only, <=100 steps",
  "RG-02.checked: integrationGateDiagnosis records terminal_external_proof_found=false and repo_local_import_checked=false, <=100 steps",
  "RG-03.checked: repoLocalIntegrationDebtGate forbids completed THM-M-0996 state from relying on anchor-only evidence, <=100 steps",
  "RG-04.open: public blueprint/todo/README surfaces must be merged serially before any completion state is claimed",
  "RG-05.open: final gate requires local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned validation for the terminal theorem"
]

/--
Top-level theorem-tree ledger for THM-M-0996.

Each package is independently budgeted by one of the `*LeafLedger`
declarations above.  This declaration intentionally records open leaves for the
terminal isoperimetric core and concentration corollaries; it is not completion
evidence.
-/
def theoremTreeLeafLedgers : List (String × List String) := [
  ("PT-0996-01.statement-normalization", statementNormalizationLeafLedger),
  ("PT-0996-02.mathlib-object-model", mathlibObjectModelLeafLedger),
  ("PT-0996-03.profile-enlargement-api", profileEnlargementLeafLedger),
  ("PT-0996-04.isoperimetric-core", isoperimetricCoreLeafLedger),
  ("PT-0996-05.concentration-corollaries", concentrationCorollaryLeafLedger),
  ("PT-0996-06.repo-local-closure-gate", repoLocalClosureGateLeafLedger)
]

/-- Status note for the THM-M-0996 proof-tree split. -/
def proofTreeSplitStatus : String :=
  "proof-tree split recorded; terminal Gaussian isoperimetry remains open formalization_debt"

end AwesomeTheorems.Stage1.S1_M_276
