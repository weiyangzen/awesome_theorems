import Mathlib.Analysis.InnerProductSpace.MeanErgodic
import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Function.ConditionalExpectation.CondexpL2
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# S1-M-246 / THM-M-1054: von Neumann mean ergodic theorem

This Stage1 artifact records a Lean 4 wrapper for the checked Hilbert-space
von Neumann mean ergodic theorem in pinned mathlib, and specializes it to the
Koopman operator on `L^2` induced by a measure-preserving map.

The checked conclusion is norm convergence of Cesaro/Birkhoff averages to the
orthogonal projection onto the fixed-vector subspace.  The stronger
probability-facing identification of this projection with conditional
expectation onto the invariant sigma-algebra, and with constants under
ergodicity, is kept as a statement boundary for later integration.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal MeasureTheory Topology

namespace AwesomeTheorems.Stage1.S1_M_246

universe u v w

variable {𝕜 : Type u} {H : Type v}
variable [RCLike 𝕜] [NormedAddCommGroup H] [InnerProductSpace 𝕜 H] [CompleteSpace H]

/-- Fixed vectors of a continuous linear operator. -/
abbrev FixedSubspace (U : H →L[𝕜] H) : Submodule 𝕜 H :=
  LinearMap.eqLocus U 1

/-- The Hilbert-space limit object in the von Neumann mean ergodic theorem. -/
abbrev FixedProjection (U : H →L[𝕜] H) (x : H) : H :=
  ((FixedSubspace U).orthogonalProjection x : H)

/-- Cesaro averages of iterates of a continuous linear self-map. -/
abbrev TimeAverage (U : H →L[𝕜] H) : ℕ → H → H :=
  birkhoffAverage 𝕜 U _root_.id

/-- Hilbert-space conclusion of the von Neumann mean ergodic theorem. -/
def HilbertMeanErgodicConclusion (U : H →L[𝕜] H) : Prop :=
  ∀ x : H, Tendsto (fun n : ℕ => TimeAverage U n x) atTop
    (𝓝 (FixedProjection U x))

/--
Stage1 statement shape for the Hilbert-space theorem: every contractive
operator has Cesaro averages converging to the fixed-subspace projection.
-/
def HilbertMeanErgodicStatementShape (𝕜 : Type u) (H : Type v)
    [RCLike 𝕜] [NormedAddCommGroup H] [InnerProductSpace 𝕜 H] [CompleteSpace H] :
    Prop :=
  ∀ U : H →L[𝕜] H, ‖U‖ ≤ 1 → HilbertMeanErgodicConclusion U

/-- Local wrapper around mathlib's von Neumann mean ergodic theorem. -/
theorem hilbert_meanErgodic_from_mathlib
    (U : H →L[𝕜] H) (hU : ‖U‖ ≤ 1) :
    HilbertMeanErgodicConclusion U := by
  intro x
  simpa [HilbertMeanErgodicConclusion, TimeAverage, FixedProjection, FixedSubspace]
    using ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
      (𝕜 := 𝕜) (E := H) U hU x

/-- Checked closure of the Hilbert-space statement shape. -/
theorem hilbertMeanErgodicStatementShape_from_mathlib :
    HilbertMeanErgodicStatementShape 𝕜 H := by
  intro U hU
  exact hilbert_meanErgodic_from_mathlib U hU

section L2Koopman

variable {α : Type w} [MeasurableSpace α] {μ : Measure α}
variable {E : Type v} [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]

/-- The `L^2` space used by this Stage1 slot. -/
abbrev L2Space (α : Type w) [MeasurableSpace α] (μ : Measure α)
    (E : Type v) [NormedAddCommGroup E] :=
  α →₂[μ] E

/--
Koopman operator on `L^2` induced by a measure-preserving self-map.

It sends an equivalence class represented by `g` to the class represented by
`g ∘ T`; mathlib provides it as a linear isometry on `Lp`.
-/
abbrev KoopmanOperator
    (𝕜 : Type u) [RCLike 𝕜]
    {α : Type w} [MeasurableSpace α] {μ : Measure α}
    (E : Type v) [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]
    (T : α → α) (hT : MeasurePreserving T μ μ) :
    L2Space α μ E →L[𝕜] L2Space α μ E :=
  (Lp.compMeasurePreservingₗᵢ 𝕜 (E := E) (p := (2 : ℝ≥0∞)) T hT).toContinuousLinearMap

/-- The Koopman operator is contractive, in fact an isometry, on `L^2`. -/
theorem koopmanOperator_norm_le_one
    (T : α → α) (hT : MeasurePreserving T μ μ) :
    ‖KoopmanOperator 𝕜 E T hT‖ ≤ 1 := by
  dsimp [KoopmanOperator]
  exact LinearIsometry.norm_toContinuousLinearMap_le _

/--
`L^2` von Neumann conclusion for a concrete measure-preserving system:
Koopman Cesaro averages converge in `L^2` norm to the orthogonal projection
onto the invariant/fixed-vector subspace.
-/
def L2KoopmanMeanErgodicConclusion
    (T : α → α) (hT : MeasurePreserving T μ μ) : Prop :=
  HilbertMeanErgodicConclusion
    (𝕜 := 𝕜) (H := L2Space α μ E)
    (KoopmanOperator 𝕜 E T hT)

/--
Checked `L^2` Koopman wrapper obtained by applying mathlib's Hilbert-space
mean ergodic theorem to `Lp.compMeasurePreserving`.
-/
theorem l2_koopman_meanErgodic_from_mathlib
    (T : α → α) (hT : MeasurePreserving T μ μ) :
    L2KoopmanMeanErgodicConclusion (𝕜 := 𝕜) (E := E) T hT :=
  hilbert_meanErgodic_from_mathlib
    (𝕜 := 𝕜) (H := L2Space α μ E)
    (KoopmanOperator 𝕜 E T hT)
    (koopmanOperator_norm_le_one (𝕜 := 𝕜) (E := E) T hT)

/--
Public audit alias for `S1-M-246-PUB-03`.

This is the fixed-projection `L^2` Koopman wrapper checked through the repo's
pinned mathlib dependency.  It deliberately has the same conclusion as
`l2_koopman_meanErgodic_from_mathlib`; the probability-facing
conditional-expectation and ergodic-constant interpretations remain outside
this checked theorem.
-/
theorem l2_koopman_fixedProjection_checked_at_pinned_mathlib
    (T : α → α) (hT : MeasurePreserving T μ μ) :
    L2KoopmanMeanErgodicConclusion (𝕜 := 𝕜) (E := E) T hT :=
  l2_koopman_meanErgodic_from_mathlib (𝕜 := 𝕜) (E := E) T hT

/-! ## Fixed `L^2` observables -/

/--
`L^2` observables invariant under the Koopman operator induced by `T`.

This is the repo-local bridge package for `S1-M-246-PUB-05`: it names the
observable-side fixedness predicate without identifying the fixed-vector
projection with conditional expectation.
-/
def InvariantL2Observable
    (T : α → α) (hT : MeasurePreserving T μ μ) (g : L2Space α μ E) : Prop :=
  KoopmanOperator 𝕜 E T hT g = g

/-- Submodule of `L^2` observables invariant under the Koopman operator. -/
abbrev InvariantL2Observables
    (T : α → α) (hT : MeasurePreserving T μ μ) : Submodule 𝕜 (L2Space α μ E) :=
  LinearMap.eqLocus (KoopmanOperator 𝕜 E T hT) 1

/--
Membership in `LinearMap.eqLocus (KoopmanOperator 𝕜 E T hT) 1` is exactly
the named invariant-`L^2` observable predicate.
-/
theorem mem_fixedSubspace_iff_invariantL2Observable
    (T : α → α) (hT : MeasurePreserving T μ μ) (g : L2Space α μ E) :
    g ∈ LinearMap.eqLocus (KoopmanOperator 𝕜 E T hT) 1 ↔
      InvariantL2Observable (𝕜 := 𝕜) (E := E) T hT g :=
  Iff.rfl

/--
The fixed-vector submodule for the Koopman operator is definitionally the
submodule of invariant `L^2` observables.
-/
theorem fixedSubspace_koopman_eq_invariantL2Observables
    (T : α → α) (hT : MeasurePreserving T μ μ) :
    FixedSubspace (KoopmanOperator 𝕜 E T hT) =
      InvariantL2Observables (𝕜 := 𝕜) (E := E) T hT :=
  rfl

/--
Observable-side formulation of Koopman invariance: composing a representative
with `T` agrees almost everywhere with the original `L^2` observable.
-/
theorem invariantL2Observable_iff_ae_comp_eq
    (T : α → α) (hT : MeasurePreserving T μ μ) (g : L2Space α μ E) :
    InvariantL2Observable (𝕜 := 𝕜) (E := E) T hT g ↔
      g ∘ T =ᵐ[μ] g := by
  constructor
  · intro hg
    have hg' : Lp.compMeasurePreserving T hT g = g := by
      simpa [InvariantL2Observable, KoopmanOperator] using hg
    have hcomp' : g =ᵐ[μ] g ∘ T := by
      simpa [hg'] using
        (Lp.coeFn_compMeasurePreserving (p := (2 : ℝ≥0∞)) g hT)
    exact hcomp'.symm
  · intro hg
    change Lp.compMeasurePreserving T hT g = g
    apply Subtype.ext
    exact AEEqFun.ext
      ((Lp.coeFn_compMeasurePreserving (p := (2 : ℝ≥0∞)) g hT).trans hg)

/-! ## Ergodic scalar constants -/

theorem scalar_koopman_const
    [IsFiniteMeasure μ] (T : α → α) (hT : MeasurePreserving T μ μ) (c : 𝕜) :
    InvariantL2Observable (𝕜 := 𝕜) (E := 𝕜) T hT
      (Lp.const (2 : ℝ≥0∞) μ c) := by
  change
    Lp.compMeasurePreserving (E := 𝕜) (p := (2 : ℝ≥0∞)) T hT
        (Lp.const (2 : ℝ≥0∞) μ c) =
      Lp.const (2 : ℝ≥0∞) μ c
  apply Subtype.ext
  apply AEEqFun.ext
  calc
    ((Lp.compMeasurePreserving (E := 𝕜) (p := (2 : ℝ≥0∞)) T hT
        (Lp.const (2 : ℝ≥0∞) μ c) : Lp 𝕜 (2 : ℝ≥0∞) μ) : α → 𝕜)
        =ᵐ[μ]
          ((Lp.const (2 : ℝ≥0∞) μ c : Lp 𝕜 (2 : ℝ≥0∞) μ) : α → 𝕜) ∘ T := by
            exact Lp.coeFn_compMeasurePreserving (p := (2 : ℝ≥0∞))
              (Lp.const (2 : ℝ≥0∞) μ c) hT
    _ =ᵐ[μ] Function.const α c := by
            simpa using hT.quasiMeasurePreserving.ae_eq_comp
              (Lp.coeFn_const (2 : ℝ≥0∞) μ c)
    _ =ᵐ[μ] ((Lp.const (2 : ℝ≥0∞) μ c : Lp 𝕜 (2 : ℝ≥0∞) μ) : α → 𝕜) := by
            exact (Lp.coeFn_const (2 : ℝ≥0∞) μ c).symm

/--
Under ergodicity and a probability measure, a scalar `L^2` observable fixed by
the Koopman operator is a.e. equal to the constant with value its integral.

This is the checked repo-local constant-identification component for
`S1-M-246-PUB-07`.
-/
theorem invariantScalarL2Observable_ae_eq_integral_const
    [IsProbabilityMeasure μ] (T : α → α) (hT : Ergodic T μ)
    (g : L2Space α μ 𝕜)
    (hg : InvariantL2Observable (𝕜 := 𝕜) (E := 𝕜) T hT.toMeasurePreserving g) :
    (g : α → 𝕜) =ᵐ[μ] Function.const α (∫ x, g x ∂μ) := by
  have hgA : (g : α →ₘ[μ] 𝕜).compMeasurePreserving T hT.toMeasurePreserving = g := by
    have hLp : Lp.compMeasurePreserving T hT.toMeasurePreserving g = g := by
      simpa [InvariantL2Observable, KoopmanOperator] using hg
    exact congrArg Subtype.val hLp
  rcases hT.eq_const_of_compMeasurePreserving_eq (g := (g : α →ₘ[μ] 𝕜)) hgA with ⟨c, hc⟩
  have hc_ae : (g : α → 𝕜) =ᵐ[μ] Function.const α c := by
    rw [hc]
    exact AEEqFun.coeFn_const α c
  have hcoef : ∫ x, g x ∂μ = c := by
    rw [integral_congr_ae hc_ae]
    simp
  simpa [hcoef] using hc_ae

/-- `Lp` equality form of `invariantScalarL2Observable_ae_eq_integral_const`. -/
theorem invariantScalarL2Observable_eq_const_integral
    [IsProbabilityMeasure μ] (T : α → α) (hT : Ergodic T μ)
    (g : L2Space α μ 𝕜)
    (hg : InvariantL2Observable (𝕜 := 𝕜) (E := 𝕜) T hT.toMeasurePreserving g) :
    g = Lp.const (2 : ℝ≥0∞) μ (∫ x, g x ∂μ) := by
  apply Subtype.ext
  exact AEEqFun.ext
    ((invariantScalarL2Observable_ae_eq_integral_const
      (𝕜 := 𝕜) T hT g hg).trans
        (Lp.coeFn_const (2 : ℝ≥0∞) μ (∫ x, g x ∂μ)).symm)

/--
Reduction form of the scalar ergodic `L^2` limit.

The remaining unchecked ingredient is the projection identity
`FixedProjection ... g = Lp.const 2 μ (∫ x, g x ∂μ)`.  Once supplied, the
checked fixed-projection mean-ergodic theorem immediately gives convergence to
the integral constant.
-/
theorem l2_koopman_ergodic_scalar_meanErgodic_const_of_fixedProjection_eq
    [IsProbabilityMeasure μ] (T : α → α) (hT : Ergodic T μ)
    (g : L2Space α μ 𝕜)
    (hproj :
      FixedProjection (KoopmanOperator 𝕜 𝕜 T hT.toMeasurePreserving) g =
        Lp.const (2 : ℝ≥0∞) μ (∫ x, g x ∂μ)) :
    Tendsto
      (fun n : ℕ => TimeAverage
        (KoopmanOperator 𝕜 𝕜 T hT.toMeasurePreserving) n g)
      atTop
      (𝓝 (Lp.const (2 : ℝ≥0∞) μ (∫ x, g x ∂μ))) := by
  have hmean :=
    l2_koopman_meanErgodic_from_mathlib
      (𝕜 := 𝕜) (E := 𝕜) T hT.toMeasurePreserving g
  simpa [hproj] using hmean

/--
Exact invariant measurable sets for a self-map.

This is the set-level package used by this Stage1 file for the invariant
sigma-algebra.  The later probability-facing bridge must still compare this
exact set-level object with the usual a.e. invariant `L^2` fixed-observable
formulation.
-/
def InvariantMeasurableSet (T : α → α) (s : Set α) : Prop :=
  MeasurableSet s ∧ T ⁻¹' s = s

theorem invariantMeasurableSet_univ (T : α → α) :
    InvariantMeasurableSet T Set.univ := by
  simp [InvariantMeasurableSet]

theorem InvariantMeasurableSet.compl {T : α → α} {s : Set α}
    (hs : InvariantMeasurableSet T s) :
    InvariantMeasurableSet T sᶜ := by
  refine ⟨hs.1.compl, ?_⟩
  ext x
  exact not_congr (Set.ext_iff.mp hs.2 x)

theorem invariantMeasurableSet_iUnion {T : α → α} {s : ℕ → Set α}
    (hs : ∀ n, InvariantMeasurableSet T (s n)) :
    InvariantMeasurableSet T (⋃ n, s n) := by
  refine ⟨MeasurableSet.iUnion fun n => (hs n).1, ?_⟩
  ext x
  simp only [Set.mem_preimage, Set.mem_iUnion]
  exact exists_congr fun n => Set.ext_iff.mp (hs n).2 x

/--
The exact invariant sigma-algebra of a self-map, represented as a
sub-`MeasurableSpace` of the ambient measurable space.
-/
@[reducible]
def invariantMeasurableSpace (T : α → α) : MeasurableSpace α where
  MeasurableSet' := InvariantMeasurableSet T
  measurableSet_empty := by
    simpa using (InvariantMeasurableSet.compl (invariantMeasurableSet_univ T))
  measurableSet_compl := fun _s hs => hs.compl
  measurableSet_iUnion := fun _s hs => invariantMeasurableSet_iUnion hs

/-- The invariant sigma-algebra is a sub-sigma-algebra of the ambient one. -/
theorem invariantMeasurableSpace_le (T : α → α) :
    invariantMeasurableSpace (α := α) T ≤ ‹MeasurableSpace α› := by
  intro s hs
  exact hs.1

/-- Measurable sets in the invariant sigma-algebra are exactly invariant sets. -/
theorem measurableSet_invariantMeasurableSpace_iff (T : α → α) (s : Set α) :
    MeasurableSet[invariantMeasurableSpace (α := α) T] s ↔
      InvariantMeasurableSet T s :=
  Iff.rfl

/-! ## Conditional expectation onto invariant observables -/

/--
The `L^2` submodule of observables measurable for the chosen exact invariant
sigma-algebra.
-/
abbrev InvariantLpMeasSubspace (T : α → α) : Submodule 𝕜 (L2Space α μ E) :=
  lpMeas E 𝕜 (invariantMeasurableSpace (α := α) T) 2 μ

/--
Conditional expectation onto the exact invariant sigma-algebra.

This definition fixes the representation choice for the public backfill:
use a sub-`MeasurableSpace`, not an abstract set subalgebra, so it plugs
directly into mathlib's `condExpL2` API.
-/
abbrev invariantCondExpL2 (T : α → α) :
    L2Space α μ E →L[𝕜]
      lpMeas E 𝕜 (invariantMeasurableSpace (α := α) T) 2 μ :=
  condExpL2 E 𝕜 (invariantMeasurableSpace_le (α := α) T)

/--
The invariant conditional expectation regarded as an endomorphism of ambient
`L^2`.
-/
abbrev invariantCondExpL2Projection (T : α → α) :
    L2Space α μ E →L[𝕜] L2Space α μ E :=
  (InvariantLpMeasSubspace (𝕜 := 𝕜) (E := E) (μ := μ) T).subtypeL.comp
    (invariantCondExpL2 (𝕜 := 𝕜) (E := E) (μ := μ) T)

/--
The star projection onto the `lpMeas` submodule for the invariant
sigma-algebra.  The local `Fact` supplies the closed-subspace projection
instance required by `lpMeas`.
-/
abbrev invariantLpMeasStarProjection (T : α → α) :
    L2Space α μ E →L[𝕜] L2Space α μ E :=
  haveI : Fact (invariantMeasurableSpace (α := α) T ≤ ‹MeasurableSpace α›) :=
    ⟨invariantMeasurableSpace_le (α := α) T⟩
  (InvariantLpMeasSubspace (𝕜 := 𝕜) (E := E) (μ := μ) T).starProjection

/--
Mathlib's `condExpL2` is definitionally the orthogonal/star projection onto
`lpMeas` for the selected sub-sigma-algebra.

This is the closed repo-local part of `S1-M-246-PUB-06`; it does not identify
that `lpMeas` submodule with the Koopman fixed-vector submodule.
-/
theorem invariantCondExpL2Projection_eq_invariantLpMeas_starProjection
    (T : α → α) :
    invariantCondExpL2Projection (𝕜 := 𝕜) (E := E) (μ := μ) T =
      invariantLpMeasStarProjection (𝕜 := 𝕜) (E := E) (μ := μ) T :=
  rfl

/--
Reduction target for `S1-M-246-PUB-06`.

If a later proof identifies the chosen invariant-measurable `lpMeas` projection
with the fixed-vector projection of the Koopman operator, then the conditional
expectation projection agrees with the fixed-vector projection.
-/
theorem invariantCondExpL2Projection_eq_fixedProjection_of_starProjection_eq
    (T : α → α) (hT : MeasurePreserving T μ μ)
    (hproj :
      invariantLpMeasStarProjection (𝕜 := 𝕜) (E := E) (μ := μ) T =
        (FixedSubspace (KoopmanOperator 𝕜 E T hT)).starProjection) :
    invariantCondExpL2Projection (𝕜 := 𝕜) (E := E) (μ := μ) T =
      (FixedSubspace (KoopmanOperator 𝕜 E T hT)).starProjection :=
  (invariantCondExpL2Projection_eq_invariantLpMeas_starProjection
    (𝕜 := 𝕜) (E := E) (μ := μ) T).trans hproj

/--
Pointwise form of
`invariantCondExpL2Projection_eq_fixedProjection_of_starProjection_eq`.
-/
theorem invariantCondExpL2Projection_apply_eq_fixedProjection_of_starProjection_eq
    (T : α → α) (hT : MeasurePreserving T μ μ)
    (hproj :
      invariantLpMeasStarProjection (𝕜 := 𝕜) (E := E) (μ := μ) T =
        (FixedSubspace (KoopmanOperator 𝕜 E T hT)).starProjection)
    (g : L2Space α μ E) :
    invariantCondExpL2Projection (𝕜 := 𝕜) (E := E) (μ := μ) T g =
      FixedProjection (KoopmanOperator 𝕜 E T hT) g := by
  have hmap :=
    congrArg (fun L : L2Space α μ E →L[𝕜] L2Space α μ E => L g)
      (invariantCondExpL2Projection_eq_fixedProjection_of_starProjection_eq
        (𝕜 := 𝕜) (E := E) (μ := μ) T hT hproj)
  exact hmap

/--
Probability-facing bridge data not closed by this file.

Future work should identify the fixed-vector projection with conditional
expectation onto the invariant sigma-algebra, and, under ergodicity, with the
constant function given by the space average.
-/
structure InvariantProjectionBridge
    (T : α → α) (hT : MeasurePreserving T μ μ) : Type (max u v w) where
  conditionalExpectationProjection :
    L2Space α μ E →L[𝕜] L2Space α μ E
  projection_eq_fixedProjection :
    ∀ g : L2Space α μ E,
      conditionalExpectationProjection g =
        FixedProjection (KoopmanOperator 𝕜 E T hT) g
  representsInvariantSigmaAlgebra : Prop
  ergodicConstantsIdentified : Prop

/-- Boundary statement for the invariant-sigma-algebra interpretation. -/
def InvariantSigmaAlgebraBridgeStatement : Prop :=
  ∀ (T : α → α) (hT : MeasurePreserving T μ μ),
    ∃ _bridge : InvariantProjectionBridge (𝕜 := 𝕜) (E := E) T hT,
      True

/--
Normalized Stage1 statement shape for THM-M-1054.

This theorem-shaped proposition is the checked `L^2` Koopman mean ergodic
statement.  It does not assert the invariant-sigma-algebra bridge above.
-/
def StatementShape : Prop :=
  ∀ (𝕜 : Type u) [RCLike 𝕜]
    (α : Type w) [MeasurableSpace α] (μ : Measure α)
    (E : Type v) [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E],
      ∀ (T : α → α) (hT : MeasurePreserving T μ μ),
        L2KoopmanMeanErgodicConclusion (𝕜 := 𝕜) (E := E) T hT

/-- Checked closure of the normalized `L^2` Koopman statement shape. -/
theorem statementShape_from_mathlib : StatementShape.{u, v, w} := by
  intro 𝕜 _ α _ μ E _ _ _ T hT
  exact l2_koopman_meanErgodic_from_mathlib (𝕜 := 𝕜) (E := E) T hT

end L2Koopman

/-- Mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.MeanErgodic",
  "Mathlib.MeasureTheory.Function.L2Space",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.Dynamics.BirkhoffSum.Average",
  "Mathlib.Dynamics.BirkhoffSum.NormedSpace",
  "Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving",
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.Function",
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.CondexpL2"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
  "LinearMap.tendsto_birkhoffAverage_of_ker_subset_closure",
  "birkhoffAverage",
  "MeasureTheory.Lp.compMeasurePreserving",
  "MeasureTheory.Lp.compMeasurePreservingₗᵢ",
  "MeasureTheory.Lp.compMeasurePreserving_iterate",
  "MeasureTheory.Lp.coeFn_compMeasurePreserving",
  "MeasureTheory.Lp.isometry_compMeasurePreserving",
  "MeasureTheory.L2.innerProductSpace",
  "MeasureTheory.condExpL2",
  "Ergodic",
  "Ergodic.eq_const_of_compMeasurePreserving_eq",
  "MeasureTheory.Lp.const",
  "MeasureTheory.MeasurePreserving"
]

/-- Primary-source anchors audited at the pinned mathlib revision. -/
def primarySourceAnchors : List String := [
  "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/InnerProductSpace/MeanErgodic.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Function/L2Space.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Dynamics/Ergodic/Ergodic.lean"
]

/-! ## Expanded M0387 leaf ledgers for `S1-M-246-PUB-08` -/

/--
One independent `<= 100` step ledger row for the unchecked
`S1-M-246-L014` through `S1-M-246-L024` leaves.

These rows are checked planning metadata.  They do not prove the
probability-facing von Neumann theorem beyond the existing local wrappers.
-/
structure MeanErgodicExpandedLeafLedger where
  leafId : String
  packageId : String
  independentTarget : String
  requiredInputs : String
  downstreamOutput : String
  maxProofSteps : Nat
  status : String
  debtClassification : String

/--
Expanded split for `S1-M-246-L014` through `S1-M-246-L024`.

Each row is intentionally independent and capped at `<= 100` future local proof
steps.  The terminal probability-facing theorem remains open until these
ledger rows are promoted to proof bodies or pinned checked wrappers.
-/
def meanErgodicExpandedLeafLedgers : List MeanErgodicExpandedLeafLedger := [
  { leafId := "S1-M-246-L014",
    packageId := "M1054.P4.invariant-sigma-algebra",
    independentTarget :=
      "Represent the invariant sigma-algebra of a measure-preserving map as a sub-MeasurableSpace.",
    requiredInputs :=
      "MeasurableSpace α, self-map T, exact invariant set predicate, measurable set closure under complement and countable union.",
    downstreamOutput :=
      "A chosen invariantMeasurableSpace T together with invariantMeasurableSpace_le.",
    maxProofSteps := 45,
    status := "checked_statement_boundary_open_formalization_debt",
    debtClassification := "formalization_debt" },
  { leafId := "S1-M-246-L015",
    packageId := "M1054.P4.invariant-sigma-algebra",
    independentTarget :=
      "Compare exact invariant measurable sets with the a.e. invariant set convention used in ergodic theory.",
    requiredInputs :=
      "InvariantMeasurableSet T, MeasurePreserving T μ μ, ae equality and null-set completion APIs.",
    downstreamOutput :=
      "A bridge lemma selecting exact or completed invariant sigma-algebra semantics.",
    maxProofSteps := 90,
    status := "unchecked_requires_api_selection",
    debtClassification := "formalization_debt" },
  { leafId := "S1-M-246-L016",
    packageId := "M1054.P5.fixed-observable-bridge",
    independentTarget :=
      "Identify LinearMap.eqLocus (KoopmanOperator 𝕜 E T hT) 1 with the named invariant L2 observable predicate.",
    requiredInputs :=
      "KoopmanOperator, InvariantL2Observable, FixedSubspace, LinearMap.eqLocus.",
    downstreamOutput :=
      "The checked fixed-subspace membership bridge used by the projection package.",
    maxProofSteps := 25,
    status := "checked_local_wrapper",
    debtClassification := "local_wrapper_upstream_mathlib" },
  { leafId := "S1-M-246-L017",
    packageId := "M1054.P5.fixed-observable-bridge",
    independentTarget :=
      "Convert Koopman fixedness of an L2 class into a.e. equality of a representative with its T-composition.",
    requiredInputs :=
      "Lp.compMeasurePreserving, Lp.coeFn_compMeasurePreserving, AEEqFun.ext.",
    downstreamOutput :=
      "A representative-level invariant observable theorem for later sigma-algebra comparison.",
    maxProofSteps := 55,
    status := "checked_local_wrapper",
    debtClassification := "local_wrapper_upstream_mathlib" },
  { leafId := "S1-M-246-L018",
    packageId := "M1054.P6.conditional-expectation-projection",
    independentTarget :=
      "Package condExpL2 onto invariantMeasurableSpace T as an ambient L2 continuous linear projection.",
    requiredInputs :=
      "condExpL2, lpMeas, invariantMeasurableSpace_le, submodule subtypeL.",
    downstreamOutput :=
      "invariantCondExpL2Projection and its star-projection normal form.",
    maxProofSteps := 60,
    status := "checked_local_wrapper",
    debtClassification := "local_wrapper_upstream_mathlib" },
  { leafId := "S1-M-246-L019",
    packageId := "M1054.P6.conditional-expectation-projection",
    independentTarget :=
      "Prove that invariant-measurable L2 observables are Koopman fixed.",
    requiredInputs :=
      "InvariantLpMeasSubspace, MeasurePreserving T μ μ, representative measurability for invariantMeasurableSpace T.",
    downstreamOutput :=
      "One inclusion from lpMeas invariant observables to the Koopman fixed submodule.",
    maxProofSteps := 100,
    status := "unchecked_projection_bridge_leaf",
    debtClassification := "formalization_debt" },
  { leafId := "S1-M-246-L020",
    packageId := "M1054.P6.conditional-expectation-projection",
    independentTarget :=
      "Prove that Koopman fixed L2 observables are invariant-measurable for the selected invariant sigma-algebra.",
    requiredInputs :=
      "a.e. invariant representative theorem, invariantMeasurableSpace semantics, Lp measurability transport.",
    downstreamOutput :=
      "The reverse inclusion from the Koopman fixed submodule to lpMeas invariant observables.",
    maxProofSteps := 100,
    status := "unchecked_projection_bridge_leaf",
    debtClassification := "formalization_debt" },
  { leafId := "S1-M-246-L021",
    packageId := "M1054.P6.conditional-expectation-projection",
    independentTarget :=
      "Transport the two submodule inclusions into equality of star projections.",
    requiredInputs :=
      "L019, L020, Submodule equality, starProjection extensionality for closed subspaces.",
    downstreamOutput :=
      "invariantLpMeasStarProjection equals the fixed-subspace star projection.",
    maxProofSteps := 85,
    status := "unchecked_projection_bridge_leaf",
    debtClassification := "formalization_debt" },
  { leafId := "S1-M-246-L022",
    packageId := "M1054.P7.ergodic-scalar-specialization",
    independentTarget :=
      "Under Ergodic T μ and probability measure, identify scalar fixed L2 observables with integral constants.",
    requiredInputs :=
      "Ergodic.eq_const_of_compMeasurePreserving_eq, Lp.const, integral_congr_ae.",
    downstreamOutput :=
      "The checked scalar fixed-observable constant identification.",
    maxProofSteps := 70,
    status := "checked_local_wrapper",
    debtClassification := "local_wrapper_upstream_mathlib" },
  { leafId := "S1-M-246-L023",
    packageId := "M1054.P7.ergodic-scalar-specialization",
    independentTarget :=
      "Deduce scalar Cesaro convergence to the integral constant from the fixed-projection identity.",
    requiredInputs :=
      "l2_koopman_meanErgodic_from_mathlib and a proof that FixedProjection g equals Lp.const 2 μ integral.",
    downstreamOutput :=
      "A reduction theorem for the probability-facing scalar mean ergodic statement.",
    maxProofSteps := 35,
    status := "checked_reduction_open_projection_identity",
    debtClassification := "formalization_debt" },
  { leafId := "S1-M-246-L024",
    packageId := "M1054.P8.repo-local-completion-gate",
    independentTarget :=
      "Gate any public completion claim on validation, public merge-back, external-anchor handling, and no completed-state repo_local_integration_debt.",
    requiredInputs :=
      "Local Lean validation, public blueprint/todo/README synchronization, external proof audit result.",
    downstreamOutput :=
      "A public integration checklist that keeps THM-M-1054 open until every M0387 gate passes.",
    maxProofSteps := 40,
    status := "checked_split_only_gate_not_theorem_completion",
    debtClassification := "formalization_debt" }
]

/-- The C008 expansion covers exactly the public leaves `L014` through `L024`. -/
theorem meanErgodicExpandedLeafLedgers_length :
    meanErgodicExpandedLeafLedgers.length = 11 := by
  native_decide

/-- Every C008 expanded leaf carries an explicit M0387 `<= 100` proof-step budget. -/
theorem meanErgodicExpandedLeafLedgers_all_budget_le_100 :
    meanErgodicExpandedLeafLedgers.all
      (fun leaf => decide (leaf.maxProofSteps ≤ 100)) = true := by
  native_decide

/--
Split-only status for `S1-M-246-PUB-08`.

The leaf ledger is checked, but the full probability-facing von Neumann
ergodic theorem is not claimed completed by this metadata.
-/
def meanErgodicExpandedLeafLedgersSplitStatus : String :=
  "split_complete_terminal_probability_facing_theorem_open_formalization_debt"

/-- No completed state in the C008 split retains `repo_local_integration_debt`. -/
def meanErgodicC008RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

theorem meanErgodicC008RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    meanErgodicC008RepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## External Lean 4 audit gate for `S1-M-246-PUB-09` -/

/--
Primary external Lean 4 candidate audited for `S1-M-246-PUB-09`.

This metadata records a source-level audit result only.  It is intentionally not
a completion witness unless the external proof is pinned/imported/checked by
this repository's Lake closure.
-/
structure MeanErgodicExternalLeanAudit where
  project : String
  revision : String
  license : String
  leanToolchain : String
  mathlibRevision : String
  sourceFiles : List String
  strongerTheoremNames : List String
  auditedConclusion : String
  repoLocalIntegrationStatus : String
  concreteBlocker : String

/--
The strongest external Lean 4 candidate found in the C009 audit.

`cameronfreer/exchangeability` contains a shift-specialized conditional
expectation bridge (`proj_eq_condexp`) and a shift-specialized convergence to
conditional expectation (`birkhoffAverage_tendsto_condexp`).  That is stronger
than this file's general fixed-projection wrapper for the path-space shift
case, but it is not currently in this repository's validation closure.
-/
def meanErgodicC009ExternalLeanAudit : MeanErgodicExternalLeanAudit where
  project := "github.com/cameronfreer/exchangeability"
  revision := "e9c9ed5341dd8de7aac6e5575dcf3802830e0125"
  license := "Apache-2.0"
  leanToolchain := "leanprover/lean4:v4.27.0-rc1"
  mathlibRevision := "32d24245c7a12ded17325299fd41d412022cd3fe"
  sourceFiles := [
    "Exchangeability/Ergodic/KoopmanMeanErgodic.lean",
    "Exchangeability/Ergodic/InvariantSigma.lean",
    "Exchangeability/DeFinetti/ViaKoopman/KoopmanCommutation.lean"
  ]
  strongerTheoremNames := [
    "Exchangeability.Ergodic.birkhoffAverage_tendsto_metProjection",
    "Exchangeability.DeFinetti.proj_eq_condexp",
    "Exchangeability.DeFinetti.ViaKoopman.birkhoffAverage_tendsto_condexp"
  ]
  auditedConclusion :=
    "Shift-specialized Lean route from Koopman Birkhoff averages to condexpL2 for the shift-invariant sigma algebra."
  repoLocalIntegrationStatus :=
    "external_upstream_anchor_only_not_completed"
  concreteBlocker :=
    "Toolchain/API blocker: external project pins Lean v4.27.0-rc1 and mathlib 32d24245c7a12ded17325299fd41d412022cd3fe, while this repository pins Lean v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; pin/import/check would require a serialized Lake dependency/toolchain compatibility pass outside this child write scope."

/-- C009 found a stronger external shift-specialized candidate but did not integrate it. -/
def meanErgodicC009StrongerExternalCandidateFound : Bool :=
  true

/-- The external candidate is not a repo-local completion witness in this pass. -/
def meanErgodicC009AnchorOnlyCompletionClaimed : Bool :=
  false

/-- No completed state in the C009 audit retains `repo_local_integration_debt`. -/
def meanErgodicC009RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

theorem meanErgodicC009AnchorOnlyCompletionClaimed_eq_false :
    meanErgodicC009AnchorOnlyCompletionClaimed = false :=
  rfl

theorem meanErgodicC009RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    meanErgodicC009RepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## Audit probes -/

#check HilbertMeanErgodicStatementShape
#check hilbertMeanErgodicStatementShape_from_mathlib
#check KoopmanOperator
#check L2KoopmanMeanErgodicConclusion
#check l2_koopman_meanErgodic_from_mathlib
#check l2_koopman_fixedProjection_checked_at_pinned_mathlib
#check InvariantL2Observable
#check InvariantL2Observables
#check mem_fixedSubspace_iff_invariantL2Observable
#check fixedSubspace_koopman_eq_invariantL2Observables
#check invariantL2Observable_iff_ae_comp_eq
#check scalar_koopman_const
#check invariantScalarL2Observable_ae_eq_integral_const
#check invariantScalarL2Observable_eq_const_integral
#check l2_koopman_ergodic_scalar_meanErgodic_const_of_fixedProjection_eq
#check InvariantMeasurableSet
#check invariantMeasurableSpace
#check invariantMeasurableSpace_le
#check InvariantLpMeasSubspace
#check invariantCondExpL2
#check invariantCondExpL2Projection
#check invariantLpMeasStarProjection
#check invariantCondExpL2Projection_eq_invariantLpMeas_starProjection
#check invariantCondExpL2Projection_eq_fixedProjection_of_starProjection_eq
#check invariantCondExpL2Projection_apply_eq_fixedProjection_of_starProjection_eq
#check InvariantSigmaAlgebraBridgeStatement
#check StatementShape
#check statementShape_from_mathlib
#check MeanErgodicExpandedLeafLedger
#check meanErgodicExpandedLeafLedgers
#check meanErgodicExpandedLeafLedgers_length
#check meanErgodicExpandedLeafLedgers_all_budget_le_100
#check meanErgodicExpandedLeafLedgersSplitStatus
#check meanErgodicC008RepoLocalIntegrationDebtRetainedInCompletedState
#check meanErgodicC008RepoLocalIntegrationDebtRetainedInCompletedState_eq_false
#check MeanErgodicExternalLeanAudit
#check meanErgodicC009ExternalLeanAudit
#check meanErgodicC009StrongerExternalCandidateFound
#check meanErgodicC009AnchorOnlyCompletionClaimed
#check meanErgodicC009RepoLocalIntegrationDebtRetainedInCompletedState
#check meanErgodicC009AnchorOnlyCompletionClaimed_eq_false
#check meanErgodicC009RepoLocalIntegrationDebtRetainedInCompletedState_eq_false
#check ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
#check Lp.compMeasurePreservingₗᵢ
#check Lp.compMeasurePreserving_iterate
#check MeasureTheory.condExpL2
#check Ergodic

end AwesomeTheorems.Stage1.S1_M_246
