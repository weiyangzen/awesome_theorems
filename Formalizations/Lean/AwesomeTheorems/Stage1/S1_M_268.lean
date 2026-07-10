import Mathlib.Probability.CentralLimitTheorem

/-!
# S1-M-268 / THM-M-0988: Lindeberg-Levy central limit theorem

This Stage1 artifact records a checked repo-local wrapper for the one-dimensional
Lindeberg-Levy central limit theorem available in the pinned mathlib snapshot.

The mathlib theorem
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` proves the iid
real-valued finite-second-moment CLT: centered sums, scaled by `sqrt n`, converge
in distribution to a Gaussian law with variance equal to the variance of the
reference random variable.  This is the standard Lindeberg-Levy central limit
theorem in Lean's `TendstoInDistribution` API.

This wrapper was audited against mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

No new kernel assumptions or placeholders are introduced here.  The terminal
proof body is upstream in pinned mathlib; this file supplies the repo-local
statement shape, small projection wrappers, and the checked local wrapper
theorem.

Boundary: this Stage1 artifact closes only the one-dimensional iid
Lindeberg-Levy CLT exposed by the pinned mathlib theorem.  It does not claim a
multivariate CLT, a triangular-array CLT, or the full Lindeberg-Feller CLT.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Filter Finset
open scoped Real Topology ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_268

universe u v

/--
Centered and `sqrt n`-normalized partial sum for a real-valued random sequence.

The definition intentionally matches the expression in mathlib's central limit
theorem.  The `n = 0` value is harmless for convergence along `atTop`.
-/
def centeredNormalizedSum
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω)
    (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  (√(n : ℝ))⁻¹ * (∑ k ∈ Finset.range n, X k ω - (n : ℝ) * ∫ x, X 0 x ∂P)

/--
Normalized data for the Lindeberg-Levy central limit theorem in the form
available in mathlib.

The target random variable `Y` lives on a second probability space and has law
`gaussianReal 0 (variance (X 0) P).toNNReal`.  The source variables are
independent, identically distributed, and the reference variable has finite
second moment.
-/
structure LindebergLevyData
    (Ω : Type u) [MeasurableSpace Ω]
    (Ω' : Type v) [MeasurableSpace Ω'] where
  P : Measure Ω
  P' : Measure Ω'
  X : ℕ → Ω → ℝ
  Y : Ω' → ℝ
  sourceProbability : IsProbabilityMeasure P
  targetProbability : IsProbabilityMeasure P'
  limitHasLaw : HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P'
  squareIntegrable : MemLp (X 0) 2 P
  independent : iIndepFun X P
  identDistrib : ∀ i : ℕ, IdentDistrib (X i) (X 0) P P

/-- Distributional convergence conclusion of the Lindeberg-Levy CLT. -/
def LindebergLevyConclusion
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') : Prop :=
  letI : IsProbabilityMeasure D.P := D.sourceProbability
  letI : IsProbabilityMeasure D.P' := D.targetProbability
  TendstoInDistribution
    (fun (n : ℕ) (ω : Ω) => centeredNormalizedSum D.P D.X n ω)
    atTop D.Y (fun _ : ℕ => D.P) D.P'

/--
Stage1 normalized statement shape for the iid central limit theorem.

This is closed locally by `lindebergLevy_clt_mathlib_wrapper`, whose proof body
calls the pinned mathlib theorem.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ (Ω' : Type v) [MeasurableSpace Ω'],
      ∀ D : LindebergLevyData Ω Ω',
        LindebergLevyConclusion D

/-- The statement-shape definition unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ (Ω' : Type v) [MeasurableSpace Ω'],
          ∀ D : LindebergLevyData Ω Ω',
            LindebergLevyConclusion D :=
  Iff.rfl

/-- Project the finite-second-moment hypothesis from the normalized data package. -/
theorem squareIntegrable_reference
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') :
    MemLp (D.X 0) 2 D.P :=
  D.squareIntegrable

/-- Project independence of the input sequence from the normalized data package. -/
theorem independent_sequence
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') :
    iIndepFun D.X D.P :=
  D.independent

/-- Project identical distribution of every coordinate with the reference variable. -/
theorem identDistrib_coordinate
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') (i : ℕ) :
    IdentDistrib (D.X i) (D.X 0) D.P D.P :=
  D.identDistrib i

/-- Project the Gaussian limit-law hypothesis from the normalized data package. -/
theorem limit_hasLaw
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') :
    HasLaw D.Y (gaussianReal 0 (variance (D.X 0) D.P).toNNReal) D.P' :=
  D.limitHasLaw

/-- The normalized partial-sum notation unfolds to the mathlib CLT expression. -/
theorem centeredNormalizedSum_apply
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω)
    (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) :
    centeredNormalizedSum P X n ω =
      (√(n : ℝ))⁻¹ * (∑ k ∈ Finset.range n, X k ω - (n : ℝ) * ∫ x, X 0 x ∂P) :=
  rfl

/--
Checked repo-local wrapper around mathlib's Lindeberg-Levy central limit
theorem.
-/
theorem lindebergLevy_clt_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') :
    LindebergLevyConclusion D := by
  letI : IsProbabilityMeasure D.P := D.sourceProbability
  letI : IsProbabilityMeasure D.P' := D.targetProbability
  exact tendstoInDistribution_inv_sqrt_mul_sum_sub
    D.limitHasLaw D.squareIntegrable D.independent D.identDistrib

/-- The normalized Stage1 statement is closed by the pinned mathlib theorem. -/
theorem statementShape_mathlib_wrapper :
    StatementShape.{u, v} := by
  intro Ω _mΩ Ω' _mΩ' D
  exact lindebergLevy_clt_mathlib_wrapper D

/-- mathlib's characteristic-function factorization for normalized iid sums. -/
theorem charFun_inv_sqrt_mul_sum_anchor
    {Ω : Type u} [MeasurableSpace Ω]
    {Ω' : Type v} [MeasurableSpace Ω']
    (D : LindebergLevyData Ω Ω') {n : ℕ} {t : ℝ} :
    charFun (D.P.map (fun ω => (√(n : ℝ))⁻¹ * ∑ k ∈ Finset.range n, D.X k ω)) t =
      (charFun (D.P.map (D.X 0)) ((√(n : ℝ))⁻¹ * t)) ^ n :=
  charFun_inv_sqrt_mul_sum D.independent D.identDistrib

/-- mathlib modules checked while locating repo-local central-limit anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.CentralLimitTheorem",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.Probability.Independence.CharacteristicFunction",
  "Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic",
  "Mathlib.MeasureTheory.Measure.CharacteristicFunction.TaylorExpansion",
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Moments.Variance"
]

/-- Checked declaration names used or audited as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum",
  "ProbabilityTheory.charFun_inv_sqrt_mul_sum",
  "ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow",
  "MeasureTheory.TendstoInDistribution",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.gaussianReal",
  "ProbabilityTheory.variance",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IdentDistrib",
  "MeasureTheory.MemLp",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun"
]

/--
Search terms checked for alternative or absent central-limit anchors.  The
pinned mathlib theorem already closes this Stage1 Lean target.
-/
def auditSearchTerms : List String := [
  "CentralLimitTheorem",
  "central limit theorem",
  "Lindeberg",
  "Lévy",
  "Levy",
  "tendstoInDistribution_inv_sqrt_mul_sum_sub",
  "TendstoInDistribution",
  "charFun_inv_sqrt_mul_sum",
  "gaussianReal",
  "iIndepFun",
  "IdentDistrib"
]

/-- Boundary text for public backfill surfaces. -/
def publicBoundarySummary : String :=
  "One-dimensional iid Lindeberg-Levy CLT is closed via pinned mathlib; " ++
  "no multivariate, triangular-array, or full Lindeberg-Feller CLT extension is claimed."

/--
Public merge-back theorem-tree leaves that must remain distinguishable.

The checked wrapper is closed locally, the upstream proof-package anchors identify
where mathlib carries the proof body, and public consistency remains a serial
documentation merge task.
-/
def publicMergeBackTreeSplit : List String := [
  "M0988.machine-wrapper: local Stage1 wrapper theorem " ++
    "AwesomeTheorems.Stage1.S1_M_268.lindebergLevy_clt_mathlib_wrapper",
  "M0988.upstream-proof-package-anchors: pinned mathlib theorem " ++
    "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub " ++
    "and characteristic-function CLT anchors",
  "M0988.public-consistency-leaf: serial public backfill keeps machine wrapper, " ++
    "upstream anchors, validation command, import-surface policy, and scope " ++
    "boundary synchronized without broadening the theorem claim"
]

/-- Pinned mathlib revision used for the Stage1 wrapper audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check statementShape_mathlib_wrapper
#check lindebergLevy_clt_mathlib_wrapper
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.charFun_inv_sqrt_mul_sum
#check ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow
#check MeasureTheory.TendstoInDistribution
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.variance
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.IdentDistrib
#check publicMergeBackTreeSplit

end S1_M_268
end Stage1
end AwesomeTheorems
