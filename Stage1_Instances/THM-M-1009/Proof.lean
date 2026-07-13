import Statement
import ObligationTree

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

universe u

namespace Stage1Instances.THM_M_1009

/-- The finite counting random variable used in the second-moment argument. -/
def eventCount {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega) : Real :=
  Finset.sum (Finset.range n) fun k => (A k).indicator (fun _ => 1) omega

theorem partialEventMass_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) :
    0 <= partialEventMass mu A n := by
  exact Finset.sum_nonneg fun _ _ => measureReal_nonneg

theorem pairwiseEventMass_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) :
    0 <= pairwiseEventMass mu A n := by
  exact Finset.sum_nonneg fun _ _ =>
    Finset.sum_nonneg fun _ _ => measureReal_nonneg

theorem pairwiseEventMass_pos_of_partialEventMass_pos
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat)
    (h : 0 < partialEventMass mu A n) :
    0 < pairwiseEventMass mu A n := by
  classical
  unfold partialEventMass at h
  rcases (Finset.sum_pos_iff_of_nonneg
    (fun _ _ => measureReal_nonneg)).1 h with ⟨i, hi, hAi⟩
  unfold pairwiseEventMass
  refine Finset.sum_pos' (fun _ _ =>
    Finset.sum_nonneg fun _ _ => measureReal_nonneg) ⟨i, hi, ?_⟩
  refine Finset.sum_pos' (fun _ _ => measureReal_nonneg) ⟨i, hi, ?_⟩
  simpa [Set.inter_self] using hAi

theorem eventMassRatio_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) :
    0 <= eventMassRatio mu A n := by
  exact div_nonneg (sq_nonneg _) (pairwiseEventMass_nonneg mu A n)

theorem measurable_eventCount {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    Measurable (eventCount A n) := by
  unfold eventCount
  exact Finset.measurable_fun_sum _ fun k _ => measurable_const.indicator (hA k)

theorem integrable_eventCount {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    Integrable (eventCount A n) mu := by
  unfold eventCount
  exact integrable_finset_sum _ fun k _ => (integrable_const 1).indicator (hA k)

theorem integral_eventCount {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    (∫ omega, eventCount A n omega ∂mu) = partialEventMass mu A n := by
  unfold eventCount partialEventMass
  rw [integral_finset_sum]
  · exact Finset.sum_congr rfl fun k _ => integral_indicator_one (hA k)
  · exact fun k _ => (integrable_const 1).indicator (hA k)

theorem eventCount_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega) :
    0 <= eventCount A n omega := by
  refine Finset.sum_nonneg fun k _ => ?_
  by_cases h : omega ∈ A k
  · simp [Set.indicator_of_mem h]
  · simp [Set.indicator_of_notMem h]

theorem eventCount_sq_eq {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega) :
    (eventCount A n omega) ^ 2 =
      Finset.sum (Finset.range n) fun i =>
        Finset.sum (Finset.range n) fun j =>
          (A i ∩ A j).indicator (fun _ => (1 : Real)) omega := by
  classical
  unfold eventCount
  rw [pow_two, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i hi
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  by_cases hi' : omega ∈ A i <;> by_cases hj' : omega ∈ A j <;>
    simp [Set.indicator_of_mem, Set.indicator_of_notMem, hi', hj']

theorem integrable_eventCount_sq {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    Integrable (fun omega => (eventCount A n omega) ^ 2) mu := by
  apply Integrable.congr (integrable_finset_sum _ fun i _ =>
    integrable_finset_sum _ fun j _ =>
      (integrable_const 1).indicator ((hA i).inter (hA j)))
  exact Filter.Eventually.of_forall fun omega => (eventCount_sq_eq A n omega).symm

theorem integral_eventCount_sq {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    (∫ omega, (eventCount A n omega) ^ 2 ∂mu) = pairwiseEventMass mu A n := by
  classical
  simp_rw [eventCount_sq_eq A n]
  unfold pairwiseEventMass
  rw [integral_finset_sum]
  · apply Finset.sum_congr rfl
    intro i hi
    rw [integral_finset_sum]
    · exact Finset.sum_congr rfl fun j _ => integral_indicator_one ((hA i).inter (hA j))
    · exact fun j _ => (integrable_const 1).indicator ((hA i).inter (hA j))
  · intro i hi
    exact integrable_finset_sum _ fun j _ =>
      (integrable_const 1).indicator ((hA i).inter (hA j))

/-- The union of the first `n` events. -/
def eventUnion {Omega : Type u} (A : Nat -> Set Omega) (n : Nat) : Set Omega :=
  ⋃ k ∈ Finset.range n, A k

theorem measurable_eventUnion {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    MeasurableSet (eventUnion A n) := by
  exact Finset.measurableSet_biUnion _ fun k _ => hA k

theorem eventCount_zero_outside_eventUnion {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega)
    (homega : omega ∉ eventUnion A n) : eventCount A n omega = 0 := by
  classical
  unfold eventCount eventUnion at *
  simp only [Set.mem_iUnion, not_exists] at homega
  apply Finset.sum_eq_zero
  intro k hk
  simp [Set.indicator_of_notMem (homega k hk)]

/-- Finite Cauchy-Schwarz bound for a nonnegative function supported on `U`. -/
theorem finite_secondMoment_bound
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (X : Omega -> Real) (hX : Measurable X) (hX2 : Integrable (fun w => X w ^ 2) mu)
    (U : Set Omega) (hU : MeasurableSet U)
    (hzero : forall w, w ∉ U -> X w = 0)
    (hXnonneg : forall w, 0 <= X w) :
    (∫ w, X w ∂mu) ^ 2 <= mu.real U * (∫ w, X w ^ 2 ∂mu) := by
  have hXlp : MemLp X 2 mu :=
    (memLp_two_iff_integrable_sq hX.aestronglyMeasurable).2 hX2
  let oneU : Omega -> Real := U.indicator (fun _ => 1)
  have h1lp : MemLp oneU 2 mu :=
    memLp_indicator_const 2 hU 1 (Or.inr (measure_ne_top mu U))
  have hofreal : ENNReal.ofReal (2 : Real) = 2 := by norm_num
  have hone : ∀ᵐ w ∂mu, 0 <= oneU w := Filter.Eventually.of_forall fun w => by
    by_cases hw : w ∈ U <;>
      simp [oneU, Set.indicator_of_mem, Set.indicator_of_notMem, hw]
  have hxn : ∀ᵐ w ∂mu, 0 <= X w := Filter.Eventually.of_forall hXnonneg
  have hcs := integral_mul_le_Lp_mul_Lq_of_nonneg Real.HolderConjugate.two_two
      hxn hone (hofreal ▸ hXlp) (hofreal ▸ h1lp)
  have hmul : (fun w => X w * oneU w) = X := by
    funext w
    by_cases hw : w ∈ U
    · simp [oneU, Set.indicator_of_mem hw]
    · simp [oneU, Set.indicator_of_notMem hw, hzero w hw]
  rw [show (∫ w, X w * oneU w ∂mu) = ∫ w, X w ∂mu by rw [hmul], one_div] at hcs
  norm_num at hcs
  have hintU : (∫ w, oneU w ^ 2 ∂mu) = mu.real U := by
    rw [show (fun w => oneU w ^ 2) = oneU by
      funext w
      by_cases hw : w ∈ U <;>
        simp [oneU, Set.indicator_of_mem, Set.indicator_of_notMem, hw],
      show (∫ w, oneU w ∂mu) = mu.real U by exact integral_indicator_one hU]
  rw [hintU, ← Real.sqrt_eq_rpow, ← Real.sqrt_eq_rpow] at hcs
  have hsq : 0 <= (∫ w, X w ∂mu) := integral_nonneg hXnonneg
  have hdu : 0 <= (∫ w, X w ^ 2 ∂mu) := integral_nonneg fun w => sq_nonneg _
  have hmu : 0 <= mu.real U := measureReal_nonneg
  have hsqrtprod : 0 <= Real.sqrt (∫ w, X w ^ 2 ∂mu) * Real.sqrt (mu.real U) :=
    mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
  nlinarith [Real.sq_sqrt hdu, Real.sq_sqrt hmu, hsqrtprod]

theorem finite_eventMassRatio_le_eventUnion {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    eventMassRatio mu A n <= mu.real (eventUnion A n) := by
  have hb := finite_secondMoment_bound mu (eventCount A n)
    (measurable_eventCount A hA n) (integrable_eventCount_sq mu A hA n)
    (eventUnion A n) (measurable_eventUnion A hA n)
    (eventCount_zero_outside_eventUnion A n) (eventCount_nonneg A n)
  rw [integral_eventCount mu A hA n, integral_eventCount_sq mu A hA n] at hb
  by_cases hs : 0 < partialEventMass mu A n
  · have hd := pairwiseEventMass_pos_of_partialEventMass_pos mu A n hs
    rw [eventMassRatio, div_le_iff₀ hd]
    simpa [mul_comm] using hb
  · have hs0 : partialEventMass mu A n = 0 :=
      le_antisymm (not_lt.1 hs) (partialEventMass_nonneg mu A n)
    simp [eventMassRatio, hs0, measureReal_nonneg]

theorem eventMassRatio_le_one {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    eventMassRatio mu A n <= 1 := by
  exact (finite_eventMassRatio_le_eventUnion mu A hA n).trans <|
    (measureReal_mono (μ := mu) (s₁ := eventUnion A n) (s₂ := Set.univ)
      (Set.subset_univ _) (measure_ne_top mu Set.univ)).trans_eq probReal_univ

/-- The measurable union of all events at indices at least `m`. -/
def eventTail {Omega : Type u} (A : Nat -> Set Omega) (m : Nat) : Set Omega :=
  ⋃ k : Nat, A (m + k)

def windowEventCount {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (m n : Nat) (omega : Omega) : Real :=
  Finset.sum (Finset.Ico m n) fun k => (A k).indicator (fun _ => 1) omega

theorem measurable_eventTail {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (m : Nat) :
    MeasurableSet (eventTail A m) := by
  exact MeasurableSet.iUnion fun k => hA _

theorem windowEventCount_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (m n : Nat) (omega : Omega) :
    0 <= windowEventCount A m n omega := by
  refine Finset.sum_nonneg fun k _ => ?_
  by_cases h : omega ∈ A k <;>
    simp [Set.indicator_of_mem, Set.indicator_of_notMem, h]

theorem measurable_windowEventCount {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (m n : Nat) :
    Measurable (windowEventCount A m n) := by
  exact Finset.measurable_fun_sum _ fun k _ => measurable_const.indicator (hA k)

theorem windowEventCount_zero_outside_tail {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (m n : Nat) (omega : Omega)
    (homega : omega ∉ eventTail A m) : windowEventCount A m n omega = 0 := by
  classical
  unfold windowEventCount eventTail at *
  simp only [Set.mem_iUnion, not_exists] at homega
  apply Finset.sum_eq_zero
  intro k hk
  have hmk : m <= k := (Finset.mem_Ico.1 hk).1
  have hnmem : omega ∉ A k := by
    intro hak
    exact homega (k - m) (by
      rw [Nat.add_sub_of_le hmk]
      exact hak)
  simp [Set.indicator_of_notMem hnmem]

theorem windowEventCount_eq_sub {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (m n : Nat) (hmn : m <= n) :
    windowEventCount A m n = fun omega => eventCount A n omega - eventCount A m omega := by
  funext omega
  unfold windowEventCount eventCount
  exact Finset.sum_Ico_eq_sub _ hmn

theorem integrable_windowEventCount_sq {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (m n : Nat) :
    Integrable (fun omega => windowEventCount A m n omega ^ 2) mu := by
  classical
  have hsquare : (fun omega => windowEventCount A m n omega ^ 2) = fun omega =>
      Finset.sum (Finset.Ico m n) fun i =>
        Finset.sum (Finset.Ico m n) fun j =>
          (A i ∩ A j).indicator (fun _ => (1 : Real)) omega := by
    funext omega
    unfold windowEventCount
    rw [pow_two, Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro i hi
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    by_cases hi' : omega ∈ A i <;> by_cases hj' : omega ∈ A j <;>
      simp [Set.indicator_of_mem, Set.indicator_of_notMem, hi', hj']
  rw [hsquare]
  exact integrable_finset_sum _ fun i _ =>
    integrable_finset_sum _ fun j _ =>
      (integrable_const 1).indicator ((hA i).inter (hA j))

theorem shifted_secondMoment_bound {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k))
    (m n : Nat) (hmn : m <= n) :
    (partialEventMass mu A n - partialEventMass mu A m) ^ 2 <=
      mu.real (eventTail A m) * pairwiseEventMass mu A n := by
  have hb := finite_secondMoment_bound mu (windowEventCount A m n)
    (measurable_windowEventCount A hA m n) (integrable_windowEventCount_sq mu A hA m n)
    (eventTail A m) (measurable_eventTail A hA m)
    (windowEventCount_zero_outside_tail A m n) (windowEventCount_nonneg A m n)
  have hwin_int : (∫ omega, windowEventCount A m n omega ∂mu) =
      partialEventMass mu A n - partialEventMass mu A m := by
    rw [windowEventCount_eq_sub A m n hmn]
    rw [integral_sub (by
      unfold eventCount
      exact integrable_finset_sum _ fun k _ => (integrable_const 1).indicator (hA k)) (by
      unfold eventCount
      exact integrable_finset_sum _ fun k _ => (integrable_const 1).indicator (hA k)),
      integral_eventCount mu A hA n, integral_eventCount mu A hA m]
  rw [hwin_int] at hb
  calc
    _ <= mu.real (eventTail A m) * (∫ omega, windowEventCount A m n omega ^ 2 ∂mu) := hb
    _ <= mu.real (eventTail A m) * (∫ omega, eventCount A n omega ^ 2 ∂mu) := by
      apply mul_le_mul_of_nonneg_left _ measureReal_nonneg
      apply integral_mono (integrable_windowEventCount_sq mu A hA m n)
        (integrable_eventCount_sq mu A hA n)
      intro omega
      have hle : windowEventCount A m n omega <= eventCount A n omega := by
        unfold windowEventCount eventCount
        exact Finset.sum_le_sum_of_subset_of_nonneg (by
          intro k hk
          exact Finset.mem_range.2 (Finset.mem_Ico.1 hk).2)
          (fun k _ _ => by
            by_cases hk : omega ∈ A k <;>
              simp [Set.indicator_of_mem, Set.indicator_of_notMem, hk])
      nlinarith [windowEventCount_nonneg A m n omega, eventCount_nonneg A n omega]
    _ = _ := by rw [integral_eventCount_sq mu A hA n]

theorem eventMassRatio_le_tail_add_error {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k))
    (m n : Nat) (hmn : m <= n) (hsn : 0 < partialEventMass mu A n) :
    eventMassRatio mu A n <= mu.real (eventTail A m) +
      2 * partialEventMass mu A m / partialEventMass mu A n := by
  let sn := partialEventMass mu A n
  let sm := partialEventMass mu A m
  let dn := pairwiseEventMass mu A n
  let q := mu.real (eventTail A m)
  have hdn : 0 < dn := pairwiseEventMass_pos_of_partialEventMass_pos mu A n hsn
  have hsm : 0 <= sm := partialEventMass_nonneg mu A m
  have hmono : sm <= sn := by
    unfold sm sn partialEventMass
    exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono hmn)
      (fun _ _ _ => measureReal_nonneg)
  have htail : (sn - sm) ^ 2 <= q * dn := shifted_secondMoment_bound mu A hA m n hmn
  have hglobal : sn ^ 2 <= dn := by
    have hf := finite_eventMassRatio_le_eventUnion mu A hA n
    rw [eventMassRatio, div_le_iff₀ hdn] at hf
    exact hf.trans (by
      have hu : mu.real (eventUnion A n) <= 1 := by
        exact (measureReal_mono (μ := mu) (s₁ := eventUnion A n) (s₂ := Set.univ)
          (Set.subset_univ _) (measure_ne_top mu Set.univ)).trans_eq probReal_univ
      nlinarith)
  rw [eventMassRatio]
  unfold sn sm dn q at *
  rw [div_le_iff₀ hdn]
  have herr : 0 <= 2 * partialEventMass mu A m / partialEventMass mu A n :=
    div_nonneg (mul_nonneg (by norm_num) hsm) hsn.le
  rw [add_mul]
  have hcross : 2 * partialEventMass mu A m * partialEventMass mu A n <=
      (2 * partialEventMass mu A m / partialEventMass mu A n) *
        pairwiseEventMass mu A n := by
    rw [div_mul_eq_mul_div, le_div_iff₀ hsn]
    nlinarith [hglobal]
  nlinarith [htail]

theorem tendsto_error_zero {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega)
    (hdiv : Tendsto (partialEventMass mu A) atTop atTop) (m : Nat) :
    Tendsto (fun n => 2 * partialEventMass mu A m / partialEventMass mu A n)
      atTop (nhds 0) := by
  have hinv : Tendsto (fun n => (partialEventMass mu A n)⁻¹) atTop (nhds 0) :=
    hdiv.inv_tendsto_atTop
  simpa [div_eq_mul_inv] using hinv.const_mul (2 * partialEventMass mu A m)

theorem limsup_eventMassRatio_le_eventTail {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k))
    (hdiv : Tendsto (partialEventMass mu A) atTop atTop) (m : Nat) :
    Filter.limsup (eventMassRatio mu A) atTop <= mu.real (eventTail A m) := by
  let err := fun n => 2 * partialEventMass mu A m / partialEventMass mu A n
  have herr : Tendsto err atTop (nhds 0) := tendsto_error_zero mu A hdiv m
  have hmle : ∀ᶠ n : Nat in atTop, m <= n := eventually_ge_atTop m
  have hpos : ∀ᶠ n : Nat in atTop, 0 < partialEventMass mu A n :=
    hdiv.eventually_gt_atTop 0
  have hle : ∀ᶠ n : Nat in atTop,
      eventMassRatio mu A n <= mu.real (eventTail A m) + err n := by
    filter_upwards [hmle, hpos] with n hmn hn
    exact eventMassRatio_le_tail_add_error mu A hA m n hmn hn
  have hlim : Tendsto (fun n => mu.real (eventTail A m) + err n) atTop
      (nhds (mu.real (eventTail A m))) := by
    simpa using tendsto_const_nhds.add herr
  have hlow : IsCoboundedUnder (fun x y : Real => x <= y) atTop
      (eventMassRatio mu A) :=
    IsCoboundedUnder.of_frequently_ge
      (Filter.Eventually.frequently (Filter.Eventually.of_forall fun n =>
        eventMassRatio_nonneg mu A n))
  exact (limsup_le_limsup hle hlow hlim.isBoundedUnder_le).trans_eq hlim.limsup_eq

theorem eventTail_antitone {Omega : Type u} (A : Nat -> Set Omega) :
    Antitone (eventTail A) := by
  intro m n hmn omega homega
  simp only [eventTail, Set.mem_iUnion] at homega ⊢
  rcases homega with ⟨k, hk⟩
  refine ⟨n - m + k, ?_⟩
  rw [← Nat.add_assoc, Nat.add_sub_of_le hmn]
  exact hk

theorem iInter_eventTail_eq_limsup {Omega : Type u} (A : Nat -> Set Omega) :
    (⋂ m, eventTail A m) = limsup A atTop := by
  rw [limsup_eq_iInf_iSup_of_nat]
  simp only [iSup_eq_iUnion, iInf_eq_iInter, eventTail]
  ext omega
  simp only [Set.mem_iInter, Set.mem_iUnion]
  constructor
  · intro h n
    rcases h n with ⟨k, hk⟩
    exact ⟨n + k, ⟨by omega, hk⟩⟩
  · intro h n
    rcases h n with ⟨k, hkn, hk⟩
    exact ⟨k - n, by
      rw [Nat.add_sub_of_le hkn]
      exact hk⟩

theorem tendsto_eventTail_measureReal {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) :
    Tendsto (fun m => mu.real (eventTail A m)) atTop
      (nhds (mu.real (limsup A atTop))) := by
  have he : Tendsto (mu ∘ eventTail A) atTop
      (nhds (mu (⋂ m, eventTail A m))) :=
    tendsto_measure_iInter_atTop
      (fun m => (measurable_eventTail A hA m).nullMeasurableSet)
      (eventTail_antitone A) ⟨0, measure_ne_top mu _⟩
  rw [iInter_eventTail_eq_limsup A] at he
  exact (ENNReal.tendsto_toReal (measure_ne_top mu _)).comp he

theorem erdosRenyiLowerBound {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k))
    (hdiv : Tendsto (partialEventMass mu A) atTop atTop) :
    Filter.limsup (eventMassRatio mu A) atTop <= mu.real (limsup A atTop) := by
  let L := Filter.limsup (eventMassRatio mu A) atTop
  have hle : forall m, L <= mu.real (eventTail A m) :=
    limsup_eventMassRatio_le_eventTail mu A hA hdiv
  have ht := tendsto_eventTail_measureReal mu A hA
  exact ge_of_tendsto' ht hle

/-- Exact proof wrapper for the proposition frozen in `Statement.lean`. -/
theorem erdosRenyiLowerBoundTarget : ErdosRenyiLowerBoundTarget.{u} := by
  intro Omega _ mu _ A hA hdiv
  exact erdosRenyiLowerBound mu A hA hdiv

/-- The local proof also inhabits the root interface frozen by the obligation tree. -/
theorem erdosRenyiObligationRoot : ObligationTree.Root.{u} := by
  intro Omega _ mu _ A hA hdiv
  exact erdosRenyiLowerBound mu A hA hdiv

/-- Checked use of the obligation tree's frozen terminal composition certificate. -/
theorem erdosRenyiObligationRoot_via_frozen_composition : ObligationTree.Root.{u} :=
  ObligationTree.root_compose erdosRenyiObligationRoot

#check (erdosRenyiLowerBoundTarget : ErdosRenyiLowerBoundTarget.{u})
#print axioms erdosRenyiLowerBoundTarget
#print axioms erdosRenyiObligationRoot_via_frozen_composition

end Stage1Instances.THM_M_1009

#print axioms Stage1Instances.THM_M_1009.partialEventMass_nonneg
#print axioms Stage1Instances.THM_M_1009.pairwiseEventMass_pos_of_partialEventMass_pos
#print axioms Stage1Instances.THM_M_1009.integral_eventCount
#print axioms Stage1Instances.THM_M_1009.integral_eventCount_sq
