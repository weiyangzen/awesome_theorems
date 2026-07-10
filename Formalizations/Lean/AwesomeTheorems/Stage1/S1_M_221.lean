import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.MeasureTheory.Integral.IntegrableOn
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.Kolmogorov

/-!
# S1-M-221 / THM-M-1028: properties of Wiener process

This Stage1 artifact records a conservative Lean 4 statement boundary for the
classical theorem that Brownian/Wiener paths are almost surely continuous and
almost surely nowhere differentiable.

The pinned mathlib snapshot contains useful stochastic-process infrastructure:
Gaussian processes, independent increments, filtrations/adaptedness, and the
Kolmogorov moment condition.  It does not expose a canonical Brownian-motion
structure, Wiener measure on path space, a Kolmogorov-Chentsov continuity
theorem, or a terminal nowhere-differentiability theorem for Brownian paths.
The declarations below therefore freeze the normalized statement shape and add
small checked wrappers around available mathlib anchors.  No terminal Brownian
path theorem is claimed here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal NNReal ProbabilityTheory Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_221

universe u

/-- Real-valued stochastic process indexed by real time. -/
abbrev RealProcess (Ω : Type u) : Type u :=
  ℝ → Ω → ℝ

/--
Canonical nonnegative Brownian time domain as a subtype of real time.

For this Stage1 boundary the canonical process carrier remains `ℝ → Ω → ℝ`;
terminal path properties are restricted to `Set.Ici 0`.  This subtype is the
checked bridge for APIs that want an intrinsically nonnegative time parameter.
-/
abbrev NonnegativeTime : Type :=
  {t : ℝ // 0 ≤ t}

/-- Real-valued stochastic process indexed directly by the nonnegative real subtype. -/
abbrev NonnegativeTimeProcess (Ω : Type u) : Type u :=
  NonnegativeTime → Ω → ℝ

/-- Real-valued stochastic process indexed by mathlib's `ℝ≥0`. -/
abbrev NNRealProcess (Ω : Type u) : Type u :=
  ℝ≥0 → Ω → ℝ

/-- A subtype nonnegative time is a member of the canonical real-time domain `Set.Ici 0`. -/
theorem nonnegativeTime_mem_Ici (t : NonnegativeTime) :
    (t : ℝ) ∈ Ici (0 : ℝ) :=
  t.property

/-- The real coercion of an `ℝ≥0` time is a member of `Set.Ici 0`. -/
theorem nnreal_mem_Ici (t : ℝ≥0) :
    (t : ℝ) ∈ Ici (0 : ℝ) :=
  t.property

/-- Convert mathlib's `ℝ≥0` time type to the chosen nonnegative real subtype. -/
def nnrealToNonnegativeTime (t : ℝ≥0) : NonnegativeTime :=
  ⟨(t : ℝ), nnreal_mem_Ici t⟩

/-- Coercing the `ℝ≥0` bridge back to real time is definitionally the usual coercion. -/
theorem nnrealToNonnegativeTime_coe (t : ℝ≥0) :
    ((nnrealToNonnegativeTime t : NonnegativeTime) : ℝ) = (t : ℝ) :=
  rfl

/-- Restrict a real-time process to the nonnegative real subtype. -/
def restrictToNonnegativeTime {Ω : Type u} (X : RealProcess Ω) :
    NonnegativeTimeProcess Ω :=
  fun t => X (t : ℝ)

/-- Restrict a real-time process to mathlib's `ℝ≥0` time type. -/
def restrictToNNReal {Ω : Type u} (X : RealProcess Ω) :
    NNRealProcess Ω :=
  fun t => X (t : ℝ)

/-- Evaluation of the subtype restriction is just real-time evaluation at the coerced time. -/
theorem restrictToNonnegativeTime_apply {Ω : Type u} (X : RealProcess Ω)
    (t : NonnegativeTime) (ω : Ω) :
    restrictToNonnegativeTime X t ω = X (t : ℝ) ω :=
  rfl

/-- Evaluation of the `ℝ≥0` restriction is just real-time evaluation at the coerced time. -/
theorem restrictToNNReal_apply {Ω : Type u} (X : RealProcess Ω) (t : ℝ≥0)
    (ω : Ω) :
    restrictToNNReal X t ω = X (t : ℝ) ω :=
  rfl

/--
The two nonnegative-time views agree after the explicit `ℝ≥0`-to-subtype
coercion bridge.
-/
theorem restrictToNonnegativeTime_nnrealToNonnegativeTime
    {Ω : Type u} (X : RealProcess Ω) (t : ℝ≥0) :
    restrictToNonnegativeTime X (nnrealToNonnegativeTime t) =
      restrictToNNReal X t :=
  rfl

/-- Adjacent increment vector along a finite real-time grid. -/
def brownianIncrementVector {Ω : Type u} (X : RealProcess Ω) {n : ℕ}
    (t : Fin (n + 1) → ℝ) : Ω → Fin n → ℝ :=
  fun ω i => X (t i.succ) ω - X (t i.castSucc) ω

/-- Ordered finite grid condition for Brownian increment packages. -/
def NondecreasingGrid {n : ℕ} (t : Fin (n + 1) → ℝ) : Prop :=
  ∀ i : Fin n, t i.castSucc ≤ t i.succ

/--
Brownian covariance matrix for adjacent increments on an ordered grid.

For a grid `t₀ ≤ t₁ ≤ ... ≤ tₙ`, the intended covariance of
`B_{t_{i+1}} - B_{t_i}` and `B_{t_{j+1}} - B_{t_j}` is the interval length
on the diagonal and zero off the diagonal.
-/
def brownianIncrementCovariance {n : ℕ} (t : Fin (n + 1) → ℝ)
    (i j : Fin n) : ℝ :=
  if i = j then t i.succ - t i.castSucc else 0

/--
Concrete finite-dimensional Brownian-increment law package.

This replaces the former opaque `stationaryGaussianIncrements : Prop` boundary:
for every ordered finite grid, the adjacent increment vector is Gaussian, has
zero coordinate means, and has the diagonal covariance matrix determined by
increment lengths.  Because Gaussian laws are determined by mean and covariance,
this is the repo-local statement shape needed for stationary independent
Brownian increments without naming a non-existent Brownian-motion structure.
-/
structure BrownianIncrementFiniteDimensionalLaw {Ω : Type u} [MeasurableSpace Ω]
    (X : RealProcess Ω) (P : Measure Ω) : Prop where
  hasGaussianLaw_increments :
    ∀ {n : ℕ} (t : Fin (n + 1) → ℝ),
      NondecreasingGrid t →
        HasGaussianLaw (brownianIncrementVector X t) P
  mean_zero :
    ∀ {n : ℕ} (t : Fin (n + 1) → ℝ) (_ht : NondecreasingGrid t) (i : Fin n),
      P[fun ω => brownianIncrementVector X t ω i] = 0
  covariance_eq :
    ∀ {n : ℕ} (t : Fin (n + 1) → ℝ) (_ht : NondecreasingGrid t) (i j : Fin n),
      cov[fun ω => brownianIncrementVector X t ω i,
          fun ω => brownianIncrementVector X t ω j; P] =
        brownianIncrementCovariance t i j

/--
Quantitative increment-moment package in the exact shape expected by mathlib's
Kolmogorov-process constructor.

For Brownian motion the classical fourth-moment estimate supplies the special
case `p = 4`, `q = 2`, and some finite constant `M`.
-/
structure KolmogorovIncrementMomentEstimate {Ω : Type u} [MeasurableSpace Ω]
    (X : RealProcess Ω) (P : Measure Ω) (p q : ℝ) (M : ℝ≥0) : Prop where
  measurable : ∀ t : ℝ, Measurable (X t)
  increment_moment_bound :
    ∀ s t : ℝ, ∫⁻ ω, edist (X s ω) (X t ω) ^ p ∂P ≤ M * edist s t ^ q
  p_pos : 0 < p
  q_pos : 0 < q

/--
Brownian fourth-moment estimate normalized for the Kolmogorov condition.

The missing Brownian-specific work is to derive this estimate from a canonical
Brownian law/covariance object.  Once the estimate is available, the checked
bridge below converts it to `IsAEKolmogorovProcess`.
-/
abbrev BrownianFourthMomentKolmogorovEstimate {Ω : Type u} [MeasurableSpace Ω]
    (X : RealProcess Ω) (P : Measure Ω) (M : ℝ≥0) : Prop :=
  KolmogorovIncrementMomentEstimate X P (4 : ℝ) (2 : ℝ) M

/--
Continuity conclusion package for a future Kolmogorov-Chentsov theorem.

Pinned mathlib currently provides `IsKolmogorovProcess` and
`IsAEKolmogorovProcess`; this package records the missing terminal continuity
output without claiming the theorem.
-/
structure KolmogorovChentsovContinuityConclusion {Ω : Type u} [MeasurableSpace Ω]
    (X : RealProcess Ω) (P : Measure Ω) (timeDomain : Set ℝ) : Type u where
  modification : RealProcess Ω
  ae_eq_modification :
    ∀ t : ℝ, X t =ᵐ[P] modification t
  continuous_paths :
    ∀ᵐ ω ∂P, ContinuousOn (fun t => modification t ω) timeDomain

/--
Statement shape for the missing Kolmogorov-Chentsov continuity theorem in the
current real-process boundary.
-/
def KolmogorovChentsovStatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (X : RealProcess Ω) (P : Measure Ω)
    (timeDomain : Set ℝ) (p q : ℝ) (M : ℝ≥0),
    IsAEKolmogorovProcess X P p q M →
      Nonempty (KolmogorovChentsovContinuityConclusion X P timeDomain)

/--
Pathwise nowhere differentiability on a prescribed time domain.

For Brownian motion the intended domain is `[0, ∞)`, encoded in data by
`timeDomain_eq_nonnegative`.  The predicate is stated with
`DifferentiableWithinAt` so that endpoint behavior is meaningful without
changing the time index away from `ℝ`.
-/
def NowhereDifferentiableOnDomain (timeDomain : Set ℝ) (f : ℝ → ℝ) : Prop :=
  ∀ t ∈ timeDomain, ¬ DifferentiableWithinAt ℝ f timeDomain t

/--
Pathwise nowhere differentiability on the canonical Brownian time domain
`[0, ∞)`, represented as `Set.Ici 0` inside the real-time process boundary.
-/
def NowhereDifferentiableOnNonnegative (f : ℝ → ℝ) : Prop :=
  NowhereDifferentiableOnDomain (Ici (0 : ℝ)) f

/--
Unfolding lemma for the explicit nonnegative-time nowhere-differentiability
criterion requested by the Brownian/Wiener path branch.
-/
theorem nowhereDifferentiableOnNonnegative_iff (f : ℝ → ℝ) :
    NowhereDifferentiableOnNonnegative f ↔
      ∀ t ∈ Ici (0 : ℝ), ¬ DifferentiableWithinAt ℝ f (Ici (0 : ℝ)) t :=
  Iff.rfl

/--
Normalized input package for a future formal Brownian/Wiener-path theorem.

The field `stationaryGaussianIncrements` is a concrete finite-dimensional
Gaussian-law and covariance package for adjacent Brownian increments on ordered
finite grids.  `varianceNormalization` remains a proposition field because the
current repo-local dependency closure has no canonical Brownian-motion
structure tying process-level covariance to `min s t`.  The process-level
Gaussian, independent-increments, filtration, and Kolmogorov-condition
interfaces are concrete mathlib objects.
-/
structure WienerProcessData (Ω : Type u) [MeasurableSpace Ω] : Type u where
  process : RealProcess Ω
  probabilityMeasure : Measure Ω
  timeDomain : Set ℝ
  timeDomain_eq_nonnegative : timeDomain = Ici (0 : ℝ)
  zeroAtOrigin : ∀ᵐ ω ∂probabilityMeasure, process 0 ω = 0
  gaussianProcess : IsGaussianProcess process probabilityMeasure
  indepIncrements : HasIndepIncrements process probabilityMeasure
  filtration : Filtration ℝ ‹MeasurableSpace Ω›
  adapted : Adapted filtration process
  kolmogorovContinuityMoment :
    ∃ (p q : ℝ) (M : ℝ≥0),
      IsAEKolmogorovProcess process probabilityMeasure p q M
  stationaryGaussianIncrements :
    BrownianIncrementFiniteDimensionalLaw process probabilityMeasure
  varianceNormalization : Prop

/-- Explicit hypothesis side for the normalized Wiener-path statement. -/
def WienerPathHypotheses {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) : Prop :=
  BrownianIncrementFiniteDimensionalLaw D.process D.probabilityMeasure ∧
    D.varianceNormalization

/--
Conclusion package expected from the terminal Brownian/Wiener path theorem.

The modification, almost-everywhere equality, path continuity, and
nowhere-differentiability conclusions are all stated with concrete mathlib
predicates.  A future proof must replace the current Stage1 statement boundary
with a genuine construction or import of this package.
-/
structure WienerPathConclusion {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) : Type u where
  modification : RealProcess Ω
  ae_eq_modification :
    ∀ t : ℝ, D.process t =ᵐ[D.probabilityMeasure] modification t
  continuous_paths :
    ∀ᵐ ω ∂D.probabilityMeasure,
      ContinuousOn (fun t => modification t ω) D.timeDomain
  nowhere_differentiable_paths :
    ∀ᵐ ω ∂D.probabilityMeasure,
      NowhereDifferentiableOnDomain D.timeDomain (fun t => modification t ω)

/--
Stage1 normalized statement shape for THM-M-1028.

Every real-valued process satisfying the Brownian/Wiener object model should
have a modification whose paths are continuous and nowhere differentiable on
the nonnegative real time domain.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (D : WienerProcessData Ω),
    WienerPathHypotheses D → Nonempty (WienerPathConclusion D)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω] (D : WienerProcessData Ω),
      WienerPathHypotheses D → Nonempty (WienerPathConclusion D)) :
    StatementShape.{u} :=
  h

/-- Checked wrapper exposing the stored Gaussian-process field. -/
theorem wiener_isGaussianProcess {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    IsGaussianProcess D.process D.probabilityMeasure :=
  D.gaussianProcess

/-- Checked wrapper exposing the stored independent-increments field. -/
theorem wiener_hasIndepIncrements {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    HasIndepIncrements D.process D.probabilityMeasure :=
  D.indepIncrements

/-- Checked wrapper exposing the a.e. zero initial condition. -/
theorem wiener_zeroAtOrigin {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    ∀ᵐ ω ∂D.probabilityMeasure, D.process 0 ω = 0 :=
  D.zeroAtOrigin

/-- Checked wrapper exposing the canonical real-time domain choice. -/
theorem wiener_timeDomain_eq_nonnegative {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    D.timeDomain = Ici (0 : ℝ) :=
  D.timeDomain_eq_nonnegative

/-- A nonnegative real time belongs to the stored Wiener time domain. -/
theorem wiener_mem_timeDomain_of_nonneg {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {t : ℝ} (ht : 0 ≤ t) :
    t ∈ D.timeDomain := by
  rw [D.timeDomain_eq_nonnegative]
  exact ht

/-- A subtype nonnegative time belongs to the stored Wiener time domain. -/
theorem wiener_nonnegativeTime_mem_timeDomain {Ω : Type u}
    [MeasurableSpace Ω] (D : WienerProcessData Ω) (t : NonnegativeTime) :
    (t : ℝ) ∈ D.timeDomain :=
  wiener_mem_timeDomain_of_nonneg D t.property

/-- An `ℝ≥0` time belongs to the stored Wiener time domain after coercion to `ℝ`. -/
theorem wiener_nnreal_mem_timeDomain {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) (t : ℝ≥0) :
    (t : ℝ) ∈ D.timeDomain :=
  wiener_mem_timeDomain_of_nonneg D t.property

/-- The subtype-time view of a Wiener process is the canonical restriction of its real process. -/
theorem wiener_restrictToNonnegativeTime_eq {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    restrictToNonnegativeTime D.process = fun t : NonnegativeTime => D.process (t : ℝ) :=
  rfl

/-- The `ℝ≥0`-time view of a Wiener process is the canonical restriction of its real process. -/
theorem wiener_restrictToNNReal_eq {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    restrictToNNReal D.process = fun t : ℝ≥0 => D.process (t : ℝ) :=
  rfl

/-- Checked wrapper exposing the adaptedness field. -/
theorem wiener_adapted {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    Adapted D.filtration D.process :=
  D.adapted

/-- Checked wrapper exposing the Kolmogorov-moment data used for continuity. -/
theorem wiener_has_aeKolmogorovProcess {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    ∃ (p q : ℝ) (M : ℝ≥0),
      IsAEKolmogorovProcess D.process D.probabilityMeasure p q M :=
  D.kolmogorovContinuityMoment

/--
Checked bridge from the repo-local increment-moment package to mathlib's exact
Kolmogorov-process predicate.
-/
theorem kolmogorovIncrementMomentEstimate_isKolmogorovProcess
    {Ω : Type u} [MeasurableSpace Ω] {X : RealProcess Ω} {P : Measure Ω}
    {p q : ℝ} {M : ℝ≥0}
    (h : KolmogorovIncrementMomentEstimate X P p q M) :
    IsKolmogorovProcess X P p q M :=
  IsKolmogorovProcess.mk_of_secondCountableTopology
    h.measurable h.increment_moment_bound h.p_pos h.q_pos

/--
Checked bridge from the repo-local increment-moment package to the a.e.
Kolmogorov-process predicate used in `WienerProcessData`.
-/
theorem kolmogorovIncrementMomentEstimate_isAEKolmogorovProcess
    {Ω : Type u} [MeasurableSpace Ω] {X : RealProcess Ω} {P : Measure Ω}
    {p q : ℝ} {M : ℝ≥0}
    (h : KolmogorovIncrementMomentEstimate X P p q M) :
    IsAEKolmogorovProcess X P p q M :=
  (kolmogorovIncrementMomentEstimate_isKolmogorovProcess h).IsAEKolmogorovProcess

/--
Checked Brownian fourth-moment bridge: once the Brownian fourth-moment estimate
is proved or imported, it supplies the `IsAEKolmogorovProcess` field with
exponents `4` and `2`.
-/
theorem brownianFourthMomentEstimate_isAEKolmogorovProcess
    {Ω : Type u} [MeasurableSpace Ω] {X : RealProcess Ω} {P : Measure Ω}
    {M : ℝ≥0}
    (h : BrownianFourthMomentKolmogorovEstimate X P M) :
    IsAEKolmogorovProcess X P (4 : ℝ) (2 : ℝ) M :=
  kolmogorovIncrementMomentEstimate_isAEKolmogorovProcess h

/-- Checked wrapper exposing the concrete Brownian finite-dimensional increment-law field. -/
theorem wiener_brownianIncrementFiniteDimensionalLaw {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) :
    BrownianIncrementFiniteDimensionalLaw D.process D.probabilityMeasure :=
  D.stationaryGaussianIncrements

/-- Checked Gaussian-process anchor: every coordinate is a.e. measurable. -/
theorem gaussianCoordinate_aemeasurable {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) (t : ℝ) :
    AEMeasurable (D.process t) D.probabilityMeasure :=
  D.gaussianProcess.aemeasurable t

/-- Checked Gaussian-process anchor: every coordinate has a Gaussian law. -/
theorem gaussianCoordinate_hasGaussianLaw {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) (t : ℝ) :
    HasGaussianLaw (D.process t) D.probabilityMeasure :=
  D.gaussianProcess.hasGaussianLaw_eval t

/-- Checked Gaussian-process anchor: increments of a Gaussian process are Gaussian. -/
theorem gaussianIncrement_hasGaussianLaw {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) (s t : ℝ) :
    HasGaussianLaw (fun ω => D.process t ω - D.process s ω) D.probabilityMeasure :=
  D.gaussianProcess.hasGaussianLaw_fun_sub (s := t) (t := s)

/-- Checked Gaussian-process anchor: every finite adjacent increment vector is Gaussian. -/
theorem gaussianIncrementVector_hasGaussianLaw {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {n : ℕ} (t : Fin (n + 1) → ℝ) :
    HasGaussianLaw (brownianIncrementVector D.process t) D.probabilityMeasure :=
  D.gaussianProcess.hasGaussianLaw_increments (t := t)

/--
The Brownian-increment package specializes the finite-dimensional Gaussian law
to ordered grids and pairs it with zero means and Brownian covariance.
-/
theorem brownianIncrementVector_hasGaussianLaw {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {n : ℕ} (t : Fin (n + 1) → ℝ)
    (ht : NondecreasingGrid t) :
    HasGaussianLaw (brownianIncrementVector D.process t) D.probabilityMeasure :=
  D.stationaryGaussianIncrements.hasGaussianLaw_increments t ht

/-- The concrete Brownian-increment package exposes zero coordinate means. -/
theorem brownianIncrement_mean_zero {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {n : ℕ} (t : Fin (n + 1) → ℝ)
    (ht : NondecreasingGrid t) (i : Fin n) :
    D.probabilityMeasure[fun ω => brownianIncrementVector D.process t ω i] = 0 :=
  D.stationaryGaussianIncrements.mean_zero t ht i

/-- The concrete Brownian-increment package exposes the Brownian covariance matrix. -/
theorem brownianIncrement_covariance_eq {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {n : ℕ} (t : Fin (n + 1) → ℝ)
    (ht : NondecreasingGrid t) (i j : Fin n) :
    cov[fun ω => brownianIncrementVector D.process t ω i,
        fun ω => brownianIncrementVector D.process t ω j; D.probabilityMeasure] =
      brownianIncrementCovariance t i j :=
  D.stationaryGaussianIncrements.covariance_eq t ht i j

/-- Checked Gaussian-law anchor: every Gaussian coordinate has finite second moment. -/
theorem gaussianCoordinate_memLp_two {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) (t : ℝ) :
    MemLp (D.process t) 2 D.probabilityMeasure :=
  (D.gaussianProcess.hasGaussianLaw_eval t).memLp_two

/-- Checked Gaussian-law anchor: every Gaussian increment has finite second moment. -/
theorem gaussianIncrement_memLp_two {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) (s t : ℝ) :
    MemLp (fun ω => D.process t ω - D.process s ω) 2 D.probabilityMeasure :=
  (gaussianIncrement_hasGaussianLaw D s t).memLp_two

/-- Checked independent-increments anchor for two adjacent increments. -/
theorem indepIncrements_sub_sub {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {r s t : ℝ} (hrs : r ≤ s) (hst : s ≤ t) :
    (D.process s - D.process r) ⟂ᵢ[D.probabilityMeasure]
      (D.process t - D.process s) :=
  D.indepIncrements.indepFun_sub_sub hrs hst

/-- Checked independent-increments anchor using the a.e. zero initial condition. -/
theorem indepIncrements_eval_sub_from_zero {Ω : Type u} [MeasurableSpace Ω]
    (D : WienerProcessData Ω) {s t : ℝ} (h0s : 0 ≤ s) (hst : s ≤ t) :
    D.process s ⟂ᵢ[D.probabilityMeasure] (D.process t - D.process s) :=
  D.indepIncrements.indepFun_eval_sub h0s hst D.zeroAtOrigin

/-- Checked Kolmogorov-process anchor: an exact Kolmogorov process has measurable coordinates. -/
theorem kolmogorovProcess_measurable_at {Ω : Type u} [MeasurableSpace Ω]
    {X : RealProcess Ω} {P : Measure Ω} {p q : ℝ} {M : ℝ≥0}
    (hX : IsKolmogorovProcess X P p q M) (t : ℝ) :
    Measurable (X t) :=
  hX.measurable t

/--
Checked Kolmogorov-process anchor: an a.e. Kolmogorov process has a.e.
measurable coordinates.
-/
theorem aeKolmogorovProcess_aemeasurable_at {Ω : Type u} [MeasurableSpace Ω]
    {X : RealProcess Ω} {P : Measure Ω} {p q : ℝ} {M : ℝ≥0}
    (hX : IsAEKolmogorovProcess X P p q M) (t : ℝ) :
    AEMeasurable (X t) P :=
  hX.aemeasurable t

/-- Checked Kolmogorov-process anchor: the a.e. wrapper preserves the moment inequality. -/
theorem aeKolmogorovProcess_kolmogorovCondition {Ω : Type u} [MeasurableSpace Ω]
    {X : RealProcess Ω} {P : Measure Ω} {p q : ℝ} {M : ℝ≥0}
    (hX : IsAEKolmogorovProcess X P p q M) (s t : ℝ) :
    ∫⁻ ω, edist (X s ω) (X t ω) ^ p ∂P ≤ M * edist s t ^ q :=
  hX.kolmogorovCondition s t

/-- The Kolmogorov-Chentsov conclusion exposes the chosen continuous modification. -/
theorem kolmogorovChentsovConclusion_continuous_paths
    {Ω : Type u} [MeasurableSpace Ω] {X : RealProcess Ω} {P : Measure Ω}
    {timeDomain : Set ℝ}
    (C : KolmogorovChentsovContinuityConclusion X P timeDomain) :
    ∀ᵐ ω ∂P, ContinuousOn (fun t => C.modification t ω) timeDomain :=
  C.continuous_paths

/-- The Kolmogorov-Chentsov conclusion exposes coordinatewise a.e. equality. -/
theorem kolmogorovChentsovConclusion_ae_eq_modification
    {Ω : Type u} [MeasurableSpace Ω] {X : RealProcess Ω} {P : Measure Ω}
    {timeDomain : Set ℝ}
    (C : KolmogorovChentsovContinuityConclusion X P timeDomain) (t : ℝ) :
    X t =ᵐ[P] C.modification t :=
  C.ae_eq_modification t

/-- The conclusion exposes path continuity of the chosen modification. -/
theorem conclusion_continuous_paths {Ω : Type u} [MeasurableSpace Ω]
    {D : WienerProcessData Ω} (C : WienerPathConclusion D) :
    ∀ᵐ ω ∂D.probabilityMeasure,
      ContinuousOn (fun t => C.modification t ω) D.timeDomain :=
  C.continuous_paths

/-- The conclusion exposes pathwise nowhere differentiability of the chosen modification. -/
theorem conclusion_nowhere_differentiable_paths {Ω : Type u} [MeasurableSpace Ω]
    {D : WienerProcessData Ω} (C : WienerPathConclusion D) :
    ∀ᵐ ω ∂D.probabilityMeasure,
      NowhereDifferentiableOnDomain D.timeDomain (fun t => C.modification t ω) :=
  C.nowhere_differentiable_paths

/-- The conclusion specializes nowhere differentiability to `Set.Ici 0`. -/
theorem conclusion_nowhere_differentiable_on_nonnegative
    {Ω : Type u} [MeasurableSpace Ω]
    {D : WienerProcessData Ω} (C : WienerPathConclusion D) :
    ∀ᵐ ω ∂D.probabilityMeasure,
      NowhereDifferentiableOnNonnegative (fun t => C.modification t ω) :=
  C.nowhere_differentiable_paths.mono fun ω hω => by
    change NowhereDifferentiableOnDomain (Ici (0 : ℝ)) (fun t => C.modification t ω)
    rw [← D.timeDomain_eq_nonnegative]
    exact hω

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic",
  "Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence",
  "Mathlib.Probability.Independence.Process.Basic",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.HittingTime",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.MeasureTheory.Constructions.Projective",
  "Mathlib.MeasureTheory.Constructions.Cylinders"
]

/-- Nearby mathlib names audited for the Brownian/Wiener statement boundary. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.IsGaussianProcess",
  "ProbabilityTheory.IsGaussianProcess.aemeasurable",
  "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval",
  "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_fun_sub",
  "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_increments",
  "AwesomeTheorems.Stage1.S1_M_221.BrownianIncrementFiniteDimensionalLaw",
  "AwesomeTheorems.Stage1.S1_M_221.brownianIncrementVector",
  "AwesomeTheorems.Stage1.S1_M_221.brownianIncrementCovariance",
  "ProbabilityTheory.HasGaussianLaw.memLp_two",
  "ProbabilityTheory.covariance",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.HasIndepIncrements.indepFun_sub_sub",
  "ProbabilityTheory.HasIndepIncrements.indepFun_eval_sub",
  "ProbabilityTheory.IsKolmogorovProcess",
  "ProbabilityTheory.IsAEKolmogorovProcess",
  "ProbabilityTheory.IsKolmogorovProcess.mk_of_secondCountableTopology",
  "ProbabilityTheory.IsKolmogorovProcess.IsAEKolmogorovProcess",
  "ProbabilityTheory.IsAEKolmogorovProcess.kolmogorovCondition",
  "ProbabilityTheory.IsKolmogorovProcess.measurable",
  "ProbabilityTheory.IsAEKolmogorovProcess.aemeasurable",
  "AwesomeTheorems.Stage1.S1_M_221.NonnegativeTime",
  "AwesomeTheorems.Stage1.S1_M_221.NonnegativeTimeProcess",
  "AwesomeTheorems.Stage1.S1_M_221.NNRealProcess",
  "AwesomeTheorems.Stage1.S1_M_221.nonnegativeTime_mem_Ici",
  "AwesomeTheorems.Stage1.S1_M_221.nnreal_mem_Ici",
  "AwesomeTheorems.Stage1.S1_M_221.nnrealToNonnegativeTime",
  "AwesomeTheorems.Stage1.S1_M_221.restrictToNonnegativeTime",
  "AwesomeTheorems.Stage1.S1_M_221.restrictToNNReal",
  "AwesomeTheorems.Stage1.S1_M_221.wiener_timeDomain_eq_nonnegative",
  "AwesomeTheorems.Stage1.S1_M_221.wiener_nonnegativeTime_mem_timeDomain",
  "AwesomeTheorems.Stage1.S1_M_221.wiener_nnreal_mem_timeDomain",
  "AwesomeTheorems.Stage1.S1_M_221.KolmogorovIncrementMomentEstimate",
  "AwesomeTheorems.Stage1.S1_M_221.BrownianFourthMomentKolmogorovEstimate",
  "AwesomeTheorems.Stage1.S1_M_221.KolmogorovChentsovContinuityConclusion",
  "AwesomeTheorems.Stage1.S1_M_221.KolmogorovChentsovStatementShape",
  "AwesomeTheorems.Stage1.S1_M_221.brownianFourthMomentEstimate_isAEKolmogorovProcess",
  "AwesomeTheorems.Stage1.S1_M_221.NowhereDifferentiableOnNonnegative",
  "AwesomeTheorems.Stage1.S1_M_221.nowhereDifferentiableOnNonnegative_iff",
  "AwesomeTheorems.Stage1.S1_M_221.conclusion_nowhere_differentiable_on_nonnegative",
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "ContinuousOn",
  "DifferentiableWithinAt"
]

/-- Search terms that did not locate a terminal Brownian-path theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Brownian",
  "brownian",
  "Wiener",
  "wiener",
  "BrownianMotion",
  "IsBrownianMotion",
  "WienerMeasure",
  "continuous modification",
  "Kolmogorov-Chentsov",
  "nowhere differentiable",
  "nondifferentiable"
]

/-!
The C002 Brownian/Wiener object audit searched the pinned local mathlib
`Probability`, `MeasureTheory`, and `Analysis` trees for the names below.  No
canonical Brownian-motion or Wiener-measure object was present there; the usable
repo-local closure is therefore the checked Gaussian-process, independent
increments, Kolmogorov-process, filtration, and path regularity boundary above.
-/

/-- C002 search terms used for the canonical Brownian/Wiener object audit. -/
def absentBrownianWienerObjectSearchTerms : List String := [
  "Brownian",
  "brownian",
  "BrownianMotion",
  "IsBrownianMotion",
  "IsBrownian",
  "IsPreBrownian",
  "standard Brownian motion",
  "Wiener",
  "wiener",
  "WienerProcess",
  "WienerMeasure",
  "wienerMeasure"
]

/--
C002 audit conclusion for the pinned mathlib snapshot.

This is checked metadata, not a proof of absence inside Lean: the repository
grep audit found no canonical Brownian/Wiener object in local mathlib, so there
are no mathlib Brownian/Wiener theorem names to pin/import/check for this slot.
-/
def mathlibBrownianWienerObjectAuditConclusion : String :=
  "No canonical BrownianMotion/IsBrownian/WienerMeasure object was found in the \
  pinned local mathlib Probability, MeasureTheory, or Analysis trees."

/-!
The C006 public-backfill child is serial integration work: it should merge the
checked wrapper list and unchecked terminal leaf ledger into the authoritative
Stage1 public surface after integrator review.  The two lists below keep that
merge payload in this locally checked artifact without editing public planning
documents from a parallel worker.
-/

/-- Checked wrapper names ready for later public-surface merge-back. -/
def publicSurfaceCheckedWrapperNames : List String := [
  "StatementShape.intro",
  "wiener_isGaussianProcess",
  "wiener_hasIndepIncrements",
  "wiener_zeroAtOrigin",
  "wiener_timeDomain_eq_nonnegative",
  "wiener_mem_timeDomain_of_nonneg",
  "wiener_nonnegativeTime_mem_timeDomain",
  "wiener_nnreal_mem_timeDomain",
  "wiener_restrictToNonnegativeTime_eq",
  "wiener_restrictToNNReal_eq",
  "wiener_adapted",
  "wiener_has_aeKolmogorovProcess",
  "kolmogorovIncrementMomentEstimate_isKolmogorovProcess",
  "kolmogorovIncrementMomentEstimate_isAEKolmogorovProcess",
  "brownianFourthMomentEstimate_isAEKolmogorovProcess",
  "wiener_brownianIncrementFiniteDimensionalLaw",
  "gaussianCoordinate_aemeasurable",
  "gaussianCoordinate_hasGaussianLaw",
  "gaussianIncrement_hasGaussianLaw",
  "gaussianIncrementVector_hasGaussianLaw",
  "brownianIncrementVector_hasGaussianLaw",
  "brownianIncrement_mean_zero",
  "brownianIncrement_covariance_eq",
  "gaussianCoordinate_memLp_two",
  "gaussianIncrement_memLp_two",
  "indepIncrements_sub_sub",
  "indepIncrements_eval_sub_from_zero",
  "kolmogorovProcess_measurable_at",
  "aeKolmogorovProcess_aemeasurable_at",
  "aeKolmogorovProcess_kolmogorovCondition",
  "kolmogorovChentsovConclusion_continuous_paths",
  "kolmogorovChentsovConclusion_ae_eq_modification",
  "conclusion_continuous_paths",
  "conclusion_nowhere_differentiable_paths",
  "conclusion_nowhere_differentiable_on_nonnegative"
]

/-- Unchecked terminal leaves that must remain open on the public surface. -/
def publicSurfaceUncheckedTerminalLeaves : List String := [
  "Construct canonical Brownian/Wiener object or import one.",
  "Formalize variance/covariance normalization for Brownian increments, not only a Prop field.",
  "Prove or import Kolmogorov-Chentsov continuity theorem in the needed form.",
  "Instantiate Brownian moments into IsAEKolmogorovProcess.",
  "Construct a continuous modification satisfying coordinatewise a.e. equality.",
  "Formalize Brownian path oscillation estimates or equivalent nowhere-differentiability criterion.",
  "Prove a.e. nowhere differentiability on [0, infinity) using DifferentiableWithinAt.",
  "Keep public completion open until checked wrappers, unchecked leaves, local validation, and no repo_local_integration_debt gate are synchronized."
]

/-! ## Audit probes -/

#check IsGaussianProcess
#check IsGaussianProcess.hasGaussianLaw_eval
#check IsGaussianProcess.hasGaussianLaw_fun_sub
#check IsGaussianProcess.hasGaussianLaw_increments
#check BrownianIncrementFiniteDimensionalLaw
#check brownianIncrementVector
#check brownianIncrementCovariance
#check covariance
#check HasGaussianLaw.memLp_two
#check HasIndepIncrements
#check HasIndepIncrements.indepFun_sub_sub
#check HasIndepIncrements.indepFun_eval_sub
#check IsKolmogorovProcess
#check IsAEKolmogorovProcess
#check IsKolmogorovProcess.mk_of_secondCountableTopology
#check IsKolmogorovProcess.IsAEKolmogorovProcess
#check IsAEKolmogorovProcess.kolmogorovCondition
#check IsKolmogorovProcess.measurable
#check IsAEKolmogorovProcess.aemeasurable
#check NonnegativeTime
#check NonnegativeTimeProcess
#check NNRealProcess
#check nonnegativeTime_mem_Ici
#check nnreal_mem_Ici
#check nnrealToNonnegativeTime
#check nnrealToNonnegativeTime_coe
#check restrictToNonnegativeTime
#check restrictToNNReal
#check restrictToNonnegativeTime_apply
#check restrictToNNReal_apply
#check restrictToNonnegativeTime_nnrealToNonnegativeTime
#check wiener_timeDomain_eq_nonnegative
#check wiener_mem_timeDomain_of_nonneg
#check wiener_nonnegativeTime_mem_timeDomain
#check wiener_nnreal_mem_timeDomain
#check wiener_restrictToNonnegativeTime_eq
#check wiener_restrictToNNReal_eq
#check KolmogorovIncrementMomentEstimate
#check BrownianFourthMomentKolmogorovEstimate
#check KolmogorovChentsovContinuityConclusion
#check KolmogorovChentsovStatementShape
#check kolmogorovIncrementMomentEstimate_isKolmogorovProcess
#check kolmogorovIncrementMomentEstimate_isAEKolmogorovProcess
#check brownianFourthMomentEstimate_isAEKolmogorovProcess
#check aeKolmogorovProcess_kolmogorovCondition
#check kolmogorovChentsovConclusion_continuous_paths
#check kolmogorovChentsovConclusion_ae_eq_modification
#check NowhereDifferentiableOnNonnegative
#check nowhereDifferentiableOnNonnegative_iff
#check conclusion_nowhere_differentiable_on_nonnegative
#check Filtration
#check Adapted
#check ContinuousOn
#check DifferentiableWithinAt
#check StatementShape
#check absentBrownianWienerObjectSearchTerms
#check mathlibBrownianWienerObjectAuditConclusion
#check publicSurfaceCheckedWrapperNames
#check publicSurfaceUncheckedTerminalLeaves

end S1_M_221
end Stage1
end AwesomeTheorems
