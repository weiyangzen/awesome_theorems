import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Analytic.Within
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.MeasureTheory.Integral.CircleIntegral
import Mathlib.Analysis.Complex.RemovableSingularity
import Mathlib.Analysis.Complex.Spectrum
import Mathlib.Analysis.Normed.Operator.Compact
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Analysis.Fourier.AddCircle

/-!
# S1-M-178 / THM-M-1559: Riemann-Hilbert problem

This Stage1 artifact records a conservative Lean 4 boundary for the
Riemann-Hilbert problem as it appears in integrable-systems analytic
factorization problems.

The pinned mathlib snapshot has complex analytic functions, Cauchy integral
formulae, continuous linear operators, compact operators, spectra, and the
Fredholm alternative.  It does not expose a terminal theorem for
operator-valued/matrix-valued Riemann-Hilbert jump factorization with
normalization and integrable-system compatibility data.  The declarations below
therefore normalize the statement boundary and provide small checked wrappers
around available analytic and operator-theoretic anchors.
-/

noncomputable section

open scoped Topology
open Metric
open Module End
open Complex

universe u

namespace AwesomeTheorems.Stage1.S1_M_178

/--
Operator-valued loop used for a normalized Riemann-Hilbert jump problem.

In finite-dimensional matrix formulations this should later be specialized to
matrix-valued maps or to continuous linear automorphisms.  The current boundary
uses continuous linear operators so that it sits inside existing mathlib
analysis and Fredholm APIs.
-/
abbrev OperatorLoop (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E] :
    Type u :=
  ℂ → E →L[ℂ] E

/--
Input data for an operator-valued Riemann-Hilbert jump problem.

The analytic contour geometry, trace spaces, invertibility of the jump, and the
integrable-system compatibility conditions are not yet concrete mathlib APIs,
so they are isolated as explicit fields.
-/
structure RiemannHilbertJumpData
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E] : Type u where
  contour : Set ℂ
  interiorDomain : Set ℂ
  exteriorDomain : Set ℂ
  jump : OperatorLoop E
  normalization : E →L[ℂ] E
  contour_closed : IsClosed contour
  interior_open : IsOpen interiorDomain
  exterior_open : IsOpen exteriorDomain
  interior_exterior_disjoint : Disjoint interiorDomain exteriorDomain
  contour_is_common_boundary : Prop
  jump_continuousOn : ContinuousOn jump contour
  jump_invertible_on_contour : Prop
  normalization_compatible : Prop
  integrable_system_compatibility : Prop

/--
Candidate solution object for a Riemann-Hilbert jump problem.

The plus/minus analytic factors are represented by operator-valued analytic
maps on the two complementary domains.  Boundary traces, jump relation,
normalization at infinity, and uniqueness class are retained as proposition
fields until concrete contour-trace and automorphism APIs are selected.
-/
structure RiemannHilbertSolution
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (D : RiemannHilbertJumpData E) : Type u where
  plus : OperatorLoop E
  minus : OperatorLoop E
  plus_analytic : AnalyticOn ℂ plus D.interiorDomain
  minus_analytic : AnalyticOn ℂ minus D.exteriorDomain
  plusBoundaryTrace : OperatorLoop E
  minusBoundaryTrace : OperatorLoop E
  trace_agrees_plus : Prop
  trace_agrees_plus_holds : trace_agrees_plus
  trace_agrees_minus : Prop
  trace_agrees_minus_holds : trace_agrees_minus
  jump_relation : Prop
  jump_relation_holds : jump_relation
  normalization_at_infinity : Prop
  normalization_at_infinity_holds : normalization_at_infinity
  unique_in_class : Prop
  unique_in_class_holds : unique_in_class

/--
Normalized Stage1 statement-shape candidate for THM-M-1559.

For every complete complex normed space and every admissible Riemann-Hilbert
jump datum, the intended theorem asserts existence of analytic plus/minus
factors satisfying the boundary jump relation and normalization conditions.

This is only a statement boundary.  The terminal proof requires concrete
contour traces, automorphism-valued jumps, singular-integral/Fredholm analysis,
and the integrable-system compatibility theorem.
-/
def StatementShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E] [CompleteSpace E]
    (D : RiemannHilbertJumpData E),
      D.contour_is_common_boundary →
        D.jump_invertible_on_contour →
          D.normalization_compatible →
            D.integrable_system_compatibility →
              Nonempty (RiemannHilbertSolution E D)

/--
Public statement-normalization note for THM-M-1559.

`AwesomeTheorems.Stage1.S1_M_178.StatementShape` is the current repo-local Lean
boundary: it packages the Riemann-Hilbert problem as an operator-valued
jump-data existence statement with analytic plus/minus factors, abstract
boundary traces, a jump relation, normalization, and uniqueness data.  This
boundary is intentionally not a terminal Riemann-Hilbert proof; contour
regularity, trace spaces, automorphism-valued jumps, Plemelj-Sokhotski and
Cauchy singular-integral estimates, Fredholm/small-norm solvability,
integrable-system compatibility, normalization, and uniqueness still need
concrete APIs or pinned proof dependencies.
-/
def statementNormalizationNote : String :=
  "AwesomeTheorems.Stage1.S1_M_178.StatementShape is the current repo-local " ++
  "Lean boundary for THM-M-1559; it is not a terminal Riemann-Hilbert proof."

/--
Canonical Stage1 split of the currently missing formal APIs for THM-M-1559.

These are proof obligations, not assumptions and not terminal theorem claims.
They name the interfaces that must eventually replace the abstract proposition
fields in `RiemannHilbertJumpData` and `RiemannHilbertSolution`.
-/
inductive MissingAPI : Type
  | contourRegularity
  | boundaryTraceSpaces
  | automorphismMatrixJumps
  | plemeljSokhotskiFormula
  | cauchySingularIntegralBoundedness
  | fredholmSmallNormSolvability
  | integrableSystemCompatibility
  | normalization
  | uniqueness
  deriving DecidableEq, Repr

namespace MissingAPI

/-- Stable human-readable label for a missing Riemann-Hilbert formal API. -/
def label : MissingAPI → String
  | contourRegularity => "contour regularity"
  | boundaryTraceSpaces => "boundary trace spaces"
  | automorphismMatrixJumps => "automorphism/matrix-valued jumps"
  | plemeljSokhotskiFormula => "Plemelj-Sokhotski formula"
  | cauchySingularIntegralBoundedness =>
      "Cauchy singular-integral boundedness"
  | fredholmSmallNormSolvability => "Fredholm/small-norm solvability"
  | integrableSystemCompatibility => "integrable-system compatibility"
  | normalization => "normalization"
  | uniqueness => "uniqueness"

/--
Repo-local boundary currently blocking this API.

The strings intentionally describe integration targets rather than providing
new axioms.  Each target remains `formalization_debt` until backed by a local
proof body, pinned mathlib wrapper, or pinned external dependency.
-/
def localBoundary : MissingAPI → String
  | contourRegularity =>
      "Replace the abstract contour set by a rectifiable/Jordan/Carleson-contour API with inside/outside boundary lemmas."
  | boundaryTraceSpaces =>
      "Select Hardy/Sobolev/Hilbert boundary trace spaces and prove plus/minus trace agreement for analytic factors."
  | automorphismMatrixJumps =>
      "Specialize operator loops to invertible continuous linear maps or finite-dimensional matrix-valued jumps."
  | plemeljSokhotskiFormula =>
      "Prove the plus/minus nontangential boundary values of the Cauchy transform and their jump relation."
  | cauchySingularIntegralBoundedness =>
      "Prove boundedness of the Cauchy singular integral on the selected trace spaces."
  | fredholmSmallNormSolvability =>
      "Connect singular-integral equations to Fredholm alternative and small-norm Neumann-series solvability."
  | integrableSystemCompatibility =>
      "State and prove compatibility of the Riemann-Hilbert data with the intended Lax/isomonodromy system."
  | normalization =>
      "Formalize normalization at infinity or a selected base point and its interaction with analytic continuation."
  | uniqueness =>
      "Prove uniqueness in the normalized solution class, typically through a Liouville/removable-singularity argument."

end MissingAPI

/-- Exact Stage1 missing-API split required before a terminal Riemann-Hilbert proof. -/
def missingAPISplit : List MissingAPI := [
  MissingAPI.contourRegularity,
  MissingAPI.boundaryTraceSpaces,
  MissingAPI.automorphismMatrixJumps,
  MissingAPI.plemeljSokhotskiFormula,
  MissingAPI.cauchySingularIntegralBoundedness,
  MissingAPI.fredholmSmallNormSolvability,
  MissingAPI.integrableSystemCompatibility,
  MissingAPI.normalization,
  MissingAPI.uniqueness
]

/-- Human-readable checked labels for `missingAPISplit`. -/
def missingAPISplitLabels : List String :=
  missingAPISplit.map MissingAPI.label

/-- Checked normalization of the exact missing-API inventory. -/
theorem missingAPISplit_eq :
    missingAPISplit = [
      MissingAPI.contourRegularity,
      MissingAPI.boundaryTraceSpaces,
      MissingAPI.automorphismMatrixJumps,
      MissingAPI.plemeljSokhotskiFormula,
      MissingAPI.cauchySingularIntegralBoundedness,
      MissingAPI.fredholmSmallNormSolvability,
      MissingAPI.integrableSystemCompatibility,
      MissingAPI.normalization,
      MissingAPI.uniqueness
    ] :=
  rfl

/-- The current Riemann-Hilbert missing-API inventory has nine leaves. -/
theorem missingAPISplit_length : missingAPISplit.length = 9 :=
  rfl

/-- Checked normalization of the labels exposed for public backfill. -/
theorem missingAPISplitLabels_eq :
    missingAPISplitLabels = [
      "contour regularity",
      "boundary trace spaces",
      "automorphism/matrix-valued jumps",
      "Plemelj-Sokhotski formula",
      "Cauchy singular-integral boundedness",
      "Fredholm/small-norm solvability",
      "integrable-system compatibility",
      "normalization",
      "uniqueness"
    ] :=
  rfl

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E] [CompleteSpace E]
      (D : RiemannHilbertJumpData E),
        D.contour_is_common_boundary →
          D.jump_invertible_on_contour →
            D.normalization_compatible →
              D.integrable_system_compatibility →
                Nonempty (RiemannHilbertSolution E D)) :
    StatementShape.{u} :=
  h

/-- Projection wrapper: a solution exposes its plus-side analytic factor. -/
theorem RiemannHilbertSolution.plus_analytic_on
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {D : RiemannHilbertJumpData E} (S : RiemannHilbertSolution E D) :
    AnalyticOn ℂ S.plus D.interiorDomain :=
  S.plus_analytic

/-- Projection wrapper: a solution exposes its minus-side analytic factor. -/
theorem RiemannHilbertSolution.minus_analytic_on
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {D : RiemannHilbertJumpData E} (S : RiemannHilbertSolution E D) :
    AnalyticOn ℂ S.minus D.exteriorDomain :=
  S.minus_analytic

/-- Projection wrapper: a solution satisfies its abstract jump relation. -/
theorem RiemannHilbertSolution.satisfies_jump_relation
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {D : RiemannHilbertJumpData E} (S : RiemannHilbertSolution E D) :
    S.jump_relation :=
  S.jump_relation_holds

/-- Projection wrapper: a solution satisfies its abstract normalization condition. -/
theorem RiemannHilbertSolution.satisfies_normalization
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {D : RiemannHilbertJumpData E} (S : RiemannHilbertSolution E D) :
    S.normalization_at_infinity :=
  S.normalization_at_infinity_holds

/--
Checked complex-analysis anchor: the Cauchy integral formula on a disk for
Banach-valued functions.
-/
theorem cauchy_integral_formula_anchor
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E] [CompleteSpace E]
    {R : ℝ} {c w : ℂ} {f : ℂ → E}
    (hd : DifferentiableOn ℂ f (closedBall c R)) (hw : w ∈ ball c R) :
    (∮ z in C(c, R), (z - w)⁻¹ • f z) = (2 * Real.pi * I : ℂ) • f w :=
  DifferentiableOn.circleIntegral_sub_inv_smul hd hw

/--
Checked operator-theoretic anchor: the Fredholm alternative for compact
operators on a complete normed complex vector space.
-/
theorem compactOperator_fredholmAlternative_anchor
    {X : Type u} [NormedAddCommGroup X] [NormedSpace ℂ X] [CompleteSpace X]
    {T : X →L[ℂ] X} (hT : IsCompactOperator T) {μ : ℂ} (hμ : μ ≠ 0) :
    HasEigenvalue (T : End ℂ X) μ ∨ μ ∈ resolventSet ℂ T :=
  IsCompactOperator.hasEigenvalue_or_mem_resolventSet hT hμ

/-- mathlib modules checked while locating repo-local Riemann-Hilbert anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Analytic.Basic",
  "Mathlib.Analysis.Analytic.Within",
  "Mathlib.Analysis.Analytic.IsolatedZeros",
  "Mathlib.Analysis.Complex.CauchyIntegral",
  "Mathlib.Analysis.Complex.RemovableSingularity",
  "Mathlib.Analysis.Complex.Spectrum",
  "Mathlib.Analysis.Normed.Operator.Compact",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.Analysis.Normed.Operator.Banach",
  "Mathlib.Analysis.Fourier.AddCircle",
  "Mathlib.MeasureTheory.Integral.CircleIntegral"
]

/-- Nearby checked names used or audited for this Stage1 statement boundary. -/
def mathlibAnchorNames : List String := [
  "AnalyticOn",
  "AnalyticOnNhd",
  "DifferentiableOn.circleIntegral_sub_inv_smul",
  "circleIntegral_sub_inv_smul_of_differentiable_on_off_countable",
  "DiffContOnCl.circleIntegral_sub_inv_smul",
  "IsCompactOperator",
  "IsCompactOperator.hasEigenvalue_or_mem_resolventSet",
  "IsCompactOperator.hasEigenvalue_iff_mem_spectrum",
  "resolventSet",
  "spectrum",
  "fourierBasis"
]

/--
Search terms that did not locate a terminal Riemann-Hilbert theorem in the
local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "RiemannHilbert",
  "Riemann-Hilbert",
  "Riemann Hilbert",
  "jump factorization",
  "matrix Riemann-Hilbert",
  "Birkhoff factorization",
  "monodromy data",
  "isomonodromy",
  "Hardy projection",
  "Cauchy singular integral",
  "Plemelj",
  "Sokhotski"
]

/-- Exact external-audit query inventory requested for `THM-M-1559.external-audit`. -/
def externalAuditSearchTerms : List String := [
  "RiemannHilbert",
  "Riemann-Hilbert",
  "jump factorization",
  "Birkhoff factorization",
  "isomonodromy",
  "Hardy projection",
  "Cauchy singular integral",
  "Plemelj",
  "Sokhotski",
  "Toeplitz"
]

/--
Local pinned-mathlib hits for the requested external-audit terms.

`Toeplitz` appears only through Hellinger--Toeplitz operator-theory results,
not through Riemann-Hilbert, Hardy projection, or singular-integral machinery.
-/
def externalAuditLocalMathlibHits : List String := [
  "Mathlib.Analysis.InnerProductSpace.Symmetric: LinearMap.IsSymmetric.continuous",
  "Mathlib.Analysis.InnerProductSpace.Adjoint: LinearMap.IsSymmetric.toSelfAdjoint"
]

/--
Machine-closure states allowed by the Stage1 integration gate.

Only the first three states can support a repo-local completion claim.  The
anchor-only state records an external pointer that has not entered this
repository's checked dependency closure, and therefore cannot close the
Riemann-Hilbert task.
-/
inductive MachineClosureStatus : Type
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  | notRepoLocalClosed
  deriving DecidableEq, Repr

namespace MachineClosureStatus

/-- Whether this status can support a repo-local completed theorem claim. -/
def repoLocalCompleted : MachineClosureStatus → Bool
  | localProofBody => true
  | localWrapperUpstreamMathlib => true
  | externalUpstreamPinned => true
  | externalUpstreamAnchorOnly => false
  | notRepoLocalClosed => false

end MachineClosureStatus

/--
Current machine status for the terminal THM-M-1559 Riemann-Hilbert theorem.

The surrounding declarations are checked statement/audit surfaces only; no
local proof body, mathlib wrapper, or pinned external dependency currently
proves `StatementShape`.
-/
def terminalRiemannHilbertMachineStatus : MachineClosureStatus :=
  MachineClosureStatus.notRepoLocalClosed

/--
Concrete blockers that prevent any public completion claim for the terminal
Riemann-Hilbert theorem under the Stage1 integration gate.
-/
def integrationGateBlockers : List String := [
  "No authenticated external Lean 4 search result has identified a terminal Riemann-Hilbert closure.",
  "The pinned local mathlib audit found no terminal Riemann-Hilbert theorem or jump-factorization theorem.",
  "A future external Lean 4 closure must be pinned/imported/checked locally, or assigned a concrete Lake/toolchain/license blocker, before any public completion claim."
]

/-- Current integration-gate decision for the terminal THM-M-1559 theorem. -/
def terminalCompletionAllowedByIntegrationGate : Bool :=
  terminalRiemannHilbertMachineStatus.repoLocalCompleted

#check OperatorLoop
#check RiemannHilbertJumpData
#check RiemannHilbertSolution
#check StatementShape
#check statementNormalizationNote
#check MissingAPI
#check missingAPISplit
#check missingAPISplitLabels
#check missingAPISplit_length
#check StatementShape.intro
#check cauchy_integral_formula_anchor
#check compactOperator_fredholmAlternative_anchor
#check externalAuditSearchTerms
#check externalAuditLocalMathlibHits
#check MachineClosureStatus
#check terminalRiemannHilbertMachineStatus
#check integrationGateBlockers
#check terminalCompletionAllowedByIntegrationGate

/--
Pinned mathlib revision audited for the THM-M-1559 Stage1 Riemann-Hilbert
statement boundary.
-/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Exact module inventory requested by `THM-M-1559.mathlib-audit`.

The imports at the top of this file check that these modules are available in
the pinned local Lean environment.
-/
def mathlibAuditAvailableModules : List String := [
  "Analysis.Analytic.Basic",
  "Analysis.Analytic.Within",
  "Analysis.Analytic.IsolatedZeros",
  "Analysis.Complex.CauchyIntegral",
  "MeasureTheory.Integral.CircleIntegral",
  "Analysis.Complex.RemovableSingularity",
  "Analysis.Complex.Spectrum",
  "Analysis.Normed.Operator.Compact",
  "Analysis.Normed.Operator.FredholmAlternative",
  "Analysis.Fourier.AddCircle"
]

/-- Checked normalization of the pinned revision audit string. -/
theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision =
      "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked normalization of the exact mathlib module audit list. -/
theorem mathlibAuditAvailableModules_eq :
    mathlibAuditAvailableModules = [
      "Analysis.Analytic.Basic",
      "Analysis.Analytic.Within",
      "Analysis.Analytic.IsolatedZeros",
      "Analysis.Complex.CauchyIntegral",
      "MeasureTheory.Integral.CircleIntegral",
      "Analysis.Complex.RemovableSingularity",
      "Analysis.Complex.Spectrum",
      "Analysis.Normed.Operator.Compact",
      "Analysis.Normed.Operator.FredholmAlternative",
      "Analysis.Fourier.AddCircle"
    ] :=
  rfl

/-- Checked normalization of the exact external-audit query inventory. -/
theorem externalAuditSearchTerms_eq :
    externalAuditSearchTerms = [
      "RiemannHilbert",
      "Riemann-Hilbert",
      "jump factorization",
      "Birkhoff factorization",
      "isomonodromy",
      "Hardy projection",
      "Cauchy singular integral",
      "Plemelj",
      "Sokhotski",
      "Toeplitz"
    ] :=
  rfl

/-- Checked normalization of local pinned-mathlib hits for external audit terms. -/
theorem externalAuditLocalMathlibHits_eq :
    externalAuditLocalMathlibHits = [
      "Mathlib.Analysis.InnerProductSpace.Symmetric: LinearMap.IsSymmetric.continuous",
      "Mathlib.Analysis.InnerProductSpace.Adjoint: LinearMap.IsSymmetric.toSelfAdjoint"
    ] :=
  rfl

/-- Checked current status: the terminal theorem is not repo-locally closed. -/
theorem terminalRiemannHilbertMachineStatus_eq :
    terminalRiemannHilbertMachineStatus =
      MachineClosureStatus.notRepoLocalClosed :=
  rfl

/-- Checked blocker count for the current integration-gate surface. -/
theorem integrationGateBlockers_length :
    integrationGateBlockers.length = 3 :=
  rfl

/--
Checked current gate result: public terminal completion is not allowed from the
present repo-local evidence.
-/
theorem terminalCompletionAllowedByIntegrationGate_eq :
    terminalCompletionAllowedByIntegrationGate = false :=
  rfl

end AwesomeTheorems.Stage1.S1_M_178
