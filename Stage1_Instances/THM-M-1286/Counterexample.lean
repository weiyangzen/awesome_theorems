import Mathlib.Analysis.Analytic.Uniqueness
import Mathlib.Analysis.SpecialFunctions.Integrability.Basic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Function.L1Space.Integrable
import Mathlib.MeasureTheory.Function.LpSeminorm.Indicator
import «Stage1_Instances».«THM-M-1286».Statement

/-!
# THM-M-1286: refutation of the frozen target

The frozen target is false for two independent encoding reasons. First,
`ContDiff Real top` means analytic rather than smooth, so every compactly
supported test function is zero and `HasWeakGradient` is vacuous. Second, the
target requires a pointwise real-valued radial-decreasing representative. Such
a representative is bounded above by its value at zero, but finite-`p` inputs
can be essentially unbounded.

The function `-log x` on `(0, 1)`, transported to `Fin 1 -> Real`, supplies an
exact counterexample at `n = p = 1`: it is nonnegative and integrable, and
every positive superlevel has positive finite measure.
-/

open scoped ENNReal MeasureTheory

namespace Stage1Instances.THM_M_1286.Counterexample

open MeasureTheory Set Filter

abbrev Line := Euclidean 1

def lineEquiv : Line ≃ᵐ Real := MeasurableEquiv.piUnique (fun _ : Fin 1 => Real)

noncomputable def logSpike (y : Real) : Real :=
  Ioo (0 : Real) 1 |>.indicator (fun y => -Real.log y) y

noncomputable def counterexample (x : Line) : Real := logSpike (lineEquiv x)

/-- A frozen analytic compactly supported test function is identically zero. -/
theorem analytic_compactSupport_eq_zero
    (phi : Line -> Real) (smooth : ContDiff Real ⊤ phi)
    (compact : HasCompactSupport phi) : phi = 0 := by
  have support_ne_univ : tsupport phi ≠ (univ : Set Line) := compact.ne_univ
  obtain ⟨z, hz⟩ := (ne_univ_iff_exists_notMem (tsupport phi)).mp support_ne_univ
  exact smooth.analyticOnNhd.eq_of_eventuallyEq
    analyticOnNhd_const
    (notMem_tsupport_iff_eventuallyEq.mp hz)

/-- The frozen weak-gradient predicate imposes no constraint in dimension one. -/
theorem hasWeakGradient_vacuous (f : Line -> Real) (g : Line -> Line) :
    HasWeakGradient f g := by
  intro i phi hsmooth hcompact
  rw [analytic_compactSupport_eq_zero phi hsmooth hcompact]
  simp

theorem logSpike_measurable : Measurable logSpike := by
  exact (Real.measurable_log.neg).indicator measurableSet_Ioo

theorem logSpike_integrable : Integrable logSpike volume := by
  apply IntegrableOn.integrable_indicator _ measurableSet_Ioo
  rw [← intervalIntegrable_iff_integrableOn_Ioo_of_le (by norm_num : (0 : Real) ≤ 1)]
  exact intervalIntegral.intervalIntegrable_log'.neg

theorem counterexample_integrable : Integrable counterexample volume := by
  exact (volume_preserving_piUnique (fun _ : Fin 1 => Real)).integrable_comp_of_integrable
    logSpike_integrable

theorem logSpike_nonneg (y : Real) : 0 ≤ logSpike y := by
  by_cases hy : y ∈ Ioo (0 : Real) 1
  · rw [logSpike, indicator_of_mem hy]
    exact neg_nonneg.mpr (Real.log_nonpos hy.1.le hy.2.le)
  · simp [logSpike, hy]

theorem counterexample_nonneg (x : Line) : 0 ≤ counterexample x :=
  logSpike_nonneg _

theorem counterexample_aestronglyMeasurable :
    AEStronglyMeasurable counterexample volume :=
  counterexample_integrable.aestronglyMeasurable

theorem counterexample_memLp : MemLp counterexample 1 volume :=
  memLp_one_iff_integrable.mpr counterexample_integrable

theorem counterexample_vanishesAtInfinity : VanishesAtInfinity counterexample := by
  intro t ht
  have hsubset : {x : Line | t < counterexample x} ⊆ lineEquiv ⁻¹' Ioo (0 : Real) 1 := by
    intro x hx
    by_contra hnot
    change lineEquiv x ∉ Ioo (0 : Real) 1 at hnot
    have : counterexample x = 0 := by
      rw [counterexample, logSpike, indicator_of_notMem hnot]
    exact (by simpa [this] using lt_trans ht hx)
  have hmeasure : volume (lineEquiv ⁻¹' Ioo (0 : Real) 1) = 1 := by
    change volume ((MeasurableEquiv.piUnique (fun _ : Fin 1 => Real)) ⁻¹'
      Ioo (0 : Real) 1) = 1
    rw [(volume_preserving_piUnique (fun _ : Fin 1 => Real)).measure_preimage
      measurableSet_Ioo.nullMeasurableSet, Real.volume_Ioo]
    norm_num
  have hle : volume {x : Line | t < counterexample x} ≤
      volume (lineEquiv ⁻¹' Ioo (0 : Real) 1) := measure_mono hsubset
  rw [hmeasure] at hle
  exact ne_top_of_le_ne_top ENNReal.one_ne_top hle

theorem zero_memLp : MemLp (fun _ : Line => (0 : Line)) 1 volume := MemLp.zero'

/-- Every positive strict superlevel of the counterexample has positive measure. -/
theorem counterexample_superlevel_pos (t : Real) (ht : 0 < t) :
    0 < volume {x : Line | t < counterexample x} := by
  let a := Real.exp (-t)
  have ha0 : 0 < a := Real.exp_pos _
  have ha1 : a < 1 := Real.exp_lt_one_iff.mpr (neg_lt_zero.mpr ht)
  have hsubset : lineEquiv ⁻¹' Ioo (0 : Real) a ⊆
      {x : Line | t < counterexample x} := by
    intro x hx
    change lineEquiv x ∈ Ioo (0 : Real) a at hx
    change t < logSpike (lineEquiv x)
    have hx01 : lineEquiv x ∈ Ioo (0 : Real) 1 := ⟨hx.1, hx.2.trans ha1⟩
    rw [logSpike, indicator_of_mem hx01]
    have hlog : Real.log (lineEquiv x) < Real.log a :=
      Real.strictMonoOn_log hx.1 ha0 hx.2
    have hlog' : Real.log (lineEquiv x) < -t := by
      simpa [a] using hlog
    linarith
  have hmeasure : volume (lineEquiv ⁻¹' Ioo (0 : Real) a) = ENNReal.ofReal a := by
    change volume ((MeasurableEquiv.piUnique (fun _ : Fin 1 => Real)) ⁻¹'
      Ioo (0 : Real) a) = ENNReal.ofReal a
    rw [(volume_preserving_piUnique (fun _ : Fin 1 => Real)).measure_preimage
      measurableSet_Ioo.nullMeasurableSet, Real.volume_Ioo]
    simp
  have hpreimage_pos : 0 < volume (lineEquiv ⁻¹' Ioo (0 : Real) a) := by
    rw [hmeasure, ENNReal.ofReal_pos]
    exact ha0
  exact lt_of_lt_of_le hpreimage_pos (measure_mono hsubset)

/-- Kernel-checked refutation of the exact frozen positive target. -/
theorem not_polyaSzegoTarget : Not PolyaSzegoTarget := by
  intro target
  obtain ⟨uStar, gStar, huStar_meas, huStar_memLp, huStar_symm, huStar_equi,
      huStar_grad, hgStar_memLp, henergy⟩ :=
    target 1 1 (by norm_num) (by norm_num) (by norm_num) counterexample
      (fun _ : Line => (0 : Line)) counterexample_nonneg
      counterexample_aestronglyMeasurable counterexample_memLp
      counterexample_vanishesAtInfinity
      (hasWeakGradient_vacuous counterexample (fun _ => 0)) zero_memLp
  let t := uStar 0 + 1
  have ht : 0 < t := by
    have hzero := huStar_symm.1 (0 : Line)
    dsimp [t]
    linarith
  have hstar_empty : {x : Line | t < uStar x} = ∅ := by
    ext x
    constructor
    · intro hx
      have hle := huStar_symm.2 (0 : Line) x (by simp)
      dsimp [t] at hx
      exfalso
      linarith
    · simp
  have heq := huStar_equi t ht
  have hinput_zero : volume {x : Line | t < counterexample x} = 0 := by
    simpa [hstar_empty] using heq
  exact (ne_of_gt (counterexample_superlevel_pos t ht)) hinput_zero

#check not_polyaSzegoTarget
#print axioms not_polyaSzegoTarget

end Stage1Instances.THM_M_1286.Counterexample
