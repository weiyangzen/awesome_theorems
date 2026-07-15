import Statement
import Mathlib.Combinatorics.Enumerative.Partition.Glaisher

/-!
# THM-M-0510 proof-phase bodies

This module closes the ordinary-partition formal-power-series normalization
used by the frozen circle-method architecture.  It does not prove the
Hardy-Ramanujan asymptotic: coefficient extraction, contour estimates, and
the major/minor-arc argument remain open.
-/

noncomputable section

open scoped PowerSeries.WithPiTopology

namespace Stage1Instances.THM_M_0510

open PowerSeries

/-- The ordinary partition generating series over the reals. -/
def ordinaryPartitionSeries : Real⟦X⟧ :=
  PowerSeries.mk partitionCount

/-- The coefficient convention agrees definitionally with the canonical
real-valued partition count used by the Hardy-Ramanujan target. -/
@[simp]
theorem coeff_ordinaryPartitionSeries (n : Nat) :
    ordinaryPartitionSeries.coeff n = partitionCount n := by
  simp [ordinaryPartitionSeries]

/-- Each geometric Euler factor cancels `1 - X^(i+1)`. -/
theorem geometricFactor_mul_oneSub (i : Nat) :
    (∑' j : Nat, (X : Real⟦X⟧) ^ ((i + 1) * j)) *
      (1 - X ^ (i + 1)) = 1 := by
  simpa [pow_mul] using
    (PowerSeries.WithPiTopology.tsum_pow_mul_one_sub_of_constantCoeff_eq_zero
      (f := (X : Real⟦X⟧) ^ (i + 1)) (by simp))

/-- The pinned partition generating-function theorem specialized to all
positive parts.  This fills the specialization left as a TODO in the
`Partition.GenFun` module documentation. -/
theorem hasProd_ordinaryPartitionSeries_geometric :
    HasProd
      (fun i : Nat => ∑' j : Nat, (X : Real⟦X⟧) ^ ((i + 1) * j))
      ordinaryPartitionSeries := by
  simpa [ordinaryPartitionSeries, partitionCount, Nat.Partition.restricted] using
    (Nat.Partition.hasProd_powerSeriesMk_card_restricted Real (fun _ => True))

/-- Equality form of the geometric-factor Euler product. -/
theorem ordinaryPartitionSeries_eq_geometricProduct :
    ordinaryPartitionSeries =
      ∏' i : Nat, ∑' j : Nat, (X : Real⟦X⟧) ^ ((i + 1) * j) :=
  hasProd_ordinaryPartitionSeries_geometric.tprod_eq.symm

/-- Euler's product identity: the ordinary partition series is the inverse of
the product of `1 - X^m`, expressed without adding a field-only inverse to
real formal power series. -/
theorem ordinaryPartitionSeries_mul_eulerProduct :
    ordinaryPartitionSeries *
      ∏' i : Nat, (1 - (X : Real⟦X⟧) ^ (i + 1)) = 1 := by
  rw [ordinaryPartitionSeries_eq_geometricProduct]
  rw [← hasProd_ordinaryPartitionSeries_geometric.multipliable.tprod_mul
    (PowerSeries.WithPiTopology.multipliable_one_sub_X_pow Real)]
  simpa using tprod_congr (fun i => geometricFactor_mul_oneSub i)

#check coeff_ordinaryPartitionSeries
#check geometricFactor_mul_oneSub
#check hasProd_ordinaryPartitionSeries_geometric
#check ordinaryPartitionSeries_eq_geometricProduct
#check ordinaryPartitionSeries_mul_eulerProduct

#print axioms coeff_ordinaryPartitionSeries
#print axioms geometricFactor_mul_oneSub
#print axioms hasProd_ordinaryPartitionSeries_geometric
#print axioms ordinaryPartitionSeries_eq_geometricProduct
#print axioms ordinaryPartitionSeries_mul_eulerProduct

end Stage1Instances.THM_M_0510
