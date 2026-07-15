import «Stage1_Instances».«THM-M-0996».ObligationTree
import Mathlib.Probability.CDF

/-!
# THM-M-0996 proof phase

This module proves the exact mass-indexed enlargement formula for every
unit-normal affine half-space, together with the elementary dimension split.
The arbitrary-set Gaussian isoperimetric bound remains open.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0996

universe u

/-! The frozen orthonormal-coordinate transport. -/

abbrev CoordE (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] :=
  EuclideanSpace Real (Fin (Module.finrank Real E))

/-- The canonical coordinate isometry induced by mathlib's standard
orthonormal basis. -/
def coordEquiv
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] : E ≃ₗᵢ[Real] CoordE E :=
  (stdOrthonormalBasis Real E).equiv
    (EuclideanSpace.basisFun (Fin (Module.finrank Real E)) Real) (Equiv.refl _)

theorem coordEquiv_map_stdGaussian
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E] :
    (stdGaussian E).map (coordEquiv (E := E)) = stdGaussian (CoordE E) := by
  exact stdGaussian_map (coordEquiv (E := E))

theorem coordEquiv_preimage_stdGaussian
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A : Set (CoordE E)) (hA : MeasurableSet A) :
    stdGaussian E ((coordEquiv (E := E)) ⁻¹' A) = stdGaussian (CoordE E) A := by
  rw [← Measure.map_apply (coordEquiv (E := E)).continuous.measurable hA,
    coordEquiv_map_stdGaussian]

theorem coordEquiv_image_stdGaussian
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A : Set E) (hA : MeasurableSet A) :
    stdGaussian (CoordE E) ((coordEquiv (E := E)) '' A) = stdGaussian E A := by
  have himage : (coordEquiv (E := E)) '' A =
      (coordEquiv (E := E)).symm ⁻¹' A := by
    ext y
    constructor
    · rintro ⟨x, hx, rfl⟩
      simpa using hx
    · intro hy
      exact ⟨(coordEquiv (E := E)).symm y, hy,
        (coordEquiv (E := E)).apply_symm_apply y⟩
  rw [himage]
  have hmap : (stdGaussian (CoordE E)).map (coordEquiv (E := E)).symm =
      stdGaussian E := stdGaussian_map (coordEquiv (E := E)).symm
  rw [← Measure.map_apply (coordEquiv (E := E)).symm.continuous.measurable hA,
    hmap]

theorem coordEquiv_image_thickening
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] (r : Real) (A : Set E) :
    (coordEquiv (E := E)) '' Metric.thickening r A =
      Metric.thickening r ((coordEquiv (E := E)) '' A) := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    rw [Metric.mem_thickening_iff] at hx ⊢
    obtain ⟨z, hz, hxz⟩ := hx
    exact ⟨coordEquiv z, ⟨z, hz, rfl⟩,
      (coordEquiv (E := E)).dist_map x z ▸ hxz⟩
  · intro hy
    rw [Metric.mem_thickening_iff] at hy
    obtain ⟨z, ⟨w, hw, rfl⟩, hyz⟩ := hy
    refine ⟨(coordEquiv (E := E)).symm y, ?_,
      (coordEquiv (E := E)).apply_symm_apply y⟩
    rw [Metric.mem_thickening_iff]
    refine ⟨w, hw, ?_⟩
    calc
      dist ((coordEquiv (E := E)).symm y) w =
          dist ((coordEquiv (E := E)).symm y)
            ((coordEquiv (E := E)).symm (coordEquiv w)) := by simp
      _ = dist y (coordEquiv w) :=
        (coordEquiv (E := E)).symm.dist_map y (coordEquiv w)
      _ < r := hyz

theorem coordEquiv_preimage_thickening
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] (r : Real) (A : Set (CoordE E)) :
    (coordEquiv (E := E)) ⁻¹' Metric.thickening r A =
      Metric.thickening r ((coordEquiv (E := E)) ⁻¹' A) := by
  ext x
  constructor
  · intro hx
    change coordEquiv x ∈ Metric.thickening r A at hx
    rw [Metric.mem_thickening_iff] at hx
    rw [Metric.mem_thickening_iff]
    obtain ⟨z, hz, hxz⟩ := hx
    refine ⟨(coordEquiv (E := E)).symm z, ?_, ?_⟩
    · simpa using hz
    · calc
        dist x ((coordEquiv (E := E)).symm z) =
            dist ((coordEquiv (E := E)).symm (coordEquiv x))
              ((coordEquiv (E := E)).symm z) := by simp
        _ = dist (coordEquiv x) z :=
          (coordEquiv (E := E)).symm.dist_map (coordEquiv x) z
        _ < r := hxz
  · intro hx
    rw [Metric.mem_thickening_iff] at hx
    change coordEquiv x ∈ Metric.thickening r A
    rw [Metric.mem_thickening_iff]
    obtain ⟨z, hz, hxz⟩ := hx
    exact ⟨coordEquiv z, hz, by simpa using hxz⟩

theorem coordEquiv_thickening_measure
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (r : Real) (A : Set E) :
    stdGaussian (CoordE E)
        (Metric.thickening r ((coordEquiv (E := E)) '' A)) =
      stdGaussian E (Metric.thickening r A) := by
  rw [← coordEquiv_image_thickening]
  apply coordEquiv_image_stdGaussian
  exact Metric.isOpen_thickening.measurableSet

/-- Pulling a unit-normal defining functional across the inverse coordinate
isometry preserves its operator norm. -/
theorem coordEquiv_comp_norm
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] (L : E →L[Real] Real) :
    ‖L.comp (coordEquiv (E := E)).symm.toLinearIsometry.toContinuousLinearMap‖ =
      ‖L‖ := by
  exact L.opNorm_comp_linearIsometryEquiv (coordEquiv (E := E)).symm

/-- The coordinate image of a frozen unit-normal half-space is again a
frozen unit-normal half-space. -/
theorem coordEquiv_image_isUnitHalfspace
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] {H : Set E} (hH : IsUnitHalfspace H) :
    IsUnitHalfspace ((coordEquiv (E := E)) '' H) := by
  obtain ⟨L, c, hL, rfl⟩ := hH
  let L' : CoordE E →L[Real] Real :=
    L.comp (coordEquiv (E := E)).symm.toLinearIsometry.toContinuousLinearMap
  refine ⟨L', c, ?_, ?_⟩
  · simpa only [L'] using (coordEquiv_comp_norm L).trans hL
  · ext y
    constructor
    · rintro ⟨x, hx, rfl⟩
      change L ((coordEquiv (E := E)).symm (coordEquiv x)) <= c
      rw [(coordEquiv (E := E)).symm_apply_apply]
      exact hx
    · intro hy
      refine ⟨(coordEquiv (E := E)).symm y, ?_,
        (coordEquiv (E := E)).apply_symm_apply y⟩
      simpa only [Set.mem_setOf_eq, L', ContinuousLinearMap.comp_apply,
        LinearIsometryEquiv.coe_toLinearIsometry] using hy

/-- A frozen half-space is closed, hence Borel measurable in the ambient
`BorelSpace`. -/
theorem measurableSet_of_isUnitHalfspace
    {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    [MeasurableSpace E] [BorelSpace E] {H : Set E}
    (hH : IsUnitHalfspace H) : MeasurableSet H := by
  obtain ⟨L, c, _, rfl⟩ := hH
  exact isClosed_Iic.preimage L.continuous |>.measurableSet

/-- A unit-normal projection of the standard Gaussian has the standard real
Gaussian law, so the frozen half-space has the expected one-dimensional
measure. -/
theorem stdGaussian_unitHalfspace_measure
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (L : E →L[Real] Real) (c : Real) (hL : ‖L‖ = 1) :
    stdGaussian E {x : E | L x <= c} = gaussianReal 0 1 (Set.Iic c) := by
  change stdGaussian E (L ⁻¹' Set.Iic c) = gaussianReal 0 1 (Set.Iic c)
  rw [← Measure.map_apply L.measurable measurableSet_Iic]
  rw [IsGaussian.map_eq_gaussianReal]
  simp [integral_strongDual_stdGaussian, variance_dual_stdGaussian, hL]

/-- A unit-normal functional is one-Lipschitz. -/
theorem norm_sub_apply_le_of_isUnitNormal
    {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    (L : E →L[Real] Real) (hL : ‖L‖ = 1) (x y : E) :
    |L x - L y| <= dist x y := by
  rw [← map_sub, ← Real.norm_eq_abs, dist_eq_norm]
  calc
    ‖L (x - y)‖ <= ‖L‖ * ‖x - y‖ := L.le_opNorm (x - y)
    _ = ‖x - y‖ := by rw [hL, one_mul]

/-- Every point in the thickening lies below the shifted threshold. -/
theorem thickening_unitHalfspace_subset
    {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    (L : E →L[Real] Real) (c r : Real) (hL : ‖L‖ = 1) :
    Metric.thickening r {y : E | L y <= c} ⊆ {x : E | L x < c + r} := by
  intro x hx
  rw [Metric.mem_thickening_iff] at hx
  obtain ⟨y, hy, hxy⟩ := hx
  change L y <= c at hy
  change L x < c + r
  have hdiff : L x - L y < r := by
    calc
      L x - L y <= |L x - L y| := le_abs_self _
      _ <= dist x y := norm_sub_apply_le_of_isUnitNormal L hL x y
      _ < r := hxy
  linarith

/-- The reverse inclusion moves a point along the Riesz representer of the
unit functional. -/
theorem shifted_unitHalfspace_subset_thickening
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E]
    (L : E →L[Real] Real) (c r : Real) (hr : 0 < r) (hL : ‖L‖ = 1) :
    {x : E | L x < c + r} ⊆ Metric.thickening r {x : E | L x <= c} := by
  let v : E := (InnerProductSpace.toDual Real E).symm L
  have hvnorm : ‖v‖ = 1 := by
    change ‖(InnerProductSpace.toDual Real E).symm L‖ = 1
    rw [(InnerProductSpace.toDual Real E).symm.norm_map, hL]
  have hLv (x : E) : L x = @inner Real E _ v x := by
    symm
    exact InnerProductSpace.toDual_symm_apply
  intro x hx
  rw [Metric.mem_thickening_iff]
  by_cases hxc : L x <= c
  · exact ⟨x, hxc, by simpa using hr⟩
  · let t : Real := L x - c
    let y : E := x - t • v
    have htpos : 0 < t := sub_pos.mpr (lt_of_not_ge hxc)
    have htr : t < r := by
      change L x - c < r
      change L x < c + r at hx
      linarith
    refine ⟨y, ?_, ?_⟩
    · change L y <= c
      simp only [y, map_sub, map_smul, hLv v, real_inner_self_eq_norm_sq,
        hvnorm, one_pow, smul_eq_mul, mul_one, t]
      linarith
    · rw [dist_eq_norm]
      simp [y, norm_smul, hvnorm, abs_of_pos htpos, htr]

/-- Exact open-thickening formula for a unit-normal closed affine half-space. -/
theorem thickening_unitHalfspace_eq
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E]
    (L : E →L[Real] Real) (c r : Real) (hr : 0 < r) (hL : ‖L‖ = 1) :
    Metric.thickening r {x : E | L x <= c} = {x : E | L x < c + r} := by
  apply Set.Subset.antisymm
  · exact thickening_unitHalfspace_subset L c r hL
  · exact shifted_unitHalfspace_subset_thickening L c r hr hL

/-- Gaussian mass of every positive thickening of a frozen unit half-space. -/
theorem stdGaussian_unitHalfspace_thickening_measure
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (L : E →L[Real] Real) (c r : Real) (hr : 0 < r) (hL : ‖L‖ = 1) :
    stdGaussian E (Metric.thickening r {x : E | L x <= c}) =
      gaussianReal 0 1 (Set.Iic (c + r)) := by
  rw [thickening_unitHalfspace_eq L c r hr hL]
  change stdGaussian E (L ⁻¹' Set.Iio (c + r)) =
    gaussianReal 0 1 (Set.Iic (c + r))
  rw [← Measure.map_apply L.measurable measurableSet_Iio]
  rw [IsGaussian.map_eq_gaussianReal]
  simp only [integral_strongDual_stdGaussian, variance_dual_stdGaussian, hL,
    pow_two, one_mul, Real.toNNReal_one]
  letI : NoAtoms (gaussianReal 0 1) := noAtoms_gaussianReal (by norm_num)
  exact measure_congr (Iio_ae_eq_Iic (μ := gaussianReal 0 1))

/-- The standard real Gaussian assigns positive mass to each nonempty bounded
interval. -/
theorem stdGaussianReal_Ioc_pos {a b : Real} (hab : a < b) :
    0 < gaussianReal 0 1 (Set.Ioc a b) := by
  rw [gaussianReal_apply 0 (by norm_num) (Set.Ioc a b)]
  rw [setLIntegral_pos_iff (measurable_gaussianPDF 0 1),
    support_gaussianPDF (by norm_num), Set.univ_inter]
  rw [Real.volume_Ioc, ENNReal.ofReal_pos]
  linarith

/-- Gaussian mass of a closed lower ray is strictly increasing in its
threshold. -/
theorem strictMono_stdGaussianReal_Iic :
    StrictMono (fun c : Real => gaussianReal 0 1 (Set.Iic c)) := by
  intro a b hab
  change gaussianReal 0 1 (Set.Iic a) < gaussianReal 0 1 (Set.Iic b)
  rw [← Set.Iic_union_Ioc_eq_Iic hab.le,
    measure_union (Set.Iic_disjoint_Ioc le_rfl) measurableSet_Ioc]
  exact ENNReal.lt_add_right (measure_ne_top _ _)
    (stdGaussianReal_Ioc_pos hab).ne'

/-- Every finite standard-Gaussian threshold has strictly positive mass. -/
theorem stdGaussianReal_Iic_pos (c : Real) :
    0 < gaussianReal 0 1 (Set.Iic c) := by
  exact lt_of_le_of_lt (zero_le _)
    (strictMono_stdGaussianReal_Iic (sub_one_lt c))

/-- Every finite standard-Gaussian threshold has mass strictly below one. -/
theorem stdGaussianReal_Iic_lt_one (c : Real) :
    gaussianReal 0 1 (Set.Iic c) < 1 := by
  calc
    gaussianReal 0 1 (Set.Iic c) < gaussianReal 0 1 (Set.Iic (c + 1)) :=
      strictMono_stdGaussianReal_Iic (lt_add_one c)
    _ <= gaussianReal 0 1 Set.univ := measure_mono (Set.subset_univ _)
    _ = 1 := measure_univ

/-- The standard real Gaussian CDF is continuous. -/
theorem continuous_stdGaussianReal_cdf :
    Continuous (cdf (gaussianReal 0 1)) := by
  rw [continuous_iff_continuousAt]
  intro x
  rw [(cdf (gaussianReal 0 1)).mono.continuousAt_iff_leftLim_eq_rightLim,
    (cdf (gaussianReal 0 1)).rightLim_eq]
  haveI : NoAtoms (gaussianReal 0 1) := noAtoms_gaussianReal (by norm_num)
  have hsingleton :
      (cdf (gaussianReal 0 1)).measure {x} = 0 := by
    rw [measure_cdf]
    exact measure_singleton x
  rw [StieltjesFunction.measure_singleton] at hsingleton
  have hnonneg :
      0 <= cdf (gaussianReal 0 1) x - Function.leftLim
        (cdf (gaussianReal 0 1)) x :=
    sub_nonneg.mpr ((cdf (gaussianReal 0 1)).mono.leftLim_le le_rfl)
  exact (sub_eq_zero.mp (le_antisymm (ENNReal.ofReal_eq_zero.mp hsingleton) hnonneg)).symm

/-- Gaussian mass of a closed lower ray varies continuously with its
threshold. -/
theorem continuous_stdGaussianReal_Iic :
    Continuous (fun c : Real => gaussianReal 0 1 (Set.Iic c)) := by
  have hEq : (fun c : Real => gaussianReal 0 1 (Set.Iic c)) =
      fun c => ENNReal.ofReal (cdf (gaussianReal 0 1) c) := by
    funext c
    exact (ofReal_cdf (gaussianReal 0 1) c).symm
  rw [hEq]
  exact ENNReal.continuous_ofReal.comp continuous_stdGaussianReal_cdf

/-- Every mass strictly between zero and one is realized by a finite standard
Gaussian threshold. -/
theorem stdGaussianReal_Iic_surjective_Ioo :
    Set.Ioo (0 : ENNReal) 1 ⊆
      Set.range (fun c : Real => gaussianReal 0 1 (Set.Iic c)) := by
  intro p hp
  have hpReal : 0 < p.toReal ∧ p.toReal < 1 := by
    have hpTop : p ≠ (⊤ : ENNReal) :=
      ne_top_of_lt (hp.2.trans ENNReal.one_lt_top)
    constructor
    · exact ENNReal.toReal_pos hp.1.ne' hpTop
    · simpa only [ENNReal.toReal_one] using
        (ENNReal.toReal_lt_toReal hpTop ENNReal.one_ne_top).2 hp.2
  have hRange : p.toReal ∈ Set.range (cdf (gaussianReal 0 1)) := by
    apply mem_range_of_exists_le_of_exists_ge continuous_stdGaussianReal_cdf
    · obtain ⟨a, ha⟩ := ((tendsto_cdf_atBot (gaussianReal 0 1)).eventually
        (eventually_lt_nhds hpReal.1)).exists
      exact ⟨a, ha.le⟩
    · obtain ⟨b, hb⟩ := ((tendsto_cdf_atTop (gaussianReal 0 1)).eventually
        (eventually_gt_nhds hpReal.2)).exists
      exact ⟨b, hb.le⟩
  obtain ⟨c, hc⟩ := hRange
  refine ⟨c, ?_⟩
  change gaussianReal 0 1 (Set.Iic c) = p
  rw [← ofReal_cdf (gaussianReal 0 1) c, hc]
  exact ENNReal.ofReal_toReal (ne_top_of_lt (hp.2.trans ENNReal.one_lt_top))

/-- The finite-threshold standard-Gaussian masses are exactly the open unit
interval. -/
theorem stdGaussianReal_Iic_range :
    Set.range (fun c : Real => gaussianReal 0 1 (Set.Iic c)) =
      Set.Ioo (0 : ENNReal) 1 := by
  apply Set.Subset.antisymm
  · rintro _ ⟨c, rfl⟩
    exact ⟨stdGaussianReal_Iic_pos c, stdGaussianReal_Iic_lt_one c⟩
  · exact stdGaussianReal_Iic_surjective_Ioo

/-- A total mass-radius Gaussian profile. Null and full masses use their
natural endpoint values; finite-threshold masses use the inverse CDF. The
remaining off-range branch is irrelevant under an equal-half-space-mass
hypothesis and is totalized by zero. -/
def halfspaceProfile (p : ENNReal) (r : Real) : ENNReal := by
  classical
  let mass : Real → ENNReal := fun c => gaussianReal 0 1 (Set.Iic c)
  exact if p = 0 then 0 else if p = 1 then 1 else
    if h : p ∈ Set.range mass then
      mass ((strictMono_stdGaussianReal_Iic.orderIso mass).symm ⟨p, h⟩ + r)
    else 0

/-- The profile at a realized Gaussian mass is the shifted threshold mass. -/
theorem halfspaceProfile_stdGaussianReal_Iic (c r : Real) :
    halfspaceProfile (gaussianReal 0 1 (Set.Iic c)) r =
      gaussianReal 0 1 (Set.Iic (c + r)) := by
  rw [halfspaceProfile, if_neg (stdGaussianReal_Iic_pos c).ne',
    if_neg (stdGaussianReal_Iic_lt_one c).ne, dif_pos ⟨c, rfl⟩]
  congr 1
  apply add_right_cancel (b := -r)
  simpa only [add_neg_cancel_right] using
    Equiv.ofInjective_symm_apply strictMono_stdGaussianReal_Iic.injective c

/-- Exact inhabitant of the frozen mass-indexed half-space interface. -/
theorem halfspaceEnlargementFormula :
    forall (E : Type u) [NormedAddCommGroup E]
      [InnerProductSpace Real E] [MeasurableSpace E] [BorelSpace E]
      [FiniteDimensional Real E],
      HalfspaceEnlargementFormula (E := E) halfspaceProfile := by
  intro E _ _ _ _ _ H hH r hr
  obtain ⟨L, c, hL, rfl⟩ := hH
  rw [stdGaussian_unitHalfspace_thickening_measure L c r hr hL,
    stdGaussian_unitHalfspace_measure L c hL,
    halfspaceProfile_stdGaussianReal_Iic]

/-- Witness-level package of the threshold, thickening, and profile formulas. -/
theorem unitHalfspace_profile_formula
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    {H : Set E} (hH : IsUnitHalfspace H) (r : Real) (hr : 0 < r) :
    exists (L : E →L[Real] Real) (c : Real),
      ‖L‖ = 1 /\ H = {x | L x <= c} /\
      Metric.thickening r H = {x | L x < c + r} /\
      stdGaussian E H = gaussianReal 0 1 (Set.Iic c) /\
      stdGaussian E (Metric.thickening r H) =
        gaussianReal 0 1 (Set.Iic (c + r)) /\
      stdGaussian E (Metric.thickening r H) =
        halfspaceProfile (stdGaussian E H) r := by
  obtain ⟨L, c, hL, rfl⟩ := hH
  refine ⟨L, c, hL, rfl, thickening_unitHalfspace_eq L c r hr hL, ?_,
    stdGaussian_unitHalfspace_thickening_measure L c r hr hL, ?_⟩
  · exact stdGaussian_unitHalfspace_measure L c hL
  · exact halfspaceEnlargementFormula E _ (by exact ⟨L, c, hL, rfl⟩) r hr

/-- Coordinate transport consumes the frozen coordinate child and preserves
the complete half-space profile formula. -/
theorem coordEquiv_unitHalfspace_profile_formula
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    {H : Set E} (hH : IsUnitHalfspace H) (r : Real) (hr : 0 < r) :
    IsUnitHalfspace ((coordEquiv (E := E)) '' H) /\
      stdGaussian (CoordE E) ((coordEquiv (E := E)) '' H) = stdGaussian E H /\
      stdGaussian (CoordE E)
          (Metric.thickening r ((coordEquiv (E := E)) '' H)) =
        stdGaussian E (Metric.thickening r H) /\
      stdGaussian (CoordE E)
          (Metric.thickening r ((coordEquiv (E := E)) '' H)) =
        halfspaceProfile
          (stdGaussian (CoordE E) ((coordEquiv (E := E)) '' H)) r := by
  have hMeasurable : MeasurableSet H := measurableSet_of_isUnitHalfspace hH
  refine ⟨coordEquiv_image_isUnitHalfspace hH,
    coordEquiv_image_stdGaussian H hMeasurable, coordEquiv_thickening_measure r H, ?_⟩
  exact halfspaceEnlargementFormula (CoordE E) _
    (coordEquiv_image_isUnitHalfspace hH) r hr

/-- In dimension zero a unit-normal continuous linear functional cannot
exist. -/
theorem no_unitHalfspace_of_finrank_zero
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] (hE : Module.finrank Real E = 0) :
    forall H : Set E, ¬ IsUnitHalfspace H := by
  letI : Subsingleton E := Module.finrank_zero_iff.mp hE
  intro H hH
  obtain ⟨L, _, hL, _⟩ := hH
  have hLzero : L = 0 := by
    ext x
    rw [Subsingleton.elim x 0]
    exact L.map_zero
  have : (0 : Real) = 1 := by
    rw [hLzero, norm_zero] at hL
    exact hL
  norm_num at this

/-- A unit-normal half-space witness forces positive finite dimension. -/
theorem finrank_pos_of_unitHalfspace
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] (H : Set E) (hH : IsUnitHalfspace H) :
    0 < Module.finrank Real E := by
  exact Nat.pos_of_ne_zero fun hE => no_unitHalfspace_of_finrank_zero E hE H hH

/-- The exact comparison in the zero-dimensional branch is vacuous. -/
theorem target_of_finrank_zero
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (hE : Module.finrank Real E = 0) (A H : Set E) :
    MeasurableSet A -> IsUnitHalfspace H ->
      stdGaussian E A = stdGaussian E H ->
      forall r : Real, 0 < r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A) := by
  intro _ hH
  exact (no_unitHalfspace_of_finrank_zero E hE H hH).elim

/-- Recompose the exact target from the still-open arbitrary-set profile
bound. This theorem gives no proof credit to that premise. -/
theorem target_of_generalSetEnlargementBound
    (hGeneral : forall (E : Type u) [NormedAddCommGroup E]
      [InnerProductSpace Real E] [MeasurableSpace E] [BorelSpace E]
      [FiniteDimensional Real E],
      GeneralSetEnlargementBound (E := E) halfspaceProfile) :
    GaussianIsoperimetricTarget.{u} := by
  exact target_of_profile_bounds halfspaceProfile halfspaceEnlargementFormula hGeneral

/-- Exhaustive dimension recomposition. The positive-dimensional comparison
remains an explicit premise. -/
theorem target_of_positive_finrank_branch
    (hPositive : forall (E : Type u) [NormedAddCommGroup E]
      [InnerProductSpace Real E] [MeasurableSpace E] [BorelSpace E]
      [FiniteDimensional Real E], 0 < Module.finrank Real E ->
        forall (A H : Set E), MeasurableSet A -> IsUnitHalfspace H ->
          stdGaussian E A = stdGaussian E H -> forall r : Real, 0 < r ->
            stdGaussian E (Metric.thickening r H) <=
              stdGaussian E (Metric.thickening r A)) :
    GaussianIsoperimetricTarget.{u} := by
  intro E _ _ _ _ _ A H hA hH hMeasure r hr
  by_cases hE : Module.finrank Real E = 0
  · exact target_of_finrank_zero E hE A H hA hH hMeasure r hr
  · exact hPositive E (Nat.pos_of_ne_zero hE) A H hA hH hMeasure r hr

end Stage1Instances.THM_M_0996

#print axioms Stage1Instances.THM_M_0996.measurableSet_of_isUnitHalfspace
#print axioms Stage1Instances.THM_M_0996.coordEquiv
#print axioms Stage1Instances.THM_M_0996.coordEquiv_map_stdGaussian
#print axioms Stage1Instances.THM_M_0996.coordEquiv_preimage_stdGaussian
#print axioms Stage1Instances.THM_M_0996.coordEquiv_image_stdGaussian
#print axioms Stage1Instances.THM_M_0996.coordEquiv_image_thickening
#print axioms Stage1Instances.THM_M_0996.coordEquiv_preimage_thickening
#print axioms Stage1Instances.THM_M_0996.coordEquiv_thickening_measure
#print axioms Stage1Instances.THM_M_0996.coordEquiv_comp_norm
#print axioms Stage1Instances.THM_M_0996.coordEquiv_image_isUnitHalfspace
#print axioms Stage1Instances.THM_M_0996.stdGaussian_unitHalfspace_measure
#print axioms Stage1Instances.THM_M_0996.norm_sub_apply_le_of_isUnitNormal
#print axioms Stage1Instances.THM_M_0996.thickening_unitHalfspace_subset
#print axioms Stage1Instances.THM_M_0996.shifted_unitHalfspace_subset_thickening
#print axioms Stage1Instances.THM_M_0996.thickening_unitHalfspace_eq
#print axioms Stage1Instances.THM_M_0996.stdGaussian_unitHalfspace_thickening_measure
#print axioms Stage1Instances.THM_M_0996.stdGaussianReal_Ioc_pos
#print axioms Stage1Instances.THM_M_0996.strictMono_stdGaussianReal_Iic
#print axioms Stage1Instances.THM_M_0996.stdGaussianReal_Iic_pos
#print axioms Stage1Instances.THM_M_0996.stdGaussianReal_Iic_lt_one
#print axioms Stage1Instances.THM_M_0996.continuous_stdGaussianReal_cdf
#print axioms Stage1Instances.THM_M_0996.continuous_stdGaussianReal_Iic
#print axioms Stage1Instances.THM_M_0996.stdGaussianReal_Iic_surjective_Ioo
#print axioms Stage1Instances.THM_M_0996.stdGaussianReal_Iic_range
#print axioms Stage1Instances.THM_M_0996.halfspaceProfile
#print axioms Stage1Instances.THM_M_0996.halfspaceProfile_stdGaussianReal_Iic
#print axioms Stage1Instances.THM_M_0996.halfspaceEnlargementFormula
#print axioms Stage1Instances.THM_M_0996.unitHalfspace_profile_formula
#print axioms Stage1Instances.THM_M_0996.coordEquiv_unitHalfspace_profile_formula
#print axioms Stage1Instances.THM_M_0996.no_unitHalfspace_of_finrank_zero
#print axioms Stage1Instances.THM_M_0996.finrank_pos_of_unitHalfspace
#print axioms Stage1Instances.THM_M_0996.target_of_finrank_zero
#print axioms Stage1Instances.THM_M_0996.target_of_generalSetEnlargementBound
#print axioms Stage1Instances.THM_M_0996.target_of_positive_finrank_branch
