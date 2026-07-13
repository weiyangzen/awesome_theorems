import Mathlib.Probability.BorelCantelli
import «ObligationTree»
import «Statement»

/-!
# THM-M-1007 proof execution

This module closes the truncation package, large-jump event independence, both
Borel--Cantelli bridges, finite-prefix convergence transport, and centering
normalization from the frozen proof tree. The bounded independent-series
necessity direction is not available in pinned mathlib, so no declaration of
the canonical root is made here.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_1007.Proof

universe u

/-- The scalar function whose postcomposition realizes the canonical truncation. -/
def truncationFunction (c : Real) (x : Real) : Real :=
  if |x| <= c then x else 0

/-- Scalar truncation is Borel measurable. -/
theorem measurable_truncationFunction (c : Real) :
    Measurable (truncationFunction c) := by
  exact Measurable.ite (measurableSet_le measurable_id.norm measurable_const)
    measurable_id measurable_const

/-- The canonical truncation of a measurable random variable is measurable. -/
theorem measurable_truncate {Omega : Type u} [MeasurableSpace Omega]
    {c : Real} {Z : Omega -> Real} (hZ : Measurable Z) :
    Measurable (Stage1Instances.THM_M_1007.truncate c Z) := by
  simpa [Stage1Instances.THM_M_1007.truncate, truncationFunction,
    Function.comp_def] using (measurable_truncationFunction c).comp hZ

/-- Canonical truncation is uniformly bounded, including for nonpositive
cutoffs where it is identically zero. -/
theorem norm_truncate_le {Omega : Type u} {c : Real} {Z : Omega -> Real}
    (omega : Omega) :
    ‖Stage1Instances.THM_M_1007.truncate c Z omega‖ <= |c| := by
  by_cases h : |Z omega| <= c
  · simpa [Stage1Instances.THM_M_1007.truncate, h, Real.norm_eq_abs] using
      h.trans (le_abs_self c)
  · simp [Stage1Instances.THM_M_1007.truncate, h]

/-- Bounded measurable truncations have every finite-measure `Lp` moment. -/
theorem memLp_truncate {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} [IsFiniteMeasure mu] {c : Real} {Z : Omega -> Real}
    (hZ : Measurable Z) {p : ENNReal} :
    MemLp (Stage1Instances.THM_M_1007.truncate c Z) p mu := by
  exact MemLp.of_bound (measurable_truncate hZ).aestronglyMeasurable |c|
    (Eventually.of_forall norm_truncate_le)

/-- In particular, a measurable truncation is integrable. -/
theorem integrable_truncate {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} [IsFiniteMeasure mu] {c : Real} {Z : Omega -> Real}
    (hZ : Measurable Z) :
    Integrable (Stage1Instances.THM_M_1007.truncate c Z) mu :=
  (memLp_truncate hZ (p := 1)).integrable (by simp)

/-- The strict large-jump event in the canonical target is measurable. -/
theorem measurableSet_largeJump {Omega : Type u} [MeasurableSpace Omega]
    {X : Nat -> Omega -> Real} (hX : forall n, Measurable (X n))
    (c : Real) (n : Nat) :
    MeasurableSet {omega | c < |X n omega|} := by
  exact measurableSet_lt measurable_const (hX n).norm

/-- Strict large-jump events inherit mutual independence from the random
variables. -/
theorem iIndepSet_largeJump {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : Nat -> Omega -> Real}
    (hX : forall n, Measurable (X n)) (hI : iIndepFun X mu) (c : Real) :
    iIndepSet (fun n => {omega | c < |X n omega|}) mu := by
  let s : Nat -> Set Omega := fun n => {omega | c < |X n omega|}
  have hs : forall n, MeasurableSet (s n) :=
    fun n => measurableSet_largeJump hX c n
  apply (iIndepSet_iff_meas_biInter hs).2
  intro t
  simpa [s] using hI.measure_inter_preimage_eq_mul t
    (sets := fun _ => {x : Real | c < |x|})
    (fun _ _ => measurableSet_lt measurable_const measurable_id.norm)

/-- Measurable coordinatewise truncation preserves independence. -/
theorem iIndepFun_truncate {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : Nat -> Omega -> Real}
    (hX : iIndepFun X mu) (c : Real) :
    iIndepFun (fun n => Stage1Instances.THM_M_1007.truncate c (X n)) mu := by
  simpa [Stage1Instances.THM_M_1007.truncate, truncationFunction,
    Function.comp_def] using
      hX.comp (fun _ : Nat => truncationFunction c)
        (fun _ : Nat => measurable_truncationFunction c)

/-- Real summability of event probabilities supplies the `ENNReal` hypothesis
of pinned Borel--Cantelli. -/
theorem largeJump_tsum_ne_top {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real)
    (hs : Summable (fun n => mu.real {omega | c < |X n omega|})) :
    (∑' n, mu {omega | c < |X n omega|}) ≠ (⊤ : ENNReal) := by
  simpa [ofReal_measureReal] using
    (Summable.tsum_ofReal_ne_top
      (f := fun n => mu.real {omega | c < |X n omega|}) hs)

/-- The first three-series condition implies that large jumps occur only
finitely often, almost surely. -/
theorem ae_eventually_no_largeJump {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real)
    (hs : Summable (fun n => mu.real {omega | c < |X n omega|})) :
    ∀ᵐ omega ∂mu, ∀ᶠ n in atTop, ¬ c < |X n omega| := by
  simpa only [Set.mem_setOf_eq] using
    (ae_eventually_notMem (largeJump_tsum_ne_top mu X c hs))

/-- Conversely, eventual absence of independent large jumps forces their real
probabilities to be summable. This is the contrapositive of pinned second
Borel--Cantelli. -/
theorem summable_largeJump_of_ae_eventually_no_largeJump
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real)
    (hX : forall n, Measurable (X n)) (hI : iIndepFun X mu)
    (hevent : ∀ᵐ omega ∂mu, ∀ᶠ n in atTop, ¬ c < |X n omega|) :
    Summable (fun n => mu.real {omega | c < |X n omega|}) := by
  let s : Nat -> Set Omega := fun n => {omega | c < |X n omega|}
  have hnotfreq : ∀ᵐ omega ∂mu, ¬ ∃ᶠ n in atTop, omega ∈ s n := by
    filter_upwards [hevent] with omega homega
    exact not_frequently.mpr homega
  have hlimsup0 : mu (limsup s atTop) = 0 := by
    rw [measure_eq_zero_iff_ae_notMem]
    filter_upwards [hnotfreq] with omega homega
    simpa [mem_limsup_iff_frequently_mem] using homega
  have htsum_ne_top : (∑' n, mu (s n)) ≠ (⊤ : ENNReal) := by
    intro htop
    have hone := measure_limsup_eq_one
      (μ := mu) (s := s)
      (fun n => measurableSet_largeJump hX c n)
      (iIndepSet_largeJump hX hI c) htop
    rw [hlimsup0] at hone
    norm_num at hone
  have hsum_toReal : Summable (fun n => ENNReal.toReal (mu (s n))) :=
    ENNReal.summable_toReal htsum_ne_top
  simpa [s, measureReal_def] using hsum_toReal

/-- Natural partial-sum convergence makes the terms tend to zero, so at every
positive cutoff large jumps eventually disappear. -/
theorem ae_eventually_no_largeJump_of_seriesConverges
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real) (c : Real) (hc : 0 < c)
    (hconv : ∀ᵐ omega ∂mu,
      Stage1Instances.THM_M_1007.SeriesConverges (fun n => X n omega)) :
    ∀ᵐ omega ∂mu, ∀ᶠ n in atTop, ¬ c < |X n omega| := by
  filter_upwards [hconv] with omega hseries
  obtain ⟨l, hl⟩ := hseries
  have hterm : Tendsto (fun n => X n omega) atTop (nhds 0) := by
    have hsucc := (tendsto_add_atTop_iff_nat 1).mpr hl
    have hdiff := hsucc.sub hl
    have heq : (fun n => X n omega) =ᶠ[atTop]
        (fun n => (∑ i ∈ Finset.range (n + 1), X i omega) -
          ∑ i ∈ Finset.range n, X i omega) := by
      filter_upwards with n
      rw [Finset.sum_range_succ]
      ring
    simpa using hdiff.congr' heq.symm
  have hnorm : Tendsto (fun n => |X n omega|) atTop (nhds 0) := by
    simpa [Real.norm_eq_abs] using hterm.norm
  have hev : ∀ᶠ n in atTop, |X n omega| < c :=
    (tendsto_order.1 hnorm).2 c hc
  exact hev.mono fun _ hn => not_lt_of_ge hn.le

/-- The necessity large-jump condition, with no extra premise beyond the
canonical target interface. -/
theorem summable_largeJump_of_seriesConverges
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real) (hc : 0 < c)
    (hX : forall n, Measurable (X n)) (hI : iIndepFun X mu)
    (hconv : ∀ᵐ omega ∂mu,
      Stage1Instances.THM_M_1007.SeriesConverges (fun n => X n omega)) :
    Summable (fun n => mu.real {omega | c < |X n omega|}) :=
  summable_largeJump_of_ae_eventually_no_largeJump mu X c hX hI
    (ae_eventually_no_largeJump_of_seriesConverges mu X c hc hconv)

/-- Eventual absence of large jumps makes the original and truncated terms
eventually identical, pointwise. -/
theorem eventuallyEq_truncate {Omega : Type u} (X : Nat -> Omega -> Real)
    (c : Real) (omega : Omega)
    (h : ∀ᶠ n in atTop, ¬ c < |X n omega|) :
    (fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega) =ᶠ[atTop]
      (fun n => X n omega) := by
  filter_upwards [h] with n hn
  simp [Stage1Instances.THM_M_1007.truncate, not_lt.mp hn]

/-- Changing finitely many terms preserves convergence of natural partial
sums, including conditionally convergent real series. -/
theorem seriesConverges_iff_of_eventuallyEq {a b : Nat -> Real}
    (h : a =ᶠ[atTop] b) :
    Stage1Instances.THM_M_1007.SeriesConverges a <->
      Stage1Instances.THM_M_1007.SeriesConverges b := by
  obtain ⟨k, hk⟩ := eventually_atTop.1 h
  let d : Real := (∑ n ∈ Finset.range k, b n) -
    ∑ n ∈ Finset.range k, a n
  have hsum : (fun N => ∑ n ∈ Finset.range N, b n) =ᶠ[atTop]
      (fun N => (∑ n ∈ Finset.range N, a n) + d) := by
    filter_upwards [eventually_ge_atTop k] with N hN
    rw [← Finset.sum_range_add_sum_Ico b hN,
      ← Finset.sum_range_add_sum_Ico a hN]
    have htail : (∑ n ∈ Finset.Ico k N, b n) =
        ∑ n ∈ Finset.Ico k N, a n :=
      Finset.sum_congr rfl fun n hn =>
        (hk n (Finset.mem_Ico.mp hn).1).symm
    rw [htail]
    dsimp [d]
    ring
  constructor
  · rintro ⟨l, hl⟩
    exact ⟨l + d, (hl.add_const d).congr' hsum.symm⟩
  · rintro ⟨l, hl⟩
    refine ⟨l - d, ?_⟩
    have ht := hl.add_const (-d)
    have heq : (fun N => ∑ n ∈ Finset.range N, a n) =ᶠ[atTop]
        (fun N => (∑ n ∈ Finset.range N, b n) + (-d)) := by
      filter_upwards [hsum] with N hN
      rw [hN]
      ring
    exact ht.congr' heq.symm

/-- Under the summable-large-jump condition, the original and truncated
series converge on exactly the same almost-sure set. -/
theorem ae_seriesConverges_truncate_iff_of_summable_largeJump
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real)
    (hs : Summable (fun n => mu.real {omega | c < |X n omega|})) :
    (∀ᵐ omega ∂mu, Stage1Instances.THM_M_1007.SeriesConverges
      (fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega)) <->
      (∀ᵐ omega ∂mu, Stage1Instances.THM_M_1007.SeriesConverges
        (fun n => X n omega)) := by
  have hevent := ae_eventually_no_largeJump mu X c hs
  constructor <;> intro hconv
  · filter_upwards [hevent, hconv] with omega hlarge hseries
    exact (seriesConverges_iff_of_eventuallyEq
      (eventuallyEq_truncate X c omega hlarge)).1 hseries
  · filter_upwards [hevent, hconv] with omega hlarge hseries
    exact (seriesConverges_iff_of_eventuallyEq
      (eventuallyEq_truncate X c omega hlarge)).2 hseries

/-- Centered canonical truncation. -/
def centeredTruncate [MeasurableSpace Omega] (mu : Measure Omega)
    (c : Real) (Z : Omega -> Real) (omega : Omega) : Real :=
  Stage1Instances.THM_M_1007.truncate c Z omega -
    integral mu (Stage1Instances.THM_M_1007.truncate c Z)

/-- Scalar postcomposition realizing centered truncation. -/
def centeredTruncationFunction [MeasurableSpace Omega] (mu : Measure Omega)
    (c : Real) (Z : Omega -> Real) (x : Real) : Real :=
  truncationFunction c x -
    integral mu (Stage1Instances.THM_M_1007.truncate c Z)

/-- Centering splits a truncation into its centered and deterministic parts. -/
theorem truncate_eq_centeredTruncate_add_mean {Omega : Type u}
    [MeasurableSpace Omega] (mu : Measure Omega) (c : Real)
    (Z : Omega -> Real) (omega : Omega) :
    Stage1Instances.THM_M_1007.truncate c Z omega =
      centeredTruncate mu c Z omega +
        integral mu (Stage1Instances.THM_M_1007.truncate c Z) := by
  simp [centeredTruncate]

theorem measurable_centeredTruncationFunction [MeasurableSpace Omega]
    (mu : Measure Omega) (c : Real) (Z : Omega -> Real) :
    Measurable (centeredTruncationFunction mu c Z) := by
  exact (measurable_truncationFunction c).sub measurable_const

theorem measurable_centeredTruncate {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {c : Real} {Z : Omega -> Real}
    (hZ : Measurable Z) :
    Measurable (centeredTruncate mu c Z) := by
  exact (measurable_truncate hZ).sub measurable_const

/-- Coordinatewise centering preserves the truncated family's independence. -/
theorem iIndepFun_centeredTruncate {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : Nat -> Omega -> Real}
    (hX : iIndepFun X mu) (c : Real) :
    iIndepFun (fun n => centeredTruncate mu c (X n)) mu := by
  simpa [centeredTruncate, centeredTruncationFunction,
    Stage1Instances.THM_M_1007.truncate, truncationFunction,
    Function.comp_def] using
      hX.comp (fun n : Nat => centeredTruncationFunction mu c (X n))
        (fun n : Nat => measurable_centeredTruncationFunction mu c (X n))

/-- Centering by the integral gives a zero-mean truncation. -/
theorem integral_centeredTruncate {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {c : Real} {Z : Omega -> Real} (hZ : Measurable Z) :
    integral mu (centeredTruncate mu c Z) = 0 := by
  change (∫ omega, Stage1Instances.THM_M_1007.truncate c Z omega -
    integral mu (Stage1Instances.THM_M_1007.truncate c Z) ∂mu) = 0
  rw [integral_sub (integrable_truncate hZ) (integrable_const _)]
  rw [integral_const]
  rw [probReal_univ, one_smul, sub_self]

/-- Centering doubles at most the canonical truncation bound. -/
theorem norm_centeredTruncate_le {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {c : Real} {Z : Omega -> Real} (omega : Omega) :
    ‖centeredTruncate mu c Z omega‖ <= 2 * |c| := by
  calc
    ‖centeredTruncate mu c Z omega‖ <=
        ‖Stage1Instances.THM_M_1007.truncate c Z omega‖ +
          ‖integral mu (Stage1Instances.THM_M_1007.truncate c Z)‖ := by
      exact norm_sub_le _ _
    _ <= |c| + |c| := add_le_add (norm_truncate_le omega) (by
      simpa [probReal_univ] using
        (norm_integral_le_of_norm_le_const
          (μ := mu) (f := Stage1Instances.THM_M_1007.truncate c Z)
          (C := |c|) (Eventually.of_forall norm_truncate_le)))
    _ = 2 * |c| := by ring

theorem memLp_centeredTruncate {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {c : Real} {Z : Omega -> Real} (hZ : Measurable Z) {p : ENNReal} :
    MemLp (centeredTruncate mu c Z) p mu := by
  exact MemLp.of_bound (measurable_centeredTruncate hZ).aestronglyMeasurable
    (2 * |c|) (Eventually.of_forall (norm_centeredTruncate_le mu))

/-- Centering does not change the variance of a measurable truncation. -/
theorem variance_centeredTruncate {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {c : Real} {Z : Omega -> Real} (hZ : Measurable Z) :
    variance (centeredTruncate mu c Z) mu =
      variance (Stage1Instances.THM_M_1007.truncate c Z) mu := by
  exact variance_sub_const (measurable_truncate hZ).aestronglyMeasurable _

/-- A convergent deterministic correction can be removed from or added to a
natural-order series without changing convergence. -/
theorem seriesConverges_add_iff {a b : Nat -> Real}
    (hb : Stage1Instances.THM_M_1007.SeriesConverges b) :
    Stage1Instances.THM_M_1007.SeriesConverges (fun n => a n + b n) <->
      Stage1Instances.THM_M_1007.SeriesConverges a := by
  rcases hb with ⟨lb, hb⟩
  constructor
  · rintro ⟨lab, hab⟩
    refine ⟨lab - lb, ?_⟩
    have heq : (fun N => ∑ n ∈ Finset.range N, a n) =
        fun N => (∑ n ∈ Finset.range N, (a n + b n)) -
          (∑ n ∈ Finset.range N, b n) := by
      funext N
      rw [Finset.sum_add_distrib]
      abel
    rw [heq]
    exact hab.sub hb
  · rintro ⟨la, ha⟩
    refine ⟨la + lb, ?_⟩
    simpa only [Finset.sum_add_distrib] using ha.add hb

/-- When the deterministic mean series converges, the centered and uncentered
truncated series converge together. -/
theorem seriesConverges_centered_iff
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real)
    (c : Real) (omega : Omega)
    (hmeans : Stage1Instances.THM_M_1007.SeriesConverges
      (fun n => integral mu
        (Stage1Instances.THM_M_1007.truncate c (X n)))) :
    Stage1Instances.THM_M_1007.SeriesConverges
        (fun n => centeredTruncate mu c (X n) omega) <->
      Stage1Instances.THM_M_1007.SeriesConverges
        (fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega) := by
  have hneg : Stage1Instances.THM_M_1007.SeriesConverges
      (fun n => - integral mu
        (Stage1Instances.THM_M_1007.truncate c (X n))) := by
    rcases hmeans with ⟨l, hl⟩
    refine ⟨-l, ?_⟩
    simpa only [Finset.sum_neg_distrib] using hl.neg
  simpa only [centeredTruncate, sub_eq_add_neg] using
    (seriesConverges_add_iff
      (a := fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega)
      hneg)

/-- On a probability space the `L^1` norm is bounded by the `L^2` norm. -/
lemma eLpNorm_one_le_two {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} [IsProbabilityMeasure mu] {f : Omega -> Real}
    (hf : AEStronglyMeasurable f mu) :
    eLpNorm f 1 mu <= eLpNorm f 2 mu := by
  exact eLpNorm_le_eLpNorm_of_exponent_le (by norm_num) hf

/-- An `L^2` second-moment bound gives the `L^1` bound needed by the
martingale convergence theorem. -/
lemma eLpNorm_one_le_sqrt_integral_sq {Omega : Type u}
    [MeasurableSpace Omega] {mu : Measure Omega} [IsProbabilityMeasure mu]
    {f : Omega -> Real} (hf : MemLp f 2 mu) {C : Real}
    (h_int_sq : integral mu (fun x => ‖f x‖ ^ (2 : Real)) <= C) :
    eLpNorm f 1 mu <= ENNReal.ofReal (Real.sqrt C) := by
  calc
    eLpNorm f 1 mu <= eLpNorm f 2 mu :=
      eLpNorm_one_le_two hf.aestronglyMeasurable
    _ = ENNReal.ofReal
        ((integral mu (fun x => ‖f x‖ ^ (2 : Real))) ^ ((2 : Real) : Real)⁻¹) := by
      rw [hf.eLpNorm_eq_integral_rpow_norm (by norm_num) (by norm_num)]
      norm_num
    _ = ENNReal.ofReal (Real.sqrt
        (integral mu (fun x => ‖f x‖ ^ (2 : Real)))) := by
      rw [Real.sqrt_eq_rpow]
      norm_num
    _ <= ENNReal.ofReal (Real.sqrt C) := by
      exact ENNReal.ofReal_le_ofReal (Real.sqrt_le_sqrt h_int_sq)

/-- Independent, centered, integrable variables whose partial sums are
uniformly `L^1` bounded converge almost surely. -/
theorem ae_tendsto_sum_of_indep_centered_L1bdd {Omega : Type u}
    [MeasurableSpace Omega] {mu : Measure Omega} [IsProbabilityMeasure mu]
    {Z : Nat -> Omega -> Real}
    (hZ_sm : forall n, StronglyMeasurable (Z n))
    (hZ_indep : iIndepFun (m := fun _ => inferInstance) Z mu)
    (hZ_mean : forall n, integral mu (Z n) = 0)
    (hZ_int : forall n, Integrable (Z n) mu) {R : NNReal}
    (hZ_L1_bdd : forall n,
      eLpNorm (fun omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) 1 mu <= (R : ENNReal)) :
    ∀ᵐ omega ∂mu, exists c,
      Tendsto (fun n => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) atTop (nhds c) := by
  set F := Filtration.natural (β := fun _ : Nat => Real) Z hZ_sm
  have sum_eq : forall n,
      (fun omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) =
        Finset.sum (Finset.range (n + 1)) Z := by
    intro n
    ext omega
    simp [Finset.sum_apply]
  have hS_int : forall n, Integrable
      (fun omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) mu := fun n =>
    integrable_finset_sum _ (fun k _ => hZ_int k)
  have hS_sm_m : forall n, StronglyMeasurable[F n]
      (fun omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) := by
    intro n
    rw [sum_eq]
    exact Finset.stronglyMeasurable_sum _ (fun k hk => by
      have hkn : k <= n := by
        have := Finset.mem_range.mp hk
        omega
      exact (Filtration.stronglyAdapted_natural hZ_sm k).mono (F.mono hkn))
  have hS_mart : Martingale
      (fun n omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) F mu := by
    apply martingale_nat (fun n => hS_sm_m n) hS_int
    intro i
    have heq_add :
        (fun omega => Finset.sum (Finset.range (i + 2))
          (fun k => Z k omega)) =
          (fun omega => Finset.sum (Finset.range (i + 1))
            (fun k => Z k omega)) + Z (i + 1) := by
      ext omega
      simp [Finset.sum_range_succ, Pi.add_apply]
    rw [heq_add]
    have hce := condExp_add (hS_int i) (hZ_int (i + 1))
      (F i : MeasurableSpace Omega)
    have hSi_ce :
        mu[(fun omega => Finset.sum (Finset.range (i + 1))
          (fun k => Z k omega)) | (F i : MeasurableSpace Omega)] =
          fun omega => Finset.sum (Finset.range (i + 1))
            (fun k => Z k omega) :=
      condExp_of_stronglyMeasurable (F.le i) (hS_sm_m i) (hS_int i)
    have hZi1_ce : mu[Z (i + 1) | (F i : MeasurableSpace Omega)] =ᵐ[mu]
        fun _ => (0 : Real) := by
      have h := hZ_indep.condExp_natural_ae_eq_of_lt hZ_sm
        (show i < i + 1 by omega)
      simpa [hZ_mean (i + 1)] using h
    filter_upwards [hce, hZi1_ce] with omega homega1 homega3
    simp only [Pi.add_apply] at homega1
    rw [hSi_ce] at homega1
    linarith
  exact hS_mart.submartingale.exists_ae_tendsto_of_bdd (R := R) hZ_L1_bdd

/-- Summable variances force almost-sure natural-order convergence of the
series of centered canonical truncations. -/
theorem ae_seriesConverges_centered_of_variance_summable {Omega : Type u}
    [MeasurableSpace Omega] {mu : Measure Omega} [IsProbabilityMeasure mu]
    {X : Nat -> Omega -> Real} (hX_meas : forall n, Measurable (X n))
    (hX_indep : iIndepFun X mu) {c : Real} (hc : 0 < c)
    (hvar : Summable (fun n =>
      variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu)) :
    ∀ᵐ omega ∂mu, Stage1Instances.THM_M_1007.SeriesConverges (fun n =>
      Stage1Instances.THM_M_1007.truncate c (X n) omega -
        integral mu (Stage1Instances.THM_M_1007.truncate c (X n))) := by
  let mean : Nat -> Real := fun n =>
    integral mu (Stage1Instances.THM_M_1007.truncate c (X n))
  let Z : Nat -> Omega -> Real := fun n omega =>
    Stage1Instances.THM_M_1007.truncate c (X n) omega - mean n
  have htrunc_sm : forall n, StronglyMeasurable
      (Stage1Instances.THM_M_1007.truncate c (X n)) := fun n =>
    (measurable_truncate (hX_meas n)).stronglyMeasurable
  have htrunc_norm : forall n omega,
      ‖Stage1Instances.THM_M_1007.truncate c (X n) omega‖ <= c := by
    intro n omega
    exact (norm_truncate_le (c := c) (Z := X n) omega).trans_eq
      (abs_of_pos hc)
  have hZ_sm : forall n, StronglyMeasurable (Z n) := fun n =>
    (htrunc_sm n).sub stronglyMeasurable_const
  have hZ_bdd : forall n omega, ‖Z n omega‖ <= 2 * c := by
    intro n omega
    have h1 := htrunc_norm n omega
    have h2 : ‖mean n‖ <= c :=
      calc
        ‖mean n‖ = ‖integral mu
            (Stage1Instances.THM_M_1007.truncate c (X n))‖ := rfl
        _ <= integral mu (fun omega =>
            ‖Stage1Instances.THM_M_1007.truncate c (X n) omega‖) :=
          norm_integral_le_integral_norm _
        _ <= integral mu (fun _ => c) :=
          integral_mono_of_nonneg (Eventually.of_forall fun _ => norm_nonneg _)
            (integrable_const c) (Eventually.of_forall fun omega => htrunc_norm n omega)
        _ = c := by simp
    calc
      ‖Z n omega‖ = ‖Stage1Instances.THM_M_1007.truncate c (X n) omega -
          mean n‖ := rfl
      _ <= ‖Stage1Instances.THM_M_1007.truncate c (X n) omega‖ +
          ‖mean n‖ := norm_sub_le _ _
      _ <= c + c := add_le_add h1 h2
      _ = 2 * c := by ring
  have hZ_int : forall n, Integrable (Z n) mu := fun n =>
    (memLp_top_of_bound (hZ_sm n).aestronglyMeasurable (2 * c)
      (Eventually.of_forall (hZ_bdd n))).integrable le_top
  have hZ_mean : forall n, integral mu (Z n) = 0 := by
    intro n
    simpa only [Z, mean] using
      integral_centeredTruncate mu (hX_meas n)
  have hZ_indep : iIndepFun (m := fun _ => inferInstance) Z mu := by
    simpa only [Z, mean] using iIndepFun_centeredTruncate hX_indep c
  have hZ_memLp : forall n, MemLp (Z n) 2 mu := fun n =>
    (memLp_top_of_bound (hZ_sm n).aestronglyMeasurable (2 * c)
      (Eventually.of_forall (hZ_bdd n))).mono_exponent le_top
  have hVar_eq : forall n, variance (Z n) mu =
      variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu := by
    intro n
    simpa only [Z, mean] using variance_centeredTruncate mu (hX_meas n)
  let C : Real := ∑' n,
    variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu
  have hR_bound : forall n,
      eLpNorm (fun omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) 1 mu <= ENNReal.ofReal (Real.sqrt C) := by
    intro n
    have hS_sm : StronglyMeasurable (fun omega =>
        Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)) := by
      have h := Finset.stronglyMeasurable_sum (Finset.range (n + 1))
        (fun k _ => hZ_sm k)
      convert h using 1
      ext omega
      simp [Finset.sum_apply]
    have hS_memLp : MemLp (fun omega =>
        Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)) 2 mu := by
      have hbdd : forall omega,
          ‖Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)‖ <=
            (n + 1) * (2 * c) := by
        intro omega
        calc
          ‖Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)‖ <=
              Finset.sum (Finset.range (n + 1)) (fun k => ‖Z k omega‖) :=
            norm_sum_le _ _
          _ <= Finset.sum (Finset.range (n + 1)) (fun _ => 2 * c) :=
            Finset.sum_le_sum (fun k _ => hZ_bdd k omega)
          _ = (n + 1) * (2 * c) := by simp [mul_comm]
      exact (memLp_top_of_bound hS_sm.aestronglyMeasurable
        ((n + 1) * (2 * c)) (Eventually.of_forall hbdd)).mono_exponent le_top
    have h_int_bound : integral mu (fun omega =>
        ‖Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)‖ ^
          (2 : Real)) <= C := by
      have hconv : (fun omega =>
          ‖Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)‖ ^
            (2 : Real)) =
          fun omega => (Finset.sum (Finset.range (n + 1))
            (fun k => Z k omega)) ^ 2 := by
        ext omega
        rw [show (2 : Real) = (2 : Nat) by norm_num, Real.rpow_natCast,
          sq, sq, Real.norm_eq_abs, abs_mul_abs_self]
      rw [hconv]
      have hmean_sum : integral mu (fun omega =>
          Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)) = 0 := by
        rw [integral_finset_sum _ (fun k _ => hZ_int k)]
        exact Finset.sum_eq_zero (fun k _ => hZ_mean k)
      have haem : AEMeasurable (fun omega =>
          Finset.sum (Finset.range (n + 1)) (fun k => Z k omega)) mu :=
        hS_sm.aestronglyMeasurable.aemeasurable
      rw [← variance_of_integral_eq_zero haem hmean_sum]
      have hpw : Set.Pairwise (↑(Finset.range (n + 1)))
          (fun i j => (Z i) ⟂ᵢ[mu] (Z j)) :=
        fun i _ j _ hij => hZ_indep.indepFun hij
      rw [show (fun omega => Finset.sum (Finset.range (n + 1))
          (fun k => Z k omega)) = Finset.sum (Finset.range (n + 1)) Z by
        ext omega
        simp [Finset.sum_apply]]
      rw [IndepFun.variance_sum (fun k _ => hZ_memLp k) hpw]
      calc
        Finset.sum (Finset.range (n + 1)) (fun k => variance (Z k) mu) =
            Finset.sum (Finset.range (n + 1)) (fun k =>
              variance (Stage1Instances.THM_M_1007.truncate c (X k)) mu) :=
          Finset.sum_congr rfl (fun k _ => hVar_eq k)
        _ <= C := hvar.sum_le_tsum _ (fun k _ => variance_nonneg _ _)
    exact eLpNorm_one_le_sqrt_integral_sq hS_memLp h_int_bound
  have hR_nn : (0 : Real) <= Real.sqrt C := Real.sqrt_nonneg _
  let R : NNReal := ⟨Real.sqrt C, hR_nn⟩
  have hR_eq : (R : ENNReal) = ENNReal.ofReal (Real.sqrt C) := by
    simp [R, ENNReal.ofReal_eq_coe_nnreal hR_nn]
  have hR_bdd : forall n,
      eLpNorm (fun omega => Finset.sum (Finset.range (n + 1))
        (fun k => Z k omega)) 1 mu <= (R : ENNReal) := by
    intro n
    rw [hR_eq]
    exact hR_bound n
  have h := ae_tendsto_sum_of_indep_centered_L1bdd hZ_sm hZ_indep
    hZ_mean hZ_int hR_bdd
  filter_upwards [h] with omega homega
  obtain ⟨l, hl⟩ := homega
  exact ⟨l, by
    simpa only [Z, mean] using
      (Filter.tendsto_add_atTop_iff_nat 1).mp hl⟩

/-- Convergent means plus summable variances imply almost-sure convergence of
the canonical truncations. -/
theorem ae_seriesConverges_truncate_of_mean_variance {Omega : Type u}
    [MeasurableSpace Omega] {mu : Measure Omega} [IsProbabilityMeasure mu]
    {X : Nat -> Omega -> Real} (hX_meas : forall n, Measurable (X n))
    (hX_indep : iIndepFun X mu) {c : Real} (hc : 0 < c)
    (hmean : Stage1Instances.THM_M_1007.SeriesConverges (fun n =>
      integral mu (Stage1Instances.THM_M_1007.truncate c (X n))))
    (hvar : Summable (fun n =>
      variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu)) :
    ∀ᵐ omega ∂mu, Stage1Instances.THM_M_1007.SeriesConverges (fun n =>
      Stage1Instances.THM_M_1007.truncate c (X n) omega) := by
  filter_upwards [ae_seriesConverges_centered_of_variance_summable
    hX_meas hX_indep hc hvar] with omega hcenter
  exact (seriesConverges_centered_iff mu X c omega hmean).mp (by
    simpa only [centeredTruncate] using hcenter)

/-- Exact sufficiency direction of the frozen three-series statement. -/
theorem threeSeries_sufficiency {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real) (hc : 0 < c)
    (hX : forall n, Measurable (X n)) (hIndep : iIndepFun X mu)
    (hconditions :
      Summable (fun n => mu.real {omega | c < |X n omega|}) /\
      Stage1Instances.THM_M_1007.SeriesConverges (fun n =>
        integral mu (Stage1Instances.THM_M_1007.truncate c (X n))) /\
      Summable (fun n =>
        variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu)) :
    ∀ᵐ omega ∂mu,
      Stage1Instances.THM_M_1007.SeriesConverges (fun n => X n omega) := by
  obtain ⟨hjump, hmean, hvar⟩ := hconditions
  exact (ae_seriesConverges_truncate_iff_of_summable_largeJump mu X c hjump).mp
    (ae_seriesConverges_truncate_of_mean_variance hX hIndep hc hmean hvar)

/-- Exact wrapper at the frozen obligation-tree sufficiency type. -/
theorem obligationTree_sufficiency :
    Stage1Instances.THM_M_1007.ObligationTree.Sufficiency.{u} := by
  intro Omega _ mu _ X c hc hX hIndep hconditions
  exact threeSeries_sufficiency mu X c hc hX hIndep hconditions

#print axioms measurable_truncationFunction
#print axioms measurable_truncate
#print axioms norm_truncate_le
#print axioms memLp_truncate
#print axioms integrable_truncate
#print axioms measurableSet_largeJump
#print axioms iIndepSet_largeJump
#print axioms iIndepFun_truncate
#print axioms largeJump_tsum_ne_top
#print axioms ae_eventually_no_largeJump
#print axioms summable_largeJump_of_ae_eventually_no_largeJump
#print axioms ae_eventually_no_largeJump_of_seriesConverges
#print axioms summable_largeJump_of_seriesConverges
#print axioms eventuallyEq_truncate
#print axioms seriesConverges_iff_of_eventuallyEq
#print axioms ae_seriesConverges_truncate_iff_of_summable_largeJump
#print axioms truncate_eq_centeredTruncate_add_mean
#print axioms measurable_centeredTruncationFunction
#print axioms measurable_centeredTruncate
#print axioms iIndepFun_centeredTruncate
#print axioms integral_centeredTruncate
#print axioms norm_centeredTruncate_le
#print axioms memLp_centeredTruncate
#print axioms variance_centeredTruncate
#print axioms seriesConverges_add_iff
#print axioms seriesConverges_centered_iff
#print axioms eLpNorm_one_le_two
#print axioms eLpNorm_one_le_sqrt_integral_sq
#print axioms ae_tendsto_sum_of_indep_centered_L1bdd
#print axioms ae_seriesConverges_centered_of_variance_summable
#print axioms ae_seriesConverges_truncate_of_mean_variance
#print axioms threeSeries_sufficiency
#print axioms obligationTree_sufficiency

end Stage1Instances.THM_M_1007.Proof
