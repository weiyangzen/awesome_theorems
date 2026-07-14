import Statement
import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-1084 Gaussian MGF bridge

This module proves the first analytic leaf of the frozen Dudley chaining route: a centered real
Gaussian random variable is sub-Gaussian with parameter equal to its second moment.  The body uses
the exact Gaussian pushforward law and its pinned moment-generating-function formula.
-/

noncomputable section

open MeasureTheory Set
open scoped NNReal

namespace Stage1Instances.THM_M_1084.Proof

universe u v

/-- Exact increment-Gaussian consequence of the frozen finite-linear-combination definition. -/
theorem increment_hasGaussianLaw {T : Type u} {Omega : Type v} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : T -> Omega -> Real}
    (hX : IsRealGaussianProcess mu X) (s t : T) :
    ProbabilityTheory.HasGaussianLaw (fun omega => X s omega - X t omega) mu := by
  classical
  by_cases hst : s = t
  · subst t
    convert hX ∅ (fun _ => 0) using 1
    simp
  · convert hX {s, t} (fun x => if x = s then 1 else if x = t then -1 else 0) using 1
    ext omega
    simp [hst, Ne.symm hst, sub_eq_add_neg]

/-- The frozen process interface entails that the ambient measure is a probability measure. -/
theorem isProbabilityMeasure_of_process {T : Type u} [Nonempty T]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega} {X : T -> Omega -> Real}
    (hX : IsRealGaussianProcess mu X) : IsProbabilityMeasure mu := by
  let t : T := Classical.choice inferInstance
  exact (increment_hasGaussianLaw hX t t).isProbabilityMeasure

/-- Every frozen process coordinate is integrable. -/
theorem coordinate_integrable {T : Type u} {Omega : Type v} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : T -> Omega -> Real}
    (hX : IsRealGaussianProcess mu X) (s : T) : Integrable (X s) mu := by
  classical
  convert (hX {s} (fun _ => 1)).integrable using 1
  ext omega
  simp

/-- A Gaussian law represented by the frozen finite-linear-combination interface has the exact
Gaussian pushforward measure. -/
theorem gaussian_map_eq
    {Omega : Type*} [MeasurableSpace Omega] {mu : Measure Omega} {Y : Omega -> Real}
    (hGaussian : ProbabilityTheory.HasGaussianLaw Y mu) :
    mu.map Y = ProbabilityTheory.gaussianReal (∫ omega, Y omega ∂mu)
      (Real.toNNReal (ProbabilityTheory.variance Y mu)) := by
  have hMap := hGaussian.isGaussian_map.eq_gaussianReal (mu.map Y)
  rw [MeasureTheory.integral_map hGaussian.aemeasurable (f := id)
    measurable_id'.aestronglyMeasurable] at hMap
  rw [ProbabilityTheory.variance_map (X := id) measurable_id'.aemeasurable
    hGaussian.aemeasurable] at hMap
  simpa only [id_eq] using hMap

/-- A centered real Gaussian variable has its variance as an exact sub-Gaussian MGF parameter. -/
theorem hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero
    {Omega : Type*} [MeasurableSpace Omega] {mu : Measure Omega} {Y : Omega -> Real}
    (hGaussian : ProbabilityTheory.HasGaussianLaw Y mu)
    (hCentered : ∫ omega, Y omega ∂mu = 0) :
    ProbabilityTheory.HasSubgaussianMGF Y
      (Real.toNNReal (∫ omega, Y omega ^ 2 ∂mu)) mu := by
  have hMap : mu.map Y = ProbabilityTheory.gaussianReal 0
      (Real.toNNReal (∫ omega, Y omega ^ 2 ∂mu)) := by
    rw [gaussian_map_eq hGaussian,
      ProbabilityTheory.variance_of_integral_eq_zero hGaussian.aemeasurable hCentered,
      hCentered]
  constructor
  · intro t
    have hMapped := ProbabilityTheory.integrable_exp_mul_gaussianReal
      (μ := 0) (v := Real.toNNReal (∫ omega, Y omega ^ 2 ∂mu)) t
    rw [← hMap] at hMapped
    rw [MeasureTheory.integrable_map_measure (by fun_prop) hGaussian.aemeasurable] at hMapped
    exact hMapped
  · intro t
    rw [ProbabilityTheory.mgf_gaussianReal hMap]
    simp

/-- The exact Gaussian-to-canonical-sub-Gaussian MGF identity required by native chaining. -/
theorem increment_mgf_eq_dist_sq
    {T : Type u} [PseudoMetricSpace T] {Omega : Type v} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : T -> Omega -> Real}
    (hX : IsRealGaussianProcess mu X)
    (hCentered : forall t, ∫ omega, X t omega ∂mu = 0)
    (hCanonical : forall s t, dist s t = canonicalDist mu X s t)
    (s t : T) (l : Real) :
    ProbabilityTheory.mgf (fun omega => X s omega - X t omega) mu l =
      Real.exp (l ^ 2 * dist s t ^ 2 / 2) := by
  have hGaussian := increment_hasGaussianLaw hX s t
  have hIncrementCentered : ∫ omega, X s omega - X t omega ∂mu = 0 := by
    rw [integral_sub (coordinate_integrable hX s) (coordinate_integrable hX t), hCentered,
      hCentered, sub_self]
  have hMap := gaussian_map_eq hGaussian
  rw [ProbabilityTheory.mgf_gaussianReal hMap]
  rw [ProbabilityTheory.variance_of_integral_eq_zero hGaussian.aemeasurable hIncrementCentered]
  rw [hIncrementCentered]
  have hnonneg : 0 <= ∫ omega, (X s omega - X t omega) ^ 2 ∂mu :=
    integral_nonneg fun _ => sq_nonneg _
  have hdistSq : dist s t ^ 2 = ∫ omega, (X s omega - X t omega) ^ 2 ∂mu := by
    rw [hCanonical, canonicalDist]
    exact Real.sq_sqrt hnonneg
  rw [Real.coe_toNNReal _ hnonneg, hdistSq]
  ring_nf

/-- Each canonical increment is sub-Gaussian with the exact squared-distance parameter. -/
theorem increment_hasSubgaussianMGF
    {T : Type u} [PseudoMetricSpace T] {Omega : Type v} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : T -> Omega -> Real}
    (hX : IsRealGaussianProcess mu X)
    (hCentered : forall t, ∫ omega, X t omega ∂mu = 0)
    (hCanonical : forall s t, dist s t = canonicalDist mu X s t)
    (s t : T) :
    ProbabilityTheory.HasSubgaussianMGF (fun omega => X s omega - X t omega)
      (Real.toNNReal (dist s t ^ 2)) mu := by
  have hGaussian := increment_hasGaussianLaw hX s t
  have hIncrementCentered : ∫ omega, X s omega - X t omega ∂mu = 0 := by
    rw [integral_sub (coordinate_integrable hX s) (coordinate_integrable hX t), hCentered,
      hCentered, sub_self]
  have h :=
    hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero hGaussian hIncrementCentered
  have hnonneg : 0 <= ∫ omega, (X s omega - X t omega) ^ 2 ∂mu :=
    integral_nonneg fun _ => sq_nonneg _
  have hparam : Real.toNNReal (∫ omega, (X s omega - X t omega) ^ 2 ∂mu) =
      Real.toNNReal (dist s t ^ 2) := by
    congr 1
    rw [hCanonical, canonicalDist, Real.sq_sqrt hnonneg]
  rw [← hparam]
  exact h

/-- Exact package for the frozen Gaussian-to-sub-Gaussian MGF obligation. -/
def GaussianIncrementMGFPackage : Prop :=
  forall (T : Type u) [PseudoMetricSpace T] [Nonempty T]
    (Omega : Type v) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : T -> Omega -> Real),
      IsRealGaussianProcess mu X ->
      (forall t, ∫ omega, X t omega ∂mu = 0) ->
      (forall s t, dist s t = canonicalDist mu X s t) ->
      forall s t,
        ProbabilityTheory.HasSubgaussianMGF (fun omega => X s omega - X t omega)
          (Real.toNNReal (dist s t ^ 2)) mu

/-- The local scalar and increment bridges compose into the exact frozen MGF package. -/
theorem gaussianIncrementMGFPackage : GaussianIncrementMGFPackage.{u, v} := by
  intro T _ _ Omega _ mu X hGaussian hCentered hCanonical s t
  exact increment_hasSubgaussianMGF hGaussian hCentered hCanonical s t

#print sorries hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero
#print axioms hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero
#print sorries increment_mgf_eq_dist_sq
#print axioms increment_mgf_eq_dist_sq
#print sorries increment_hasSubgaussianMGF
#print axioms increment_hasSubgaussianMGF
#print sorries gaussianIncrementMGFPackage
#print axioms gaussianIncrementMGFPackage

end Stage1Instances.THM_M_1084.Proof
