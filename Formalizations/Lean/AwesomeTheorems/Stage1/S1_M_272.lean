import Mathlib.Probability.Moments.Variance

/-!
# S1-M-272 / THM-M-0992: Chebyshev's inequality

This Stage1 artifact records a Lean 4 statement shape for Chebyshev's
inequality over real-valued random variables.  The proof body is a local wrapper
around pinned mathlib theorems in `Mathlib.Probability.Moments.Variance`; it does
not introduce kernel assumptions or placeholders.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped MeasureTheory ProbabilityTheory ENNReal NNReal

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_272

/--
Chebyshev's inequality in the `ℝ≥0∞`-valued variance form.  This version only
requires almost-everywhere strong measurability of the real-valued random
variable.
-/
def ChebyshevEVarianceStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) (X : Ω → ℝ),
    AEStronglyMeasurable X P →
      ∀ c : ℝ≥0,
        c ≠ 0 →
          P {ω | ↑c ≤ |X ω - P[X]|} ≤
            ProbabilityTheory.evariance X P / c ^ 2

/--
Chebyshev's inequality in the usual real variance form for square-integrable
random variables over finite measures.
-/
def ChebyshevVarianceStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsFiniteMeasure P] (X : Ω → ℝ),
    MemLp X 2 P →
      ∀ c : ℝ,
        0 < c →
          P {ω | c ≤ |X ω - P[X]|} ≤
            ENNReal.ofReal (ProbabilityTheory.variance X P / c ^ 2)

/--
Normalized Stage1 statement-shape candidate for the probability-theory
Chebyshev inequality: the extended-variance theorem plus the common
square-integrable real-variance corollary.
-/
def StatementShape : Prop :=
  ChebyshevEVarianceStatement.{u} ∧ ChebyshevVarianceStatement.{u}

/-- Checked mathlib wrapper: Chebyshev's inequality for extended variance. -/
theorem chebyshevEVariance_mathlib
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) {X : Ω → ℝ}
    (hX : AEStronglyMeasurable X P) {c : ℝ≥0} (hc : c ≠ 0) :
    P {ω | ↑c ≤ |X ω - P[X]|} ≤
      ProbabilityTheory.evariance X P / c ^ 2 :=
  ProbabilityTheory.meas_ge_le_evariance_div_sq (μ := P) hX hc

/-- Checked mathlib wrapper: Chebyshev's inequality for real variance. -/
theorem chebyshevVariance_mathlib
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsFiniteMeasure P]
    {X : Ω → ℝ} (hX : MemLp X 2 P) {c : ℝ} (hc : 0 < c) :
    P {ω | c ≤ |X ω - P[X]|} ≤
      ENNReal.ofReal (ProbabilityTheory.variance X P / c ^ 2) :=
  ProbabilityTheory.meas_ge_le_variance_div_sq (μ := P) hX hc

/-- Local wrapper closing the normalized Stage1 statement shape from mathlib. -/
theorem statementShape_mathlib : StatementShape.{u} := by
  constructor
  · intro Ω _ P X hX c hc
    exact chebyshevEVariance_mathlib P hX hc
  · intro Ω _ P _ X hX c hc
    exact chebyshevVariance_mathlib P hX hc

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check ChebyshevEVarianceStatement
#check ChebyshevVarianceStatement
#check chebyshevEVariance_mathlib
#check chebyshevVariance_mathlib
#check statementShape_mathlib
#check ProbabilityTheory.meas_ge_le_evariance_div_sq
#check ProbabilityTheory.meas_ge_le_variance_div_sq
#check ProbabilityTheory.evariance
#check ProbabilityTheory.variance
#check MeasureTheory.MemLp
#check MeasureTheory.AEStronglyMeasurable

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Moments.Variance",
  "Mathlib.MeasureTheory.Integral.Lebesgue.Markov",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.Probability.Notation"
]

/-- Pinned mathlib theorem names wrapped or audited for this Stage1 artifact. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.meas_ge_le_evariance_div_sq",
  "ProbabilityTheory.meas_ge_le_variance_div_sq",
  "ProbabilityTheory.variance_le_expectation_sq",
  "MeasureTheory.meas_ge_le_lintegral_div",
  "MeasureTheory.mul_meas_ge_le_lintegral₀",
  "ProbabilityTheory.evariance",
  "ProbabilityTheory.variance"
]

/-- Search terms used in the pinned local mathlib tree for the anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "Chebyshev",
  "chebyshev",
  "meas_ge_le_variance_div_sq",
  "meas_ge_le_evariance_div_sq",
  "variance",
  "evariance",
  "Markov's inequality",
  "mul_meas_ge_le_lintegral",
  "measure deviation expectation variance"
]

/-- Primary-source pin for the mathlib proof body used by this local wrapper. -/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4, revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-! ## Theorem-tree merge metadata for Stage1 public backfill. -/

/-- The M0992 proof-package ids carried by the private Stage1 theorem tree. -/
def theoremTreePackageIds : List String := [
  "M0992.P0.statement_normalization",
  "M0992.P1.mathlib_object_model",
  "M0992.P2.markov_reduction",
  "M0992.P3.evariance_chebyshev",
  "M0992.P4.variance_chebyshev",
  "M0992.P5.statement_shape_closure",
  "M0992.P6.public_merge_surface",
  "M0992.P7.repo_local_gate"
]

/-- Local leaf ids whose proof/audit units are closed by this checked file. -/
def checkedLocalLeafIds : List String := [
  "M0992-L001",
  "M0992-L002",
  "M0992-L003",
  "M0992-L004",
  "M0992-L005",
  "M0992-L006",
  "M0992-L007"
]

/-- Public merge/status leaf ids that must remain unchecked until integrator backfill. -/
def uncheckedPublicLeafIds : List String := [
  "M0992-L008",
  "M0992-L009",
  "M0992-L010"
]

/--
Repo-local theorem-tree gate note: the checked Lean wrapper closes the local
mathlib-backed proof leaves, but public merge and status leaves remain unchecked.
-/
def theoremTreeMergeGate : String :=
  "Merge M0992.P0 through M0992.P7 and M0992-L001 through M0992-L010 in the public surface; keep M0992-L008, M0992-L009, and M0992-L010 unchecked until public backfill, status synchronization, and clean integrator validation rerun."

/-! ## Public status-gate metadata for Stage1 integration. -/

/--
Public surfaces that must be synchronized before any Stage1 checkbox promotion
for `THM-M-0992`.
-/
def publicStatusGateSurfaces : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md",
  "any authoritative public meta/status surface used by the integrator"
]

/--
Status-gate requirements for the public completion decision.  These are
metadata, not a public completion claim by this Lean artifact.
-/
def publicStatusGateRequirements : List String := [
  "merge the checked StatementShape and both Chebyshev formulations into the public Stage1 surface",
  "record pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 with module Mathlib.Probability.Moments.Variance",
  "record theorem anchors ProbabilityTheory.meas_ge_le_evariance_div_sq and ProbabilityTheory.meas_ge_le_variance_div_sq",
  "merge theorem-tree packages M0992.P0 through M0992.P7 and leaf ids M0992-L001 through M0992-L010",
  "preserve unchecked status for public merge/status/clean-validation leaves until the integrator closes them",
  "rerun cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_272.lean after public synchronization",
  "confirm no completed state retains repo_local_integration_debt",
  "decide variant scope separately before adding broader Chebyshev variants"
]

/--
Current public status-gate verdict for the child execution pass: the repo-local
wrapper validates, but public completion remains blocked until serialized
public-surface synchronization and an integrator validation rerun.
-/
def publicStatusGateVerdict : String :=
  "Do not promote the public Stage1 checkbox for THM-M-0992 from this child pass alone; the local wrapper is checked, but public docs, todo, README/meta surfaces, variant scope, and a clean integrator validation rerun must be synchronized first."

#check publicStatusGateSurfaces
#check publicStatusGateRequirements
#check publicStatusGateVerdict

/-! ## Variant-scope metadata for Stage1 integration. -/

/--
Chebyshev variants covered by the checked `StatementShape`.  The current local
wrapper intentionally covers exactly the two mathlib-backed real-valued
deviation forms recorded here.
-/
def variantScopeCoveredForms : List String := [
  "extended-variance deviation bound: AEStronglyMeasurable X P, c : NNReal, c != 0, conclusion using ProbabilityTheory.evariance X P / c ^ 2",
  "real-variance deviation bound: finite measure, MemLp X 2 P, 0 < c, conclusion using ENNReal.ofReal (ProbabilityTheory.variance X P / c ^ 2)"
]

/--
Broader Chebyshev-style variants that are not silently included in this checked
wrapper.  Each item needs its own statement-normalization and proof-anchor task
before it can be claimed publicly.
-/
def variantScopeOutOfCurrentWrapper : List String := [
  "one-sided Chebyshev or Cantelli inequality",
  "two-sided bounds expressed with probability measures or normalized probability notation beyond the current measure statement",
  "covariance-matrix or vector-valued Chebyshev inequalities",
  "conditional-expectation or conditional-variance Chebyshev inequalities",
  "Banach-space or Hilbert-space norm variants",
  "process-indexed maximal inequalities such as Kolmogorov or Doob-style bounds",
  "finite-family union-bound corollaries or sample-mean specializations"
]

/--
Variant-scope verdict for `THM-M-0992.variant-scope`: do not broaden
`StatementShape` in place.  If any broader Chebyshev variant is desired, split it
into a separately named Stage1 child task with its own anchor and validation
gate.
-/
def variantScopeVerdict : String :=
  "The Stage1 wrapper scope is exactly the two checked real-valued mathlib Chebyshev formulations in StatementShape. Broader Chebyshev variants are not in scope for this wrapper; add separate child tasks before claiming them."

/-- Integration-ready public child tasks for optional broader Chebyshev variants. -/
def proposedVariantChildTasks : List String := [
  "THM-M-0992.variant-cantelli: decide and formalize a one-sided Cantelli/Chebyshev form only if a pinned Lean anchor or local proof plan is available",
  "THM-M-0992.variant-vector: decide and formalize covariance-matrix or vector-valued Chebyshev only as a separate theorem target",
  "THM-M-0992.variant-conditional: decide and formalize conditional-expectation or conditional-variance Chebyshev only as a separate theorem target",
  "THM-M-0992.variant-maximal: decide and formalize process-indexed maximal Chebyshev-style inequalities only as separate theorem targets"
]

#check variantScopeCoveredForms
#check variantScopeOutOfCurrentWrapper
#check variantScopeVerdict
#check proposedVariantChildTasks

end S1_M_272
end Stage1
end AwesomeTheorems
