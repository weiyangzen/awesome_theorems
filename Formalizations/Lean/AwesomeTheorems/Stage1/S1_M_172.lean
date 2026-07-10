import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.Topology.MetricSpace.Sequences
import Mathlib.Topology.Sequences

/-!
# S1-M-172 / THM-M-1292: Struwe compactness lemma

This Stage1 artifact records a conservative Lean 4 boundary for a Struwe
compactness/monotonicity-trick lemma used as an alternative to assuming a full
Palais-Smale condition at the outset.

The pinned mathlib snapshot has the generic substrates needed to express the
boundary: Frechet derivatives, dual-norm residuals, `Tendsto`, compactness and
subsequence extraction, Lp/Sobolev infrastructure, and distribution-adjacent
analysis.  It does not provide a terminal Struwe compactness theorem,
Palais-Smale min-max package, or PDE-specific entropy estimate.  The
declarations below therefore expose the exact formalization boundary and prove
only low-risk wrappers around available mathlib facts.
-/

noncomputable section

open Filter
open scoped Topology
open scoped ENNReal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_172

universe u v

/-- Frechet-derivative residual for a real-valued functional on a normed space. -/
def FrechetResidual
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (F : E → ℝ) (x : E) : ℝ :=
  ‖fderiv ℝ F x‖

/-- A Palais-Smale sequence at level `c`, expressed with mathlib `Tendsto`. -/
def IsPalaisSmaleSeq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (F : E → ℝ) (c : ℝ) (u : ℕ → E) : Prop :=
  Tendsto (fun n => F (u n)) atTop (𝓝 c) ∧
    Tendsto (fun n => FrechetResidual F (u n)) atTop (𝓝 0)

/-- Concrete topological target: a sequence has a convergent subsequence. -/
def HasConvergentSubsequence
    {E : Type u} [TopologicalSpace E] (u : ℕ → E) : Prop :=
  ∃ x : E, ∃ φ : ℕ → ℕ, StrictMono φ ∧ Tendsto (fun n => u (φ n)) atTop (𝓝 x)

/-- Palais-Smale compactness at a single level. -/
def PSCompactnessAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (F : E → ℝ) (c : ℝ) : Prop :=
  ∀ u : ℕ → E, IsPalaisSmaleSeq F c u → HasConvergentSubsequence u

/--
Abstract min-max class used by the Struwe monotonicity-trick interface.

The `sweepout` and `support` fields are intentionally type-level data rather
than a concrete path or cycle space: different Struwe applications use paths,
families of maps, or homology classes.  The `level` field is the class-specific
min-max value for a functional.
-/
structure MinMaxClass (E : Type u) where
  sweepout : Type u
  support : sweepout → Set E
  nonempty_sweepout : Nonempty sweepout
  level : (E → ℝ) → ℝ

/-- The level function induced by an abstract min-max class. -/
def minmaxLevelFromClass {E : Type u} (C : MinMaxClass E) (F : E → ℝ) : ℝ :=
  C.level F

/-- The class-induced level unfolds to the `level` field. -/
theorem minmaxLevelFromClass_eq {E : Type u} (C : MinMaxClass E) (F : E → ℝ) :
    minmaxLevelFromClass C F = C.level F :=
  rfl

/--
Deformation-lemma package for a level window.

The proposition-valued fields are named proof obligations, not proof evidence
for Struwe's lemma.  A terminal proof must replace them by local estimates for
the selected min-max class and functional.
-/
structure DeformationLemmaPackage (E : Type u) where
  deformation : E → E
  classPreserved : Prop
  fixedOutsideWindow : Prop
  decreasesNearLevel : Prop
  residualControl : Prop

/--
Pseudo-gradient flow package for a variational functional.

This records the API needed by the deformation lemma: a vector field, its flow,
and the descent/existence/regularity obligations that future local proof leaves
must discharge.
-/
structure PseudoGradientFlowPackage (E : Type u) where
  vectorField : E → E
  flow : ℝ → E → E
  flowAtZero : Prop
  localExistence : Prop
  descentEstimate : Prop
  residualCompatibility : Prop

/--
Good-parameter differentiability rule for a min-max level.

For each good parameter, this package supplies the derivative of the level and
the checked Lean predicate that the one-dimensional level function has that
derivative at the parameter.
-/
structure GoodParameterDifferentiabilityRule
    (level : ℝ → ℝ) (goodParameter : ℝ → Prop) where
  derivative : ℝ → ℝ
  differentiableAtGood : ∀ σ, goodParameter σ → HasDerivAt level (derivative σ) σ

/-- Extract the differentiability fact at a good parameter. -/
theorem GoodParameterDifferentiabilityRule.hasDerivAt
    {level : ℝ → ℝ} {goodParameter : ℝ → Prop}
    (R : GoodParameterDifferentiabilityRule level goodParameter)
    {σ : ℝ} (hσ : goodParameter σ) :
    HasDerivAt level (R.derivative σ) σ :=
  R.differentiableAtGood σ hσ

/--
Concrete PDE-side estimate package for the Struwe entropy branch.

`observable` is the PDE quantity whose `L^p` control is needed; `sobolevProbe`
is the Sobolev-side controlled quantity, such as a gradient or localized
derivative proxy.  The bounds are parameter dependent because Struwe's
monotonicity trick usually works along a real parameter family.
-/
structure StruwePDEEstimatePackage
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ω : Type v) [MeasurableSpace Ω] where
  measure : MeasureTheory.Measure Ω
  observable : E → Ω → ℝ
  sobolevProbe : E → Ω → ℝ
  lpExponent : ℝ≥0∞
  sobolevExponent : ℝ≥0∞
  normBound : ℝ → ℝ
  lpBound : ℝ → ℝ≥0∞
  sobolevBound : ℝ → ℝ≥0∞
  entropyFunctional : ℝ → E → ℝ
  entropyUpperBound : ℝ → ℝ

namespace StruwePDEEstimatePackage

/--
Concrete replacement for the former abstract `entropyBound` field.

It records the simultaneous norm, Lp, Sobolev-probe, and entropy estimates that
future PDE specializations must prove for every sequence element.
-/
structure EntropyEstimate
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (D : StruwePDEEstimatePackage E Ω) (σ : ℝ) (u : E) : Prop where
  norm_le : ‖u‖ ≤ D.normBound σ
  observable_memLp : MeasureTheory.MemLp (D.observable u) D.lpExponent D.measure
  observable_eLpNorm_le :
    MeasureTheory.eLpNorm (D.observable u) D.lpExponent D.measure ≤ D.lpBound σ
  sobolev_memLp : MeasureTheory.MemLp (D.sobolevProbe u) D.sobolevExponent D.measure
  sobolev_eLpNorm_le :
    MeasureTheory.eLpNorm (D.sobolevProbe u) D.sobolevExponent D.measure ≤
      D.sobolevBound σ
  entropy_le : D.entropyFunctional σ u ≤ D.entropyUpperBound σ

/--
Concrete replacement for the former abstract `boundednessOrCoercivityInput`.

The obligation is now an explicit implication from checked Lp/Sobolev/entropy
bounds to a norm bound in the ambient variational space.
-/
def BoundednessOrCoercivityInput
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (D : StruwePDEEstimatePackage E Ω) : Prop :=
  ∀ σ u,
    MeasureTheory.MemLp (D.observable u) D.lpExponent D.measure →
      MeasureTheory.eLpNorm (D.observable u) D.lpExponent D.measure ≤ D.lpBound σ →
        MeasureTheory.MemLp (D.sobolevProbe u) D.sobolevExponent D.measure →
          MeasureTheory.eLpNorm (D.sobolevProbe u) D.sobolevExponent D.measure ≤
              D.sobolevBound σ →
            D.entropyFunctional σ u ≤ D.entropyUpperBound σ →
              ‖u‖ ≤ D.normBound σ

/-- Build the concrete entropy estimate from the coercivity input and PDE bounds. -/
theorem entropyEstimate_of_bounds
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    {D : StruwePDEEstimatePackage E Ω} {σ : ℝ} {u : E}
    (hcoercive : D.BoundednessOrCoercivityInput)
    (hLp : MeasureTheory.MemLp (D.observable u) D.lpExponent D.measure)
    (hLpBound :
      MeasureTheory.eLpNorm (D.observable u) D.lpExponent D.measure ≤ D.lpBound σ)
    (hSobolev :
      MeasureTheory.MemLp (D.sobolevProbe u) D.sobolevExponent D.measure)
    (hSobolevBound :
      MeasureTheory.eLpNorm (D.sobolevProbe u) D.sobolevExponent D.measure ≤
        D.sobolevBound σ)
    (hEntropy : D.entropyFunctional σ u ≤ D.entropyUpperBound σ) :
    D.EntropyEstimate σ u :=
  ⟨hcoercive σ u hLp hLpBound hSobolev hSobolevBound hEntropy,
    hLp, hLpBound, hSobolev, hSobolevBound, hEntropy⟩

/-- The concrete entropy estimate exposes its ambient norm bound. -/
theorem EntropyEstimate.norm_bound
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    {D : StruwePDEEstimatePackage E Ω} {σ : ℝ} {u : E}
    (h : D.EntropyEstimate σ u) :
    ‖u‖ ≤ D.normBound σ :=
  h.norm_le

/-- The concrete entropy estimate exposes its `MemLp` observable control. -/
theorem EntropyEstimate.observable_memLp'
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    {D : StruwePDEEstimatePackage E Ω} {σ : ℝ} {u : E}
    (h : D.EntropyEstimate σ u) :
    MeasureTheory.MemLp (D.observable u) D.lpExponent D.measure :=
  h.observable_memLp

/-- The concrete entropy estimate exposes its Sobolev-probe `eLpNorm` bound. -/
theorem EntropyEstimate.sobolev_eLpNorm_bound
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    {D : StruwePDEEstimatePackage E Ω} {σ : ℝ} {u : E}
    (h : D.EntropyEstimate σ u) :
    MeasureTheory.eLpNorm (D.sobolevProbe u) D.sobolevExponent D.measure ≤
      D.sobolevBound σ :=
  h.sobolev_eLpNorm_le

end StruwePDEEstimatePackage

/--
Abstract variational problem data for a Struwe monotonicity/compactness lemma.

The remaining proposition-valued fields are the current formalization boundary:
a terminal formalization must replace them by concrete min-max classes,
parameter monotonicity, and deformation estimates.  The entropy/coercivity side
is no longer a bare proposition: it is routed through `pdeEstimates`, whose
obligations are concrete norm, Lp, Sobolev-probe, and entropy estimates.
-/
structure StruweCompactnessProblem
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ω : Type v) [MeasurableSpace Ω] where
  parameterSet : Set ℝ
  goodParameter : ℝ → Prop
  functional : ℝ → E → ℝ
  minmaxClass : MinMaxClass E
  minmaxLevel : ℝ → ℝ
  pdeEstimates : StruwePDEEstimatePackage E Ω
  minmaxLevel_eq_class_level :
    ∀ σ, minmaxLevel σ = minmaxLevelFromClass minmaxClass (functional σ)
  deformationPackage : ℝ → DeformationLemmaPackage E
  pseudoGradientFlow : ℝ → PseudoGradientFlowPackage E
  goodParameterDifferentiabilityRule :
    GoodParameterDifferentiabilityRule minmaxLevel goodParameter
  monotoneParameterFamily : Prop
  minmaxGeometry : Prop
  differentiabilityOfMinmaxLevel : Prop
  deformationEstimate : Prop

/-- Existence of the PS/entropy sequence supplied by the Struwe argument. -/
def PSAlternativeExists
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω) : Prop :=
  ∀ σ ∈ P.parameterSet,
    P.goodParameter σ →
      ∃ u : ℕ → E,
        IsPalaisSmaleSeq (P.functional σ) (P.minmaxLevel σ) u ∧
          ∀ n : ℕ, P.pdeEstimates.EntropyEstimate σ (u n)

/-- Compactness conclusion after adding a Palais-Smale compactness criterion. -/
def CompactnessAlternativeConclusion
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω) : Prop :=
  ∀ σ ∈ P.parameterSet,
    P.goodParameter σ →
      PSCompactnessAt (P.functional σ) (P.minmaxLevel σ) →
        ∃ u : ℕ → E,
          IsPalaisSmaleSeq (P.functional σ) (P.minmaxLevel σ) u ∧
            (∀ n : ℕ, P.pdeEstimates.EntropyEstimate σ (u n)) ∧
              HasConvergentSubsequence u

/--
Entropy-aware compactness criterion for one good parameter.

This is the checked Stage1 boundary for the compactness-api branch: once the
Struwe argument has produced a PS sequence with concrete entropy/PDE estimates,
this criterion is exactly the remaining theorem needed to extract a convergent
subsequence.  Concrete PDE applications should prove this from compact
embeddings, weak-to-strong upgrades, or a Palais-Smale theorem in the selected
function space.
-/
def EntropyCompactnessCriterion
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω) (σ : ℝ) : Prop :=
  ∀ u : ℕ → E,
    IsPalaisSmaleSeq (P.functional σ) (P.minmaxLevel σ) u →
      (∀ n : ℕ, P.pdeEstimates.EntropyEstimate σ (u n)) →
        HasConvergentSubsequence u

/-- Candidate readings considered for the THM-M-1292 variant-choice child task. -/
inductive StruweVariantChoice where
  | abstractMonotonicityTrick
  | pdeEntropyCompactnessLemma
  | minMaxCompactnessAlternative
  | concreteFunctionalFamilyTheorem
  deriving DecidableEq

/--
Selected Stage1 variant for THM-M-1292.

The repo-local target is the abstract Struwe monotonicity trick: a real
parameter family of variational functionals, a min-max level, good parameters
where that level is differentiable, deformation estimates, and
boundedness/coercivity input produce Palais-Smale/entropy sequences.  The PDE
entropy lemma, standalone compactness alternative, and concrete
functional-family theorem are downstream specializations, not the current root
variant.
-/
def selectedVariant : StruweVariantChoice :=
  .abstractMonotonicityTrick

/-- The variant choice is definitionally fixed to the abstract monotonicity trick. -/
theorem selectedVariant_eq_abstractMonotonicityTrick :
    selectedVariant = StruweVariantChoice.abstractMonotonicityTrick :=
  rfl

/-- Exact parameters attached to the selected THM-M-1292 variant. -/
def selectedVariantParameters : List String := [
  "variant: abstract Struwe monotonicity trick",
  "ambient_space: arbitrary real normed vector space E",
  "pde_domain: measurable space Omega carrying the observed PDE quantities",
  "parameter: sigma : Real with sigma in P.parameterSet and P.goodParameter sigma",
  "functional_family: P.functional : Real -> E -> Real",
  "level_function: P.minmaxLevel : Real -> Real, tied to P.minmaxClass by P.minmaxLevel_eq_class_level",
  "pde_estimates: P.pdeEstimates packages normBound, MemLp/eLpNorm Lp control, Sobolev-probe control, entropyFunctional, and BoundednessOrCoercivityInput",
  "hypotheses: monotoneParameterFamily, minmaxGeometry, differentiabilityOfMinmaxLevel, deformationEstimate, pdeEstimates.BoundednessOrCoercivityInput",
  "output: PSAlternativeExists P, i.e. a Palais-Smale sequence at P.minmaxLevel sigma with concrete PDE entropy estimates along the sequence",
  "compactness_followup: CompactnessAlternativeConclusion P additionally requires PSCompactnessAt for the chosen level",
  "excluded_root_variants: PDE entropy compactness lemma, standalone min-max compactness alternative, concrete functional-family theorem"
]

/--
Normalized Stage1 statement shape for Struwe's compactness lemma.

Read this as the monotonicity-trick branch: monotone parameter family,
min-max geometry, differentiability of the level at good parameters,
deformation estimates, and boundedness/coercivity input produce the
Palais-Smale/entropy sequence.  A separate wrapper below records the standard
compactness consequence when a Palais-Smale compactness criterion is available.
-/
def StatementShape
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ω : Type v) [MeasurableSpace Ω] : Prop :=
  ∀ P : StruweCompactnessProblem E Ω,
    P.monotoneParameterFamily →
      P.minmaxGeometry →
        P.differentiabilityOfMinmaxLevel →
          P.deformationEstimate →
            P.pdeEstimates.BoundednessOrCoercivityInput →
              PSAlternativeExists P

/--
Public statement-normalization note for THM-M-1292.

`AwesomeTheorems.Stage1.S1_M_172.StatementShape` is the current repo-local Lean
boundary for this Stage1 slot.  It records an abstract monotonicity-trick
interface that produces Palais-Smale/entropy sequences from placeholder
variational hypotheses; it is not a terminal Struwe compactness proof, and it
does not yet prove the concrete min-max API obligations, entropy estimates, or
Palais-Smale compactness theorem needed to close the mathematical statement.
-/
def statementNormalizationNote : List String := [
  "THM-M-1292.statement",
  "current_repo_local_boundary: AwesomeTheorems.Stage1.S1_M_172.StatementShape",
  "scope: abstract Struwe monotonicity-trick statement shape producing PS/entropy sequences",
  "not_terminal_proof: no terminal Struwe compactness theorem is proved here",
  "checked_api_boundary: MinMaxClass, minmaxLevelFromClass, DeformationLemmaPackage, PseudoGradientFlowPackage, GoodParameterDifferentiabilityRule",
  "checked_entropy_api_boundary: StruwePDEEstimatePackage, EntropyEstimate, BoundednessOrCoercivityInput, entropyEstimate_of_bounds",
  "open_formalization_debt: concrete min-max API proofs, PDE estimates for a selected model, and PS compactness criterion remain to be supplied"
]

/-- The statement shape unfolds to the expected quantified problem interface. -/
theorem statementShape_iff_forall_problem
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ω : Type v) [MeasurableSpace Ω] :
    StatementShape E Ω ↔
      ∀ P : StruweCompactnessProblem E Ω,
        P.monotoneParameterFamily →
          P.minmaxGeometry →
            P.differentiabilityOfMinmaxLevel →
              P.deformationEstimate →
                P.pdeEstimates.BoundednessOrCoercivityInput →
                  PSAlternativeExists P :=
  Iff.rfl

/-- The selected problem's level is exactly the level induced by its min-max class. -/
theorem StruweCompactnessProblem.minmaxLevel_eq_fromClass
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω) (σ : ℝ) :
    P.minmaxLevel σ = minmaxLevelFromClass P.minmaxClass (P.functional σ) :=
  P.minmaxLevel_eq_class_level σ

/-- Good parameters give differentiability of the selected min-max level. -/
theorem StruweCompactnessProblem.hasDerivAt_minmaxLevel_of_good
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω) {σ : ℝ} (hσ : P.goodParameter σ) :
    HasDerivAt P.minmaxLevel (P.goodParameterDifferentiabilityRule.derivative σ) σ :=
  P.goodParameterDifferentiabilityRule.hasDerivAt hσ

/-- Concrete checked names supplied for the `THM-M-1292.minmax-api` child. -/
def minmaxApiRecord : List String := [
  "MinMaxClass: abstract sweepout/support/nonempty/level interface",
  "minmaxLevelFromClass: class-induced level function",
  "DeformationLemmaPackage: deformation, class preservation, window fixing, decrease, residual control",
  "PseudoGradientFlowPackage: vector field, flow, existence, descent, residual compatibility",
  "GoodParameterDifferentiabilityRule: HasDerivAt rule at every good parameter",
  "StruweCompactnessProblem.minmaxLevel_eq_fromClass: checked level projection",
  "StruweCompactnessProblem.hasDerivAt_minmaxLevel_of_good: checked good-parameter differentiability projection"
]

/-- Concrete checked names supplied for the `THM-M-1292.entropy-api` child. -/
def entropyApiRecord : List String := [
  "StruwePDEEstimatePackage: PDE estimate data with measure, observable, Sobolev probe, Lp exponents, norm/Lp/Sobolev bounds, and entropy functional",
  "StruwePDEEstimatePackage.EntropyEstimate: simultaneous norm, MemLp, eLpNorm, Sobolev-probe, and entropy estimates for one state",
  "StruwePDEEstimatePackage.BoundednessOrCoercivityInput: explicit coercivity implication from Lp/Sobolev/entropy bounds to ambient norm control",
  "StruwePDEEstimatePackage.entropyEstimate_of_bounds: checked constructor from coercivity plus concrete PDE estimates",
  "StruwePDEEstimatePackage.EntropyEstimate.norm_bound: checked projection of ambient norm control",
  "StruwePDEEstimatePackage.EntropyEstimate.observable_memLp': checked projection of observable MemLp control",
  "StruwePDEEstimatePackage.EntropyEstimate.sobolev_eLpNorm_bound: checked projection of Sobolev-probe eLpNorm control",
  "StruweCompactnessProblem.pdeEstimates: replacement for former abstract entropy/coercivity fields"
]

/-- Concrete checked names supplied for the `THM-M-1292.compactness-api` child. -/
def compactnessApiRecord : List String := [
  "PSCompactnessAt: abstract levelwise Palais-Smale compactness criterion",
  "EntropyCompactnessCriterion: entropy-aware compactness branch for PS/entropy sequences",
  "HasConvergentSubsequence.of_psCompactnessAt: checked application of PSCompactnessAt",
  "hasConvergentSubsequence_of_isCompact_range: checked extraction from IsCompact.tendsto_subseq",
  "psCompactnessAt_of_compact_range_bound: compact containment instantiates PSCompactnessAt",
  "EntropyCompactnessCriterion.of_compact_range_bound: compact containment instantiates the PS/entropy compactness branch",
  "compactnessAlternativeConclusion_of_psAlternative: PS alternative plus PSCompactnessAt gives the convergent-subsequence conclusion",
  "compactnessAlternativeConclusion_of_psAlternative_and_entropyCompactness: PS/entropy alternative plus EntropyCompactnessCriterion gives the convergent-subsequence conclusion",
  "open_formalization_debt: concrete compact embedding, weak-to-strong upgrade, or PDE-specific Palais-Smale theorem remains to be proved/imported"
]

/-- Extract energy convergence from the normalized Palais-Smale predicate. -/
theorem IsPalaisSmaleSeq.energy_tendsto
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : E → ℝ} {c : ℝ} {u : ℕ → E}
    (h : IsPalaisSmaleSeq F c u) :
    Tendsto (fun n => F (u n)) atTop (𝓝 c) :=
  h.1

/-- Extract derivative-residual convergence from the normalized Palais-Smale predicate. -/
theorem IsPalaisSmaleSeq.residual_tendsto_zero
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : E → ℝ} {c : ℝ} {u : ℕ → E}
    (h : IsPalaisSmaleSeq F c u) :
    Tendsto (fun n => FrechetResidual F (u n)) atTop (𝓝 0) :=
  h.2

/-- Apply an abstract PS compactness criterion to a PS sequence. -/
theorem HasConvergentSubsequence.of_psCompactnessAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : E → ℝ} {c : ℝ} {u : ℕ → E}
    (hcompact : PSCompactnessAt F c) (hps : IsPalaisSmaleSeq F c u) :
    HasConvergentSubsequence u :=
  hcompact u hps

/-- Compact sets provide the concrete subsequence target used by the PS gate. -/
theorem hasConvergentSubsequence_of_isCompact_range
    {E : Type u} [TopologicalSpace E] [FirstCountableTopology E]
    {K : Set E} {u : ℕ → E} (hK : IsCompact K) (hu : ∀ n, u n ∈ K) :
    HasConvergentSubsequence u := by
  rcases hK.tendsto_subseq hu with ⟨x, _hxK, φ, hφ, hlim⟩
  exact ⟨x, φ, hφ, by simpa [Function.comp_def] using hlim⟩

/--
A compact containment theorem is enough to instantiate the abstract
Palais-Smale compactness criterion.
-/
theorem psCompactnessAt_of_compact_range_bound
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [FirstCountableTopology E]
    {F : E → ℝ} {c : ℝ} {K : Set E}
    (hK : IsCompact K)
    (hcontained :
      ∀ u : ℕ → E, IsPalaisSmaleSeq F c u → ∀ n : ℕ, u n ∈ K) :
    PSCompactnessAt F c := by
  intro u hps
  exact hasConvergentSubsequence_of_isCompact_range hK (hcontained u hps)

/--
Compact containment of all PS/entropy sequences proves the entropy-aware
compactness criterion for the chosen Struwe problem and parameter.
-/
theorem EntropyCompactnessCriterion.of_compact_range_bound
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [FirstCountableTopology E]
    {Ω : Type v} [MeasurableSpace Ω]
    {P : StruweCompactnessProblem E Ω} {σ : ℝ} {K : Set E}
    (hK : IsCompact K)
    (hcontained :
      ∀ u : ℕ → E,
        IsPalaisSmaleSeq (P.functional σ) (P.minmaxLevel σ) u →
          (∀ n : ℕ, P.pdeEstimates.EntropyEstimate σ (u n)) →
            ∀ n : ℕ, u n ∈ K) :
    EntropyCompactnessCriterion P σ := by
  intro u hps hentropy
  exact hasConvergentSubsequence_of_isCompact_range hK (hcontained u hps hentropy)

/--
Once the Struwe PS alternative supplies a sequence, an ordinary PS compactness
criterion turns it into the compactness conclusion.
-/
theorem compactnessAlternativeConclusion_of_psAlternative
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω) (hAlt : PSAlternativeExists P) :
    CompactnessAlternativeConclusion P := by
  intro σ hσ hgood hcompact
  rcases hAlt σ hσ hgood with ⟨u, hps, hentropy⟩
  exact ⟨u, hps, hentropy, hcompact u hps⟩

/--
The entropy compactness branch closes the same compactness conclusion without
discarding the entropy estimates carried by the Struwe alternative.
-/
theorem compactnessAlternativeConclusion_of_psAlternative_and_entropyCompactness
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Ω : Type v} [MeasurableSpace Ω]
    (P : StruweCompactnessProblem E Ω)
    (hAlt : PSAlternativeExists P)
    (hEntropyCompact :
      ∀ σ ∈ P.parameterSet, P.goodParameter σ → EntropyCompactnessCriterion P σ) :
    CompactnessAlternativeConclusion P := by
  intro σ hσ hgood _hcompact
  rcases hAlt σ hσ hgood with ⟨u, hps, hentropy⟩
  exact ⟨u, hps, hentropy, hEntropyCompact σ hσ hgood u hps hentropy⟩

/-- Pinned mathlib revision audited for this Stage1 slot. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact audit record requested by `THM-M-1292.mathlib-audit`. -/
def mathlibAuditRecord : List String := [
  "mathlib_revision: 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "anchor: fderiv",
  "anchor: IsCompact.tendsto_subseq",
  "anchor: IsSeqCompact",
  "anchor: MeasureTheory.MemLp",
  "anchor: MeasureTheory.Lp",
  "anchor: MeasureTheory.eLpNorm",
  "infrastructure: Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "infrastructure: Mathlib.Analysis.Distribution.Distribution",
  "infrastructure: Mathlib.Analysis.ODE.Gronwall"
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.Calculus.Gradient.Basic",
  "Mathlib.Analysis.Calculus.LocalExtr.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.Topology.Sequences",
  "Mathlib.Topology.MetricSpace.Sequences",
  "Mathlib.Topology.UniformSpace.Cauchy",
  "Mathlib.Analysis.ODE.Gronwall"
]

/-- Search terms that did not locate a terminal Struwe compactness theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Struwe",
  "PalaisSmale",
  "Palais-Smale",
  "monotonicity trick",
  "compactness lemma",
  "minmax",
  "mountain pass",
  "entropy condition",
  "critical point compactness"
]

/--
External-audit record for `THM-M-1292.external-audit`.

This is intentionally a checked metadata boundary, not a theorem completion
claim.  Authenticated GitHub code search was unavailable in the worker
environment, so the current repo-local state remains negative local/source
audit plus a concrete authentication blocker for the public backfill.
-/
def externalAuditRecord : List String := [
  "child: S1-M-172-C007 / THM-M-1292.external-audit",
  "date: 2026-05-01",
  "local_dependencies_checked: mathlib and flt-regular in the current Lake closure",
  "mathlib_commit: 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "flt_regular_commit: 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
  "query_terms: Struwe, PalaisSmale, Palais-Smale, monotonicity trick, compactness lemma, minmax, mountain pass, entropy condition",
  "local_source_result: no matches in current Lake dependency Lean sources",
  "github_auth_status: gh not logged in and no GH_TOKEN/GITHUB_TOKEN available",
  "github_code_search_result: authenticated search blocked locally; unauthenticated GitHub code search requires sign-in",
  "repository_search_result: no repository-level Lean candidates for Struwe, PalaisSmale, Palais-Smale, monotonicity trick, compactness lemma, mountain pass, or entropy condition",
  "terminal_external_closure: none verified",
  "lake_dependency_feasibility: no candidate dependency to pin/import/check",
  "repo_local_integration_debt_gate: no completed-state repo_local_integration_debt is introduced"
]

/-- One integration-gate decision row for external Lean 4 theorem closures. -/
structure IntegrationGateDecisionRow where
  publicTaskId : String
  checkedLocalSurfaces : List String
  externalClosureFound : Bool
  repoLocalActionRequiredBeforeCompletion : String
  currentGateStatus : String
deriving Repr

/--
Integration-gate surface for `THM-M-1292.integration-gate`.

This row records the repo-local decision boundary: the current Lake closure has
no terminal Struwe/Palais-Smale compactness theorem to pin/import/check.  If a
future authenticated external audit locates such a Lean 4 closure, the public
task must remain open until that proof is either included in the repo-local
validation closure or a specific blocker is recorded.
-/
def integrationGateDecisionRows : List IntegrationGateDecisionRow := [
  { publicTaskId := "THM-M-1292.integration-gate",
    checkedLocalSurfaces := [
      "mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "flt-regular@56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
      "AwesomeTheorems.Stage1.S1_M_172.externalAuditRecord"
    ],
    externalClosureFound := false,
    repoLocalActionRequiredBeforeCompletion :=
      "No completion claim is permitted from anchor-only evidence.  If an external " ++
        "Lean 4 Struwe compactness, Palais-Smale compactness, monotonicity-trick, " ++
        "or min-max compactness proof is later found, pin/import/check it in the " ++
        "Lake closure or record a concrete blocker such as incompatible Lean " ++
        "toolchain, dependency conflict, license barrier, non-Lake project shape, " ++
        "or proof placeholders in the relevant path.",
    currentGateStatus :=
      "open_not_completed: no external Lean 4 closure was verified in the current " ++
        "repo-local Lake closure, and no external_upstream_anchor_only state is " ++
        "being counted as completed" }
]

/-- The integration-gate child contributes exactly one decision row. -/
theorem integrationGateDecisionRows_length :
    integrationGateDecisionRows.length = 1 :=
  rfl

/--
M0387 completion gate for the integration-gate child.

There is no completed-state repo-local integration debt because this artifact
does not count any external anchor-only evidence as a theorem closure.  The
parent theorem remains open until a terminal local proof body, mathlib wrapper,
or pinned external dependency is validated.
-/
def integrationGateCompletionGate : String :=
  "open_not_completed_no_repo_local_integration_debt: no external Lean 4 " ++
    "Struwe/Palais-Smale compactness closure is present in the current Lake " ++
    "validation closure; any future external closure must be pinned/imported/" ++
    "checked or blocked concretely before public completion"

/-- Current machine-proof debt classification for this repaired Stage1 module. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: full Struwe compactness lemma is not repo-local closed",
  "not_repo_local_closed: this file is a statement-shape wrapper plus checked min-max and PDE-estimate API anchors",
  "repo_local_integration_debt_gate: no completion claim may retain anchor-only external evidence"
]

/-- Theorem-internal child leaves for the next M0387-level module split. -/
def theoremInternalChildLeaves : List String := [
  "S1-M-172-leaf-001 statement normalization and notation freeze",
  "S1-M-172-leaf-002 variational Banach/Hilbert space object model and boundary-condition API",
  "S1-M-172-leaf-003 Palais-Smale sequence predicate and dual-residual normalization",
  "S1-M-172-leaf-004 monotone parameter family and min-max level differentiability bridge",
  "S1-M-172-leaf-005 deformation estimate and concrete norm/Sobolev/Lp entropy package",
  "S1-M-172-leaf-006 compactness criterion: boundedness/coercivity to convergent subsequence",
  "S1-M-172-leaf-007 weak/classical PDE formulation bridge for concrete Struwe applications",
  "S1-M-172-leaf-008 mathlib and external Lean 4 terminal theorem audit",
  "S1-M-172-leaf-009 pin/import/check or integration-blocker handling for any external closure",
  "S1-M-172-leaf-010 replacement of StatementShape by local proof body or checked upstream wrapper"
]

/-! ## Audit probes -/

#check fderiv
#check IsCompact
#check IsCompact.tendsto_subseq
#check IsPalaisSmaleSeq
#check PSCompactnessAt
#check CompactnessAlternativeConclusion
#check EntropyCompactnessCriterion
#check MinMaxClass
#check minmaxLevelFromClass
#check minmaxLevelFromClass_eq
#check DeformationLemmaPackage
#check PseudoGradientFlowPackage
#check GoodParameterDifferentiabilityRule
#check GoodParameterDifferentiabilityRule.hasDerivAt
#check StruwePDEEstimatePackage
#check StruwePDEEstimatePackage.EntropyEstimate
#check StruwePDEEstimatePackage.BoundednessOrCoercivityInput
#check StruwePDEEstimatePackage.entropyEstimate_of_bounds
#check StruwePDEEstimatePackage.EntropyEstimate.norm_bound
#check StruwePDEEstimatePackage.EntropyEstimate.observable_memLp'
#check StruwePDEEstimatePackage.EntropyEstimate.sobolev_eLpNorm_bound
#check StruweCompactnessProblem.minmaxLevel_eq_fromClass
#check StruweCompactnessProblem.hasDerivAt_minmaxLevel_of_good
#check minmaxApiRecord
#check entropyApiRecord
#check compactnessApiRecord
#check StruweVariantChoice
#check selectedVariant
#check selectedVariant_eq_abstractMonotonicityTrick
#check selectedVariantParameters
#check statementNormalizationNote
#check pinnedMathlibRevision
#check mathlibAuditRecord
#check externalAuditRecord
#check integrationGateDecisionRows
#check integrationGateDecisionRows_length
#check integrationGateCompletionGate
#check machineProofDebtClassification
#check theoremInternalChildLeaves
#check HasConvergentSubsequence.of_psCompactnessAt
#check hasConvergentSubsequence_of_isCompact_range
#check psCompactnessAt_of_compact_range_bound
#check EntropyCompactnessCriterion.of_compact_range_bound
#check compactnessAlternativeConclusion_of_psAlternative
#check compactnessAlternativeConclusion_of_psAlternative_and_entropyCompactness
#check IsSeqCompact
#check MeasureTheory.MemLp
#check MeasureTheory.Lp
#check MeasureTheory.eLpNorm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check Distribution
#check Distribution.mapCLM
#check gronwallBound
#check norm_le_gronwallBound_of_norm_deriv_right_le

end S1_M_172
end Stage1
end AwesomeTheorems
