import «Stage1_Instances».«THM-M-0990».Statement

/-!
# Normalization packages for THM-M-0990

This module centers each triangular-array entry, restricts row `n` to `Fin n`,
and divides by the frozen row scale. The checked lemmas transport
measurability, second moments, centering, independence, variance, and row sums
without strengthening the eventual positivity premise in `StatementShape`.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped BigOperators ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0990

universe u

variable {Omega : Type u} [MeasurableSpace Omega]

def normalizedIncrement (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (n : Nat) (k : Fin n) (omega : Omega) : Real :=
  (rowScale P X n)⁻¹ * centered P X n k.val omega

theorem centered_measurable
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (hMeas : ∀ n k, Measurable (X n k)) (n k : Nat) :
    Measurable (centered P X n k) := by
  exact (hMeas n k).sub measurable_const

theorem centered_memLp
    [IsProbabilityMeasure P] (X : Nat -> Nat -> Omega -> Real)
    (hLp : ∀ n k, MemLp (X n k) 2 P) (n k : Nat) :
    MemLp (centered P X n k) 2 P := by
  exact (hLp n k).sub (memLp_const _)

theorem centered_integral_eq_zero
    {P : Measure Omega} [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real)
    (hLp : ∀ n k, MemLp (X n k) 2 P) (n k : Nat) :
    P[centered P X n k] = 0 := by
  unfold centered
  rw [integral_sub, integral_const]
  · simp
  · exact (hLp n k).integrable (by norm_num)
  · exact integrable_const _

theorem normalizedIncrement_memLp
    {P : Measure Omega} [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real)
    (hLp : ∀ n k, MemLp (X n k) 2 P) (n : Nat) (k : Fin n) :
    MemLp (normalizedIncrement P X n k) 2 P := by
  exact (centered_memLp X hLp n k.val).const_mul _

theorem normalizedIncrement_integral_eq_zero
    {P : Measure Omega} [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real)
    (hLp : ∀ n k, MemLp (X n k) 2 P) (n : Nat) (k : Fin n) :
    P[normalizedIncrement P X n k] = 0 := by
  unfold normalizedIncrement
  rw [integral_const_mul, centered_integral_eq_zero X hLp n k.val, mul_zero]

theorem normalizedIncrement_independent
    {P : Measure Omega} [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real)
    (hInd : ∀ n, iIndepFun (X n) P) (n : Nat) :
    iIndepFun (normalizedIncrement P X n) P := by
  have hpre : iIndepFun (fun k : Fin n => X n k.val) P :=
    (hInd n).precomp Fin.val_injective
  have hcomp := hpre.comp
    (fun k x => (rowScale P X n)⁻¹ * (x - ∫ y, X n k.val y ∂P))
    (by intro k; fun_prop)
  exact hcomp

theorem normalizedIncrement_variance_sum
    {P : Measure Omega} [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real)
    (hMeas : ∀ n k, Measurable (X n k))
    (n : Nat) (hvar : 0 < rowVarianceSum P X n) :
    (∑ k : Fin n, variance (normalizedIncrement P X n k) P) = 1 := by
  have hscale : 0 < rowScale P X n := by
    exact Real.sqrt_pos.2 hvar
  unfold normalizedIncrement
  have hvarcenter (k : Fin n) :
      variance (centered P X n k.val) P =
        variance (X n k.val) P :=
    variance_sub_const (hMeas n k.val).aestronglyMeasurable _
  rw [Finset.sum_congr rfl (fun k _ => by
    rw [variance_const_mul, hvarcenter k])]
  rw [← Finset.mul_sum]
  have hfin : (∑ k : Fin n, variance (X n k.val) P) =
      ∑ k ∈ Finset.range n, variance (X n k) P := by
    rw [Finset.sum_fin_eq_sum_range]
    exact Finset.sum_congr rfl fun k hk => by
      rw [dif_pos (Finset.mem_range.1 hk)]
  rw [hfin]
  change (rowScale P X n)⁻¹ ^ 2 * rowVarianceSum P X n = 1
  have hsquare : rowScale P X n ^ 2 = rowVarianceSum P X n := by
    unfold rowScale
    exact Real.sq_sqrt hvar.le
  rw [← hsquare]
  field_simp

theorem normalizedIncrement_sum
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real) (n : Nat) :
    (fun omega => ∑ k : Fin n, normalizedIncrement P X n k omega) =
      normalizedRowSum P X n := by
  funext omega
  unfold normalizedIncrement normalizedRowSum
  rw [← Finset.mul_sum]
  congr 1
  rw [Finset.sum_fin_eq_sum_range]
  exact Finset.sum_congr rfl fun k hk => by
    rw [dif_pos (Finset.mem_range.1 hk)]

#print axioms normalizedIncrement_variance_sum
#print axioms centered_measurable
#print axioms centered_memLp
#print axioms centered_integral_eq_zero
#print axioms normalizedIncrement_memLp
#print axioms normalizedIncrement_integral_eq_zero
#print axioms normalizedIncrement_independent
#print axioms normalizedIncrement_sum

end Stage1Instances.THM_M_0990
