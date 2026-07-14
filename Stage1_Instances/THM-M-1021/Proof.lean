import External.Bochner.Main
import «Stage1_Instances».«THM-M-1021».BochnerStatement
import Mathlib.MeasureTheory.Measure.CharacteristicFunction.TaylorExpansion

open scoped BigOperators
open MeasureTheory

namespace AwesomeTheorems.Stage1.THM_M_1021

/-- The explicit integral convention in the frozen target is exactly mathlib's
real characteristic-function convention. -/
lemma targetIntegral_eq_charFun (mu : Measure Real) (s : Real) :
    integral mu (fun x : Real =>
      Complex.exp (Complex.I * (s : Complex) * (x : Complex))) = charFun mu s := by
  rw [charFun_apply_real]
  congr with x
  congr 1
  ring

private noncomputable def wave (t : Real) (x : Real) : Complex :=
  Complex.exp (Complex.I * (t : Complex) * (x : Complex))

private lemma wave_eq_innerProbChar (t x : Real) :
    wave t x = BoundedContinuousFunction.innerProbChar t x := by
  rw [BoundedContinuousFunction.innerProbChar_apply]
  dsimp [wave]
  congr 1
  change Complex.I * t * x = (inner Real x t : Complex) * Complex.I
  change Complex.I * t * x =
    (RCLike.re (t * starRingEnd Real x) : Complex) * Complex.I
  simp
  ring

private lemma wave_integrable (mu : Measure Real) [IsFiniteMeasure mu] (t : Real) :
    Integrable (wave t) mu := by
  have h := BoundedContinuousFunction.integrable mu
    (BoundedContinuousFunction.innerProbChar t)
  exact h.congr (ae_of_all _ fun x => (wave_eq_innerProbChar t x).symm)

private lemma wave_sub (s t x : Real) :
    wave (s - t) x = wave s x * star (wave t x) := by
  dsimp [wave]
  calc
    _ = Complex.exp (Complex.I * (s : Complex) * (x : Complex)) *
        Complex.exp (starRingEnd Complex
          (Complex.I * (t : Complex) * (x : Complex))) := by
      rw [← Complex.exp_add]
      congr 1
      simp
      ring
    _ = Complex.exp (Complex.I * (s : Complex) * (x : Complex)) *
        starRingEnd Complex
          (Complex.exp (Complex.I * (t : Complex) * (x : Complex))) := by
      rw [Complex.exp_conj]

private lemma quadratic_integral (mu : Measure Real) [IsFiniteMeasure mu]
    (n : Nat) (t : Fin n -> Real) (c : Fin n -> Complex) :
    (Finset.univ.sum fun j => Finset.univ.sum fun k =>
      c j * star (c k) * charFun mu (t j - t k)) =
      integral mu (fun x => Complex.normSq
        (Finset.univ.sum fun j => star (c j * wave (t j) x))) := by
  calc
    _ = Finset.univ.sum fun j => Finset.univ.sum fun k =>
        c j * star (c k) * integral mu (wave (t j - t k)) := by
          congr 1 with j
          congr 1 with k
          rw [charFun_apply_real]
          congr 2
          funext x
          dsimp [wave]
          congr 1
          push_cast
          ring
    _ = Finset.univ.sum fun j => Finset.univ.sum fun k =>
        integral mu (fun x => c j * star (c k) * wave (t j - t k) x) := by
          apply Finset.sum_congr rfl
          intro j hj
          apply Finset.sum_congr rfl
          intro k hk
          simpa only [mul_assoc] using
            (integral_const_mul (c j * star (c k)) (wave (t j - t k))).symm
    _ = integral mu (fun x => Finset.univ.sum fun j => Finset.univ.sum fun k =>
        c j * star (c k) * wave (t j - t k) x) := by
          calc
            _ = Finset.univ.sum fun j => integral mu (fun x =>
                Finset.univ.sum fun k =>
                  c j * star (c k) * wave (t j - t k) x) := by
              apply Finset.sum_congr rfl
              intro j hj
              exact (integral_finset_sum _ fun k _ => by
                simpa only [mul_assoc] using
                  (wave_integrable mu (t j - t k)).const_mul
                    (c j * star (c k))).symm
            _ = _ := by
              exact (integral_finset_sum _ fun j _ =>
                integrable_finset_sum _ fun k _ => by
                  simpa only [mul_assoc] using
                    (wave_integrable mu (t j - t k)).const_mul
                      (c j * star (c k))).symm
    _ = integral mu (fun x =>
        ((Complex.normSq
          (Finset.univ.sum fun j => star (c j * wave (t j) x)) : Real) : Complex)) := by
          congr 1
          funext x
          rw [Complex.normSq_eq_conj_mul_self]
          simp only [map_sum, starRingEnd_apply, star_star]
          rw [Finset.sum_mul_sum]
          apply Finset.sum_congr rfl
          intro j hj
          apply Finset.sum_congr rfl
          intro k hk
          rw [wave_sub]
          rw [star_mul]
          ring
    _ = integral mu (fun x => Complex.normSq
        (Finset.univ.sum fun j => star (c j * wave (t j) x))) := by
          exact integral_ofReal

private lemma charFun_positiveDefinite (mu : Measure Real) [IsProbabilityMeasure mu] :
    IsPositiveDefinite (charFun mu) := by
  intro n t c
  let r : Real := integral mu (fun x => Complex.normSq
    (Finset.univ.sum fun j => star (c j * wave (t j) x)))
  refine ⟨r, ?_, ?_⟩
  · exact integral_nonneg fun x => Complex.normSq_nonneg _
  · rw [quadratic_integral]

/-- The positive-definiteness branch of the forward implication. -/
lemma characteristicFunction_positiveDefinite {phi : Real -> Complex}
    (hphi : IsCharacteristicFunction phi) : IsPositiveDefinite phi := by
  obtain ⟨mu, hmu, hphi⟩ := hphi
  letI : IsProbabilityMeasure mu := hmu
  have heq : phi = charFun mu := by
    funext s
    rw [hphi s, targetIntegral_eq_charFun]
  rw [heq]
  exact charFun_positiveDefinite mu

/-- The continuity branch of the forward implication. -/
lemma characteristicFunction_continuous {phi : Real -> Complex}
    (hphi : IsCharacteristicFunction phi) : Continuous phi := by
  obtain ⟨mu, hmu, hphi⟩ := hphi
  haveI : IsProbabilityMeasure mu := hmu
  have heq : phi = charFun mu := by
    funext s
    rw [hphi s, targetIntegral_eq_charFun]
  rw [heq]
  exact continuous_charFun

/-- The value-at-zero branch of the forward implication. -/
lemma characteristicFunction_zero {phi : Real -> Complex}
    (hphi : IsCharacteristicFunction phi) : phi 0 = 1 := by
  obtain ⟨mu, hmu, hphi⟩ := hphi
  haveI : IsProbabilityMeasure mu := hmu
  rw [hphi 0, targetIntegral_eq_charFun]
  simp

/-- The full forward implication of the frozen Bochner target. -/
theorem bochner_forward (phi : Real -> Complex) :
    IsCharacteristicFunction phi ->
      Continuous phi /\ phi 0 = 1 /\ IsPositiveDefinite phi := by
  intro hphi
  exact ⟨characteristicFunction_continuous hphi,
    characteristicFunction_zero hphi,
    characteristicFunction_positiveDefinite hphi⟩

/-- The frozen quadratic-form predicate supplies the Hermitian condition used
by the vendored Bochner theorem. -/
private lemma frozen_hermitian {phi : Real -> Complex}
    (hpd : IsPositiveDefinite phi) (x : Real) :
    phi (-x) = star phi x := by
  obtain ⟨r0, hr0, h0⟩ := hpd 1 ![0] ![1]
  obtain ⟨r1, hr1, h1⟩ := hpd 2 ![x, 0] ![1, 1]
  obtain ⟨ri, hri, hi⟩ := hpd 2 ![x, 0] ![1, Complex.I]
  have h0im : (phi 0).im = 0 := by
    have him := congrArg Complex.im h0
    simpa [Fin.sum_univ_one] using him
  have h1im : (phi x).im + (phi (-x)).im = 0 := by
    have him := congrArg Complex.im h1
    simpa [Fin.sum_univ_two, h0im] using him
  have hiim : -(phi x).re + (phi (-x)).re = 0 := by
    have him := congrArg Complex.im hi
    simpa [Fin.sum_univ_two, h0im] using him
  apply Complex.ext
  · show (phi (-x)).re = (phi x).re
    linarith [hiim]
  · show (phi (-x)).im = -(phi x).im
    linarith [h1im]

/-- Transport the frozen real-witness condition to the vendored library's
Hermitian/nonnegative-real-part condition. -/
private lemma frozen_to_external {phi : Real -> Complex}
    (hpd : IsPositiveDefinite phi) : _root_.IsPositiveDefinite phi := by
  constructor
  · exact frozen_hermitian hpd
  · intro n t c
    obtain ⟨r, hr, heq⟩ := hpd n t (fun i => star (c i))
    have hre := congrArg Complex.re heq
    simp only [star_star, Complex.ofReal_re] at hre
    change 0 ≤ (Finset.univ.sum fun i => Finset.univ.sum fun j =>
      star (c i) * c j * phi (t i - t j)).re
    rw [hre]
    exact hr

/-- Reverse implication through the immutable vendored Bochner body. -/
theorem bochner_reverse (phi : Real -> Complex)
    (hcont : Continuous phi) (hzero : phi 0 = 1)
    (hpd : IsPositiveDefinite phi) : IsCharacteristicFunction phi := by
  obtain ⟨mu, hmu, _⟩ := bochner_theorem phi hcont (frozen_to_external hpd) hzero
  refine ⟨(mu : Measure Real), mu.prop, fun s => ?_⟩
  rw [targetIntegral_eq_charFun]
  exact (hmu s).symm

/-- Exact root, composed from separately checked forward and reverse bodies. -/
theorem bochner_exact (phi : Real -> Complex) : BochnerTarget phi := by
  constructor
  · exact bochner_forward phi
  · rintro ⟨hcont, hzero, hpd⟩
    exact bochner_reverse phi hcont hzero hpd

#check bochner_forward
#check bochner_reverse
#check bochner_exact

#print sorries bochner_forward
#print sorries bochner_reverse
#print sorries bochner_exact

#print axioms bochner_forward
#print axioms bochner_reverse
#print axioms bochner_exact

end AwesomeTheorems.Stage1.THM_M_1021
