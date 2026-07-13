import «Stage1_Instances».«THM-M-0989».Proof
import «Stage1_Instances».«THM-M-0989».ProdExp
import «Stage1_Instances».«THM-M-0989».CharFunBound

/-!
# Triangular-array Lindeberg estimates

This module develops the analytic estimates needed to close the exact frozen
unit-variance triangular-array target. Its proof architecture adapts the
characteristic-function argument in `Clt/Lindeberg.lean` from
`patrickrd/CLT-lindeberg` at commit
`82249ccfc05c0d97b86f33fce2582f0bf4ff9c06`; that source snapshot has SHA-256
`64020a1982986ca506b3623ff7b1f9a2bad2a57edb764ef0689ddda0ab43da3c`.
The normalized `Fin (n + 1)` row statements and proofs here are repo-local
adaptations rather than imports of the external sequence theorem.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory Complex
open scoped BigOperators ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0989

universe u

variable {Omega : Type u} [MeasurableSpace Omega]

/-- Every row second moment lies between zero and one. -/
theorem rowSecondMoment_mem_unitInterval
    (A : NormalizedTriangularArray Omega) (n : Nat) (k : Fin (n + 1)) :
    A.probabilityMeasure[(A.increment n k) ^ 2] ∈ Set.Icc (0 : Real) 1 := by
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  constructor
  · exact integral_nonneg fun x =>
      Pi.pow_apply (A.increment n k) 2 x ▸ sq_nonneg _
  · rw [← rowSecondMoment_sum A n]
    exact Finset.single_le_sum
      (fun i _ => integral_nonneg fun x =>
        Pi.pow_apply (A.increment n i) 2 x ▸ sq_nonneg _)
      (Finset.mem_univ k)

/-- A second moment is bounded by a small deterministic square plus its
strict-threshold truncated second moment. -/
theorem secondMoment_le_sq_add_truncated
    {P : Measure Omega} [IsProbabilityMeasure P]
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P)
    {epsilon : Real} (hepsilon : 0 <= epsilon) :
    P[X ^ 2] <= epsilon ^ 2 + truncatedSecondMoment P X epsilon := by
  let s : Set Omega := {omega | epsilon < ‖X omega‖}
  have hs : NullMeasurableSet s P :=
    nullMeasurableSet_lt aemeasurable_const hXmeas.norm
  have hsmall : ∫ omega in sᶜ, (X omega) ^ 2 ∂P <= epsilon ^ 2 := by
    calc
      (∫ omega in sᶜ, (X omega) ^ 2 ∂P)
          <= ∫ _omega in sᶜ, epsilon ^ 2 ∂P := by
            refine setIntegral_mono_ae_restrict hXsq.integrableOn
              (integrable_const _).integrableOn ?_
            filter_upwards [ae_restrict_mem₀ hs.compl] with omega homega
            simp only [s, Set.mem_compl_iff, Set.mem_setOf_eq] at homega
            have hnorm : ‖X omega‖ <= epsilon := le_of_not_gt homega
            rw [Real.norm_eq_abs] at hnorm
            have hsquare := mul_self_le_mul_self (abs_nonneg (X omega)) hnorm
            simpa [pow_two] using hsquare
      _ = P.real sᶜ * epsilon ^ 2 := by
            rw [setIntegral_const, smul_eq_mul]
      _ <= 1 * epsilon ^ 2 := by
            gcongr
            exact measureReal_le_one
      _ = epsilon ^ 2 := one_mul _
  have hlarge : ∫ omega in s, (X omega) ^ 2 ∂P =
      truncatedSecondMoment P X epsilon := by
    unfold truncatedSecondMoment
    rw [← integral_indicator₀ hs]
    refine integral_congr_ae ?_
    filter_upwards [] with omega
    simp only [Set.indicator, s]
    by_cases h : epsilon < ‖X omega‖ <;> simp [h]
  have hsplit := integral_add_compl₀ hs hXsq
  change (∫ x, X x ^ 2 ∂P) <= _
  rw [← hlarge, ← hsplit]
  linarith

/-- Lindeberg control and unit row variance force the sum of squared row
second moments to vanish. This is a quantitative infinitesimality package. -/
theorem tendsto_sum_rowSecondMoment_sq
    (A : NormalizedTriangularArray Omega) :
    Tendsto
      (fun n => ∑ k : Fin (n + 1),
        (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2)
      atTop (nhds 0) := by
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  rw [Metric.tendsto_nhds]
  intro delta hdelta
  let epsilon := Real.sqrt (delta / 2)
  have hepsilon : 0 < epsilon := Real.sqrt_pos.mpr (by positivity)
  have hepsilon_sq : epsilon ^ 2 = delta / 2 :=
    Real.sq_sqrt (by positivity)
  have htail := A.lindebergCondition epsilon hepsilon
  rw [Metric.tendsto_nhds] at htail
  have htail_small := htail (delta / 2) (by positivity)
  simp only [Real.dist_eq, sub_zero] at htail_small
  filter_upwards [htail_small] with n hn
  rw [Real.dist_eq, sub_zero]
  have htail_nonneg : 0 <= ∑ k : Fin (n + 1),
      truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon :=
    Finset.sum_nonneg fun k _ =>
      truncatedSecondMoment_nonneg A.probabilityMeasure (A.increment n k) epsilon
  have hn' : (∑ k : Fin (n + 1),
      truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon) <
      delta / 2 := by
    rwa [abs_of_nonneg htail_nonneg] at hn
  rw [abs_of_nonneg (Finset.sum_nonneg fun _ _ => sq_nonneg _)]
  have hterm (k : Fin (n + 1)) :
      (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2 <=
        epsilon ^ 2 * A.probabilityMeasure[(A.increment n k) ^ 2] +
          truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon := by
    have hv := rowSecondMoment_mem_unitInterval A n k
    have hbound := secondMoment_le_sq_add_truncated
      (A.rowAEMeasurable n k) (A.rowSquareIntegrable n k) hepsilon.le
    have htailnonneg := truncatedSecondMoment_nonneg
      A.probabilityMeasure (A.increment n k) epsilon
    have hv1 := hv.1
    have hv2 := hv.2
    have hmul := mul_le_mul_of_nonneg_left hbound hv1
    have hmtail := mul_le_mul_of_nonneg_right hv2 htailnonneg
    nlinarith
  calc
    (∑ k : Fin (n + 1),
        (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2)
        <= ∑ k : Fin (n + 1),
          (epsilon ^ 2 * A.probabilityMeasure[(A.increment n k) ^ 2] +
            truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon) :=
          Finset.sum_le_sum fun k _ => hterm k
    _ = epsilon ^ 2 + ∑ k : Fin (n + 1),
          truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon := by
          rw [Finset.sum_add_distrib, ← Finset.mul_sum, rowSecondMoment_sum, mul_one]
    _ < delta / 2 + delta / 2 := by rw [hepsilon_sq]; linarith
    _ = delta := by ring

section CharacteristicFunctionHelpers

variable {P : Measure Omega} [IsProbabilityMeasure P]

/-- Square integrability implies first-moment integrability on a probability
space. -/
private theorem integrable_of_integrable_sq
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P) :
    Integrable X P := by
  have hone : Integrable (fun _ : Omega => (1 : Real)) P := integrable_const _
  have hdom : Integrable (fun omega => 1 + (X omega) ^ 2) P := hone.add hXsq
  refine hdom.mono hXmeas.aestronglyMeasurable ?_
  filter_upwards [] with omega
  simp only [Real.norm_eq_abs]
  have hnonneg : 0 <= 1 + (X omega) ^ 2 := by positivity
  rw [abs_of_nonneg hnonneg]
  nlinarith [sq_nonneg (|X omega| - 1), sq_abs (X omega)]

/-- Rewrite the characteristic function of an AE-measurable pushforward as
an integral on the original probability space. -/
private theorem charFun_map_eq_integral
    {X : Omega -> Real} (hXmeas : AEMeasurable X P) (t : Real) :
    charFun (P.map X) t =
      ∫ omega, cexp (((t * X omega : Real) : Complex) * I) ∂P := by
  rw [charFun_apply_real]
  rw [integral_map hXmeas (by fun_prop)]
  congr 1
  funext omega
  push_cast
  ring

private theorem integrable_cexp_mul_I
    {X : Omega -> Real} (hXmeas : AEMeasurable X P) (t : Real) :
    Integrable (fun omega => cexp (((t * X omega : Real) : Complex) * I)) P := by
  have hstrong : AEStronglyMeasurable
      (fun omega => cexp (((t * X omega : Real) : Complex) * I)) P := by
    have hreal : AEMeasurable (fun omega => t * X omega) P :=
      aemeasurable_const.mul hXmeas
    exact (Complex.measurable_exp.comp_aemeasurable
      ((Complex.measurable_ofReal.comp_aemeasurable hreal).mul_const I)).aestronglyMeasurable
  refine ⟨hstrong, ?_⟩
  refine (integrable_const (1 : Real)).hasFiniteIntegral.mono ?_
  filter_upwards [] with omega
  rw [Real.norm_eq_abs, abs_of_nonneg zero_le_one, norm_exp_ofReal_mul_I]

private theorem integrable_linear_complex
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P) (t : Real) :
    Integrable (fun omega => (((t * X omega : Real) : Complex) * I)) P := by
  have hXint := integrable_of_integrable_sq hXmeas hXsq
  exact (hXint.const_mul t).ofReal.mul_const I

private theorem integrable_quadratic_complex
    {X : Omega -> Real}
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P) (t : Real) :
    Integrable (fun omega => ((((t * X omega) ^ 2 / 2 : Real)) : Complex)) P := by
  have heq : (fun omega => (t * X omega) ^ 2 / 2) =
      (fun omega => (t ^ 2 / 2) * X omega ^ 2) := by
    funext omega
    ring
  have hreal : Integrable (fun omega => (t * X omega) ^ 2 / 2) P := by
    rw [heq]
    exact hXsq.const_mul _
  exact hreal.ofReal

private theorem integrable_secondOrderRemainder
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P) (t : Real) :
    Integrable (fun omega =>
      cexp (((t * X omega : Real) : Complex) * I) - 1 -
        ((t * X omega : Real) : Complex) * I +
          (((t * X omega) ^ 2 / 2 : Real) : Complex)) P := by
  exact (((integrable_cexp_mul_I hXmeas t).sub (integrable_const _)).sub
    (integrable_linear_complex hXmeas hXsq t)).add
      (integrable_quadratic_complex hXsq t)

private theorem integral_linear_complex_eq_zero
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P)
    (hcenter : P[X] = 0) (t : Real) :
    (∫ omega, ((t * X omega : Real) : Complex) * I ∂P) = 0 := by
  have hXint := integrable_of_integrable_sq hXmeas hXsq
  have hreal :
      (∫ omega, ((t * X omega : Real) : Complex) ∂P) =
        (((∫ omega, t * X omega ∂P : Real)) : Complex) := by
    exact @integral_ofReal Omega _ P Complex _
      (fun omega => t * X omega)
  calc
    (∫ omega, ((t * X omega : Real) : Complex) * I ∂P) =
        (∫ omega, ((t * X omega : Real) : Complex) ∂P) * I :=
      integral_mul_const I _
    _ = (((∫ omega, t * X omega ∂P : Real) : Complex)) * I := by rw [hreal]
    _ = (((t * ∫ omega, X omega ∂P : Real) : Complex)) * I := by
      rw [integral_const_mul]
    _ = 0 := by rw [hcenter]; simp

/-- The centered characteristic-function error is the integral of the exact
second-order exponential remainder. -/
private theorem charFun_sub_one_add_quadratic_eq_integral
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P)
    (hcenter : P[X] = 0) (t : Real) :
    charFun (P.map X) t - 1 +
        (((P[fun omega => X omega ^ 2] * t ^ 2 / 2 : Real)) : Complex) =
      ∫ omega,
        (cexp (((t * X omega : Real) : Complex) * I) - 1 -
          ((t * X omega : Real) : Complex) * I +
            (((t * X omega) ^ 2 / 2 : Real) : Complex)) ∂P := by
  rw [charFun_map_eq_integral hXmeas t]
  have hexp := integrable_cexp_mul_I hXmeas t
  have hlin := integrable_linear_complex hXmeas hXsq t
  have hquad := integrable_quadratic_complex hXsq t
  have hlinearIntegral := integral_linear_complex_eq_zero hXmeas hXsq hcenter t
  have hquadIntegral :
      (∫ omega, (((t * X omega) ^ 2 / 2 : Real) : Complex) ∂P) =
        (((P[fun omega => X omega ^ 2] * t ^ 2 / 2 : Real)) : Complex) := by
    have hcast :
        (∫ omega, (((t * X omega) ^ 2 / 2 : Real) : Complex) ∂P) =
          (((∫ omega, (t * X omega) ^ 2 / 2 ∂P : Real)) : Complex) := by
      exact @integral_ofReal Omega _ P Complex _
        (fun omega => (t * X omega) ^ 2 / 2)
    rw [hcast]
    have heq : (fun omega => (t * X omega) ^ 2 / 2) =
        (fun omega => (t ^ 2 / 2) * X omega ^ 2) := by
      funext omega
      ring
    rw [heq, integral_const_mul]
    push_cast
    ring
  have hfull :
      (∫ omega,
        (cexp (((t * X omega : Real) : Complex) * I) - 1 -
          ((t * X omega : Real) : Complex) * I +
            (((t * X omega) ^ 2 / 2 : Real) : Complex)) ∂P) =
      (∫ omega, cexp (((t * X omega : Real) : Complex) * I) ∂P) -
        (∫ _omega, (1 : Complex) ∂P) -
        (∫ omega, ((t * X omega : Real) : Complex) * I ∂P) +
        (∫ omega, (((t * X omega) ^ 2 / 2 : Real) : Complex) ∂P) := by
    have hone : Integrable (fun _ : Omega => (1 : Complex)) P := integrable_const _
    have hadd := integral_add ((hexp.sub hone).sub hlin) hquad
    have hsub1 := integral_sub (hexp.sub hone) hlin
    have hsub2 := integral_sub hexp hone
    exact hadd.trans (congrArg (fun z => z +
      (∫ omega, (((t * X omega) ^ 2 / 2 : Real) : Complex) ∂P))
      (hsub1.trans (congrArg (fun z => z -
        (∫ omega, ((t * X omega : Real) : Complex) * I ∂P)) hsub2)))
  rw [hfull, integral_const, hlinearIntegral, hquadIntegral]
  simp

/-- A centered characteristic function differs from one by at most half its
second moment times the squared frequency. -/
private theorem norm_charFun_sub_one_le
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P)
    (hcenter : P[X] = 0) (t : Real) :
    ‖charFun (P.map X) t - 1‖ <=
      (t ^ 2 / 2) * P[fun omega => X omega ^ 2] := by
  let f : Omega -> Complex := fun omega =>
    cexp (((t * X omega : Real) : Complex) * I) - 1 -
      ((t * X omega : Real) : Complex) * I
  have hfint : Integrable f P :=
    (integrable_cexp_mul_I hXmeas t).sub (integrable_const _) |>.sub
      (integrable_linear_complex hXmeas hXsq t)
  have hidentity : charFun (P.map X) t - 1 = ∫ omega, f omega ∂P := by
    have hlinearIntegral :=
      integral_linear_complex_eq_zero hXmeas hXsq hcenter t
    rw [charFun_map_eq_integral hXmeas t]
    have hfull :
        (∫ omega, f omega ∂P) =
          (∫ omega, cexp (((t * X omega : Real) : Complex) * I) ∂P) -
          (∫ _omega, (1 : Complex) ∂P) -
          (∫ omega, ((t * X omega : Real) : Complex) * I ∂P) := by
      have hone : Integrable (fun _ : Omega => (1 : Complex)) P := integrable_const _
      have hsub1 := integral_sub
        ((integrable_cexp_mul_I hXmeas t).sub hone)
        (integrable_linear_complex hXmeas hXsq t)
      have hsub2 := integral_sub (integrable_cexp_mul_I hXmeas t) hone
      change (∫ omega,
        (cexp (((t * X omega : Real) : Complex) * I) - 1 -
          ((t * X omega : Real) : Complex) * I) ∂P) = _
      exact hsub1.trans (congrArg (fun z => z -
        (∫ omega, ((t * X omega : Real) : Complex) * I ∂P)) hsub2)
    rw [hfull, integral_const, hlinearIntegral]
    simp
  rw [hidentity]
  calc
    ‖∫ omega, f omega ∂P‖ <= ∫ omega, ‖f omega‖ ∂P :=
      norm_integral_le_integral_norm _
    _ <= ∫ omega, (t * X omega) ^ 2 / 2 ∂P := by
      refine integral_mono_of_nonneg (ae_of_all _ fun _ => norm_nonneg _) ?_ ?_
      · have heq : (fun omega => (t * X omega) ^ 2 / 2) =
            (fun omega => (t ^ 2 / 2) * X omega ^ 2) := by
          funext omega
          ring
        rw [heq]
        exact hXsq.const_mul _
      · filter_upwards [] with omega
        exact CharFunBound.norm_cexp_mul_I_sub_one_sub_le_half_sq (t * X omega)
    _ = (t ^ 2 / 2) * P[fun omega => X omega ^ 2] := by
      have heq : (fun omega => (t * X omega) ^ 2 / 2) =
          (fun omega => (t ^ 2 / 2) * X omega ^ 2) := by
        funext omega
        ring
      rw [heq, integral_const_mul]

/-- The sum of squared characteristic-function increments tends to zero. -/
private theorem tendsto_sum_rowCharFun_sub_one_norm_sq
    (A : NormalizedTriangularArray Omega) (t : Real) :
    Tendsto
      (fun n => ∑ k : Fin (n + 1),
        ‖charFun (A.probabilityMeasure.map (A.increment n k)) t - 1‖ ^ 2)
      atTop (nhds 0) := by
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  have hmom := tendsto_sum_rowSecondMoment_sq A
  rw [Metric.tendsto_nhds]
  rw [Metric.tendsto_nhds] at hmom
  intro delta hdelta
  let C : Real := (t ^ 2 / 2) ^ 2
  by_cases hC : C = 0
  · have ht : t = 0 := by
      dsimp only [C] at hC
      have : t ^ 2 / 2 = 0 := sq_eq_zero_iff.mp hC
      nlinarith
    subst t
    filter_upwards [] with n
    have hzero (k : Fin (n + 1)) :
        charFun (A.probabilityMeasure.map (A.increment n k)) 0 = 1 := by
      letI : IsProbabilityMeasure
          (A.probabilityMeasure.map (A.increment n k)) :=
        A.probabilityMeasure.isProbabilityMeasure_map (A.rowAEMeasurable n k)
      rw [charFun_zero]
      simp
    simp_rw [hzero]
    simpa using hdelta
  · have hCpos : 0 < C := lt_of_le_of_ne (sq_nonneg _) (Ne.symm hC)
    have hev := hmom (delta / C) (div_pos hdelta hCpos)
    filter_upwards [hev] with n hn
    rw [Real.dist_eq, sub_zero] at hn ⊢
    have hmomnonneg : 0 <= ∑ k : Fin (n + 1),
        (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2 :=
      Finset.sum_nonneg fun _ _ => sq_nonneg _
    rw [abs_of_nonneg hmomnonneg] at hn
    rw [abs_of_nonneg (Finset.sum_nonneg fun _ _ => sq_nonneg _)]
    have hterm (k : Fin (n + 1)) :
        ‖charFun (A.probabilityMeasure.map (A.increment n k)) t - 1‖ ^ 2 <=
          C * (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2 := by
      have hbound := norm_charFun_sub_one_le
        (A.rowAEMeasurable n k) (A.rowSquareIntegrable n k)
        (A.rowCentered n k) t
      have hnonneg := norm_nonneg
        (charFun (A.probabilityMeasure.map (A.increment n k)) t - 1)
      have hmomnonneg := (rowSecondMoment_mem_unitInterval A n k).1
      have hmomeq :
          A.probabilityMeasure[(A.increment n k) ^ 2] =
            A.probabilityMeasure[fun omega => A.increment n k omega ^ 2] := by
        rfl
      rw [← hmomeq] at hbound
      dsimp only [C]
      calc
        ‖charFun (A.probabilityMeasure.map (A.increment n k)) t - 1‖ ^ 2
            <= ((t ^ 2 / 2) *
                A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2 :=
          (sq_le_sq₀ hnonneg (mul_nonneg (by positivity) hmomnonneg)).mpr hbound
        _ = (t ^ 2 / 2) ^ 2 *
            (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2 := by ring
    calc
      (∑ k : Fin (n + 1),
        ‖charFun (A.probabilityMeasure.map (A.increment n k)) t - 1‖ ^ 2)
          <= C * ∑ k : Fin (n + 1),
            (A.probabilityMeasure[(A.increment n k) ^ 2]) ^ 2 := by
              rw [Finset.mul_sum]
              exact Finset.sum_le_sum fun k _ => hterm k
      _ < C * (delta / C) := by gcongr
      _ = delta := by field_simp

/-- A quantitative small/large split for the integrated second-order
characteristic-function remainder. -/
private theorem norm_secondOrderRemainder_integral_le
    {X : Omega -> Real} (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P)
    (t epsilon : Real) (hepsilon : 0 < epsilon)
    (hepsilon_t : epsilon * |t| <= 1) :
    ‖∫ omega,
        (cexp (((t * X omega : Real) : Complex) * I) - 1 -
          ((t * X omega : Real) : Complex) * I +
            (((t * X omega) ^ 2 / 2 : Real) : Complex)) ∂P‖ <=
      (epsilon * |t| ^ 3) * P[fun omega => X omega ^ 2] +
        (2 / epsilon ^ 2 + |t| / epsilon + t ^ 2 / 2) *
          truncatedSecondMoment P X epsilon := by
  let g : Omega -> Complex := fun omega =>
    cexp (((t * X omega : Real) : Complex) * I) - 1 -
      ((t * X omega : Real) : Complex) * I +
        (((t * X omega) ^ 2 / 2 : Real) : Complex)
  let C : Real := 2 / epsilon ^ 2 + |t| / epsilon + t ^ 2 / 2
  let tail : Omega -> Real := fun omega =>
    X omega ^ 2 * if epsilon < ‖X omega‖ then 1 else 0
  have hCnonneg : 0 <= C := by
    dsimp only [C]
    positivity
  have hcoefnonneg : 0 <= epsilon * |t| ^ 3 := by positivity
  have htailint : Integrable tail P := by
    dsimp only [tail]
    exact integrable_truncatedSecondMoment_integrand hXmeas hXsq
  have hboundint : Integrable
      (fun omega => (epsilon * |t| ^ 3) * X omega ^ 2 + C * tail omega) P :=
    (hXsq.const_mul _).add (htailint.const_mul _)
  have hpoint (omega : Omega) :
      ‖g omega‖ <= (epsilon * |t| ^ 3) * X omega ^ 2 + C * tail omega := by
    by_cases hlarge : epsilon < ‖X omega‖
    · have hXabs : epsilon < |X omega| := by
        simpa [Real.norm_eq_abs] using hlarge
      have hXabspos : 0 < |X omega| := hepsilon.trans hXabs
      have hXsqpos : 0 < X omega ^ 2 := by
        rw [← sq_abs]
        positivity
      have hone : (1 : Real) <= X omega ^ 2 / epsilon ^ 2 := by
        rw [le_div_iff₀ (sq_pos_of_pos hepsilon)]
        nlinarith [sq_abs (X omega)]
      have habs : |X omega| <= X omega ^ 2 / epsilon := by
        rw [le_div_iff₀ hepsilon]
        rw [← sq_abs]
        nlinarith [abs_nonneg (X omega)]
      have hcrude := CharFunBound.norm_cexp_mul_I_sub_taylor_two_le_crude
        (t * X omega)
      have h2 : (2 : Real) <= (2 / epsilon ^ 2) * X omega ^ 2 := by
        calc
          (2 : Real) = 2 * 1 := by ring
          _ <= 2 * (X omega ^ 2 / epsilon ^ 2) := by gcongr
          _ = (2 / epsilon ^ 2) * X omega ^ 2 := by ring
      have htX : |t * X omega| <= (|t| / epsilon) * X omega ^ 2 := by
        rw [abs_mul]
        calc
          |t| * |X omega| <= |t| * (X omega ^ 2 / epsilon) := by gcongr
          _ = (|t| / epsilon) * X omega ^ 2 := by ring
      have hquad : (t * X omega) ^ 2 / 2 =
          (t ^ 2 / 2) * X omega ^ 2 := by ring
      have hgC : ‖g omega‖ <= C * X omega ^ 2 := by
        dsimp only [g]
        calc
          ‖cexp (((t * X omega : Real) : Complex) * I) - 1 -
              ((t * X omega : Real) : Complex) * I +
                (((t * X omega) ^ 2 / 2 : Real) : Complex)‖
              <= 2 + |t * X omega| + (t * X omega) ^ 2 / 2 := hcrude
          _ = 2 + |t * X omega| + t ^ 2 / 2 * X omega ^ 2 := by rw [hquad]
          _ <= (2 / epsilon ^ 2) * X omega ^ 2 +
              (|t| / epsilon) * X omega ^ 2 +
                (t ^ 2 / 2) * X omega ^ 2 := by gcongr
          _ = (2 / epsilon ^ 2 + |t| / epsilon + t ^ 2 / 2) *
              X omega ^ 2 := by ring
      dsimp only [tail]
      rw [if_pos hlarge]
      have hfirst : 0 <= (epsilon * |t| ^ 3) * X omega ^ 2 := by positivity
      linarith
    · have hXabs : |X omega| <= epsilon := by
        simpa [Real.norm_eq_abs] using le_of_not_gt hlarge
      have htX : |t * X omega| <= 1 := by
        rw [abs_mul]
        calc
          |t| * |X omega| <= |t| * epsilon := by gcongr
          _ = epsilon * |t| := mul_comm _ _
          _ <= 1 := hepsilon_t
      have hsmall := CharFunBound.norm_cexp_mul_I_sub_taylor_two_le htX
      have hcubic : |t * X omega| ^ 3 <=
          (epsilon * |t| ^ 3) * X omega ^ 2 := by
        rw [abs_mul, mul_pow, ← sq_abs (X omega)]
        have hnonneg : 0 <= |t| ^ 3 * |X omega| ^ 2 := by positivity
        calc
          |t| ^ 3 * |X omega| ^ 3 =
              (|t| ^ 3 * |X omega| ^ 2) * |X omega| := by ring
          _ <= (|t| ^ 3 * |X omega| ^ 2) * epsilon := by gcongr
          _ = (epsilon * |t| ^ 3) * |X omega| ^ 2 := by ring
      dsimp only [g] at hsmall ⊢
      dsimp only [tail]
      rw [if_neg hlarge]
      simp only [mul_zero, add_zero]
      exact hsmall.trans hcubic
  change ‖∫ omega, g omega ∂P‖ <= _
  calc
    ‖∫ omega, g omega ∂P‖ <= ∫ omega, ‖g omega‖ ∂P :=
      norm_integral_le_integral_norm _
    _ <= ∫ omega, ((epsilon * |t| ^ 3) * X omega ^ 2 + C * tail omega) ∂P := by
      refine integral_mono_of_nonneg (ae_of_all _ fun _ => norm_nonneg _) hboundint ?_
      exact ae_of_all _ hpoint
    _ = (epsilon * |t| ^ 3) * P[fun omega => X omega ^ 2] + C *
        truncatedSecondMoment P X epsilon := by
      rw [integral_add (hXsq.const_mul _) (htailint.const_mul _),
        integral_const_mul, integral_const_mul]
      rfl

/-- The summed second-order characteristic-function errors vanish under the
frozen Lindeberg condition. -/
private theorem tendsto_sum_rowCharFun_secondOrderError
    (A : NormalizedTriangularArray Omega) (t : Real) :
    Tendsto
      (fun n => ∑ k : Fin (n + 1),
        (charFun (A.probabilityMeasure.map (A.increment n k)) t - 1 +
          (((A.probabilityMeasure[(A.increment n k) ^ 2] * t ^ 2 / 2 : Real)) :
            Complex)))
      atTop (nhds 0) := by
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  by_cases ht : t = 0
  · subst t
    have heq (n : Nat) : (∑ k : Fin (n + 1),
        (charFun (A.probabilityMeasure.map (A.increment n k)) 0 - 1 +
          (((A.probabilityMeasure[(A.increment n k) ^ 2] * 0 ^ 2 / 2 : Real)) :
            Complex))) = 0 := by
      have hzero (k : Fin (n + 1)) :
          charFun (A.probabilityMeasure.map (A.increment n k)) 0 = 1 := by
        letI : IsProbabilityMeasure
            (A.probabilityMeasure.map (A.increment n k)) :=
          A.probabilityMeasure.isProbabilityMeasure_map (A.rowAEMeasurable n k)
        rw [charFun_zero]
        simp
      simp_rw [hzero]
      simp
    simp_rw [heq]
    exact tendsto_const_nhds
  have ht_abs : 0 < |t| := abs_pos.mpr ht
  rw [Metric.tendsto_nhds]
  intro delta hdelta
  let epsilon := min (1 / |t|) (delta / (2 * (|t| ^ 3 + 1)))
  have hepsilon : 0 < epsilon := lt_min (by positivity) (by positivity)
  have hepsilon_t : epsilon * |t| <= 1 := by
    have hle : epsilon <= 1 / |t| := min_le_left _ _
    calc
      epsilon * |t| <= (1 / |t|) * |t| := by gcongr
      _ = 1 := by field_simp
  have hepsilon_t3 : epsilon * |t| ^ 3 <= delta / 2 := by
    have hle : epsilon <= delta / (2 * (|t| ^ 3 + 1)) := min_le_right _ _
    have hp : |t| ^ 3 <= |t| ^ 3 + 1 := by linarith
    calc
      epsilon * |t| ^ 3 <=
          (delta / (2 * (|t| ^ 3 + 1))) * |t| ^ 3 := by gcongr
      _ <= (delta / (2 * (|t| ^ 3 + 1))) * (|t| ^ 3 + 1) := by gcongr
      _ = delta / 2 := by field_simp
  let C : Real := 2 / epsilon ^ 2 + |t| / epsilon + t ^ 2 / 2
  have hCpos : 0 < C := by
    dsimp only [C]
    have hfirst : 0 < 2 / epsilon ^ 2 := by positivity
    have hsecond : 0 <= |t| / epsilon := by positivity
    have hthird : 0 <= t ^ 2 / 2 := by positivity
    linarith
  have htail := A.lindebergCondition epsilon hepsilon
  rw [Metric.tendsto_nhds] at htail
  have htail_small := htail (delta / (2 * C)) (by positivity)
  simp only [Real.dist_eq, sub_zero] at htail_small
  filter_upwards [htail_small] with n hn
  rw [dist_zero_right]
  have htail_nonneg : 0 <= ∑ k : Fin (n + 1),
      truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon :=
    Finset.sum_nonneg fun k _ =>
      truncatedSecondMoment_nonneg A.probabilityMeasure (A.increment n k) epsilon
  have hn' : (∑ k : Fin (n + 1),
      truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon) <
      delta / (2 * C) := by
    rwa [abs_of_nonneg htail_nonneg] at hn
  have heq (k : Fin (n + 1)) :
      charFun (A.probabilityMeasure.map (A.increment n k)) t - 1 +
          (((A.probabilityMeasure[(A.increment n k) ^ 2] * t ^ 2 / 2 : Real)) :
            Complex) =
        ∫ omega,
          (cexp (((t * A.increment n k omega : Real) : Complex) * I) - 1 -
            ((t * A.increment n k omega : Real) : Complex) * I +
              (((t * A.increment n k omega) ^ 2 / 2 : Real) : Complex))
            ∂A.probabilityMeasure :=
    charFun_sub_one_add_quadratic_eq_integral
      (A.rowAEMeasurable n k) (A.rowSquareIntegrable n k)
      (A.rowCentered n k) t
  rw [show (∑ k : Fin (n + 1),
      (charFun (A.probabilityMeasure.map (A.increment n k)) t - 1 +
        (((A.probabilityMeasure[(A.increment n k) ^ 2] * t ^ 2 / 2 : Real)) :
          Complex))) =
      ∑ k : Fin (n + 1),
        ∫ omega,
          (cexp (((t * A.increment n k omega : Real) : Complex) * I) - 1 -
            ((t * A.increment n k omega : Real) : Complex) * I +
              (((t * A.increment n k omega) ^ 2 / 2 : Real) : Complex))
            ∂A.probabilityMeasure by
      exact Finset.sum_congr rfl fun k _ => heq k]
  calc
    ‖∑ k : Fin (n + 1),
        ∫ omega,
          (cexp (((t * A.increment n k omega : Real) : Complex) * I) - 1 -
            ((t * A.increment n k omega : Real) : Complex) * I +
              (((t * A.increment n k omega) ^ 2 / 2 : Real) : Complex))
            ∂A.probabilityMeasure‖
        <= ∑ k : Fin (n + 1),
          ‖∫ omega,
            (cexp (((t * A.increment n k omega : Real) : Complex) * I) - 1 -
              ((t * A.increment n k omega : Real) : Complex) * I +
                (((t * A.increment n k omega) ^ 2 / 2 : Real) : Complex))
              ∂A.probabilityMeasure‖ := norm_sum_le _ _
    _ <= ∑ k : Fin (n + 1),
        ((epsilon * |t| ^ 3) *
            A.probabilityMeasure[(A.increment n k) ^ 2] +
          C * truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon) := by
      exact Finset.sum_le_sum fun k _ => by
        dsimp only [C]
        exact norm_secondOrderRemainder_integral_le
          (A.rowAEMeasurable n k) (A.rowSquareIntegrable n k)
          t epsilon hepsilon hepsilon_t
    _ = epsilon * |t| ^ 3 + C *
        (∑ k : Fin (n + 1),
          truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon) := by
      rw [Finset.sum_add_distrib, ← Finset.mul_sum, rowSecondMoment_sum, mul_one,
        ← Finset.mul_sum]
    _ < delta / 2 + delta / 2 := by
      have htailC : C * (∑ k : Fin (n + 1),
          truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon) <
          delta / 2 := by
        calc
          C * (∑ k : Fin (n + 1),
              truncatedSecondMoment A.probabilityMeasure (A.increment n k) epsilon)
              < C * (delta / (2 * C)) := by gcongr
          _ = delta / 2 := by field_simp
      linarith
    _ = delta := by ring

/-- The row sums of `charFun - 1` converge to the Gaussian logarithmic
coefficient. -/
private theorem tendsto_sum_rowCharFun_sub_one
    (A : NormalizedTriangularArray Omega) (t : Real) :
    Tendsto
      (fun n => ∑ k : Fin (n + 1),
        (charFun (A.probabilityMeasure.map (A.increment n k)) t - 1))
      atTop (nhds (-(t ^ 2 / 2 : Real) : Complex)) := by
  have herr := tendsto_sum_rowCharFun_secondOrderError A t
  have hquad : Tendsto
      (fun _n : Nat => (((t ^ 2 / 2 : Real)) : Complex))
      atTop (nhds (((t ^ 2 / 2 : Real)) : Complex)) := tendsto_const_nhds
  have hsub := herr.sub hquad
  convert hsub using 1
  · funext n
    rw [← rowGaussianQuadraticCoefficient A n t]
    push_cast
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro k _
    ring
  · push_cast
    ring

/-- Pointwise convergence of exact row-law characteristic functions to the
standard Gaussian characteristic function. -/
theorem rowLawCharFunConverges_proof
    (A : NormalizedTriangularArray Omega) :
    RowLawCharFunConverges A := by
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  intro t
  have hsum := tendsto_sum_rowCharFun_sub_one A t
  have hsq := tendsto_sum_rowCharFun_sub_one_norm_sq A t
  have hprod := ProductLimit.tendsto_row_prod_one_add_of_sum_norm_sq hsum hsq
  rw [show (fun n => charFun (A.probabilityMeasure.map (rowSum A n)) t) =
      fun n => ∏ k : Fin (n + 1),
        (1 + (charFun (A.probabilityMeasure.map (A.increment n k)) t - 1)) by
    funext n
    rw [congrFun (rowCharFun_factorization A n) t]
    rw [Finset.prod_apply]
    apply Finset.prod_congr rfl
    intro k _
    ring]
  convert hprod using 1
  rw [charFun_gaussianReal]
  push_cast
  ring_nf

/-- Exact frozen Lindeberg-Feller triangular-array theorem. -/
theorem lindebergFeller_exact : Statement.{u} := by
  intro Omega _ A
  exact root_of_row_charFun_convergence A (rowLawCharFunConverges_proof A)

#print axioms rowSecondMoment_mem_unitInterval
#print axioms secondMoment_le_sq_add_truncated
#print axioms tendsto_sum_rowSecondMoment_sq
#print axioms rowLawCharFunConverges_proof
#print axioms lindebergFeller_exact

end CharacteristicFunctionHelpers

end Stage1Instances.THM_M_0989
