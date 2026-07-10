import Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving
import Mathlib.Dynamics.BirkhoffSum.NormedSpace
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# S1-M-247 / THM-M-1055: Birkhoff ergodic theorem

This Stage1 artifact records a conservative Lean 4 boundary for the pointwise
Birkhoff ergodic theorem.  The pinned mathlib snapshot contains Birkhoff sums
and averages, measure-preserving and ergodic maps, a.e. equality transport for
Birkhoff averages under quasi-measure-preserving maps, and several topological
or fixed-point Birkhoff-average lemmas.

The file does not claim a terminal proof of the a.e. convergence theorem.
Instead it freezes the statement shape and exposes small checked wrappers around
the currently available mathlib anchors.
-/

noncomputable section

open MeasureTheory Filter Function
open scoped Topology ENNReal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_247

universe u

/-- Real-valued observable on a measured dynamical system. -/
abbrev Observable (Ω : Type u) :=
  Ω → ℝ

/-- The sequence of Birkhoff averages of an observable along a self-map. -/
abbrev AverageProcess {Ω : Type u} (T : Ω → Ω) (g : Observable Ω) :=
  fun n x => birkhoffAverage ℝ T g n x

/--
Limit data expected in the non-ergodic pointwise Birkhoff theorem.

For an integrable observable `g` and a measure-preserving map `T`, the classical
theorem produces an integrable invariant limit function whose pointwise values
are the almost-sure limits of the Birkhoff averages.  This structure records
that target shape without asserting its existence.
-/
structure BirkhoffLimitPackage (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (T : Ω → Ω) (g : Observable Ω) : Type u where
  limit : Observable Ω
  limit_aestronglyMeasurable : AEStronglyMeasurable limit μ
  limit_integrable : Integrable limit μ
  invariant_ae : limit ∘ T =ᵐ[μ] limit
  average_ae_tendsto :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => birkhoffAverage ℝ T g n x) atTop (𝓝 (limit x))
  integral_limit_eq : (∫ x, limit x ∂μ) = ∫ x, g x ∂μ

/--
Ergodic specialization of the Birkhoff theorem: the invariant limit is
almost everywhere the constant space mean.
-/
structure ErgodicBirkhoffConclusion (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (T : Ω → Ω) (g : Observable Ω) : Type u where
  limitPackage : BirkhoffLimitPackage Ω μ T g
  mean_ae : limitPackage.limit =ᵐ[μ] fun _ : Ω => ∫ x, g x ∂μ

/--
Stage1 normalized statement shape for the Birkhoff ergodic theorem.

For every probability space, every ergodic measure-preserving self-map, and
every integrable real-valued observable, the Birkhoff averages converge almost
everywhere to the space mean.  This is only the statement boundary for the
current Stage1 slot.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Ω → Ω) (g : Observable Ω),
    Ergodic T μ → Integrable g μ → Nonempty (ErgodicBirkhoffConclusion Ω μ T g)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
      (T : Ω → Ω) (g : Observable Ω),
      Ergodic T μ → Integrable g μ → Nonempty (ErgodicBirkhoffConclusion Ω μ T g)) :
    StatementShape.{u} :=
  h

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_ergodic_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
        (T : Ω → Ω) (g : Observable Ω),
        Ergodic T μ → Integrable g μ → Nonempty (ErgodicBirkhoffConclusion Ω μ T g) :=
  Iff.rfl

/-!
## Public statement-normalization boundary

`StatementNormalizationBoundary` is the checked Stage1 declaration that public
backfill text should cite for this slot.  It deliberately aliases the current
repo-local `StatementShape`; it does not assert that the Birkhoff ergodic
theorem has been proved or imported into this repository.
-/

/--
Public statement-normalization boundary for `THM-M-1055`.

The boundary exposes the typed `BirkhoffLimitPackage` and
`ErgodicBirkhoffConclusion` target shape for later proof or dependency
integration.  It remains a statement boundary only.
-/
def StatementNormalizationBoundary : Prop :=
  StatementShape.{u}

/-- The public statement-normalization boundary is exactly `StatementShape`. -/
theorem statementNormalizationBoundary_iff_statementShape :
    StatementNormalizationBoundary.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/-- The public statement-normalization boundary unfolds to the expected ergodic target. -/
theorem statementNormalizationBoundary_iff_forall_ergodic_data :
    StatementNormalizationBoundary.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
        (T : Ω → Ω) (g : Observable Ω),
        Ergodic T μ → Integrable g μ → Nonempty (ErgodicBirkhoffConclusion Ω μ T g) :=
  Iff.rfl

/-- Canonical checked name for the current public statement-normalization boundary. -/
def statementNormalizationBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_247.StatementNormalizationBoundary"

/-- Machine-readable warning: this Stage1 boundary is not a terminal theorem proof. -/
def statementNormalizationIsTerminalTheorem : Bool :=
  false

/-- Checked form of the no-completion warning for the statement-normalization boundary. -/
theorem statementNormalizationIsTerminalTheorem_eq_false :
    statementNormalizationIsTerminalTheorem = false :=
  rfl

/-- Public backfill notes for the serial Stage1 integration pass. -/
def statementNormalizationPublicNotes : List String := [
  "Use AwesomeTheorems.Stage1.S1_M_247.StatementNormalizationBoundary as the current repo-local Lean statement boundary for THM-M-1055.",
  "The boundary includes AwesomeTheorems.Stage1.S1_M_247.BirkhoffLimitPackage and AwesomeTheorems.Stage1.S1_M_247.ErgodicBirkhoffConclusion.",
  "This is a checked statement-shape artifact only; it is not a completed proof of the Birkhoff ergodic theorem."
]

/-!
## Pinned mathlib audit boundary

The following metadata records the mathlib anchors requested by
`THM-M-1055.mathlib-audit`.  It is intentionally an audit table, not a theorem
claim for the pointwise Birkhoff ergodic theorem.
-/

/-- The pinned mathlib commit used for the Birkhoff-anchor audit. -/
def mathlibAuditCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked spelling of the pinned mathlib commit used by this audit. -/
theorem mathlibAuditCommit_eq :
    mathlibAuditCommit = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- A source-level mathlib anchor recorded for this Stage1 audit. -/
structure PinnedMathlibAnchor where
  displayName : String
  leanName : String
  moduleName : String
  sourceFile : String
  sourceLine : Nat
  sourceKind : String
  deriving Repr

/-- Required mathlib anchors for `THM-M-1055.mathlib-audit` at `mathlibAuditCommit`. -/
def requiredPinnedMathlibAnchors : List PinnedMathlibAnchor := [
  {
    displayName := "birkhoffSum",
    leanName := "birkhoffSum",
    moduleName := "Mathlib.Dynamics.BirkhoffSum.Basic",
    sourceFile := "Mathlib/Dynamics/BirkhoffSum/Basic.lean",
    sourceLine := 31,
    sourceKind := "def"
  },
  {
    displayName := "birkhoffAverage",
    leanName := "birkhoffAverage",
    moduleName := "Mathlib.Dynamics.BirkhoffSum.Average",
    sourceFile := "Mathlib/Dynamics/BirkhoffSum/Average.lean",
    sourceLine := 46,
    sourceKind := "def"
  },
  {
    displayName := "MeasurePreserving",
    leanName := "MeasureTheory.MeasurePreserving",
    moduleName := "Mathlib.Dynamics.Ergodic.MeasurePreserving",
    sourceFile := "Mathlib/Dynamics/Ergodic/MeasurePreserving.lean",
    sourceLine := 45,
    sourceKind := "structure"
  },
  {
    displayName := "Ergodic",
    leanName := "Ergodic",
    moduleName := "Mathlib.Dynamics.Ergodic.Ergodic",
    sourceFile := "Mathlib/Dynamics/Ergodic/Ergodic.lean",
    sourceLine := 50,
    sourceKind := "structure"
  },
  {
    displayName := "Integrable",
    leanName := "MeasureTheory.Integrable",
    moduleName := "Mathlib.MeasureTheory.Function.L1Space.Integrable",
    sourceFile := "Mathlib/MeasureTheory/Function/L1Space/Integrable.lean",
    sourceLine := 58,
    sourceKind := "def"
  },
  {
    displayName := "AEStronglyMeasurable",
    leanName := "MeasureTheory.AEStronglyMeasurable",
    moduleName := "Mathlib.MeasureTheory.Function.StronglyMeasurable.AEStronglyMeasurable",
    sourceFile := "Mathlib/MeasureTheory/Function/StronglyMeasurable/AEStronglyMeasurable.lean",
    sourceLine := 66,
    sourceKind := "def"
  },
  {
    displayName := "Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq",
    leanName := "MeasureTheory.Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq",
    moduleName := "Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving",
    sourceFile := "Mathlib/Dynamics/BirkhoffSum/QuasiMeasurePreserving.lean",
    sourceLine := 43,
    sourceKind := "theorem"
  }
]

/-- Count of required pinned mathlib anchors recorded by this audit child. -/
def requiredPinnedMathlibAnchorCount : Nat :=
  requiredPinnedMathlibAnchors.length

/-- The audit records exactly the seven mathlib anchors named in the child task. -/
theorem requiredPinnedMathlibAnchorCount_eq :
    requiredPinnedMathlibAnchorCount = 7 :=
  rfl

/-- Public backfill note for the mathlib-anchor audit child. -/
def mathlibAuditPublicNotes : List String := [
  "Pinned mathlib commit: 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "Recorded anchors: birkhoffSum, birkhoffAverage, MeasurePreserving, Ergodic, Integrable, AEStronglyMeasurable, and MeasureTheory.Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq.",
  "This audit records usable mathlib APIs only; mathlib at the pinned commit does not provide a terminal pointwise Birkhoff ergodic theorem for this Stage1 slot."
]

/-- A packaged Birkhoff limit exposes the a.e. convergence of averages. -/
theorem average_ae_tendsto_of_package {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} {g : Observable Ω}
    (P : BirkhoffLimitPackage Ω μ T g) :
    ∀ᵐ x ∂μ, Tendsto (AverageProcess T g · x) atTop (𝓝 (P.limit x)) :=
  P.average_ae_tendsto

/-- A packaged Birkhoff limit exposes the a.e. invariance of the limit. -/
theorem invariant_ae_of_package {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} {g : Observable Ω}
    (P : BirkhoffLimitPackage Ω μ T g) :
    P.limit ∘ T =ᵐ[μ] P.limit :=
  P.invariant_ae

/-- A packaged ergodic Birkhoff conclusion exposes the constant mean limit. -/
theorem mean_ae_of_ergodicConclusion {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} {g : Observable Ω}
    (C : ErgodicBirkhoffConclusion Ω μ T g) :
    C.limitPackage.limit =ᵐ[μ] fun _ : Ω => ∫ x, g x ∂μ :=
  C.mean_ae

/-- Checked anchor: an ergodic map is measure-preserving. -/
theorem ergodic_measurePreserving {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} (hT : Ergodic T μ) :
    MeasurePreserving T μ μ :=
  hT.toMeasurePreserving

/-- Checked anchor: an ergodic map is quasi-measure-preserving. -/
theorem ergodic_quasiMeasurePreserving {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} (hT : Ergodic T μ) :
    Measure.QuasiMeasurePreserving T μ μ :=
  hT.toMeasurePreserving.quasiMeasurePreserving

/--
Checked anchor: a.e. equal observables have a.e. equal Birkhoff averages under
a measure-preserving map.
-/
theorem birkhoffAverage_ae_eq_of_ae_eq_real {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} {g h : Observable Ω}
    (hT : MeasurePreserving T μ μ) (hgh : g =ᵐ[μ] h) (n : ℕ) :
    birkhoffAverage ℝ T g n =ᵐ[μ] birkhoffAverage ℝ T h n :=
  hT.quasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq ℝ hgh n

/-- Checked anchor: Birkhoff averages at a fixed point tend to the observable value. -/
theorem fixedPoint_tendsto_birkhoffAverage {Ω : Type u} (T : Ω → Ω)
    (g : Observable Ω) {x : Ω} (hx : Function.IsFixedPt T x) :
    Tendsto (fun n : ℕ => birkhoffAverage ℝ T g n x) atTop (𝓝 (g x)) :=
  hx.tendsto_birkhoffAverage ℝ g

/-- Checked anchor: strictly invariant observables have identical nonzero Birkhoff averages. -/
theorem invariant_birkhoffAverage_eq {Ω : Type u} {T : Ω → Ω}
    {g : Observable Ω} (hg : g ∘ T = g) {n : ℕ} (hn : (n : ℝ) ≠ 0) :
    birkhoffAverage ℝ T g n = g :=
  birkhoffAverage_of_comp_eq (R := ℝ) hg hn

/-- mathlib modules checked while locating local anchors for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Dynamics.BirkhoffSum.Basic",
  "Mathlib.Dynamics.BirkhoffSum.Average",
  "Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving",
  "Mathlib.Dynamics.BirkhoffSum.NormedSpace",
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.Function",
  "Mathlib.MeasureTheory.Function.AEEqFun",
  "Mathlib.MeasureTheory.Function.L1Space.Integrable",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "birkhoffSum",
  "birkhoffAverage",
  "birkhoffAverage_of_comp_eq",
  "Function.IsFixedPt.tendsto_birkhoffAverage",
  "MeasureTheory.Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq",
  "MeasureTheory.MeasurePreserving",
  "MeasureTheory.MeasurePreserving.iterate",
  "MeasureTheory.MeasurePreserving.quasiMeasurePreserving",
  "Ergodic",
  "Ergodic.quasiErgodic",
  "Ergodic.ae_eq_const_of_ae_eq_comp_ae",
  "MeasureTheory.Integrable",
  "MeasureTheory.AEStronglyMeasurable",
  "MeasureTheory.integral"
]

/-- Search terms that did not locate a terminal pointwise Birkhoff theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Birkhoff ergodic theorem",
  "pointwise ergodic theorem",
  "ae_tendsto_birkhoffAverage",
  "tendsto_birkhoffAverage_ae",
  "conditional expectation invariant sigma algebra",
  "birkhoffAverage_integral",
  "birkhoffAverage_mean",
  "almost sure ergodic theorem"
]

/-!
## External anchor audit boundary

The project `lua-vr/pointwise-birkhoff` at commit
`fc06094ca0506d8d74eba8b45b34882ce5930bf4` contains candidate Lean 4 theorem
declarations for the pointwise Birkhoff ergodic theorem.  This section records
the pinned upstream source metadata only.  The external project is not imported
by this repository, so the state remains `external_upstream_anchor_only`.
-/

/-- A source-level declaration or module in the external Birkhoff proof candidate. -/
structure ExternalBirkhoffAnchor where
  displayName : String
  moduleName : String
  sourceFile : String
  sourceLine : Nat
  sourceKind : String
  role : String
  deriving Repr

/-- Pinned commit for `lua-vr/pointwise-birkhoff` audited by `THM-M-1055.external-anchor`. -/
def externalBirkhoffAuditCommit : String :=
  "fc06094ca0506d8d74eba8b45b34882ce5930bf4"

/-- Checked spelling of the pinned external Birkhoff audit commit. -/
theorem externalBirkhoffAuditCommit_eq :
    externalBirkhoffAuditCommit = "fc06094ca0506d8d74eba8b45b34882ce5930bf4" :=
  rfl

/-- Git repository URL for the external pointwise Birkhoff proof candidate. -/
def externalBirkhoffRepository : String :=
  "https://github.com/lua-vr/pointwise-birkhoff"

/-- Upstream Lean toolchain recorded at the pinned external commit. -/
def externalBirkhoffLeanToolchain : String :=
  "leanprover/lean4:v4.20.0-rc5"

/-- Upstream mathlib revision recorded in the pinned external `lake-manifest.json`. -/
def externalBirkhoffMathlibRevision : String :=
  "83f3832c6cfeecbc8d16b0248c98346956a7f0e5"

/-- License file observed in the pinned external repository. -/
def externalBirkhoffLicense : String :=
  "Apache-2.0"

/--
The external package imports mathlib through `lakefile.lean` without an `@`
revision; the manifest pins the effective mathlib closure separately.
-/
def externalBirkhoffLakefilePinsMathlib : Bool :=
  false

/-- Checked spelling of the effective external mathlib revision. -/
theorem externalBirkhoffMathlibRevision_eq :
    externalBirkhoffMathlibRevision = "83f3832c6cfeecbc8d16b0248c98346956a7f0e5" :=
  rfl

/--
The theorem declarations and local PR-style modules found in the external
project at the pinned commit.
-/
def externalBirkhoffAnchors : List ExternalBirkhoffAnchor := [
  {
    displayName := "birkhoffErgodicTheorem",
    moduleName := "BirkhoffErgodicThm",
    sourceFile := "BirkhoffErgodicThm.lean",
    sourceLine := 329,
    sourceKind := "theorem",
    role := "main theorem assuming a measurable real observable"
  },
  {
    displayName := "birkhoffErgodicTheorem'",
    moduleName := "BirkhoffErgodicThm",
    sourceFile := "BirkhoffErgodicThm.lean",
    sourceLine := 371,
    sourceKind := "theorem",
    role := "main theorem dropping the explicit measurable-observable assumption"
  },
  {
    displayName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    sourceFile := "BirkhoffErgodicThm/BirkhoffSumPR.lean",
    sourceLine := 1,
    sourceKind := "module",
    role := "Birkhoff sum and average algebra for invariant, negative, additive, and subtractive observables"
  },
  {
    displayName := "InvariantsPR",
    moduleName := "BirkhoffErgodicThm.InvariantsPR",
    sourceFile := "BirkhoffErgodicThm/InvariantsPR.lean",
    sourceLine := 1,
    sourceKind := "module",
    role := "invariant function extraction from measurability over the invariant sigma-algebra"
  },
  {
    displayName := "PartialSupsPR",
    moduleName := "BirkhoffErgodicThm.PartialSupsPR",
    sourceFile := "BirkhoffErgodicThm/PartialSupsPR.lean",
    sourceLine := 1,
    sourceKind := "module",
    role := "partial supremum lemmas used by the Birkhoff maximal function"
  },
  {
    displayName := "FilterPR",
    moduleName := "BirkhoffErgodicThm.FilterPR",
    sourceFile := "BirkhoffErgodicThm/FilterPR.lean",
    sourceLine := 1,
    sourceKind := "module",
    role := "eventual equality transport under pointwise addition"
  },
  {
    displayName := "QuasiMeasurePreservingPR",
    moduleName := "BirkhoffErgodicThm.QuasiMeasurePreservingPR",
    sourceFile := "BirkhoffErgodicThm/QuasiMeasurePreservingPR.lean",
    sourceLine := 1,
    sourceKind := "module",
    role := "a.e. equality transport for Birkhoff sums and averages under quasi-measure-preserving maps"
  }
]

/-- Number of external theorem/module anchors recorded for the Birkhoff audit. -/
def externalBirkhoffAnchorCount : Nat :=
  externalBirkhoffAnchors.length

/-- The external audit records both theorem names and the five requested local modules. -/
theorem externalBirkhoffAnchorCount_eq :
    externalBirkhoffAnchorCount = 7 :=
  rfl

/-- Exact external imports used by the pinned top-level proof file. -/
def externalBirkhoffTopLevelImports : List String := [
  "BirkhoffErgodicThm.BirkhoffSumPR",
  "BirkhoffErgodicThm.InvariantsPR",
  "BirkhoffErgodicThm.PartialSupsPR",
  "BirkhoffErgodicThm.FilterPR",
  "BirkhoffErgodicThm.QuasiMeasurePreservingPR"
]

/-- Current repo-local closure state for the external Birkhoff project. -/
def externalBirkhoffRepoLocalState : String :=
  "external_upstream_anchor_only"

/-- Machine-readable warning: the external Birkhoff proof is not in this repo's validation closure. -/
def externalBirkhoffImportedLocally : Bool :=
  false

/-- Checked warning that the external Birkhoff proof has not yet been imported locally. -/
theorem externalBirkhoffImportedLocally_eq_false :
    externalBirkhoffImportedLocally = false :=
  rfl

/-- Concrete blockers before this external anchor can support any completion claim. -/
def externalBirkhoffIntegrationBlockers : List String := [
  "This repository uses leanprover/lean4:v4.29.0, while the external project uses leanprover/lean4:v4.20.0-rc5.",
  "This repository pins mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, while the external manifest pins mathlib 83f3832c6cfeecbc8d16b0248c98346956a7f0e5.",
  "The external lakefile imports mathlib from git without an explicit lakefile revision; only lake-manifest.json pins the effective dependency closure.",
  "A vendored-source probe against this repository's Lake environment failed immediately on BirkhoffErgodicThm.BirkhoffSumPR because birkhoffAverage_neg, birkhoffAverage_add, and birkhoffAverage_sub are already declared in the local mathlib closure.",
  "The external theorem conclusion is convergence to invCondexp; a local StatementShape wrapper still needs an invariant conditional-expectation-to-mean bridge under Ergodic T μ.",
  "The external proof depends on PR-style local modules that must be imported as a pinned Lake dependency or vendored and checked against this repository before a wrapper theorem can close StatementShape."
]

/--
Concrete blocker classification for `THM-M-1055.blocker`.

The labels mirror the public Stage1 checklist categories so a serial integrator
can copy the checked metadata without interpreting free-form prose.
-/
structure ExternalBirkhoffBlockerClassification where
  category : String
  isBlocker : Bool
  evidence : String
  nextAction : String
  deriving Repr

/-- Exact blocker audit requested by `THM-M-1055.blocker`. -/
def externalBirkhoffBlockerClassification : List ExternalBirkhoffBlockerClassification := [
  {
    category := "Lean toolchain",
    isBlocker := true,
    evidence := "External project uses leanprover/lean4:v4.20.0-rc5; this repository uses leanprover/lean4:v4.29.0.",
    nextAction := "Choose either a pinned separate dependency closure or port the proof to this repository's Lean toolchain."
  },
  {
    category := "mathlib revision",
    isBlocker := true,
    evidence := "External manifest pins mathlib 83f3832c6cfeecbc8d16b0248c98346956a7f0e5; this repository pins mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
    nextAction := "Port or pin against one coherent mathlib revision before claiming repo-local closure."
  },
  {
    category := "unpinned dependency",
    isBlocker := true,
    evidence := "The external lakefile requires mathlib from git without an explicit @ revision; only lake-manifest.json records the effective mathlib commit.",
    nextAction := "Preserve and verify the manifest closure or add an explicit pin in any vendored/pinned integration patch."
  },
  {
    category := "module naming",
    isBlocker := false,
    evidence := "The audited modules have stable names under BirkhoffErgodicThm.* and were located at the pinned commit.",
    nextAction := "Keep module names unchanged unless the vendored proof is ported and renamed to avoid local declaration collisions."
  },
  {
    category := "proof API drift",
    isBlocker := true,
    evidence := "The vendored-source probe failed because BirkhoffSumPR redeclares birkhoffAverage_neg, birkhoffAverage_add, and birkhoffAverage_sub, now present in local mathlib; the final theorem also targets invCondexp rather than the local ergodic mean package.",
    nextAction := "Reuse or rename the duplicate lemmas, then prove the invCondexp-to-constant-mean bridge under Ergodic T μ."
  },
  {
    category := "license issue",
    isBlocker := false,
    evidence := "The pinned external repository contains an Apache-2.0 license.",
    nextAction := "Retain license attribution if vendoring source; no license blocker was observed in this child audit."
  }
]

/-- Count of exact blocker categories audited for `THM-M-1055.blocker`. -/
def externalBirkhoffBlockerClassificationCount : Nat :=
  externalBirkhoffBlockerClassification.length

/-- The blocker audit records all six requested category checks. -/
theorem externalBirkhoffBlockerClassificationCount_eq :
    externalBirkhoffBlockerClassificationCount = 6 :=
  rfl

/-- Public backfill notes for the serial external-anchor integration pass. -/
def externalBirkhoffPublicNotes : List String := [
  "Audit lua-vr/pointwise-birkhoff at commit fc06094ca0506d8d74eba8b45b34882ce5930bf4 as an external Lean 4 proof candidate for THM-M-1055.",
  "The pinned top-level file BirkhoffErgodicThm.lean declares birkhoffErgodicTheorem at line 329 and birkhoffErgodicTheorem' at line 371.",
  "The pinned proof imports BirkhoffErgodicThm.BirkhoffSumPR, InvariantsPR, PartialSupsPR, FilterPR, and QuasiMeasurePreservingPR.",
  "Treat this as external_upstream_anchor_only until a pinned dependency or vendored proof body is checked locally against AwesomeTheorems.Stage1.S1_M_247.StatementShape."
]

/-!
## External integration attempt boundary

This section records the `THM-M-1055.integration` child probe.  Because the
child worker is not allowed to edit shared Lake files or vendor external source
files into the repository, the concrete import attempt was run in `/tmp` against
this repository's `lake env`.  It did not enter the external proof into the
repo-local validation closure.
-/

/-- Date of the vendored-source import probe for `lua-vr/pointwise-birkhoff`. -/
def externalBirkhoffIntegrationAttemptDate : String :=
  "2026-05-01"

/-- Exact style of integration attempt executed by the child worker. -/
def externalBirkhoffIntegrationAttemptKind : String :=
  "vendored-source probe in /tmp using this repository's lake env"

/-- Representative command for the first failing vendored-source import probe. -/
def externalBirkhoffVendoredProbeCommand : String :=
  "cd Formalizations/Lean && LEAN_PATH=/tmp/s1-m-247-birkhoff.TYDfE2 lake env lean -R /tmp/s1-m-247-birkhoff.TYDfE2 -o /tmp/s1-m-247-birkhoff.TYDfE2/BirkhoffErgodicThm/BirkhoffSumPR.olean /tmp/s1-m-247-birkhoff.TYDfE2/BirkhoffErgodicThm/BirkhoffSumPR.lean"

/-- The vendored-source probe did not successfully import the external package locally. -/
def externalBirkhoffVendoredProbeSucceeded : Bool :=
  false

/-- Checked result of the vendored-source probe status. -/
theorem externalBirkhoffVendoredProbeSucceeded_eq_false :
    externalBirkhoffVendoredProbeSucceeded = false :=
  rfl

/-- First local compiler diagnostics from the vendored-source import probe. -/
def externalBirkhoffVendoredProbeDiagnostics : List String := [
  "BirkhoffErgodicThm/BirkhoffSumPR.lean:40:6: error: birkhoffAverage_neg has already been declared",
  "BirkhoffErgodicThm/BirkhoffSumPR.lean:47:6: error: birkhoffAverage_add has already been declared",
  "BirkhoffErgodicThm/BirkhoffSumPR.lean:55:6: error: birkhoffAverage_sub has already been declared"
]

/--
Minimal wrapper input expected from a successful external integration.

The upstream theorem currently targets an invariant conditional expectation.
For this repository's `StatementShape`, the imported proof must also provide
the ergodic specialization identifying that limit with the constant space mean.
-/
structure ExternalBirkhoffWrapperInput (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (T : Ω → Ω) (g : Observable Ω) : Type u where
  limitPackage : BirkhoffLimitPackage Ω μ T g
  ergodicMeanBridge : limitPackage.limit =ᵐ[μ] fun _ : Ω => ∫ x, g x ∂μ

/-- Convert a successfully integrated external wrapper input into this slot's conclusion. -/
def ExternalBirkhoffWrapperInput.toConclusion {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {T : Ω → Ω} {g : Observable Ω}
    (W : ExternalBirkhoffWrapperInput Ω μ T g) :
    ErgodicBirkhoffConclusion Ω μ T g where
  limitPackage := W.limitPackage
  mean_ae := W.ergodicMeanBridge

/--
Local wrapper check against `StatementShape`.

This theorem verifies the exact repo-local wrapper shape that a future pinned
dependency or vendored proof must satisfy.  It does not import or complete the
external theorem.
-/
theorem StatementShape.of_externalBirkhoffWrapperInput
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
      (T : Ω → Ω) (g : Observable Ω),
      Ergodic T μ → Integrable g μ →
        Nonempty (ExternalBirkhoffWrapperInput Ω μ T g)) :
    StatementShape.{u} := by
  intro Ω _ μ _ T g hT hg
  rcases h Ω μ T g hT hg with ⟨W⟩
  exact ⟨W.toConclusion⟩

/-!
## External proof leaf ledger

The upstream `lua-vr/pointwise-birkhoff` proof graph is not imported locally,
but the public completion gate requires a local leaf split before any future
completion claim.  The following checked ledger splits the audited external
graph into fewer than one hundred integration leaves.  Each leaf is still
`unchecked locally` until a pinned dependency or vendored proof body validates
against this repository.
-/

/-- A local leaf in the audited external pointwise-Birkhoff proof graph. -/
structure ExternalBirkhoffProofLeaf where
  leafId : String
  packageName : String
  moduleName : String
  declarationName : String
  localObligation : String
  maxLocalSteps : Nat
  currentStatus : String
  deriving Repr

/-- Local proof-budget ceiling used for every external Birkhoff proof leaf. -/
def externalBirkhoffProofLeafStepBudget : Nat :=
  100

/--
Leaf split for the external proof graph rooted at
`BirkhoffErgodicThm.birkhoffErgodicTheorem'`.

The split follows the pinned source modules and declarations audited above.
The entries are integration-ready obligations, not completed repo-local proofs.
-/
def externalBirkhoffProofLeafLedger : List ExternalBirkhoffProofLeaf := [
  {
    leafId := "M1055-EXT-L001",
    packageName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    declarationName := "invariant_iter",
    localObligation := "Port or reuse the iterate invariance lemma for functions fixed by f.",
    maxLocalSteps := 20,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L002",
    packageName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    declarationName := "birkhoffSum_of_invariant",
    localObligation := "Derive the Birkhoff sum of an invariant observable from invariant_iter.",
    maxLocalSteps := 30,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L003",
    packageName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    declarationName := "birkhoffAverage_of_invariant",
    localObligation := "Show a positive-length Birkhoff average of an invariant observable is the observable.",
    maxLocalSteps := 40,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L004",
    packageName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    declarationName := "birkhoffAverage_neg",
    localObligation := "Reuse or rename the upstream negation lemma that collides with local mathlib.",
    maxLocalSteps := 30,
    currentStatus := "integration-blocked by duplicate local declaration"
  },
  {
    leafId := "M1055-EXT-L005",
    packageName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    declarationName := "birkhoffAverage_add",
    localObligation := "Reuse or rename the upstream addition lemma that collides with local mathlib.",
    maxLocalSteps := 30,
    currentStatus := "integration-blocked by duplicate local declaration"
  },
  {
    leafId := "M1055-EXT-L006",
    packageName := "BirkhoffSumPR",
    moduleName := "BirkhoffErgodicThm.BirkhoffSumPR",
    declarationName := "birkhoffAverage_sub",
    localObligation := "Reuse or rename the upstream subtraction lemma that collides with local mathlib.",
    maxLocalSteps := 30,
    currentStatus := "integration-blocked by duplicate local declaration"
  },
  {
    leafId := "M1055-EXT-L007",
    packageName := "InvariantsPR",
    moduleName := "BirkhoffErgodicThm.InvariantsPR",
    declarationName := "MeasurableSpace.invariant_of_measurable_invariants",
    localObligation := "Port invariant-function extraction from measurability over the invariant sigma-algebra.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L008",
    packageName := "PartialSupsPR",
    moduleName := "BirkhoffErgodicThm.PartialSupsPR",
    declarationName := "map_partialSups",
    localObligation := "Port the sup-hom transport lemma for partialSups.",
    maxLocalSteps := 25,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L009",
    packageName := "PartialSupsPR",
    moduleName := "BirkhoffErgodicThm.PartialSupsPR",
    declarationName := "add_partialSups",
    localObligation := "Port the add-left transport lemma for partialSups.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L010",
    packageName := "FilterPR",
    moduleName := "BirkhoffErgodicThm.FilterPR",
    declarationName := "Filter.EventuallyEq.add_right",
    localObligation := "Port eventual-equality transport under right addition.",
    maxLocalSteps := 15,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L011",
    packageName := "FilterPR",
    moduleName := "BirkhoffErgodicThm.FilterPR",
    declarationName := "Filter.EventuallyEq.add_left",
    localObligation := "Port eventual-equality transport under left addition.",
    maxLocalSteps := 15,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L012",
    packageName := "QuasiMeasurePreservingPR",
    moduleName := "BirkhoffErgodicThm.QuasiMeasurePreservingPR",
    declarationName := "birkhoffSum_ae_eq_of_ae_eq",
    localObligation := "Port a.e. equality transport from observables to Birkhoff sums.",
    maxLocalSteps := 70,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L013",
    packageName := "QuasiMeasurePreservingPR",
    moduleName := "BirkhoffErgodicThm.QuasiMeasurePreservingPR",
    declarationName := "birkhoffAverage_ae_eq_of_ae_eq",
    localObligation := "Port a.e. equality transport from observables to Birkhoff averages.",
    maxLocalSteps := 30,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L014",
    packageName := "BirkhoffMax",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMax",
    localObligation := "Define the partial-supremum maximum of positive Birkhoff sums.",
    maxLocalSteps := 15,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L015",
    packageName := "BirkhoffMax",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMax_succ",
    localObligation := "Prove the successor recurrence for birkhoffMax using add_partialSups.",
    maxLocalSteps := 70,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L016",
    packageName := "BirkhoffMax",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMaxDiff_aux",
    localObligation := "Relate the max-difference term to phi minus the negative part of the next max.",
    maxLocalSteps := 45,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L017",
    packageName := "BirkhoffMax",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMaxDiff_antitone",
    localObligation := "Show the max-difference sequence is antitone.",
    maxLocalSteps := 45,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L018",
    packageName := "Measurability",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffSum_measurable",
    localObligation := "Prove measurability of finite Birkhoff sums from measurable f and phi.",
    maxLocalSteps := 25,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L019",
    packageName := "Measurability",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMax_measurable",
    localObligation := "Prove measurability of birkhoffMax by induction on partial suprema.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L020",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffSup",
    localObligation := "Define the EReal supremum of positive Birkhoff sums.",
    maxLocalSteps := 15,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L021",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffSup_measurable",
    localObligation := "Prove measurability of the EReal Birkhoff supremum.",
    maxLocalSteps := 25,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L022",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "divergentSet",
    localObligation := "Define the top-level divergent set where the Birkhoff supremum is top.",
    maxLocalSteps := 15,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L023",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "divergentSet_invariant",
    localObligation := "Prove forward-backward invariance of the divergent set.",
    maxLocalSteps := 95,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L024",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "divergentSet_measurable",
    localObligation := "Prove measurability of the divergent set.",
    maxLocalSteps := 25,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L025",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "divergentSet_mem_invalg",
    localObligation := "Package divergent-set measurability over the invariant sigma-algebra.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L026",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMax_tendsto_top_mem_divergentSet",
    localObligation := "Convert divergent-set membership into atTop divergence of birkhoffMax.",
    maxLocalSteps := 55,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L027",
    packageName := "DivergentSet",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMaxDiff_tendsto_of_mem_divergentSet",
    localObligation := "Prove max-difference convergence to phi on the divergent set.",
    maxLocalSteps := 70,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L028",
    packageName := "UpperLimit",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "nonneg",
    localObligation := "Define the filter encoding nonpositive limsup behavior.",
    maxLocalSteps := 10,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L029",
    packageName := "UpperLimit",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffAverage_tendsto_nonpos_of_not_mem_divergentSet",
    localObligation := "Turn non-membership in the divergent set into a nonpositive limsup bound.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L030",
    packageName := "Integrability",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "iterates_integrable",
    localObligation := "Prove integrability is preserved along measure-preserving iterates.",
    maxLocalSteps := 55,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L031",
    packageName := "Integrability",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffSum_integrable",
    localObligation := "Prove integrability of Birkhoff sums by finite summation.",
    maxLocalSteps := 25,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L032",
    packageName := "Integrability",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMax_integrable",
    localObligation := "Prove integrability of birkhoffMax by induction using Integrable.sup.",
    maxLocalSteps := 45,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L033",
    packageName := "Integrability",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffMaxDiff_integrable",
    localObligation := "Prove integrability of birkhoffMaxDiff by subtraction and map-measure transport.",
    maxLocalSteps := 70,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L034",
    packageName := "MaximalInequality",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "int_birkhoffMaxDiff_in_divergentSet_tendsto",
    localObligation := "Apply dominated convergence to max-difference integrals over the divergent set.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L035",
    packageName := "MaximalInequality",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "int_birkhoffMaxDiff_in_divergentSet_nonneg",
    localObligation := "Prove nonnegativity of restricted max-difference integrals.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L036",
    packageName := "MaximalInequality",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "int_in_divergentSet_nonneg",
    localObligation := "Pass nonnegativity to the limiting integral over the divergent set.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L037",
    packageName := "ConditionalExpectation",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "nullMeasurableSpace_le",
    localObligation := "Bridge the ambient measurable space into the null-measurable-space instance.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L038",
    packageName := "ConditionalExpectation",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "divergentSet_zero_meas_of_condexp_neg",
    localObligation := "Show negative invariant conditional expectation forces the divergent set to be null.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L039",
    packageName := "ConditionalExpectation",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "limsup_birkhoffAverage_nonpos_of_condexp_neg",
    localObligation := "Use the null divergent set to obtain the nonpositive limsup conclusion a.e.",
    maxLocalSteps := 55,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L040",
    packageName := "ConditionalExpectation",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "invCondexp",
    localObligation := "Define the invariant conditional-expectation target.",
    maxLocalSteps := 15,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L041",
    packageName := "AuxiliaryTheorem",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem_aux.psi_setup",
    localObligation := "Introduce psi and prove integrability and measurability for the shifted observable.",
    maxLocalSteps := 80,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L042",
    packageName := "AuxiliaryTheorem",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem_aux.condexp_shift",
    localObligation := "Compute the conditional expectation of the shifted observable.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L043",
    packageName := "AuxiliaryTheorem",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem_aux.limsup_nonpos",
    localObligation := "Apply the conditional-expectation negative branch to psi.",
    maxLocalSteps := 65,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L044",
    packageName := "AuxiliaryTheorem",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem_aux.average_rewrite",
    localObligation := "Rewrite Birkhoff averages of psi using invariant and constant average lemmas.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L045",
    packageName := "AuxiliaryTheorem",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem_aux",
    localObligation := "Assemble the shifted-observable limsup estimate for every positive epsilon.",
    maxLocalSteps := 90,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L046",
    packageName := "MainTheoremMeasurable",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem.two_sided_setup",
    localObligation := "Apply the auxiliary estimate to phi and -phi for reciprocal epsilon bounds.",
    maxLocalSteps := 90,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L047",
    packageName := "MainTheoremMeasurable",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem.abs_bound",
    localObligation := "Combine positive and negative estimates into eventual absolute-value bounds.",
    maxLocalSteps := 100,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L048",
    packageName := "MainTheoremMeasurable",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem.metric_tendsto",
    localObligation := "Convert reciprocal eventual bounds into metric Tendsto.",
    maxLocalSteps := 80,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L049",
    packageName := "MainTheoremGeneral",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem'.measurable_representative",
    localObligation := "Choose a measurable representative of an integrable observable and transfer integrability.",
    maxLocalSteps := 55,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L050",
    packageName := "MainTheoremGeneral",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem'.condexp_congr_set",
    localObligation := "Extract a full-measure set where conditional expectations of a.e.-equal observables agree.",
    maxLocalSteps := 45,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L051",
    packageName := "MainTheoremGeneral",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem'.measurable_theorem_set",
    localObligation := "Extract a full-measure set carrying the measurable-observable theorem.",
    maxLocalSteps := 35,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L052",
    packageName := "MainTheoremGeneral",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem'.average_ae_eq_set",
    localObligation := "Extract a full-measure set where all Birkhoff averages of a.e.-equal observables agree.",
    maxLocalSteps := 45,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L053",
    packageName := "MainTheoremGeneral",
    moduleName := "BirkhoffErgodicThm",
    declarationName := "birkhoffErgodicTheorem'",
    localObligation := "Intersect the three full-measure sets and finish the nonmeasurable-observable theorem.",
    maxLocalSteps := 45,
    currentStatus := "external-source-audited; unchecked locally"
  },
  {
    leafId := "M1055-EXT-L054",
    packageName := "LocalWrapperBridge",
    moduleName := "AwesomeTheorems.Stage1.S1_M_247",
    declarationName := "ExternalBirkhoffWrapperInput",
    localObligation := "Bridge the external invCondexp target to this repo's ErgodicBirkhoffConclusion package.",
    maxLocalSteps := 100,
    currentStatus := "not in upstream proof; required for repo-local wrapper"
  },
  {
    leafId := "M1055-EXT-L055",
    packageName := "LocalIntegrationGate",
    moduleName := "AwesomeTheorems.Stage1.S1_M_247",
    declarationName := "StatementShape.of_externalBirkhoffWrapperInput",
    localObligation := "Instantiate the checked wrapper after the external dependency or vendored source imports.",
    maxLocalSteps := 40,
    currentStatus := "wrapper shape checked; external proof input unavailable"
  }
]

/-- Number of leaves in the external Birkhoff proof split. -/
def externalBirkhoffProofLeafCount : Nat :=
  externalBirkhoffProofLeafLedger.length

/-- The external proof graph has been split into fewer than one hundred local leaves. -/
theorem externalBirkhoffProofLeafCount_le_100 :
    externalBirkhoffProofLeafCount ≤ 100 := by
  native_decide

/-- Boolean audit that every listed leaf has local proof budget at most one hundred steps. -/
def externalBirkhoffProofLeafBudgetsWithinLimit : Bool :=
  externalBirkhoffProofLeafLedger.all
    (fun leaf => decide (leaf.maxLocalSteps ≤ externalBirkhoffProofLeafStepBudget))

/-- Checked audit: every listed external proof leaf has a `<=100` local proof budget. -/
theorem externalBirkhoffProofLeafBudgetsWithinLimit_eq_true :
    externalBirkhoffProofLeafBudgetsWithinLimit = true := by
  native_decide

/-- Machine-readable warning: the leaf ledger alone does not complete the theorem. -/
def externalBirkhoffProofLeafLedgerClosesTheorem : Bool :=
  false

/-- Checked no-completion warning for the external proof leaf ledger. -/
theorem externalBirkhoffProofLeafLedgerClosesTheorem_eq_false :
    externalBirkhoffProofLeafLedgerClosesTheorem = false :=
  rfl

/-- Public backfill notes for the external proof leaf-ledger child. -/
def externalBirkhoffProofLeafLedgerPublicNotes : List String := [
  "The audited external proof graph rooted at BirkhoffErgodicThm.birkhoffErgodicTheorem' is split into 55 local leaves in externalBirkhoffProofLeafLedger.",
  "Every listed leaf has maxLocalSteps <= 100, checked by externalBirkhoffProofLeafBudgetsWithinLimit_eq_true.",
  "This leaf ledger is integration-ready only; the external proof remains outside the repo-local validation closure until imported or vendored and checked locally."
]

/-! ## Audit probes retained in the checked file. -/

#check Observable
#check AverageProcess
#check BirkhoffLimitPackage
#check ErgodicBirkhoffConclusion
#check StatementShape
#check statementShape_iff_forall_ergodic_data
#check StatementNormalizationBoundary
#check statementNormalizationBoundary_iff_statementShape
#check statementNormalizationBoundary_iff_forall_ergodic_data
#check statementNormalizationIsTerminalTheorem_eq_false
#check mathlibAuditCommit
#check mathlibAuditCommit_eq
#check PinnedMathlibAnchor
#check requiredPinnedMathlibAnchors
#check requiredPinnedMathlibAnchorCount_eq
#check birkhoffSum
#check birkhoffAverage
#check birkhoffAverage_of_comp_eq
#check Function.IsFixedPt.tendsto_birkhoffAverage
#check MeasureTheory.Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq
#check MeasureTheory.MeasurePreserving
#check MeasureTheory.MeasurePreserving.iterate
#check MeasureTheory.MeasurePreserving.quasiMeasurePreserving
#check Ergodic
#check Ergodic.quasiErgodic
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#check MeasureTheory.Integrable
#check MeasureTheory.AEStronglyMeasurable
#check MeasureTheory.integral
#check ExternalBirkhoffAnchor
#check externalBirkhoffAuditCommit
#check externalBirkhoffAuditCommit_eq
#check externalBirkhoffRepository
#check externalBirkhoffLeanToolchain
#check externalBirkhoffMathlibRevision
#check externalBirkhoffMathlibRevision_eq
#check externalBirkhoffAnchors
#check externalBirkhoffAnchorCount_eq
#check externalBirkhoffTopLevelImports
#check externalBirkhoffRepoLocalState
#check externalBirkhoffImportedLocally_eq_false
#check externalBirkhoffIntegrationBlockers
#check ExternalBirkhoffBlockerClassification
#check externalBirkhoffBlockerClassification
#check externalBirkhoffBlockerClassificationCount_eq
#check externalBirkhoffIntegrationAttemptDate
#check externalBirkhoffIntegrationAttemptKind
#check externalBirkhoffVendoredProbeCommand
#check externalBirkhoffVendoredProbeSucceeded_eq_false
#check externalBirkhoffVendoredProbeDiagnostics
#check ExternalBirkhoffWrapperInput
#check ExternalBirkhoffWrapperInput.toConclusion
#check StatementShape.of_externalBirkhoffWrapperInput
#check ExternalBirkhoffProofLeaf
#check externalBirkhoffProofLeafStepBudget
#check externalBirkhoffProofLeafLedger
#check externalBirkhoffProofLeafCount
#check externalBirkhoffProofLeafCount_le_100
#check externalBirkhoffProofLeafBudgetsWithinLimit_eq_true
#check externalBirkhoffProofLeafLedgerClosesTheorem_eq_false

end S1_M_247
end Stage1
end AwesomeTheorems
