import Mathlib.MeasureTheory.Function.ConvergenceInDistribution

/-!
# S1-M-293 / THM-M-1014: Continuous mapping theorem

This Stage1 artifact records the probability-measure form of the continuous
mapping theorem: weak convergence of probability measures is preserved by
push-forward along a continuous map.

The pinned mathlib snapshot already contains this theorem for
`ProbabilityMeasure`, using the weak-convergence topology encoded by
convergence of bounded continuous test-function integrals.  The local theorem
below is therefore a thin checked wrapper around the mathlib anchor, plus a
normalized statement shape for the Stage1 slot.  The random-variable form is
not a separate primitive topology: mathlib's `TendstoInDistribution` packages
convergence of the laws, namely push-forwards `(μ n).map (X n)` and `μ'.map Z`,
as convergence in the same `ProbabilityMeasure` weak topology.
-/

noncomputable section

open MeasureTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_293

universe u v w

/--
Predicate form of the continuous mapping theorem for probability measures.

If `νs` converges weakly to `ν` on `Ω`, then the push-forward probability
measures under any continuous `f : Ω → Ω'` converge weakly to the push-forward
of `ν`.
-/
def ContinuousMappingTheorem
    (Ω : Type u) (Ω' : Type v)
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    [MeasurableSpace Ω'] [TopologicalSpace Ω'] [BorelSpace Ω']
    (ι : Type w) (L : Filter ι)
    (νs : ι → ProbabilityMeasure Ω) (ν : ProbabilityMeasure Ω)
    (f : Ω → Ω') : Prop :=
  ∀ hf : Continuous f, Filter.Tendsto νs L (nhds ν) →
    Filter.Tendsto (fun i ↦ (νs i).map hf.measurable.aemeasurable) L
      (nhds (ν.map hf.measurable.aemeasurable))

/--
Normalized Stage1 statement-shape candidate for THM-M-1014.

This is stated directly in mathlib's `ProbabilityMeasure` object model for weak
convergence.  It is intentionally not a raw random-variable statement; the law
of a random variable is represented by the corresponding push-forward measure.
-/
def StatementShape
    (Ω : Type u) (Ω' : Type v)
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    [MeasurableSpace Ω'] [TopologicalSpace Ω'] [BorelSpace Ω']
    (ι : Type w) (L : Filter ι)
    (νs : ι → ProbabilityMeasure Ω) (ν : ProbabilityMeasure Ω)
    (f : Ω → Ω') : Prop :=
  ContinuousMappingTheorem Ω Ω' ι L νs ν f

/-- The Stage1 statement shape unfolds to the probability-measure theorem. -/
theorem statementShape_iff
    (Ω : Type u) (Ω' : Type v)
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    [MeasurableSpace Ω'] [TopologicalSpace Ω'] [BorelSpace Ω']
    (ι : Type w) (L : Filter ι)
    (νs : ι → ProbabilityMeasure Ω) (ν : ProbabilityMeasure Ω)
    (f : Ω → Ω') :
    StatementShape Ω Ω' ι L νs ν f ↔
      ∀ hf : Continuous f, Filter.Tendsto νs L (nhds ν) →
        Filter.Tendsto (fun i ↦ (νs i).map hf.measurable.aemeasurable) L
          (nhds (ν.map hf.measurable.aemeasurable)) :=
  Iff.rfl

/--
Checked mathlib wrapper for the continuous mapping theorem.

Proof body is supplied by the pinned mathlib theorem
`ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous`.
-/
theorem continuousMappingTheorem_mathlib_wrapper
    {Ω : Type u} {Ω' : Type v}
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    [MeasurableSpace Ω'] [TopologicalSpace Ω'] [BorelSpace Ω']
    {ι : Type w} {L : Filter ι}
    (νs : ι → ProbabilityMeasure Ω) (ν : ProbabilityMeasure Ω)
    {f : Ω → Ω'} (hf : Continuous f)
    (hlim : Filter.Tendsto νs L (nhds ν)) :
    Filter.Tendsto (fun i ↦ (νs i).map hf.measurable.aemeasurable) L
      (nhds (ν.map hf.measurable.aemeasurable)) :=
  ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous νs ν hlim hf

/-- Predicate-level wrapper: the local statement shape is fulfilled by pinned mathlib. -/
theorem continuousMappingTheorem_holds
    (Ω : Type u) (Ω' : Type v)
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    [MeasurableSpace Ω'] [TopologicalSpace Ω'] [BorelSpace Ω']
    (ι : Type w) (L : Filter ι)
    (νs : ι → ProbabilityMeasure Ω) (ν : ProbabilityMeasure Ω)
    (f : Ω → Ω') :
    ContinuousMappingTheorem Ω Ω' ι L νs ν f :=
  fun hf hlim => continuousMappingTheorem_mathlib_wrapper νs ν hf hlim

/-- The push-forward map on probability measures is continuous in the weak topology. -/
theorem probabilityMeasure_pushForward_continuous_mathlib_wrapper
    {Ω : Type u} {Ω' : Type v}
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    [MeasurableSpace Ω'] [TopologicalSpace Ω'] [BorelSpace Ω']
    {f : Ω → Ω'} (hf : Continuous f) :
    Continuous (fun ν : ProbabilityMeasure Ω ↦ ν.map hf.measurable.aemeasurable) :=
  ProbabilityMeasure.continuous_map hf

/-- Integral-test-function characterization of weak convergence for probability measures. -/
theorem probabilityMeasure_tendsto_iff_integral_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] [TopologicalSpace Ω]
    [OpensMeasurableSpace Ω]
    {ι : Type w} {L : Filter ι}
    {νs : ι → ProbabilityMeasure Ω} {ν : ProbabilityMeasure Ω} :
    Filter.Tendsto νs L (nhds ν) ↔
      ∀ g : BoundedContinuousFunction Ω ℝ,
        Filter.Tendsto (fun i ↦ ∫ x, g x ∂(νs i : Measure Ω)) L
          (nhds (∫ x, g x ∂(ν : Measure Ω))) :=
  ProbabilityMeasure.tendsto_iff_forall_integral_tendsto

/--
Law/push-forward field of mathlib's random-variable convergence definition.

This records the PUB-05 distinction in checked form: random-variable convergence
in distribution is represented by weak convergence of the push-forward
probability measures, not by a separate random-variable topology.
-/
theorem tendstoInDistribution_laws_tendsto_mathlib_field
    {ι E Ω' : Type*} {Ω : ι → Type*}
    [MeasurableSpace E] [TopologicalSpace E] [OpensMeasurableSpace E]
    {m : ∀ i, MeasurableSpace (Ω i)}
    {μ : (i : ι) → Measure (Ω i)} [∀ i, IsProbabilityMeasure (μ i)]
    {m' : MeasurableSpace Ω'} {μ' : Measure Ω'} [IsProbabilityMeasure μ']
    {X : (i : ι) → Ω i → E} {Z : Ω' → E} {l : Filter ι}
    (h : TendstoInDistribution X l Z μ μ') :
    Filter.Tendsto (β := ProbabilityMeasure E)
      (fun n ↦
        ⟨(μ n).map (X n), Measure.isProbabilityMeasure_map (h.forall_aemeasurable n)⟩) l
      (nhds ⟨μ'.map Z, Measure.isProbabilityMeasure_map h.aemeasurable_limit⟩) :=
  h.tendsto

/--
Checked random-variable form of the continuous mapping theorem.

This wraps mathlib's `TendstoInDistribution.continuous_comp`, whose statement
is already named as the continuous mapping theorem for convergence in
distribution.
-/
theorem tendstoInDistribution_continuous_comp_mathlib_wrapper
    {ι E F Ω' : Type*} {Ω : ι → Type*}
    [MeasurableSpace E] [TopologicalSpace E] [OpensMeasurableSpace E]
    [MeasurableSpace F] [TopologicalSpace F] [BorelSpace F]
    {m : ∀ i, MeasurableSpace (Ω i)}
    {μ : (i : ι) → Measure (Ω i)} [∀ i, IsProbabilityMeasure (μ i)]
    {m' : MeasurableSpace Ω'} {μ' : Measure Ω'} [IsProbabilityMeasure μ']
    {X : (i : ι) → Ω i → E} {Z : Ω' → E} {l : Filter ι}
    {g : E → F} (hg : Continuous g)
    (h : TendstoInDistribution X l Z μ μ') :
    TendstoInDistribution (fun n ↦ g ∘ X n) l (g ∘ Z) μ μ' :=
  TendstoInDistribution.continuous_comp hg h

/-- mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.FiniteMeasure",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.Map",
  "Mathlib.MeasureTheory.Integral.BoundedContinuousFunction",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution"
]

/-- Pinned mathlib revision used for the audited continuous-mapping anchors. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Primary mathlib source files for the continuous-mapping anchors. -/
def mathlibPrimarySourceFiles : List String := [
  "Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean",
  "Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean"
]

/-- Integration-ready public note for `S1-M-293-PUB-05`. -/
def publicTheoremTreeNotePUB05 : String :=
  "The measure-level continuous mapping theorem is stated in mathlib as weak convergence in the " ++
  "`ProbabilityMeasure` topology: if `νs -> ν`, then the push-forwards " ++
  "`(νs i).map f` converge to `ν.map f`. The random-variable theorem is the same " ++
  "measure-level statement applied to laws: `TendstoInDistribution X l Z μ μ'` stores " ++
  "weak convergence of the push-forward laws `(μ n).map (X n)` to `μ'.map Z`, and " ++
  "`TendstoInDistribution.continuous_comp` pushes those laws forward again along the continuous map."

/-- Metadata row for optional continuous-mapping variants that are not closed here. -/
structure OptionalVariantChild where
  childId : String
  variantScope : String
  currentStatus : String
  closureGate : String
deriving Repr

/--
Optional variants for `S1-M-293-PUB-07` that remain unchecked child tasks.

The checked wrappers in this file close only the probability-measure weak
convergence theorem and mathlib's law/push-forward `TendstoInDistribution`
continuous-composition theorem.  These rows deliberately do not assert a proof
of almost-sure-continuity, discontinuity-set, Skorokhod-space, or path-space
variants.
-/
def optionalVariantUncheckedChildrenPUB07 : List OptionalVariantChild := [
  {
    childId := "S1-M-293-L025",
    variantScope := "almost-sure-continuity or discontinuity-set continuous mapping variants",
    currentStatus := "unchecked_optional_child",
    closureGate := "must be separately stated, pinned/imported/checked locally, and given a <=100-step leaf ledger"
  },
  {
    childId := "S1-M-293-L026",
    variantScope := "Skorokhod-space, stochastic-process path-space, or other path mapping variants",
    currentStatus := "unchecked_optional_child",
    closureGate := "must be separately stated, pinned/imported/checked locally, and given a <=100-step leaf ledger"
  }
]

/-- Integration-ready public note for `S1-M-293-PUB-07`. -/
def publicOptionalVariantNotePUB07 : String :=
  "Optional continuous-mapping variants are not counted as closed by the core " ++
  "`ProbabilityMeasure` and `TendstoInDistribution.continuous_comp` wrappers. " ++
  "Almost-sure-continuity or discontinuity-set variants and Skorokhod/path-space " ++
  "continuous mapping theorems remain unchecked child tasks unless a later patch " ++
  "separately states the exact variant, pins/imports a proof or supplies a local " ++
  "proof body, runs a repo-local Lean check, and adds an independent <=100-step " ++
  "leaf ledger."

/-- Pinned declarations used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous",
  "MeasureTheory.TendstoInDistribution.continuous_comp",
  "MeasureTheory.ProbabilityMeasure.continuous_map",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_lintegral_tendsto",
  "MeasureTheory.FiniteMeasure.tendsto_map_of_tendsto_of_continuous",
  "MeasureTheory.FiniteMeasure.continuous_map",
  "MeasureTheory.Measure.map",
  "MeasureTheory.Measure.map_map",
  "MeasureTheory.Measure.map_apply",
  "MeasureTheory.ConvergenceInDistribution"
]

/-- Search terms used while auditing for a terminal continuous-mapping anchor. -/
def anchorSearchTerms : List String := [
  "continuous mapping theorem",
  "weak convergence probability measure map continuous",
  "convergence in distribution map continuous",
  "tendsto_map_of_tendsto_of_continuous",
  "ProbabilityMeasure.continuous_map",
  "Measure.map continuous Tendsto",
  "law push-forward weak convergence"
]

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check ContinuousMappingTheorem
#check continuousMappingTheorem_mathlib_wrapper
#check continuousMappingTheorem_holds
#check probabilityMeasure_pushForward_continuous_mathlib_wrapper
#check probabilityMeasure_tendsto_iff_integral_mathlib_wrapper
#check tendstoInDistribution_laws_tendsto_mathlib_field
#check tendstoInDistribution_continuous_comp_mathlib_wrapper
#check mathlibPinnedRevision
#check mathlibPrimarySourceFiles
#check publicTheoremTreeNotePUB05
#check OptionalVariantChild
#check optionalVariantUncheckedChildrenPUB07
#check publicOptionalVariantNotePUB07
#check ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
#check TendstoInDistribution.continuous_comp
#check ProbabilityMeasure.continuous_map
#check ProbabilityMeasure.tendsto_iff_forall_integral_tendsto
#check FiniteMeasure.tendsto_map_of_tendsto_of_continuous

end S1_M_293
end Stage1
end AwesomeTheorems
