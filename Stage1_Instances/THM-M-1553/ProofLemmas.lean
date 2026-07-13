import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import «Statement»

noncomputable section

namespace Stage1Instances.THM_M_1553.ProofLemmas

open Stage1Instances.THM_M_1553

theorem sliceX_contDiff {n : WithTop ℕ∞} (tau : Field)
    (h : ContDiff ℝ n tau) (t : ℝ) :
    ContDiff ℝ n (fun x : ℝ => tau (x, t)) := by
  exact h.comp (contDiff_prodMk_left t)

theorem sliceT_contDiff {n : WithTop ℕ∞} (tau : Field)
    (h : ContDiff ℝ n tau) (x : ℝ) :
    ContDiff ℝ n (fun t : ℝ => tau (x, t)) := by
  exact h.comp (contDiff_prodMk_right x)

theorem partialX_differentiable (tau : Field) (h : ContDiff ℝ 2 tau) :
    Differentiable ℝ (partialX tau) := by
  change Differentiable ℝ (fun w : ℝ × ℝ =>
    deriv (fun x : ℝ => tau (x, w.2)) w.1)
  rw [show (fun w : ℝ × ℝ => deriv (fun x : ℝ => tau (x, w.2)) w.1) =
      fun w => fderiv ℝ tau w (1, 0) by
    funext w
    have ht := HasFDerivAt.comp w.1
      (g := tau) (f := fun x : ℝ => (x, w.2))
      (h.differentiable two_ne_zero w).hasFDerivAt
      (hasFDerivAt_prodMk_left w.1 w.2)
    have hd := ht.hasDerivAt
    change deriv (tau ∘ fun x : ℝ => (x, w.2)) w.1 = _
    rw [hd.deriv]
    simp]
  exact (h.fderiv_right (m := 1) (by norm_num) |>.clm_apply
    (contDiff_const : ContDiff ℝ 1 (fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ))))).differentiable one_ne_zero

theorem partialT_differentiable (tau : Field) (h : ContDiff ℝ 2 tau) :
    Differentiable ℝ (partialT tau) := by
  change Differentiable ℝ (fun w : ℝ × ℝ =>
    deriv (fun t : ℝ => tau (w.1, t)) w.2)
  rw [show (fun w : ℝ × ℝ => deriv (fun t : ℝ => tau (w.1, t)) w.2) =
      fun w => fderiv ℝ tau w (0, 1) by
    funext w
    have ht := HasFDerivAt.comp w.2
      (g := tau) (f := fun t : ℝ => (w.1, t))
      (h.differentiable two_ne_zero w).hasFDerivAt
      (hasFDerivAt_prodMk_right w.1 w.2)
    have hd := ht.hasDerivAt
    change deriv (tau ∘ fun t : ℝ => (w.1, t)) w.2 = _
    rw [hd.deriv]
    simp]
  exact (h.fderiv_right (m := 1) (by norm_num) |>.clm_apply
    (contDiff_const : ContDiff ℝ 1 (fun _ : ℝ × ℝ => ((0 : ℝ), (1 : ℝ))))).differentiable one_ne_zero

theorem log_contDiff (tau : Field) (h : ContDiff ℝ 5 tau)
    (positive : ∀ z, 0 < tau z) :
    ContDiff ℝ 5 (fun z => Real.log (tau z)) := by
  exact h.log (fun z => ne_of_gt (positive z))

theorem partialX_contDiff (n : ℕ) (tau : Field)
    (h : ContDiff ℝ (n + 1) tau) :
    ContDiff ℝ n (partialX tau) := by
  change ContDiff ℝ n (fun w : ℝ × ℝ =>
    deriv (fun x : ℝ => tau (x, w.2)) w.1)
  rw [show (fun w : ℝ × ℝ => deriv (fun x : ℝ => tau (x, w.2)) w.1) =
      fun w => fderiv ℝ tau w (1, 0) by
    funext w
    have ht := HasFDerivAt.comp w.1
      (g := tau) (f := fun x : ℝ => (x, w.2))
      (h.differentiable (by simp) w).hasFDerivAt
      (hasFDerivAt_prodMk_left w.1 w.2)
    have hd := ht.hasDerivAt
    change deriv (tau ∘ fun x : ℝ => (x, w.2)) w.1 = _
    rw [hd.deriv]
    simp]
  exact h.fderiv_right (m := n) (by simp) |>.clm_apply
    (contDiff_const : ContDiff ℝ n (fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ))))

theorem partialT_contDiff (n : ℕ) (tau : Field)
    (h : ContDiff ℝ (n + 1) tau) :
    ContDiff ℝ n (partialT tau) := by
  change ContDiff ℝ n (fun w : ℝ × ℝ =>
    deriv (fun t : ℝ => tau (w.1, t)) w.2)
  rw [show (fun w : ℝ × ℝ => deriv (fun t : ℝ => tau (w.1, t)) w.2) =
      fun w => fderiv ℝ tau w (0, 1) by
    funext w
    have ht := HasFDerivAt.comp w.2
      (g := tau) (f := fun t : ℝ => (w.1, t))
      (h.differentiable (by simp) w).hasFDerivAt
      (hasFDerivAt_prodMk_right w.1 w.2)
    have hd := ht.hasDerivAt
    change deriv (tau ∘ fun t : ℝ => (w.1, t)) w.2 = _
    rw [hd.deriv]
    simp]
  exact h.fderiv_right (m := n) (by simp) |>.clm_apply
    (contDiff_const : ContDiff ℝ n (fun _ : ℝ × ℝ => ((0 : ℝ), (1 : ℝ))))

theorem iterate_partialX_contDiff (k n : ℕ) (tau : Field)
    (h : ContDiff ℝ (n + k) tau) :
    ContDiff ℝ n (iterate partialX k tau) := by
  induction k generalizing n tau with
  | zero => simpa [iterate] using h
  | succ k ih =>
      have h' : ContDiff ℝ ((n + 1 : ℕ) + k) tau := by
        convert h using 1
        push_cast
        ring
      simpa [iterate, Function.comp_def] using
        partialX_contDiff n _ (ih (tau := tau) (n := n + 1) h')

theorem iterate_partialT_contDiff (k n : ℕ) (tau : Field)
    (h : ContDiff ℝ (n + k) tau) :
    ContDiff ℝ n (iterate partialT k tau) := by
  induction k generalizing n tau with
  | zero => simpa [iterate] using h
  | succ k ih =>
      have h' : ContDiff ℝ ((n + 1 : ℕ) + k) tau := by
        convert h using 1
        push_cast
        ring
      simpa [iterate, Function.comp_def] using
        partialT_contDiff n _ (ih (tau := tau) (n := n + 1) h')

theorem mixedDerivative_contDiff (xOrder tOrder n : ℕ) (tau : Field)
    (h : ContDiff ℝ (n + (xOrder + tOrder)) tau) :
    ContDiff ℝ n (mixedDerivative xOrder tOrder tau) := by
  unfold mixedDerivative
  have ht : ContDiff ℝ (n + xOrder) (iterate partialT tOrder tau) := by
    apply iterate_partialT_contDiff tOrder (n + xOrder) tau
    convert h using 1
    push_cast
    ring
  exact iterate_partialX_contDiff xOrder n _ ht

theorem partialX_mixedDerivative (xOrder tOrder : ℕ) (tau : Field) :
    partialX (mixedDerivative xOrder tOrder tau) =
      mixedDerivative (xOrder + 1) tOrder tau := by
  simp [mixedDerivative, iterate, Function.comp_def]

theorem partial_commute (f : Field) (h : ContDiff ℝ 2 f) :
    partialT (partialX f) = partialX (partialT f) := by
  funext z
  have hx : partialX f = fun w => fderiv ℝ f w (1, 0) := by
    funext w
    change deriv (fun x : ℝ => f (x, w.2)) w.1 = _
    have ht := HasFDerivAt.comp w.1
      (g := f) (f := fun x : ℝ => (x, w.2))
      (h.differentiable two_ne_zero w).hasFDerivAt
      (hasFDerivAt_prodMk_left w.1 w.2)
    exact ht.hasDerivAt.deriv.trans (by simp)
  have ht : partialT f = fun w => fderiv ℝ f w (0, 1) := by
    funext w
    change deriv (fun t : ℝ => f (w.1, t)) w.2 = _
    have ht := HasFDerivAt.comp w.2
      (g := f) (f := fun t : ℝ => (w.1, t))
      (h.differentiable two_ne_zero w).hasFDerivAt
      (hasFDerivAt_prodMk_right w.1 w.2)
    exact ht.hasDerivAt.deriv.trans (by simp)
  rw [hx, ht]
  change deriv (fun t : ℝ => fderiv ℝ f (z.1, t) (1, 0)) z.2 =
    deriv (fun x : ℝ => fderiv ℝ f (x, z.2) (0, 1)) z.1
  have hfd : Differentiable ℝ (fderiv ℝ f) :=
    (h.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero
  have hxt := HasFDerivAt.comp z.2
    (g := fun w => fderiv ℝ f w (1, 0))
    (f := fun t : ℝ => (z.1, t))
    (hfd.clm_apply (differentiable_const ((1 : ℝ), (0 : ℝ))) z).hasFDerivAt
    (hasFDerivAt_prodMk_right z.1 z.2)
  have htx := HasFDerivAt.comp z.1
    (g := fun w => fderiv ℝ f w (0, 1))
    (f := fun x : ℝ => (x, z.2))
    (hfd.clm_apply (differentiable_const ((0 : ℝ), (1 : ℝ))) z).hasFDerivAt
    (hasFDerivAt_prodMk_left z.1 z.2)
  change deriv ((fun w => fderiv ℝ f w (1, 0)) ∘
      fun t : ℝ => (z.1, t)) z.2 =
    deriv ((fun w => fderiv ℝ f w (0, 1)) ∘
      fun x : ℝ => (x, z.2)) z.1
  rw [hxt.hasDerivAt.deriv, htx.hasDerivAt.deriv]
  simp
  rw [fderiv_clm_apply hfd.differentiableAt
      (differentiableAt_const ((1 : ℝ), (0 : ℝ))),
    fderiv_clm_apply hfd.differentiableAt
      (differentiableAt_const ((0 : ℝ), (1 : ℝ)))]
  simp
  exact (h.contDiffAt.isSymmSndFDerivAt (by norm_num)).eq (0, 1) (1, 0)

theorem partialT_mixedDerivative (xOrder tOrder : ℕ) (tau : Field)
    (h : ContDiff ℝ (xOrder + tOrder + 2) tau) :
    partialT (mixedDerivative xOrder tOrder tau) =
      mixedDerivative xOrder (tOrder + 1) tau := by
  induction xOrder generalizing tOrder tau with
  | zero => simp [mixedDerivative, iterate]
  | succ xOrder ih =>
      have hprev : ContDiff ℝ (xOrder + tOrder + 2) tau := by
        apply h.of_le
        gcongr
        push_cast
        norm_num
      have hfield : ContDiff ℝ 2 (mixedDerivative xOrder tOrder tau) := by
        apply mixedDerivative_contDiff xOrder tOrder 2 tau
        convert hprev using 1
        push_cast
        ring
      have hcomm : partialT (partialX (mixedDerivative xOrder tOrder tau)) =
          partialX (partialT (mixedDerivative xOrder tOrder tau)) :=
        partial_commute _ hfield
      rw [show mixedDerivative (xOrder + 1) tOrder tau =
          partialX (mixedDerivative xOrder tOrder tau) by
        ext z
        simp [mixedDerivative, iterate, Function.comp_def]]
      rw [hcomm, ih (tOrder := tOrder) (tau := tau) hprev]
      ext z
      simp [mixedDerivative, iterate, Function.comp_def]

theorem hirotaD_four_zero (tau : Field) (z : ℝ × ℝ) :
    hirotaD 4 0 tau tau z =
      2 * (tau z * mixedDerivative 4 0 tau z -
        4 * mixedDerivative 1 0 tau z * mixedDerivative 3 0 tau z +
        3 * (mixedDerivative 2 0 tau z) ^ 2) := by
  simp [hirotaD]
  norm_num [Finset.sum_range_succ, mixedDerivative, iterate, Nat.choose]
  ring

theorem hirotaD_one_one (tau : Field) (z : ℝ × ℝ) :
    hirotaD 1 1 tau tau z =
      2 * (tau z * mixedDerivative 1 1 tau z -
        mixedDerivative 1 0 tau z * mixedDerivative 0 1 tau z) := by
  simp [hirotaD]
  norm_num [Finset.sum_range_succ, mixedDerivative, iterate]
  ring

theorem partialX_mul (f g : Field) (hf : ContDiff ℝ 1 f)
    (hg : ContDiff ℝ 1 g) :
    partialX (fun z => f z * g z) =
      fun z => partialX f z * g z + f z * partialX g z := by
  funext z
  unfold partialX
  rw [deriv_fun_mul]
  · exact (hf.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1
  · exact (hg.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1

theorem partialT_mul (f g : Field) (hf : ContDiff ℝ 1 f)
    (hg : ContDiff ℝ 1 g) :
    partialT (fun z => f z * g z) =
      fun z => partialT f z * g z + f z * partialT g z := by
  funext z
  unfold partialT
  rw [deriv_fun_mul]
  · exact (hf.comp (contDiff_prodMk_right z.1)).differentiable one_ne_zero z.2
  · exact (hg.comp (contDiff_prodMk_right z.1)).differentiable one_ne_zero z.2

theorem partialX_const_mul (c : ℝ) (f : Field) :
    partialX (fun z => c * f z) = fun z => c * partialX f z := by
  funext z
  unfold partialX
  rw [deriv_const_mul_field]

theorem partialT_const_mul (c : ℝ) (f : Field) :
    partialT (fun z => c * f z) = fun z => c * partialT f z := by
  funext z
  unfold partialT
  rw [deriv_const_mul_field]

theorem iterate_partialX_const_mul (k : ℕ) (c : ℝ) (f : Field) :
    iterate partialX k (fun z => c * f z) =
      fun z => c * iterate partialX k f z := by
  induction k with
  | zero => simp [iterate]
  | succ k ih =>
      simp only [iterate, Function.comp_apply]
      rw [ih, partialX_const_mul]

theorem partialX_log (tau : Field) (h : ContDiff ℝ 1 tau)
    (positive : ∀ z, 0 < tau z) :
    partialX (fun z => Real.log (tau z)) =
      fun z => partialX tau z / tau z := by
  funext z
  unfold partialX
  rw [deriv.log]
  · exact (h.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1
  · exact ne_of_gt (positive z)

theorem partialT_log (tau : Field) (h : ContDiff ℝ 1 tau)
    (positive : ∀ z, 0 < tau z) :
    partialT (fun z => Real.log (tau z)) =
      fun z => partialT tau z / tau z := by
  funext z
  unfold partialT
  rw [deriv.log]
  · exact (h.comp (contDiff_prodMk_right z.1)).differentiable one_ne_zero z.2
  · exact ne_of_gt (positive z)

theorem tau_mixedDerivative_of_log (tau : Field)
    (positive : ∀ z, 0 < tau z) (xOrder tOrder : ℕ) :
    mixedDerivative xOrder tOrder tau =
      mixedDerivative xOrder tOrder (fun z => Real.exp (Real.log (tau z))) := by
  congr 1
  funext z
  exact (Real.exp_log (positive z)).symm

theorem partialX_exp (f : Field) (h : ContDiff ℝ 1 f) :
    partialX (fun z => Real.exp (f z)) =
      fun z => Real.exp (f z) * partialX f z := by
  funext z
  unfold partialX
  rw [deriv_exp]
  exact (h.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1

theorem partialT_exp (f : Field) (h : ContDiff ℝ 1 f) :
    partialT (fun z => Real.exp (f z)) =
      fun z => Real.exp (f z) * partialT f z := by
  funext z
  unfold partialT
  rw [deriv_exp]
  exact (h.comp (contDiff_prodMk_right z.1)).differentiable one_ne_zero z.2

theorem exp_mixed_zero_zero (f : Field) :
    mixedDerivative 0 0 (fun z => Real.exp (f z)) =
      fun z => Real.exp (f z) := by
  rfl

theorem exp_mixed_one_zero (f : Field) (h : ContDiff ℝ 1 f) :
    mixedDerivative 1 0 (fun z => Real.exp (f z)) =
      fun z => Real.exp (f z) * mixedDerivative 1 0 f z := by
  simpa [mixedDerivative, iterate, Function.comp_def] using partialX_exp f h

theorem exp_mixed_zero_one (f : Field) (h : ContDiff ℝ 1 f) :
    mixedDerivative 0 1 (fun z => Real.exp (f z)) =
      fun z => Real.exp (f z) * mixedDerivative 0 1 f z := by
  simpa [mixedDerivative, iterate, Function.comp_def] using partialT_exp f h

theorem exp_mixed_two_zero (f : Field) (h : ContDiff ℝ 2 f) :
    mixedDerivative 2 0 (fun z => Real.exp (f z)) = fun z =>
      Real.exp (f z) * (mixedDerivative 2 0 f z + (mixedDerivative 1 0 f z) ^ 2) := by
  rw [show mixedDerivative 2 0 (fun z => Real.exp (f z)) =
      partialX (fun z => Real.exp (f z) * partialX f z) by
    simp [mixedDerivative, iterate, Function.comp_def, partialX_exp f (h.of_le (by norm_num))]]
  rw [partialX_mul]
  · rw [partialX_exp f (h.of_le (by norm_num))]
    ext z
    simp [mixedDerivative, iterate, Function.comp_def]
    ring
  · exact h.exp.of_le (by norm_num)
  · exact partialX_contDiff 1 f h

theorem exp_mixed_three_zero (f : Field) (h : ContDiff ℝ 3 f) :
    mixedDerivative 3 0 (fun z => Real.exp (f z)) = fun z =>
      Real.exp (f z) * (mixedDerivative 3 0 f z +
        3 * mixedDerivative 1 0 f z * mixedDerivative 2 0 f z +
        (mixedDerivative 1 0 f z) ^ 3) := by
  have hf1 : ContDiff ℝ 1 (mixedDerivative 1 0 f) :=
    mixedDerivative_contDiff 1 0 1 f (h.of_le (by norm_num))
  have hf2 : ContDiff ℝ 1 (mixedDerivative 2 0 f) :=
    mixedDerivative_contDiff 2 0 1 f (h.of_le (by norm_num))
  calc
    mixedDerivative 3 0 (fun z => Real.exp (f z)) =
        partialX (mixedDerivative 2 0 (fun z => Real.exp (f z))) := by
      symm
      exact partialX_mixedDerivative 2 0 _
    _ = partialX (fun z => Real.exp (f z) *
          (mixedDerivative 2 0 f z + (mixedDerivative 1 0 f z) ^ 2)) := by
      rw [exp_mixed_two_zero f (h.of_le (by norm_num))]
    _ = fun z => Real.exp (f z) * (mixedDerivative 3 0 f z +
          3 * mixedDerivative 1 0 f z * mixedDerivative 2 0 f z +
          (mixedDerivative 1 0 f z) ^ 3) := by
      rw [partialX_mul]
      · rw [partialX_exp f (h.of_le (by norm_num))]
        ext z
        unfold partialX
        rw [deriv_fun_add]
        · rw [deriv_fun_pow]
          · have h12 := congrFun (partialX_mixedDerivative 1 0 f) z
            have h23 := congrFun (partialX_mixedDerivative 2 0 f) z
            change partialX (mixedDerivative 1 0 f) z =
              mixedDerivative 2 0 f z at h12
            change partialX (mixedDerivative 2 0 f) z =
              mixedDerivative 3 0 f z at h23
            have h01 := congrFun (partialX_mixedDerivative 0 0 f) z
            change partialX f z = mixedDerivative 1 0 f z at h01
            norm_num
            change (Real.exp (f z) * partialX f z) *
                (mixedDerivative 2 0 f z + mixedDerivative 1 0 f z ^ 2) +
              Real.exp (f z) *
                (partialX (mixedDerivative 2 0 f) z +
                  2 * mixedDerivative 1 0 f z *
                    partialX (mixedDerivative 1 0 f) z) = _
            rw [h01, h12, h23]
            ring
          · exact (hf1.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1
        · exact (hf2.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1
        · exact ((hf1.pow 2).comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1
      · exact h.exp.of_le (by norm_num)
      · exact hf2.add (hf1.pow 2)

theorem partialX_add (f g : Field) (hf : ContDiff ℝ 1 f)
    (hg : ContDiff ℝ 1 g) :
    partialX (fun z => f z + g z) = fun z => partialX f z + partialX g z := by
  funext z
  unfold partialX
  rw [deriv_fun_add]
  · exact (hf.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1
  · exact (hg.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1

theorem partialX_pow_two (f : Field) (h : ContDiff ℝ 1 f) :
    partialX (fun z => f z ^ 2) = fun z => 2 * f z * partialX f z := by
  funext z
  unfold partialX
  rw [deriv_fun_pow]
  ring
  exact (h.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1

theorem partialX_pow_three (f : Field) (h : ContDiff ℝ 1 f) :
    partialX (fun z => f z ^ 3) = fun z => 3 * f z ^ 2 * partialX f z := by
  funext z
  unfold partialX
  rw [deriv_fun_pow]
  norm_num
  exact (h.comp (contDiff_prodMk_left z.2)).differentiable one_ne_zero z.1

theorem exp_mixed_four_zero (f : Field) (h : ContDiff ℝ 4 f) :
    mixedDerivative 4 0 (fun z => Real.exp (f z)) = fun z =>
      Real.exp (f z) * (mixedDerivative 4 0 f z +
        4 * mixedDerivative 1 0 f z * mixedDerivative 3 0 f z +
        3 * (mixedDerivative 2 0 f z) ^ 2 +
        6 * (mixedDerivative 1 0 f z) ^ 2 * mixedDerivative 2 0 f z +
        (mixedDerivative 1 0 f z) ^ 4) := by
  have hf1 : ContDiff ℝ 1 (mixedDerivative 1 0 f) :=
    mixedDerivative_contDiff 1 0 1 f (h.of_le (by norm_num))
  have hf2 : ContDiff ℝ 1 (mixedDerivative 2 0 f) :=
    mixedDerivative_contDiff 2 0 1 f (h.of_le (by norm_num))
  have hf3 : ContDiff ℝ 1 (mixedDerivative 3 0 f) :=
    mixedDerivative_contDiff 3 0 1 f (h.of_le (by norm_num))
  have hpoly :
      partialX (fun z => mixedDerivative 3 0 f z +
        3 * mixedDerivative 1 0 f z * mixedDerivative 2 0 f z +
        (mixedDerivative 1 0 f z) ^ 3) = fun z =>
          mixedDerivative 4 0 f z +
          3 * (mixedDerivative 2 0 f z * mixedDerivative 2 0 f z +
            mixedDerivative 1 0 f z * mixedDerivative 3 0 f z) +
          3 * (mixedDerivative 1 0 f z) ^ 2 * mixedDerivative 2 0 f z := by
    rw [partialX_add]
    · rw [partialX_add]
      · rw [partialX_mul]
        · rw [partialX_const_mul,
              partialX_pow_three (mixedDerivative 1 0 f) hf1]
          funext z
          have h12 := congrFun (partialX_mixedDerivative 1 0 f) z
          have h23 := congrFun (partialX_mixedDerivative 2 0 f) z
          have h34 := congrFun (partialX_mixedDerivative 3 0 f) z
          change partialX (mixedDerivative 1 0 f) z =
            mixedDerivative 2 0 f z at h12
          change partialX (mixedDerivative 2 0 f) z =
            mixedDerivative 3 0 f z at h23
          change partialX (mixedDerivative 3 0 f) z =
            mixedDerivative 4 0 f z at h34
          simp only [Function.comp_apply]
          rw [h12, h23, h34]
          ring
        · exact contDiff_const.mul hf1
        · exact hf2
      · exact hf3
      · exact (contDiff_const.mul hf1).mul hf2
    · exact hf3.add ((contDiff_const.mul hf1).mul hf2)
    · exact hf1.pow 3
  calc
    mixedDerivative 4 0 (fun z => Real.exp (f z)) =
        partialX (mixedDerivative 3 0 (fun z => Real.exp (f z))) := by
      symm
      exact partialX_mixedDerivative 3 0 _
    _ = partialX (fun z => Real.exp (f z) *
          (mixedDerivative 3 0 f z +
            3 * mixedDerivative 1 0 f z * mixedDerivative 2 0 f z +
            (mixedDerivative 1 0 f z) ^ 3)) := by
      rw [exp_mixed_three_zero f (h.of_le (by norm_num))]
    _ = fun z => Real.exp (f z) * (mixedDerivative 4 0 f z +
          4 * mixedDerivative 1 0 f z * mixedDerivative 3 0 f z +
          3 * (mixedDerivative 2 0 f z) ^ 2 +
          6 * (mixedDerivative 1 0 f z) ^ 2 * mixedDerivative 2 0 f z +
          (mixedDerivative 1 0 f z) ^ 4) := by
      rw [partialX_mul]
      · rw [partialX_exp f (h.of_le (by norm_num))]
        rw [hpoly]
        funext z
        have h01 := congrFun (partialX_mixedDerivative 0 0 f) z
        change partialX f z = mixedDerivative 1 0 f z at h01
        change (Real.exp (f z) * partialX f z) * _ + Real.exp (f z) * _ = _
        rw [h01]
        ring
      · exact h.exp.of_le (by norm_num)
      · exact hf3.add ((contDiff_const.mul hf1).mul hf2) |>.add (hf1.pow 3)

theorem exp_mixed_one_one (f : Field) (h : ContDiff ℝ 2 f) :
    mixedDerivative 1 1 (fun z => Real.exp (f z)) = fun z =>
      Real.exp (f z) * (mixedDerivative 1 1 f z +
        mixedDerivative 1 0 f z * mixedDerivative 0 1 f z) := by
  calc
    mixedDerivative 1 1 (fun z => Real.exp (f z)) =
        partialX (mixedDerivative 0 1 (fun z => Real.exp (f z))) := by
      symm
      exact partialX_mixedDerivative 0 1 _
    _ = partialX (fun z => Real.exp (f z) * mixedDerivative 0 1 f z) := by
      rw [exp_mixed_zero_one f (h.of_le (by norm_num))]
    _ = fun z => Real.exp (f z) * (mixedDerivative 1 1 f z +
          mixedDerivative 1 0 f z * mixedDerivative 0 1 f z) := by
      rw [partialX_mul]
      · rw [partialX_exp f (h.of_le (by norm_num))]
        funext z
        have hx := congrFun (partialX_mixedDerivative 0 0 f) z
        have hxt := congrFun (partialX_mixedDerivative 0 1 f) z
        change partialX f z = mixedDerivative 1 0 f z at hx
        change partialX (mixedDerivative 0 1 f) z =
          mixedDerivative 1 1 f z at hxt
        change Real.exp (f z) * partialX f z * mixedDerivative 0 1 f z +
          Real.exp (f z) * partialX (mixedDerivative 0 1 f) z = _
        rw [hx, hxt]
        ring
      · exact h.exp.of_le (by norm_num)
      · exact mixedDerivative_contDiff 0 1 1 f (by simpa using h)

#print axioms sliceX_contDiff
#print axioms sliceT_contDiff
#print axioms partialX_differentiable
#print axioms partialT_differentiable
#print axioms log_contDiff
#print axioms partialX_contDiff
#print axioms partialT_contDiff
#print axioms iterate_partialX_contDiff
#print axioms iterate_partialT_contDiff
#print axioms mixedDerivative_contDiff
#print axioms partialX_mixedDerivative
#print axioms partial_commute
#print axioms partialT_mixedDerivative
#print axioms hirotaD_four_zero
#print axioms hirotaD_one_one
#print axioms partialX_mul
#print axioms partialT_mul
#print axioms partialX_const_mul
#print axioms partialT_const_mul
#print axioms iterate_partialX_const_mul
#print axioms partialX_log
#print axioms partialT_log

end Stage1Instances.THM_M_1553.ProofLemmas
