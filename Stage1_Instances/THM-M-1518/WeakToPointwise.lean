import «Stage1_Instances».«THM-M-1518».ObligationTree
import Mathlib.Analysis.Distribution.AEEqOfIntegralContDiff
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.ContDiff.FiniteDimension
import Mathlib.Analysis.Calculus.Deriv.Support
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Measure.OpenPos
import Mathlib.LinearAlgebra.StdBasis

noncomputable section

open Set MeasureTheory

namespace Stage1Instances.THM_M_1518.ObligationTree

open Stage1Instances.THM_M_1518

/-- The weak variational identity implies the strong derivative equation for
continuously differentiable continuous-linear-map-valued coefficients. -/
theorem weak_to_pointwise_abstract
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (a b : ℝ) (hab : a < b)
    (A P : ℝ → E →L[ℝ] ℝ)
    (hA : ContDiff ℝ 1 A) (hP : ContDiff ℝ 1 P)
    (hweak : ∀ η : ℝ → E, ContDiff ℝ 1 η → η a = 0 → η b = 0 →
      ∫ t in a..b, A t (η t) + P t (deriv η t) = 0) :
    ∀ t ∈ Ioo a b, HasDerivAt P (A t) t := by
  have _ := hab
  have hPd : Differentiable ℝ P := hP.differentiable one_ne_zero
  have hAd : Continuous A := hA.continuous
  have hdP : Continuous (deriv P) := hP.continuous_deriv_one
  intro t ht
  have hderiv : deriv P t = A t := by
    ext v
    let r : ℝ → ℝ := fun x ↦ A x v - deriv P x v
    have hr : Continuous r :=
      (hAd.clm_apply continuous_const).sub (hdP.clm_apply continuous_const)
    have hPv : ∀ x, HasDerivAt (fun y ↦ P y v) (deriv P x v) x := by
      intro x
      simpa using (hPd x).hasDerivAt.clm_apply (hasDerivAt_const x v)
    have hae : ∀ᵐ x ∂volume, x ∈ Ioo a b → r x = 0 := by
      apply isOpen_Ioo.ae_eq_zero_of_integral_contDiff_smul_eq_zero
      · exact hr.continuousOn.locallyIntegrableOn measurableSet_Ioo
      · intro g hg hgc hgs
        have hgd : Differentiable ℝ g :=
          (hg.of_le (by simp)).differentiable one_ne_zero
        have hg1 : ContDiff ℝ 1 g := hg.of_le (by simp)
        have hga : g a = 0 := by
          by_contra hga
          exact (lt_irrefl a)
            (hgs (subset_tsupport g (Function.mem_support.mpr hga))).1
        have hgb : g b = 0 := by
          by_contra hgb
          exact (lt_irrefl b)
            (hgs (subset_tsupport g (Function.mem_support.mpr hgb))).2
        let η : ℝ → E := fun x ↦ g x • v
        have hη1 : ContDiff ℝ 1 η := hg1.smul_const v
        have hηa : η a = 0 := by simp [η, hga]
        have hηb : η b = 0 := by simp [η, hgb]
        have hηderiv : ∀ x, deriv η x = deriv g x • v := by
          intro x
          exact deriv_smul_const (hgd x) v
        have hw := hweak η hη1 hηa hηb
        simp_rw [hηderiv] at hw
        simp only [map_smul, smul_eq_mul] at hw
        have hw' : ∫ t in a..b, g t * A t v + deriv g t * P t v = 0 := by
          simpa [η] using hw
        have hgA_int : IntervalIntegrable (fun x ↦ g x * A x v) volume a b :=
          (hg.continuous.mul
            (hAd.clm_apply continuous_const)).intervalIntegrable a b
        have hdgP_int :
            IntervalIntegrable (fun x ↦ deriv g x * P x v) volume a b :=
          (hg1.continuous_deriv_one.mul
            (hP.continuous.clm_apply continuous_const)).intervalIntegrable a b
        rw [intervalIntegral.integral_add hgA_int hdgP_int] at hw'
        have hgDP_int :
            IntervalIntegrable (fun x ↦ g x * deriv P x v) volume a b :=
          (hg.continuous.mul
            (hdP.clm_apply continuous_const)).intervalIntegrable a b
        have hdg_int : IntervalIntegrable (deriv g) volume a b :=
          hg1.continuous_deriv_one.intervalIntegrable a b
        have hdPv_int :
            IntervalIntegrable (fun x ↦ deriv P x v) volume a b :=
          (hdP.clm_apply continuous_const).intervalIntegrable a b
        have hibp := intervalIntegral.integral_mul_deriv_eq_deriv_mul
          (a := a) (b := b)
          (u := g) (u' := deriv g)
          (v := fun x ↦ P x v) (v' := fun x ↦ deriv P x v)
          (fun x _ ↦ (hgd x).hasDerivAt) (fun x _ ↦ hPv x)
          hdg_int hdPv_int
        have hinterval : ∫ x in a..b, g x * r x = 0 := by
          simp only [r, mul_sub]
          rw [intervalIntegral.integral_sub hgA_int hgDP_int, hibp]
          simpa [hga, hgb] using hw'
        have hsupp : Function.support (fun x ↦ g x • r x) ⊆ Ioc a b := by
          intro x hx
          have hgx : g x ≠ 0 := by
            intro hgx
            apply hx
            simp [hgx]
          exact Ioo_subset_Ioc_self
            (hgs (subset_tsupport g (Function.mem_support.mpr hgx)))
        rw [← intervalIntegral.integral_eq_integral_of_support_subset hsupp]
        simpa [smul_eq_mul] using hinterval
    have hae' : r =ᵐ[volume.restrict (Ioo a b)] (fun _ ↦ 0) := by
      have hae0 : ∀ᵐ x ∂volume.restrict (Ioo a b), r x = 0 := by
        rw [ae_restrict_iff' measurableSet_Ioo]
        exact hae
      filter_upwards [hae0] with x hx
      simpa using hx
    have hrzero : EqOn r (fun _ ↦ 0) (Ioo a b) :=
      Measure.eqOn_open_of_ae_eq hae' isOpen_Ioo
        hr.continuousOn continuousOn_const
    exact (sub_eq_zero.mp (hrzero ht)).symm
  simpa only [hderiv] using (hPd t).hasDerivAt

/-- The position partial derivative along a `C²` path is continuously
differentiable. -/
private theorem position_contDiff {n : Nat}
    (L : ℝ × (Configuration n × Configuration n) → ℝ) (q : Path n)
    (hL : ContDiff ℝ 2 L) (hq : ContDiff ℝ 2 q) :
    ContDiff ℝ 1 (fun t => PositionDerivative L t (q t) (deriv q t)) := by
  let jet : ℝ → ℝ × (Configuration n × Configuration n) :=
    fun t => (t, (q t, deriv q t))
  have hjet : ContDiff ℝ 1 jet := by
    exact contDiff_id.prodMk
      ((hq.of_le (by norm_num)).prodMk (hq.deriv' (n := 1)))
  let inPos : Configuration n →L[ℝ] ℝ × (Configuration n × Configuration n) :=
    (ContinuousLinearMap.inr ℝ ℝ (Configuration n × Configuration n)).comp
      (ContinuousLinearMap.inl ℝ (Configuration n) (Configuration n))
  have hfull : ContDiff ℝ 1 (fun t => (fderiv ℝ L (jet t)).comp inPos) := by
    exact ((hL.fderiv_right (m := 1) (by norm_num)).comp hjet).clm_comp
      contDiff_const
  convert hfull using 1
  funext t
  rw [PositionDerivative]
  have hdL : DifferentiableAt ℝ L (jet t) :=
    (hL.differentiable (by norm_num)) _
  have hins : DifferentiableAt ℝ
      (fun y : Configuration n => (t, y, deriv q t)) (q t) := by
    fun_prop
  have hinner :
      fderiv ℝ (fun y : Configuration n => (t, y, deriv q t)) (q t) = inPos := by
    exact (show HasFDerivAt
      (fun y : Configuration n => (t, (y, deriv q t))) inPos (q t) by
        fun_prop).fderiv
  rw [fderiv_comp' (x := q t) hdL hins, hinner]

/-- The velocity partial derivative along a `C²` path is continuously
differentiable. -/
private theorem velocity_contDiff {n : Nat}
    (L : ℝ × (Configuration n × Configuration n) → ℝ) (q : Path n)
    (hL : ContDiff ℝ 2 L) (hq : ContDiff ℝ 2 q) :
    ContDiff ℝ 1 (fun t => VelocityDerivative L t (q t) (deriv q t)) := by
  let jet : ℝ → ℝ × (Configuration n × Configuration n) :=
    fun t => (t, (q t, deriv q t))
  have hjet : ContDiff ℝ 1 jet := by
    exact contDiff_id.prodMk
      ((hq.of_le (by norm_num)).prodMk (hq.deriv' (n := 1)))
  let inVel : Configuration n →L[ℝ] ℝ × (Configuration n × Configuration n) :=
    (ContinuousLinearMap.inr ℝ ℝ (Configuration n × Configuration n)).comp
      (ContinuousLinearMap.inr ℝ (Configuration n) (Configuration n))
  have hfull : ContDiff ℝ 1 (fun t => (fderiv ℝ L (jet t)).comp inVel) := by
    exact ((hL.fderiv_right (m := 1) (by norm_num)).comp hjet).clm_comp
      contDiff_const
  convert hfull using 1
  funext t
  rw [VelocityDerivative]
  have hdL : DifferentiableAt ℝ L (jet t) :=
    (hL.differentiable (by norm_num)) _
  have hins : DifferentiableAt ℝ
      (fun w : Configuration n => (t, q t, w)) (deriv q t) := by
    fun_prop
  have hinner :
      fderiv ℝ (fun w : Configuration n => (t, q t, w)) (deriv q t) = inVel := by
    exact (show HasFDerivAt
      (fun w : Configuration n => (t, (q t, w))) inVel (deriv q t) by
        fun_prop).fderiv
  rw [fderiv_comp' (x := deriv q t) hdL hins, hinner]

/-- Inhabitant of the frozen integration-by-parts and fundamental-lemma
package. -/
theorem weakToPointwise : WeakToPointwise := by
  intro n L B q hL hq hw
  apply weak_to_pointwise_abstract
      B.initialTime B.finalTime B.timeOrder
      (fun t => PositionDerivative L t (q t) (deriv q t))
      (fun t => VelocityDerivative L t (q t) (deriv q t))
      (position_contDiff L q hL hq) (velocity_contDiff L q hL hq)
  intro η hη hηa hηb
  exact hw η ⟨hη, hηa, hηb⟩

#check weakToPointwise
#print axioms weakToPointwise

end Stage1Instances.THM_M_1518.ObligationTree
