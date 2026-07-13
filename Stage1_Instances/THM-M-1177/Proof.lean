import ObligationTree
import Mathlib.Analysis.Matrix.PosDef

/-!
# THM-M-1177 proof-phase bodies

This module closes the complete nonpositive-maximum branch of the frozen ABP
architecture.  The contact-set/area-formula positive branch remains an
explicit premise of the final composition theorem below.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1177

/-- The statement's coordinate positive-definiteness predicate agrees with
mathlib's finite positive-definite matrix predicate. -/
theorem frozenSPD_to_posDef {n : Nat}
    {A : Matrix (Fin n) (Fin n) Real}
    (hA : IsSymmetricPositiveDefinite A) : A.PosDef := by
  rw [Matrix.posDef_iff_dotProduct_mulVec]
  constructor
  · simpa [Matrix.IsHermitian] using hA.1
  · intro v hv
    simpa [dotProduct] using hA.2 v hv

/-- The determinant-weighted integrand is nonnegative wherever the frozen
positive-definiteness hypothesis applies. -/
theorem weightedIntegrand_nonneg_on_domain {n : Nat}
    {Omega : Set (Euclidean n)} {f : Euclidean n -> Real}
    {A : Euclidean n -> Matrix (Fin n) (Fin n) Real}
    (hApos : ∀ x, x ∈ Omega -> IsSymmetricPositiveDefinite (A x)) :
    ∀ x, x ∈ Omega ->
      0 <= (max (-f x) 0) ^ n / Matrix.det (A x) := by
  intro x hx
  exact div_nonneg (pow_nonneg (le_max_right _ _) _)
    ((frozenSPD_to_posDef (hApos x hx)).det_pos.le)

/-- The frozen contact-set definition retains domain membership. -/
theorem upperContactSet_subset_domain {n : Nat}
    (Omega : Set (Euclidean n)) (u : Euclidean n -> Real) :
    upperContactSet Omega u ⊆ Omega := fun _ hx => hx.1

/-- A contact set inside a bounded Euclidean domain has finite volume. -/
theorem upperContactSet_volume_ne_top {n : Nat}
    {Omega : Set (Euclidean n)} {u : Euclidean n -> Real}
    (hbounded : Bornology.IsBounded Omega) :
    volume (upperContactSet Omega u) ≠ (⊤ : ENNReal) := by
  exact (lt_of_le_of_lt
    (measure_mono (upperContactSet_subset_domain Omega u) :
      volume (upperContactSet Omega u) <= volume Omega)
    (hbounded.measure_lt_top : volume Omega < ⊤)).ne

/-- The weighted set integral is nonnegative.  No measurability of the frozen
contact set is assumed: finite volume identifies its restriction measure with
the restriction to the intersection of its measurable hull and the measurable
open domain. -/
theorem weightedIntegral_nonneg {n : Nat}
    {Omega : Set (Euclidean n)} {u f : Euclidean n -> Real}
    {A : Euclidean n -> Matrix (Fin n) (Fin n) Real}
    (hopen : IsOpen Omega)
    (hbounded : Bornology.IsBounded Omega)
    (hApos : ∀ x, x ∈ Omega -> IsSymmetricPositiveDefinite (A x)) :
    0 <= ∫ x in upperContactSet Omega u,
      (max (-f x) 0) ^ n / Matrix.det (A x) := by
  let contact := upperContactSet Omega u
  have hfinite : volume contact ≠ (⊤ : ENNReal) :=
    upperContactSet_volume_ne_top hbounded
  have hrestrict : volume.restrict (Omega ∩ toMeasurable volume contact) =
      volume.restrict contact := by
    apply Measure.restrict_inter_toMeasurable hfinite
    · exact hopen.measurableSet
    · exact upperContactSet_subset_domain Omega u
  apply integral_nonneg_of_ae
  rw [← hrestrict]
  exact (ae_restrict_mem
    (hopen.measurableSet.inter
      (measurableSet_toMeasurable volume contact))).mono fun x hx =>
    weightedIntegrand_nonneg_on_domain hApos x
      hx.1

/-- The real-power normalization in the frozen right-hand side is
nonnegative. -/
theorem weightedNegativeNorm_nonneg {n : Nat}
    {Omega : Set (Euclidean n)} {u f : Euclidean n -> Real}
    {A : Euclidean n -> Matrix (Fin n) (Fin n) Real}
    (hopen : IsOpen Omega)
    (hbounded : Bornology.IsBounded Omega)
    (hApos : ∀ x, x ∈ Omega -> IsSymmetricPositiveDefinite (A x)) :
    0 <= weightedNegativeNorm Omega u f A := by
  apply Real.rpow_nonneg
  exact weightedIntegral_nonneg hopen hbounded hApos

/-- Closed proof body for frozen obligation `M1177-B-DEGENERATE`. -/
theorem degenerateMaximumPackage (n : Nat) (Cn : Real)
    (hCn : 0 <= Cn) : DegenerateMaximumPackage n Cn := by
  intro Omega u f A hypotheses hmax
  unfold ABPBound
  exact hmax.trans (mul_nonneg
    (mul_nonneg hCn Metric.diam_nonneg)
    (weightedNegativeNorm_nonneg hypotheses.1 hypotheses.2.2.1
      hypotheses.2.2.2.2.2.2.2.1))

/-- Root composition with only the substantive positive-maximum package left
explicit. -/
theorem abpTarget_of_positiveMaximumPackage
    (positive : forall n : Nat, 1 <= n ->
      exists Cn : Real, 0 <= Cn ∧ PositiveMaximumPackage n Cn) :
    AlexandrovBakelmanPucciTarget := by
  apply root_of_architecture
  intro n hn
  obtain ⟨Cn, hCn, hpositive⟩ := positive n hn
  exact ⟨Cn, hCn, degenerateMaximumPackage n Cn hCn, hpositive⟩

#print axioms frozenSPD_to_posDef
#print axioms weightedIntegrand_nonneg_on_domain
#print axioms upperContactSet_subset_domain
#print axioms upperContactSet_volume_ne_top
#print axioms weightedIntegral_nonneg
#print axioms weightedNegativeNorm_nonneg
#print axioms degenerateMaximumPackage
#print axioms abpTarget_of_positiveMaximumPackage

end Stage1Instances.THM_M_1177
