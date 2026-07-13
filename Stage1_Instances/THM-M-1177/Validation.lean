import Statement
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1177 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently reconstructs the nonpositive-maximum package directly from the
frozen statement definitions. The positive-maximum package and exact ABP root
remain open.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1177.Validation

/-- The frozen coordinate positive-definiteness predicate implies mathlib's
finite-matrix positive-definiteness predicate. -/
private theorem validationSPDToPosDef {n : Nat}
    {A : Matrix (Fin n) (Fin n) Real}
    (hA : IsSymmetricPositiveDefinite A) : A.PosDef := by
  rw [Matrix.posDef_iff_dotProduct_mulVec]
  constructor
  · simpa [Matrix.IsHermitian] using hA.1
  · intro v hv
    simpa [dotProduct] using hA.2 v hv

/-- The determinant-weighted integrand is nonnegative on the domain. -/
private theorem validationIntegrandNonneg {n : Nat}
    {Omega : Set (Euclidean n)} {f : Euclidean n -> Real}
    {A : Euclidean n -> Matrix (Fin n) (Fin n) Real}
    (hApos : forall x, x ∈ Omega -> IsSymmetricPositiveDefinite (A x)) :
    forall x, x ∈ Omega ->
      0 <= (max (-f x) 0) ^ n / Matrix.det (A x) := by
  intro x hx
  exact div_nonneg (pow_nonneg (le_max_right _ _) _)
    ((validationSPDToPosDef (hApos x hx)).det_pos.le)

/-- The frozen contact set is contained in the domain. -/
private theorem validationContactSubset {n : Nat}
    (Omega : Set (Euclidean n)) (u : Euclidean n -> Real) :
    upperContactSet Omega u ⊆ Omega := fun _ hx => hx.1

/-- The weighted contact-set integral is nonnegative without assuming that
the contact set itself is measurable. -/
private theorem validationIntegralNonneg {n : Nat}
    {Omega : Set (Euclidean n)} {u f : Euclidean n -> Real}
    {A : Euclidean n -> Matrix (Fin n) (Fin n) Real}
    (hopen : IsOpen Omega)
    (hbounded : Bornology.IsBounded Omega)
    (hApos : forall x, x ∈ Omega -> IsSymmetricPositiveDefinite (A x)) :
    0 <= ∫ x in upperContactSet Omega u,
      (max (-f x) 0) ^ n / Matrix.det (A x) := by
  let contact := upperContactSet Omega u
  have hfinite : volume contact ≠ (⊤ : ENNReal) := by
    exact (lt_of_le_of_lt
      (measure_mono (validationContactSubset Omega u) :
        volume contact <= volume Omega)
      (hbounded.measure_lt_top : volume Omega < ⊤)).ne
  have hrestrict : volume.restrict (Omega ∩ toMeasurable volume contact) =
      volume.restrict contact := by
    apply Measure.restrict_inter_toMeasurable hfinite
    · exact hopen.measurableSet
    · exact validationContactSubset Omega u
  apply integral_nonneg_of_ae
  rw [← hrestrict]
  exact (ae_restrict_mem
    (hopen.measurableSet.inter
      (measurableSet_toMeasurable volume contact))).mono fun x hx =>
    validationIntegrandNonneg hApos x hx.1

/-- Same-worker differential reconstruction of frozen obligation
`M1177-B-DEGENERATE`. -/
theorem differentialDegenerateMaximumPackage (n : Nat) (Cn : Real)
    (hCn : 0 <= Cn) :
    forall (Omega : Set (Euclidean n))
      (u f : Euclidean n -> Real)
      (A : Euclidean n -> Matrix (Fin n) (Fin n) Real),
      IsOpen Omega -> IsPreconnected Omega -> Bornology.IsBounded Omega ->
      ContinuousOn u (closure Omega) -> ContDiffOn Real 2 u Omega ->
      Measurable f ->
      (forall i j, Measurable fun x => A x i j) ->
      (forall x, x ∈ Omega -> IsSymmetricPositiveDefinite (A x)) ->
      (forall x, x ∈ Omega ->
        Matrix.trace (A x * hessian u x) >= f x) ->
      (forall x, x ∈ frontier Omega -> u x <= 0) ->
      IntegrableOn
        (fun x => (max (-f x) 0) ^ n / Matrix.det (A x))
        (upperContactSet Omega u) ->
      sSup (u '' Omega) <= 0 ->
      sSup (u '' Omega) <=
        Cn * Metric.diam Omega * weightedNegativeNorm Omega u f A := by
  intro Omega u f A hopen _ hbounded _ _ _ _ hApos _ _ _ hmax
  exact hmax.trans (mul_nonneg
    (mul_nonneg hCn Metric.diam_nonneg)
    (Real.rpow_nonneg
      (validationIntegralNonneg hopen hbounded hApos) _))

assert_no_sorry differentialDegenerateMaximumPackage
#print sorries differentialDegenerateMaximumPackage
#print axioms differentialDegenerateMaximumPackage

end Stage1Instances.THM_M_1177.Validation
