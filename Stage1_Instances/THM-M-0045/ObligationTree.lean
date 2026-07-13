import Statement

/-!
# THM-M-0045 conditional obligation composition

This module checks only the exact child-to-root interface. The equation package is an explicit
premise: no Schur witnesses are constructed and the historical external proof is not installed.
-/

namespace Stage1Instances.THM_M_0045.ObligationTree

/-- The exact equation-form witness package required for every matrix by the planned proof route. -/
def SchurEquationPackage : Prop :=
  forall (n : Nat) (A : Matrix (Fin n) (Fin n) Complex),
    exists U T : Matrix (Fin n) (Fin n) Complex,
      U ∈ Matrix.unitaryGroup (Fin n) Complex ∧
        Matrix.BlockTriangular T id ∧ A = U * T * star U

/-- The frozen target includes every natural matrix dimension, including zero and one. -/
def DimensionBoundary : Prop := forall n : Nat, n = 0 ∨ 0 < n

/-- The boundary premise is discharged without excluding any dimension. -/
theorem dimensionBoundary : DimensionBoundary := by
  intro n
  exact n.eq_zero_or_pos

/-- A single unitary equation witness yields the canonical triangular conjugate. -/
theorem equationWitness_implies_targetAt {n : Nat} {A U T : Matrix (Fin n) (Fin n) Complex}
    (hU : U ∈ Matrix.unitaryGroup (Fin n) Complex)
    (hT : Matrix.BlockTriangular T id) (hA : A = U * T * star U) :
    Matrix.BlockTriangular (star U * A * U) id := by
  have hleft : star U * U = 1 := Matrix.mem_unitaryGroup_iff'.mp hU
  convert hT using 1
  calc
    star U * A * U = (star U * U) * T * (star U * U) := by
      rw [hA]
      noncomm_ring
    _ = T := by rw [hleft, one_mul, mul_one]

/-- Checked root composition. Its single required child is bound and explicitly consumed. -/
theorem root_of_equationPackage (package : SchurEquationPackage)
    : Stage1Instances.THM_M_0045.SchurTriangularizationTarget := by
  intro n A
  obtain ⟨U, T, hU, hT, hA⟩ := package n A
  exact ⟨U, hU, equationWitness_implies_targetAt hU hT hA⟩

#check SchurEquationPackage
#check DimensionBoundary
#check dimensionBoundary
#check equationWitness_implies_targetAt
#check root_of_equationPackage
set_option pp.universes true in
#print SchurEquationPackage
set_option pp.universes true in
#print DimensionBoundary
set_option pp.universes true in
#print equationWitness_implies_targetAt
#print axioms equationWitness_implies_targetAt
#print axioms root_of_equationPackage

end Stage1Instances.THM_M_0045.ObligationTree
