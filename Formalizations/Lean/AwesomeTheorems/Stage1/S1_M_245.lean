import Mathlib.Analysis.InnerProductSpace.MeanErgodic
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.Probability.StrongLaw

/-!
# S1-M-245 / THM-M-1053: Ergodic theorem

This Stage1 artifact records a conservative Lean 4 boundary for the
pointwise ergodic theorem slogan "time average equals space average".

The pinned mathlib snapshot has a concrete API for measure-preserving and
ergodic maps, invariant functions under an ergodic map, the von Neumann mean
ergodic theorem in Hilbert spaces, and strong laws of large numbers.  A
terminal Birkhoff pointwise ergodic theorem for integrable observables was not
found in the local dependency closure.  A public external Lean project contains
pointwise Birkhoff theorem candidates, but it is not pinned or imported by this
repository and uses a different Lean/mathlib dependency surface, so the main
theorem is kept as a statement shape rather than a claimed repo-local proof.
-/

noncomputable section

open Filter Finset Function MeasureTheory
open scoped Topology MeasureTheory ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_245

universe u v

def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

structure MathlibAnchorRecord where
  declaration : String
  moduleName : String
  checkedBy : String
  role : String

/--
Decision space for the Stage1 terminal theorem target.

The public slogan "time average equals space average" is normalized below to
the Birkhoff pointwise ergodic theorem.  The von Neumann mean ergodic theorem
and strong-law interfaces remain checked adjacent anchors, not the terminal
statement for `THM-M-1053`.
-/
inductive TerminalTheoremKind where
  | birkhoffPointwise
  | vonNeumannMean
  | stagedFamily
  deriving DecidableEq, Repr

/-- Stage1 decision: use the Birkhoff pointwise form as the canonical target. -/
def terminalTheoremDecision : TerminalTheoremKind :=
  .birkhoffPointwise

/-- Checked marker for the child decision task. -/
theorem terminalTheoremDecision_is_birkhoff :
    terminalTheoremDecision = TerminalTheoremKind.birkhoffPointwise :=
  rfl

/--
The canonical Lean declaration name carrying the source slogan
"time average equals space average" for this Stage1 slot.
-/
def canonicalSloganStatementName : String :=
  "AwesomeTheorems.Stage1.S1_M_245.StatementShape"

/-- Data package for the classical real-valued Birkhoff ergodic theorem. -/
structure BirkhoffErgodicProblem (Ω : Type u) [MeasurableSpace Ω] : Type u where
  μ : Measure Ω
  T : Ω → Ω
  observable : Ω → ℝ
  observable_integrable : Integrable observable μ
  transformation_ergodic : Ergodic T μ

/-- The `n`-th orbit/time average of an observable along a transformation. -/
def timeAverage {Ω : Type u} [MeasurableSpace Ω] (P : BirkhoffErgodicProblem Ω)
    (n : ℕ) (ω : Ω) : ℝ :=
  (∑ k ∈ Finset.range n, P.observable ((P.T^[k]) ω)) / (n : ℝ)

/-- The space average, i.e. the integral of the observable over the invariant measure. -/
def spaceAverage {Ω : Type u} [MeasurableSpace Ω] (P : BirkhoffErgodicProblem Ω) : ℝ :=
  ∫ ω, P.observable ω ∂P.μ

/--
Expected terminal conclusion of the pointwise ergodic theorem for an ergodic
measure-preserving transformation.

This is a statement boundary only.  The current repo-local Lean closure does
not contain a proof that these time averages converge almost everywhere to the
space average for every integrable observable.
-/
def BirkhoffErgodicConclusion {Ω : Type u} [MeasurableSpace Ω]
    (P : BirkhoffErgodicProblem Ω) : Prop :=
  ∀ᵐ ω ∂P.μ, Tendsto (fun n : ℕ => timeAverage P n ω) atTop (𝓝 (spaceAverage P))

/--
Stage1 normalized statement-shape candidate for the ergodic theorem:
for every measurable space, ergodic measure-preserving transformation, and
integrable real-valued observable, time averages converge almost everywhere to
the space average.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ P : BirkhoffErgodicProblem Ω,
      BirkhoffErgodicConclusion P

/-- The statement-shape definition unfolds to the normalized Birkhoff form. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ P : BirkhoffErgodicProblem Ω,
          BirkhoffErgodicConclusion P :=
  Iff.rfl

/--
Terminal-wrapper interface for a future repo-local or pinned-upstream proof of
the normalized statement shape.

This theorem does not prove the ergodic theorem.  It only records the exact
checked projection that an eventual proof of `StatementShape` must provide:
the conclusion is definitionally the canonical `BirkhoffErgodicConclusion`.
-/
theorem statementShape_to_birkhoffErgodicConclusion
    (h : StatementShape.{u}) (Ω : Type u) [MeasurableSpace Ω]
    (P : BirkhoffErgodicProblem Ω) :
    BirkhoffErgodicConclusion P :=
  h Ω P

/--
Problem-level wrapper endpoint for a future terminal theorem.

The conclusion is exactly `BirkhoffErgodicConclusion P`; the hypothesis is the
future terminal proof obligation for this specific problem instance.
-/
theorem birkhoffErgodicConclusion_wrapper
    {Ω : Type u} [MeasurableSpace Ω] (P : BirkhoffErgodicProblem Ω)
    (h : BirkhoffErgodicConclusion P) :
    BirkhoffErgodicConclusion P :=
  h

/-- The ergodic hypothesis exposes a checked mathlib `MeasurePreserving` anchor. -/
theorem transformation_measurePreserving {Ω : Type u} [MeasurableSpace Ω]
    (P : BirkhoffErgodicProblem Ω) :
    MeasurePreserving P.T P.μ P.μ :=
  P.transformation_ergodic.toMeasurePreserving

/-- The ergodic transformation is a.e. measurable with respect to its measure. -/
theorem transformation_aemeasurable {Ω : Type u} [MeasurableSpace Ω]
    (P : BirkhoffErgodicProblem Ω) :
    AEMeasurable P.T P.μ :=
  P.transformation_ergodic.toMeasurePreserving.aemeasurable

/-- The observable field exposes the checked mathlib `Integrable` hypothesis. -/
theorem observable_integrable {Ω : Type u} [MeasurableSpace Ω]
    (P : BirkhoffErgodicProblem Ω) :
    Integrable P.observable P.μ :=
  P.observable_integrable

/--
Checked mathlib wrapper: an a.e. invariant, a.e. strongly measurable function
under an ergodic map is a.e. constant.

This is an ergodic-function anchor, not the Birkhoff pointwise theorem.
-/
theorem ergodic_ae_eq_const_of_ae_eq_comp_ae_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} {T : Ω → Ω}
    {X : Type v} [Nonempty X] [MeasurableSpace X] [MeasurableSpace.CountablySeparated X]
    {g : Ω → X}
    (hT : Ergodic T μ) (hg : NullMeasurable g μ)
    (hinv : g ∘ T =ᵐ[μ] g) :
    ∃ c, g =ᵐ[μ] const Ω c :=
  hT.ae_eq_const_of_ae_eq_comp₀ hg hinv

/--
Checked mathlib wrapper: von Neumann mean ergodic theorem in a Hilbert space.

This supplies a norm-convergence mean-ergodic anchor for contractions, but it
does not itself close the pointwise Birkhoff theorem above.
-/
theorem meanErgodic_hilbert_mathlib_wrapper
    {𝕜 : Type u} {E : Type v} [RCLike 𝕜] [NormedAddCommGroup E]
    [InnerProductSpace 𝕜 E] [CompleteSpace E]
    (T : E →L[𝕜] E) (hT : ‖T‖ ≤ 1) (x : E) :
    Tendsto (birkhoffAverage 𝕜 T _root_.id · x) atTop
      (𝓝 <| (LinearMap.eqLocus T 1).orthogonalProjection x) :=
  ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection T hT x

/--
Checked mathlib wrapper: strong law of large numbers for Banach-valued
independent identically distributed random variables.

This validates a stochastic-process averaging interface adjacent to the Stage1
scope, but its hypotheses are iid independence rather than ergodic dynamics.
-/
theorem strongLaw_ae_mathlib_wrapper
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] {μ : Measure Ω}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (X : ℕ → Ω → E) (hint : Integrable (X 0) μ)
    (hindep : Pairwise ((· ⟂ᵢ[μ] ·) on X))
    (hident : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ) :
    ∀ᵐ ω ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, X i ω))
        atTop (𝓝 μ[X 0]) :=
  ProbabilityTheory.strong_law_ae X hint hindep hident

/-- Checked mathlib anchor: identically distributed integrable functions have equal integrals. -/
theorem identDistrib_integral_eq_wrapper
    {α : Type u} {β : Type v} [MeasurableSpace α] [MeasurableSpace β]
    {μ : Measure α} {ν : Measure β} {f : α → ℝ} {g : β → ℝ}
    (h : ProbabilityTheory.IdentDistrib f g μ ν) :
    ∫ x, f x ∂μ = ∫ y, g y ∂ν :=
  h.integral_eq

/--
Integration-ready anchor table for the public Stage1 backfill row at
`pinnedMathlibRevision`.

Rows marked by a wrapper are locally checked in this file.  Structure or
hypothesis rows are checked by using them in the statement shape and wrappers.
None of these rows is a terminal pointwise Birkhoff proof.
-/
def publicMathlibAnchorTable : List MathlibAnchorRecord := [
  {
    declaration := "MeasureTheory.MeasurePreserving",
    moduleName := "Mathlib.Dynamics.Ergodic.MeasurePreserving",
    checkedBy := "transformation_measurePreserving",
    role := "measure-preserving transformation interface exposed by Ergodic"
  },
  {
    declaration := "Ergodic",
    moduleName := "Mathlib.Dynamics.Ergodic.Ergodic",
    checkedBy := "BirkhoffErgodicProblem.transformation_ergodic",
    role := "ergodic map hypothesis used by the normalized Birkhoff statement shape"
  },
  {
    declaration := "Ergodic.ae_eq_const_of_ae_eq_comp₀",
    moduleName := "Mathlib.Dynamics.Ergodic.Function",
    checkedBy := "ergodic_ae_eq_const_of_ae_eq_comp_ae_wrapper",
    role := "a.e. invariant functions under an ergodic map are a.e. constant"
  },
  {
    declaration := "ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
    moduleName := "Mathlib.Analysis.InnerProductSpace.MeanErgodic",
    checkedBy := "meanErgodic_hilbert_mathlib_wrapper",
    role := "von Neumann mean ergodic theorem anchor, not pointwise Birkhoff"
  },
  {
    declaration := "ProbabilityTheory.strong_law_ae",
    moduleName := "Mathlib.Probability.StrongLaw",
    checkedBy := "strongLaw_ae_mathlib_wrapper",
    role := "iid strong law averaging interface adjacent to ergodic averages"
  },
  {
    declaration := "ProbabilityTheory.IdentDistrib.integral_eq",
    moduleName := "Mathlib.Probability.IdentDistrib",
    checkedBy := "identDistrib_integral_eq_wrapper",
    role := "identical distributions have equal integrals"
  }
]

/-- mathlib modules checked while locating repo-local ergodic-theorem anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.Function",
  "Mathlib.Dynamics.Ergodic.AddCircleAdd",
  "Mathlib.Analysis.InnerProductSpace.MeanErgodic",
  "Mathlib.Dynamics.BirkhoffSum.NormedSpace",
  "Mathlib.Probability.StrongLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Martingale.Convergence"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MeasurePreserving",
  "Ergodic",
  "PreErgodic",
  "QuasiErgodic",
  "Ergodic.ae_eq_const_of_ae_eq_comp₀",
  "ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
  "ProbabilityTheory.strong_law_ae",
  "ProbabilityTheory.strong_law_Lp",
  "ProbabilityTheory.IdentDistrib.integral_eq",
  "MeasureTheory.Integrable.tendsto_ae_condExp"
]

/-- Search terms that did not locate a terminal Birkhoff pointwise theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Birkhoff pointwise ergodic",
  "pointwise ergodic theorem",
  "birkhoffAverage Ergodic",
  "time average space average",
  "ae Tendsto timeAverage",
  "Tendsto (fun n => _ / n) Ergodic",
  "ergodic theorem"
]

/--
External Lean 4 anchor candidates found during the Stage1 repair audit.

These are not imported by this Lake workspace and therefore remain integration
blockers rather than repo-local proof closures.
-/
def externalAnchorCandidates : List String := [
  "https://github.com/lua-vr/pointwise-birkhoff",
  "lua-vr/pointwise-birkhoff@fc06094ca0506d8d74eba8b45b34882ce5930bf4",
  "raw file candidate: BirkhoffErgodicThm.lean",
  "theorem candidates: birkhoffErgodicTheorem, birkhoffErgodicTheorem'",
  "external lean-toolchain: leanprover/lean4:v4.20.0-rc5",
  "local lean-toolchain: leanprover/lean4:v4.29.0",
  "lakefile requires mathlib from git without a pinned revision",
  "not present in Formalizations/Lean/lakefile.lean dependency closure",
  "conclusion targets conditional expectation under invariants, so an ergodic constant/integral bridge is still needed for BirkhoffErgodicConclusion"
]

/-- Current external-primary-source audit date for the pointwise Birkhoff candidate. -/
def externalPrimarySourceAuditDate : String :=
  "2026-05-01"

/-- Checkable source commit for the external pointwise Birkhoff candidate. -/
def externalPointwiseBirkhoffSourceCommit : String :=
  "fc06094ca0506d8d74eba8b45b34882ce5930bf4"

/-- The external pointwise Birkhoff candidate is recorded at the audited commit. -/
theorem externalPointwiseBirkhoffSourceCommit_eq :
    externalPointwiseBirkhoffSourceCommit =
      "fc06094ca0506d8d74eba8b45b34882ce5930bf4" :=
  rfl

/-- Primary-source audit row for an external Lean 4 candidate. -/
structure ExternalLeanAuditRecord where
  sourceRepository : String
  sourceCommit : String
  sourceFiles : List String
  theoremCandidates : List String
  sourceLeanToolchain : String
  sourceMathlibRevision : String
  sourceLicense : String
  primarySourceChecks : List String
  repoLocalStatus : String
  integrationBlocker : String

/--
Fresh primary-source external Lean 4 audit for the terminal pointwise
Birkhoff branch.

This record intentionally remains `external_upstream_anchor_only`: the source
is useful evidence, but it has not been pinned, imported, or checked inside
this Lake workspace.
-/
def externalPrimarySourceAudit : ExternalLeanAuditRecord where
  sourceRepository := "https://github.com/lua-vr/pointwise-birkhoff"
  sourceCommit := externalPointwiseBirkhoffSourceCommit
  sourceFiles := [
    "README.md",
    "lean-toolchain",
    "lake-manifest.json",
    "LICENSE",
    "BirkhoffErgodicThm.lean"
  ]
  theoremCandidates := [
    "BirkhoffErgodicThm.birkhoffErgodicTheorem",
    "BirkhoffErgodicThm.birkhoffErgodicTheorem'"
  ]
  sourceLeanToolchain := "leanprover/lean4:v4.20.0-rc5"
  sourceMathlibRevision := "83f3832c6cfeecbc8d16b0248c98346956a7f0e5"
  sourceLicense := "Apache-2.0"
  primarySourceChecks := [
    "git ls-remote confirms refs/heads/main at fc06094ca0506d8d74eba8b45b34882ce5930bf4",
    "raw lean-toolchain confirms leanprover/lean4:v4.20.0-rc5",
    "raw lake-manifest.json confirms mathlib revision 83f3832c6cfeecbc8d16b0248c98346956a7f0e5",
    "raw BirkhoffErgodicThm.lean contains theorem birkhoffErgodicTheorem",
    "raw BirkhoffErgodicThm.lean contains theorem birkhoffErgodicTheorem'",
    "GitHub repository search for BirkhoffErgodicThm returned no additional repositories",
    "GitHub repository search for lean4 ergodic theorem returned no additional repositories"
  ]
  repoLocalStatus := "external_upstream_anchor_only"
  integrationBlocker :=
    "The external project is not in Formalizations/Lean/lakefile.lean, uses Lean 4.20.0-rc5 and mathlib 83f3832c6cfeecbc8d16b0248c98346956a7f0e5 rather than this workspace's Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, and its conditional-expectation endpoint still needs a repo-local bridge to BirkhoffErgodicConclusion."

/--
Bridge package for the conditional-expectation route to the ergodic theorem.

The abstract sub-sigma-algebra `invariant` is intentionally not defined here as
the full invariant sigma-algebra of `T`; mathlib does not expose that object as
a ready-made Birkhoff endpoint in this local dependency closure.  Instead this
package records the exact local proof obligations needed after an upstream or
local pointwise Birkhoff theorem returns a conditional expectation against such
a sub-sigma-algebra.
-/
structure InvariantConditionalExpectationBridge (Ω : Type u) [mΩ : MeasurableSpace Ω] : Type u where
  μ : Measure[mΩ] Ω
  T : Ω → Ω
  observable : Ω → ℝ
  observable_integrable : Integrable observable μ
  transformation_ergodic : Ergodic T μ
  invariant : MeasurableSpace Ω
  invariant_le : invariant ≤ mΩ
  invariant_sigmaFinite : SigmaFinite (μ.trim invariant_le)
  conditionalExpectationInvariant :
    (MeasureTheory.condExp invariant μ observable) ∘ T =ᵐ[μ]
      MeasureTheory.condExp invariant μ observable

/-- Forget the bridge-only invariant sigma-algebra data. -/
def InvariantConditionalExpectationBridge.toBirkhoffProblem
    {Ω : Type u} [MeasurableSpace Ω]
    (B : InvariantConditionalExpectationBridge Ω) : BirkhoffErgodicProblem Ω where
  μ := B.μ
  T := B.T
  observable := B.observable
  observable_integrable := B.observable_integrable
  transformation_ergodic := B.transformation_ergodic

/-- Conditional expectation of the observable against the bridge sub-sigma-algebra. -/
def invariantCondExp {Ω : Type u} [MeasurableSpace Ω]
    (B : InvariantConditionalExpectationBridge Ω) : Ω → ℝ :=
  MeasureTheory.condExp B.invariant B.μ B.observable

/-- The bridge conditional expectation is integrable. -/
theorem invariantCondExp_integrable {Ω : Type u} [MeasurableSpace Ω]
    (B : InvariantConditionalExpectationBridge Ω) :
    Integrable (invariantCondExp B) B.μ := by
  dsimp [invariantCondExp]
  exact MeasureTheory.integrable_condExp

/-- The bridge conditional expectation has the same integral as the original observable. -/
theorem invariantCondExp_integral_eq_spaceAverage {Ω : Type u} [MeasurableSpace Ω]
    (B : InvariantConditionalExpectationBridge Ω) :
    ∫ ω, invariantCondExp B ω ∂B.μ =
      spaceAverage B.toBirkhoffProblem := by
  letI := B.invariant_sigmaFinite
  dsimp [invariantCondExp, spaceAverage,
    InvariantConditionalExpectationBridge.toBirkhoffProblem]
  exact MeasureTheory.integral_condExp B.invariant_le

/-- The bridge records the invariance hypothesis needed by the ergodic collapse. -/
theorem invariantCondExp_comp_ae_eq {Ω : Type u} [MeasurableSpace Ω]
    (B : InvariantConditionalExpectationBridge Ω) :
    invariantCondExp B ∘ B.T =ᵐ[B.μ] invariantCondExp B :=
  B.conditionalExpectationInvariant

/--
Under ergodicity, the invariant conditional expectation collapses to an a.e.
constant.  This is the checked local bridge from a Birkhoff theorem with
conditional-expectation target toward the `BirkhoffErgodicConclusion` target.
-/
theorem invariantCondExp_ae_constant_from_ergodic
    {Ω : Type u} [MeasurableSpace Ω]
    (B : InvariantConditionalExpectationBridge Ω) :
    ∃ c : ℝ, invariantCondExp B =ᵐ[B.μ] const Ω c := by
  have hsm : StronglyMeasurable (invariantCondExp B) := by
    dsimp [invariantCondExp]
    exact MeasureTheory.stronglyMeasurable_condExp.mono B.invariant_le
  exact B.transformation_ergodic.ae_eq_const_of_ae_eq_comp_ae
    hsm.aestronglyMeasurable B.conditionalExpectationInvariant

/-- Leaf identifiers for the conditional-expectation bridge package. -/
inductive BridgeLeafId where
  | U001
  | U002
  | U003
  | U004
  | U005
  | U006
  | U007
  | U008
  deriving DecidableEq, Repr

/-- Stable public code for a bridge leaf identifier. -/
def BridgeLeafId.code : BridgeLeafId → String
  | .U001 => "U001"
  | .U002 => "U002"
  | .U003 => "U003"
  | .U004 => "U004"
  | .U005 => "U005"
  | .U006 => "U006"
  | .U007 => "U007"
  | .U008 => "U008"

/-- Integration-ready bridge leaf ledger row. -/
structure BridgeLeafRecord where
  leaf : BridgeLeafId
  localStatementName : String
  mathlibAnchor : String
  localBudgetSteps : Nat
  status : String
  debtClass : String
  role : String

/--
U001-U008 bridge package split.

Rows marked `local_proof_body` are checked in this file and each local proof is
well under the `<=100` M0387 step budget.  Rows marked `blocked` deliberately
do not claim completion: they require a terminal pointwise Birkhoff theorem
inside the repo-local Lake dependency closure before `BirkhoffErgodicConclusion`
can be wrapped as a theorem.
-/
def invariantConditionalExpectationBridgeLeaves : List BridgeLeafRecord := [
  {
    leaf := .U001,
    localStatementName :=
      "InvariantConditionalExpectationBridge.toBirkhoffProblem",
    mathlibAnchor := "BirkhoffErgodicProblem",
    localBudgetSteps := 1,
    status := "local_proof_body",
    debtClass := "none",
    role := "forget bridge-only invariant sigma-algebra data back to the canonical problem"
  },
  {
    leaf := .U002,
    localStatementName := "invariantCondExp",
    mathlibAnchor := "MeasureTheory.condExp",
    localBudgetSteps := 1,
    status := "local_proof_body",
    debtClass := "none",
    role := "name the conditional expectation against the bridge sub-sigma-algebra"
  },
  {
    leaf := .U003,
    localStatementName := "invariantCondExp_integrable",
    mathlibAnchor := "MeasureTheory.integrable_condExp",
    localBudgetSteps := 2,
    status := "local_proof_body",
    debtClass := "none",
    role := "show the bridge conditional expectation is integrable"
  },
  {
    leaf := .U004,
    localStatementName := "invariantCondExp_integral_eq_spaceAverage",
    mathlibAnchor := "MeasureTheory.integral_condExp",
    localBudgetSteps := 5,
    status := "local_proof_body",
    debtClass := "none",
    role := "identify the conditional-expectation integral with the canonical space average"
  },
  {
    leaf := .U005,
    localStatementName := "invariantCondExp_comp_ae_eq",
    mathlibAnchor := "EventuallyEq",
    localBudgetSteps := 1,
    status := "local_proof_body",
    debtClass := "none",
    role := "expose the bridge invariance hypothesis as a named checked theorem"
  },
  {
    leaf := .U006,
    localStatementName := "invariantCondExp_ae_constant_from_ergodic",
    mathlibAnchor := "Ergodic.ae_eq_const_of_ae_eq_comp_ae",
    localBudgetSteps := 6,
    status := "local_proof_body",
    debtClass := "none",
    role := "collapse an invariant conditional expectation to an a.e. constant under ergodicity"
  },
  {
    leaf := .U007,
    localStatementName := "terminal pointwise Birkhoff theorem returning invariant condExp",
    mathlibAnchor := "external or future local Birkhoff theorem",
    localBudgetSteps := 0,
    status := "blocked",
    debtClass := "formalization_debt_or_integration_blocker",
    role := "supply a repo-local theorem that time averages converge to the invariant conditional expectation"
  },
  {
    leaf := .U008,
    localStatementName := "birkhoffErgodicConclusion_wrapper",
    mathlibAnchor := "BirkhoffErgodicConclusion",
    localBudgetSteps := 1,
    status := "wrapper_checked_terminal_proof_blocked",
    debtClass := "formalization_debt_or_integration_blocker",
    role := "checked endpoint wrapper whose conclusion is definitionally the canonical terminal conclusion; still needs U007 or a pinned terminal proof"
  }
]

end S1_M_245
end Stage1
end AwesomeTheorems
