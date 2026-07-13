import «Stage1_Instances».«THM-M-0989».ObligationTree

/-!
# Partial proof bodies for THM-M-0989

This module closes three exact obligations from the frozen proof architecture:
finite-row measurability, characteristic-function factorization, and the
centered second-moment normalization.  It does not assert the triangular-array
Lindeberg estimate or the theorem root.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped BigOperators ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0989

universe u

/-- `M0989-S-MEAS`: every finite row sum is almost-everywhere measurable. -/
theorem rowSumsAEMeasurable_proof
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) :
    RowSumsAEMeasurable A := by
  intro n
  exact Finset.aemeasurable_fun_sum Finset.univ
    (fun k _ => A.rowAEMeasurable n k)

/-- `M0989-C-FACTOR`: row independence factors the row characteristic function. -/
theorem rowCharFun_factorization
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) (n : Nat) :
    charFun (A.probabilityMeasure.map (rowSum A n)) =
      ∏ k : Fin (n + 1),
        charFun (A.probabilityMeasure.map (A.increment n k)) := by
  apply (A.rowIndependent n).charFun_map_fun_sum_eq_prod
  exact A.rowAEMeasurable n

/-- `M0989-N-MOMENTS`: centering identifies variance with the second moment,
so the row second moments sum to one. -/
theorem rowSecondMoment_sum
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) (n : Nat) :
    (∑ k : Fin (n + 1),
      A.probabilityMeasure[(A.increment n k) ^ 2]) = 1 := by
  rw [← A.rowVarianceNormalized n]
  apply Finset.sum_congr rfl
  intro k _
  rw [variance_of_integral_eq_zero
    (A.rowAEMeasurable n k) (A.rowCentered n k)]
  rfl

/-- The total linear term in every centered row is zero. -/
theorem rowExpectation_sum
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) (n : Nat) :
    (∑ k : Fin (n + 1),
      A.probabilityMeasure[A.increment n k]) = 0 := by
  simp [A.rowCentered]

/-- Unit total second moment gives the Gaussian quadratic coefficient at
every frequency. -/
theorem rowGaussianQuadraticCoefficient
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) (n : Nat) (t : Real) :
    (∑ k : Fin (n + 1),
      A.probabilityMeasure[(A.increment n k) ^ 2] * t ^ 2 / 2) =
        t ^ 2 / 2 := by
  rw [← Finset.sum_div, ← Finset.sum_mul, rowSecondMoment_sum]
  simp

/-- The frozen truncated second moment is nonnegative. -/
theorem truncatedSecondMoment_nonneg
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Omega -> Real) (epsilon : Real) :
    0 <= truncatedSecondMoment P X epsilon := by
  apply integral_nonneg
  intro omega
  exact mul_nonneg (sq_nonneg _) (by split <;> simp_all)

/-- Square integrability implies integrability of the exact strict-threshold
truncation used by the frozen Lindeberg condition. -/
theorem integrable_truncatedSecondMoment_integrand
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {X : Omega -> Real} {epsilon : Real}
    (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P) :
    Integrable (fun omega => (X omega) ^ 2 *
      if epsilon < ‖X omega‖ then 1 else 0) P := by
  let s : Set Omega := {omega | epsilon < ‖X omega‖}
  have hs : NullMeasurableSet s P :=
    nullMeasurableSet_lt aemeasurable_const hXmeas.norm
  have hind : s.indicator (fun omega => (X omega) ^ 2) =
      fun omega => (X omega) ^ 2 *
        if epsilon < ‖X omega‖ then 1 else 0 := by
    funext omega
    by_cases h : omega ∈ s <;> simp [Set.indicator, s]
  rw [← hind]
  exact hXsq.indicator₀ hs

/-- The truncated second moment is bounded by the full second moment. -/
theorem truncatedSecondMoment_le_secondMoment
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {X : Omega -> Real} {epsilon : Real}
    (hXmeas : AEMeasurable X P)
    (hXsq : Integrable (fun omega => (X omega) ^ 2) P) :
    truncatedSecondMoment P X epsilon <=
      integral P (fun omega => (X omega) ^ 2) := by
  unfold truncatedSecondMoment
  apply integral_mono
    (integrable_truncatedSecondMoment_integrand hXmeas hXsq) hXsq
  intro omega
  change X omega ^ 2 * (if epsilon < ‖X omega‖ then 1 else 0) <=
    X omega ^ 2
  split <;> simp [sq_nonneg]

/-- Checked composition after discharging the measurability package.  The
characteristic-function limit remains an explicit, unproved premise. -/
theorem root_of_row_charFun_convergence
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega)
    (hchar : RowLawCharFunConverges A) :
    letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
    TendstoInDistribution
      (fun n => rowSum A n)
      atTop
      (id : Real -> Real)
      (fun _ => A.probabilityMeasure)
      (gaussianReal 0 1) :=
  root_of_row_charFun_packages A (rowSumsAEMeasurable_proof A) hchar

#print axioms rowSumsAEMeasurable_proof
#print axioms rowCharFun_factorization
#print axioms rowSecondMoment_sum
#print axioms rowExpectation_sum
#print axioms rowGaussianQuadraticCoefficient
#print axioms truncatedSecondMoment_nonneg
#print axioms integrable_truncatedSecondMoment_integrand
#print axioms truncatedSecondMoment_le_secondMoment
#print axioms root_of_row_charFun_convergence

end Stage1Instances.THM_M_0989
