import Mathlib.Probability.Martingale.Convergence

/-!
# S1-M-282 / THM-M-1002: Doob martingale convergence theorem

This Stage1 artifact records the repo-local Lean 4 boundary for the Doob
martingale convergence theorem for upper and lower martingales.

The pinned mathlib snapshot already contains a discrete-time real-valued
submartingale convergence theorem:

* `MeasureTheory.Submartingale.ae_tendsto_limitProcess`
* `MeasureTheory.Submartingale.tendsto_eLpNorm_one_limitProcess`
* `MeasureTheory.Submartingale.ae_tendsto_limitProcess_of_uniformIntegrable`
* `MeasureTheory.Martingale.ae_eq_condExp_limitProcess`

The declarations below wrap those checked mathlib facts.  They should be read
as the verified discrete real-valued branch of the source theorem, not as a
claim that every possible continuous-time or extended-valued Doob convergence
formulation has been integrated in this repository.
-/

noncomputable section

open MeasureTheory Filter TopologicalSpace

open scoped NNReal ENNReal MeasureTheory ProbabilityTheory Topology

namespace AwesomeTheorems.Stage1.S1_M_282

universe u

/--
Normalized discrete-time real-valued submartingale convergence shape.

For a finite measure space, an `L1`-bounded real submartingale converges almost
everywhere to mathlib's canonical `Filtration.limitProcess`.
-/
def SubmartingaleConvergenceShape
    (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (ℱ : Filtration ℕ ‹MeasurableSpace Ω›) : Prop :=
  ∀ [IsFiniteMeasure μ] (f : ℕ → Ω → ℝ) (R : ℝ≥0),
    Submartingale f ℱ μ →
      (∀ n : ℕ, eLpNorm (f n) 1 μ ≤ (R : ℝ≥0∞)) →
        ∀ᵐ ω ∂μ, Tendsto (fun n => f n ω) atTop (𝓝 (ℱ.limitProcess f μ ω))

/--
Normalized discrete-time real-valued supermartingale convergence shape.

The limit is expressed as the negative of the `limitProcess` for the negated
submartingale.  This keeps the wrapper definitionally close to the available
mathlib theorem and avoids inventing a second canonical limit chooser.
-/
def SupermartingaleConvergenceShape
    (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (ℱ : Filtration ℕ ‹MeasurableSpace Ω›) : Prop :=
  ∀ [IsFiniteMeasure μ] (f : ℕ → Ω → ℝ) (R : ℝ≥0),
    Supermartingale f ℱ μ →
      (∀ n : ℕ, eLpNorm (f n) 1 μ ≤ (R : ℝ≥0∞)) →
        ∀ᵐ ω ∂μ, Tendsto (fun n => f n ω) atTop
          (𝓝 (-(ℱ.limitProcess (fun n ω => - f n ω) μ ω)))

/--
Stage1 statement shape for the checked discrete-time real-valued branch of
Doob convergence: both lower (`Submartingale`) and upper (`Supermartingale`)
processes converge almost everywhere under an `L1` bound.
-/
def StatementShape
    (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (ℱ : Filtration ℕ ‹MeasurableSpace Ω›) : Prop :=
  SubmartingaleConvergenceShape Ω μ ℱ ∧
    SupermartingaleConvergenceShape Ω μ ℱ

/-- mathlib directly proves the normalized submartingale convergence shape. -/
theorem submartingale_convergence_mathlib_anchor
    (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (ℱ : Filtration ℕ ‹MeasurableSpace Ω›) :
    SubmartingaleConvergenceShape Ω μ ℱ := by
  intro _ f R hf hbdd
  exact hf.ae_tendsto_limitProcess hbdd

/--
mathlib's supermartingale branch follows from the submartingale theorem applied
to the negated process.
-/
theorem supermartingale_convergence_via_negated_submartingale
    (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (ℱ : Filtration ℕ ‹MeasurableSpace Ω›) :
    SupermartingaleConvergenceShape Ω μ ℱ := by
  intro _ f R hf hbdd
  have hneg_bdd :
      ∀ n : ℕ, eLpNorm ((fun n ω => - f n ω) n) 1 μ ≤ (R : ℝ≥0∞) := by
    intro n
    change eLpNorm (-(f n)) 1 μ ≤ (R : ℝ≥0∞)
    rw [eLpNorm_neg]
    exact hbdd n
  have hconv :
      ∀ᵐ ω ∂μ, Tendsto (fun n => (fun n ω => - f n ω) n ω) atTop
        (𝓝 (ℱ.limitProcess (fun n ω => - f n ω) μ ω)) :=
    hf.neg.ae_tendsto_limitProcess hneg_bdd
  filter_upwards [hconv] with ω hω
  simpa using hω.neg

/--
Combined wrapper for the checked discrete-time real-valued Doob convergence
branch.
-/
theorem statementShape_mathlib_anchor
    (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω)
    (ℱ : Filtration ℕ ‹MeasurableSpace Ω›) :
    StatementShape Ω μ ℱ :=
  ⟨submartingale_convergence_mathlib_anchor Ω μ ℱ,
    supermartingale_convergence_via_negated_submartingale Ω μ ℱ⟩

/--
Integration-ready public note for the Stage1 backfill surface.

This string intentionally names the checked wrapper theorem rather than making
a broader Doob convergence completion claim.
-/
def publicWrapperBackfillNote : String :=
  "S1-M-282 has a repo-local Lean wrapper for the discrete-time real-valued " ++
    "Doob convergence branch via " ++
    "AwesomeTheorems.Stage1.S1_M_282.statementShape_mathlib_anchor."

/--
Recommended public wording decision for the Stage1 backfill surface.

The checked local theorem is intentionally narrower than an unqualified Doob
martingale convergence theorem.  Public completion wording should therefore
name the discrete-time real-valued sub/supermartingale branch under an `L1`
bound, unless the broader variants are split into unchecked child tasks.
-/
def publicWordingNarrowingRecommendation : String :=
  "Narrow THM-M-1002's public wording to the discrete-time real-valued " ++
    "sub/supermartingale convergence branch under L1 boundedness, matching " ++
    "AwesomeTheorems.Stage1.S1_M_282.statementShape_mathlib_anchor.  If the " ++
    "broader Doob martingale convergence wording is retained, keep the parent " ++
    "open and add unchecked child tasks for continuous-time martingales, local " ++
    "martingales, extended-valued or vector-valued variants, and stopping-time " ++
    "convergence APIs."

/--
Integration-ready child tasks required if the public theorem wording keeps the
broader, unqualified Doob martingale convergence scope.

These are deliberately data, not theorems: the checked theorem above only
closes the discrete-time real-valued `L1`-bounded branch.
-/
def broaderDoobVariantChildTasks : List String := [
  "S1-M-282-continuous-time: audit or formalize continuous-time martingale " ++
    "convergence APIs; pin/import/check any external Lean 4 proof before " ++
    "marking the branch complete.",
  "S1-M-282-local-martingale: audit or formalize local martingale convergence " ++
    "and localization hypotheses; leave as formalization_debt until validated " ++
    "repo-locally.",
  "S1-M-282-extended-valued: audit or formalize extended-valued, vector-valued, " ++
    "or Banach-valued Doob convergence variants; do not count anchor-only " ++
    "evidence as complete.",
  "S1-M-282-stopping-time: audit or formalize stopping-time, optional " ++
    "sampling, and convergence-at-stopping-time APIs needed by the broader " ++
    "public wording."
]

/--
Public backfill text for the broader-variant split.

An integrator can merge this text into the public blueprint/todo surface if
they decide not to narrow THM-M-1002 to the checked discrete-time real-valued
branch.
-/
def broaderDoobVariantBackfillText : String :=
  "If THM-M-1002 keeps broader Doob martingale convergence wording, keep " ++
    "S1-M-282 open and add unchecked child tasks for: (1) continuous-time " ++
    "martingale convergence APIs; (2) local martingale convergence and " ++
    "localization hypotheses; (3) extended-valued, vector-valued, or " ++
    "Banach-valued variants; and (4) stopping-time, optional sampling, and " ++
    "convergence-at-stopping-time APIs.  Each branch needs a repo-local Lean " ++
    "validation path or a concrete integration blocker; anchor-only external " ++
    "evidence is not a completed state."

/-- Pinned mathlib revision audited for the Doob convergence wrapper. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Pinned mathlib source file containing the imported convergence anchors. -/
def mathlibSourceFile : String :=
  "Mathlib/Probability/Martingale/Convergence.lean"

/--
Integration-ready public machine-anchor audit row.

This is metadata for a later serialized public-doc merge.  The checked Lean
wrapper remains `statementShape_mathlib_anchor`.
-/
def publicMachineAnchorAuditBackfillText : String :=
  "Record S1-M-282 as local_wrapper_upstream_mathlib for the discrete-time " ++
    "real-valued Doob convergence branch; local wrapper theorem " ++
    "AwesomeTheorems.Stage1.S1_M_282.statementShape_mathlib_anchor; " ++
    "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95; source file " ++
    "Mathlib/Probability/Martingale/Convergence.lean."

/--
Checked local leaf ledger for the discrete-time real-valued Doob convergence
branch.

These strings are an integration-ready public theorem-tree surface.  They do
not close the broader continuous-time, local-martingale, extended-valued, or
stopping-time branches.
-/
def dmcCheckedLeafLedgerBackfill : List String := [
  "DMC-L01 checked: SubmartingaleConvergenceShape statement normalization; " ++
    "under 20 local proof/definition steps.",
  "DMC-L02 checked: submartingale_convergence_mathlib_anchor; 2 local proof " ++
    "steps after binder introduction, delegating to pinned mathlib theorem " ++
    "Submartingale.ae_tendsto_limitProcess.",
  "DMC-L03 checked: SupermartingaleConvergenceShape statement normalization; " ++
    "under 20 local proof/definition steps.",
  "DMC-L04 checked: supermartingale_convergence_via_negated_submartingale; " ++
    "under 15 local proof steps: construct the negated L1 bound, call " ++
    "hf.neg.ae_tendsto_limitProcess, and apply Tendsto.neg.",
  "DMC-L05 checked: statementShape_mathlib_anchor; 1 pair-constructor step " ++
    "from the checked lower and upper branch wrappers.",
  "DMC-L06 checked: submartingale_l1_convergence_mathlib_anchor; 1 call to " ++
    "hf.tendsto_eLpNorm_one_limitProcess.",
  "DMC-L07 checked: " ++
    "submartingale_ae_convergence_of_uniformIntegrable_mathlib_anchor; " ++
    "1 call to hf.ae_tendsto_limitProcess_of_uniformIntegrable.",
  "DMC-L08 checked: martingale_ae_eq_condExp_limitProcess_mathlib_anchor; " ++
    "1 call to hf.ae_eq_condExp_limitProcess."
]

/--
Unchecked DMC leaves that must remain open unless a later branch gets its own
repo-local Lean validation path or concrete integration blocker.
-/
def dmcUncheckedLeafBoundary : List String := [
  "DMC-U01 unchecked: public theorem wording audit for the exact generality " ++
    "of upper and lower martingales in THM-M-1002.",
  "DMC-U02 unchecked: continuous-time branch search and object-model " ++
    "comparison.",
  "DMC-U03 unchecked: non-real-valued, extended-valued, vector-valued, or " ++
    "Banach-valued branch search.",
  "DMC-U04 unchecked: local martingale and stopping-time convergence " ++
    "variants.",
  "DMC-U05 unchecked: public merge-back and status synchronization after " ++
    "serial integrator review."
]

/--
Integration-ready public theorem-tree text for merging the checked DMC leaves
without marking unchecked branches complete.
-/
def dmcLeafLedgerPublicBackfillText : String :=
  "Merge DMC-L01 through DMC-L08 into the public theorem-tree surface as " ++
    "checked leaves for the discrete-time real-valued Doob convergence branch " ++
    "validated by AwesomeTheorems.Stage1.S1_M_282.statementShape_mathlib_anchor. " ++
    "Each checked leaf is below the <=100 local step budget.  Keep DMC-U01 " ++
    "through DMC-U05 unchecked: public wording, continuous-time, non-real or " ++
    "extended/vector-valued, local-martingale, stopping-time, and public " ++
    "merge-back/status-synchronization branches are not closed by the current " ++
    "wrapper."

/-- L1 convergence branch available in mathlib under uniform integrability. -/
theorem submartingale_l1_convergence_mathlib_anchor
    {Ω : Type u} {m0 : MeasurableSpace Ω} {μ : Measure Ω}
    {ℱ : Filtration ℕ m0} {f : ℕ → Ω → ℝ} [IsFiniteMeasure μ]
    (hf : Submartingale f ℱ μ) (hunif : UniformIntegrable f 1 μ) :
    Tendsto (fun n => eLpNorm (f n - ℱ.limitProcess f μ) 1 μ) atTop (𝓝 0) :=
  hf.tendsto_eLpNorm_one_limitProcess hunif

/-- Uniform integrability also gives the a.e. convergence branch in mathlib. -/
theorem submartingale_ae_convergence_of_uniformIntegrable_mathlib_anchor
    {Ω : Type u} {m0 : MeasurableSpace Ω} {μ : Measure Ω}
    {ℱ : Filtration ℕ m0} {f : ℕ → Ω → ℝ} [IsFiniteMeasure μ]
    (hf : Submartingale f ℱ μ) (hunif : UniformIntegrable f 1 μ) :
    ∀ᵐ ω ∂μ, Tendsto (fun n => f n ω) atTop (𝓝 (ℱ.limitProcess f μ ω)) :=
  hf.ae_tendsto_limitProcess_of_uniformIntegrable hunif

/-- Martingales expose the conditional-expectation representation of the limit. -/
theorem martingale_ae_eq_condExp_limitProcess_mathlib_anchor
    {Ω : Type u} {m0 : MeasurableSpace Ω} {μ : Measure Ω}
    {ℱ : Filtration ℕ m0} {f : ℕ → Ω → ℝ} [IsFiniteMeasure μ]
    (hf : Martingale f ℱ μ) (hunif : UniformIntegrable f 1 μ) (n : ℕ) :
    f n =ᵐ[μ] μ[ℱ.limitProcess f μ | ℱ n] :=
  hf.ae_eq_condExp_limitProcess hunif n

/-! ## Audit probes retained in the checked file. -/

#check Filtration
#check Filtration.limitProcess
#check Filtration.stronglyMeasurable_limitProcess
#check Filtration.memLp_limitProcess_of_eLpNorm_bdd
#check Submartingale
#check Supermartingale
#check Martingale
#check Supermartingale.neg
#check Submartingale.ae_tendsto_limitProcess
#check Submartingale.tendsto_eLpNorm_one_limitProcess
#check Submartingale.ae_tendsto_limitProcess_of_uniformIntegrable
#check Martingale.ae_eq_condExp_limitProcess
#check Integrable.tendsto_ae_condExp
#check eLpNorm_neg
#check SubmartingaleConvergenceShape
#check SupermartingaleConvergenceShape
#check StatementShape
#check statementShape_mathlib_anchor
#check publicWrapperBackfillNote
#check publicWordingNarrowingRecommendation
#check broaderDoobVariantChildTasks
#check broaderDoobVariantBackfillText
#check mathlibPinnedRevision
#check mathlibSourceFile
#check publicMachineAnchorAuditBackfillText
#check dmcCheckedLeafLedgerBackfill
#check dmcUncheckedLeafBoundary
#check dmcLeafLedgerPublicBackfillText

/-- mathlib modules checked while locating Doob convergence anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.Upcrossing",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.MeasureTheory.Function.UniformIntegrable"
]

/-- Pinned theorem and definition names used as repo-local anchors. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess",
  "MeasureTheory.Submartingale.tendsto_eLpNorm_one_limitProcess",
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess_of_uniformIntegrable",
  "MeasureTheory.Martingale.ae_eq_condExp_limitProcess",
  "MeasureTheory.Integrable.tendsto_ae_condExp",
  "MeasureTheory.Filtration.limitProcess",
  "MeasureTheory.Filtration.stronglyMeasurable_limitProcess",
  "MeasureTheory.Filtration.memLp_limitProcess_of_eLpNorm_bdd",
  "MeasureTheory.Submartingale.mul_lintegral_upcrossings_le_lintegral_pos_part",
  "MeasureTheory.Submartingale.mul_integral_upcrossingsBefore_le_integral_pos_part",
  "MeasureTheory.Supermartingale.neg"
]

/-- Search terms used for terminal or broader variants not wrapped here. -/
def broaderVariantSearchTerms : List String := [
  "Doob",
  "martingale convergence",
  "supermartingale convergence",
  "submartingale convergence",
  "continuous-time martingale convergence",
  "local martingale convergence",
  "almost sure convergence"
]

end AwesomeTheorems.Stage1.S1_M_282
