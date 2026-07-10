import Mathlib.Probability.Moments.SubGaussian

/-!
# S1-M-274 / THM-M-0994: Hoeffding inequality, Stage1 wrapper

This file records a conservative Lean 4 normalization of Hoeffding's inequality
for sums of independent bounded real random variables.

The pinned mathlib snapshot already contains the sub-Gaussian infrastructure,
Hoeffding's lemma for bounded variables, and the finite-sum Hoeffding bound for
independent sub-Gaussian random variables.  The declarations below wrap those
facts into the Stage1 theorem shape for centered finite sums.  They do not
update public blueprint/checklist status.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_274

universe u

/-- Centered finite sum of the first `n` random variables. -/
def centeredRangeSum {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  ∑ i ∈ Finset.range n, (X i ω - μ[X i])

/--
Rewrite the internal centered-sum normal form into the displayed finite-sum
expression `sum X_i - sum E[X_i]`.
-/
theorem centeredRangeSum_eq_sum_sub_sum_integral {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) :
    centeredRangeSum μ X n ω =
      (∑ i ∈ Finset.range n, X i ω) - ∑ i ∈ Finset.range n, μ[X i] := by
  simp [centeredRangeSum, Finset.sum_sub_distrib]

/--
The variance proxy in mathlib's sub-Gaussian Hoeffding bound.

For each variable bounded in `[a i, b i]`, Hoeffding's lemma gives
sub-Gaussian parameter `((‖b i - a i‖₊) / 2)^2`.
-/
def hoeffdingVarianceProxy (a b : ℕ → ℝ) (n : ℕ) : ℝ≥0 :=
  ∑ i ∈ Finset.range n, ((‖b i - a i‖₊ / 2) ^ 2)

/--
Input package for the bounded independent real-valued random variables used in
the normalized Stage1 Hoeffding statement.
-/
structure BoundedIndependentData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  X : ℕ → Ω → ℝ
  a : ℕ → ℝ
  b : ℕ → ℝ
  isProbability : IsProbabilityMeasure μ
  measurable : ∀ n : ℕ, Measurable (X n)
  independent : ProbabilityTheory.iIndepFun X μ
  boundedAE : ∀ n : ℕ, ∀ᵐ ω ∂μ, X n ω ∈ Set.Icc (a n) (b n)

/--
One-sided centered Hoeffding upper-tail conclusion for all finite initial
segments.  This is the mathlib-backed statement normalized in this file.
-/
def HoeffdingConclusion {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) : Prop :=
  ∀ (n : ℕ) {ε : ℝ}, 0 ≤ ε →
    D.μ.real {ω | ε ≤ centeredRangeSum D.μ D.X n ω} ≤
      exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n))

/--
Stage1 theorem shape for Hoeffding's inequality in the centered finite-sum
form.  The proof is provided by `statementShape_from_mathlib`.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : BoundedIndependentData Ω,
      HoeffdingConclusion D

/--
Statement-normalization note for the public Stage1 backfill.

`AwesomeTheorems.Stage1.S1_M_274.StatementShape` is the checked repo-local
Lean statement for the one-sided centered finite-sum Hoeffding inequality for
independent bounded real random variables.  It is not a two-sided
absolute-value wrapper, an uncentered displayed-sum wrapper, or an
Azuma/McDiarmid bounded-difference process theorem.
-/
def statementNormalizationNote : String :=
  "AwesomeTheorems.Stage1.S1_M_274.StatementShape is the checked repo-local " ++
    "Lean statement for the one-sided centered finite-sum Hoeffding inequality " ++
    "for independent bounded real random variables."

/-- The normalized statement unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : BoundedIndependentData Ω,
          HoeffdingConclusion D :=
  Iff.rfl

/-- Project the independent-family hypothesis from the normalized data. -/
theorem independent_from_data {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) :
    ProbabilityTheory.iIndepFun D.X D.μ :=
  D.independent

/-- Project measurability of each random variable from the normalized data. -/
theorem measurable_X {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (n : ℕ) :
    Measurable (D.X n) :=
  D.measurable n

/-- Project the almost-sure boundedness interval for each random variable. -/
theorem boundedAE_X {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (n : ℕ) :
    ∀ᵐ ω ∂D.μ, D.X n ω ∈ Set.Icc (D.a n) (D.b n) :=
  D.boundedAE n

/-- Centering each coordinate preserves independence by measurable composition. -/
theorem centered_iIndepFun {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) :
    ProbabilityTheory.iIndepFun (fun i ω => D.X i ω - D.μ[D.X i]) D.μ := by
  simpa [Function.comp_def] using
    D.independent.comp
      (fun i x => x - D.μ[D.X i])
      (fun _ => by fun_prop)

/--
Hoeffding's lemma from mathlib turns a bounded random variable into a centered
sub-Gaussian random variable.
-/
theorem centered_hasSubgaussianMGF {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (i : ℕ) :
    ProbabilityTheory.HasSubgaussianMGF
      (fun ω => D.X i ω - D.μ[D.X i])
      ((‖D.b i - D.a i‖₊ / 2) ^ 2) D.μ := by
  haveI : IsProbabilityMeasure D.μ := D.isProbability
  exact ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
    (D.measurable i).aemeasurable (D.boundedAE i)

/--
mathlib-backed Hoeffding inequality for centered finite sums of bounded
independent random variables.
-/
theorem hoeffding_upper_tail {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (n : ℕ) {ε : ℝ} (hε : 0 ≤ ε) :
    D.μ.real {ω | ε ≤ centeredRangeSum D.μ D.X n ω} ≤
      exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
  simpa [centeredRangeSum, hoeffdingVarianceProxy] using
    ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
      (X := fun i ω => D.X i ω - D.μ[D.X i])
      (c := fun i => ((‖D.b i - D.a i‖₊ / 2) ^ 2))
      (s := Finset.range n)
      (centered_iIndepFun D)
      (fun i _hi => centered_hasSubgaussianMGF D i)
      hε

/--
Uncentered displayed finite-sum wrapper for the same one-sided upper tail.

This is only a rewrite of `hoeffding_upper_tail`; the probability event is
displayed as `sum X_i - sum E[X_i]`.
-/
theorem hoeffding_upper_tail_uncentered_sum {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (n : ℕ) {ε : ℝ} (hε : 0 ≤ ε) :
    D.μ.real
        {ω |
          ε ≤ (∑ i ∈ Finset.range n, D.X i ω) -
            ∑ i ∈ Finset.range n, D.μ[D.X i]} ≤
      exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
  simpa [centeredRangeSum_eq_sum_sub_sum_integral] using
    hoeffding_upper_tail D n hε

/--
The matching lower-tail bound, written as an upper tail for the negated
centered finite sum.
-/
theorem hoeffding_negative_tail {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (n : ℕ) {ε : ℝ} (hε : 0 ≤ ε) :
    D.μ.real {ω | ε ≤ -centeredRangeSum D.μ D.X n ω} ≤
      exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
  simpa [centeredRangeSum, hoeffdingVarianceProxy] using
    ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
      (X := fun i ω => -(D.X i ω - D.μ[D.X i]))
      (c := fun i => ((‖D.b i - D.a i‖₊ / 2) ^ 2))
      (s := Finset.range n)
      ((centered_iIndepFun D).comp
        (fun _ x => -x)
        (fun _ => by fun_prop))
      (fun i _hi => (centered_hasSubgaussianMGF D i).neg)
      hε

/--
Two-sided absolute-tail Hoeffding wrapper obtained by the union bound from the
positive and negative centered tails.
-/
theorem hoeffding_two_sided_abs_tail {Ω : Type u} [MeasurableSpace Ω]
    (D : BoundedIndependentData Ω) (n : ℕ) {ε : ℝ} (hε : 0 ≤ ε) :
    D.μ.real {ω | ε ≤ |centeredRangeSum D.μ D.X n ω|} ≤
      2 * exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
  haveI : IsProbabilityMeasure D.μ := D.isProbability
  let Epos : Set Ω := {ω | ε ≤ centeredRangeSum D.μ D.X n ω}
  let Eneg : Set Ω := {ω | ε ≤ -centeredRangeSum D.μ D.X n ω}
  have hsubset :
      {ω | ε ≤ |centeredRangeSum D.μ D.X n ω|} ⊆ Epos ∪ Eneg := by
    intro ω hω
    have hω' : ε ≤ |centeredRangeSum D.μ D.X n ω| := hω
    exact (le_abs.mp hω')
  have hpos :
      D.μ.real Epos ≤
        exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
    simpa [Epos] using hoeffding_upper_tail D n hε
  have hneg :
      D.μ.real Eneg ≤
        exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
    simpa [Eneg] using hoeffding_negative_tail D n hε
  calc
    D.μ.real {ω | ε ≤ |centeredRangeSum D.μ D.X n ω|}
        ≤ D.μ.real (Epos ∪ Eneg) := measureReal_mono hsubset
    _ ≤ D.μ.real Epos + D.μ.real Eneg := measureReal_union_le Epos Eneg
    _ ≤ exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) +
          exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) :=
        add_le_add hpos hneg
    _ = 2 * exp (-ε ^ 2 / (2 * hoeffdingVarianceProxy D.a D.b n)) := by
        ring

/--
The Stage1 normalized Hoeffding statement is closed by pinned mathlib's
sub-Gaussian Hoeffding package.
-/
theorem statementShape_from_mathlib : StatementShape.{u} := by
  intro Ω _ D n ε hε
  exact hoeffding_upper_tail D n hε

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Moments.SubGaussian",
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.Probability.Moments.MGFAnalytic",
  "Mathlib.Probability.Moments.Tilted",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Kernel.Condexp",
  "Mathlib.Probability.Process.Filtration"
]

/-- Pinned mathlib commit used for the public Stage1 anchor row. -/
def mathlibPinnedCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Integration-ready public anchor row for the serial blueprint/todo backfill.

Parallel child workers must not edit shared public docs directly; this checked
constant records the exact mathlib commit, module, and declarations for the
later public merge.
-/
def publicMathlibAnchorRow : String :=
  "| `S1-M-274.mathlib-anchor` | mathlib " ++ mathlibPinnedCommit ++
    " | `Mathlib.Probability.Moments.SubGaussian` | " ++
    "`ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun`; " ++
    "`ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc` | " ++
    "`local_wrapper_upstream_mathlib`; repo-local wrapper validated by " ++
    "`cd Formalizations/Lean && lake env lean " ++
    "AwesomeTheorems/Stage1/S1_M_274.lean` |"

/-- Validation command recorded by the parent Stage1 worker on 2026-04-30. -/
def wrapperValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_274.lean"

/-- Historical parent-worker validation result for the checked Stage1 wrapper. -/
def wrapperValidationRecord20260430 : String :=
  wrapperValidationCommand ++ " passed on 2026-04-30 with exit code 0."

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.HasSubgaussianMGF",
  "ProbabilityTheory.HasSubgaussianMGF.measure_ge_le",
  "ProbabilityTheory.HasSubgaussianMGF.sum_of_iIndepFun",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun",
  "ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero",
  "ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc",
  "ProbabilityTheory.HasCondSubgaussianMGF",
  "ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF",
  "ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.comp"
]

/--
Search terms that did not locate a separately named terminal theorem called
`Hoeffding` outside the sub-Gaussian module in the pinned local mathlib snapshot.
-/
def absentSeparateTerminalSearchTerms : List String := [
  "Hoeffding outside Mathlib.Probability.Moments.SubGaussian",
  "McDiarmid",
  "bounded difference concentration",
  "two-sided Hoeffding theorem name"
]

/--
Decision for the public Stage1 target boundary.

The public item can be counted at the checked repo-local target only when the
public statement is explicitly normalized to the one-sided centered finite-sum
form `StatementShape`.  Two-sided absolute-tail and uncentered displayed-sum
wrappers are useful follow-up variants, but they are not prerequisites for the
normalized one-sided target.  They remain prerequisites for any broader public
claim that those variants have also been completed.
-/
def targetDecisionForPublicBackfill : String :=
  "Count the Stage1 target at the one-sided centered finite-sum form proved by " ++
    "AwesomeTheorems.Stage1.S1_M_274.StatementShape only after the public " ++
    "surface explicitly says that this is the normalized target.  Do not " ++
    "claim two-sided absolute-tail or uncentered displayed-sum Hoeffding " ++
    "variants until separate wrappers are added and validated."

/--
Integration-ready public text for the target-decision leaf.  This remains in
the checked Lean artifact so a serial integrator can copy the exact boundary
without treating a private child ledger as the public completion surface.
-/
def publicTargetDecisionText : String :=
  "`S1-M-274.target-decision`: count the repo-local machine closure at " ++
    "`AwesomeTheorems.Stage1.S1_M_274.StatementShape`, the one-sided centered " ++
    "finite-sum Hoeffding inequality for independent bounded real random " ++
    "variables, provided the public statement-normalization note states that " ++
    "boundary explicitly.  A two-sided absolute-tail wrapper and an uncentered " ++
    "displayed-sum wrapper are not blockers for this normalized target, but " ++
    "they must stay open as separate leaves before any public text claims " ++
    "those stronger/common variants."

/--
Integration-ready public text for the optional two-sided absolute-tail leaf.
The checked theorem is separate from `StatementShape`, so public completion
still depends on serial blueprint/todo/README synchronization.
-/
def publicTwoSidedAbsTailText : String :=
  "`S1-M-274.two-sided`: if the public target requires the common absolute " ++
    "tail form, use checked theorem " ++
    "`AwesomeTheorems.Stage1.S1_M_274.hoeffding_two_sided_abs_tail`, which " ++
    "derives `P(|centeredRangeSum| >= epsilon) <= 2 * exp " ++
    "(-epsilon^2 / (2 * hoeffdingVarianceProxy))` from the positive-tail " ++
    "wrapper `hoeffding_upper_tail`, the negative-tail wrapper " ++
    "`hoeffding_negative_tail`, and `MeasureTheory.measureReal_union_le`.  " ++
    "The local leaf budget is <=100 proof steps and the wrapper is " ++
    "repo-local closed after `cd Formalizations/Lean && lake env lean " ++
    "AwesomeTheorems/Stage1/S1_M_274.lean` passes."

/--
Integration-ready public text for the optional uncentered displayed-sum leaf.
The checked theorem is a definitional finite-sum rewrite of the centered
upper-tail wrapper.
-/
def publicUncenteredDisplayedSumText : String :=
  "`S1-M-274.uncentered`: if the public target requires the displayed " ++
    "one-sided form `P(sum X_i - sum E[X_i] >= epsilon)`, use checked " ++
    "theorem `AwesomeTheorems.Stage1.S1_M_274." ++
    "hoeffding_upper_tail_uncentered_sum`.  The bridge lemma " ++
    "`AwesomeTheorems.Stage1.S1_M_274." ++
    "centeredRangeSum_eq_sum_sub_sum_integral` rewrites " ++
    "`centeredRangeSum mu X n omega` to " ++
    "`(sum i in Finset.range n, X i omega) - " ++
    "sum i in Finset.range n, mu[X i]`, and the wrapper then applies " ++
    "`hoeffding_upper_tail` with the same variance proxy.  The local leaf " ++
    "budget is <=100 proof steps and the wrapper is repo-local closed after " ++
    "`cd Formalizations/Lean && lake env lean " ++
    "AwesomeTheorems/Stage1/S1_M_274.lean` passes."

/--
Integration-gate text for the serial public-doc merge.

The checked wrapper has no remaining `repo_local_integration_debt`, but this
private Lean artifact is not the public completion surface.  The public Stage1
checkbox must remain open until the blueprint, todo, and README surfaces are
updated together by a serial integrator.
-/
def publicIntegrationGateText : String :=
  "`S1-M-274.integration-gate`: keep the public Stage1 checkbox open until " ++
    "`Docs/Stage1_Blueprint.md`, `Docs/todos_20260430.md`, and `README.md` " ++
    "are synchronized with the checked repo-local wrapper.  The normalized " ++
    "one-sided centered target has machine status `local_wrapper_upstream_" ++
    "mathlib` after `cd Formalizations/Lean && lake env lean " ++
    "AwesomeTheorems/Stage1/S1_M_274.lean` passes, so no completed-state " ++
    "`repo_local_integration_debt` remains for that target.  Do not mark " ++
    "broader two-sided, uncentered, or martingale/process variants complete " ++
    "unless their checked wrappers and public status rows are merged too."

/-! ## Audit probes retained in the checked file. -/

#check ProbabilityTheory.HasSubgaussianMGF
#check ProbabilityTheory.HasSubgaussianMGF.measure_ge_le
#check ProbabilityTheory.HasSubgaussianMGF.sum_of_iIndepFun
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
#check ProbabilityTheory.HasCondSubgaussianMGF
#check ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF
#check ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.comp
#check centeredRangeSum_eq_sum_sub_sum_integral
#check hoeffding_upper_tail_uncentered_sum

end S1_M_274
end Stage1
end AwesomeTheorems
