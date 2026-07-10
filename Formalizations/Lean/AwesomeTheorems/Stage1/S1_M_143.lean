import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.Distribution.TemperedDistribution

/-!
# S1-M-143 / THM-M-1153: Wiener criterion

This Stage1 artifact records a conservative Lean statement-shape boundary for
Wiener's criterion for regular boundary points of the Dirichlet problem.

The pinned mathlib snapshot has concrete substrates for harmonic functions,
Laplacians, tempered distributions, and topological boundary/frontier notions.
The audit did not locate a terminal Newtonian capacity object, Perron solution
model, weak-to-classical PDE regularity theorem, or Wiener-criterion theorem.
The declarations below therefore expose a small variational-capacity interface
with monotonicity, compact approximation, and scaling obligations, a
Dirichlet/Perron regularity interface connected to harmonic barriers, a
tempered-distribution weak harmonicity boundary, and only small checked wrappers
around available analysis anchors.
-/

noncomputable section

open Filter
open scoped ENNReal Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_143

universe u v

/-- Outer radius of the `k`th dyadic annulus around a boundary point. -/
def dyadicOuterRadius (k : ℕ) : ℝ :=
  ((2 : ℝ) ^ k)⁻¹

/-- Inner radius of the `k`th dyadic annulus around a boundary point. -/
def dyadicInnerRadius (k : ℕ) : ℝ :=
  ((2 : ℝ) ^ (k + 1))⁻¹

/--
The metric dyadic annulus centered at `p`.

The convention here is `2^-(k+1) ≤ dist x p < 2^-k`; the obstacle used in the
Wiener series additionally intersects this annulus with the complement of the
open domain.
-/
def dyadicAnnulus
    (E : Type u) [PseudoMetricSpace E] (p : E) (k : ℕ) : Set E :=
  {x : E | dyadicInnerRadius k ≤ dist x p ∧ dist x p < dyadicOuterRadius k}

/--
The concrete obstacle set for the `k`th Wiener term: the dyadic annulus around
the boundary point, restricted to points outside the domain.
-/
def dyadicAnnularObstacle
    (E : Type u) [PseudoMetricSpace E] (domain : Set E) (p : E) (k : ℕ) :
    Set E :=
  dyadicAnnulus E p k ∩ domainᶜ

namespace DyadicAnnularObstacle

variable {E : Type u} [PseudoMetricSpace E]

/-- Membership in a dyadic annulus is exactly the two dyadic distance bounds. -/
theorem mem_dyadicAnnulus {p x : E} {k : ℕ} :
    x ∈ dyadicAnnulus E p k ↔
      dyadicInnerRadius k ≤ dist x p ∧ dist x p < dyadicOuterRadius k :=
  Iff.rfl

/-- Membership in the concrete obstacle adds nonmembership in the domain. -/
theorem mem_dyadicAnnularObstacle {domain : Set E} {p x : E} {k : ℕ} :
    x ∈ dyadicAnnularObstacle E domain p k ↔
      dyadicInnerRadius k ≤ dist x p ∧ dist x p < dyadicOuterRadius k ∧
        x ∉ domain := by
  simp [dyadicAnnularObstacle, dyadicAnnulus, and_assoc]

/-- The concrete obstacle is supported outside the open domain. -/
theorem dyadicAnnularObstacle_subset_compl_domain
    (domain : Set E) (p : E) (k : ℕ) :
    dyadicAnnularObstacle E domain p k ⊆ domainᶜ := by
  intro x hx
  exact hx.2

/-- The concrete obstacle is supported in the ambient dyadic annulus. -/
theorem dyadicAnnularObstacle_subset_annulus
    (domain : Set E) (p : E) (k : ℕ) :
    dyadicAnnularObstacle E domain p k ⊆ dyadicAnnulus E p k := by
  intro x hx
  exact hx.1

/-- The concrete obstacle lies in the closed ball with the outer dyadic radius. -/
theorem dyadicAnnularObstacle_subset_closedBall
    (domain : Set E) (p : E) (k : ℕ) :
    dyadicAnnularObstacle E domain p k ⊆ Metric.closedBall p (dyadicOuterRadius k) := by
  intro x hx
  exact Metric.mem_closedBall.mpr (le_of_lt hx.1.2)

/-- The concrete obstacle avoids the open ball with the inner dyadic radius. -/
theorem dyadicAnnularObstacle_disjoint_ball
    (domain : Set E) (p : E) (k : ℕ) :
    Disjoint (dyadicAnnularObstacle E domain p k)
      (Metric.ball p (dyadicInnerRadius k)) := by
  rw [Set.disjoint_left]
  intro x hx hball
  exact not_lt_of_ge hx.1.1 (Metric.mem_ball.mp hball)

end DyadicAnnularObstacle

/-- Dilation of a set by a real scalar, used to state capacity scaling. -/
def dilation
    (E : Type u) [SMul ℝ E] (r : ℝ) (s : Set E) : Set E :=
  (fun x : E => r • x) '' s

/--
Minimal variational/Newtonian capacity interface needed by the Wiener series.

This is not yet a constructed Newtonian capacity.  It is a repo-local API
boundary: any later Newtonian or Sobolev variational capacity implementation
must provide these proof fields before it can instantiate `WienerCriterionData`.
-/
structure VariationalCapacityAPI
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] :
    Type (u + 1) where
  capacity : Set E → ℝ≥0∞
  monotone : Monotone capacity
  compactApproximation :
    ∀ s : Set E,
      capacity s =
        ⨆ K : {K : Set E // IsCompact K ∧ K ⊆ s}, capacity K.1
  scalingFactor : ℝ → ℝ≥0∞
  scaling :
    ∀ (r : ℝ), 0 < r → ∀ s : Set E,
      capacity (dilation E r s) = scalingFactor r * capacity s

namespace VariationalCapacityAPI

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Capacity is monotone under set inclusion. -/
theorem capacity_mono (C : VariationalCapacityAPI E) {s t : Set E} (hst : s ⊆ t) :
    C.capacity s ≤ C.capacity t :=
  C.monotone hst

/-- Compact inner approximation formula exposed as a named checked lemma. -/
theorem capacity_eq_iSup_compact_subsets (C : VariationalCapacityAPI E) (s : Set E) :
    C.capacity s =
      ⨆ K : {K : Set E // IsCompact K ∧ K ⊆ s}, C.capacity K.1 :=
  C.compactApproximation s

/-- Capacity scaling under positive real dilations. -/
theorem capacity_dilation (C : VariationalCapacityAPI E) {r : ℝ} (hr : 0 < r)
    (s : Set E) :
    C.capacity (dilation E r s) = C.scalingFactor r * C.capacity s :=
  C.scaling r hr s

end VariationalCapacityAPI

/--
A harmonic barrier at a boundary point for an open domain.

This is a conservative local interface rather than a theorem that such barriers
exist.  It records the analytic object used in the standard Perron regularity
criterion: a real-valued harmonic function on the domain, nonnegative on the
domain, tending to zero at the boundary point, and strictly positive away from
that point inside the domain.
-/
structure HarmonicBarrier
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (domain : Set E) (p : E) : Type u where
  potential : E → ℝ
  harmonicOn_domain : InnerProductSpace.HarmonicOnNhd potential domain
  nonnegative_on_domain : ∀ x ∈ domain, 0 ≤ potential x
  tendsTo_zero_at_boundaryPoint : Tendsto potential (𝓝[domain] p) (𝓝 0)
  positive_away_from_boundaryPoint : ∀ x ∈ domain, x ≠ p → 0 < potential x

/-- Existence of a harmonic barrier at a boundary point. -/
def HasHarmonicBarrier
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (domain : Set E) (p : E) : Prop :=
  Nonempty (HarmonicBarrier E domain p)

/--
Dirichlet/Perron boundary regularity model used by the Stage1 Wiener statement.

`RegularAt` is the Perron/Dirichlet predicate selected by a later terminal
formalization.  The required bridge records the classical barrier criterion at
open-domain frontier points, without asserting that the model has already been
constructed from Perron upper/lower envelopes in this repository.
-/
structure DirichletPerronRegularityModel
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    Type (u + 1) where
  RegularAt : Set E → E → Prop
  regular_iff_harmonicBarrier :
    ∀ {domain : Set E} {p : E}, IsOpen domain → p ∈ frontier domain →
      (RegularAt domain p ↔ HasHarmonicBarrier E domain p)

namespace DirichletPerronRegularityModel

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]

/-- Boundary regularity is equivalent to the existence of a harmonic barrier. -/
theorem regular_iff_hasHarmonicBarrier
    (R : DirichletPerronRegularityModel E) {domain : Set E} {p : E}
    (hopen : IsOpen domain) (hfrontier : p ∈ frontier domain) :
    R.RegularAt domain p ↔ HasHarmonicBarrier E domain p :=
  R.regular_iff_harmonicBarrier (domain := domain) (p := p) hopen hfrontier

/-- A harmonic barrier proves regularity in the chosen Dirichlet/Perron model. -/
theorem regular_of_harmonicBarrier
    (R : DirichletPerronRegularityModel E) {domain : Set E} {p : E}
    (hopen : IsOpen domain) (hfrontier : p ∈ frontier domain)
    (hbarrier : HasHarmonicBarrier E domain p) :
    R.RegularAt domain p :=
  (R.regular_iff_hasHarmonicBarrier hopen hfrontier).mpr hbarrier

/-- Regularity in the chosen Dirichlet/Perron model gives a harmonic barrier. -/
theorem harmonicBarrier_of_regular
    (R : DirichletPerronRegularityModel E) {domain : Set E} {p : E}
    (hopen : IsOpen domain) (hfrontier : p ∈ frontier domain)
    (hregular : R.RegularAt domain p) :
    HasHarmonicBarrier E domain p :=
  (R.regular_iff_hasHarmonicBarrier hopen hfrontier).mp hregular

end DirichletPerronRegularityModel

/--
Global distributional harmonicity for a scalar tempered distribution.

This is the concrete weak side currently available from mathlib's distribution
Laplacian API.  It is still global and tempered-distribution based; a terminal
Wiener formalization must localize it to the selected domain and connect it to
the chosen weak Dirichlet/Perron solution notion.
-/
def TemperedDistributionHarmonic
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (T : TemperedDistribution E ℂ) : Prop :=
  Laplacian.laplacian T = 0

namespace TemperedDistributionHarmonic

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]

/--
Distributional harmonicity is equivalent to vanishing against every classical
Schwartz-test Laplacian.  This is a checked weak-formulation anchor from
mathlib's `TemperedDistribution.laplacian_apply_apply`.
-/
theorem iff_forall_test_laplacian_zero (T : TemperedDistribution E ℂ) :
    TemperedDistributionHarmonic E T ↔
      ∀ φ : SchwartzMap E ℂ, T (Laplacian.laplacian φ) = 0 := by
  constructor
  · intro hT φ
    have happly : (Laplacian.laplacian T) φ = 0 := by
      rw [hT]
      rfl
    rwa [TemperedDistribution.laplacian_apply_apply] at happly
  · intro hT
    ext φ
    rw [TemperedDistribution.laplacian_apply_apply, hT φ]
    rfl

/-- A named elimination form for the checked weak formulation. -/
theorem test_laplacian_zero
    {T : TemperedDistribution E ℂ} (hT : TemperedDistributionHarmonic E T)
    (φ : SchwartzMap E ℂ) :
    T (Laplacian.laplacian φ) = 0 :=
  (iff_forall_test_laplacian_zero T).mp hT φ

end TemperedDistributionHarmonic

/--
Repo-local bridge contract from weak distributional harmonicity to classical
mathlib harmonicity.

The fields deliberately separate three obligations that are missing from local
mathlib for Wiener's criterion:

* representing a domain-level weak solution by a scalar tempered distribution;
* identifying the chosen weak harmonic predicate with distributional
  Laplacian-zero;
* upgrading the weak solution to `InnerProductSpace.HarmonicOnNhd` on an open
  domain.

This is an integration target, not a proof that the PDE regularity theorem is
already available in this repository.
-/
structure WeakToClassicalHarmonicityBridge
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    Type (u + 1) where
  representsTemperedDistribution :
    (E → ℂ) → Set E → TemperedDistribution E ℂ → Prop
  weakHarmonicOn : (E → ℂ) → Set E → Prop
  weak_iff_distributional_laplacian_zero :
    ∀ {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ},
      representsTemperedDistribution f domain T →
        (weakHarmonicOn f domain ↔ TemperedDistributionHarmonic E T)
  classical_of_weak :
    ∀ {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ},
      IsOpen domain →
        representsTemperedDistribution f domain T →
          weakHarmonicOn f domain →
            InnerProductSpace.HarmonicOnNhd f domain
  weak_of_classical :
    ∀ {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ},
      representsTemperedDistribution f domain T →
        InnerProductSpace.HarmonicOnNhd f domain →
          weakHarmonicOn f domain

namespace WeakToClassicalHarmonicityBridge

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]

/-- The bridge identifies weak harmonicity with zero distributional Laplacian. -/
theorem weak_iff_distributional_harmonic
    (B : WeakToClassicalHarmonicityBridge E)
    {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ}
    (hrep : B.representsTemperedDistribution f domain T) :
    B.weakHarmonicOn f domain ↔ TemperedDistributionHarmonic E T :=
  B.weak_iff_distributional_laplacian_zero hrep

/-- A weak harmonic function is classically harmonic once the bridge is supplied. -/
theorem classical_of_weakHarmonicOn
    (B : WeakToClassicalHarmonicityBridge E)
    {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ}
    (hopen : IsOpen domain)
    (hrep : B.representsTemperedDistribution f domain T)
    (hweak : B.weakHarmonicOn f domain) :
    InnerProductSpace.HarmonicOnNhd f domain :=
  B.classical_of_weak hopen hrep hweak

/-- Classical harmonicity feeds back into the selected weak harmonic predicate. -/
theorem weakHarmonicOn_of_classical
    (B : WeakToClassicalHarmonicityBridge E)
    {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ}
    (hrep : B.representsTemperedDistribution f domain T)
    (hclassical : InnerProductSpace.HarmonicOnNhd f domain) :
    B.weakHarmonicOn f domain :=
  B.weak_of_classical hrep hclassical

/--
The checked test-function consequence available after the bridge identifies the
weak predicate with distributional Laplacian-zero.
-/
theorem test_laplacian_zero_of_weakHarmonicOn
    (B : WeakToClassicalHarmonicityBridge E)
    {f : E → ℂ} {domain : Set E} {T : TemperedDistribution E ℂ}
    (hrep : B.representsTemperedDistribution f domain T)
    (hweak : B.weakHarmonicOn f domain)
    (φ : SchwartzMap E ℂ) :
    T (Laplacian.laplacian φ) = 0 :=
  TemperedDistributionHarmonic.test_laplacian_zero
    ((B.weak_iff_distributional_harmonic hrep).mp hweak) φ

end WeakToClassicalHarmonicityBridge

/--
Normalized data needed to state the Wiener criterion at one boundary point.

The obstacle sets are now derived from concrete dyadic annuli around
`boundaryPoint` intersected with the complement of `domain`. For a terminal
formalization, `capacityAPI` should still be replaced by concrete Newtonian
capacity, `regularityModel` should be constructed from the chosen Perron or
Dirichlet solution API, and `weakClassicalBridge` should be instantiated by a
domain-local elliptic regularity theorem or pinned PDE dependency.
-/
structure WienerCriterionData
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    Type (u + 1) where
  domain : Set E
  boundaryPoint : E
  isOpen_domain : IsOpen domain
  boundaryPoint_mem_frontier : boundaryPoint ∈ frontier domain
  capacityAPI : VariationalCapacityAPI E
  scaleWeight : ℕ → ℝ≥0∞
  regularityModel : DirichletPerronRegularityModel E
  weakClassicalBridge : WeakToClassicalHarmonicityBridge E
  harmonicDirichletModelAvailable : Prop

namespace WienerCriterionData

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]

/-- The capacity attached to a Wiener data package. -/
def capacity (D : WienerCriterionData E) : Set E → ℝ≥0∞ :=
  D.capacityAPI.capacity

/-- The concrete dyadic obstacle used in the `k`th Wiener term. -/
def annularObstacle (D : WienerCriterionData E) (k : ℕ) : Set E :=
  dyadicAnnularObstacle E D.domain D.boundaryPoint k

/-- Capacity monotonicity inherited by the Wiener data package. -/
theorem capacity_mono (D : WienerCriterionData E) {s t : Set E} (hst : s ⊆ t) :
    D.capacity s ≤ D.capacity t :=
  D.capacityAPI.capacity_mono hst

/-- Compact inner approximation inherited by the Wiener data package. -/
theorem capacity_eq_iSup_compact_subsets (D : WienerCriterionData E) (s : Set E) :
    D.capacity s =
      ⨆ K : {K : Set E // IsCompact K ∧ K ⊆ s}, D.capacity K.1 :=
  D.capacityAPI.capacity_eq_iSup_compact_subsets s

/-- Positive-dilation scaling inherited by the Wiener data package. -/
theorem capacity_dilation (D : WienerCriterionData E) {r : ℝ} (hr : 0 < r)
    (s : Set E) :
    D.capacity (dilation E r s) = D.capacityAPI.scalingFactor r * D.capacity s :=
  D.capacityAPI.capacity_dilation hr s

/-- Membership in the concrete obstacle attached to Wiener data. -/
theorem mem_annularObstacle (D : WienerCriterionData E) {x : E} {k : ℕ} :
    x ∈ D.annularObstacle k ↔
      dyadicInnerRadius k ≤ dist x D.boundaryPoint ∧
        dist x D.boundaryPoint < dyadicOuterRadius k ∧ x ∉ D.domain :=
  DyadicAnnularObstacle.mem_dyadicAnnularObstacle

/-- The Wiener obstacle is supported outside the domain. -/
theorem annularObstacle_subset_compl_domain (D : WienerCriterionData E) (k : ℕ) :
    D.annularObstacle k ⊆ D.domainᶜ :=
  DyadicAnnularObstacle.dyadicAnnularObstacle_subset_compl_domain D.domain D.boundaryPoint k

/-- The Wiener obstacle is supported in its dyadic annulus. -/
theorem annularObstacle_subset_annulus (D : WienerCriterionData E) (k : ℕ) :
    D.annularObstacle k ⊆ dyadicAnnulus E D.boundaryPoint k :=
  DyadicAnnularObstacle.dyadicAnnularObstacle_subset_annulus D.domain D.boundaryPoint k

/-- The Wiener obstacle lies in the closed ball with the outer dyadic radius. -/
theorem annularObstacle_subset_closedBall (D : WienerCriterionData E) (k : ℕ) :
    D.annularObstacle k ⊆ Metric.closedBall D.boundaryPoint (dyadicOuterRadius k) :=
  DyadicAnnularObstacle.dyadicAnnularObstacle_subset_closedBall D.domain D.boundaryPoint k

/-- The Wiener obstacle avoids the open ball with the inner dyadic radius. -/
theorem annularObstacle_disjoint_ball (D : WienerCriterionData E) (k : ℕ) :
    Disjoint (D.annularObstacle k)
      (Metric.ball D.boundaryPoint (dyadicInnerRadius k)) :=
  DyadicAnnularObstacle.dyadicAnnularObstacle_disjoint_ball D.domain D.boundaryPoint k

/-- Boundary regularity at the distinguished point in the chosen Perron model. -/
def isRegularBoundaryPoint (D : WienerCriterionData E) : Prop :=
  D.regularityModel.RegularAt D.domain D.boundaryPoint

/-- The chosen boundary regularity predicate is connected to harmonic barriers. -/
theorem isRegularBoundaryPoint_iff_hasHarmonicBarrier (D : WienerCriterionData E) :
    D.isRegularBoundaryPoint ↔ HasHarmonicBarrier E D.domain D.boundaryPoint :=
  D.regularityModel.regular_iff_hasHarmonicBarrier
    D.isOpen_domain D.boundaryPoint_mem_frontier

/-- A harmonic barrier proves boundary regularity for the distinguished point. -/
theorem isRegularBoundaryPoint_of_harmonicBarrier (D : WienerCriterionData E)
    (hbarrier : HasHarmonicBarrier E D.domain D.boundaryPoint) :
    D.isRegularBoundaryPoint :=
  D.regularityModel.regular_of_harmonicBarrier
    D.isOpen_domain D.boundaryPoint_mem_frontier hbarrier

/-- Boundary regularity for the distinguished point gives a harmonic barrier. -/
theorem harmonicBarrier_of_isRegularBoundaryPoint (D : WienerCriterionData E)
    (hregular : D.isRegularBoundaryPoint) :
    HasHarmonicBarrier E D.domain D.boundaryPoint :=
  D.regularityModel.harmonicBarrier_of_regular
    D.isOpen_domain D.boundaryPoint_mem_frontier hregular

/-- The `k`th term of the normalized Wiener capacity series. -/
def wienerTerm (D : WienerCriterionData E) (k : ℕ) : ℝ≥0∞ :=
  D.scaleWeight k * D.capacity (D.annularObstacle k)

/-- Partial sums of the normalized Wiener capacity series. -/
def partialWienerSum (D : WienerCriterionData E) (N : ℕ) : ℝ≥0∞ :=
  ∑ k ∈ Finset.range N, D.wienerTerm k

/-- Divergence of the normalized Wiener series. -/
def WienerSeriesDiverges (D : WienerCriterionData E) : Prop :=
  Tendsto D.partialWienerSum atTop atTop

/--
Convergence side of the normalized Wiener series for the Stage1 branch split.

For the current `ℝ≥0∞` partial-sum statement shape this is recorded as
non-divergence to `atTop`.  A terminal Newtonian-capacity formalization may
replace this by an equivalent finite-sum/summability predicate once the
capacity normalization and comparison lemmas are fixed.
-/
def WienerSeriesConverges (D : WienerCriterionData E) : Prop :=
  ¬ D.WienerSeriesDiverges

/--
The Wiener criterion formula: the normalized capacity series diverges exactly
when the boundary point is regular for the Dirichlet problem.
-/
def WienerCriterionFormula (D : WienerCriterionData E) : Prop :=
  D.WienerSeriesDiverges ↔ D.isRegularBoundaryPoint

/-- The zeroth partial sum is definitionally the empty finite sum. -/
theorem partialWienerSum_zero (D : WienerCriterionData E) :
    D.partialWienerSum 0 = 0 := by
  simp [partialWienerSum]

/-- The divergence-to-regularity branch of the Wiener criterion. -/
def WienerDivergenceBranchFormula (D : WienerCriterionData E) : Prop :=
  D.WienerSeriesDiverges → D.isRegularBoundaryPoint

/-- Irregularity at the distinguished boundary point in the chosen Perron model. -/
def isIrregularBoundaryPoint (D : WienerCriterionData E) : Prop :=
  ¬ D.isRegularBoundaryPoint

/-- The convergence-to-irregularity branch of the Wiener criterion. -/
def WienerConvergenceIrregularityBranchFormula (D : WienerCriterionData E) : Prop :=
  D.WienerSeriesConverges → D.isIrregularBoundaryPoint

/--
The divergence branch is the forward projection of the bidirectional criterion.

This is a checked logical projection, not a proof of Wiener's criterion itself:
the hypothesis `D.WienerCriterionFormula` still has to be supplied by a concrete
local proof body or a pinned checked dependency.
-/
theorem divergenceBranch_of_wienerCriterionFormula
    (D : WienerCriterionData E) (hcriterion : D.WienerCriterionFormula) :
    D.WienerDivergenceBranchFormula :=
  hcriterion.mp

/--
The convergence/irregularity branch is the contrapositive projection of the
regularity-to-divergence direction of the bidirectional criterion.

This is a checked logical projection, not a proof of Wiener's criterion itself:
the hypothesis `D.WienerCriterionFormula` still has to be supplied by a concrete
local proof body or a pinned checked dependency.
-/
theorem convergenceIrregularityBranch_of_wienerCriterionFormula
    (D : WienerCriterionData E) (hcriterion : D.WienerCriterionFormula) :
    D.WienerConvergenceIrregularityBranchFormula := by
  intro hconverges hregular
  exact hconverges (hcriterion.mpr hregular)

end WienerCriterionData

/--
Stage1 statement-shape candidate for Wiener's criterion.

This is intentionally a proposition only.  It does not assert a proof of the
criterion; it fixes the Lean shape that a later capacity/Perron formalization
or pinned external dependency must close.
-/
def StatementShape
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] : Prop :=
  ∀ D : WienerCriterionData E, D.WienerCriterionFormula

/-- The statement shape unfolds to the per-boundary-point Wiener formula. -/
theorem statementShape_iff_forall_data
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    StatementShape E ↔
      ∀ D : WienerCriterionData E, D.WienerSeriesDiverges ↔ D.isRegularBoundaryPoint :=
  Iff.rfl

/-- Stage1 statement-shape candidate for the divergence branch alone. -/
def DivergenceBranchShape
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    Prop :=
  ∀ D : WienerCriterionData E, D.WienerDivergenceBranchFormula

/-- The divergence-branch shape unfolds to the forward implication for every data package. -/
theorem divergenceBranchShape_iff_forall_data
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    DivergenceBranchShape E ↔
      ∀ D : WienerCriterionData E, D.WienerSeriesDiverges → D.isRegularBoundaryPoint :=
  Iff.rfl

/-- The full statement shape implies the divergence-branch statement shape. -/
theorem divergenceBranchShape_of_statementShape
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (hshape : StatementShape E) :
    DivergenceBranchShape E := by
  intro D
  exact D.divergenceBranch_of_wienerCriterionFormula (hshape D)

/-- Stage1 statement-shape candidate for the convergence/irregularity branch alone. -/
def ConvergenceIrregularityBranchShape
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    Prop :=
  ∀ D : WienerCriterionData E, D.WienerConvergenceIrregularityBranchFormula

/--
The convergence/irregularity-branch shape unfolds to the contrapositive
implication for every data package.
-/
theorem convergenceIrregularityBranchShape_iff_forall_data
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] :
    ConvergenceIrregularityBranchShape E ↔
      ∀ D : WienerCriterionData E, D.WienerSeriesConverges → D.isIrregularBoundaryPoint :=
  Iff.rfl

/-- The full statement shape implies the convergence/irregularity-branch shape. -/
theorem convergenceIrregularityBranchShape_of_statementShape
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (hshape : StatementShape E) :
    ConvergenceIrregularityBranchShape E := by
  intro D
  exact D.convergenceIrregularityBranch_of_wienerCriterionFormula (hshape D)

/--
Checked wrapper: constant functions are harmonic on finite-dimensional real
inner-product spaces.  This is harmonic-function substrate, not the Wiener
criterion.
-/
theorem harmonicOnNhd_const_mathlib_wrapper
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (F : Type v) [NormedAddCommGroup F] [NormedSpace ℝ F]
    (s : Set E) (c : F) :
    InnerProductSpace.HarmonicOnNhd (fun _ : E => c) s := by
  exact InnerProductSpace.harmonicOnNhd_const (E := E) (F := F) (s := s) (c := c)

/-- Checked wrapper: harmonic-on-neighborhood functions are continuous on the set. -/
theorem harmonicOnNhd_continuousOn_mathlib_wrapper
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {s : Set E} {f : E → F}
    (hf : InnerProductSpace.HarmonicOnNhd f s) :
    ContinuousOn f s :=
  hf.continuousOn

/--
Checked wrapper: the distributional Laplacian of a tempered distribution acts by
testing against the classical Laplacian on Schwartz functions.
-/
theorem tempered_laplacian_apply_mathlib_wrapper
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace ℂ F]
    (T : TemperedDistribution E F) (φ : SchwartzMap E ℂ) :
    (Laplacian.laplacian T) φ = T (Laplacian.laplacian φ) :=
  TemperedDistribution.laplacian_apply_apply T φ

/--
Proof-route segments for child task `S1-M-143-C005`, the
divergence-to-regularity branch of Wiener's criterion.

These segment names are a checked local budget ledger, not theorem completion
evidence.  Turning them into proof-bearing declarations still requires concrete
capacity, capacitary-potential, barrier, summation, and Perron-regularity APIs.
-/
inductive WienerDivergenceBranchSegment where
  | capacityModel
  | annularCapacityEstimate
  | capacitaryPotential
  | barrierConstruction
  | divergentSeriesLimit
  | regularityBridge
  | terminalWrapper
  | externalImportGate
  deriving DecidableEq, Repr

/-- One `<=100`-step proof-route leaf in the C005 divergence-branch ledger. -/
structure ChildC005DivergenceBranchLeaf where
  leafId : String
  segment : WienerDivergenceBranchSegment
  target : String
  prerequisites : List String
  expectedOutput : String
  estimatedStepBudget : Nat
  currentRepoLocalStatus : String
  blocker : String

/--
Checked `<=100`-step leaf split for the divergence branch.

The rows are intentionally blockers/targets.  The local artifact now has the
named branch formula and logical projection from the bidirectional criterion,
but it does not contain a proof-bearing divergence theorem.
-/
def childC005DivergenceBranchLeaves : List ChildC005DivergenceBranchLeaf := [
  {
    leafId := "WIENER-C005-CAP-01"
    segment := WienerDivergenceBranchSegment.capacityModel
    target := "Instantiate a concrete Newtonian or variational capacity API."
    prerequisites := [
      "selected capacity convention",
      "monotonicity theorem",
      "compact inner approximation theorem",
      "positive-dilation scaling theorem"
    ]
    expectedOutput :=
      "A proof-bearing replacement for the abstract `VariationalCapacityAPI` input."
    estimatedStepBudget := 90
    currentRepoLocalStatus := "formalization_debt"
    blocker :=
      "Pinned mathlib does not expose a located Newtonian capacity API for this slot."
  },
  {
    leafId := "WIENER-C005-ANN-01"
    segment := WienerDivergenceBranchSegment.annularCapacityEstimate
    target := "Prove the dyadic annular capacity lower estimates used by the branch."
    prerequisites := [
      "concrete dyadic obstacle sets",
      "capacity scaling",
      "annular support and monotonicity lemmas"
    ]
    expectedOutput :=
      "A checked estimate connecting `D.capacity (D.annularObstacle k)` to the \
      normalized Wiener term."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "Only support lemmas for dyadic obstacles are currently present."
  },
  {
    leafId := "WIENER-C005-POT-01"
    segment := WienerDivergenceBranchSegment.capacitaryPotential
    target := "Construct capacitary potentials for annular obstacle pieces."
    prerequisites := [
      "capacity minimizer or equilibrium-potential existence",
      "energy minimization API",
      "obstacle boundary values"
    ]
    expectedOutput :=
      "A potential package with harmonicity away from the obstacle and energy control."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "The repository has no capacitary-potential construction."
  },
  {
    leafId := "WIENER-C005-POT-02"
    segment := WienerDivergenceBranchSegment.capacitaryPotential
    target := "Bridge weak/distributional potential harmonicity to classical harmonicity."
    prerequisites := [
      "capacitary potentials",
      "weak harmonic predicate",
      "domain-local weak-to-classical regularity theorem"
    ]
    expectedOutput :=
      "An instantiation or pinned proof for `WeakToClassicalHarmonicityBridge`."
    estimatedStepBudget := 95
    currentRepoLocalStatus := "formalization_debt"
    blocker :=
      "The current bridge is an interface; no domain-local elliptic regularity theorem is supplied."
  },
  {
    leafId := "WIENER-C005-BAR-01"
    segment := WienerDivergenceBranchSegment.barrierConstruction
    target := "Assemble a harmonic barrier from normalized capacitary potentials."
    prerequisites := [
      "capacitary potentials",
      "annular estimates",
      "positivity and harmonicity away from obstacle pieces"
    ]
    expectedOutput := "A `HasHarmonicBarrier E D.domain D.boundaryPoint` proof."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "Barrier construction lemmas are not present locally or through a pinned dependency."
  },
  {
    leafId := "WIENER-C005-SER-01"
    segment := WienerDivergenceBranchSegment.divergentSeriesLimit
    target := "Use divergence of the Wiener series to force the barrier limit at the boundary point."
    prerequisites := [
      "`D.WienerSeriesDiverges`",
      "capacity lower estimates",
      "potential comparison or product/sum estimates near the boundary point"
    ]
    expectedOutput :=
      "The zero-limit property required by `HarmonicBarrier.tendsTo_zero_at_boundaryPoint`."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "The needed analytic comparison and summation estimates are absent."
  },
  {
    leafId := "WIENER-C005-REG-01"
    segment := WienerDivergenceBranchSegment.regularityBridge
    target := "Transfer the constructed barrier to Perron/Dirichlet boundary regularity."
    prerequisites := [
      "`HasHarmonicBarrier E D.domain D.boundaryPoint`",
      "`DirichletPerronRegularityModel.regular_of_harmonicBarrier`",
      "frontier membership of the boundary point"
    ]
    expectedOutput := "`D.isRegularBoundaryPoint`."
    estimatedStepBudget := 50
    currentRepoLocalStatus := "checked_interface_only"
    blocker := "The transfer wrapper is present, but the barrier proof is absent."
  },
  {
    leafId := "WIENER-C005-TERM-01"
    segment := WienerDivergenceBranchSegment.terminalWrapper
    target := "Wrap the branch as `D.WienerDivergenceBranchFormula`."
    prerequisites := [
      "divergence-series hypothesis",
      "barrier construction",
      "regularity bridge"
    ]
    expectedOutput :=
      "A proof-bearing theorem of `D.WienerSeriesDiverges → D.isRegularBoundaryPoint`."
    estimatedStepBudget := 60
    currentRepoLocalStatus := "checked_target_only"
    blocker :=
      "`WienerDivergenceBranchFormula` is defined, but no branch proof body is available."
  },
  {
    leafId := "WIENER-C005-EXT-01"
    segment := WienerDivergenceBranchSegment.externalImportGate
    target := "If an external Lean 4 divergence-branch proof exists, pin/import/check it."
    prerequisites := [
      "authenticated Lean 4 source repository",
      "exact commit and module path",
      "placeholder-free proof path",
      "Lake dependency or vendoring plan"
    ]
    expectedOutput :=
      "A repo-local wrapper theorem checked by `lake env lean`, or a concrete integration blocker."
    estimatedStepBudget := 75
    currentRepoLocalStatus := "not_repo_local_closed"
    blocker :=
      "No external divergence-branch proof has been pinned or checked in this child pass."
  }
]

/-- The C005 divergence-branch route split contains nine local leaves. -/
theorem childC005DivergenceBranchLeaves_length :
    childC005DivergenceBranchLeaves.length = 9 :=
  rfl

/-- Machine-checkable budget predicate for a divergence-branch leaf. -/
def childC005DivergenceBranchLeafWithinBudget
    (leaf : ChildC005DivergenceBranchLeaf) : Bool :=
  decide (leaf.estimatedStepBudget <= 100)

/-- The current C005 divergence split satisfies the syntactic `<=100` budget. -/
def childC005EveryDivergenceBranchLeafWithinBudget : Bool :=
  childC005DivergenceBranchLeaves.all childC005DivergenceBranchLeafWithinBudget

/-- Checked C005 divergence-branch leaf-budget gate. -/
theorem childC005EveryDivergenceBranchLeafWithinBudget_eq_true :
    childC005EveryDivergenceBranchLeafWithinBudget = true :=
  rfl

/-- Completion gate for the C005 divergence-branch split. -/
structure ChildC005DivergenceBranchGate where
  childTask : String
  currentMachineStatus : String
  debtClassification : String
  branchFormulaName : String
  checkedProjectionName : String
  proofBearingDivergenceBranchClaimed : Bool
  parentCompletionAllowed : Bool
  repoLocalIntegrationDebtCompletionResidue : Bool
  leafCount : Nat
  allLeavesWithinBudget : Bool
  routeLeaves : List ChildC005DivergenceBranchLeaf
  nextPublicMergeTarget : String

/--
S1-M-143-C005 result.

The divergence branch now has a checked formula target, a checked projection
from the full bidirectional criterion, and a local `<=100` route ledger.  It
does not prove the divergence branch of Wiener's criterion.
-/
def childC005DivergenceBranchGate : ChildC005DivergenceBranchGate where
  childTask := "S1-M-143-C005"
  currentMachineStatus := "checked_divergence_branch_target_and_budget_metadata_only"
  debtClassification := "formalization_debt"
  branchFormulaName := "WienerCriterionData.WienerDivergenceBranchFormula"
  checkedProjectionName := "WienerCriterionData.divergenceBranch_of_wienerCriterionFormula"
  proofBearingDivergenceBranchClaimed := false
  parentCompletionAllowed := false
  repoLocalIntegrationDebtCompletionResidue := false
  leafCount := childC005DivergenceBranchLeaves.length
  allLeavesWithinBudget := childC005EveryDivergenceBranchLeafWithinBudget
  routeLeaves := childC005DivergenceBranchLeaves
  nextPublicMergeTarget :=
    "Serial integrator should merge the C005 divergence-branch ledger into \
    Docs/Stage1_Blueprint.md and synchronized todo surfaces without marking \
    THM-M-1153 complete."

/-- C005 records nine divergence-branch leaves. -/
theorem childC005DivergenceBranchGate_leafCount_eq :
    childC005DivergenceBranchGate.leafCount = 9 :=
  rfl

/-- C005 divergence-branch metadata satisfies the `<=100` leaf gate. -/
theorem childC005DivergenceBranchGate_allLeavesWithinBudget_eq_true :
    childC005DivergenceBranchGate.allLeavesWithinBudget = true :=
  rfl

/-- C005 does not claim a proof-bearing divergence branch. -/
theorem childC005_proofBearingDivergenceBranchClaimed_eq_false :
    childC005DivergenceBranchGate.proofBearingDivergenceBranchClaimed = false :=
  rfl

/-- C005 does not allow parent completion from branch-target metadata alone. -/
theorem childC005_parentCompletionAllowed_eq_false :
    childC005DivergenceBranchGate.parentCompletionAllowed = false :=
  rfl

/-- C005 leaves no completed-state repo-local integration-debt residue. -/
theorem childC005_no_repoLocalIntegrationDebtCompletionResidue :
    childC005DivergenceBranchGate.repoLocalIntegrationDebtCompletionResidue = false :=
  rfl

/-! ## C006 convergence/irregularity branch ledger -/

/--
Proof-route segments for child task `S1-M-143-C006`, the
convergence-to-irregularity branch of Wiener's criterion.

These segment names are a checked local budget ledger, not theorem completion
evidence.  Turning them into proof-bearing declarations still requires concrete
capacity, thinness/convergence estimates, Perron irregularity, and external
pin/import/check closure if a terminal Lean proof is found.
-/
inductive WienerConvergenceIrregularityBranchSegment where
  | convergenceNormalization
  | capacityModel
  | annularUpperEstimate
  | thinnessPotential
  | irregularityWitness
  | perronBridge
  | terminalContrapositiveWrapper
  | externalImportGate
  deriving DecidableEq, Repr

/-- One `<=100`-step proof-route leaf in the C006 convergence/irregularity ledger. -/
structure ChildC006ConvergenceIrregularityBranchLeaf where
  leafId : String
  segment : WienerConvergenceIrregularityBranchSegment
  target : String
  prerequisites : List String
  expectedOutput : String
  estimatedStepBudget : Nat
  currentRepoLocalStatus : String
  blocker : String

/--
Checked `<=100`-step leaf split for the convergence/irregularity branch.

The rows are intentionally blockers/targets.  The local artifact now has the
named branch formula and checked contrapositive projection from the
bidirectional criterion, but it does not contain a proof-bearing convergence
branch theorem.
-/
def childC006ConvergenceIrregularityBranchLeaves :
    List ChildC006ConvergenceIrregularityBranchLeaf := [
  {
    leafId := "WIENER-C006-NORM-01"
    segment := WienerConvergenceIrregularityBranchSegment.convergenceNormalization
    target :=
      "Replace `WienerSeriesConverges = ¬ WienerSeriesDiverges` by the selected \
      finite-sum or summability formulation, or prove the equivalence for the \
      chosen `ℝ≥0∞` normalization."
    prerequisites := [
      "concrete scale weights",
      "monotonicity of partial Wiener sums",
      "summability or finite-limit API for `ℝ≥0∞` series"
    ]
    expectedOutput :=
      "A checked equivalence between the analytic convergence hypothesis and \
      the branch predicate used by `WienerConvergenceIrregularityBranchFormula`."
    estimatedStepBudget := 85
    currentRepoLocalStatus := "checked_target_only"
    blocker :=
      "The current file records convergence as non-divergence because the \
      terminal capacity normalization is not fixed."
  },
  {
    leafId := "WIENER-C006-CAP-01"
    segment := WienerConvergenceIrregularityBranchSegment.capacityModel
    target := "Instantiate the concrete Newtonian or variational capacity API used by the branch."
    prerequisites := [
      "selected Newtonian/Sobolev capacity",
      "monotonicity theorem",
      "compact approximation theorem",
      "positive-dilation scaling theorem"
    ]
    expectedOutput := "A proof-bearing replacement for the abstract `VariationalCapacityAPI` input."
    estimatedStepBudget := 90
    currentRepoLocalStatus := "formalization_debt"
    blocker := "Pinned mathlib does not expose a located Newtonian capacity API for this slot."
  },
  {
    leafId := "WIENER-C006-ANN-01"
    segment := WienerConvergenceIrregularityBranchSegment.annularUpperEstimate
    target := "Prove the dyadic annular capacity upper/control estimates used by the convergence branch."
    prerequisites := [
      "concrete dyadic obstacle sets",
      "capacity scaling",
      "annular support lemmas",
      "compact approximation"
    ]
    expectedOutput :=
      "A checked estimate converting finite Wiener mass into thinness/control \
      near the boundary point."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "Only support lemmas for dyadic obstacles are currently present."
  },
  {
    leafId := "WIENER-C006-THIN-01"
    segment := WienerConvergenceIrregularityBranchSegment.thinnessPotential
    target := "Construct the thinness/capacitary-potential package from the convergent Wiener series."
    prerequisites := [
      "annular upper/control estimates",
      "capacitary potentials",
      "series comparison estimates near the boundary point"
    ]
    expectedOutput :=
      "A potential-theoretic witness showing the complement is thin at the boundary point."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "The repository has no thinness or capacitary-potential construction."
  },
  {
    leafId := "WIENER-C006-THIN-02"
    segment := WienerConvergenceIrregularityBranchSegment.thinnessPotential
    target := "Bridge weak/distributional harmonicity of the thinness witness to classical harmonicity."
    prerequisites := [
      "thinness witness",
      "weak harmonic predicate",
      "domain-local weak-to-classical regularity theorem"
    ]
    expectedOutput := "An instantiation or pinned proof for `WeakToClassicalHarmonicityBridge`."
    estimatedStepBudget := 95
    currentRepoLocalStatus := "formalization_debt"
    blocker :=
      "The current bridge is an interface; no domain-local elliptic regularity theorem is supplied."
  },
  {
    leafId := "WIENER-C006-WIT-01"
    segment := WienerConvergenceIrregularityBranchSegment.irregularityWitness
    target := "Build the Perron/Dirichlet irregularity witness from the thinness package."
    prerequisites := [
      "thinness/capacitary-potential package",
      "comparison principle",
      "boundary limit failure for a Perron solution or barrier negation"
    ]
    expectedOutput := "`D.isIrregularBoundaryPoint`, equivalently `¬ D.isRegularBoundaryPoint`."
    estimatedStepBudget := 100
    currentRepoLocalStatus := "formalization_debt"
    blocker := "No Perron irregularity witness or comparison-principle API is present locally."
  },
  {
    leafId := "WIENER-C006-PER-01"
    segment := WienerConvergenceIrregularityBranchSegment.perronBridge
    target := "Transfer the analytic irregularity witness to the selected Perron regularity predicate."
    prerequisites := [
      "Dirichlet/Perron regularity model",
      "barrier criterion",
      "proof that the thinness witness refutes harmonic barriers or regular Perron limits"
    ]
    expectedOutput := "`D.isIrregularBoundaryPoint` in the chosen `DirichletPerronRegularityModel`."
    estimatedStepBudget := 80
    currentRepoLocalStatus := "checked_interface_only"
    blocker := "The barrier-to-regularity bridge is present, but the irregularity witness is absent."
  },
  {
    leafId := "WIENER-C006-TERM-01"
    segment := WienerConvergenceIrregularityBranchSegment.terminalContrapositiveWrapper
    target := "Wrap the branch as `D.WienerConvergenceIrregularityBranchFormula`."
    prerequisites := [
      "convergence-series hypothesis",
      "irregularity witness",
      "Perron bridge"
    ]
    expectedOutput :=
      "A proof-bearing theorem of `D.WienerSeriesConverges → D.isIrregularBoundaryPoint`."
    estimatedStepBudget := 60
    currentRepoLocalStatus := "checked_target_only"
    blocker :=
      "`WienerConvergenceIrregularityBranchFormula` is defined, but no analytic branch proof body is available."
  },
  {
    leafId := "WIENER-C006-EXT-01"
    segment := WienerConvergenceIrregularityBranchSegment.externalImportGate
    target := "If an external Lean 4 convergence/irregularity proof exists, pin/import/check it."
    prerequisites := [
      "authenticated Lean 4 source repository",
      "exact commit and module path",
      "placeholder-free proof path",
      "Lake dependency or vendoring plan"
    ]
    expectedOutput :=
      "A repo-local wrapper theorem checked by `lake env lean`, or a concrete integration blocker."
    estimatedStepBudget := 75
    currentRepoLocalStatus := "not_repo_local_closed"
    blocker :=
      "No external convergence/irregularity branch proof has been pinned or checked in this child pass."
  }
]

/-- The C006 convergence/irregularity route split contains nine local leaves. -/
theorem childC006ConvergenceIrregularityBranchLeaves_length :
    childC006ConvergenceIrregularityBranchLeaves.length = 9 :=
  rfl

/-- Machine-checkable budget predicate for a convergence/irregularity leaf. -/
def childC006ConvergenceIrregularityBranchLeafWithinBudget
    (leaf : ChildC006ConvergenceIrregularityBranchLeaf) : Bool :=
  decide (leaf.estimatedStepBudget <= 100)

/-- The current C006 convergence/irregularity split satisfies the syntactic `<=100` budget. -/
def childC006EveryConvergenceIrregularityBranchLeafWithinBudget : Bool :=
  childC006ConvergenceIrregularityBranchLeaves.all
    childC006ConvergenceIrregularityBranchLeafWithinBudget

/-- Checked C006 convergence/irregularity leaf-budget gate. -/
theorem childC006EveryConvergenceIrregularityBranchLeafWithinBudget_eq_true :
    childC006EveryConvergenceIrregularityBranchLeafWithinBudget = true :=
  rfl

/-- Completion gate for the C006 convergence/irregularity split. -/
structure ChildC006ConvergenceIrregularityBranchGate where
  childTask : String
  currentMachineStatus : String
  debtClassification : String
  branchFormulaName : String
  checkedProjectionName : String
  proofBearingConvergenceIrregularityBranchClaimed : Bool
  parentCompletionAllowed : Bool
  repoLocalIntegrationDebtCompletionResidue : Bool
  leafCount : Nat
  allLeavesWithinBudget : Bool
  routeLeaves : List ChildC006ConvergenceIrregularityBranchLeaf
  nextPublicMergeTarget : String

/--
S1-M-143-C006 result.

The convergence/irregularity branch now has a checked formula target, a checked
contrapositive projection from the full bidirectional criterion, and a local
`<=100` route ledger.  It does not prove the convergence/irregularity branch of
Wiener's criterion.
-/
def childC006ConvergenceIrregularityBranchGate :
    ChildC006ConvergenceIrregularityBranchGate where
  childTask := "S1-M-143-C006"
  currentMachineStatus :=
    "checked_convergence_irregularity_branch_target_and_budget_metadata_only"
  debtClassification := "formalization_debt"
  branchFormulaName := "WienerCriterionData.WienerConvergenceIrregularityBranchFormula"
  checkedProjectionName :=
    "WienerCriterionData.convergenceIrregularityBranch_of_wienerCriterionFormula"
  proofBearingConvergenceIrregularityBranchClaimed := false
  parentCompletionAllowed := false
  repoLocalIntegrationDebtCompletionResidue := false
  leafCount := childC006ConvergenceIrregularityBranchLeaves.length
  allLeavesWithinBudget := childC006EveryConvergenceIrregularityBranchLeafWithinBudget
  routeLeaves := childC006ConvergenceIrregularityBranchLeaves
  nextPublicMergeTarget :=
    "Serial integrator should merge the C006 convergence/irregularity branch \
    ledger into Docs/Stage1_Blueprint.md and synchronized todo surfaces \
    without marking THM-M-1153 complete."

/-- C006 records nine convergence/irregularity branch leaves. -/
theorem childC006ConvergenceIrregularityBranchGate_leafCount_eq :
    childC006ConvergenceIrregularityBranchGate.leafCount = 9 :=
  rfl

/-- C006 convergence/irregularity metadata satisfies the `<=100` leaf gate. -/
theorem childC006ConvergenceIrregularityBranchGate_allLeavesWithinBudget_eq_true :
    childC006ConvergenceIrregularityBranchGate.allLeavesWithinBudget = true :=
  rfl

/-- C006 does not claim a proof-bearing convergence/irregularity branch. -/
theorem childC006_proofBearingConvergenceIrregularityBranchClaimed_eq_false :
    childC006ConvergenceIrregularityBranchGate.proofBearingConvergenceIrregularityBranchClaimed =
      false :=
  rfl

/-- C006 does not allow parent completion from branch-target metadata alone. -/
theorem childC006_parentCompletionAllowed_eq_false :
    childC006ConvergenceIrregularityBranchGate.parentCompletionAllowed = false :=
  rfl

/-- C006 leaves no completed-state repo-local integration-debt residue. -/
theorem childC006_no_repoLocalIntegrationDebtCompletionResidue :
    childC006ConvergenceIrregularityBranchGate.repoLocalIntegrationDebtCompletionResidue = false :=
  rfl

/-! ## C007 external Lean 4 source-search gate -/

/--
One external-source search probe for child task `S1-M-143-C007`.

These rows are audit metadata.  They do not certify a proof of Wiener's
criterion, and they record the authentication blocker separately from the
absence of a located proof candidate.
-/
structure ChildC007ExternalSearchProbe where
  searchTerm : String
  searchedLean4Sources : String
  authenticationStatus : String
  locatedProofCandidate : Bool
  candidateRepository : String
  candidateCommit : String
  candidateModuleOrTheorem : String
  integrationAction : String

/--
External Lean 4 source-search probes required by C007.

The GitHub CLI in this execution environment was not logged in and GitHub's
unauthenticated code-search API was rate-limited.  Therefore the rows record an
authentication blocker and preserve the completion gate as open.  Web and
primary-source spot checks found no terminal Lean 4 Wiener-criterion proof to
pin in this pass.
-/
def childC007ExternalSearchProbes : List ChildC007ExternalSearchProbe := [
  {
    searchTerm := "WienerCriterion"
    searchedLean4Sources :=
      "repo-local Lean tree, web/GitHub primary-source search, GitHub code API attempt"
    authenticationStatus :=
      "blocked: `gh auth status` reports no logged-in GitHub host; code API rate-limited"
    locatedProofCandidate := false
    candidateRepository := ""
    candidateCommit := ""
    candidateModuleOrTheorem := ""
    integrationAction :=
      "No pin/import/check action available; keep as formalization_debt."
  },
  {
    searchTerm := "Newtonian capacity"
    searchedLean4Sources :=
      "repo-local Lean tree, mathlib anchor list, web/GitHub primary-source search, GitHub code API attempt"
    authenticationStatus :=
      "blocked: `gh auth status` reports no logged-in GitHub host; code API rate-limited"
    locatedProofCandidate := false
    candidateRepository := ""
    candidateCommit := ""
    candidateModuleOrTheorem := ""
    integrationAction :=
      "No concrete Lean 4 Newtonian-capacity API was located for this slot."
  },
  {
    searchTerm := "Perron solution"
    searchedLean4Sources :=
      "repo-local Lean tree, web/GitHub primary-source search, GitHub code API attempt"
    authenticationStatus :=
      "blocked: `gh auth status` reports no logged-in GitHub host; code API rate-limited"
    locatedProofCandidate := false
    candidateRepository := ""
    candidateCommit := ""
    candidateModuleOrTheorem := ""
    integrationAction :=
      "No Perron-solution proof candidate was located; keep regularity model abstract."
  },
  {
    searchTerm := "regular boundary point"
    searchedLean4Sources :=
      "repo-local Lean tree, web/GitHub primary-source search, GitHub code API attempt"
    authenticationStatus :=
      "blocked: `gh auth status` reports no logged-in GitHub host; code API rate-limited"
    locatedProofCandidate := false
    candidateRepository := ""
    candidateCommit := ""
    candidateModuleOrTheorem := ""
    integrationAction :=
      "No terminal Lean 4 regular-boundary-point theorem was found for this Wiener slot."
  }
]

/-- C007 records the four required external-search probes. -/
theorem childC007ExternalSearchProbes_length :
    childC007ExternalSearchProbes.length = 4 :=
  rfl

/-- Completion gate for the C007 external-source audit. -/
structure ChildC007ExternalSearchGate where
  childTask : String
  currentMachineStatus : String
  authenticatedSearchCompleted : Bool
  externalProofLocated : Bool
  externalProofPinnedImportedChecked : Bool
  parentCompletionAllowed : Bool
  repoLocalIntegrationDebtCompletionResidue : Bool
  probes : List ChildC007ExternalSearchProbe
  nextAction : String

/--
S1-M-143-C007 result.

The child audit did not locate a Lean 4 proof to pin, and the environment did
not provide authenticated GitHub search.  This gate therefore blocks any
completion claim and records the remaining action as an authenticated rerun or
an explicit integration blocker if a proof candidate later appears.
-/
def childC007ExternalSearchGate : ChildC007ExternalSearchGate where
  childTask := "S1-M-143-C007"
  currentMachineStatus := "external_search_metadata_only_no_terminal_proof_claim"
  authenticatedSearchCompleted := false
  externalProofLocated := false
  externalProofPinnedImportedChecked := false
  parentCompletionAllowed := false
  repoLocalIntegrationDebtCompletionResidue := false
  probes := childC007ExternalSearchProbes
  nextAction :=
    "Rerun authenticated GitHub/source search with credentials; if a proof is \
    found, pin/import/check it or record a concrete integration blocker before \
    any completion claim."

/-- C007 did not complete the authenticated-search gate in this environment. -/
theorem childC007_authenticatedSearchCompleted_eq_false :
    childC007ExternalSearchGate.authenticatedSearchCompleted = false :=
  rfl

/-- C007 located no external Lean 4 Wiener-criterion proof candidate. -/
theorem childC007_externalProofLocated_eq_false :
    childC007ExternalSearchGate.externalProofLocated = false :=
  rfl

/-- C007 did not pin/import/check an external proof. -/
theorem childC007_externalProofPinnedImportedChecked_eq_false :
    childC007ExternalSearchGate.externalProofPinnedImportedChecked = false :=
  rfl

/-- C007 does not allow parent completion from search metadata. -/
theorem childC007_parentCompletionAllowed_eq_false :
    childC007ExternalSearchGate.parentCompletionAllowed = false :=
  rfl

/-- C007 leaves no completed-state repo-local integration-debt residue. -/
theorem childC007_no_repoLocalIntegrationDebtCompletionResidue :
    childC007ExternalSearchGate.repoLocalIntegrationDebtCompletionResidue = false :=
  rfl

/-! ## C008 public backfill gate -/

/--
Completion gate for child task `S1-M-143-C008`, the serial public-document
backfill task.

The public-document task is intentionally blocked until the parent theorem has
machine closure.  The current artifact has checked statement-shape interfaces,
branch target ledgers, and audit metadata, but not a proof-bearing Wiener
criterion theorem.
-/
structure ChildC008PublicBackfillGate where
  childTask : String
  currentMachineStatus : String
  machineClosureObserved : Bool
  publicDocsEditedByChild : Bool
  parentCompletionAllowed : Bool
  repoLocalIntegrationDebtCompletionResidue : Bool
  requiredSerialTargets : List String
  nextAction : String

/--
S1-M-143-C008 result.

No public-document backfill is authorized yet, because the parent remains open
as formalization debt and the authenticated external-source gate is not closed.
-/
def childC008PublicBackfillGate : ChildC008PublicBackfillGate where
  childTask := "S1-M-143-C008"
  currentMachineStatus := "public_backfill_deferred_until_machine_closure"
  machineClosureObserved := false
  publicDocsEditedByChild := false
  parentCompletionAllowed := false
  repoLocalIntegrationDebtCompletionResidue := false
  requiredSerialTargets := [
    "Docs/Stage1_Blueprint.md",
    "Docs/todos_20260430.md",
    "README.md"
  ]
  nextAction :=
    "Serial integrator should not mark THM-M-1153 complete or backfill public \
    completion status until a proof-bearing local theorem, pinned mathlib \
    theorem, or imported external proof validates in this Lake closure and the \
    remaining C007 authenticated search gate is either closed or blocked by a \
    concrete integration reason."

/-- C008 observes no machine closure for the parent theorem. -/
theorem childC008_machineClosureObserved_eq_false :
    childC008PublicBackfillGate.machineClosureObserved = false :=
  rfl

/-- C008 made no public-document edits. -/
theorem childC008_publicDocsEditedByChild_eq_false :
    childC008PublicBackfillGate.publicDocsEditedByChild = false :=
  rfl

/-- C008 does not allow parent completion from metadata-only child ledgers. -/
theorem childC008_parentCompletionAllowed_eq_false :
    childC008PublicBackfillGate.parentCompletionAllowed = false :=
  rfl

/-- C008 leaves no completed-state repo-local integration-debt residue. -/
theorem childC008_no_repoLocalIntegrationDebtCompletionResidue :
    childC008PublicBackfillGate.repoLocalIntegrationDebtCompletionResidue = false :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic",
  "Mathlib.Analysis.InnerProductSpace.Harmonic.Constructions",
  "Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl",
  "Mathlib.Analysis.Complex.Harmonic.MeanValue",
  "Mathlib.Analysis.Complex.Harmonic.Poisson",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "InnerProductSpace.HarmonicAt",
  "InnerProductSpace.HarmonicOnNhd",
  "InnerProductSpace.harmonicOnNhd_const",
  "InnerProductSpace.HarmonicOnNhd.continuousOn",
  "InnerProductSpace.HarmonicOnNhd.add",
  "InnerProductSpace.HarmonicOnNhd.sub",
  "InnerProductSpace.HarmonicOnNhd.neg",
  "Laplacian",
  "LineDeriv.laplacianCLM",
  "SchwartzMap.laplacian_eq_sum",
  "SchwartzMap.integral_bilinear_laplacian_right_eq_left",
  "TemperedDistribution.laplacian_apply_apply",
  "TemperedDistributionHarmonic",
  "TemperedDistributionHarmonic.iff_forall_test_laplacian_zero",
  "WeakToClassicalHarmonicityBridge",
  "WeakToClassicalHarmonicityBridge.classical_of_weakHarmonicOn",
  "WeakToClassicalHarmonicityBridge.test_laplacian_zero_of_weakHarmonicOn",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "S1_M_143.HarmonicBarrier",
  "S1_M_143.HasHarmonicBarrier",
  "S1_M_143.DirichletPerronRegularityModel"
]

/--
Search terms that did not locate a terminal Wiener-criterion theorem or
Newtonian capacity object in local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Wiener criterion",
  "WienerCriterion",
  "regular boundary point",
  "boundary regular",
  "Dirichlet problem",
  "Newtonian capacity",
  "capacitary",
  "potential theory",
  "Perron solution",
  "harmonic measure"
]

end S1_M_143
end Stage1
end AwesomeTheorems
