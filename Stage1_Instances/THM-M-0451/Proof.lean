import ObligationTree
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# THM-M-0451 partial proof bodies

This module implements the analytic Tate limiting argument downstream of the
still-open elliptic-curve height estimates.  It derives the exact limit,
comparison, doubling, nonnegativity, parallelogram, integer-square, and
torsion-to-zero laws from explicit premises.  No estimate is assumed to exist
here and the exact Neron-Tate root remains open.
-/

noncomputable section

open Filter
open scoped Topology WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0451

universe u

namespace Proof

/-- The comparison height used by the frozen target. -/
def naiveHeight {K : Type u} [Field K] [NumberField K]
    {E : WeierstrassCurve K} (P : E⟮K⟯) : ℝ :=
  xHeight P / 2

/-- The dyadic self-map on an additive group. -/
def doublePoint {G : Type*} [AddMonoid G] (P : G) : G :=
  (2 : ℕ) • P

/-- The normalized Tate sequence for a self-map with expected expansion
factor `r`. -/
def tateSequence {S : Type*} (φ : S → S) (h : S → ℝ) (r : ℝ)
    (x : S) (n : ℕ) : ℝ :=
  h (φ^[n] x) / r ^ n

/-- Consecutive terms of the Tate sequence are controlled by the rescaled
one-step error. -/
lemma tateSequence_dist {S : Type*} (φ : S → S) (h : S → ℝ)
    (r : ℝ) (hr : 1 < r) (C : ℝ)
    (hbound : ∀ x, |h (φ x) - r * h x| ≤ C) (x : S) (n : ℕ) :
    dist (tateSequence φ h r x n) (tateSequence φ h r x (n + 1)) ≤
      C / r ^ (n + 1) := by
  rw [Real.dist_eq]
  have hr_pos : (0 : ℝ) < r := by linarith
  have hrn1_pos : (0 : ℝ) < r ^ (n + 1) := pow_pos hr_pos (n + 1)
  simp only [tateSequence, Function.iterate_succ', Function.comp_def]
  have key : h (φ^[n] x) / r ^ n - h (φ (φ^[n] x)) / r ^ (n + 1) =
      (r * h (φ^[n] x) - h (φ (φ^[n] x))) / r ^ (n + 1) := by
    rw [pow_succ']
    field_simp
  rw [key, abs_div, abs_of_pos hrn1_pos, abs_sub_comm]
  exact div_le_div_of_nonneg_right (hbound (φ^[n] x)) hrn1_pos.le

/-- The geometric error series used by the Tate construction is summable. -/
lemma summable_tate_bound {r : ℝ} (hr : 1 < r) (C : ℝ) :
    Summable (fun n : ℕ ↦ C / r ^ (n + 1)) := by
  have hinv_nn : 0 ≤ r⁻¹ := by positivity
  have hinv : r⁻¹ < 1 := inv_lt_one_of_one_lt₀ hr
  have hseq : (fun n : ℕ ↦ C / r ^ (n + 1)) =
      fun n ↦ C / r * (r⁻¹) ^ n := by
    ext n
    simp [pow_succ', div_mul_eq_mul_div]
    ring
  rw [hseq]
  exact (summable_geometric_of_lt_one hinv_nn hinv).mul_left (C / r)

/-- A uniformly bounded expansion error makes every Tate sequence Cauchy. -/
lemma tateSequence_cauchy {S : Type*} (φ : S → S) (h : S → ℝ)
    (r : ℝ) (hr : 1 < r) (C : ℝ)
    (hbound : ∀ x, |h (φ x) - r * h x| ≤ C) (x : S) :
    CauchySeq (tateSequence φ h r x) :=
  cauchySeq_of_dist_le_of_summable _
    (tateSequence_dist φ h r hr C hbound x) (summable_tate_bound hr C)

/-- The canonical value selected by the Tate construction. -/
def tateLimit {S : Type*} (φ : S → S) (h : S → ℝ) (r : ℝ)
    (x : S) : ℝ :=
  limUnder atTop (tateSequence φ h r x)

/-- The Tate sequence converges to the selected limit. -/
lemma tateSequence_tendsto {S : Type*} (φ : S → S) (h : S → ℝ)
    (r : ℝ) (hr : 1 < r) (C : ℝ)
    (hbound : ∀ x, |h (φ x) - r * h x| ≤ C) (x : S) :
    Tendsto (tateSequence φ h r x) atTop (nhds (tateLimit φ h r x)) := by
  exact (tateSequence_cauchy φ h r hr C hbound x).tendsto_limUnder

/-- The Tate limit stays uniformly close to the original height. -/
lemma tateLimit_sub_le {S : Type*} (φ : S → S) (h : S → ℝ)
    (r : ℝ) (hr : 1 < r) (C : ℝ)
    (hbound : ∀ x, |h (φ x) - r * h x| ≤ C) (x : S) :
    |tateLimit φ h r x - h x| ≤ C / (r - 1) := by
  have htend := tateSequence_tendsto φ h r hr C hbound x
  have hd := dist_le_tsum_of_dist_le_of_tendsto₀ _
    (tateSequence_dist φ h r hr C hbound x) (summable_tate_bound hr C) htend
  have hsum : ∑' n : ℕ, C / r ^ (n + 1) = C / (r - 1) := by
    have hinv_nn : 0 ≤ r⁻¹ := by positivity
    have hinv : r⁻¹ < 1 := inv_lt_one_of_one_lt₀ hr
    have hseq : (fun n : ℕ ↦ C / r ^ (n + 1)) =
        fun n ↦ C / r * (r⁻¹) ^ n := by
      ext n
      simp [pow_succ', div_mul_eq_mul_div]
      ring
    rw [hseq, tsum_mul_left, tsum_geometric_of_lt_one hinv_nn hinv]
    rw [show (1 : ℝ) - r⁻¹ = (r - 1) / r by field_simp]
    field_simp
  simpa [tateSequence, tateLimit, Real.dist_eq, abs_sub_comm, hsum] using hd

/-- The Tate limit scales exactly under the expanding self-map. -/
lemma tateLimit_map {S : Type*} (φ : S → S) (h : S → ℝ)
    (r : ℝ) (hr : 1 < r) (C : ℝ)
    (hbound : ∀ x, |h (φ x) - r * h x| ≤ C) (x : S) :
    tateLimit φ h r (φ x) = r * tateLimit φ h r x := by
  have hseq : tateSequence φ h r (φ x) =
      fun n => r * tateSequence φ h r x (n + 1) := by
    funext n
    simp only [tateSequence]
    rw [show φ^[n] (φ x) = φ^[n + 1] x from
      (Function.iterate_succ_apply φ n x).symm, pow_succ']
    field_simp
  have hshift : Tendsto (fun n => tateSequence φ h r x (n + 1)) atTop
      (nhds (tateLimit φ h r x)) :=
    (tateSequence_tendsto φ h r hr C hbound x).comp (tendsto_add_atTop_nat 1)
  have htend : Tendsto (tateSequence φ h r (φ x)) atTop
      (nhds (r * tateLimit φ h r x)) := by
    rw [hseq]
    exact hshift.const_mul r
  exact htend.limUnder_eq

/-- Iterating doubling `n` times is multiplication by `2^n`. -/
lemma doublePoint_iterate {G : Type*} [AddMonoid G] (P : G) (n : ℕ) :
    doublePoint^[n] P = ((2 : ℕ) ^ n) • P := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      simp only [doublePoint, ih, pow_succ]
      rw [mul_comm, mul_smul]

/-- The generic sequence specializes definitionally to the exact normalized
sequence frozen in `Statement.lean`. -/
lemma tateSequence_eq_target_sequence
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K}
    [E.IsElliptic]
    (P : E⟮K⟯) (n : ℕ) :
    tateSequence doublePoint naiveHeight 4 P n =
      (4 : ℝ) ^ (-(n : ℤ)) * xHeight (((2 : ℕ) ^ n) • P) / 2 := by
  rw [tateSequence, doublePoint_iterate]
  simp only [naiveHeight]
  rw [zpow_neg, zpow_natCast]
  field_simp

/-- The canonical height constructed from the exact frozen naive height. -/
def constructedCanonicalHeight
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K}
    [E.IsElliptic]
    (P : E⟮K⟯) : ℝ :=
  tateLimit doublePoint naiveHeight 4 P

/-- `M0451-LIMIT`: convergence of the exact frozen sequence follows from a
uniform doubling estimate for the exact comparison height. -/
theorem limit_formula_of_doubling_bound
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K}
    [E.IsElliptic]
    (C : ℝ)
    (hbound : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ C) :
    ∀ P : E⟮K⟯,
      Tendsto (fun n : ℕ ↦ (4 : ℝ) ^ (-(n : ℤ)) *
        xHeight (((2 : ℕ) ^ n) • P) / 2) atTop
        (nhds (constructedCanonicalHeight P)) := by
  intro P
  simpa only [← tateSequence_eq_target_sequence P] using
    tateSequence_tendsto doublePoint naiveHeight 4 (by norm_num) C hbound P

/-- `M0451-BOUNDED`: the constructed height differs uniformly from the exact
comparison height whenever the same doubling estimate is supplied. -/
theorem bounded_difference_of_doubling_bound
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K}
    [E.IsElliptic]
    (C : ℝ)
    (hbound : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ C) :
    ∃ D : ℝ, ∀ P : E⟮K⟯,
      |constructedCanonicalHeight P - xHeight P / 2| ≤ D := by
  refine ⟨C / (4 - 1), fun P ↦ ?_⟩
  simpa only [naiveHeight] using
    tateLimit_sub_le doublePoint naiveHeight 4 (by norm_num) C hbound P

/-- The construction satisfies the exact doubling law under the same one-step
estimate used for convergence. -/
theorem constructedCanonicalHeight_double
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic]
    (C : ℝ)
    (hbound : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ C) :
    ∀ P : E⟮K⟯,
      constructedCanonicalHeight (doublePoint P) =
        4 * constructedCanonicalHeight P := by
  intro P
  exact tateLimit_map doublePoint naiveHeight 4 (by norm_num) C hbound P

/-- The exact comparison height is nonnegative. -/
lemma naiveHeight_nonnegative
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K}
    [E.IsElliptic]
    (P : E⟮K⟯) : 0 ≤ naiveHeight P := by
  exact div_nonneg (Height.logHeight_nonneg P.xRep) (by norm_num)

/-- `M0451-NONNEGATIVE`: the constructed height is nonnegative once its
convergence is supplied by the doubling estimate. -/
theorem constructedCanonicalHeight_nonnegative
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K}
    [E.IsElliptic]
    (C : ℝ)
    (hbound : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ C) :
    ∀ P : E⟮K⟯, 0 ≤ constructedCanonicalHeight P := by
  intro P
  apply ge_of_tendsto
    (tateSequence_tendsto doublePoint naiveHeight 4 (by norm_num) C hbound P)
  exact Eventually.of_forall fun n =>
    div_nonneg (naiveHeight_nonnegative (doublePoint^[n] P)) (by positivity)

/-- A uniform approximate parallelogram law becomes exact after dyadic
normalization. -/
lemma tateLimit_parallelogram {G : Type*} [AddCommGroup G]
    (h : G → ℝ) (Cdouble Cpar : ℝ)
    (hdouble : ∀ P, |h (doublePoint P) - 4 * h P| ≤ Cdouble)
    (hpar : ∀ P Q,
      |h (P + Q) + h (P - Q) - 2 * h P - 2 * h Q| ≤ Cpar)
    (P Q : G) :
    tateLimit doublePoint h 4 (P + Q) + tateLimit doublePoint h 4 (P - Q) =
      2 * tateLimit doublePoint h 4 P + 2 * tateLimit doublePoint h 4 Q := by
  have ht (R : G) : Tendsto (tateSequence doublePoint h 4 R) atTop
      (nhds (tateLimit doublePoint h 4 R)) :=
    tateSequence_tendsto doublePoint h 4 (by norm_num) Cdouble hdouble R
  have hlimit : Tendsto
      (fun n : ℕ =>
        tateSequence doublePoint h 4 (P + Q) n +
          tateSequence doublePoint h 4 (P - Q) n -
          2 * tateSequence doublePoint h 4 P n -
          2 * tateSequence doublePoint h 4 Q n)
      atTop (nhds
        (tateLimit doublePoint h 4 (P + Q) +
          tateLimit doublePoint h 4 (P - Q) -
          2 * tateLimit doublePoint h 4 P -
          2 * tateLimit doublePoint h 4 Q)) :=
    (((ht (P + Q)).add (ht (P - Q))).sub ((ht P).const_mul 2)).sub
      ((ht Q).const_mul 2)
  have hzero : Tendsto
      (fun n : ℕ =>
        tateSequence doublePoint h 4 (P + Q) n +
          tateSequence doublePoint h 4 (P - Q) n -
          2 * tateSequence doublePoint h 4 P n -
          2 * tateSequence doublePoint h 4 Q n)
      atTop (nhds 0) := by
    have hnorm : ∀ n : ℕ,
        |tateSequence doublePoint h 4 (P + Q) n +
            tateSequence doublePoint h 4 (P - Q) n -
            2 * tateSequence doublePoint h 4 P n -
            2 * tateSequence doublePoint h 4 Q n| ≤ Cpar / (4 : ℝ) ^ n := by
      intro n
      simp only [tateSequence, doublePoint_iterate]
      rw [nsmul_add, nsmul_sub]
      have hp := hpar (((2 : ℕ) ^ n) • P) (((2 : ℕ) ^ n) • Q)
      have hden : (0 : ℝ) < 4 ^ n := pow_pos (by norm_num) n
      have heq :
          h (2 ^ n • P + 2 ^ n • Q) / 4 ^ n +
                h (2 ^ n • P - 2 ^ n • Q) / 4 ^ n -
                2 * (h (2 ^ n • P) / 4 ^ n) -
                2 * (h (2 ^ n • Q) / 4 ^ n) =
            (h (2 ^ n • P + 2 ^ n • Q) +
                h (2 ^ n • P - 2 ^ n • Q) -
                2 * h (2 ^ n • P) - 2 * h (2 ^ n • Q)) / 4 ^ n := by
        ring
      rw [heq, abs_div, abs_of_pos hden]
      exact div_le_div_of_nonneg_right hp hden.le
    have hright : Tendsto (fun n : ℕ => Cpar / (4 : ℝ) ^ n)
        atTop (nhds 0) := by
      rw [show (fun n : ℕ => Cpar / (4 : ℝ) ^ n) =
          fun n => Cpar * ((4 : ℝ)⁻¹ ^ n) from by
        ext n
        rw [div_eq_mul_inv, inv_pow]]
      simpa using (tendsto_pow_atTop_nhds_zero_of_lt_one (r := (4 : ℝ)⁻¹)
        (by norm_num) (by norm_num)).const_mul Cpar
    simpa only [Real.norm_eq_abs] using squeeze_zero_norm hnorm hright
  have huniq := tendsto_nhds_unique hlimit hzero
  linarith

/-- `M0451-PARALLELOGRAM`: an approximate parallelogram estimate for the
exact comparison height yields the exact law for the constructed height. -/
theorem constructedCanonicalHeight_parallelogram_of_bounds
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic]
    (Cdouble Cpar : ℝ)
    (hdouble : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ Cdouble)
    (hpar : ∀ P Q : E⟮K⟯,
      |naiveHeight (P + Q) + naiveHeight (P - Q) -
        2 * naiveHeight P - 2 * naiveHeight Q| ≤ Cpar) :
    ∀ P Q : E⟮K⟯,
      constructedCanonicalHeight (P + Q) + constructedCanonicalHeight (P - Q) =
        2 * constructedCanonicalHeight P + 2 * constructedCanonicalHeight Q := by
  exact tateLimit_parallelogram naiveHeight Cdouble Cpar hdouble hpar

/-- The exact parallelogram law and the value at zero imply the square law
for every natural multiple. -/
lemma quadratic_nsmul_of_parallelogram {G : Type*} [AddCommGroup G]
    (q : G → ℝ) (qzero : q 0 = 0)
    (qpar : ∀ P Q, q (P + Q) + q (P - Q) = 2 * q P + 2 * q Q) :
    ∀ (n : ℕ) (P : G), q (n • P) = (n : ℝ) ^ 2 * q P := by
  intro n
  induction n using Nat.twoStepInduction with
  | zero => intro P; simp [qzero]
  | one => intro P; simp
  | more n hn hn1 =>
      intro P
      have hp := qpar ((n + 1) • P) P
      have hsub : (n + 1) • P - P = n • P := by
        rw [add_nsmul, one_nsmul, add_sub_cancel_right]
      have hadd : (n + 1) • P + P = (n + 2) • P := by
        calc
          (n + 1) • P + P = (n • P + P) + P := by rw [add_nsmul, one_nsmul]
          _ = n • P + (2 • P) := by simp [two_nsmul, add_assoc]
          _ = (n + 2) • P := (add_nsmul P n 2).symm
      rw [hsub, hadd, hn P, hn1 P] at hp
      rw [show ((n + 2 : ℕ) : ℝ) = (n : ℝ) + 2 by norm_num]
      rw [show ((n + 1 : ℕ) : ℝ) = (n : ℝ) + 1 by norm_num] at hp
      ring_nf at hp ⊢
      linarith

/-- The same hypotheses make a quadratic function even. -/
lemma even_of_parallelogram {G : Type*} [AddCommGroup G]
    (q : G → ℝ) (qzero : q 0 = 0)
    (qpar : ∀ P Q, q (P + Q) + q (P - Q) = 2 * q P + 2 * q Q)
    (P : G) : q (-P) = q P := by
  have hp := qpar 0 P
  simp only [zero_add, zero_sub, qzero] at hp
  linarith

/-- The exact parallelogram law and `q 0 = 0` imply integer quadraticity. -/
lemma quadratic_zsmul_of_parallelogram {G : Type*} [AddCommGroup G]
    (q : G → ℝ) (qzero : q 0 = 0)
    (qpar : ∀ P Q, q (P + Q) + q (P - Q) = 2 * q P + 2 * q Q) :
    ∀ (m : ℤ) (P : G), q (m • P) = (m : ℝ) ^ 2 * q P := by
  intro m P
  cases m with
  | ofNat n =>
      simpa using quadratic_nsmul_of_parallelogram q qzero qpar n P
  | negSucc n =>
      rw [negSucc_zsmul, even_of_parallelogram q qzero qpar]
      rw [quadratic_nsmul_of_parallelogram q qzero qpar]
      push_cast
      ring

/-- `M0451-QUADRATIC`: the same two estimates yield all-integer
quadraticity of the constructed height. -/
theorem constructedCanonicalHeight_quadratic_of_bounds
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic]
    (Cdouble Cpar : ℝ)
    (hdouble : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ Cdouble)
    (hpar : ∀ P Q : E⟮K⟯,
      |naiveHeight (P + Q) + naiveHeight (P - Q) -
        2 * naiveHeight P - 2 * naiveHeight Q| ≤ Cpar) :
    ∀ (m : ℤ) (P : E⟮K⟯),
      constructedCanonicalHeight (m • P) =
        (m : ℝ) ^ 2 * constructedCanonicalHeight P := by
  have hparExact :=
    constructedCanonicalHeight_parallelogram_of_bounds Cdouble Cpar hdouble hpar
  have hzero : constructedCanonicalHeight (0 : E⟮K⟯) = 0 := by
    have hdoubleZero := constructedCanonicalHeight_double Cdouble hdouble (0 : E⟮K⟯)
    simp only [doublePoint, nsmul_zero] at hdoubleZero
    linarith
  exact quadratic_zsmul_of_parallelogram constructedCanonicalHeight hzero hparExact

/-- A finite dyadic orbit is bounded, so its normalized Tate limit vanishes. -/
theorem tateLimit_torsion_zero {G : Type*} [AddCommGroup G]
    (h : G → ℝ) (C : ℝ)
    (hbound : ∀ P, |h (doublePoint P) - 4 * h P| ≤ C)
    (P : G) (hP : IsOfFinAddOrder P) :
    tateLimit doublePoint h 4 P = 0 := by
  obtain ⟨k, hkPos, hk⟩ := hP.exists_nsmul_eq_zero
  let f : Fin k → G := fun i => (i : ℕ) • P
  have horbit : ∀ n : ℕ,
      ((2 : ℕ) ^ n) • P = f ⟨(2 ^ n) % k, Nat.mod_lt _ hkPos⟩ := by
    intro n
    simp only [f]
    exact nsmul_eq_mod_nsmul _ hk
  have hbounded : ∃ D : ℝ, ∀ n : ℕ, |h (((2 : ℕ) ^ n) • P)| ≤ D := by
    let D := ∑ i : Fin k, |h (f i)|
    refine ⟨D, fun n => ?_⟩
    rw [horbit n]
    exact Finset.single_le_sum (fun i _ => abs_nonneg (h (f i))) (Finset.mem_univ _)
  obtain ⟨D, hD⟩ := hbounded
  have hseqZero : Tendsto (tateSequence doublePoint h 4 P) atTop (nhds 0) := by
    have hnorm : ∀ n : ℕ,
        ‖tateSequence doublePoint h 4 P n‖ ≤ D / (4 : ℝ) ^ n := by
      intro n
      rw [tateSequence, doublePoint_iterate, Real.norm_eq_abs, abs_div,
        abs_of_pos (pow_pos (by norm_num : (0 : ℝ) < 4) n)]
      exact div_le_div_of_nonneg_right (hD n) (by positivity)
    have ht : Tendsto (fun n : ℕ => D / (4 : ℝ) ^ n) atTop (nhds 0) := by
      rw [show (fun n : ℕ => D / (4 : ℝ) ^ n) =
          fun n => D * ((4 : ℝ)⁻¹ ^ n) from by
        ext n
        rw [div_eq_mul_inv, inv_pow]]
      simpa using (tendsto_pow_atTop_nhds_zero_of_lt_one (r := (4 : ℝ)⁻¹)
        (by norm_num) (by norm_num)).const_mul D
    exact squeeze_zero_norm hnorm ht
  exact tendsto_nhds_unique
    (tateSequence_tendsto doublePoint h 4 (by norm_num) C hbound P) hseqZero

/-- `M0451-TORSION-ZERO`: the constructed height vanishes on torsion directly
from the doubling estimate, without assuming the full integer square law. -/
theorem constructedCanonicalHeight_torsion_zero
    {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic]
    (C : ℝ)
    (hbound : ∀ P : E⟮K⟯,
      |naiveHeight (doublePoint P) - 4 * naiveHeight P| ≤ C) :
    ∀ P : E⟮K⟯, IsOfFinAddOrder P → constructedCanonicalHeight P = 0 := by
  exact tateLimit_torsion_zero naiveHeight C hbound

/-- `M0451-TORSION-ZERO`: integer quadraticity forces every torsion point to
have height zero. -/
theorem torsion_to_zero_of_quadratic
    {G : Type*} [AddCommGroup G] (h : G → ℝ)
    (hquad : ∀ (m : ℤ) (P : G), h (m • P) = (m : ℝ) ^ 2 * h P) :
    ∀ P : G, IsOfFinAddOrder P → h P = 0 := by
  intro P hP
  obtain ⟨n, hn, hnP⟩ := hP.exists_nsmul_eq_zero
  have hzero : h 0 = 0 := by
    simpa using hquad 0 P
  have hscale := hquad (n : ℤ) P
  rw [natCast_zsmul, hnP, hzero] at hscale
  have hnreal : (n : ℝ) ≠ 0 := by exact_mod_cast hn.ne'
  exact (mul_eq_zero.mp hscale.symm).resolve_left (pow_ne_zero 2 hnreal)

#print axioms tateSequence_tendsto
#print axioms tateLimit_sub_le
#print axioms tateLimit_map
#print axioms limit_formula_of_doubling_bound
#print axioms bounded_difference_of_doubling_bound
#print axioms constructedCanonicalHeight_double
#print axioms constructedCanonicalHeight_nonnegative
#print axioms constructedCanonicalHeight_parallelogram_of_bounds
#print axioms constructedCanonicalHeight_quadratic_of_bounds
#print axioms constructedCanonicalHeight_torsion_zero
#print axioms torsion_to_zero_of_quadratic

end Proof

end Stage1Instances.THM_M_0451
