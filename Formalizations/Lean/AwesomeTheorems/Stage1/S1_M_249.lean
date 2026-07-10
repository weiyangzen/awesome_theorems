import Mathlib.Analysis.Subadditive
import Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Function.L1Space.Integrable
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# S1-M-249 / THM-M-1057: Kingman's subadditive ergodic theorem

This Stage1 artifact records a conservative Lean 4 boundary for Kingman's
subadditive ergodic theorem.

The pinned mathlib snapshot has measure-preserving and ergodic maps, Birkhoff
sums and averages, integrability transport along measure-preserving maps,
almost-everywhere convergence predicates, invariant-function constancy for
ergodic maps, and deterministic Fekete convergence for subadditive real
sequences.  A terminal theorem named `Kingman`, or a pointwise subadditive
ergodic theorem for stochastic processes, was not found in the local dependency
closure.

Accordingly this file provides only a checked statement shape and wrappers
around the currently available mathlib anchors.  No terminal proof of
Kingman's theorem is claimed here.
-/

noncomputable section

open Filter Function MeasureTheory Set
open scoped MeasureTheory Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_249

universe u

/--
Data package for the ergodic real-valued form of Kingman's theorem.

The process is indexed by natural numbers and satisfies the usual cocycle
subadditivity inequality along iterates of a measure-preserving transformation.
The `limit` field is the future almost-everywhere limit candidate; the checked
file records the type of the desired conclusion but does not prove that this
limit exists from the listed hypotheses.
-/
structure KingmanProcess (Ω : Type u) [MeasurableSpace Ω] : Type u where
  μ : Measure Ω
  T : Ω → Ω
  process : ℕ → Ω → ℝ
  limit : Ω → ℝ
  isProbability : IsProbabilityMeasure μ
  transformation_ergodic : Ergodic T μ
  process_integrable : ∀ n : ℕ, Integrable (process n) μ
  process_zero : process 0 =ᵐ[μ] fun _ => 0
  subadditive_cocycle :
    ∀ m n : ℕ,
      process (m + n) =ᵐ[μ] (fun ω => process m ω + process n ((T^[m]) ω))
        ∨ process (m + n) ≤ᵐ[μ] (fun ω => process m ω + process n ((T^[m]) ω))
  lowerBoundedExpectedAverages :
    ∃ C : ℝ, ∀ n : ℕ, n ≠ 0 → C ≤ (∫ ω, process n ω ∂μ) / (n : ℝ)

/-- The normalized random average `X_n(ω) / n` used in Kingman's conclusion. -/
def normalizedProcess {Ω : Type u} [MeasurableSpace Ω] (P : KingmanProcess Ω)
    (n : ℕ) (ω : Ω) : ℝ :=
  P.process n ω / (n : ℝ)

/-- Expected normalized process, used in the ergodic constant. -/
def expectedAverage {Ω : Type u} [MeasurableSpace Ω] (P : KingmanProcess Ω)
    (n : ℕ) : ℝ :=
  (∫ ω, P.process n ω ∂P.μ) / (n : ℝ)

/--
The expected Kingman constant in the ergodic case: the infimum of normalized
expectations over positive indices.
-/
def ergodicKingmanValue {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) : ℝ :=
  sInf ((fun n : ℕ => expectedAverage P n) '' Ici 1)

/--
Expected terminal conclusion for the ergodic Kingman theorem.

For an ergodic measure-preserving transformation, the normalized subadditive
process should converge almost everywhere, the limit should be invariant, and
the invariant limit should be almost everywhere the infimum of expected
normalized values.  This is a statement boundary only.
-/
def KingmanConclusion {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) : Prop :=
  (∀ᵐ ω ∂P.μ, Tendsto (fun n : ℕ => normalizedProcess P n ω) atTop (𝓝 (P.limit ω))) ∧
    P.limit ∘ P.T =ᵐ[P.μ] P.limit ∧
      P.limit =ᵐ[P.μ] fun _ => ergodicKingmanValue P

/--
Stage1 normalized statement-shape candidate for Kingman's subadditive ergodic
theorem in the ergodic real-valued probability-space form.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ P : KingmanProcess Ω,
      KingmanConclusion P

/-- The statement-shape definition unfolds to the normalized Kingman form. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ P : KingmanProcess Ω,
          KingmanConclusion P :=
  Iff.rfl

/-- The ergodic hypothesis exposes a checked mathlib `MeasurePreserving` anchor. -/
theorem transformation_measurePreserving {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) :
    MeasurePreserving P.T P.μ P.μ :=
  P.transformation_ergodic.toMeasurePreserving

/-- The transformation is quasi-measure-preserving, as required by a.e. pullback APIs. -/
theorem transformation_quasiMeasurePreserving {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) :
    Measure.QuasiMeasurePreserving P.T P.μ P.μ :=
  P.transformation_ergodic.toMeasurePreserving.quasiMeasurePreserving

/-- Every iterate of the transformation is measure-preserving. -/
theorem transformation_iterate_measurePreserving {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) (n : ℕ) :
    MeasurePreserving (P.T^[n]) P.μ P.μ :=
  P.transformation_ergodic.toMeasurePreserving.iterate n

/-- Project the integrability of each process time slice. -/
theorem process_integrable {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) (n : ℕ) :
    Integrable (P.process n) P.μ :=
  P.process_integrable n

/--
Checked mathlib wrapper: composing a process slice with an iterate of the
measure-preserving transformation preserves integrability.
-/
theorem process_integrable_comp_iterate {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) (m n : ℕ) :
    Integrable (P.process n ∘ (P.T^[m])) P.μ :=
  (transformation_iterate_measurePreserving P m).integrable_comp_of_integrable
    (P.process_integrable n)

/--
Checked expectation-side wrapper: composing a process slice with a
measure-preserving iterate leaves its Bochner integral unchanged.
-/
theorem integral_process_comp_iterate {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) (m n : ℕ) :
    (∫ ω, P.process n ((P.T^[m]) ω) ∂P.μ) =
      ∫ ω, P.process n ω ∂P.μ := by
  let hmp := transformation_iterate_measurePreserving P m
  calc
    (∫ ω, P.process n ((P.T^[m]) ω) ∂P.μ) =
        ∫ ω, P.process n ω ∂Measure.map (P.T^[m]) P.μ := by
      refine (integral_map hmp.aemeasurable ?_).symm
      simpa [hmp.map_eq] using (P.process_integrable n).aestronglyMeasurable
    _ = ∫ ω, P.process n ω ∂P.μ := by
      rw [hmp.map_eq]

/--
Expectation subadditivity from the a.e. cocycle inequality and measure
preservation.

This is the local formalization leaf requested by the Stage1 child task.  It
does not prove Kingman's theorem; it closes only the expectation-level
subadditivity bridge for one pair of indices.
-/
theorem expectation_subadditive_of_ae_cocycle_le {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) (m n : ℕ)
    (hineq :
      P.process (m + n) ≤ᵐ[P.μ]
        (fun ω => P.process m ω + P.process n ((P.T^[m]) ω))) :
    (∫ ω, P.process (m + n) ω ∂P.μ) ≤
      (∫ ω, P.process m ω ∂P.μ) + ∫ ω, P.process n ω ∂P.μ := by
  have hright :
      Integrable (fun ω => P.process m ω + P.process n ((P.T^[m]) ω)) P.μ :=
    (P.process_integrable m).add (process_integrable_comp_iterate P m n)
  calc
    (∫ ω, P.process (m + n) ω ∂P.μ) ≤
        ∫ ω, P.process m ω + P.process n ((P.T^[m]) ω) ∂P.μ :=
      integral_mono_ae (P.process_integrable (m + n)) hright hineq
    _ = (∫ ω, P.process m ω ∂P.μ) +
          ∫ ω, P.process n ((P.T^[m]) ω) ∂P.μ := by
      simpa only [Function.comp_apply] using
        (integral_add (P.process_integrable m) (process_integrable_comp_iterate P m n))
    _ = (∫ ω, P.process m ω ∂P.μ) + ∫ ω, P.process n ω ∂P.μ := by
      rw [integral_process_comp_iterate P m n]

/-- Project the a.e. zero normalization at time zero. -/
theorem process_zero_ae {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) :
    P.process 0 =ᵐ[P.μ] fun _ => 0 :=
  P.process_zero

/-- Project the subadditive cocycle boundary. -/
theorem subadditive_cocycle_boundary {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) (m n : ℕ) :
    P.process (m + n) =ᵐ[P.μ]
        (fun ω => P.process m ω + P.process n ((P.T^[m]) ω))
      ∨ P.process (m + n) ≤ᵐ[P.μ]
        (fun ω => P.process m ω + P.process n ((P.T^[m]) ω)) :=
  P.subadditive_cocycle m n

/-- Project the lower bound on expected normalized values. -/
theorem lowerBoundedExpectedAverages {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω) :
    ∃ C : ℝ, ∀ n : ℕ, n ≠ 0 → C ≤ expectedAverage P n :=
  P.lowerBoundedExpectedAverages

/--
Checked mathlib wrapper: deterministic Fekete convergence for a real-valued
subadditive sequence.

This is an anchor for the expectation-level branch of Kingman's theorem; it is
not the stochastic pointwise theorem.
-/
theorem deterministic_fekete_tendsto
    {u : ℕ → ℝ} (h : Subadditive u)
    (hbdd : BddBelow (range fun n => u n / n)) :
    Tendsto (fun n => u n / n) atTop (𝓝 (Subadditive.lim h)) :=
  h.tendsto_lim hbdd

/--
Checked mathlib wrapper: an a.e. invariant, a.e. strongly measurable real
function under an ergodic map is a.e. constant.

This closes only the invariant-limit-to-constant branch, assuming a limit and
its invariance have already been obtained.
-/
theorem ergodic_limit_const_wrapper {Ω : Type u} [MeasurableSpace Ω]
    (P : KingmanProcess Ω)
    (hlim_meas : AEStronglyMeasurable P.limit P.μ)
    (hinv : P.limit ∘ P.T =ᵐ[P.μ] P.limit) :
    ∃ c : ℝ, P.limit =ᵐ[P.μ] const Ω c :=
  P.transformation_ergodic.ae_eq_const_of_ae_eq_comp_ae hlim_meas hinv

/-- mathlib modules checked while locating repo-local Kingman anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Subadditive",
  "Mathlib.Dynamics.BirkhoffSum.Basic",
  "Mathlib.Dynamics.BirkhoffSum.Average",
  "Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving",
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.Function",
  "Mathlib.MeasureTheory.Function.L1Space.Integrable",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.Probability.Martingale.Convergence"
]

/--
Integration-ready row for the public mathlib anchor table requested for the
Kingman Stage1 backfill.

The `checkedBy` field names the repo-local declaration in this file that
exercises the anchor under `lake env lean`; it is not a terminal Kingman proof.
-/
structure PublicMathlibAnchorRow where
  anchor : String
  moduleName : String
  checkedBy : String
  role : String
  closureStatus : String

/-- Public mathlib anchor table for the currently checked Kingman-adjacent APIs. -/
def publicMathlibAnchorTable : List PublicMathlibAnchorRow := [
  {
    anchor := "Subadditive.tendsto_lim"
    moduleName := "Mathlib.Analysis.Subadditive"
    checkedBy := "deterministic_fekete_tendsto"
    role := "Fekete convergence for deterministic subadditive real sequences; " ++
      "supports only the expectation-level branch, not pointwise Kingman."
    closureStatus := "local_wrapper_upstream_mathlib"
  },
  {
    anchor := "MeasureTheory.MeasurePreserving.iterate"
    moduleName := "Mathlib.Dynamics.Ergodic.MeasurePreserving"
    checkedBy := "transformation_iterate_measurePreserving"
    role := "Transports measure preservation from the ergodic transformation " ++
      "to all natural iterates T^[n]."
    closureStatus := "local_wrapper_upstream_mathlib"
  },
  {
    anchor := "MeasureTheory.MeasurePreserving.integrable_comp_of_integrable"
    moduleName := "Mathlib.MeasureTheory.Function.L1Space.Integrable"
    checkedBy := "process_integrable_comp_iterate"
    role := "Pulls integrability of each process slice through a " ++
      "measure-preserving iterate."
    closureStatus := "local_wrapper_upstream_mathlib"
  },
  {
    anchor := "Ergodic.ae_eq_const_of_ae_eq_comp_ae"
    moduleName := "Mathlib.Dynamics.Ergodic.Function"
    checkedBy := "ergodic_limit_const_wrapper"
    role := "Turns an a.e. invariant a.e. strongly measurable limit into an " ++
      "a.e. constant under ergodicity, after existence and invariance are proved."
    closureStatus := "local_wrapper_upstream_mathlib"
  }
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MeasurePreserving",
  "MeasureTheory.MeasurePreserving.iterate",
  "MeasureTheory.MeasurePreserving.integrable_comp_of_integrable",
  "MeasureTheory.QuasiMeasurePreserving",
  "Ergodic",
  "Ergodic.ae_eq_const_of_ae_eq_comp_ae",
  "birkhoffSum",
  "birkhoffAverage",
  "Subadditive",
  "Subadditive.lim",
  "Subadditive.tendsto_lim",
  "TendstoInMeasure",
  "MeasureTheory.Integrable.tendsto_ae_condExp"
]

/-- Search terms that did not locate a terminal Kingman theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Kingman",
  "subadditive ergodic theorem",
  "subadditive process",
  "SubadditiveErgodic",
  "pointwise subadditive",
  "ergodic theorem subadditive",
  "ae Tendsto normalized subadditive",
  "Tendsto (fun n => process n _ / n)"
]

/--
External Lean 4 anchor-audit query row for Kingman's theorem.

This is a checked data contract for the serial public backfill.  A search hit
does not close the theorem unless the hit is turned into a pinned dependency,
vendored proof body, or repo-local wrapper that passes the local Lake command.
-/
structure ExternalLeanAnchorAuditQuery where
  query : String
  requiredHitRecord : String
  completionGate : String

/--
GitHub code-search queries that must be re-run before any external-upstream
Kingman claim is made.
-/
def externalLeanAnchorAuditQueries : List ExternalLeanAnchorAuditQuery := [
  {
    query := "Kingman language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "theorem or definition name, placeholder status, license, and dependency " ++
      "summary"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  },
  {
    query := "SubadditiveErgodic language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "theorem or definition name, placeholder status, license, and dependency " ++
      "summary"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  },
  {
    query := "\"subadditive ergodic theorem\" language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "theorem or definition name, placeholder status, license, and dependency " ++
      "summary"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  }
]

/--
Machine-readable external-anchor completion guard.

This remains false until an external Lean 4 Kingman proof is pinned or vendored
into this repository's Lake closure and a local wrapper or imported theorem
passes validation.
-/
def externalAnchorOnlyCompletionAllowed : Bool := false

/-- The external-anchor-only completion guard is intentionally closed. -/
theorem externalAnchorOnlyCompletionAllowed_eq_false :
    externalAnchorOnlyCompletionAllowed = false :=
  rfl

/-- Candidate proof-route families for the future terminal Kingman proof. -/
inductive KingmanProofRoute where
  | maximalInequalityUpcrossing
  | martingaleStyleReduction

/--
Selected first implementation route for the local Kingman proof package.

The maximal-inequality/upcrossing route is selected because the current local
closure already has measure-preserving iterates, integrability transport,
expectation subadditivity, deterministic Fekete convergence, and ergodic
invariant-function constancy.  The martingale-style route is kept as an
alternative audit target, but no checked subadditive-to-martingale reduction is
currently available in the repo-local Lean closure.
-/
def selectedKingmanProofRoute : KingmanProofRoute :=
  KingmanProofRoute.maximalInequalityUpcrossing

/-- The route selection is intentionally fixed to the maximal/upcrossing branch. -/
theorem selectedKingmanProofRoute_eq :
    selectedKingmanProofRoute = KingmanProofRoute.maximalInequalityUpcrossing :=
  rfl

/--
Integration-ready route leaf for the future Kingman proof tree.

These rows are checked Lean data, not completed proof leaves.  `localStatus`
must remain non-completed until the named target is backed by a local proof
body, a checked mathlib wrapper, or a pinned upstream dependency in the local
Lake closure.
-/
structure KingmanProofRouteLeaf where
  id : String
  route : KingmanProofRoute
  package : String
  target : String
  localStatus : String
  budget : String

/--
Selected maximal-inequality/upcrossing proof route, split into M0387-sized
future leaves.  The terminal theorem remains open.
-/
def selectedMaximalUpcrossingRouteLeaves : List KingmanProofRouteLeaf := [
  {
    id := "S1-M-249-R01"
    route := selectedKingmanProofRoute
    package := "cocycle_to_expectation_subadditivity"
    target := "Keep `expectation_subadditive_of_ae_cocycle_le` as the checked " ++
      "expectation bridge and lift it to a positive-index `Subadditive` " ++
      "sequence for deterministic Fekete use."
    localStatus := "partial_local_proof_body"
    budget := "<=100 steps for the positive-index Subadditive wrapper"
  },
  {
    id := "S1-M-249-R02"
    route := selectedKingmanProofRoute
    package := "truncation_and_integrable_envelopes"
    target := "Define truncated excess processes and prove integrability, " ++
      "measurability, monotonicity, and finite-horizon sum bounds needed by " ++
      "the maximal inequality."
    localStatus := "formalization_debt"
    budget := "<=100 steps per truncation/envelope lemma"
  },
  {
    id := "S1-M-249-R03"
    route := selectedKingmanProofRoute
    package := "maximal_inequality"
    target := "Prove the subadditive maximal inequality for the selected " ++
      "truncated process over finite horizons, using measure-preserving " ++
      "iterate invariance and expectation subadditivity."
    localStatus := "formalization_debt"
    budget := "<=100 steps per finite-horizon inequality leaf"
  },
  {
    id := "S1-M-249-R04"
    route := selectedKingmanProofRoute
    package := "upcrossing_convergence"
    target := "Convert the maximal inequality into a finite-upcrossings " ++
      "statement and then into a.e. convergence of normalized process " ++
      "averages."
    localStatus := "formalization_debt"
    budget := "<=100 steps per upcrossing/counting/convergence leaf"
  },
  {
    id := "S1-M-249-R05"
    route := selectedKingmanProofRoute
    package := "limit_invariance_and_ergodic_constant"
    target := "Prove invariance of the a.e. limit, apply " ++
      "`ergodic_limit_const_wrapper`, and identify the constant with " ++
      "`ergodicKingmanValue` using expectation subadditivity and Fekete " ++
      "convergence."
    localStatus := "formalization_debt"
    budget := "<=100 steps per invariance/constant-identification leaf"
  },
  {
    id := "S1-M-249-R06"
    route := KingmanProofRoute.martingaleStyleReduction
    package := "alternative_martingale_reduction_audit"
    target := "Audit whether a checked martingale-style reduction can replace " ++
      "or shorten the maximal/upcrossing branch; require exact theorem names " ++
      "and local Lake validation before changing the selected route."
    localStatus := "audit_only_alternative"
    budget := "<=100 steps for any future checked reduction wrapper"
  }
]

/-- Route-selection summary for serial public backfill. -/
def proofRouteBackfillSummary : List String := [
  "selected route: maximal inequality/upcrossing, recorded by " ++
    "selectedKingmanProofRoute and selectedKingmanProofRoute_eq",
  "reason: current local closure already checks measure-preserving iterates, " ++
    "integrability transport, expectation subadditivity, deterministic " ++
    "Fekete convergence, and ergodic invariant-function constancy",
  "remaining route leaves: positive-index Subadditive expectation wrapper, " ++
    "truncation/integrable envelopes, subadditive maximal inequality, " ++
    "upcrossing-to-a.e.-convergence bridge, limit invariance, and " ++
    "ergodic-constant identification",
  "martingale-style reduction remains an audit-only alternative until an exact " ++
    "repo-local checked reduction theorem is found or implemented"
]

/--
Machine-readable completion gate for this Stage1 slot.

The value remains `false` because this file has a checked statement shape and
local mathlib wrappers, but no terminal Kingman proof and no pinned upstream
wrapper inside the repo-local Lean validation closure.
-/
def repoLocalCompletionGateSatisfied : Bool := false

/--
Machine-readable closure checklist item for the public Stage1 completion gate.

The public checkbox for S1-M-249 must remain open until `validationCommand`
passes and `closureEvidenceRequired` is discharged by either a terminal local
Kingman theorem or a pinned upstream wrapper in the repo-local Lake closure.
-/
structure ClosureGateChecklistItem where
  id : String
  validationCommand : String
  closureEvidenceRequired : String
  currentClosureEvidence : String
  maySetCompletionCheckbox : Bool

/--
Integration-ready closure gate requested by child task S1-M-249-C006.

This is checked data for the serial public backfill.  The gate is intentionally
closed because the file has wrappers and partial leaves, but no terminal local
Kingman theorem and no pinned upstream wrapper.
-/
def closureGateChecklistItem : ClosureGateChecklistItem := {
  id := "S1-M-249-closure-gate"
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_249.lean"
  closureEvidenceRequired :=
    "Either a terminal repo-local Kingman theorem, or a pinned/imported upstream " ++
      "wrapper theorem in this repository's Lake closure, must pass the same " ++
      "validation command before any public completion checkbox is set."
  currentClosureEvidence :=
    "No terminal Kingman theorem and no pinned upstream wrapper are present; " ++
      "current checked declarations are statement-shape and anchor wrappers only."
  maySetCompletionCheckbox := repoLocalCompletionGateSatisfied
}

/-- The S1-M-249 public completion checkbox is blocked in the current artifact. -/
theorem closureGateChecklistItem_blocks_completion :
    closureGateChecklistItem.maySetCompletionCheckbox = false :=
  rfl

/-- Integration-ready summary lines for the serial public Stage1 backfill. -/
def publicBackfillSummary : List String := [
  "checked statement shape only: KingmanProcess, normalizedProcess, expectedAverage, " ++
    "ergodicKingmanValue, KingmanConclusion, StatementShape, statementShape_iff",
  "public mathlib anchor table ready: publicMathlibAnchorTable records " ++
    "Subadditive.tendsto_lim, MeasurePreserving.iterate, " ++
    "MeasurePreserving.integrable_comp_of_integrable, and " ++
    "Ergodic.ae_eq_const_of_ae_eq_comp_ae",
  "checked mathlib wrappers: transformation_measurePreserving, " ++
    "transformation_iterate_measurePreserving, process_integrable_comp_iterate, " ++
    "deterministic_fekete_tendsto, ergodic_limit_const_wrapper",
  "checked expectation subadditivity leaf: integral_process_comp_iterate and " ++
    "expectation_subadditive_of_ae_cocycle_le prove expectation subadditivity " ++
    "for one pair of indices from the a.e. cocycle inequality and " ++
    "measure-preserving iterate invariance",
  "proof route selected but not completed: selectedKingmanProofRoute fixes the " ++
    "first implementation route to maximal inequality/upcrossing, and " ++
    "selectedMaximalUpcrossingRouteLeaves records remaining M0387-sized leaves",
  "closure gate item ready: closureGateChecklistItem requires `cd " ++
    "Formalizations/Lean && lake env lean " ++
    "AwesomeTheorems/Stage1/S1_M_249.lean` plus either a terminal local " ++
    "Kingman theorem or a pinned upstream wrapper before any public completion " ++
    "checkbox is set",
  "completion status: no terminal Kingman theorem, no local proof body, " ++
    "no pinned upstream wrapper; remaining debt is formalization_debt unless an " ++
    "external proof is later found and integrated"
]

end S1_M_249
end Stage1
end AwesomeTheorems
