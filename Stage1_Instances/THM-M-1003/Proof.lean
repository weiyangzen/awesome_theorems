import ObligationTree
import Mathlib.MeasureTheory.Function.ConditionalExpectation.CondJensen
import Mathlib.MeasureTheory.Function.LpSeminorm.CompareExp
import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.MeasureTheory.Function.SimpleFuncDenseLp

/-!
# THM-M-1003 proof execution

This module discharges the finite-measure Lp-to-L1 reduction, reconstructs the
generic finite-exponent conditional-expectation contraction and Levy upward
approximation, constructs the common MemLp/almost-everywhere limit candidate,
and closes the exact frozen target through the checked obligation composition.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal MeasureTheory NNReal Topology

universe u

namespace Stage1Instances.THM_M_1003.Proof

/-- Convexity of the real `q`-power of the norm.  This is the analytic input
needed to apply conditional Jensen at an arbitrary finite exponent. -/
theorem convexOn_univ_norm_rpow {E : Type*} [SeminormedAddCommGroup E]
    [NormedSpace Real E] {q : Real} (hq : 1 <= q) :
    ConvexOn Real Set.univ (fun x : E => ‖x‖ ^ q) := by
  refine ⟨convex_univ, fun x _ y _ a b ha hb hab => ?_⟩
  calc
    ‖a • x + b • y‖ ^ q <= (a * ‖x‖ + b * ‖y‖) ^ q := by
      apply Real.rpow_le_rpow (norm_nonneg _) ?_ (zero_le_one.trans hq)
      calc
        ‖a • x + b • y‖ <= ‖a • x‖ + ‖b • y‖ := norm_add_le _ _
        _ = a * ‖x‖ + b * ‖y‖ := by
          rw [norm_smul, norm_smul, Real.norm_of_nonneg ha, Real.norm_of_nonneg hb]
    _ <= a * ‖x‖ ^ q + b * ‖y‖ ^ q := by
      simpa only [smul_eq_mul] using
        (convexOn_rpow hq).2 (norm_nonneg x) (norm_nonneg y) ha hb hab

/-- Continuity of the real `q`-power of the norm for nonnegative `q`. -/
theorem continuous_norm_rpow {E : Type*} [SeminormedAddCommGroup E]
    {q : Real} (hq : 0 <= q) : Continuous (fun x : E => ‖x‖ ^ q) := by
  exact (Real.continuous_rpow_const hq).comp continuous_norm

/-- Conditional expectation is an `L^p` contraction for every finite exponent
`1 <= p`.  The pinned library packages this only for exponents one and two, so
the proof is reconstructed from conditional Jensen. -/
theorem eLpNorm_condExp_le {Omega : Type u}
    {m m0 : MeasurableSpace Omega} {mu : Measure Omega}
    {f : Omega -> Real} {p : ENNReal} (hm : m <= m0)
    [SigmaFinite (mu.trim hm)] [IsFiniteMeasure mu]
    (hp1 : 1 <= p) (hp0 : p ≠ 0) (hptop : p ≠ (⊤ : ENNReal))
    (hf : MemLp f p mu) :
    eLpNorm (mu[f | m]) p mu <= eLpNorm f p mu := by
  have hpR : 1 <= p.toReal := by
    simpa using ENNReal.toReal_mono hptop hp1
  have hfint : Integrable f mu := hf.integrable hp1
  have hpowint : Integrable ((fun x : Real => ‖x‖ ^ p.toReal) ∘ f) mu := by
    simpa only [Function.comp_apply] using
      (hf.norm_rpow hp0 hptop).integrable le_rfl
  have hjensen :
      (fun x : Real => ‖x‖ ^ p.toReal) ∘ mu[f | m] ≤ᵐ[mu]
        mu[((fun x : Real => ‖x‖ ^ p.toReal) ∘ f) | m] :=
    (convexOn_univ_norm_rpow hpR).map_condExp_le_univ hm
      (continuous_norm_rpow (zero_le_one.trans hpR)).lowerSemicontinuous hfint hpowint
  have hcondpowint :
      Integrable (mu[((fun x : Real => ‖x‖ ^ p.toReal) ∘ f) | m]) mu :=
    integrable_condExp
  have hleftint : Integrable ((fun x : Real => ‖x‖ ^ p.toReal) ∘ mu[f | m]) mu := by
    refine hcondpowint.mono' ?_ ?_
    · exact ((continuous_norm_rpow (zero_le_one.trans hpR)).aestronglyMeasurable.comp_aemeasurable
        (stronglyMeasurable_condExp.mono hm).aemeasurable)
    · filter_upwards [hjensen] with x hx
      change ‖‖mu[f | m] x‖ ^ p.toReal‖ <= _
      rw [Real.norm_of_nonneg (Real.rpow_nonneg (norm_nonneg _) _)]
      exact hx
  have hintegral :
      ∫ x, ‖mu[f | m] x‖ ^ p.toReal ∂mu <= ∫ x, ‖f x‖ ^ p.toReal ∂mu := by
    calc
      ∫ x, ‖mu[f | m] x‖ ^ p.toReal ∂mu
          <= ∫ x, mu[((fun y : Real => ‖y‖ ^ p.toReal) ∘ f) | m] x ∂mu :=
        integral_mono_ae hleftint hcondpowint hjensen
      _ = ∫ x, ‖f x‖ ^ p.toReal ∂mu := by
        simpa only [Function.comp_apply] using
          (integral_condExp (m := m) (μ := mu)
            (f := (fun y : Real => ‖y‖ ^ p.toReal) ∘ f) hm)
  have hcondmem : MemLp (mu[f | m]) p mu := by
    refine ⟨(stronglyMeasurable_condExp.mono hm).aestronglyMeasurable, ?_⟩
    rw [eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top hp0 hptop]
    have hpowlt : ∫⁻ x, ENNReal.ofReal (‖mu[f | m] x‖ ^ p.toReal) ∂mu < (⊤ : ENNReal) := by
      exact (hasFiniteIntegral_iff_ofReal
        (Eventually.of_forall fun x => Real.rpow_nonneg (norm_nonneg _) _)).1
        hleftint.hasFiniteIntegral
    simpa only [← ENNReal.ofReal_rpow_of_nonneg (norm_nonneg _) ENNReal.toReal_nonneg,
      ofReal_norm_eq_enorm] using hpowlt
  rw [hcondmem.eLpNorm_eq_integral_rpow_norm hp0 hptop,
    hf.eLpNorm_eq_integral_rpow_norm hp0 hptop]
  exact ENNReal.ofReal_le_ofReal (Real.rpow_le_rpow
    (integral_nonneg_of_ae <| Eventually.of_forall fun x => by positivity)
    hintegral (inv_nonneg.2 ENNReal.toReal_nonneg))

/-- Conditional expectations of a uniformly bounded terminal variable converge
in every finite `L^p`.  This is the bounded approximation component of the
same-exponent Levy upward theorem. -/
theorem boundedCondExpTendstoLp {Omega : Type u}
    {m0 : MeasurableSpace Omega} {mu : Measure Omega}
    {g : Omega -> Real} {p : ENNReal} {F : Filtration Nat m0}
    [IsFiniteMeasure mu] (hp : 1 <= p) (hptop : p ≠ (⊤ : ENNReal))
    (hgint : Integrable g mu) (hgmeas : StronglyMeasurable[⨆ n, F n] g)
    {C : NNReal} (hbound : ∀ᵐ x ∂mu, |g x| <= C) :
    Tendsto (fun n => eLpNorm (mu[g | F n] - g) p mu) atTop (nhds 0) := by
  have hp0 : p ≠ 0 := (zero_lt_one.trans_le hp).ne'
  have hcondmeas : ∀ n, AEStronglyMeasurable (mu[g | F n]) mu := fun n =>
    (stronglyMeasurable_condExp.mono (F.le n)).aestronglyMeasurable
  have hgmem : MemLp g p mu := by
    refine ⟨(hgmeas.mono (iSup_le fun n => F.le n)).aestronglyMeasurable, ?_⟩
    exact (eLpNorm_le_of_ae_bound (hbound.mono fun x hx => by
      simpa [Real.norm_eq_abs])).trans_lt (by finiteness)
  apply tendsto_Lp_finite_of_tendsto_ae hp hptop hcondmeas hgmem
  · intro eps heps
    refine ⟨(eps / (C + 1)) ^ p.toReal,
      Real.rpow_pos_of_pos (div_pos heps (by positivity)) _, fun n s hs hmus => ?_⟩
    rw [eLpNorm_indicator_eq_eLpNorm_restrict hs]
    have hboundn : ∀ᵐ x ∂mu.restrict s, ‖mu[g | F n] x‖ <= (C : Real) + 1 :=
      ae_restrict_of_ae ((ae_bdd_condExp_of_ae_bdd (m := F n) hbound).mono fun x hx => by
        have hx' : ‖mu[g | F n] x‖ <= (C : Real) := by
          simpa [Real.norm_eq_abs] using hx
        exact hx'.trans (le_add_of_nonneg_right zero_le_one))
    refine (eLpNorm_le_of_ae_bound hboundn).trans ?_
    rw [Measure.restrict_apply MeasurableSet.univ, Set.univ_inter,
      ← ENNReal.le_div_iff_mul_le (Or.inl _) (Or.inl ENNReal.ofReal_ne_top)]
    · rw [ENNReal.rpow_inv_le_iff (ENNReal.toReal_pos hp0 hptop)]
      refine hmus.trans ?_
      rw [← ENNReal.ofReal_rpow_of_pos (div_pos heps (by positivity)),
        ENNReal.rpow_le_rpow_iff (ENNReal.toReal_pos hp0 hptop)]
      rw [ENNReal.ofReal_div_of_pos (by positivity)]
    · simpa only [ENNReal.ofReal_eq_zero, not_le, Ne] using
        (show (0 : Real) < (C : Real) + 1 by positivity)
  · exact hgint.tendsto_ae_condExp hgmeas

/-- An almost-everywhere bounded family is uniformly integrable at every
finite exponent. -/
theorem unifIntegrableOfAeBound {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {p : ENNReal} (hp : 1 <= p)
    (hptop : p ≠ (⊤ : ENNReal)) {f : Nat -> Omega -> Real}
    (hf : ∀ n, AEStronglyMeasurable (f n) mu) (R : NNReal)
    (hbdd : ∀ n, ∀ᵐ x ∂mu, |f n x| <= R) : UnifIntegrable f p mu := by
  apply unifIntegrable_of hp hptop hf
  intro epsilon hepsilon
  refine ⟨R + 1, fun n => ?_⟩
  let fn := (hf n).mk (f n)
  have hfnmeas : StronglyMeasurable fn := (hf n).stronglyMeasurable_mk
  have hs : MeasurableSet {x | R + 1 <= ‖fn x‖₊} :=
    measurableSet_le measurable_const hfnmeas.nnnorm.measurable
  have htailMeas : AEStronglyMeasurable
      ({x | R + 1 <= ‖f n x‖₊}.indicator (f n)) mu := by
    refine (hfnmeas.aestronglyMeasurable.indicator hs).congr ?_
    filter_upwards [(hf n).ae_eq_mk] with x hx
    simp only [Set.indicator_apply, fn]
    simp [hx]
  have hzero : eLpNorm ({x | R + 1 <= ‖f n x‖₊}.indicator (f n)) p mu = 0 := by
    rw [eLpNorm_eq_zero_iff htailMeas (ne_of_gt (zero_lt_one.trans_le hp))]
    filter_upwards [hbdd n] with x hx
    simp only [Set.indicator_apply]
    split_ifs with h
    · exfalso
      have : (R : Real) + 1 <= |f n x| := by simpa using h
      exact (not_le_of_gt (lt_of_le_of_lt hx (lt_add_one (R : Real)))) this
    · rfl
  rw [hzero]
  exact bot_le

/-- Levy's upward theorem in the original finite exponent.  The proof uses a
bounded simple approximation, projects it to the joined filtration, applies
the bounded case, and controls both approximation errors with the conditional
expectation contraction above. -/
theorem memLpTendstoCondExp {Omega : Type u} {m0 : MeasurableSpace Omega}
    {mu : Measure Omega} {F : Filtration Nat m0} [IsFiniteMeasure mu]
    {p : ENNReal} (hp : 1 <= p) (hptop : p ≠ (⊤ : ENNReal))
    {g : Omega -> Real} (hg : MemLp g p mu)
    (hgmeas : StronglyMeasurable[⨆ n, F n] g) :
    Tendsto (fun n => eLpNorm (mu[g | F n] - g) p mu) atTop (nhds 0) := by
  have hp0 : p ≠ 0 := (zero_lt_one.trans_le hp).ne'
  rw [ENNReal.tendsto_atTop_zero]
  intro eps heps
  have heighth : eps / 3 ≠ 0 := ENNReal.div_ne_zero.2 ⟨heps.ne', by norm_num⟩
  obtain ⟨s, hsclose, hsmem⟩ := hg.exists_simpleFunc_eLpNorm_sub_lt hptop heighth
  let h : Omega -> Real := mu[(s : Omega -> Real) | ⨆ n, F n]
  have hsint : Integrable (s : Omega -> Real) mu := (s.memLp_top mu).integrable (by simp)
  have hhmem : MemLp h p mu := by
    have hle := eLpNorm_condExp_le (mu := mu) (m := ⨆ n, F n)
      (iSup_le fun n => F.le n) hp hp0 hptop hsmem
    exact ⟨(stronglyMeasurable_condExp.mono (iSup_le fun n => F.le n)).aestronglyMeasurable,
      hle.trans_lt hsmem.eLpNorm_lt_top⟩
  have hhclose : eLpNorm (g - h) p mu < eps / 3 := by
    have hcondsub := condExp_sub (hg.integrable hp) hsint (⨆ n, F n)
    have hgid : mu[g | ⨆ n, F n] =ᵐ[mu] g :=
      condExp_of_aestronglyMeasurable' (iSup_le fun n => F.le n)
        hgmeas.aestronglyMeasurable (hg.integrable hp)
    have heq : mu[g - (s : Omega -> Real) | ⨆ n, F n] =ᵐ[mu] g - h :=
      hcondsub.trans (hgid.sub (EventuallyEq.rfl : h =ᵐ[mu] h))
    calc
      eLpNorm (g - h) p mu = eLpNorm (mu[g - (s : Omega -> Real) | ⨆ n, F n]) p mu :=
        eLpNorm_congr_ae heq.symm
      _ <= eLpNorm (g - (s : Omega -> Real)) p mu :=
        eLpNorm_condExp_le (iSup_le fun n => F.le n) hp hp0 hptop (hg.sub hsmem)
      _ < eps / 3 := hsclose
  obtain ⟨Rreal, hRreal⟩ := s.exists_forall_norm_le
  let R : NNReal := ⟨max Rreal 0, le_max_right _ _⟩
  have hsbound : ∀ᵐ x ∂mu, |(s : Omega -> Real) x| <= R := by
    filter_upwards with x
    change |s x| <= max Rreal 0
    exact (hRreal x).trans (le_max_left _ _)
  have hhbound : ∀ᵐ x ∂mu, |h x| <= R := ae_bdd_condExp_of_ae_bdd hsbound
  have hhint : Integrable h mu := integrable_condExp
  have hhmeas : StronglyMeasurable[⨆ n, F n] h := stronglyMeasurable_condExp
  have hhtend := boundedCondExpTendstoLp hp hptop hhint hhmeas hhbound
  rw [ENNReal.tendsto_atTop_zero] at hhtend
  obtain ⟨N, hN⟩ := hhtend (eps / 3) (ENNReal.div_pos heps.ne' (by norm_num))
  refine ⟨N, fun n hn => ?_⟩
  have hgint : Integrable g mu := hg.integrable hp
  have hcondgmem : MemLp (mu[g | F n]) p mu := by
    have hle := eLpNorm_condExp_le (F.le n) hp hp0 hptop hg
    exact ⟨(stronglyMeasurable_condExp.mono (F.le n)).aestronglyMeasurable,
      hle.trans_lt hg.eLpNorm_lt_top⟩
  have hcondhmem : MemLp (mu[h | F n]) p mu := by
    have hle := eLpNorm_condExp_le (F.le n) hp hp0 hptop hhmem
    exact ⟨(stronglyMeasurable_condExp.mono (F.le n)).aestronglyMeasurable,
      hle.trans_lt hhmem.eLpNorm_lt_top⟩
  have hceclose : eLpNorm (mu[g | F n] - mu[h | F n]) p mu < eps / 3 := by
    rw [← eLpNorm_congr_ae (condExp_sub hgint hhint (F n))]
    exact (eLpNorm_condExp_le (F.le n) hp hp0 hptop (hg.sub hhmem)).trans_lt hhclose
  calc
    eLpNorm (mu[g | F n] - g) p mu =
        eLpNorm ((mu[g | F n] - mu[h | F n]) +
          ((mu[h | F n] - h) + (h - g))) p mu := by
      congr 1
      funext x
      simp
    _ <= eLpNorm (mu[g | F n] - mu[h | F n]) p mu +
          eLpNorm ((mu[h | F n] - h) + (h - g)) p mu :=
      eLpNorm_add_le (hcondgmem.1.sub hcondhmem.1)
        ((hcondhmem.1.sub hhmem.1).add (hhmem.1.sub hg.1)) hp
    _ <= eLpNorm (mu[g | F n] - mu[h | F n]) p mu +
          (eLpNorm (mu[h | F n] - h) p mu + eLpNorm (h - g) p mu) := by
      gcongr
      exact eLpNorm_add_le (hcondhmem.1.sub hhmem.1) (hhmem.1.sub hg.1) hp
    _ <= eps / 3 + (eps / 3 + eps / 3) := by
      apply add_le_add
      · exact hceclose.le
      · apply add_le_add
        · exact hN n hn
        · rw [eLpNorm_sub_comm]
          exact hhclose.le
    _ = eps := by rw [← add_assoc, ENNReal.add_thirds]

/-- A uniform Lp bound with p > 1 gives the L1 bound needed by the pinned
almost-everywhere martingale convergence theorem on a finite measure space. -/
theorem uniformL1Bound {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) :
    ∃ bound : NNReal, ∀ n, eLpNorm (D.process n) 1 D.measure ≤ bound := by
  letI : IsFiniteMeasure D.measure := D.finiteMeasure
  obtain ⟨bound, hbound⟩ := D.lpBounded
  let factor : ENNReal :=
    D.measure Set.univ ^ (1 - 1 / D.exponent.toReal)
  have hfactor : factor ≠ ∞ := by
    apply ENNReal.rpow_ne_top_of_nonneg
    · rw [sub_nonneg, div_le_one]
      · exact ENNReal.toReal_mono D.exponent_lt_top.ne D.one_lt_exponent.le
      · exact ENNReal.toReal_pos
          (ne_of_gt (zero_lt_one.trans D.one_lt_exponent))
          D.exponent_lt_top.ne
    · exact IsFiniteMeasure.measure_univ_lt_top.ne
  refine ⟨bound * factor.toNNReal, fun n => ?_⟩
  calc
    eLpNorm (D.process n) 1 D.measure ≤
        eLpNorm (D.process n) D.exponent D.measure * factor := by
      simpa [factor] using
        (eLpNorm_le_eLpNorm_mul_rpow_measure_univ
          (show (1 : ENNReal) ≤ D.exponent from D.one_lt_exponent.le)
          (((D.martingale.stronglyMeasurable n).mono
            (D.filtration.le n)).aestronglyMeasurable))
    _ ≤ (bound : ENNReal) * factor := by
      gcongr
      exact hbound n
    _ = ((bound * factor.toNNReal : NNReal) : ENNReal) := by
      rw [ENNReal.coe_mul, ENNReal.coe_toNNReal hfactor]

/-- The selected mathlib limit process supplies the complete candidate package:
same-exponent MemLp membership and almost-everywhere convergence. -/
theorem limitCandidate {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) :
    ∃ limit : Omega -> Real, LimitCandidatePackage D limit := by
  letI : IsFiniteMeasure D.measure := D.finiteMeasure
  obtain ⟨bound, hbound⟩ := uniformL1Bound D
  let limit := D.filtration.limitProcess D.process D.measure
  refine ⟨limit, ?_, ?_⟩
  · obtain ⟨lpBound, hlpBound⟩ := D.lpBounded
    exact D.martingale.submartingale.memLp_limitProcess hlpBound
  · exact D.martingale.submartingale.ae_tendsto_limitProcess hbound

/-- Universally packaged candidate premise consumed by the frozen root
composition theorem. -/
theorem candidatePackage :
    forall (Omega : Type u) [MeasurableSpace Omega]
      (D : LpBoundedMartingale Omega),
        Exists fun limit : Omega -> Real => LimitCandidatePackage D limit := by
  intro Omega _ D
  exact limitCandidate D

/-- Uniform `L^p` boundedness above exponent one implies uniform
integrability in `L^1`.  The exponent-comparison estimate is applied under the
restricted measure so that its measure factor is `measure s`, rather than the
measure of the whole space. -/
theorem uniformL1UI {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) :
    UniformIntegrable D.process 1 D.measure := by
  letI : IsFiniteMeasure D.measure := D.finiteMeasure
  have hmeas : ∀ n, AEStronglyMeasurable (D.process n) D.measure := fun n =>
    ((D.martingale.stronglyMeasurable n).mono
      (D.filtration.le n)).aestronglyMeasurable
  obtain ⟨bound, hbound⟩ := D.lpBounded
  refine ⟨hmeas, ?_, ?_⟩
  · intro epsilon hepsilon
    have hexponentReal : 1 < D.exponent.toReal := by
      rw [← ENNReal.toReal_one,
        ENNReal.toReal_lt_toReal ENNReal.one_ne_top D.exponent_lt_top.ne]
      exact D.one_lt_exponent
    let holderExponent : Real := 1 - 1 / D.exponent.toReal
    have hholderExponent : 0 < holderExponent := by
      dsimp [holderExponent]
      rw [sub_pos, div_lt_one (zero_lt_one.trans hexponentReal)]
      exact hexponentReal
    let delta : Real :=
      (epsilon / ((bound : Real) + 1)) ^ (1 / holderExponent)
    have hdelta : 0 < delta :=
      Real.rpow_pos_of_pos (div_pos hepsilon (by positivity)) _
    refine ⟨delta, hdelta, fun n s hs hmeasure => ?_⟩
    let restricted := D.measure.restrict s
    have hcompare := eLpNorm_le_eLpNorm_mul_rpow_measure_univ
      (μ := restricted) (f := D.process n) (p := (1 : ENNReal))
      (q := D.exponent) D.one_lt_exponent.le
      (hmeas n).restrict
    have hindicatorBound :
        eLpNorm (s.indicator (D.process n)) D.exponent D.measure ≤ bound :=
      (eLpNorm_indicator_le _).trans (hbound n)
    calc
      eLpNorm (s.indicator (D.process n)) 1 D.measure ≤
          eLpNorm (s.indicator (D.process n)) D.exponent D.measure *
            D.measure s ^ (1 - 1 / D.exponent.toReal) := by
        simpa [restricted, eLpNorm_indicator_eq_eLpNorm_restrict hs,
          Measure.restrict_apply MeasurableSet.univ, Set.univ_inter] using hcompare
      _ ≤ (bound : ENNReal) * (ENNReal.ofReal delta) ^ holderExponent := by
        gcongr
      _ ≤ ENNReal.ofReal epsilon := by
        rw [← ENNReal.ofReal_coe_nnreal,
          ENNReal.ofReal_rpow_of_pos hdelta,
          ← ENNReal.ofReal_mul (NNReal.coe_nonneg bound)]
        apply ENNReal.ofReal_le_ofReal
        dsimp [delta]
        rw [← Real.rpow_mul (div_nonneg hepsilon.le (by positivity)),
          one_div_mul_cancel hholderExponent.ne', Real.rpow_one]
        have hdenominator : 0 < (bound : Real) + 1 := by positivity
        calc
          (bound : Real) * (epsilon / ((bound : Real) + 1)) ≤
              ((bound : Real) + 1) *
                (epsilon / ((bound : Real) + 1)) := by
            gcongr
            exact le_add_of_nonneg_right zero_le_one
          _ = epsilon := by field_simp
  · exact uniformL1Bound D

/-- Same-exponent norm convergence for the canonical mathlib limit process.
The martingale representation turns each process value into a conditional
expectation of this limit, to which `memLpTendstoCondExp` applies. -/
theorem sameExponentNormCanonical {Omega : Type u}
    [MeasurableSpace Omega] (D : LpBoundedMartingale Omega) :
    SameExponentNormPackage D
      (D.filtration.limitProcess D.process D.measure) := by
  letI : IsFiniteMeasure D.measure := D.finiteMeasure
  let limit := D.filtration.limitProcess D.process D.measure
  have hlimit : MemLp limit D.exponent D.measure := by
    obtain ⟨bound, hbound⟩ := D.lpBounded
    exact D.martingale.submartingale.memLp_limitProcess hbound
  have htendsto := memLpTendstoCondExp
    D.one_lt_exponent.le D.exponent_lt_top.ne hlimit
    (D.filtration.stronglyMeasurable_limitProcess :
      StronglyMeasurable[⨆ n, D.filtration n] limit)
  have hrepresentation : ∀ n, D.process n =ᵐ[D.measure]
      D.measure[limit | D.filtration n] :=
    D.martingale.ae_eq_condExp_limitProcess (uniformL1UI D)
  exact htendsto.congr fun n => (eLpNorm_congr_ae
    ((hrepresentation n).sub
      (EventuallyEq.rfl : limit =ᵐ[D.measure] limit))).symm

/-- The same-exponent package for any candidate satisfying the frozen common
limit interface.  Almost-everywhere uniqueness transports convergence from
the canonical limit process. -/
theorem sameExponentPackage :
    forall (Omega : Type u) [MeasurableSpace Omega]
      (D : LpBoundedMartingale Omega) (limit : Omega -> Real),
      LimitCandidatePackage D limit -> SameExponentNormPackage D limit := by
  intro Omega _ D limit hlimit
  letI : IsFiniteMeasure D.measure := D.finiteMeasure
  let canonical := D.filtration.limitProcess D.process D.measure
  have hbound := uniformL1Bound D
  have hcanonicalAE :=
    D.martingale.submartingale.ae_tendsto_limitProcess hbound.choose_spec
  have heq : canonical =ᵐ[D.measure] limit := by
    filter_upwards [hcanonicalAE, hlimit.2] with omega hcanonical hcandidate
    exact tendsto_nhds_unique hcanonical hcandidate
  have htendsto := sameExponentNormCanonical D
  exact htendsto.congr fun n => eLpNorm_congr_ae
    ((EventuallyEq.rfl :
      D.process n =ᵐ[D.measure] D.process n).sub heq)

/-- Exact frozen theorem root, assembled without additional premises. -/
theorem target : LpMartingaleConvergenceTarget.{u} :=
  root_of_limit_packages candidatePackage sameExponentPackage

#check uniformL1Bound
#check eLpNorm_condExp_le
#check boundedCondExpTendstoLp
#check memLpTendstoCondExp
#check limitCandidate
#check candidatePackage
#check uniformL1UI
#check sameExponentNormCanonical
#check sameExponentPackage
#check target
#print sorries convexOn_univ_norm_rpow
#print sorries continuous_norm_rpow
#print sorries eLpNorm_condExp_le
#print sorries boundedCondExpTendstoLp
#print sorries unifIntegrableOfAeBound
#print sorries memLpTendstoCondExp
#print sorries uniformL1Bound
#print sorries limitCandidate
#print sorries candidatePackage
#print sorries uniformL1UI
#print sorries sameExponentNormCanonical
#print sorries sameExponentPackage
#print sorries target
#print axioms convexOn_univ_norm_rpow
#print axioms continuous_norm_rpow
#print axioms eLpNorm_condExp_le
#print axioms boundedCondExpTendstoLp
#print axioms unifIntegrableOfAeBound
#print axioms memLpTendstoCondExp
#print axioms uniformL1Bound
#print axioms limitCandidate
#print axioms candidatePackage
#print axioms uniformL1UI
#print axioms sameExponentNormCanonical
#print axioms sameExponentPackage
#print axioms target

end Stage1Instances.THM_M_1003.Proof
