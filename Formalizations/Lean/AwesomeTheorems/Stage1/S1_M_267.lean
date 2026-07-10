import Mathlib.Probability.CentralLimitTheorem

/-!
# S1-M-267 / THM-M-0987: Central limit theorem

This Stage1 artifact records a repo-local Lean 4 wrapper for the one-dimensional
i.i.d. central limit theorem already present in the pinned mathlib snapshot.

The imported mathlib theorem is
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`: for independent,
identically distributed real random variables with finite second moment, the
centered sums scaled by `1 / sqrt n` converge in distribution to a Gaussian
law with variance `Var[X 0; P]`.

This file does not claim multivariate, triangular-array, martingale, or
Lindeberg-Feller versions of the central limit theorem.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Real Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_267

universe uΩ uΩ'

/--
Data package for the pinned mathlib one-dimensional i.i.d. central limit
theorem.

The target random variable `Y` is allowed to live on a separate probability
space.  Its law is required to be `gaussianReal 0 Var[X 0; P].toNNReal`, matching
the terminal mathlib theorem.
-/
structure CentralLimitTheoremData
    (Ω : Type uΩ) (Ω' : Type uΩ') [MeasurableSpace Ω] [MeasurableSpace Ω'] :
    Type (max uΩ uΩ') where
  P : Measure Ω
  P' : Measure Ω'
  isProbabilityP : IsProbabilityMeasure P
  isProbabilityP' : IsProbabilityMeasure P'
  X : ℕ → Ω → ℝ
  Y : Ω' → ℝ
  gaussianLimitLaw : HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P'
  squareIntegrable : MemLp (X 0) 2 P
  independent : iIndepFun X P
  identDistrib : ∀ i : ℕ, IdentDistrib (X i) (X 0) P P

/--
The centered, `sqrt n`-scaled sum appearing in mathlib's one-dimensional CLT.
-/
def centeredNormalizedSum
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') : ℕ → Ω → ℝ :=
  fun n ω => (√(n : ℝ))⁻¹ * (∑ k ∈ Finset.range n, D.X k ω - (n : ℝ) * D.P[D.X 0])

/--
Conclusion package: convergence in distribution of centered normalized sums to
the supplied Gaussian-limit random variable.
-/
def CentralLimitTheoremConclusion
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') : Prop := by
  letI : IsProbabilityMeasure D.P := D.isProbabilityP
  letI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  exact TendstoInDistribution (centeredNormalizedSum D) atTop D.Y (fun _ : ℕ => D.P) D.P'

/--
Stage1 normalized statement shape for THM-M-0987.

This is the exact one-dimensional i.i.d. CLT shape currently provided by pinned
mathlib, expressed through `CentralLimitTheoremData`.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) (Ω' : Type uΩ') [MeasurableSpace Ω] [MeasurableSpace Ω'],
    ∀ D : CentralLimitTheoremData Ω Ω',
      CentralLimitTheoremConclusion D

/-- The normalized statement unfolds to the data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{uΩ, uΩ'} ↔
      ∀ (Ω : Type uΩ) (Ω' : Type uΩ') [MeasurableSpace Ω] [MeasurableSpace Ω'],
        ∀ D : CentralLimitTheoremData Ω Ω',
          CentralLimitTheoremConclusion D :=
  Iff.rfl

/--
Repo-local wrapper around mathlib's terminal one-dimensional i.i.d. CLT theorem.
-/
theorem centralLimitTheorem_mathlib_wrapper
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') :
    CentralLimitTheoremConclusion D := by
  haveI : IsProbabilityMeasure D.P := D.isProbabilityP
  haveI : IsProbabilityMeasure D.P' := D.isProbabilityP'
  simpa [CentralLimitTheoremConclusion, centeredNormalizedSum] using
    ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
      (P := D.P) (P' := D.P') (X := D.X) (Y := D.Y)
      D.gaussianLimitLaw D.squareIntegrable D.independent D.identDistrib

/--
The local statement shape is closed by the pinned mathlib theorem.
-/
theorem statementShape_mathlib :
    StatementShape.{uΩ, uΩ'} :=
  fun _ _ _ _ D => centralLimitTheorem_mathlib_wrapper D

/-- Projection wrapper: the data package exposes the ambient probability measure. -/
theorem source_isProbability
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') :
    IsProbabilityMeasure D.P :=
  D.isProbabilityP

/-- Projection wrapper: the data package exposes finite second moment. -/
theorem coordinate_zero_memLp_two
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') :
    MemLp (D.X 0) 2 D.P :=
  D.squareIntegrable

/-- Projection wrapper: the data package exposes independence. -/
theorem sequence_iIndepFun
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') :
    iIndepFun D.X D.P :=
  D.independent

/-- Projection wrapper: each coordinate has the same distribution as `X 0`. -/
theorem coordinate_identDistrib_zero
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') (i : ℕ) :
    IdentDistrib (D.X i) (D.X 0) D.P D.P :=
  D.identDistrib i

/-- Projection wrapper: the limiting random variable has the Gaussian law used by mathlib. -/
theorem limit_hasGaussianLaw
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') :
    HasLaw D.Y (gaussianReal 0 (variance (D.X 0) D.P).toNNReal) D.P' :=
  D.gaussianLimitLaw

/-- The normalized sum unfolds to the finite-sum expression used by mathlib. -/
theorem centeredNormalizedSum_apply
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    (D : CentralLimitTheoremData Ω Ω') (n : ℕ) (ω : Ω) :
    centeredNormalizedSum D n ω =
      (√(n : ℝ))⁻¹ * (∑ k ∈ Finset.range n, D.X k ω - (n : ℝ) * D.P[D.X 0]) :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.CentralLimitTheorem",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.MeasureTheory.Measure.CharacteristicFunction.TaylorExpansion",
  "Mathlib.Probability.Independence.CharacteristicFunction"
]

/--
Theorem-tree note for the checked branch.

The repo-local wrapper closes the one-dimensional i.i.d. real-valued CLT by
calling `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`.  In
pinned mathlib, that terminal theorem reduces to the centered variance-one CLT,
whose proof uses characteristic functions of independent finite sums, the
second-order Taylor expansion of a characteristic function at zero, Levy
convergence from pointwise characteristic-function convergence to convergence in
distribution, and the Gaussian characteristic function.
-/
def checkedBranchTheoremTreeNote : String :=
  "checked iid real-valued CLT branch closes through characteristic functions, " ++
  "Taylor expansion at zero, Levy convergence, and the Gaussian characteristic function, " ++
  "all inside pinned mathlib"

/-- Pinned mathlib proof-route nodes supporting `checkedBranchTheoremTreeNote`. -/
def checkedBranchTheoremTreeNodes : List String := [
  "ProbabilityTheory.charFun_inv_sqrt_mul_sum",
  "ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow",
  "MeasureTheory.taylor_charFun_two",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
  "ProbabilityTheory.charFun_gaussianReal",
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum",
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub"
]

/-- Pinned mathlib revision providing the terminal CLT proof body for this wrapper. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Terminal mathlib module for the one-dimensional i.i.d. CLT anchor. -/
def terminalMathlibAnchorModule : String :=
  "Mathlib.Probability.CentralLimitTheorem"

/-- Terminal mathlib theorem used by `centralLimitTheorem_mathlib_wrapper`. -/
def terminalMathlibAnchorName : String :=
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub"

/-- Repo-local closure classification for the checked one-dimensional i.i.d. CLT branch. -/
def repoLocalClosureStatus : String :=
  "local_wrapper_upstream_mathlib"

/-- Public validation command requested for the Stage1 backfill entry. -/
def publicValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_267.lean"

/-- Historical public validation result recorded by the parent Stage1 worker. -/
def publicValidationHistoricalResult : String :=
  "passed on 2026-04-30"

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum",
  "ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow",
  "ProbabilityTheory.charFun_inv_sqrt_mul_sum",
  "ProbabilityTheory.charFun_gaussianReal",
  "MeasureTheory.taylor_charFun_two",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
  "MeasureTheory.TendstoInDistribution",
  "ProbabilityTheory.gaussianReal",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IdentDistrib",
  "MeasureTheory.MemLp",
  "ProbabilityTheory.variance"
]

/--
Search terms that should remain outside the completed claim of this local
wrapper unless separate mathlib or external Lean anchors are integrated.
-/
def excludedGeneralizationSearchTerms : List String := [
  "multivariate central limit theorem",
  "Lindeberg",
  "Feller",
  "triangular array",
  "martingale central limit theorem",
  "Berry-Esseen",
  "functional central limit theorem",
  "Donsker"
]

/--
One checked row from the broader-variant primary-source audit.

The Boolean fields are deliberately conservative: support APIs or adjacent
source files do not count as terminal proof completion for a broader CLT
variant.
-/
structure BroaderVariantAuditRow where
  source : String
  searchTerms : List String
  pinnedRevisionOrAccess : String
  outcome : String
  terminalProofLocated : Bool
  integrationTargetForCompletion : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/--
Audit result for the pinned mathlib dependency closure.

The checked dependency exposes the one-dimensional i.i.d. CLT theorem wrapped
above and adjacent finite-dimensional characteristic-function/Levy convergence
APIs.  It does not expose a terminal multivariate, Lindeberg-Feller triangular
array, martingale, Donsker/functional, or Berry-Esseen CLT theorem for this
Stage1 slot.
-/
def mathlibBroaderVariantAudit : BroaderVariantAuditRow where
  source := "leanprover-community/mathlib4 local Lake dependency"
  searchTerms := excludedGeneralizationSearchTerms
  pinnedRevisionOrAccess := pinnedMathlibRevision
  outcome :=
    "terminal iid real-valued CLT found; requested broader CLT variants not found as terminal mathlib theorems"
  terminalProofLocated := false
  integrationTargetForCompletion := false
  completedStateRepoLocalIntegrationDebt := false

/--
Audit result for the adjacent external Lean 4 CLT source already identified by
neighboring Stage1 workers.

The repository is not completion evidence here: the audited revision contains
unclosed proof placeholders in the CLT theorem path and does not target the
requested broader CLT families.
-/
def adjacentExternalCLTAudit : BroaderVariantAuditRow where
  source := "https://github.com/uw-math-ai/central_limit_theorem"
  searchTerms := excludedGeneralizationSearchTerms
  pinnedRevisionOrAccess := "0ed57e943d642eaa95fe547780024b9e3a0dfbdf"
  outcome :=
    "adjacent iid CLT source; contains unclosed proof placeholders and no terminal broader-variant CLT declaration"
  terminalProofLocated := false
  integrationTargetForCompletion := false
  completedStateRepoLocalIntegrationDebt := false

/-- Checked audit rows retained for public backfill of the broader-variant search child. -/
def broaderVariantAuditRows : List BroaderVariantAuditRow := [
  mathlibBroaderVariantAudit,
  adjacentExternalCLTAudit
]

/-- No broader-variant terminal proof was located by the retained audit rows. -/
theorem broaderVariantAuditRows_no_terminal_proof :
    broaderVariantAuditRows.map (fun row => row.terminalProofLocated) = [false, false] :=
  rfl

/-- The retained audit rows do not leave completed repo-local integration debt. -/
theorem broaderVariantAuditRows_no_completed_integration_debt :
    broaderVariantAuditRows.map (fun row => row.completedStateRepoLocalIntegrationDebt) =
      [false, false] :=
  rfl

/-- Integration blocker for the broader CLT family after the C006 audit. -/
def broaderVariantIntegrationBlocker : String :=
  "No terminal Lean 4 proof for the requested broader CLT variants is present " ++
  "in the repo-local dependency closure; the adjacent external CLT source is " ++
  "not a completion target because its audited theorem path contains unclosed proof placeholders. " ++
  "Separate multivariate, Lindeberg-Feller, martingale, functional/Donsker, " ++
  "and Berry-Esseen children remain open formalization-debt targets."

/--
Scope decision for the public `THM-M-0987` wording.

The public wording "central limit theorem" / "normal convergence of sums of
independent random variables" is broader than this checked iid real-valued
wrapper.  This file therefore records the completed iid branch only.
-/
def publicStatementScopeDecision : String :=
  "broader_clt_family_not_exact_iid_real_valued"

/-- Completed branch retained under the broader public CLT family. -/
def completedScopedBranch : String :=
  "one_dimensional_iid_real_valued_finite_second_moment_clt"

/-- Broader CLT branches that require separate open children before public completion. -/
def requiredBroaderVariantChildren : List String := [
  "multivariate_clt",
  "lindeberg_feller_triangular_array_clt",
  "martingale_clt",
  "functional_clt_donsker"
]

/--
Public status boundary for child `S1-M-267-C007`.

README, blueprint, and todo summaries may record the checked scoped branch as
`local_wrapper_upstream_mathlib`, but must not collapse the broader "central
limit theorem" family into this one-dimensional iid wrapper.
-/
def publicNoOverstatementPolicy : String :=
  "Public status may mark only the one-dimensional iid real-valued finite-second-moment CLT " ++
  "as locally checked through the pinned mathlib wrapper; multivariate, Lindeberg-Feller, " ++
  "martingale, functional/Donsker, and Berry-Esseen CLT variants remain separate open work."

/-- Public documents that need serial integrator backfill for the scoped CLT status. -/
def publicBackfillTargets : List String := [
  "README.md",
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md"
]

/-! ## Audit probes retained in the checked file. -/

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow
#check ProbabilityTheory.charFun_inv_sqrt_mul_sum
#check ProbabilityTheory.charFun_gaussianReal
#check MeasureTheory.TendstoInDistribution
#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.IdentDistrib
#check MeasureTheory.MemLp
#check ProbabilityTheory.variance
#check broaderVariantAuditRows_no_terminal_proof
#check broaderVariantAuditRows_no_completed_integration_debt
#check publicNoOverstatementPolicy
#check publicBackfillTargets

end S1_M_267
end Stage1
end AwesomeTheorems
